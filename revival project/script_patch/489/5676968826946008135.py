# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/item/ltype_2_class.py
from __future__ import absolute_import
_reload_all = True
from .lobby_item_type import *
from .Item import Item
from .Role import Role
from .Mecha import Mecha
from .Fashion import Fashion
from .Voice import Voice
from .JudgeRoomCard import JudgeRoomCard
from .Component import Component
from .Product import Product
from .VehicleSkin import VehicleSkin
lobby_type_2_class = {L_ITEM_TYPE_ROLE: Role,
   L_ITEM_TYPE_ROLE_SKIN: Fashion,
   L_ITEM_TYPE_MECHA: Mecha,
   L_ITEM_TYPE_MECHA_SKIN: Fashion,
   L_ITEM_TYPE_VOICE: Voice,
   L_ITEM_ROOM_POINT: JudgeRoomCard,
   L_ITEM_TYPE_MECHA_COMPONENT: Component,
   L_ITEM_TYPE_PRODUCT: Product,
   L_ITEM_YTPE_VEHICLE_SKIN: VehicleSkin
   }

def get_create_class_by_type(ltype):
    return lobby_type_2_class.get(ltype, Item)