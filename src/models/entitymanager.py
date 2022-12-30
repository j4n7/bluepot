from pymem.exception import MemoryReadError

from src.models.entity import Entity
import data.offsets as offsets


class EntityManager:
    offset = offsets.entity_manager
    list_offset = offsets.entity_manager_list
    list_len_offset = offsets.entity_manager_list_len

    def __init__(self, pm):
        self.pm = pm
        self.address = pm.read_int(pm.base_address + EntityManager.offset)

    @property
    def entities(self):
        pointer_0_address = self.address + EntityManager.list_offset
        pointer_0 = self.pm.read_int(pointer_0_address)

        list_len_address = self.address + EntityManager.list_len_offset
        list_len = self.pm.read_int(list_len_address)

        for n in range(list_len):
            pointer_n = pointer_0 + 0x4 * n
            address_n = self.pm.read_int(pointer_n)
            try:
                entity = Entity(self.pm, address_n)
                yield entity
            except MemoryReadError:
                '''Prevents error when units are manually generated (Practice Tool)'''
