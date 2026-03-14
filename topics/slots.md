Inventory Slot Overview **by Razr**

Minescript player_inventory() uses **Player.dat** format (https://minecraft.wiki/w/Player.dat_format#Inventory_slot_numbers)

Creative/Survival Player Inventory GUI:
0-8: Hotbar
9-35: Inventory
36-39: Boots, Leggings, Chestplate, Helmet
40: Offhand

Minescript Plus Inventory clicking methods use **Protocol** format (https://minecraft.wiki/w/Java_Edition_protocol/Inventory#Player_Inventory)

Survival Player Inventory GUI:
0: 2x2 crafting Output
1-4: 2x2 crafting Input
5-8: Helmet, Chestplate, Leggings, Boots
9-35: Inventory
36-44: Hotbar
45: Offhand

Same for chests (https://minecraft.wiki/w/Java_Edition_protocol/Inventory#Chest)

Single Chest GUI (27 slots):
0-26: Chest
27-53: Inventory
54-62: Hotbar

Double Chest GUI (54 slots):
0-53: Chest
54-80: Inventory
81-89: Hotbar