# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/data/item_use_var.py
_reload_all = True
from logic.gutils.item_utils import get_item_type_id_list
from logic.gcommon.item import backpack_item_type
THROW_ID_LIST = get_item_type_id_list([
 backpack_item_type.B_ITEM_TYPE_WEAPON_BOMB,
 backpack_item_type.B_ITEM_TYPE_BUILDING,
 backpack_item_type.B_ITEM_TYPE_MAGIC_SHOP_ITEM])
USABLE_ID_LIST = get_item_type_id_list([
 backpack_item_type.B_ITEM_TYPE_HEALTH,
 backpack_item_type.B_ITEM_TYPE_FOOD,
 backpack_item_type.B_ITEM_TYPE_MECHA_BATTERY,
 backpack_item_type.B_ITEM_TYPE_SUMMON,
 backpack_item_type.B_ITEM_TYPE_BUFF,
 backpack_item_type.B_ITEM_TYPE_NEUTRAL_SHOP_CANDY,
 backpack_item_type.B_ITEM_TYPE_KIZUNAAI_FIREWORK,
 backpack_item_type.B_ITEM_TYPE_KIZUNAAI_CALL])
MECHA_USABLE_ID_LIST = get_item_type_id_list([
 backpack_item_type.B_ITEM_TYPE_HEALTH,
 backpack_item_type.B_ITEM_TYPE_FOOD,
 backpack_item_type.B_ITEM_TYPE_MECHA_BATTERY,
 backpack_item_type.B_ITEM_TYPE_SUMMON,
 backpack_item_type.B_ITEM_TYPE_BUFF,
 backpack_item_type.B_ITEM_TYPE_BUILDING,
 backpack_item_type.B_ITEM_TYPE_NEUTRAL_SHOP_CANDY,
 backpack_item_type.B_ITEM_TYPE_MAGIC_SHOP_ITEM,
 backpack_item_type.B_ITEM_TYPE_PVE_THROW_ITEM])
HIDEN_USABLE_ID_LIST = get_item_type_id_list([
 backpack_item_type.B_ITEM_TYPE_BACK_HOME])
ALL_USABLE_ID_LIST = THROW_ID_LIST + USABLE_ID_LIST + MECHA_USABLE_ID_LIST + HIDEN_USABLE_ID_LIST