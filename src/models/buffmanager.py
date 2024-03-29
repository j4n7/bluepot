from src.models.buff import Buff
import data.offsets as offsets


class BuffManager:
    offset = offsets.entity_buff_manager
    list_start_offset = offsets.entity_buff_manager_list_start
    list_end_offset = offsets.entity_buff_manager_list_end
    name_offset = offsets.entity_buff_name

    def __init__(self, pm, entity_address):
        self.pm = pm
        self.entity_address = entity_address
        self.address = entity_address + BuffManager.offset

    @property
    def buffs(self):
        pointer_0_address = self.address + BuffManager.list_start_offset
        pointer_0 = self.pm.read_int(pointer_0_address)

        pointer_last_address = self.address + BuffManager.list_end_offset
        pointer_last = self.pm.read_int(pointer_last_address)

        pointer_n = pointer_0
        while pointer_n < pointer_last:
            address_n = self.pm.read_int(pointer_n)
            pointer_n += 0x8

            pointer_name = address_n + BuffManager.name_offset
            address_name = self.pm.read_int(pointer_name)

            if address_name:
                address_name += 0x4
                name = self.pm.read_string(address_name)
                if not name.startswith('ASSETS'):
                    buff = Buff(self.pm, address_n, name)

                    yield buff
