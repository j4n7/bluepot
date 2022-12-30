from pymem.exception import MemoryReadError

from src.models.entity import Entity


class Manager:
    def __init__(self, pm, offset):
        self.pm = pm
        self.offset = offset
        self.address = pm.read_int(pm.base_address + self.offset)

    @property
    def entities(self):
        pointer_0_address = self.address + 0x4
        pointer_0 = self.pm.read_int(pointer_0_address)

        list_len_address = self.address + 0x8
        list_len = self.pm.read_int(list_len_address)

        for n in range(list_len):
            pointer_n = pointer_0 + 0x4 * n
            address_n = self.pm.read_int(pointer_n)
            try:
                entity = Entity(self.pm, address_n)
                yield entity
            except MemoryReadError:
                '''Prevents error when units are manually generated (Practice Tool)'''
