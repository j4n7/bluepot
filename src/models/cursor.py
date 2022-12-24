from src.models.entity import Entity
import data.offsets as offsets


class Cursor:
    cursor_offset = offsets.cursor
    cursor_entity_hovered_offset = offsets.cursor_entity_hovered
    cursor_pos_in_game_res_x_offset = offsets.cursor_pos_in_game_res_x
    cursor_pos_in_game_res_y_offset = offsets.cursor_pos_in_game_res_y

    def __init__(self, pm):
        self.pm = pm
        self.address = pm.read_int(pm.base_address + Cursor.cursor_offset)

    @property
    def entity_hovered(self):
        pointer = self.address + Cursor.cursor_entity_hovered_offset
        address = self.pm.read_int(pointer)

        return Entity(self.pm, address)

    @property
    def pos_in_game_res_x(self):
        return self.pm.read_int(self.address + Cursor.cursor_pos_in_game_res_x_offset)

    @property
    def pos_in_game_res_y(self):
        return self.pm.read_int(self.address + Cursor.cursor_pos_in_game_res_y_offset)
     