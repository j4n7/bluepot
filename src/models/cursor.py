from src.models.entity import Entity
import data.offsets as offsets


class Cursor:
    offset = offsets.cursor
    entity_hovered_offset = offsets.cursor_entity_hovered
    pos_x_offset = offsets.cursor_pos_x
    pos_y_offset = offsets.cursor_pos_y

    def __init__(self, pm):
        self.pm = pm
        self.address = pm.read_int(pm.base_address + Cursor.offset)

    @property
    def entity_hovered(self):
        pointer = self.address + Cursor.entity_hovered_offset
        address = self.pm.read_int(pointer)

        return Entity(self.pm, address)

    @property
    def pos_in_game_res_x(self):
        return self.pm.read_int(self.address + Cursor.pos_x_offset)

    @property
    def pos_in_game_res_y(self):
        return self.pm.read_int(self.address + Cursor.pos_y_offset)
