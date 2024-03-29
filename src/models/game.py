import json
from threading import Thread
from datetime import timedelta
from pymem.exception import MemoryReadError

from .cursor import Cursor
from .chat import Chat
from .entity import Entity
from .manager import Manager
from .entitymanager import EntityManager

from src.functions import get_base_dir, get_game_info, get_game_stats, get_game_events, get_death_time, get_drake_death_count, parse_time
import data.offsets as offsets


class Game:
    version = offsets.version
    patch_offset = offsets.patch
    game_time_offset = offsets.game_time

    minimap_offset = offsets.minimap
    minimap_data_offset = offsets.minimap_data
    minimap_data_size_a_offset = offsets.minimap_data_size_a
    minimap_data_size_b_offset = offsets.minimap_data_size_b

    unit_manager_offset = offsets.unit_manager
    tower_manager_offsset = offsets.tower_manager
    missile_manager_offsset = offsets.missile_manager
    champion_manager_offset = offsets.champion_manager

    champion_local_offset = offsets.champion_local

    server_tick_time = 0.033  # https://leagueoflegends.fandom.com/wiki/Tick_and_updates

    def __init__(self, pm):
        self.pm = pm

        self.id, self.region = get_game_info()

        self.version = Game.version

        self.chat = Chat(pm)
        self.cursor = Cursor(pm)

        self.champion_local = Entity(pm, pm.read_int(pm.base_address + Game.champion_local_offset))

        self.unit_manager = Manager(pm, Game.unit_manager_offset)
        self.champion_manager = Manager(pm, Game.champion_manager_offset)
        self.tower_manager = Manager(pm, Game.tower_manager_offsset)
        self.missile_manager = Manager(pm, Game.missile_manager_offsset)

        self.entity_manager = EntityManager(pm)

        self.champion_local.set_spells(lambda: self.time)

        self._init_game()
        self._init_jungle_path()
        self._init_jungle_smite()
        self._init_jungle_monsters()
        self._init_jungle_camps()

        self._update()

    @property
    def events(self):
        return get_game_events()

    @property
    def patch(self):
        patch = self.pm.read_string(self.pm.base_address + Game.patch_offset)
        return patch

    @property
    def time_real(self):
        seconds = self.pm.read_float(self.pm.base_address + Game.game_time_offset)
        return timedelta(seconds=seconds)

    @property
    def time(self):
        '''Seconds from latest restart'''
        return self.time_real - self.time_start

    @property
    def time_jungle_path(self):
        if self._jungle_path_offset_time:
            return self.time + self._jungle_path_offset_time
        return self.time

    @property
    def minimap_resolution(self):
        minimap_address = self.pm.read_int(self.pm.base_address + Game.minimap_offset)
        pointer = minimap_address + Game.minimap_data_offset
        minimap_data_address = self.pm.read_int(pointer)
        minimap_data_size_a = self.pm.read_float(minimap_data_address + Game.minimap_data_size_a_offset)
        minimap_data_size_b = self.pm.read_float(minimap_data_address + Game.minimap_data_size_b_offset)

        return {'width': minimap_data_size_a, 'height': minimap_data_size_b}

    @property
    def jungle_monsters_memory(self):
        for unit in self.unit_manager.entities:
            if unit.category == 'jungle_monster':
                yield unit

    @property
    def jungle_camp_respawns(self):
        for unit in self.unit_manager.entities:
            if unit.category == 'jungle_camp_resapwn':
                yield unit

    def _init_game(self):
        self.time_start = timedelta(seconds=0)
        self.restarts = 0
        self.reset = False

    def _init_jungle_path(self):
        self._jungle_path_offset_time = None
        self._jungle_path = {}
        self._jungle_camps_stopped = []

    def _init_jungle_smite(self):
        self._smite_cooldown_game_time = None
        if hasattr(self.champion_local.spells.summoner, 'Smite'):
            self._smite_cooldown_game_time = self.champion_local.spells.summoner.Smite.cooldown_game_time
        self._smite_time_first_casted = None
        self._smite_charges_n = 1  # Smite always starts with 1 charge
        self._smite_invalid = False
        self._last_hovered_monster_name = None

    def _init_jungle_monsters(self):
        '''
        Initialize the state of jungle monsters.
        Read current monsters in memory: useful when reconnecting to a game that has already started.
        Otherwise a monster can be alive and not be accounted when dying.
        '''
        base_dir = get_base_dir()
        data_dir = base_dir / 'data'

        with open(data_dir / 'jungle_monsters.json') as json_file:
            self.jungle_monsters_stored = json.load(json_file)

        self._krugs_mini = {'blue': {'alive': [], 'dead': []}, 'red': {'alive': [], 'dead': []}}

        for monster_name, monster_info in self.jungle_monsters_stored.items():
            monster_info['is_dead'] = True
            monster_info['is_smited'] = None
            monster_info['attack_time'] = None
            monster_info['death_time'] = None
            monster_info['death_visible'] = None

        for jungle_monster in self.jungle_monsters_memory:
            try:
                if jungle_monster.name in self.jungle_monsters_stored:
                    jungle_monster_stored = self.jungle_monsters_stored[jungle_monster.name]
                    jungle_monster_stored['is_dead'] = False
                    jungle_monster_stored['is_smited'] = None
                    jungle_monster_stored['attack_time'] = None
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
        base_dir = get_base_dir()
        data_dir = base_dir / 'data'

        with open(data_dir / 'jungle_camps.json') as json_file:
            self.jungle_camps_stored = json.load(json_file)

        for camp_name, camp_info in self.jungle_camps_stored.items():
            camp_info['is_dead'] = True
            camp_info['is_smited'] = None
            camp_info['attack_time'] = None
            camp_info['death_time'] = None
            camp_info['death_visible'] = None
            camp_info['spawn_time'] = None
            camp_info['timer'] = None

            camp_info['initial_time'] = parse_time(camp_info['initial_time'])
            camp_info['respawn_time'] = parse_time(camp_info['respawn_time'])
            camp_info['timer_time'] = parse_time(camp_info['timer_time'])

    def _update_game(self):
        restarts = -1
        for message in self.chat.messages_sent:
            if '/help' in message:
                restarts += 1
        if restarts > self.restarts:
            # print('Game started', self.time_start, 'Time', self.time, 'Restarts', restarts)
            self.time_start = self.time_real
            self.reset = True
            self.reset_jungle()
        self.restarts = restarts

    def _update_jungle_smite(self):
        if hasattr(self.champion_local.spells.summoner, 'Smite'):
            # * Smite's cooldown_game_time starts around ~ 15 s (15.029, 15.033, ...) because it's on a 15 s cooldown.
            # * Smite's cooldown_game_time updates to ~ 87 s (87.251) around 1:27
            # * Smite's cooldown_game_time updates to ~ 90 s (90.056) around 1:30
            # * Smite can't be casted before 1:30 under normal situations (no monsters, cannons or champs available).
            # * Therefore, until 1:27 (~ 87.251 s), smite charges are not updated properly.

            # ! Might be useless if quickly changing hovered monster before casting Smite
            self._last_hovered_monster_name = self.cursor.entity_hovered.name if self.cursor.entity_hovered.name in self.jungle_monsters_stored else self._last_hovered_monster_name

            if self.time > timedelta(seconds=87):
                if self.champion_local.spells.summoner.Smite.charges_n != self._smite_charges_n:
                    if self.champion_local.spells.summoner.Smite.charges_n > self._smite_charges_n:
                        print('Smite increased:', 'Before', self._smite_charges_n, 'Now', self.champion_local.spells.summoner.Smite.charges_n)
                    elif self.champion_local.spells.summoner.Smite.charges_n < self._smite_charges_n:
                        if self._smite_time_first_casted and self.time - self._smite_time_first_casted < cooldown_game_time(seconds=90):
                            # SMITE INVALID
                            print('INVALID SMITE')
                            self._smite_invalid = True
                        else:
                            monster_name = self._last_hovered_monster_name
                            if monster_name:
                                print('Smite casted:', monster_name, 'Before', self._smite_charges_n, 'Now', self.champion_local.spells.summoner.Smite.charges_n)
                                self._smite_time_first_casted = self.time if not self._smite_time_first_casted else self._smite_time_first_casted
                                self.jungle_monsters_stored[monster_name]['is_smited'] = True
                    self._smite_charges_n = self.champion_local.spells.summoner.Smite.charges_n
            else:
                cooldown_game_time = self.champion_local.spells.summoner.Smite.cooldown_game_time
                if cooldown_game_time != self._smite_cooldown_game_time:
                    if self._smite_time_first_casted and self.time - self._smite_time_first_casted < timedelta(seconds=90):
                        # SMITE INVALID
                        print('INVALID SMITE (< 1:30)')
                        self._smite_invalid = True
                    else:
                        monster_name = self._last_hovered_monster_name
                        if monster_name:
                            print('Smite casted (< 1:30):', monster_name, 'Before', self._smite_cooldown_game_time, 'Now', cooldown_game_time)
                            self._smite_time_first_casted = self.time if not self._smite_time_first_casted else self._smite_time_first_casted
                            self.jungle_monsters_stored[monster_name]['is_smited'] = True  
                    self._smite_cooldown_game_time = cooldown_game_time                

    def _update_jungle_monsters(self):
        for jungle_monster in self.jungle_monsters_memory:
            try:
                if jungle_monster.name in self.jungle_monsters_stored:
                    jungle_monster_stored = self.jungle_monsters_stored[jungle_monster.name]

                    if jungle_monster.is_dead:
                        # MONSTER DEAD

                        # UPDATE MINI KRUGS
                        if jungle_monster.name in ['krug_mini_blue', 'krug_mini_red']:
                            color = jungle_monster.name.split('_')[2]
                            if jungle_monster.address in self._krugs_mini[color]['alive']:
                                self._krugs_mini[color]['alive'].remove(jungle_monster.address)
                                self._krugs_mini[color]['dead'].append(jungle_monster.address)

                        if not jungle_monster_stored['is_dead']:
                            jungle_monster_stored['is_dead'] = True
                            jungle_monster_stored['death_time'] = self.time
                            jungle_monster_stored['death_visible'] = jungle_monster.is_visible

                    elif not jungle_monster.is_dead:
                        # MONSTER SPAWNED

                        # UPDATE MINI KRUGS
                        if jungle_monster.name in ['krug_mini_blue', 'krug_mini_red']:
                            color = jungle_monster.name.split('_')[2]
                            if jungle_monster.address not in self._krugs_mini[color]['alive']:
                                self._krugs_mini[color]['alive'].append(jungle_monster.address)

                        if jungle_monster_stored['is_dead']:
                            jungle_monster_stored['is_dead'] = False
                            jungle_monster_stored['is_smited'] = None
                            jungle_monster_stored['attack_time'] = None
                            jungle_monster_stored['death_time'] = None
                            jungle_monster_stored['death_visible'] = None

                            # RESET MINI KRUGS
                            if jungle_monster.name in ['ancient_krug_blue', 'ancient_krug_red']:
                                color = jungle_monster.name.split('_')[2]
                                self._krugs_mini[color] = {'alive': [], 'dead': []}

                        # MONSTER ATTACKED
                        # ! Not working when monster is attacked out of vision
                        elif not jungle_monster_stored['is_dead'] and not jungle_monster_stored['attack_time'] and jungle_monster.has_been_attacked(self.time):
                            # print('MONSTER ATTACKED', jungle_monster.name, self.time)
                            jungle_monster_stored['attack_time'] = self.time                               

            # ? Not sure if I need <UnicodeDecodeError> here
            except MemoryReadError or UnicodeDecodeError:
                pass

    def _update_jungle_epic_camps(self):
        # ? Using troys (spawn and death sounds) can perhaps make this method more accurate
        for camp_name, camp_stored_info in self.jungle_camps_stored.items():
            if camp_name in ['drake', 'herald', 'baron']:
                if camp_name == 'drake':
                    camp_is_dead = all([monster_stored_info['is_dead'] for monster_name, monster_stored_info in self.jungle_monsters_stored.items() if monster_name.startswith('drake')])
                else:
                    camp_is_dead = self.jungle_monsters_stored[camp_name]['is_dead']
                # CAMP DEAD
                if camp_is_dead and not camp_stored_info['is_dead']:
                    # print('CAMP DEAD', camp_name, self.time)
                    spawn_offset = timedelta(seconds=1)  # ? Correct time disadjustment
                    if camp_name == 'drake':
                        drake_death_count = get_drake_death_count()
                        if drake_death_count['blue'] >= 4 or drake_death_count['red'] >= 4:
                            spawn_offset = timedelta(seconds=61)  # * Elder dragon
                    death_time = get_death_time(camp_name)
                    respawn_time = camp_stored_info['respawn_time']
                    spawn_time = death_time + respawn_time + spawn_offset
                    camp_stored_info['is_dead'] = True
                    camp_stored_info['death_time'] = death_time
                    camp_stored_info['death_visible'] = None
                    camp_stored_info['spawn_time'] = spawn_time
                # CAMP SPAWNED
                elif not camp_is_dead and camp_stored_info['is_dead']:
                    # print('CAMP SPAWNED', camp_name, self.time)
                    initial_time = camp_stored_info['initial_time']
                    threshold = 10
                    # * Camps can spawn in memory before timer reaching 0 s (around 7 s before they should)
                    # * Camps manually spawned within threshold time will have to wait to be accounted (Practice Tool)
                    if (
                        camp_stored_info['timer']
                        and self.time.total_seconds() > initial_time.total_seconds()
                        and camp_stored_info['timer'].total_seconds() < threshold
                        and camp_stored_info['timer'].total_seconds() > 0
                       ):
                        continue
                    camp_stored_info['is_dead'] = False
                    camp_stored_info['death_time'] = None
                    camp_stored_info['death_visible'] = None
                    camp_stored_info['spawn_time'] = None

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
                monsters_death_time_visible = [jungle_monsters[monster]['death_time'].total_seconds() for monster in camp_monsters if (jungle_monsters[monster]['death_time'] 
                                                                                                                                       and jungle_monsters[monster]['death_visible'])]
                monsters_death_time_not_visible = [jungle_monsters[monster]['death_time'].total_seconds() for monster in camp_monsters if (jungle_monsters[monster]['death_time']
                                                                                                                                           and not jungle_monsters[monster]['death_visible'])]

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
            if camp_name not in ['drake', 'herald', 'baron']:
                respawn_time = camp_stored_info['respawn_time']
                # The all() function returns True if all items in an iterable are true, otherwise it returns False.
                # ! camp_is_dead can be inaccurate for monsters killed out of vision (approx. 4 seconds)
                camp_is_dead = all([self.jungle_monsters_stored[monster]['is_dead'] for monster in camp_stored_info['monsters']])
                camp_is_death_visible = get_camp_is_death_visible(camp_is_dead, self.jungle_monsters_stored, camp_stored_info['monsters'])

                if camp_name in ['krugs_blue', 'krugs_red']:
                    color = camp_name.split('_')[1]
                    if len(self._krugs_mini[color]['dead']) < 6:
                        camp_is_dead = False
                        camp_is_death_visible = False

                # CAMP SMITED
                if hasattr(self.champion_local.spells.summoner, 'Smite'):
                    camp_is_smited = True if True in [self.jungle_monsters_stored[monster]['is_smited'] for monster in camp_stored_info['monsters']] else False
                    if camp_is_smited and not camp_stored_info['is_smited']:
                        # print('CAMP SMITED', camp_name)
                        camp_stored_info['is_smited'] = True                         

                # CAMP DEAD
                # * Only update jungle camps where player has vision of the camp being cleared
                if (
                    camp_name not in ['scuttle_top', 'scuttle_bottom']
                    and camp_is_dead
                    and not camp_stored_info['is_dead']
                    and camp_is_death_visible
                   ):
                    # print('CAMP DEAD (PLAYER VISION)', camp_name, self.time)
                    camp_stored_info['is_dead'] = True
                    camp_stored_info['death_time'] = self.time
                    camp_stored_info['death_visible'] = True
                    spawn_offset = timedelta(seconds=1)  # ? Correct time disadjustment
                    camp_stored_info['spawn_time'] = camp_stored_info['death_time'] + respawn_time + spawn_offset
                elif not camp_is_dead:
                    # CAMP SPAWNED
                    # * Update all jungle camps
                    # * When a player has had vision of a respawn marker, camp_is_dead should be accurate
                    if camp_stored_info['is_dead']:
                        initial_time = camp_stored_info['initial_time']
                        threshold = 10
                        if (
                            camp_stored_info['timer']
                            and self.time.total_seconds() > initial_time.total_seconds()
                            and camp_stored_info['timer'].total_seconds() < threshold
                            and camp_stored_info['timer'].total_seconds() > 0
                        ):
                            continue
                        # print('CAMP SPAWNED', camp_name, self.time)
                        camp_stored_info['is_dead'] = False
                        camp_stored_info['is_smited'] = None
                        camp_stored_info['attack_time'] = None
                        camp_stored_info['death_time'] = None
                        camp_stored_info['death_visible'] = None
                        camp_stored_info['spawn_time'] = None
                    # CAMP ATTACKED
                    elif not camp_stored_info['is_dead'] and not camp_stored_info['attack_time']:
                        camp_attack_times = [self.jungle_monsters_stored[monster]['attack_time'] for monster in camp_stored_info['monsters'] if self.jungle_monsters_stored[monster]['attack_time']]
                        if camp_attack_times:
                            camp_attack_time = None
                            for attack_time in camp_attack_times:
                                if not camp_attack_time or (attack_time.total_seconds() < camp_attack_time.total_seconds()):
                                    camp_attack_time = attack_time
                            camp_stored_info['attack_time'] = camp_attack_time

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
            if camp_name not in ['drake', 'herald', 'baron']:
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
        # ! Timers for epic monsters are a bit off
        # ! They also disapear before reaching 0 s during first spawn
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
                if camp_stored_info['death_visible'] or camp_name in ['drake', 'herald', 'baron']:
                    camp_stored_info['timer'] = timedelta(seconds=timer)
                else:
                    if timer <= camp_stored_info['timer_time'].total_seconds() + 1:
                        camp_stored_info['timer'] = timedelta(seconds=timer)
                    else:
                        camp_stored_info['timer'] = None
            else:
                camp_stored_info['timer'] = None

    def _update_jungle_path(self):
        camps_untracked = ['scuttle_top', 'scuttle_bottom', 'drake', 'herald', 'baron']

        camp_times = {camp: [info['attack_time'], info['death_time']] for camp, info in self.jungle_camps_stored.items() if info['attack_time'] and camp not in camps_untracked}
        camp_times = dict(sorted(camp_times.items(), key=lambda item: item[1][0].total_seconds()))

        if camp_times and not self._jungle_path_offset_time:
            camp_name = list(camp_times.keys())[0]
            offset_start = self.jungle_camps_stored[camp_name]['initial_time']
            path_start_time = camp_times[camp_name][0]
            self._jungle_path_offset_time = offset_start - path_start_time

        last_step_name = list(self._jungle_path)[-1] if self._jungle_path else None

        for camp, info in camp_times.items():
    
            if camp not in self._jungle_path and info[0]:

                # SET PATH START TIME
                if not self._jungle_path:
                    self.offset_start = self.jungle_camps_stored[camp]['initial_time']  # * Take into account the initial spawning time of the first camp being attacked
                    self.path_start = info[0]

                # SET CAMP START TIME
                self._jungle_path[camp] = {'name': '', 'color': '', 'is_smited': None, 'start': info[0] - self.path_start + self.offset_start, 'end': None, 'total': None}

                # SET MOVING STOP TIME
                if last_step_name and 'moving' in last_step_name:
                    self._jungle_path[last_step_name]['end'] = info[0] - self.path_start + self.offset_start
                    self._jungle_path[last_step_name]['total'] = self._jungle_path[last_step_name]['end'] - self._jungle_path[last_step_name]['start']

            elif camp in self._jungle_path and not self._jungle_path[camp]['end']:
                # CAMP DEAD
                if info[1]:
                    self._jungle_path[camp]['end'] = info[1] - self.path_start + self.offset_start
                    self._jungle_path[camp]['total'] = self._jungle_path[camp]['end'] - self._jungle_path[camp]['start']
                # CAMP MANUALLY STOPPED
                else:
                    if camp in self._jungle_camps_stopped:
                        self._jungle_path[last_step_name]['end'] = self.time - self.path_start + self.offset_start
                        self._jungle_path[camp]['total'] = self._jungle_path[camp]['end'] - self._jungle_path[camp]['start']

                # CAMP SMITED
                if self.jungle_camps_stored[camp]['is_smited']:
                    # print('CAMP SMITED ADDED', camp, self.time)
                    self._jungle_path[camp]['is_smited'] = True

        camps_cleared = True
        for step_name, step_info in self._jungle_path.items():
            if not step_info['end']:
                camps_cleared = False

        n_camp_steps = len([step_name for step_name, step_info in self._jungle_path.items() if 'moving' not in step_name])

        if camps_cleared and n_camp_steps < 6 and last_step_name and 'moving' not in last_step_name:
            n_moving_steps = len([step_name for step_name, step_info in self._jungle_path.items() if 'moving' in step_name])
            death_times = [step_info['end'] for step_name, step_info in self._jungle_path.items()]
            try:
                last_death_time = sorted(death_times, key=lambda time: time.total_seconds())[-1]
                self._jungle_path[f'moving_{n_moving_steps + 1}'] = {'name': 'Moving', 'color': '', 'is_smited': None, 'start': last_death_time, 'end': None, 'total': None}
            except IndexError:
                '''Takes place when restarting game (Practice Tool)'''

    def _update_jungle(self):
        '''The order of execution of these methods is non trivial.'''
        # self._update_jungle_smite()
        self._update_jungle_monsters()
        # self._update_jungle_epic_camps()
        self._update_jungle_camps()  # ! S13: needs an update to correctly determine if player has vision
        # self._update_jungle_camp_respawns()  # ! S13: interferes with Krug camp timing (mini Krugs)
        # self._update_jungle_timers()  #  ! S13: not working till other methods are fixed
        self._update_jungle_path()

    def _update(self):
        '''Main loop'''
        def update():
            while True:
                try:
                    self._update_game()
                    self._update_jungle()
                except (MemoryReadError, UnicodeDecodeError):
                    '''Ignore memory errors'''

        thread = Thread(target=update, daemon=True)
        thread.start()

    def reset_jungle(self):
        '''Can be called from outside (e.g. overlay)'''
        # self._init_jungle_smite()
        self._init_jungle_monsters()
        self._init_jungle_camps()
        self._init_jungle_path()
