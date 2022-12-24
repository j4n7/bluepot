from src.models.spell import Spell
import data.offsets as offsets


class SpellManager:
    def __init__(self, pm, entity_address):
        self.pm = pm
        self.entity_address = entity_address
        self.address = entity_address + offsets.spell_manager

    @property
    def spells(self):
        key_hex = {
            'Q': 0x0,
            'W': 0x4,
            'E': 0x8,
            'R': 0xC,
            'D': 0x10,
            'F': 0x14,
        }
        for key, hex_ in key_hex.items():
            pointer = self.address + hex_
            address = self.pm.read_int(pointer)
            spell = Spell(self.pm, address, key)

            yield spell
