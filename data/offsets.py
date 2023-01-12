import json
import requests

from src.functions import get_base_dir, offsets_need_update, get_offset


base_dir = get_base_dir()
data_dir = base_dir / 'data'

request = requests.get('https://raw.githubusercontent.com/j4n7/bluepot/develop/data/offsets.json')
remote = request.json()

with open(data_dir / 'offsets.json') as json_file:
    local = json.load(json_file)

if offsets_need_update(remote, local):
    with open(data_dir / 'offsets.json', 'w') as json_file:
        json.dump(remote, json_file)
    offsets = remote
else:
    offsets = local

# ____________________________________________________________________________

version = offsets['version']
patch = get_offset(offsets['patch'])
game_time = get_offset(offsets['game_time'])

# ____________________________________________________________________________

# CURSOR

cursor = get_offset(offsets['cursor'][0])

cursor_entity_hovered = get_offset(offsets['cursor'][1]['entity_hovered'])
cursor_pos_x = get_offset(offsets['cursor'][1]['pos_x'])
cursor_pos_y = get_offset(offsets['cursor'][1]['pos_y'])

# ____________________________________________________________________________

# CHAT

chat = get_offset(offsets['chat'][0])

chat_times_open = get_offset(offsets['chat'][1]['times_open'])
chat_messages_sent_count = get_offset(offsets['chat'][1]['messages_sent_count'])

chat_message_sent_0 = get_offset(offsets['chat'][1]['message_sent_0'])
chat_message_sent_0_len = get_offset(offsets['chat'][1]['message_sent_0_len'])

chat_message_current = get_offset(offsets['chat'][1]['message_current'])
chat_message_current_len = get_offset(offsets['chat'][1]['message_current_len'])

# ____________________________________________________________________________

# MINIMAP

minimap = get_offset(offsets['minimap'][0])

# minimap_pos = get_offset(offsets['minimap'][1]['pos'])
# minimap_size_min = get_offset(offsets['minimap'][1]['size_min'])
# minimap_size_max = get_offset(offsets['minimap'][1]['size_max'])
# minimap_size = get_offset(offsets['minimap'][1]['size'])

minimap_data = get_offset(offsets['minimap'][1]['data'][0])
# minimap_data_coord_neg_a = get_offset(offsets['minimap'][1]['data'][1]['coord_neg_a'])
# minimap_data_coord_neg_b = get_offset(offsets['minimap'][1]['data'][1]['coord_neg_b'])
minimap_data_size_a = get_offset(offsets['minimap'][1]['data'][1]['size_a'])
minimap_data_size_b = get_offset(offsets['minimap'][1]['data'][1]['size_b'])

# ____________________________________________________________________________

# UNIT

unit_manager = get_offset(offsets['unit']['manager'])

# ____________________________________________________________________________

# TOWER

tower_manager = get_offset(offsets['tower']['manager'])

# ____________________________________________________________________________

# CHAMPION

champion_manager = get_offset(offsets['champion']['manager'])

champion_local = get_offset(offsets['champion']['local'])

champion_summoner_name = get_offset(offsets['champion']['summoner_name'])
# champion_summoner_name_len = get_offset(offsets['champion']['summoner_name_len'])

# champion_recall_state = get_offset(offsets['champion']['recall_state'])
# champion_gold = get_offset(offsets['champion']['gold'])
# champion_gold_max = get_offset(offsets['champion']['gold_max'])

# ____________________________________________________________________________

# ENTITY

entity_manager = get_offset(offsets['entity']['manager'][0])

entity_manager_list = get_offset(offsets['entity']['manager'][1]['list'])
entity_manager_list_len = get_offset(offsets['entity']['manager'][1]['list_len'])
# entity_manager_last = get_offset(offsets['entity']['manager'][1]['last'])

# entity_index = get_offset(offsets['entity']['index'])
entity_team = get_offset(offsets['entity']['team'])
entity_name_full = get_offset(offsets['entity']['name_full'])
entity_pos = get_offset(offsets['entity']['pos'])
entity_is_visible = get_offset(offsets['entity']['is_visible'])
entity_is_dead_ofuscated_n = get_offset(offsets['entity']['is_dead_ofuscated_n'])
# entity_is_dead_ofuscated_1 = get_offset(offsets['entity']['is_dead_ofuscated_1'])
# entity_is_dead_ofuscated_3 = get_offset(offsets['entity']['is_dead_ofuscated_3'])
entity_mana = get_offset(offsets['entity']['mana'])
entity_mana_max = get_offset(offsets['entity']['mana_max'])
entity_health = get_offset(offsets['entity']['health'])
entity_health_max = get_offset(offsets['entity']['health_max'])
entity_name = get_offset(offsets['entity']['name'])
# entity_aa_index_target = get_offset(offsets['entity']['aa_index_target'])
# entity_level = get_offset(offsets['entity']['level'])

# entity_attack_spped_bonus = get_offset(offsets['entity']['attack_spped_bonus'])
# entity_attack_speed_bonus_multi = get_offset(offsets['entity']['attack_speed_bonus_multi'])

# ----------------------------------------------------------------------------

# ../BUFF

entity_buff_manager = get_offset(offsets['entity']['buff']['manager'][0])
entity_buff_manager_list_start = get_offset(offsets['entity']['buff']['manager'][1]['list_start'])
entity_buff_manager_list_end = get_offset(offsets['entity']['buff']['manager'][1]['list_end'])

entity_buff_name = get_offset(offsets['entity']['buff']['name'])
entity_buff_start_time = get_offset(offsets['entity']['buff']['start_time'])
entity_buff_end_time = get_offset(offsets['entity']['buff']['end_time'])

