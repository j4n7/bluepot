import json
from datetime import timedelta
from pathlib import Path

from .chat import Chat
from .entity import Entity
from .entitymanager import EntityManager


import data.offsets as offsets


base_dir = Path(__file__).parent.parent.parent
data_dir = base_dir / 'data'

with open(data_dir / 'jungle_monsters.json') as json_file:
    jungle_monsters = json.load(json_file)

with open(data_dir / 'jungle_camps.json') as json_file:
    jungle_camps = json.load(json_file)

for monster_name, monster_info in jungle_monsters.items():
    monster_info['is_dead'] = True
    monster_info['death_time'] = '00:00'
    monster_info['spawn_time'] = ''

for camp_name, camp_info in jungle_camps.items():
    camp_info['is_dead'] = True
    camp_info['death_time'] = '00:00'
    camp_info['spawn_time'] = ''


class Game:
    game_time_offset = offsets.game_time
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

        self.jungle_camps_stored = jungle_camps
        self.jungle_monsters_stored = jungle_monsters

    @property
    def time(self):
        seconds = self.pm.read_float(self.pm.base_address + Game.game_time_offset)
        return timedelta(seconds=seconds)

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
            if minion.category == 'jungle_monster':
                if minion.name in self.jungle_monsters_stored:
                    jungle_monster = minion
                    jungle_monster_stored = self.jungle_monsters_stored[minion.name]
                    # MONSTER SPAWNED
                    if not jungle_monster.is_dead and jungle_monster_stored['is_dead']:
                        jungle_monster_stored['is_dead'] = False
                        jungle_monster_stored['spawn_time'] = self.time
                    # MONSTER DEAD
                    elif jungle_monster.is_dead and not jungle_monster_stored['is_dead']:
                        jungle_monster_stored['is_dead'] = True
                        jungle_monster_stored['death_time'] = self.time
                        jungle_monster_stored['death_visible'] = jungle_monster.is_visible

    def _update_jungle_camps(self):
        for camp_name, camp_stored_info in self.jungle_camps_stored.items():
            if camp_name != 'drake':
                # The all() function returns True if all items in an iterable are true, otherwise it returns False.
                camp_is_dead = all([self.jungle_monsters_stored[monster]['is_dead'] for monster in camp_stored_info['monsters']])
                # CAMP SPAWNED
                if not camp_is_dead and camp_stored_info['is_dead']:
                    camp_stored_info['is_dead'] = False
                    camp_stored_info['spawn_time'] = self.time
                # CAMP DEAD
                elif camp_is_dead and not camp_stored_info['is_dead']:
                    camp_is_dead_visible =  all([self.jungle_monsters_stored[monster]['death_visible'] for monster in camp_stored_info['monsters']])
                    camp_stored_info['is_dead'] = True
                    camp_stored_info['death_time'] = self.time
                    camp_stored_info['death_visible'] = camp_is_dead_visible

    def update_jungle(self):
        self._update_jungle_monsters()
        self._update_jungle_camps()
