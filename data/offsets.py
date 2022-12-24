# ____________________________________________________________________________

# Version 12.23
# Comment out offsets with [!] seem not to be working

# ____________________________________________________________________________

# <<<GAME>>>
patch_version = '12.23'
game_time = 0x3143C44  # Float
game_version = 0x315A3B0  # Str

# ____________________________________________________________________________

# <<<CHAT>>>
chat = 0x314B094  # [<League of Legends.exe> + 0x314B094]

# CHAT ATTRIBUTES.............................................................
chat_times_open = 0x6BC  # Int32 [0 = chat closed]

chat_messages_sent_count = 0x009C  # Int32 || 0x00A0 [maybe total count?]
chat_message_sent_0 = 0x00A4  # Text8Ptr [+ 0xC for next message]
chat_message_sent_0_len = 0x00A8  # Int32 [+ 0xC for next message]
chat_message_sent_0_xxx = 0x00AC  # Int32 [+ 0xC for next message, 1 or 2 chars longer than before, why?]

chat_message_current = 0x069C  # Text16Ptr
chat_message_current_len = 0x06AC  # Int32 || 0x06D0, 0x06F4

# 0x06CC, 0x06D0, 0x06D4, 0x06D8 [Chat box dimensions?]

# ____________________________________________________________________________

# <<<MINIMAP>>>
minimap = 0x3143C88  # [<League of Legends.exe> + 0x3143C88]

# MINIMAP ATTRIBUTES..........................................................

minimap_pos = 0x0048  # Int32 [left = 65793, right = 257, maybe coords?]
minimap_size_min = 0x004C  # Float
minimap_size_max = 0x0050  # Float
minimap_size = 0x0054  # Float: 0.75 - 1.5

minimap_data = 0x015C  # Ptr
minimap_data_coord_neg_a = 0x0034  # Float
minimap_data_coord_neg_b = 0x0038  # Float
minimap_data_coord_neg_a = 0x003C  # Float
minimap_data_coord_neg_b = 0x0040  # Float
minimap_data_size_a = 0x0044  # Float || 0x004C
minimap_data_size_b = 0x0048  # Float || 0x0050

# ____________________________________________________________________________

# <<<CURSOR>>>
cursor = 0x24FB364  # [<League of Legends.exe> + 0x24FB364]

# CURSOR ATTRIBUTES...........................................................

cursor_entity_hovered = 0x000C  # Ptr
cursor_pos_in_game_res_x = 0x0038  # Int32 [0 = left side; can be negative if outside window]
cursor_pos_in_game_res_y = 0x003C  # Int32 [0 = top side; can be negative if outside window]

# ____________________________________________________________________________

# <<<LOCAL PLAYER>>>
local_player = 0x314A404  # [<League of Legends.exe> + 0x314A404]

# PLAYER ATTRIBUTES...........................................................

player_summoner_name_start = 0x0054  # Text8[len]
player_summoner_name_len = 0x0064  # Int32

player_recall_state = 0x0D90  # Int32 || 0x0D78 [6 = normal; 11 = herald/baron]
player_gold = 0x1BB0  # Float
player_gold_max = 0x1BC0  # Float

# ____________________________________________________________________________

# <<<SPECIFIC MANAGERS>>>
minion_manager = 0x24FB1E4  # [<League of Legends.exe> + 0x24FB1E4]
champion_manager = 0x18ADB74  # [<League of Legends.exe> + 0x18ADB74]
tower_manager = 0x3142824  # [<League of Legends.exe> + 0x3142824]
# inhibitor_manager = 0x314B148  # [!]

# ____________________________________________________________________________

# <<<OBJECT MANAGER>>>
object_manager = 0x18ADAD8  # [<League of Legends.exe> + 0x18ADAD8]
object_list = 0x0014  # Ptr
object_list_len = 0x002C  # Int32 || 0x0038
object_last = 0x0020  # Ptr

# Object......................................................................

# object_name = 0X0054  # Text8Ptr

# ____________________________________________________________________________

# <<<BUFF MANAGER>>>
buff_manager = 0x2338
buff_list_start = 0x0010  # Ptr
buff_list_end = 0x0014  # Ptr

# BUFF........................................................................

buff_name = 0x0008  # Ptr [Trash objects dont't have a name]
buff_start_time = 0x000C  # Float || 0x0018
buff_end_time = 0x0010  # Float

# ____________________________________________________________________________

# <<<SPELL MANAGER>>>
spell_manager = 0x29C8  # [spell_book = 0x2500; spell_book + 0x04C8 = 0x29C8]

# SPELL.......................................................................

