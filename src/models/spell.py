from datetime import timedelta

import data.offsets as offsets


class Spell:
    level_offset = offsets.spell_level

    time_ready_offset = offsets.spell_time_ready
    time_cooldown_max_offset = offsets.spell_time_cooldown_max

    time_charge_ready_offset = offsets.spell_time_charge_ready
    time_charge_cooldown_max_offset = offsets.spell_time_charge_cooldown_max

    charges_n_offset = offsets.spell_charges_n

    damage_offset = offsets.spell_damage
    is_ready_offset = offsets.spell_is_ready

    data_offset = offsets.spell_data
    data_data_offset = offsets.spell_data_data
    data_data_name_offset = offsets.spell_data_data_name_1

    def __init__(self, pm, address, key):
        self.pm = pm
        self.address = address
        self.key = key

        # self.update_time_ready()
        # self.update_charges_n()

    def _game_time(self):
        '''Meant to be overwritten during instantiation'''

    @property
    def level(self):
        level = self.pm.read_int(self.address + Spell.level_offset)
        return level

    @property
    def time_ready(self):
        '''
        If Auto-Refresh Cooldowns is turned on in Practice Tool this keeps perpetually updating.
        Increasing summoner spell haste doesn't seem to immediately affect this, e.g. buying Ionian Boots of Lucidity.
        '''
        seconds = self.pm.read_float(self.address + Spell.time_ready_offset)
        return timedelta(seconds=seconds)

    @property
    def time_cooldown_max(self):
        seconds = self.pm.read_float(self.address + Spell.time_cooldown_max_offset)
        return timedelta(seconds=seconds)

    @property
    def time_cooldown(self):
        '''Current cooldown time of spell'''
        if self.time_ready.total_seconds() - self._game_time().total_seconds() >= 0:
            return self.time_ready - self._game_time()
        return timedelta(seconds=0)

    @property
    def time_cooldown_ratio(self):
        # ! Division by zero. Do we need this?
        return self.time_cooldown / self.time_cooldown_max

    @property
    def time_charge_ready(self):
        seconds = self.pm.read_float(self.address + Spell.time_charge_ready_offset)
        return timedelta(seconds=seconds)

    @property
    def time_charge_cooldown_max(self):
        seconds = self.pm.read_float(self.address + Spell.time_charge_cooldown_max_offset)
        return timedelta(seconds=seconds)

    @property
    def time_charge_cooldown(self):
        '''Current cooldown time of charge'''
        if self.time_charge_ready.total_seconds() - self._game_time().total_seconds() >= 0:
            return self.time_charge_ready - self._game_time()
        return timedelta(seconds=0)

    @property
    def time_charge_cooldown_ratio(self):
        # ! Division by zero. Do we need this?
        return self.time_charge_cooldown / self.time_charge_cooldown_max  

    @property
    def charges_n(self):
        charges_n = self.pm.read_int(self.address + Spell.charges_n_offset)
        return charges_n

    @property
    def damage(self):
        damage = self.pm.read_float(self.address + Spell.damage_offset)
        return damage

    @property
    def is_ready(self):
        is_ready = self.pm.read_int(self.address + Spell.is_ready_offset)
        return is_ready

    @property
    def name(self):
        info = self.pm.read_int(self.address + Spell.data_offset)
        data = self.pm.read_int(info + Spell.data_data_offset)
        pointer = self.pm.read_int(data + Spell.data_data_name_offset)
        name = self.pm.read_string(pointer)
        return name

    @property
    def is_summoner(self):
        if self.name.startswith('Summoner'):
            return True
        return False

    # @property
    # def is_casted(self):
    #     '''
    #     Produces errors if Auto-Refresh Cooldowns is turned on in Practice Tool.
    #     Can bring a wrong result if it is just turned on once as time_ready_now
    #     will be different than time_ready_last.
    #     '''
    #     time_ready_now = self.time_ready
    #     if time_ready_now != self.time_ready_last:
    #         self.time_ready_last = time_ready_now
    #         return True
    #     return False

    # @property
    # def is_charge_casted(self):
    #     if self.charges_n < self.charges_n_last:
    #         self.charges_n_last = self.charges_n
    #         return True
    #     return False

    # def update_time_ready(self):
    #     self.time_ready_last = self.time_ready

    # def update_charges_n(self):
    #     self.charges_n_last = self.charges_n
