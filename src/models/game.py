import json
from datetime import timedelta
from pathlib import Path
from pymem.exception import MemoryReadError

from .chat import Chat
from .entity import Entity
from .entitymanager import EntityManager
from .objectmanager import ObjectManager

from src.functions import parse_time
import data.offsets as offsets


class Game:
    game_time_offset = offsets.game_time

    minimap_hud_offset = offsets.minimap_hud
    minimap_hud_layer_offset = offsets.minimap_hud_layer
    minimap_hud_size_a_offset = offsets.minimap_hud_size_a
    minimap_hud_size_b_offset = offsets.minimap_hud_size_b

    local_player_offset = offsets.local_player
    minion_manager_offset = offsets.minion_manager
    champion_manager_offset = offsets.champion_manager
    tower_manager_offsset = offsets.tower_manager

    server_tick_time = 0.033  # https://leagueoflegends.fandom.com/wiki/Tick_and_updates

    def __init__(self, pm):
        self.pm = pm
        self.chat = Chat(pm)

        self.local_player = Entity(pm, pm.read_int(pm.base_address + Game.local_player_offset))

        self.minion_manager = EntityManager(pm, Game.minion_manager_offset)
        self.champion_manager = EntityManager(pm, Game.champion_manager_offset)
        self.tower_manager = EntityManager(pm, Game.tower_manager_offsset)

        self.object_manager = ObjectManager(pm)

        self._init_jungle_monsters()
        self._init_jungle_camps()

    @property
    def time(self):
        seconds = self.pm.read_float(self.pm.base_address + Game.game_time_offset)
        return timedelta(seconds=seconds)

    @property
    def minimap_resolution(self):
        minimap_hud_address = self.pm.read_int(self.pm.base_address + Game.minimap_hud_offset)
        pointer = minimap_hud_address + Game.minimap_hud_layer_offset
        minimap_hud_layer_address = self.pm.read_int(pointer)
        minimap_hud_size_a = self.pm.read_float(minimap_hud_layer_address + Game.minimap_hud_size_a_offset)
        minimap_hud_size_b = self.pm.read_float(minimap_hud_layer_address + Game.minimap_hud_size_b_offset)

        return {'width': minimap_hud_size_a, 'height': minimap_hud_size_b}

    @property
    def jungle_monsters(self):
        for minion in self.minion_manager.entities:
            if minion.category == 'jungle_monster':
                yield minion

    @property
    def jungle_camp_respawns(self):
        for minion in self.minion_manager.entities:
            if minion.category == 'jungle_camp_resapwn':
                yield minion

    def _init_jungle_monsters(self):
        '''
        Initialize the state of jungle monsters.
        Read current monsters in memory: useful when reconnecting to a game that has already started.
        Otherwise a monster can be alive and not be accounted when dying.
        '''
        base_dir = Path(__file__).parent.parent.parent
        data_dir = base_dir / 'data'

        with open(data_dir / 'jungle_monsters.json') as json_file:
            self.jungle_monsters_stored = json.load(json_file)

        for monster_name, monster_info in self.jungle_monsters_stored.items():
            monster_info['is_dead'] = True
            monster_info['death_time'] = None
            monster_info['death_visible'] = None

        for jungle_monster in self.jungle_monsters:
            try:
                if jungle_monster.name in self.jungle_monsters_stored:
                    jungle_monster_stored = self.jungle_monsters_stored[jungle_monster.name]
                    jungle_monster_stored['is_dead'] = False
                    jungle_monster_stored['death_time'] = None
                    jungle_monster_stored['death_visible'] = None
            # ? Not sure if I need <UnicodeDecodeError> here
            except MemoryReadError or UnicodeDecodeError:
                pass

    def _init_jungle_camps(self):
        '''
        Initialize the state of jungle camps.
        In this case there is no need to read memory as next jungle update will get their real state.
        '''
        base_dir = Path(__file__).parent.parent.parent
        data_dir = base_dir / 'data'

        with open(data_dir / 'jungle_camps.json') as json_file:
            self.jungle_camps_stored = json.load(json_file)

        for camp_name, camp_info in self.jungle_camps_stored.items():
            camp_info['is_dead'] = True
            camp_info['death_time'] = None
            camp_info['death_visible'] = None
            camp_info['spawn_time'] = None
            camp_info['timer'] = None

            camp_info['initial_time'] = parse_time(camp_info['initial_time'])
            camp_info['respawn_time'] = parse_time(camp_info['respawn_time'])
            camp_info['timer_time'] = parse_time(camp_info['timer_time'])

    def _update_jungle_monsters(self):
        for jungle_monster in self.jungle_monsters:
            try:
                if jungle_monster.name in self.jungle_monsters_stored:
                    jungle_monster_stored = self.jungle_monsters_stored[jungle_monster.name]
                    # MONSTER DEAD
                    if jungle_monster.is_dead and not jungle_monster_stored['is_dead']:
                        jungle_monster_stored['is_dead'] = True
                        jungle_monster_stored['death_time'] = self.time
                        jungle_monster_stored['death_visible'] = jungle_monster.is_visible
                    # MONSTER SPAWNED
                    elif not jungle_monster.is_dead and jungle_monster_stored['is_dead']:
                        jungle_monster_stored['is_dead'] = False
                        jungle_monster_stored['death_time'] = None
                        jungle_monster_stored['death_visible'] = None
            # ? Not sure if I need <UnicodeDecodeError> here
            except MemoryReadError or UnicodeDecodeError:
                pass

    def _update_jungle_camps(self):
        '''
        Only updates camps cleared by the player or an ally while having vision.
        Updates all spawned camps.
        Scuttle Crabs are an exception, they should't be updated even though player has vision of them being killed.
        TODO: there is chance that player or an ally clears a camp without vision. Thus this method won't work.
        TODO: this could be separeted in 2 different methods.
        '''

        def get_camp_is_death_visible(camp_is_dead, jungle_monsters, camp_monsters):
            '''
            Check if player has vision of the camp being cleared.
            This should be True if player has vision of the last remaining monster being killed and not if all monsters were killed while having vision.
            '''
            if not camp_is_dead:
                return False
            camp_is_death_visible = all([jungle_monsters[monster]['death_visible'] for monster in camp_monsters])
            if camp_is_death_visible:
                return True
            else:
                # Monsters don't have a death time before first spawn
                monsters_death_time_visible = [jungle_monsters[monster]['death_time'].total_seconds() for monster in camp_monsters if jungle_monsters[monster]['death_time'] and jungle_monsters[monster]['death_visible']]
                monsters_death_time_not_visible = [jungle_monsters[monster]['death_time'].total_seconds() for monster in camp_monsters if jungle_monsters[monster]['death_time'] and not jungle_monsters[monster]['death_visible']]

                last_monster_death_time_visible = 0
                last_monster_death_time_not_visible = 0

                if monsters_death_time_visible:
                    last_monster_death_time_visible = max(monsters_death_time_visible)
                if monsters_death_time_not_visible:
                    last_monster_death_time_not_visible = max(monsters_death_time_not_visible)

                if last_monster_death_time_visible == 0 and last_monster_death_time_not_visible == 0:
                    return False
                elif last_monster_death_time_visible >= last_monster_death_time_not_visible:
                    return True
                else:
                    return False

        for camp_name, camp_stored_info in self.jungle_camps_stored.items():
            if camp_name != 'drake':
                respawn_time = camp_stored_info['respawn_time']
                # The all() function returns True if all items in an iterable are true, otherwise it returns False.
                # ! camp_is_dead can be inaccurate for monsters killed out of vision (approx. 4 seconds)
                camp_is_dead = all([self.jungle_monsters_stored[monster]['is_dead'] for monster in camp_stored_info['monsters']])
                camp_is_death_visible = get_camp_is_death_visible(camp_is_dead, self.jungle_monsters_stored, camp_stored_info['monsters'])
                # CAMP DEAD
                # * Only update jungle camps where player has vision of the camp being cleared
                if camp_name not in ['scuttle_top', 'scuttle_bottom'] and camp_is_dead and not camp_stored_info['is_dead'] and camp_is_death_visible:
                    # print('CAMP DEAD (PLAYER VISION)', camp_name, self.time)
                    camp_stored_info['is_dead'] = True
                    camp_stored_info['death_time'] = self.time
                    camp_stored_info['death_visible'] = True
                    spawn_offset = timedelta(seconds=1)  # ? Correct time disadjustment
                    camp_stored_info['spawn_time'] = camp_stored_info['death_time'] + respawn_time + spawn_offset
                # CAMP SPAWNED
                # * Update all jungle camps
                # * When a player has had vision of a respawn marker, camp_is_dead should be accurate
                elif not camp_is_dead and camp_stored_info['is_dead']:
                    initial_time = camp_stored_info['initial_time']
                    # * Camps can spawn in memory before timer reaching 0 s
                    # TODO: check if monsters are manually spawned after initial time (Practice Tool)
                    if camp_stored_info['timer'] and self.time.total_seconds() > initial_time.total_seconds() and camp_stored_info['timer'].total_seconds() > 0:
                        continue
                    # print('CAMP SPAWNED', camp_name, self.time)
                    camp_stored_info['is_dead'] = False
                    camp_stored_info['death_time'] = None
                    camp_stored_info['death_visible'] = None
                    camp_stored_info['spawn_time'] = None

    def _update_jungle_camp_respawns(self):
        '''
        Jungle camp respawn markers only appear in memory when the player or an ally has vision of them.
        This doesn't apply for Scuttle Crabs when they have 'camprespawncountdownvisible' buff, they are visible to anyone.
        Camps can be cleared by a player without vision of the respawn marker if monsters are pulled too much.
        Therefore this method is only useful for Scuttle Crabs and camps cleared by enemies.
        Krug camp respawn timer is bugged by design (RIOT).
        '''
        jungle_camp_respawns = {camp_respawn.name: camp_respawn for camp_respawn in self.jungle_camp_respawns}
        for camp_name, camp_stored_info in self.jungle_camps_stored.items():
            if camp_name != 'drake':
                # CAMP DEAD
                # ! camp_is_dead can be inaccurate for monsters killed out of vision (approx. 4 seconds)
                camp_is_dead = all([self.jungle_monsters_stored[monster]['is_dead'] for monster in camp_stored_info['monsters']])
                if camp_is_dead and camp_name in jungle_camp_respawns.keys() and not camp_stored_info['is_dead']:
                    if camp_name in ['scuttle_top', 'scuttle_bottom']:
                        camp_respawn = jungle_camp_respawns[camp_name]
                        for buff in camp_respawn.buff_manager.buffs:
                            if buff.name == 'camprespawncountdownvisible':
                                # * Death is registered only 1 minute before Scuttle respawns
                                # print('CRAB DEAD', camp_name, self.time)
                                camp_stored_info['is_dead'] = True
                                spawn_offset = timedelta(seconds=1)  # ? Correct time disadjustment
                                camp_stored_info['death_time'] = buff.end_time - camp_stored_info['respawn_time']
                                camp_stored_info['spawn_time'] = buff.end_time + spawn_offset
                                break
                    else:
                        # print('CAMP DEAD (NO PLAYER VISION)', camp_name, self.time)
                        camp_stored_info['is_dead'] = True
                        camp_respawn = jungle_camp_respawns[camp_name]
                        for buff in camp_respawn.buff_manager.buffs:
                            if buff.name == 'camprespawncountdownhidden':
                                spawn_offset = timedelta(seconds=61)  # ? Correct time disadjustment
                                camp_stored_info['death_time'] = buff.start_time
                                camp_stored_info['spawn_time'] = buff.end_time + spawn_offset
                                break

    def _update_jungle_timers(self):
        for camp_name, camp_stored_info in self.jungle_camps_stored.items():
            # BEFORE FIRST SPAWN
            if camp_stored_info['is_dead'] and not camp_stored_info['death_time']:
                spawn_offset = timedelta(seconds=1)  # ? Correct time disadjustment
                initial_time = camp_stored_info['initial_time']
                timer = initial_time.total_seconds() + spawn_offset.total_seconds() - self.time.total_seconds()
                camp_stored_info['timer'] = timedelta(seconds=timer)
            # AFTER FIRST SPAWN
            elif camp_stored_info['is_dead'] and camp_stored_info['death_time']:
                timer = camp_stored_info['spawn_time'].total_seconds() - self.time.total_seconds()
                if camp_stored_info['death_visible']:
                    camp_stored_info['timer'] = timedelta(seconds=timer)
                else:
                    if timer <= camp_stored_info['timer_time'].total_seconds() + 1:
                        camp_stored_info['timer'] = timedelta(seconds=timer)
                    else:
                        camp_stored_info['timer'] = None
            else:
                camp_stored_info['timer'] = None

    def update_jungle(self):
        '''The order of execution of these methods is non trivial.'''
        self._update_jungle_monsters()
        self._update_jungle_camps()
        self._update_jungle_camp_respawns()
        self._update_jungle_timers()

    def get_jungle_camps(self):
        self.update_jungle()
        return self.jungle_camps_stored
