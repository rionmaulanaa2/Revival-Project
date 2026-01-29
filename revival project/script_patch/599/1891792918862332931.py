# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/com_ai_ctrl/ComRemoteControl8009.py
from __future__ import absolute_import
from logic.gcommon.component.UnitCom import UnitCom
from logic.gcommon.common_const import ai_const
from logic.gcommon.cdata import mecha_status_config
from logic.gcommon import time_utility as tutil
import math3d
import time
import logic.gcommon.const as g_const
import random
from common.utils.timer import CLOCK

class ComRemoteControl8009(UnitCom):
    BIND_EVENT = {'E_CTRL_ACTION_START': 'on_action_start',
       'E_CTRL_ACTION_STOP': 'on_action_stop',
       'G_WEAPON_TYPE': 'on_get_weapon_type',
       'E_ENTER_STATE': 'on_enter_state',
       'E_LEAVE_STATE': 'on_leave_state'
       }
    ACTION_MAP = {ai_const.CTRL_ACTION_MAIN: 'main_weapon_attack',
       ai_const.CTRL_ACTION_SUB: 'sub_weapon_attack',
       ai_const.CTRL_ACTION_JUMP: 'jump',
       ai_const.CTRL_ACTION_RUSH: 'dash'
       }

    def __init__(self):
        super(ComRemoteControl8009, self).__init__()

    def init_from_dict(self, unit_obj, bdict):
        super(ComRemoteControl8009, self).init_from_dict(unit_obj, bdict)

    def destroy(self):
        super(ComRemoteControl8009, self).destroy()

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
        if self._is_in_second_weapon_time() or self._is_in_dash_time():
            return
        if self._is_in_transform_time():
            self.ev_g_try_enter(mecha_status_config.MC_FULL_FORCE_SHOOT)
        else:
            self.ev_g_try_enter(mecha_status_config.MC_SHOOT)

    def main_weapon_attack_stop(self):
        self.ev_g_try_exit(mecha_status_config.MC_SHOOT)
        self.ev_g_try_exit(mecha_status_config.MC_FULL_FORCE_SHOOT)

    def on_enter_state(self, sid):
        if sid == mecha_status_config.MC_SECOND_WEAPON_ATTACK:

            def cast_skill():
                if not self or not self.is_valid():
                    return
                model = self.ev_g_model()
                if model and model.valid:
                    self.ev_g_try_exit(mecha_status_config.MC_SECOND_WEAPON_ATTACK)

            global_data.game_mgr.delay_exec(random.uniform(2, 3), cast_skill)

    def on_leave_state(self, sid, new_state=None):
        if sid == mecha_status_config.MC_DASH:
            self.main_weapon_attack_stop()

    def sub_weapon_attack_start(self, target_id, pos):
        if self._is_in_dash_time() or self._is_in_transform_time() or self._is_in_second_weapon_time():
            return
        self.main_weapon_attack_stop()
        self.ev_g_try_enter(mecha_status_config.MC_SECOND_WEAPON_ATTACK)

    def jump_start(self):
        self.ev_g_try_enter(mecha_status_config.MC_JUMP_1)

    def dash_start(self, dash_dir):
        if self._is_in_dash_time() or self._is_in_transform_time() or self._is_in_second_weapon_time():
            return
        self.main_weapon_attack_stop()
        self.ev_g_try_enter(mecha_status_config.MC_DASH)

    def on_get_weapon_type(self):
        wp = self.sd.ref_wp_bar_mp_weapons[1]
        return wp.get_id()

    def _is_in_dash_time(self):
        if mecha_status_config.MC_DASH in self.ev_g_cur_state():
            return True
        return False

    def _is_in_transform_time(self):
        if mecha_status_config.MC_TRANSFORM in self.ev_g_cur_state():
            return True
        return False

    def _is_in_second_weapon_time(self):
        if mecha_status_config.MC_SECOND_WEAPON_ATTACK in self.ev_g_cur_state():
            return True
        return False