# ----------------------------------------------------------------------------

# ../SPELL

entity_spell_book = get_offset(offsets['entity']['spell']['book'][0])

# ............................................................................

# ../../SLOTS

entity_spell_book_slots = get_offset(offsets['entity']['spell']['book'][1]['slots'][0])

entity_spell_book_slots_level = get_offset(offsets['entity']['spell']['book'][1]['slots'][1]['level'])

entity_spell_book_slots_cooldown_game_time = get_offset(offsets['entity']['spell']['book'][1]['slots'][1]['cooldown_game_time'])
entity_spell_book_slots_cooldown_max_time = get_offset(offsets['entity']['spell']['book'][1]['slots'][1]['cooldown_max_time'])

entity_spell_book_slots_charge_cooldown_game_time = get_offset(offsets['entity']['spell']['book'][1]['slots'][1]['charge_cooldown_game_time'])
entity_spell_book_slots_charge_cooldown_max_time = get_offset(offsets['entity']['spell']['book'][1]['slots'][1]['charge_cooldown_max_time'])

entity_spell_book_slots_charges_n = get_offset(offsets['entity']['spell']['book'][1]['slots'][1]['charges_n'])

entity_spell_book_slots_damage = get_offset(offsets['entity']['spell']['book'][1]['slots'][1]['damage'])
entity_spell_book_slots_is_used = get_offset(offsets['entity']['spell']['book'][1]['slots'][1]['is_used'])

entity_spell_book_slots_data = get_offset(offsets['entity']['spell']['book'][1]['slots'][1]['data'][0])
# entity_spell_book_slots_data_name = get_offset(offsets['entity']['spell']['book'][1]['slots'][1]['data'][1]['name'])
# entity_spell_book_slots_data_name_len = get_offset(offsets['entity']['spell']['book'][1]['slots'][1]['data'][1]['name_len'])

entity_spell_book_slots_data_data = get_offset(offsets['entity']['spell']['book'][1]['slots'][1]['data'][1]['data'][0])
entity_spell_book_slots_data_data_name = get_offset(offsets['entity']['spell']['book'][1]['slots'][1]['data'][1]['data'][1]['name'])

# ............................................................................

# ../../ACTIVE

# enitty_spell_book_active = get_offset(offsets['entity']['spell']['book'][1]['active'][0])

# enitty_spell_book_active_data = get_offset(offsets['entity']['spell']['book'][1]['active'][1]['data'][0])
# enitty_spell_book_active_data_name = get_offset(offsets['entity']['spell']['book'][1]['active'][1]['data'][1]['name'])
# enitty_spell_book_active_data_name_len = get_offset(offsets['entity']['spell']['book'][1]['active'][1]['data'][1]['name_len'])

# enitty_spell_book_active_cooldown_game_time = get_offset(offsets['entity']['spell']['book'][1]['active'][1]['cooldown_game_time'])
# enitty_spell_book_active_cooldown_max_time = get_offset(offsets['entity']['spell']['book'][1]['active'][1]['cooldown_max_time'])

# enitty_spell_book_active_index_source = get_offset(offsets['entity']['spell']['book'][1]['active'][1]['index_source'])
# enitty_spell_book_active_index_target = get_offset(offsets['entity']['spell']['book'][1]['active'][1]['index_target'][0])

# enitty_spell_book_active_pos_start = get_offset(offsets['entity']['spell']['book'][1]['active'][1]['pos_start'])
# enitty_spell_book_active_pos_end_1 = get_offset(offsets['entity']['spell']['book'][1]['active'][1]['pos_end_1'])
# enitty_spell_book_active_pos_end_2 = get_offset(offsets['entity']['spell']['book'][1]['active'][1]['pos_end_2'])

# enitty_spell_book_active_wind_up_time = get_offset(offsets['entity']['spell']['book'][1]['active'][1]['wind_up_time'])
# enitty_spell_book_active_attack_complete_time = get_offset(offsets['entity']['spell']['book'][1]['active'][1]['attack_complete_time'])

# enitty_spell_book_active_slot = get_offset(offsets['entity']['spell']['book'][1]['active'][1]['slot'])

# enitty_spell_book_active_mana_cost = get_offset(offsets['entity']['spell']['book'][1]['active'][1]['mana_cost'])

# ____________________________________________________________________________

# MISSILE

missile_manager = get_offset(offsets['missile']['manager'])

# missile_data = get_offset(offsets['missile']['data'][0])
# missile_data_team = get_offset(offsets['missile']['data'][1]['team'])
# missile_data_name = get_offset(offsets['missile']['data'][1]['name'])

# missile_data_pos_start = get_offset(offsets['missile']['data'][1]['pos_start'])
# missile_data_pos_end_1 = get_offset(offsets['missile']['data'][1]['pos_end_1'])
# missile_data_pos_end_2 = get_offset(offsets['missile']['data'][1]['pos_end_2'])

# missile_data_index_source = get_offset(offsets['missile']['data'][1]['index_source'])
# missile_data_index_target = get_offset(offsets['missile']['data'][1]['index_target'][0])

# missile_data_data = get_offset(offsets['missile']['data'][1]['data'][0])
# missile_data_data_name = get_offset(offsets['missile']['data'][1]['data'][1]['name'])
# missile_data_data_champion_name = get_offset(offsets['missile']['data'][1]['data'][1]['champion_name'])
# missile_data_data_champion_name_len = get_offset(offsets['missile']['data'][1]['data'][1]['champion_name_len'])
# missile_data_data_champion_slot = get_offset(offsets['missile']['data'][1]['data'][1]['slot'])
