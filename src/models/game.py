from datetime import timedelta

from .chat import Chat
from .entity import Entity
from .entitymanager import EntityManager


import data.offsets as offsets


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
