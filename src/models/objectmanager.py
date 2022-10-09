from pymem.exception import MemoryReadError

from src.models.entity import Entity
from data.offsets import object_manager, object_list, object_len


class ObjectManager:
    def __init__(self, pm):
        self.pm = pm
        self.address = pm.read_int(pm.base_address + object_manager)

    @property
    def entities(self):
        pointer_0_address = self.address + object_list
        pointer_0 = self.pm.read_int(pointer_0_address)

        list_len_address = self.address + object_len
        list_len = self.pm.read_int(list_len_address)

        for n in range(list_len):
            pointer_n = pointer_0 + 0x4 * n
            address_n = self.pm.read_int(pointer_n)
            try:
                entity = Entity(self.pm, address_n)
                yield entity
            except MemoryReadError:
                '''Prevents error when minions are manually generated in practice tool'''
