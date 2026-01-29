# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/com_camera/ComMechaStateTrkCamEvents.py
from __future__ import absolute_import
from logic.gcommon.component.UnitCom import UnitCom
from logic.gcommon.component.client.com_camera.ComStateTrkCamCommonEvents import ComStateTrkCamCommonEvents

class ComMechaStateTrkCamEvents(ComStateTrkCamCommonEvents):
    BIND_EVENT = dict(ComStateTrkCamCommonEvents.BIND_EVENT)
    BIND_EVENT.update({'E_EXIT_CAM_CLIP': 'on_exit_cam_clip',
       'E_ATTACK_START': '_play_auto_fire_camera_trk',
       'E_ATTACK_END': '_stop_auto_fire_camera_trk',
       'E_ON_LEAVE_MECHA': ('on_leave_mecha', -20)
       })

    def __init__(self):
        super(ComMechaStateTrkCamEvents, self).__init__()
        self._chasing_valid_timer = None
        self._is_listen_on_chasing_hit = False
        self._cur_trk_pos = None
        return

    def destroy(self):
        super(ComMechaStateTrkCamEvents, self).destroy()
        self._stop_auto_fire_camera_trk()
        if self._chasing_valid_timer:
            global_data.game_mgr.unregister_logic_timer(self._chasing_valid_timer)
            self._chasing_valid_timer = None
        self.process_chasing_hit_trk_event(False)
        return

    def process_chasing_hit_trk_event(self, is_register):
        from logic.gcommon.common_const import mecha_const as mconst
        if self.sd.ref_mecha_id == mconst.KNIGHT_MECHA_ID:
            if is_register:
                if not self._is_listen_on_chasing_hit:
                    self.send_event('E_REGISTER_ANIMATOR_EVENT', 'sword_attack_01', 'hit_start', self._check_chasing_hit, None)
                    self._is_listen_on_chasing_hit = True
            elif self._is_listen_on_chasing_hit:
                self.send_event('E_UNREGISTER_ANIMATOR_EVENT', 'sword_attack_01', 'hit_start', self._check_chasing_hit)
                self._is_listen_on_chasing_hit = False
        return

    def on_exit_cam_clip(self, clip_name):
        if clip_name == 'CHASING_HIT' and not self._is_listen_on_chasing_hit:
            self.process_chasing_hit_trk_event(True)
            from common.utils.timer import CLOCK

            def unregist_event():
                self.process_chasing_hit_trk_event(False)
                self._chasing_valid_timer = None
                return

            self._chasing_valid_timer = global_data.game_mgr.register_logic_timer(unregist_event, interval=1, times=1, mode=CLOCK)

    def _check_chasing_hit(self, data):
        self.send_event('E_PLAY_CAMERA_TRK', '8002_SWORD_CHASING_ATTACK_1')
        self.process_chasing_hit_trk_event(False)

    def _play_auto_fire_camera_trk(self, weapon_pos):
        self._stop_auto_fire_camera_trk()
        _cur_weapon = self.ev_g_wpbar_get_by_pos(weapon_pos)
        if _cur_weapon:
            item_no = _cur_weapon.get_item_id()
            if not self.get_need_play_each_fire_trk(item_no):
                self._play_weapon_fire_camera_trk(item_no)
                self._cur_trk_pos = weapon_pos

    def _stop_auto_fire_camera_trk(self, *args):
        if self._cur_trk_pos is None:
            return
        else:
            _cur_weapon = self.ev_g_wpbar_get_by_pos(self._cur_trk_pos)
            if _cur_weapon:
                self._cancel_weapon_fire_camera_trk(_cur_weapon.get_item_id())
            return

    def on_leave_mecha(self, *args):
        self._stop_auto_fire_camera_trk()