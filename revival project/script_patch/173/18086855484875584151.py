# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/com_camera/ComShotCam.py
from __future__ import absolute_import
from logic.gcommon.component.UnitCom import UnitCom

class ComShotCam(UnitCom):
    RECOVER_TIME = 0.7
    BIND_EVENT = {'E_ATTACK_START': ('_on_start_attack', 10),
       'E_ATTACK_END': ('on_end_attack', 10),
       'G_IS_IN_SHOT_CAM': '_get_is_in_shot_cam'
       }

    def __init__(self):
        super(ComShotCam, self).__init__()
        self._is_on_shot_cam = False
        self._cancel_timer = None
        return

    def init_from_dict(self, unit_obj, bdict):
        super(ComShotCam, self).init_from_dict(unit_obj, bdict)

    def destroy(self):
        self.unregist_timer()
        super(ComShotCam, self).destroy()

    def unregist_timer(self):
        global_data.game_mgr.unregister_logic_timer(self._cancel_timer)
        self._cancel_timer = None
        return

    def _on_start_attack(self):
        if global_data.cam_lplayer and self.unit_obj.id == global_data.cam_lplayer.id:
            from logic.gcommon.const import MAIN_WEAPON_LIST
            if self.sd.ref_wp_bar_cur_pos not in MAIN_WEAPON_LIST:
                return
            if not self._is_on_shot_cam:
                global_data.emgr.player_enter_shot_camera_event.emit()
                self._is_on_shot_cam = True

    def on_end_attack(self, *args):
        if self._is_on_shot_cam:
            self._is_on_shot_cam = False
            if global_data.cam_lplayer and self.unit_obj.id == global_data.cam_lplayer.id:
                self.regist_timer()

    def _get_is_in_shot_cam(self, *args):
        return self._is_on_shot_cam

    def regist_timer(self):
        self.unregist_timer()
        from common.utils.timer import CLOCK

        def recover_camera():
            global_data.emgr.player_leave_shot_camera_event.emit()

        t_id = global_data.game_mgr.register_logic_timer(recover_camera, interval=self.RECOVER_TIME, times=1, mode=CLOCK)
        if t_id:
            self._cancel_timer = t_id