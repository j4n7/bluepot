import json
import math
from functools import cached_property
from pathlib import Path

import src.offsets as offsets


base_dir = Path(__file__).parent.parent
src_dir = base_dir / 'src'

with open(src_dir / 'jungle_camp_respawns.json') as json_file:
    jungle_camps_resapwns = json.load(json_file)

with open(src_dir / 'jungle_monsters.json') as json_file:
    jungle_monsters = json.load(json_file)


class Entity:
    name_offset = offsets.name
    position_offset = offsets.position
    health_offset = offsets.health
    health_max_offset = offsets.health_max

    jungle_camps_resapwns = jungle_camps_resapwns
    jungle_monsters = jungle_monsters

    def __init__(self, pm, address):
        self.pm = pm
        self.address = address

    @cached_property
    def name_memory(self):
        pointer = self.address + Entity.name_offset
        name_memory_address = self.pm.read_int(pointer)
        name_memory = self.pm.read_string(name_memory_address)
        return name_memory

    @cached_property
    def name(self):

        if self.category == 'jungle_camp_resapwn':
            for name, camp_info in Entity.jungle_camps_resapwns.items():
                if self.position == camp_info['spawn_pos']:
                    return name
        elif self.category == 'jungle_monster':

            def _in_respawn_distance(position, spawn_pos, threshold):
                position = (position["x"], position["y"], position["z"])
                spawn_pos = (spawn_pos["x"], spawn_pos["y"], spawn_pos["z"])
                distance = math.dist(position, spawn_pos)
                if distance <= threshold:
                    return True
                return False

            for name, monster_info in Entity.jungle_monsters_resapwns.items():
                if _in_respawn_distance(self.position, monster_info['spawn_pos'], 2000):
                    return name

    @cached_property
    def category(self):
        # TODO: all plants, wards and super-minions
        if self.name_memory == 'PreSeason_Turret_Shield':
            return 'turret_shield'
        if self.name_memory == 'SRU_PlantRespawnMarker':
            return 'plant_respawn'
        if self.name_memory == 'SRU_Plant_Health':
            return 'plant_health'
        if self.name_memory == 'SRU_OrderMinionMelee':
            return 'minion_melee_blue'
        if self.name_memory == 'SRU_OrderMinionRanged':
            return 'minion_ranged_blue'
        if self.name_memory == 'SRU_OrderMinionSiege':
            return 'minion_cannon_blue'
        if self.name_memory == 'SRU_ChaosMinionMelee':
            return 'minion_melee_red'
        if self.name_memory == 'SRU_ChaosMinionRanged':
            return 'minion_ranged_red'
        if self.name_memory == 'SRU_ChaosMinionSiege':
            return 'minion_cannon_red'
        if self.name_memory == 'SRU_CampRespawnMarker':
            return 'jungle_camp_resapwn'
        if self.name_memory == 'SRU_BaronSpawn':
            return 'baron_resapwn'

    @property
    def position(self):
        x = self.pm.read_float(self.address + Entity.position_offset)
        y = self.pm.read_float(self.address + Entity.position_offset + 0x8)
        z = self.pm.read_float(self.address + Entity.position_offset + 0x4)
        return {"x": x, "y": y, "z": z}

    @property
    def health(self):
        health = self.pm.read_float(self.address + Entity.health_offset)
        return health

    @cached_property
    def health_max(self):
        health_max = self.pm.read_float(self.address + Entity.health_max_offset)
        return health_max

    @property
    def health_ratio(self):
        return self.health / self.health_max

    @property
    def interesting(self):
        a = self.pm.read_int(self.address + 0x00FC)  # 2 byte (0-3)
        b = self.pm.read_int(self.address + 0x0100)
        c = self.pm.read_int(self.address + 0x01B8)  # small number
        d = self.pm.read_int(self.address + 0x3C4)

        return (a, b, c, d)