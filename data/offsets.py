# ·····································································

# Version 12.19
# Comment out offsets with [!] seem not to be working

# ·····································································

# GAME

game_time = 0x3134810  # Float

# ·····································································

# CHAT
chat = 0x313AE7C  # [<League of Legends.exe> + 0x313AE7C]

# CHAT ATTRIBUTES
times_open = 0x0754  # Int32 [0 = chat closed]

messages_sent_count = 0x00AC  # Int32 || 0x00B0 [maybe total count?]
message_sent_0 = 0x00B4  # Text8Ptr [+ 0xC for next message]
message_sent_0_len = 0x00B8  # Int32 [+ 0xC for next message]
# message_sent_0_xxx = 0x00BC  # Int32 [+ 0xC for next message, 1 or 2 chars longer than before, why?]

message_current = 0x06AC  # Text16Ptr
message_current_len = 0x06BC  # Int32 || 0x06D0, 0x06F4

# 0x06DC, 0x06E0, 0x06E4, 0x06E8 [position of chat box]

# ·····································································

# LOCAL PLAYER
local_player = 0x313AD80  # [<League of Legends.exe> + 0x313AD80]

# LOCAL PLAYER ATTRIBUTES
local_player_name = 0x0054  # [+ 0x4 to complete full name]
# gold = 0x1B88  # Float [!]
# gold_max = 0x1B98  # Float [!]

# ·····································································

# MANAGERS
minion_manager = 0x24EBAE4  # [<League of Legends.exe> + 0x24EBAE4]
champion_manager = 0x189E2F4  # [<League of Legends.exe> + 0x189E2F4]
tower_manager = 0x3132FDC  # [<League of Legends.exe> + 0x3132FDC]
# inhibitor_manager = 0x2FB6B8C  # [!]
# missile_manager = 0x313D2B4  # [!]

# OBJECT MANAGER
object_manager = 0x189E25C  # [<League of Legends.exe> + 0x189E25C]
object_list = 0x0014  # Ptr
object_last = 0x0020  # Ptr
object_len = 0x002C  # Int32 || 0x0038

object_name = 0X0054  # Text8Ptr

# ·····································································

# MINIMAP
minimap_hud = 0x3131B80  # [<League of Legends.exe> + 0x3131B80]

# MINIMAP ATTRIBUTES
minimap_hud_pos = 0x003C  # Int32 [left = 65793, right = 257, maybe coords?]
minimap_hud_size_min = 0x0040  # Float
minimap_hud_size_max = 0x0044  # Float
minimap_hud_size = 0x0048  # Float: 0.75 - 1.5

minimap_hud_layer = 0x0128  # Pointer
minimap_hud_coord_neg_a = 0x0034  # Float
minimap_hud_coord_neg_b = 0x0038  # Float
minimap_hud_coord_neg_a = 0x003C  # Float
minimap_hud_coord_neg_b = 0x0040  # Float
minimap_hud_size_a = 0x0044  # Float || 0x004C
minimap_hud_size_b = 0x0048  # Float || 0x0050

# ·····································································

# ENTITY ATTRIBUTES
position = 0x01DC  # Vector3: x, z, y || 0x0224
is_visible = 0x0274  # Bool
is_dead_ofuscated_n = 0x0288  # Int8 || 0x010C [0, 2 = alive; 1, 3 = dead]
is_dead_ofuscated_1 = 0x0290  # [sends hex to nvwgf2um.dll ?]
is_dead_ofuscated_3 = 0x0298  # [sends hex to nvwgf2um.dll ?]
mana = 0x029C  # Float
mana_max = 0x02AC  # Float
health = 0x0E74  # Float
health_max = 0x0E84  # Float
recall_state = 0x0D90  # Int32 || 0x0D78 [6 = normal; 11 = herald/baron]
name = 0x2D7C  # Text8Ptr
name_verbose = 0x0054  # Text8Ptr [Works only in multi camp monsters and towers]
level = 0x355C  # Int32
