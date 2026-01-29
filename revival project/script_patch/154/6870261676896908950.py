# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/com_ai_ctrl/ComRemoteControl8002.py
from __future__ import absolute_import
from logic.gcommon.component.UnitCom import UnitCom
from logic.gcommon.common_const import ai_const
from logic.gcommon.cdata import mecha_status_config
from logic.gcommon import time_utility as tutil
from mobile.common.EntityManager import EntityManager
from logic.gcommon.utility import rand_by_weight
import math3d
import random
import math
import logic.gutils.delay as delay
from logic.gcommon.common_const import buff_const as bconst

class ComRemoteControl8002(UnitCom):
    BIND_EVENT = {'E_CTRL_ACTION_START': 'on_action_start',
       'E_CTRL_ACTION_STOP': 'on_action_stop',
       'E_ENTER_STATE': 'on_enter_state',
       'G_WEAPON_TYPE': 'on_get_weapon_type',
       'E_CTRL_MOVE_TO': 'move_to'
       }
    ACTION_MAP = {ai_const.CTRL_ACTION_MAIN: 'main_weapon_attack',
       ai_const.CTRL_ACTION_SUB: 'sub_weapon_attack',
       ai_const.CTRL_ACTION_JUMP: 'jump',
       ai_const.CTRL_ACTION_RUSH: 'dash'
       }

    def __init__(self):
        super(ComRemoteControl8002, self).__init__()
        self._shoot_jump_time = 0

    def init_from_dict(self, unit_obj, bdict):
        super(ComRemoteControl8002, self).init_from_dict(unit_obj, bdict)

    def destroy(self):
        super(ComRemoteControl8002, self).destroy()

    def on_enter_state(self, sid):
        pass

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
        self.ev_g_try_enter(mecha_status_config.MC_SWORD_ENERGY)
        self.check_shoot_jump()

    def main_weapon_attack_stop(self):
        self.ev_g_try_exit(mecha_status_config.MC_SWORD_ENERGY)

    def sub_weapon_attack_start(self, target_id, pos):
        self.main_weapon_attack_stop()
        self.ev_g_try_enter(mecha_status_config.MC_WHIRLWIND)

    def jump_start(self):
        if not self.unit_obj:
            return
        if self.unit_obj.ev_g_has_buff_by_id(bconst.BUFF_ID_8034_GROUNDED):
            return
        status = self.ev_g_get_status_by_action('action5')
        if status:
            self.ev_g_try_enter(status)

    def dash_start(self, enemy_id):
        self.main_weapon_attack_stop()
        m_pos = self.ev_g_position()
        if enemy_id:
            enemy = EntityManager.getentity(enemy_id)
            enemy = enemy.logic.ev_g_control_target() if enemy and enemy.logic.ev_g_is_in_mecha() else enemy
            if enemy:
                enemy_pos = enemy.logic.ev_g_model_position()
                dash_dir = m_pos - enemy_pos
                agl_range = rand_by_weight({(-60, 60): 20,(60, 300): 80})
                agl = math.radians(random.uniform(*agl_range))
                dash_dir = dash_dir * math3d.matrix.make_rotation_y(agl)
                yaw = dash_dir.yaw
                self.send_event('E_CAM_YAW', yaw)
                self.send_event('E_ACTION_SYNC_YAW', yaw)
        else:
            enemy_pos = self.ev_g_enemy_pos()
            if enemy_pos:
                dash_dir = enemy_pos - m_pos
                agl_range = rand_by_weight({(-20, 20): 80,(20, 340): 20})
                agl = math.radians(random.uniform(*agl_range))
                dash_dir = dash_dir * math3d.matrix.make_rotation_y(agl)
                yaw = dash_dir.yaw
                self.send_event('E_CAM_YAW', yaw)
                self.send_event('E_ACTION_SYNC_YAW', yaw)
        self.ev_g_try_enter(mecha_status_config.MC_DASH)

    def on_get_weapon_type(self):
        wp = self.sd.ref_wp_bar_mp_weapons[1]
        return wp.get_id()

    def move_to(self, pos, move_syn=None):
        if random.randint(1, 100) <= 30:
            self.try_combo_jump()

    def check_shoot_jump(self):
        now = tutil.get_time()
        if now < self._shoot_jump_time:
            return
        self._shoot_jump_time = now + random.uniform(0.5, 1.2)
        self.try_combo_jump()

    def try_combo_jump(self):
        self.jump_start()
        if random.random() < min(0.4, self.battle.get_ai_level() / 0.6):
            delay.call(random.uniform(0, 0.5), lambda : self.jump_start())