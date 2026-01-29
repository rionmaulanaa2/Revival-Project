# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/avatarmembers/impCommentGuide.py
from __future__ import absolute_import
from mobile.common.rpcdecorator import rpc_method, CLIENT_STUB
from mobile.common.RpcMethodArgs import Int
from logic.gcommon.common_const import guide_const

class impCommentGuide(object):

    def _init_commentguide_from_dict(self, bdict):
        global_data.emgr.lobby_scene_pause_event += self.lobby_scene_event
        self._in_lobby = True
        self._need_comment_type = None
        return

    @rpc_method(CLIENT_STUB, (Int('from_type'),))
    def guide_player_comment(self, from_type):
        self._need_comment_type = from_type
        self.comment()

    def update_comment_to_server(self, no_remind, commented):
        self.call_server_method('update_comment_status', (no_remind, commented))

    def comment(self):
        self._need_comment_type = None
        return

    def need_comment(self):
        if global_data.is_pc_mode or G_IS_NA_USER:
            return False
        if not self._need_comment_type:
            return False
        if global_data.last_scene_is_lottery and self._need_comment_type not in [guide_const.GC_TYPE_LOTTERY_RARE_SS_ITEM, guide_const.GC_TYPE_LOTTERY_RARE_S_ITEM]:
            return False
        ui = global_data.ui_mgr.get_ui('ReceiveRewardUI')
        if ui and ui.is_showing():
            return False
        ui = global_data.ui_mgr.get_ui('OpenBoxUI')
        if ui:
            return False
        ui = global_data.ui_mgr.get_ui('LotteryMainUI')
        if ui:
            return False
        return True

    def lobby_scene_event(self, pause_flag):
        if pause_flag:
            self._in_lobby = False
        else:
            self._in_lobby = True
            self.comment()
            global_data.last_scene_is_lottery = False