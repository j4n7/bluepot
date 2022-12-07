import json
import math
from pymem.exception import MemoryReadError
from functools import cached_property
from pathlib import Path

from src.models.buffmanager import BuffManager
import data.offsets as offsets


base_dir = Path(__file__).parent.parent.parent
data_dir = base_dir / 'data'

with open(data_dir / 'jungle_monsters.json') as json_file:
    jungle_monsters = json.load(json_file)

with open(data_dir / 'jungle_camps.json') as json_file:
    jungle_camps = json.load(json_file)


class Entity:
    name_offset = offsets.name
    name_full_offset = offsets.name_full
    position_offset = offsets.position
    is_visible_offset = offsets.is_visible
    mana_offset = offsets.mana
    mana_max_offset = offsets.mana_max
    health_offset = offsets.health
    health_max_offset = offsets.health_max
    is_dead_offset = offsets.is_dead_ofuscated_n

    jungle_camps = jungle_camps
    jungle_monsters = jungle_monsters

    jungle_buffs = [
        # NON EPIC CAMPS & HERALD
        'junglebotsoftretreat',
        'junglebotfullretreat',
        'junglefrustration',
        'junglefrustrationrestoring',
        # KRUGS MINI
        'Stun',
        # SCUTTLE
        'Sru_CrabDash',
        # HERALD
        'resistantskinminibaron',
        'minibaronvulnerable',
        'HeraldLeapAttack',
        # DRAKES & ELDER DRAKE
        'resistantskindragon',
        # DRAKES
        's5_dragonvengeance',
        # BARON
        'resistantskin',
        'BaronCorruption',
    ]

    def __init__(self, pm, address):
        self.pm = pm
        self.address = address

    @cached_property
    def buff_manager(self):
        return BuffManager(self.pm, self.address)

    @cached_property
    def name_memory(self):
        name_memory = None
        try:
            pointer = self.address + Entity.name_offset
            name_memory_address = self.pm.read_int(pointer)
            try:
                name_memory = self.pm.read_string(name_memory_address)
            except UnicodeDecodeError:
                pass
        except MemoryReadError:
            '''Entity from object manager'''
        return name_memory

    @cached_property
    def name_memory_full(self):
        name_memory_full = None
        try:
            pointer = self.address + Entity.name_full_offset
            name_memory_full_address = self.pm.read_int(pointer)
            try:
                name_memory_full = self.pm.read_string(name_memory_full_address)
            except UnicodeDecodeError:
                pass
        except MemoryReadError:
            pass

        return name_memory_full

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
                if self.name_memory_full:
                    if self.name_memory_full == monster_info['name_memory_full']:
                        return name
                else:
                    if self.name_memory == monster_info['name_memory']:
                        if _in_respawn_distance(self.position, monster_info['spawn_pos'], 2000):
                            return name
        elif self.category == 'champion':
            return self.name_memory

    @cached_property
    def category(self):
        # TODO: all plants, wards and super-minions
        if self.name_memory in [monster_info['name_memory'] for monster_info in Entity.jungle_monsters.values()]:
            return 'jungle_monster'
        elif self.name_memory == 'PreSeason_Turret_Shield':
            return 'tower_shield'
        elif self.name_memory == 'SRU_PlantRespawnMarker':
            return 'plant_respawn'
        elif self.name_memory == 'SRU_Plant_Health':
            return 'plant_health'
        elif self.name_memory == 'SRU_OrderMinionMelee':
            return 'minion_melee_blue'
        elif self.name_memory == 'SRU_OrderMinionRanged':
            return 'minion_ranged_blue'
        elif self.name_memory == 'SRU_OrderMinionSiege':
            return 'minion_cannon_blue'
        elif self.name_memory == 'SRU_ChaosMinionMelee':
            return 'minion_melee_red'
        elif self.name_memory == 'SRU_ChaosMinionRanged':
            return 'minion_ranged_red'
        elif self.name_memory == 'SRU_ChaosMinionSiege':
            return 'minion_cannon_red'
        elif self.name_memory == 'SRU_CampRespawnMarker':
            return 'jungle_camp_resapwn'
        elif self.name_memory == 'SRU_BaronSpawn':
            return 'baron_resapwn'
        else:
            return 'champion'

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
    def mana(self):
        mana = self.pm.read_float(self.address + Entity.mana_offset)
        return mana

    @cached_property
    def mana_max(self):
        mana_max = self.pm.read_float(self.address + Entity.mana_max_offset)
        return mana_max

    @property
    def mana_ratio(self):
        return self.mana / self.mana_max

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
    def has_been_attacked(self):
        if self.health_ratio != 1:
            return True
        for buff in self.buff_manager.buffs:
            if buff.name not in Entity.jungle_buffs:
                return True
        return False
