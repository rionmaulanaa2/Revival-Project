# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/com_ai_ctrl/ComRemoteControl8011.py
from __future__ import absolute_import
from logic.gcommon.component.UnitCom import UnitCom
from logic.gcommon.common_const import ai_const
from logic.gcommon.cdata import mecha_status_config
from logic.gcommon import time_utility as tutil
import math3d
import time
import math
import logic.gcommon.const as g_const
import random
import logic.gutils.delay as delay
from common.utils.timer import CLOCK

class ComRemoteControl8011(UnitCom):
    BIND_EVENT = {'E_CTRL_ACTION_START': 'on_action_start',
       'E_CTRL_ACTION_STOP': 'on_action_stop',
       'G_WEAPON_TYPE': 'on_get_weapon_type',
       'E_ENTER_STATE': 'on_enter_state',
       'G_IS_IN_ATTACK_TIME': 'is_in_attack_time'
       }
    ACTION_MAP = {ai_const.CTRL_ACTION_MAIN: 'main_weapon_attack',
       ai_const.CTRL_ACTION_SUB: 'sub_weapon_attack',
       ai_const.CTRL_ACTION_JUMP: 'jump',
       ai_const.CTRL_ACTION_RUSH: 'dash',
       ai_const.CTRL_ACTION_EXT: 'ext'
       }

    def __init__(self):
        super(ComRemoteControl8011, self).__init__()
        self._delay_exe_id = None
        self._attack_time = 0
        return

    def init_from_dict(self, unit_obj, bdict):
        super(ComRemoteControl8011, self).init_from_dict(unit_obj, bdict)

    def destroy(self):
        if self._delay_exe_id:
            delay.cancel(self._delay_exe_id)
            self._delay_exe_id = None
        super(ComRemoteControl8011, self).destroy()
        return

    def on_action_start(self, action_type, *args):
        if action_type in self.ACTION_MAP:
            action_handle = getattr(self, self.ACTION_MAP[action_type] + '_start')
            if action_handle:
                action_handle(*args)

    def on_action_stop(self, action_type):
        if action_type in self.ACTION_MAP:
            action_handle = getattr(self, self.ACTION_MAP[action_type] + '_stop')
            if action_handle:
                action_handle()

    def main_weapon_attack_start(self, target_id, pos, is_hit):
        self._attack_time = tutil.get_time()
        enemy_pos = self.ev_g_enemy_pos()
        if enemy_pos:
            self.send_event('E_CTRL_FACE_TO', enemy_pos, False)
        self.ev_g_try_enter(mecha_status_config.MC_SHOOT)

    def main_weapon_attack_stop(self):
        self.ev_g_try_exit(mecha_status_config.MC_SHOOT)

    def on_enter_state(self, sid):
        if sid == mecha_status_config.MC_SECOND_WEAPON_ATTACK:

            def cast_skill():
                self._delay_exe_id = None
                if not self or not self.is_valid():
                    return
                else:
                    model = self.ev_g_model()
                    if model and model.valid:
                        self.ev_g_try_exit(mecha_status_config.MC_SECOND_WEAPON_ATTACK)
                    return

            self._delay_exe_id = delay.call(random.uniform(0.6, 1.3), lambda : cast_skill())

    def sub_weapon_attack_start(self, target_id, pos):
        self._attack_time = tutil.get_time()
        self.main_weapon_attack_stop()
        enemy_pos = self.ev_g_enemy_pos()
        if enemy_pos:
            self.send_event('E_CTRL_FACE_TO', enemy_pos, False)
        self.ev_g_try_enter(mecha_status_config.MC_SECOND_WEAPON_ATTACK)

    def jump_start(self):
        self.ev_g_try_enter(mecha_status_config.MC_JUMP_1)

    def dash_start(self, dash_dir):
        self.main_weapon_attack_stop()
        if self.ev_g_in_dragon_shape():
            enemy_pos = self.ev_g_enemy_pos()
            if enemy_pos:
                self.send_event('E_CTRL_FACE_TO', enemy_pos, False)
            pitch = math.radians(random.randint(10, 30))
            self.send_event('E_CAM_PITCH', pitch)
            self.send_event('E_ACTION_SYNC_HEAD_PITCH', pitch)
            self.ev_g_try_enter(mecha_status_config.MC_DASH)
        else:
            self.ev_g_try_enter(mecha_status_config.MC_DASH_1)

    def on_get_weapon_type(self):
        wp = self.sd.ref_wp_bar_mp_weapons[1]
        return wp.get_id()

    def ext_start(self, pos, shape):
        if self._delay_exe_id:
            return
        self.ev_g_try_enter(mecha_status_config.MC_TRANSFORM)

    def is_in_attack_time(self):
        if tutil.get_time() - self._attack_time <= 1:
            return True
        return False