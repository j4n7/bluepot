# ·····································································

# Version 12.21
# Comment out offsets with [!] seem not to be working

# ·····································································

# GAME

game_time = 0x3152068  # Float

# ·····································································

# CHAT
chat = 0x3158930  # [<League of Legends.exe> + 0x3158930]

# CHAT ATTRIBUTES
times_open = 0x6D8  # Int32 [0 = chat closed]

messages_sent_count = 0x00AC  # Int32 || 0x00B0 [maybe total count?]
message_sent_0 = 0x00B4  # Text8Ptr [+ 0xC for next message]
message_sent_0_len = 0x00B8  # Int32 [+ 0xC for next message]
message_sent_0_xxx = 0x00BC  # Int32 [+ 0xC for next message, 1 or 2 chars longer than before, why?]

message_current = 0x06AC  # Text16Ptr
message_current_len = 0x06BC  # Int32 || 0x06D0, 0x06F4

# 0x06DC, 0x06E0, 0x06E4, 0x06E8 [Chat box dimensions?]

# ·····································································

# LOCAL PLAYER
local_player = 0x3157F40  # [<League of Legends.exe> + 0x3157F40]

# LOCAL PLAYER ATTRIBUTES
local_player_summoner_name_start = 0x0054  # Text8[len]
local_player_summoner_name_len = 0x0064  # Int32
gold = 0x1BA8  # Float
gold_max = 0x1BB8  # Float

# ·····································································

# MANAGERS
minion_manager = 0x25095CC  # [<League of Legends.exe> + 0x25095CC]
champion_manager = 0x18BBF40  # [<League of Legends.exe> + 0x18BBF40]
tower_manager = 0x315089C  # [<League of Legends.exe> + 0x315089C]
missile_manager = 0x31588D0  # [<League of Legends.exe> + 0x31588D0]
# inhibitor_manager = 0x25095CC  # [!]

# OBJECT MANAGER
object_manager = 0x18BBEA8  # [<League of Legends.exe> + 0x18BBEA8]
object_list = 0x0014  # Ptr
object_list_len = 0x002C  # Int32 || 0x0038
object_last = 0x0020  # Ptr

# ...Object
object_name = 0X0054  # Text8Ptr

# BUFF MANAGER
buff_manager = 0x2330
buff_list_start = 0x0010  # Ptr
buff_list_end = 0x0014  # Ptr

# ...Buff
buff_name = 0x0008  # Ptr [Trash objects dont't have a name]
buff_start_time = 0x000C  # Float || 0x0018
buff_end_time = 0x0010  # Float

# ·····································································

# MINIMAP
minimap_hud = 0x31520AC  # [<League of Legends.exe> + 0x31520AC]

# MINIMAP ATTRIBUTES
minimap_hud_pos = 0x003C  # Int32 [left = 65793, right = 257, maybe coords?]
minimap_hud_size_min = 0x0040  # Float
minimap_hud_size_max = 0x0044  # Float
minimap_hud_size = 0x0048  # Float: 0.75 - 1.5

minimap_hud_layer = 0x0150  # Pointer
minimap_hud_coord_neg_a = 0x0034  # Float
minimap_hud_coord_neg_b = 0x0038  # Float
minimap_hud_coord_neg_a = 0x003C  # Float
minimap_hud_coord_neg_b = 0x0040  # Float
minimap_hud_size_a = 0x0044  # Float || 0x004C
minimap_hud_size_b = 0x0048  # Float || 0x0050

# ·····································································

# ENTITY ATTRIBUTES
name_verbose = 0x0054  # Text8Ptr [Works only in multi camp monsters and towers]
position = 0x01DC  # Vector3: x, z, y || 0x0224
is_visible = 0x0274  # Bool
is_dead_ofuscated_n = 0x0288  # Int8 [0, 2 = alive; 1, 3 = dead]
is_dead_ofuscated_1 = 0x0290
is_dead_ofuscated_3 = 0x0298
mana = 0x029C  # Float
mana_max = 0x02AC  # Float
health = 0x0E74  # Float
health_max = 0x0E84  # Float
recall_state = 0x0D90  # Int32 || 0x0D78 [6 = normal; 11 = herald/baron]
name = 0x2DA4  # Text8Ptr || 0x3180
level = 0x3584  # Int32
