# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/com_lobby_char/ComWeaponLobby.py
from __future__ import absolute_import
from logic.gcommon.component.UnitCom import UnitCom

class ComWeaponLobby(UnitCom):
    BIND_EVENT = {'G_WEAPON_TYPE': '_get_weapon_type'
       }

    def __init__(self):
        super(ComWeaponLobby, self).__init__()

    def init_from_dict(self, unit_obj, bdict):
        super(ComWeaponLobby, self).init_from_dict(unit_obj, bdict)

    def _get_weapon_type(self):
        from logic.gcommon.common_const.animation_const import WEAPON_TYPE_EMPTY_HAND
        return WEAPON_TYPE_EMPTY_HAND