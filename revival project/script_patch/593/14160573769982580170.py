# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/com_art_check/ComArtCheckSender.py
from __future__ import absolute_import
from logic.gcommon.component.UnitCom import UnitCom
from common import utilities
import math3d

class ComArtCheckSender(UnitCom):

    def __init__(self, need_update=False):
        super(ComArtCheckSender, self).__init__(need_update)
        self.init_global_event()

    def init_global_event(self):
        global_data.emgr.trigger_lobby_player_move += self.trigger_lobby_player_move
        global_data.emgr.trigger_lobby_player_move_stop += self.trigger_lobby_player_move_stop
        global_data.emgr.trigger_lobby_player_set_yaw += self.trigger_lobby_player_set_yaw

    def trigger_lobby_player_move(self, vec):
        norm_v = math3d.vector(vec)
        if not norm_v.is_zero:
            norm_v.normalize()
        self.send_event('E_MOVE', vec)

    def trigger_lobby_player_move_stop(self):
        self.send_event('E_MOVE_STOP')

    def trigger_lobby_player_set_yaw(self, yaw):
        self.send_event('E_SET_YAW', yaw)