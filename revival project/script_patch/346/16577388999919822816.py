# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/com_camera/ComCamClipAni.py
from __future__ import absolute_import
import six_ex
from logic.gcommon.component.UnitCom import UnitCom

class ComCamClipAni(UnitCom):
    BIND_EVENT = {'E_TRIGGER_CAM_CLIP': '_on_start_clip',
       'E_EXIT_CAM_CLIP': '_on_end_clip',
       'G_IN_CAM_CLIP': '_get_is_in_clip',
       'G_RUNNING_CAM_CLIP': 'get_all_running_clip'
       }

    def __init__(self):
        super(ComCamClipAni, self).__init__()
        self._is_in_clip = {}
        self._enter_timer_dict = {}
        self._end_timer_dict = {}

    def init_from_dict(self, unit_obj, bdict):
        super(ComCamClipAni, self).init_from_dict(unit_obj, bdict)

    def destroy(self):
        super(ComCamClipAni, self).destroy()
        self.unregist_timer_dict(self._enter_timer_dict)
        self._enter_timer_dict = {}
        self.unregist_timer_dict(self._end_timer_dict)
        self._end_timer_dict = {}
        self._is_in_clip = {}

    def _on_start_clip(self, clip_state):
        if not self.ev_g_is_cam_target():
            return
        if not self._get_is_in_clip(clip_state):
            from common.cfg import confmgr
            fEnterDelay = confmgr.get('c_camera_ani_state', str(clip_state), default={}).get('fEnterDelay', 0)

            def suc_func():
                self._is_in_clip[clip_state] = True
                global_data.emgr.player_enter_camera_clip_state_event.emit(clip_state)

            if fEnterDelay:
                self.regist_timer(self._enter_timer_dict, clip_state, fEnterDelay, suc_func)
            else:
                suc_func()

    def _on_end_clip(self, clip_state):
        if not self.ev_g_is_cam_target():
            return
        if self._get_is_in_clip(clip_state):
            from common.cfg import confmgr
            fExitDelay = confmgr.get('c_camera_ani_state', str(clip_state), default={}).get('fExitDelay', 0)

            def suc_func():
                del self._is_in_clip[clip_state]
                global_data.emgr.player_exit_camera_clip_state_event.emit(clip_state)

            if fExitDelay:
                self.regist_timer(self._end_timer_dict, clip_state, fExitDelay, suc_func)
            else:
                suc_func()

    def _get_is_in_clip(self, clip_state):
        return self._is_in_clip.get(clip_state, False)

    def unregist_timer(self, timer_dict, clip_state):
        end_timer = timer_dict.get(clip_state, None)
        if end_timer:
            global_data.game_mgr.unregister_logic_timer(end_timer)
            del timer_dict[clip_state]
        return

    def regist_timer(self, timer_dict, clip_state, clip_delay, callback):
        self.unregist_timer(timer_dict, clip_state)
        from common.utils.timer import CLOCK

        def recover_camera():
            callback()

        t_id = global_data.game_mgr.register_logic_timer(recover_camera, interval=clip_delay, times=1, mode=CLOCK)
        if t_id:
            timer_dict[clip_state] = t_id

    def unregist_timer_dict(self, timer_dict):
        clip_states = six_ex.keys(timer_dict)
        for clip_state in clip_states:
            self.unregist_timer(timer_dict, clip_state)

    def get_all_running_clip(self):
        return six_ex.keys(self._is_in_clip)