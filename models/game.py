from datetime import timedelta

import src.offsets as offsets


class Game:
    game_time_offset = offsets.game_time

    def __init__(self, pm):
        self.pm = pm

    @property
    def time(self):
        seconds = self.pm.read_float(self.pm.base_address + Game.game_time_offset)
        return timedelta(seconds=seconds)
