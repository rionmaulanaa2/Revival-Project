# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/com_parachute/ComFreeDropCam.py
from __future__ import absolute_import
from logic.gcommon.component.UnitCom import UnitCom

class ComFreeDropCam(UnitCom):
    BIND_EVENT = {'E_PARACHUTE_MOVE': ('_on_move', 10),
       'E_PARACHUTE_MOVE_STOP': ('_on_move_stop', 10),
       'G_IS_IN_PARACHUTE_MOVE_CAM': '_get_parachute_move'
       }

    def __init__(self):
        super(ComFreeDropCam, self).__init__()
        self._is_on_move = False

    def init_from_dict(self, unit_obj, bdict):
        super(ComFreeDropCam, self).init_from_dict(unit_obj, bdict)

    def _on_move(self, *args):
        if not self._is_on_move:
            is_in_freedrop = self.ev_g_is_parachute_stage_free_drop()
            if is_in_freedrop:
                if global_data.cam_lplayer and self.unit_obj.id == global_data.cam_lplayer.id:
                    global_data.emgr.player_enter_free_drop_move_camera.emit()
                self._is_on_move = True

    def _on_move_stop(self, *args):
        if self._is_on_move:
            self._is_on_move = False
            if global_data.cam_lplayer and self.unit_obj.id == global_data.cam_lplayer.id:
                global_data.emgr.player_leave_free_drop_move_camera.emit()

    def _get_parachute_move(self):
        return self._is_on_move