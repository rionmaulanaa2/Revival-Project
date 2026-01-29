# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/com_camera/ComStateTrkCamCommonEvents.py
from __future__ import absolute_import
from logic.gcommon.component.UnitCom import UnitCom
from logic.gcommon.cdata import status_config
from common.cfg import confmgr

class ComStateTrkCamCommonEvents(UnitCom):
    BIND_EVENT = {'E_SHOW_MINE_TRAJECTORY': 'on_show_main_trajectory',
       'E_SHOW_SYNC_TRAJECTORY': 'on_show_main_trajectory',
       'E_SHOW_MINE_SOCK_TRAJECTORY': 'on_show_main_sock_trajectory',
       'E_SHOW_SYNC_SOCK_TRAJECTORY': 'on_show_main_sock_trajectory',
       'E_PLAY_WEAPON_FIRE_CAMERA_TRK': '_play_weapon_fire_camera_trk',
       'E_PLAY_ACC_WEAPON_FIRE_CAMERA_TRK': 'accumulate_gun_fire_helper',
       'E_CANCEL_WEAPON_FIRE_CAMERA_TRK': '_cancel_weapon_fire_camera_trk',
       'G_NEED_PLAY_EACH_FIRE_CAMERA_TRK': 'get_need_play_each_fire_trk'
       }

    def on_show_main_trajectory(self, weapon_type, fire_pos, target_end, accumulate_level, *args, **kwargs):
        self.accumulate_gun_fire_helper(weapon_type, accumulate_level)

    def on_show_main_sock_trajectory(self, weapon_type, fire_pos, target_end, accumulate_level, *args, **kwargs):
        self.accumulate_gun_fire_helper(weapon_type, accumulate_level)

    def accumulate_gun_fire_helper(self, weapon_type, accumulate_level):
        if not self.ev_g_is_cam_target():
            return
        else:
            if accumulate_level is None:
                return
            accu_weapon_type = self.get_real_accumulate_gun_harm_weapon_type(weapon_type, accumulate_level)
            if accu_weapon_type:
                self._play_weapon_fire_camera_trk(accu_weapon_type)
            return

    def _play_weapon_fire_camera_trk(self, weapon_type):
        trk_conf = confmgr.get('camera_trk_sfx_conf', 'WeaponTrkConfig').get('Content').get(str(weapon_type), {})
        fire_trk = trk_conf.get('trk_tag', None)
        if self.sd.ref_in_aim or self.ev_g_in_right_aim():
            fire_trk = trk_conf.get('aim_trk_tag', fire_trk)
        if fire_trk:
            self.send_event('E_PLAY_CAMERA_TRK', fire_trk)
        return

    def _cancel_weapon_fire_camera_trk(self, weapon_type):
        trk_conf = confmgr.get('camera_trk_sfx_conf', 'WeaponTrkConfig').get('Content').get(str(weapon_type), {})
        fire_trk = trk_conf.get('trk_tag', None)
        if fire_trk:
            self.send_event('E_CANCEL_CAMERA_TRK', fire_trk)
        return

    def get_real_accumulate_gun_harm_weapon_type(self, weapon_type, accumulate_level):
        accumulate_config = confmgr.get('accumulate_config', str(weapon_type), default=None)
        if accumulate_config:
            return accumulate_config.get('iItemID_%d' % accumulate_level)
        else:
            return

    def get_need_play_each_fire_trk(self, weapon_type):
        w_conf = confmgr.get('camera_trk_sfx_conf', 'WeaponTrkConfig').get('Content').get(str(weapon_type), {})
        if w_conf.get('is_continue_trk', 0):
            return False
        else:
            return True