# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/com_camera/ComStateTrkCamEvents.py
from __future__ import absolute_import
from logic.gcommon.component.UnitCom import UnitCom
from logic.gcommon.cdata import status_config
from logic.gcommon.component.client.com_camera.ComStateTrkCamCommonEvents import ComStateTrkCamCommonEvents
from common.cfg import confmgr

class ComStateTrkCamEvents(ComStateTrkCamCommonEvents):
    BIND_EVENT = dict(ComStateTrkCamCommonEvents.BIND_EVENT)
    BIND_EVENT.update({'E_PARACHUTE_STATUS_CHANGED': 'parachute_status_changed',
       'E_CTRL_ACCUMULATE': 'on_ctrl_accumulate',
       'E_LEAVE_STATE': 'on_leave_state',
       'E_ATTACK_START': '_play_auto_fire_camera_trk',
       'E_ATTACK_END': ('_stop_auto_fire_camera_trk', -10),
       'E_AGONY': ('on_agony', -10),
       'E_DEFEATED': ('_on_death', -10),
       'E_DEATH': ('_on_death', -10),
       'E_LOADING': '_play_loading_camera_trk',
       'E_SWITCHING_WP_MODE': ('on_switching_wp_mode', -10),
       'E_SWITCH_WEAPON': ('on_switch_weapon', -10)
       })

    def __init__(self):
        super(ComStateTrkCamEvents, self).__init__()

    def parachute_status_changed(self, stage):
        from logic.gcommon.common_utils.parachute_utils import STAGE_FREE_DROP, STAGE_PARACHUTE_DROP, STAGE_LAND
        if stage == STAGE_FREE_DROP:
            pass
        elif stage in (STAGE_PARACHUTE_DROP, STAGE_LAND):
            self.send_event('E_CANCEL_CAMERA_TRK', 'MECHA_FLY')

    def on_ctrl_accumulate(self, is_on_accumulate):
        from common.cfg import confmgr
        weapon = self.sd.ref_wp_bar_cur_weapon
        if weapon:
            trk_conf = confmgr.get('camera_trk_sfx_conf', 'WeaponTrkConfig').get('Content').get(str(weapon.iType), {})
            accumulate_trk_tag = trk_conf.get('accumulate_trk_tag', None)
            if accumulate_trk_tag:
                if is_on_accumulate:
                    self.send_event('E_PLAY_CAMERA_TRK', accumulate_trk_tag)
                else:
                    self.send_event('E_CANCEL_CAMERA_TRK', accumulate_trk_tag)
        return

    def on_leave_state(self, leave_state, new_st=None):
        if isinstance(leave_state, set) and status_config.ST_WEAPON_ACCUMULATE in leave_state or isinstance(leave_state, int) and status_config.ST_WEAPON_ACCUMULATE == leave_state:
            self.on_ctrl_accumulate(False)
        if isinstance(leave_state, set) and status_config.ST_SHOOT in leave_state or isinstance(leave_state, int) and status_config.ST_SHOOT == leave_state:
            self._stop_auto_fire_camera_trk()

    def _play_auto_fire_camera_trk(self, *args):
        _cur_weapon = self.sd.ref_wp_bar_cur_weapon
        if _cur_weapon:
            item_no = _cur_weapon.get_item_id()
            if not self.get_need_play_each_fire_trk(item_no):
                self._play_weapon_fire_camera_trk(item_no)

    def on_agony(self):
        self._stop_auto_fire_camera_trk()
        self.on_ctrl_accumulate(False)

    def _stop_auto_fire_camera_trk(self, *args):
        _cur_weapon = self.sd.ref_wp_bar_cur_weapon
        if _cur_weapon:
            self._cancel_weapon_fire_camera_trk(_cur_weapon.get_item_id())

    def _on_death(self, *args):
        self._stop_auto_fire_camera_trk()
        self.on_ctrl_accumulate(False)

    def _play_weapon_fire_camera_trk(self, weapon_type):
        trk_conf = confmgr.get('camera_trk_sfx_conf', 'WeaponTrkConfig').get('Content').get(str(weapon_type), {})
        fire_trk = trk_conf.get('trk_tag', None)
        if self.sd.ref_in_aim or self.ev_g_in_right_aim():
            fire_trk = trk_conf.get('aim_trk_tag', fire_trk)
        if fire_trk:
            self.send_event('E_PLAY_CAMERA_TRK', fire_trk)
        return

    def _play_loading_camera_trk(self):
        cur_weapon = self.sd.ref_wp_bar_cur_weapon
        if not cur_weapon:
            return
        else:
            item_no = cur_weapon.get_item_id()
            if not item_no:
                return
            trk_conf = confmgr.get('camera_trk_sfx_conf', 'WeaponTrkConfig').get('Content').get(str(item_no), {})
            loading_trk = trk_conf.get('aim_load_trk_tag', None)
            if not loading_trk:
                return
            if self.sd.ref_in_aim:
                self.send_event('E_PLAY_CAMERA_TRK', loading_trk)
            return

    def on_switching_wp_mode(self, pos, enable):
        self._stop_auto_fire_camera_trk()
        self.on_ctrl_accumulate(False)

    def on_switch_weapon(self, pos1, pos2):
        self._stop_auto_fire_camera_trk()
        self.on_ctrl_accumulate(False)

    def destroy(self):
        super(ComStateTrkCamEvents, self).destroy()
        self._stop_auto_fire_camera_trk()
        self.on_ctrl_accumulate(False)