spell_level = 0x001C  # Int32

spell_time_ready = 0x0024  # Float [Time in game seconds when the spell is going to be ready again]
spell_time_cooldown_max = 0x0074  # Float [Static number, updates after spell is casted; 0, 15 (summoner) = spell never used before]

spell_time_charge_ready = 0x0060  # Float [Time in game seconds when the charge is going to be ready again]
spell_time_charge_cooldown_max = 0x0064  # Float [Updates after spell is casted, all charges need to be used before automatically updating this value (spell haste)]

spell_charges_n = 0x0054  # Int32

spell_damage = 0x0094  # Float [Probably only makes sense in the case of Smite]
spell_is_ready = 0x00EC  # Int16 [0 = ready; 256 = cooldown, Smite can be in cooldown with 1 charge]

spell_data = 0x0120  # Ptr
spell_data_name = 0x0018  # Text8[len] or TextPtr [Not reliable]
spell_data_name_len = 0x0028  # Int32

spell_data_data = 0x0040  # Ptr
spell_data_data_name_1 = 0x006C  # Text8Ptr
spell_data_data_name_2 = 0x0090  # Text8Ptr

# spell_missile_x = 0x0108  # Float [Something related to spells that are missiles (how much they last in ms?)]

# SELL ACTIVE.................................................................

spell_active = 0x2520  # [spell_manager - 0x04A8 = 0x2520; spell_book + 0x20 = spell_active]

spell_active_data = 0x0008  # Ptr
spell_active_data_name = 0x0018  # Text8[len] or TextPtr [Not reliable]
spell_active_data_name_len = 0x0028  # Int32

spell_active_time_ready = 0x0010  # Float
spell_active_time_cooldown_max = 0x00E4  # Float

spell_active_index_source = 0x006C  # Int16
spell_active_index_target = 0x00C4  # Ptr [Read value of address as Int16]

spell_active_postion_start = 0x0088  # Vector3: x, z, y
spell_active_position_end = 0x0094  # Vector3: x, z, y
spell_active_position_end_2 = 0x00A0  # Vector3: x, z, y

spell_active_time_wind_up = 0x00D0  # Float
spell_active_time_attack_complete = 0x00E0  # Float [?]

spell_active_type = 0x00F8  # Int32 [aa = 64,65; q = 0; w = 1; e = 2; r = 3]

spell_active_mana_cost = 0x0100  # Float

# ____________________________________________________________________________

# <<<MISSILE MAANAGER>>>
missile_manager = 0x314B03C  # [<League of Legends.exe> + 0x314B03C]

# MISSILE.....................................................................

missile_data = 0x0014  # Ptr
missile_data_team = 0x0034  # Int16
missile_data_name = 0x0054  # Text8Ptr

missile_data_position_start = 0x02E0  # Vector3: x, z, y
missile_data_position_end = 0x02EC  # Vector3: x, z, y
missile_data_position_end_2 = 0x02F8  # Vector3: x, z, y
missile_data_index_source = 0x02C4  # Int16 (short) || 0X02C8 [4 digit number]
missile_data_index_target = 0x031C  # Ptr [Read value of address as Int16]

missile_data_data = 0x0260  # Ptr
missile_data_data_name = 0x0018  # Text8[len] or Text8Ptr [Pointer if aa]

missile_data_name_champ = 0x0278  # Text8[len]
missile_data_name_champ_len = 0x0288  # Int32

missile_data_type = 0x0350  # Int32 [aa = 64,65; q = 0; w = 1; e = 2; r = 3]

# ____________________________________________________________________________

# <<<ENTITY ATTRIBUTES>>>
index = 0x0008  # Int16
team = 0x0034  # Int16 [100 = Blue; 200 = Red]
name_full = 0x0054  # Text8Ptr [Works only in multi camp monsters and towers]
position = 0x01DC  # Vector3: x, z, y || 0x0224
is_visible = 0x0274  # Bool
is_dead_ofuscated_n = 0x0288  # Int8 [0, 2 = alive; 1, 3 = dead]
is_dead_ofuscated_1 = 0x0290
is_dead_ofuscated_3 = 0x0298
mana = 0x029C  # Float
mana_max = 0x02AC  # Float
health = 0x0E7C  # Float
health_max = 0x0E8C  # Float
name = 0x2DB4  # Text8Ptr || 0x3190
aa_index_target = 0x2FC4  # Int16
level = 0x35A4  # Int32

attack_spped_bonus = 0x132C  # Float [Decimal from 0 to 1]
attack_speed_bonus_multi = 0x1358  # Float [Multiplier, like 1.150]
