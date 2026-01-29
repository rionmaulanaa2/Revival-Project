# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/com_lobby_char/ComAvatarUserData.py
from __future__ import absolute_import
from logic.gcommon.component.UnitCom import UnitCom

class ComAvatarUserData(UnitCom):
    BIND_EVENT = {'G_IS_AVATAR': '_is_avatar',
       'G_ROLE_ID': '_get_role_id',
       'G_FASHION_INFO': '_get_fashion_info'
       }

    def __init__(self):
        super(ComAvatarUserData, self).__init__()
        self._user_data = {}

    def _is_avatar(self):
        return True

    def init_from_dict(self, unit_obj, bdict):
        super(ComAvatarUserData, self).init_from_dict(unit_obj, bdict)

    def _get_role_id(self):
        if not global_data.player:
            return None
        else:
            return global_data.player.get_role()

    def _get_fashion_info(self):
        if not global_data.player:
            return {}
        role_id = self._get_role_id()
        item_data = global_data.player.get_item_by_no(role_id)
        if not item_data:
            return {}
        fashion_data = item_data.get_fashion()
        return fashion_data