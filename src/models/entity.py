import json
import math
from pymem.exception import MemoryReadError
from functools import cached_property
from pathlib import Path

import data.offsets as offsets


base_dir = Path(__file__).parent.parent.parent
data_dir = base_dir / 'data'

with open(data_dir / 'jungle_monsters.json') as json_file:
    jungle_monsters = json.load(json_file)

with open(data_dir / 'jungle_camps.json') as json_file:
    jungle_camps = json.load(json_file)


class Entity:
    name_offset = offsets.name
    name_verbose_offset = offsets.name_verbose
    position_offset = offsets.position
    is_visible_offset = offsets.is_visible
    health_offset = offsets.health
    health_max_offset = offsets.health_max
    is_dead_offset = offsets.is_dead_ofuscated_n

    jungle_camps = jungle_camps
    jungle_monsters = jungle_monsters

    def __init__(self, pm, address):
        self.pm = pm
        self.address = address

    @cached_property
    def name_short(self):
        pointer = self.address + Entity.name_offset
        name_short_address = self.pm.read_int(pointer)
        name_short = self.pm.read_string(name_short_address)
        return name_short

    @cached_property
    def name_verbose(self):
        name_verbose = None
        try:
            pointer = self.address + Entity.name_verbose_offset
            name_verbose_address = self.pm.read_int(pointer)
            try:
                name_verbose = self.pm.read_string(name_verbose_address)
            except UnicodeDecodeError:
                pass
        except MemoryReadError:
            pass

        return name_verbose

    @cached_property
    def name(self):

        if self.category == 'jungle_camp_resapwn':
            for name, camp_info in Entity.jungle_camps.items():
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

            for name, monster_info in Entity.jungle_monsters.items():
                if self.name_verbose:
                    if self.name_verbose == monster_info['name_verbose']:
                        return name
                else:
                    if self.name_short == monster_info['name_short']:
                        # * Take out mini krugs that appear when killing the ancient krug
                        # * They don't have a verbose name
                        if self.name_short == 'SRU_KrugMini':
                            return 'krug_mini_child'
                        if _in_respawn_distance(self.position, monster_info['spawn_pos'], 2000):
                            return name

    @cached_property
    def category(self):
        # TODO: all plants, wards and super-minions
        if self.name_short in [monster_info['name_short'] for monster_info in Entity.jungle_monsters.values()]:
            return 'jungle_monster'
        if self.name_short == 'PreSeason_Turret_Shield':
            return 'tower_shield'
        if self.name_short == 'SRU_PlantRespawnMarker':
            return 'plant_respawn'
        if self.name_short == 'SRU_Plant_Health':
            return 'plant_health'
        if self.name_short == 'SRU_OrderMinionMelee':
            return 'minion_melee_blue'
        if self.name_short == 'SRU_OrderMinionRanged':
            return 'minion_ranged_blue'
        if self.name_short == 'SRU_OrderMinionSiege':
            return 'minion_cannon_blue'
        if self.name_short == 'SRU_ChaosMinionMelee':
            return 'minion_melee_red'
        if self.name_short == 'SRU_ChaosMinionRanged':
            return 'minion_ranged_red'
        if self.name_short == 'SRU_ChaosMinionSiege':
            return 'minion_cannon_red'
        if self.name_short == 'SRU_CampRespawnMarker':
            return 'jungle_camp_resapwn'
        if self.name_short == 'SRU_BaronSpawn':
            return 'baron_resapwn'

    @property
    def position(self):
        x = self.pm.read_float(self.address + Entity.position_offset)
        y = self.pm.read_float(self.address + Entity.position_offset + 0x8)
        z = self.pm.read_float(self.address + Entity.position_offset + 0x4)
        return {"x": x, "y": y, "z": z}

    @property
    def is_visible(self):
        is_visible = self.pm.read_bool(self.address + Entity.is_visible_offset)
        return is_visible

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

    # @property
    # def is_dead(self):
    #     return True if not self.health else False

    @property
    def is_dead(self):
        # * Superior approach
        is_dead = self.pm.read_int(self.address + Entity.is_dead_offset)
        return True if is_dead % 2 != 0 else False

    @property
    def interesting(self):
        a = self.pm.read_int(self.address + 0x00FC)  # 2 byte (0-3)
        b = self.pm.read_int(self.address + 0x0100)
        c = self.pm.read_int(self.address + 0x01B8)  # small number
        d = self.pm.read_int(self.address + 0x3C4)

        return (a, b, c, d)
