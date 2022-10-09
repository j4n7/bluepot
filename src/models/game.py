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


base_dir = Path(__file__).parent.parent.parent
data_dir = base_dir / 'data'

with open(data_dir / 'jungle_monsters.json') as json_file:
    jungle_monsters = json.load(json_file)

with open(data_dir / 'jungle_camps.json') as json_file:
    jungle_camps = json.load(json_file)

for monster_name, monster_info in jungle_monsters.items():
    monster_info['is_dead'] = True
    monster_info['death_time'] = None
    monster_info['spawn_time'] = None
    monster_info['death_visible'] = None

for camp_name, camp_info in jungle_camps.items():
    camp_info['is_dead'] = True
    camp_info['death_time'] = None
    camp_info['spawn_time'] = None
    camp_info['timer'] = None


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

    def __init__(self, pm):
        self.pm = pm
        self.chat = Chat(pm)

        self.local_player = Entity(pm, pm.read_int(pm.base_address + Game.local_player_offset))

        self.minion_manager = EntityManager(pm, Game.minion_manager_offset)
        self.champion_manager = EntityManager(pm, Game.champion_manager_offset)
        self.tower_manager = EntityManager(pm, Game.tower_manager_offsset)

        self.object_manager = ObjectManager(pm)

        self.jungle_camps_stored = jungle_camps
        self.jungle_monsters_stored = jungle_monsters

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

    def _update_jungle_monsters(self):
        for minion in self.minion_manager.entities:
            try:
                if minion.category == 'jungle_monster':
                    if minion.name in self.jungle_monsters_stored:
                        jungle_monster = minion
                        jungle_monster_stored = self.jungle_monsters_stored[minion.name]
                        # MONSTER SPAWNED
                        if not jungle_monster.is_dead and jungle_monster_stored['is_dead']:
                            jungle_monster_stored['is_dead'] = False
                            jungle_monster_stored['spawn_time'] = self.time
                            jungle_monster_stored['death_visible'] = None
                        # MONSTER DEAD
                        elif jungle_monster.is_dead and not jungle_monster_stored['is_dead']:
                            jungle_monster_stored['is_dead'] = True
                            jungle_monster_stored['death_time'] = self.time
                            jungle_monster_stored['death_visible'] = jungle_monster.is_visible
            # ? Not sure if I need <UnicodeDecodeError> here
            except MemoryReadError or UnicodeDecodeError:
                pass

    def _update_jungle_camps(self):
        spawn_offset = timedelta(seconds=1)

        for camp_name, camp_stored_info in self.jungle_camps_stored.items():
            if camp_name != 'drake':

                # The all() function returns True if all items in an iterable are true, otherwise it returns False.
                camp_is_dead = all([self.jungle_monsters_stored[monster]['is_dead'] for monster in camp_stored_info['monsters']])
                camp_is_death_visible = all([self.jungle_monsters_stored[monster]['death_visible'] for monster in camp_stored_info['monsters']])

                # ! Fairly accurate, krugs are the most problematic
                vision_offset = timedelta(seconds=0)
                if not camp_is_death_visible:
                    vision_offset = timedelta(seconds=4)
                    if camp_name in ['krugs_blue', 'krugs_red']:
                        vision_offset = timedelta(seconds=6)

                initial_time = parse_time(camp_stored_info['initial_time'])
                respawn_time = parse_time(camp_stored_info['respawn_time'])

                initial_spawn = False
                if self.time.total_seconds() <= initial_time.total_seconds():
                    spawning_time = initial_time + spawn_offset
                else:
                    # ! A camp before its initial spawning time shouldn't reach this code
                    # ! A camp that has not spawned doesn't have a death time
                    # ! It gives an error trying to sum <None> and <timedelta>
                    try:
                        spawning_time = camp_stored_info['death_time'] + respawn_time + spawn_offset - vision_offset
                        initial_spawn = True
                    except TypeError:
                        spawning_time = initial_time + spawn_offset
                timer = spawning_time.total_seconds() - self.time.total_seconds()

                # * Monsters (threfore camps) can appear in memory before they really spawn ingame
                # * Timers needs to reach 0 for a camp to be really declared as spawned
                if not camp_is_dead and timer > 0:
                    camp_is_dead = True
                
                # CAMP SPAWNED
                if not camp_is_dead and camp_stored_info['is_dead']:
                    camp_stored_info['is_dead'] = False
                    camp_stored_info['spawn_time'] = self.time
                    camp_stored_info['death_visible'] = None
                # CAMP DEAD
                elif camp_is_dead and not camp_stored_info['is_dead']:
                    camp_stored_info['is_dead'] = True
                    camp_stored_info['death_time'] = self.time
                    camp_stored_info['death_visible'] = camp_is_death_visible

                if camp_stored_info['is_dead']:
                    if initial_spawn and not camp_is_death_visible:
                        if camp_name in ['blue_blue', 'red_blue', 'blue_red', 'red_red'] and timer > 60.0:
                            camp_stored_info['timer'] = None
                        elif camp_name in ['gromp_blue', 'wolves_blue', 'raptors_blue', 'krugs_blue',
                                           'gromp_red', 'wolves_red', 'raptors_red', 'krugs_red'] and timer > 10.0:
                            camp_stored_info['timer'] = None
                    else:
                        camp_stored_info['timer'] = timedelta(seconds=timer)
                else:
                    camp_stored_info['timer'] = None

    def update_jungle(self):
        self._update_jungle_monsters()
        self._update_jungle_camps()

    def get_jungle_camps(self):
        self.update_jungle()
        return self.jungle_camps_stored
