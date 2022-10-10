from datetime import timedelta
from functools import cached_property

import data.offsets as offsets


class Buff:
    name_offset = offsets.buff_name
    start_time_offset = offsets.buff_start_time
    end_time_offset = offsets.buff_end_time

    def __init__(self, pm, address, name):
        self.pm = pm
        self.address = address
        self.name = name

    @cached_property
    def start_time(self):
        seconds = self.pm.read_float(self.address + Buff.start_time_offset)
        return timedelta(seconds=seconds)

    @cached_property
    def end_time(self):
        seconds = self.pm.read_float(self.address + Buff.end_time_offset)
        return timedelta(seconds=seconds)

    @cached_property
    def duration(self):
        return self.end_time - self.start_time
