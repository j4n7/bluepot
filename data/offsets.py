# ·····································································

# Version 12.18
# Comment out offsets seem not to be working

# ·····································································

# GAME

game_time = 0x3136040  # Float

# ·····································································

# CHAT
chat = 0x313D350  # [<League of Legends.exe> + 0x313D350]

# CHAT ATTRIBUTES
times_open = 0x0754  # Int32 [0 = chat closed]

messages_sent_count = 0x0124  # Int32 || 0x0128 [maybe total count?]
message_sent_0 = 0x012C  # Text8Ptr [+ 0xC for next message]
message_sent_0_len = 0x0130  # Int32 [+ 0xC for next message]
# message_sent_0_xxx = 0x0134  # Int32 [+ 0xC for next message, 1 or 2 chars longer than before, why?]

message_current = 0x0734  # Text16Ptr
message_current_len = 0x0744  # Int32 || 0x0758, 0x077C

# 0x0764, 0x0768, 0x076C, 0x0770 [position of chat box]

# ·····································································

# LOCAL PLAYER
local_player = 0x313D26C  # [<League of Legends.exe> + 0x313D26C]

# LOCAL PLAYER ATTRIBUTES
# namePlayer = 0x72
# teamID = 0x0034
gold = 0x1B88  # Float
gold_max = 0x1B98  # Float

# ·····································································

# MANAGERS
minion_manager = 0x24ED788  # [<League of Legends.exe> + 0x24ED788]
champion_manager = 0x18A0014  # [<League of Legends.exe> + 0x18A0014]
tower_manager = 0x3134C94  # [<League of Legends.exe> + 0x3134C94]
# inhibitor_manager = 0x2FB6B8C
# missile_manager = 0x313D2B4

# ·····································································

# MINIMAP
minimap_hud = 0x313383C  # [<League of Legends.exe> + 0x313383C]

# MINIMAP ATTRIBUTES
minimap_hud_size_min = 0x0040  # Float
minimap_hud_size_max = 0x0044  # Float
minimap_hud_size = 0x0048  # Float: 0.75 - 1.5
minimap_hud_layer = 0x0128  # Pointer
# minimap_hud_layer_pos = 0x3C

# ·····································································

# ENTITY ATTRIBUTES
position = 0x01DC  # Vector3: x, z, y || 0x0224
is_visible = 0x0274  # Bool
mana = 0x029C  # Float
mana_max = 0x02AC  # Float
health = 0x0E74  # Float
health_max = 0x0E84  # Float
name = 0x2D5C  # Text8Ptr
name_verbose = 0x0054  # Text8Ptr [Works only in multi camp monsters and towers]
is_dead_ofuscated_n = 0x0288  # Int8: 0, 2 = alive; 1, 3 = dead
is_dead_ofuscated_1 = 0x0290  # ? sends hex to nvwgf2um.dll
is_dead_ofuscated_3 = 0x0298  # ? sends hex to nvwgf2um.dll
level = 0x353C  # Int32
recall_state = 0x0D90  # 6 = normal; 11 = herald/baron

# ·····································································

# MISCELLANEOUS
audio_manager = 0x189FF7C  # [<League of Legends.exe> + 0x189FF7C]
# 0x002C, 0x0038 [audio manager list len?]
# 0x0014, 0x0058, 0x0084 [lists]
