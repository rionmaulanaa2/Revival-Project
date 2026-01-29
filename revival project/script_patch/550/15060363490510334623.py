# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComSkateCam.py
from __future__ import absolute_import
from ..UnitCom import UnitCom
from logic.gcommon.common_const import vehicle_const
import math3d
import math

class ComSkateCam(UnitCom):
    BIND_EVENT = {'E_BOARD_SKATE': ('_on_board_skate', 10),
       'E_LEAVE_SKATE': ('on_leave_skate', 10),
       'E_ACTION_MOVE': ('_on_move', 10),
       'E_ACTION_SKATE_MOVE_STOP': ('_on_move_stop', 10),
       'G_IS_IN_SKATE_MOVE_CAM': '_get_is_in_skating'
       }

    def __init__(self):
        super(ComSkateCam, self).__init__()
        self._is_on_move = False

    def init_from_dict(self, unit_obj, bdict):
        super(ComSkateCam, self).init_from_dict(unit_obj, bdict)

    def _on_board_skate(self, *args):
        pass

    def on_leave_skate(self):
        if self._is_on_move:
            self._is_on_move = False
            if global_data.cam_lplayer and self.unit_obj.id == global_data.cam_lplayer.id:
                global_data.emgr.player_leave_skate_move_camera.emit()

    def _on_move(self, *args):
        if not self._is_on_move:
            import logic.gcommon.common_const.animation_const as animation_const
            skate_state = self.ev_g_skate_action()
            if skate_state in [animation_const.SKATE_ACTION_MOVE, animation_const.SKATE_ACTION_PREPARE_MOVE]:
                if global_data.cam_lplayer and self.unit_obj.id == global_data.cam_lplayer.id:
                    global_data.emgr.player_enter_skate_move_camera.emit()
                self._is_on_move = True

    def _on_move_stop(self, *args):
        if self._is_on_move:
            self._is_on_move = False
            if global_data.cam_lplayer and self.unit_obj.id == global_data.cam_lplayer.id:
                global_data.emgr.player_leave_skate_move_camera.emit()

    def _get_is_in_skating(self, *args):
        return self._is_on_move