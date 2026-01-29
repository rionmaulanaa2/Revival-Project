# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/avatarmembers/impBattleFlag.py
from __future__ import absolute_import
from logic.gcommon.common_const import title_const
from mobile.common.rpcdecorator import rpc_method, CLIENT_STUB
from mobile.common.RpcMethodArgs import Str, Int, Bool, List, Dict
from logic.gutils import title_utils
from logic.gcommon.item.item_const import DEFAULT_FLAG_FRAME
from logic.gutils import battle_flag_utils

class impBattleFlag(object):

    def _init_battleflag_from_dict(self, bdict):
        self._battle_flag_info = bdict.get('battle_flag', {})

    def _destroy_battleflag(self):
        self._battle_flag_info = None
        return

    def get_battle_flag(self):
        return self._battle_flag_info

    def get_battle_flag_medal(self):
        return self._battle_flag_info.get('medal', [])

    def get_battle_flag_frame(self):
        return self._battle_flag_info.get('frame', DEFAULT_FLAG_FRAME())

    def set_battle_flag_frame(self, frame_item_id):
        self._battle_flag_info['frame'] = frame_item_id
        self.call_server_method('set_battle_flag_frame', (frame_item_id,))
        global_data.emgr.set_battle_flag_frame_event.emit()

    def set_battle_flag_medal(self, selected_medals):
        self._battle_flag_info['medal'] = selected_medals
        self.call_server_method('set_battle_flag_medal', (selected_medals,))
        global_data.emgr.set_battle_flag_medal_event.emit()
        return True

    @rpc_method(CLIENT_STUB, (List('medal_list'),))
    def on_set_battle_flag_medal(self, medal_list):
        self._battle_flag_info['medal'] = medal_list