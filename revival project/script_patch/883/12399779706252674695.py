# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComRunCam.py
from __future__ import absolute_import
from ..UnitCom import UnitCom
from logic.gcommon.common_const import vehicle_const
import math3d
import math

class ComRunCam(UnitCom):
    BIND_EVENT = {'E_NOTIFY_MOVE_STATE_CHANGE': ('_on_change_move_state', 10),
       'E_ACTION_MOVE_STOP': ('_on_move_stop', 10),
       'G_IS_IN_RUN_CAM': '_get_is_in_run_cam',
       'E_SET_INTO_RUN_TRK_TIME': 'set_into_run_trk_time'
       }

    def __init__(self):
        super(ComRunCam, self).__init__()
        self._is_on_run = False
        self._delay_into_run_cam_timer = None
        self._trk_cam_timer = None
        self._switch_into_run_trk_time = 1.1
        return

    def init_from_dict(self, unit_obj, bdict):
        super(ComRunCam, self).init_from_dict(unit_obj, bdict)

    def destroy(self):
        self.unregist_timer()
        self.destroy_run_trk()
        super(ComRunCam, self).destroy()

    def unregist_timer(self):
        global_data.game_mgr.unregister_logic_timer(self._delay_into_run_cam_timer)
        self._delay_into_run_cam_timer = None
        return

    def unregist_trk_timer(self):
        global_data.game_mgr.unregister_logic_timer(self._trk_cam_timer)
        self._trk_cam_timer = None
        return

    def _into_run(self):
        self._delay_into_run_cam_timer = None
        global_data.emgr.player_enter_run_camera_event.emit()
        self._is_on_run = True
        return

    def _into_run_camera_trk(self):
        self._trk_cam_timer = None
        self.send_event('E_CANCEL_CAMERA_TRK', 'CHARACTER_RUN_START', True)
        return

    def _on_change_move_state(self, *args):
        move_state = self.ev_g_move_state()
        from common.utils.timer import CLOCK
        import logic.gcommon.common_const.animation_const as animation_const
        if not self._is_on_run:
            if move_state == animation_const.MOVE_STATE_RUN:
                if global_data.cam_lplayer and self.unit_obj.id == global_data.cam_lplayer.id:
                    self.unregist_timer()
                    t_id = global_data.game_mgr.register_logic_timer(self._into_run, interval=0.6, times=1, mode=CLOCK)
                    if t_id:
                        self._delay_into_run_cam_timer = t_id
        elif self._is_on_run:
            if move_state != animation_const.MOVE_STATE_RUN:
                self._on_move_stop()
        self._on_change_move_state_trk()

    def _on_move_stop(self, *args):
        self.unregist_timer()
        if self._is_on_run:
            self._is_on_run = False
            if global_data.cam_lplayer and self.unit_obj.id == global_data.cam_lplayer.id:
                global_data.emgr.player_leave_run_camera_event.emit()
        self.on_move_stop_trk()

    def _get_is_in_run_cam(self, *args):
        return self._is_on_run

    def test_code(self):

        def callback():
            global_data.cam_lplayer.send_event('E_PLAY_CAMERA_TRK', 'CHARACTER_RUN')

        global_data.cam_lplayer.send_event('E_PLAY_CAMERA_TRK', 'CHARACTER_RUN_START', callback)

        def cancel():
            global_data.cam_lplayer.send_event('E_CANCEL_CAMERA_TRK', 'CHARACTER_RUN_START', True)

        global_data.game_mgr.register_logic_timer(cancel, interval=0.5, times=1, mode=2)

    def set_into_run_trk_time(self, time):
        self._switch_into_run_trk_time = time

    def destroy_run_trk(self):
        self.send_event('E_CANCEL_CAMERA_TRK', 'CHARACTER_MOVE')
        self.send_event('E_CANCEL_CAMERA_TRK', 'CHARACTER_RUN')
        self.send_event('E_CANCEL_CAMERA_TRK', 'CHARACTER_RUN_START')
        self.unregist_trk_timer()

    def _on_change_move_state_trk(self, *args):
        if global_data.enabel_run_trk:
            move_state = self.ev_g_move_state()
            from common.utils.timer import CLOCK
            import logic.gcommon.common_const.animation_const as animation_const
            if move_state == animation_const.MOVE_STATE_RUN:

                def end_callback():
                    self.send_event('E_PLAY_CAMERA_TRK', 'CHARACTER_RUN')

                self.send_event('E_PLAY_CAMERA_TRK', 'CHARACTER_RUN_START', end_callback)
            else:
                self.unregist_trk_timer()
                self.send_event('E_CANCEL_CAMERA_TRK', 'CHARACTER_RUN_START')
                self.send_event('E_CANCEL_CAMERA_TRK', 'CHARACTER_RUN')
            if move_state == animation_const.MOVE_STATE_WALK:
                self.send_event('E_PLAY_CAMERA_TRK', 'CHARACTER_MOVE')
            else:
                self.send_event('E_CANCEL_CAMERA_TRK', 'CHARACTER_MOVE')

    def on_move_stop_trk(self):
        if global_data.enabel_run_trk:
            self.send_event('E_CANCEL_CAMERA_TRK', 'CHARACTER_MOVE')
            self.unregist_trk_timer()
            self.send_event('E_CANCEL_CAMERA_TRK', 'CHARACTER_RUN')
            self.send_event('E_CANCEL_CAMERA_TRK', 'CHARACTER_RUN_START')