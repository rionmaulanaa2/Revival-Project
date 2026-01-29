# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/com_lobby_char/ComLobbyPuppetUserData.py
from __future__ import absolute_import
from logic.gcommon.component.UnitCom import UnitCom
from logic.gcommon.const import DEFAULT_ROLE_ID

class ComLobbyPuppetUserData(UnitCom):
    BIND_EVENT = {'G_LOBBY_USER_DATA': '_get_user_data',
       'G_LOBBY_USER_DATA_BY_KEY': '_get_user_data_by_key',
       'G_IS_AVATAR': '_is_avatar',
       'E_ON_UPDATE_LOBBY_USER_DATA': '_on_update_user_data',
       'G_ROLE_ID': '_get_role_id',
       'G_FASHION_INFO': '_get_fashion_info'
       }

    def __init__(self):
        super(ComLobbyPuppetUserData, self).__init__()
        self._user_data = {}

    def _is_avatar(self):
        return False

    def init_from_dict(self, unit_obj, bdict):
        self._user_data = bdict
        super(ComLobbyPuppetUserData, self).init_from_dict(unit_obj, bdict)

    def _on_update_user_data(self, update_dict):
        self._user_data.update(update_dict)
        self.send_event('E_ON_LOBBYPUPPET_DATA_CHANGE')

    def _get_user_data(self):
        return self._user_data

    def _get_user_data_by_key(self, key):
        return self._user_data.get(key)

    def _get_role_id(self):
        return self._user_data.get('role_id', DEFAULT_ROLE_ID)

    def _get_fashion_info(self):
        fashion_data = self._user_data.get('role_fashion', {})
        if not G_IS_CLIENT:
            return fashion_data
        else:
            from ext_package.ext_decorator import get_default_fashion
            role_id = self._get_role_id()
            return get_default_fashion(self, fashion_data, role_id)