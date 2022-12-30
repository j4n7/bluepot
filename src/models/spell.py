from datetime import timedelta

import data.offsets as offsets


class Spell:
    level_offset = offsets.entity_spell_book_slots_level

    cooldown_game_time_offset = offsets.entity_spell_book_slots_cooldown_game_time
    cooldown_max_time_offset = offsets.entity_spell_book_slots_cooldown_max_time

    charge_cooldown_game_time_offset = offsets.entity_spell_book_slots_charge_cooldown_game_time
    charge_cooldown_max_time_offset = offsets.entity_spell_book_slots_charge_cooldown_max_time

    charges_n_offset = offsets.entity_spell_book_slots_charges_n

    damage_offset = offsets.entity_spell_book_slots_damage
    is_ready_offset = offsets.entity_spell_book_slots_is_ready

    data_offset = offsets.entity_spell_book_slots_data
    data_data_offset = offsets.entity_spell_book_slots_data_data
    data_data_name_offset = offsets.entity_spell_book_slots_data_data_name_1

    def __init__(self, pm, address, key):
        self.pm = pm
        self.address = address
        self.key = key

        # self.update_cooldown_game_time()
        # self.update_charges_n()

    def _game_time(self):
        '''Meant to be overwritten during instantiation'''

    @property
    def level(self):
        level = self.pm.read_int(self.address + Spell.level_offset)
        return level

    @property
    def cooldown_game_time(self):
        '''
        If Auto-Refresh Cooldowns is turned on in Practice Tool this keeps perpetually updating.
        Increasing summoner spell haste doesn't seem to immediately affect this, e.g. buying Ionian Boots of Lucidity.
        '''
        seconds = self.pm.read_float(self.address + Spell.cooldown_game_time_offset)
        return timedelta(seconds=seconds)

    @property
    def cooldown_max_time(self):
        seconds = self.pm.read_float(self.address + Spell.cooldown_max_time_offset)
        return timedelta(seconds=seconds)

    @property
    def cooldown_time(self):
        '''Current cooldown time of spell'''
        if self.cooldown_game_time.total_seconds() - self._game_time().total_seconds() >= 0:
            return self.cooldown_game_time - self._game_time()
        return timedelta(seconds=0)

    @property
    def cooldown_time_ratio(self):
        # ! Division by zero. Do we need this?
        return self.cooldown_time / self.cooldown_max_time

    @property
    def charge_cooldown_game_time(self):
        seconds = self.pm.read_float(self.address + Spell.charge_cooldown_game_time_offset)
        return timedelta(seconds=seconds)

    @property
    def charge_cooldown_max_time(self):
        seconds = self.pm.read_float(self.address + Spell.charge_cooldown_max_time_offset)
        return timedelta(seconds=seconds)

    @property
    def charge_cooldown_time(self):
        '''Current cooldown time of charge'''
        if self.charge_cooldown_game_time.total_seconds() - self._game_time().total_seconds() >= 0:
            return self.charge_cooldown_game_time - self._game_time()
        return timedelta(seconds=0)

    @property
    def charge_cooldown_time_ratio(self):
        # ! Division by zero. Do we need this?
        return self.charge_cooldown_time / self.charge_cooldown_max_time

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
        data = self.pm.read_int(self.address + Spell.data_offset)
        data_data = self.pm.read_int(data + Spell.data_data_offset)
        pointer = self.pm.read_int(data_data + Spell.data_data_name_offset)
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
    #     Can bring a wrong result if it is just turned on once as _cooldown_game_time_now
    #     will be different than _cooldown_game_time_last.
    #     '''
    #     _cooldown_game_time_now = self.cooldown_game_time
    #     if _cooldown_game_time_now != self._cooldown_game_time_last:
    #         self._cooldown_game_time_last = _cooldown_game_time_now
    #         return True
    #     return False

    # @property
    # def is_charge_casted(self):
    #     if self.charges_n < self._charges_n_last:
    #         self._charges_n_last = self.charges_n
    #         return True
    #     return False

    # def update_cooldown_game_time(self):
    #     self._cooldown_game_time_last = self.cooldown_game_time

    # def update_charges_n(self):
    #     self._charges_n_last = self.charges_n
