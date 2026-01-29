# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/com_ai_ctrl/ComRemoteControl8006.py
from __future__ import absolute_import
from logic.gcommon.component.UnitCom import UnitCom
from logic.gcommon.common_const import ai_const
from logic.gcommon.cdata import mecha_status_config
import math3d
import random

class ComRemoteControl8006(UnitCom):
    BIND_EVENT = {'E_CTRL_ACTION_START': 'on_action_start',
       'E_CTRL_ACTION_STOP': 'on_action_stop',
       'E_FALL': 'on_fall',
       'E_ENTER_STATE': 'on_enter_state',
       'G_WEAPON_TYPE': 'on_get_weapon_type'
       }
    ACTION_MAP = {ai_const.CTRL_ACTION_MAIN: 'main_weapon_attack',
       ai_const.CTRL_ACTION_SUB: 'sub_weapon_attack',
       ai_const.CTRL_ACTION_JUMP: 'jump',
       ai_const.CTRL_ACTION_RUSH: 'dash'
       }

    def __init__(self):
        super(ComRemoteControl8006, self).__init__()

    def init_from_dict(self, unit_obj, bdict):
        super(ComRemoteControl8006, self).init_from_dict(unit_obj, bdict)

    def destroy(self):
        super(ComRemoteControl8006, self).destroy()

    def on_enter_state(self, sid):
        if sid == mecha_status_config.MC_SECOND_WEAPON_ATTACK:

            def cast_skill():
                if not self or not self.is_valid():
                    return
                model = self.ev_g_model()
                if model and model.valid:
                    self.ev_g_try_exit(mecha_status_config.MC_SECOND_WEAPON_ATTACK)

            global_data.game_mgr.delay_exec(random.uniform(1, 3), cast_skill)

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
        self.ev_g_try_enter(mecha_status_config.MC_SHOOT)

    def main_weapon_attack_stop(self):
        self.ev_g_try_exit(mecha_status_config.MC_SHOOT)

    def sub_weapon_attack_start(self, target_id, pos):
        self.main_weapon_attack_stop()
        self.ev_g_try_enter(mecha_status_config.MC_SECOND_WEAPON_ATTACK)

    def jump_start(self):
        self.main_weapon_attack_stop()
        self.ev_g_try_enter(mecha_status_config.MC_JUMP_1)

    def on_fall(self, *args):
        if random.uniform(0, 1) < 0.4:
            self.send_event('E_ACTIVE_STATE', mecha_status_config.MC_GLIDE)

    def dash_start(self, dash_dir):
        self.main_weapon_attack_stop()
        self.ev_g_try_enter(mecha_status_config.MC_DASH)

    def on_get_weapon_type(self):
        wp = self.sd.ref_wp_bar_mp_weapons[1]
        return wp.get_id()