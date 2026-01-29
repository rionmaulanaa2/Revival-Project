# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/com_ai_ctrl/ComRemoteRobotMove.py
from __future__ import absolute_import
from .ComRemoteMove import ComRemoteMove
from logic.gutils.character_ctrl_utils import check_climb, try_jump
from logic.gcommon.cdata import status_config as st_const

class ComRemoteRobotMove(ComRemoteMove):
    ST_MOVE = (
     st_const.ST_MOVE, st_const.ST_RUN)

    def __init__(self):
        super(ComRemoteRobotMove, self).__init__()
        self._last_pos = None
        return

    def destroy(self):
        super(ComRemoteRobotMove, self).destroy()

    def exec_block_move(self):
        flag = check_climb(self)
        if flag[0]:
            self.send_event('E_CLIMB', flag[1], flag[2], flag[3])
        else:
            try_jump(self)

    def in_move_state(self):
        return self.ev_g_is_in_any_state(self.ST_MOVE)