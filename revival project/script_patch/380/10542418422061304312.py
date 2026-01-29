# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/com_ai_ctrl/ComRemoteControl8017.py
from __future__ import absolute_import
from logic.gcommon.component.UnitCom import UnitCom
from logic.gcommon.common_const import ai_const
from logic.gcommon.cdata import mecha_status_config
from logic.gcommon import time_utility as tutil
from mobile.common.EntityManager import EntityManager
from logic.gcommon.common_const import buff_const
from logic.gcommon.utility import rand_by_weight
import math3d
import random
import math
import logic.gutils.delay as delay
from logic.gcommon.common_const import buff_const as bconst

class ComRemoteControl8017(UnitCom):
    BIND_EVENT = {'E_CTRL_ACTION_START': 'on_action_start',
       'E_CTRL_ACTION_STOP': 'on_action_stop',
       'E_ENTER_STATE': 'on_enter_state',
       'G_WEAPON_TYPE': 'on_get_weapon_type',
       'E_CTRL_MOVE_TO': 'move_to',
       'G_IS_IN_ATTACK_TIME': 'is_in_attack_time'
       }
    ACTION_MAP = {ai_const.CTRL_ACTION_MAIN: 'main_weapon_attack',
       ai_const.CTRL_ACTION_SUB: 'sub_weapon_attack',
       ai_const.CTRL_ACTION_JUMP: 'jump',
       ai_const.CTRL_ACTION_RUSH: 'dash'
       }

    def __init__(self):
        super(ComRemoteControl8017, self).__init__()
        self._delay_exe_id = None
        self._shoot_jump_time = 0
        self._attack_time = 0
        return

    def init_from_dict(self, unit_obj, bdict):
        super(ComRemoteControl8017, self).init_from_dict(unit_obj, bdict)

    def destroy(self):
        if self._delay_exe_id:
            delay.cancel(self._delay_exe_id)
            self._delay_exe_id = None
        super(ComRemoteControl8017, self).destroy()
        return

    def on_enter_state(self, sid):
        if sid == mecha_status_config.MC_SECOND_WEAPON_ATTACK:

            def cast_skill():
                if not self or not self.is_valid():
                    return
                else:
                    self._delay_exe_id = None
                    model = self.ev_g_model()
                    if model and model.valid:
                        self.ev_g_try_exit(mecha_status_config.MC_SECOND_WEAPON_ATTACK)
                    return

            self._delay_exe_id = delay.call(random.uniform(0.1, 0.3), lambda : cast_skill())

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
        if self._delay_exe_id:
            return
        self._attack_time = tutil.get_time()
        enemy_pos = self.ev_g_enemy_pos()
        if enemy_pos:
            self.send_event('E_CTRL_FACE_TO', enemy_pos, False)
        if self.ev_g_has_buff_by_id(buff_const.BUFF_ID_8017_EXTRA_WEAPON):
            self.ev_g_try_enter(mecha_status_config.MC_FULL_FORCE_SHOOT)
        else:
            self.ev_g_try_enter(mecha_status_config.MC_SHOOT)
        self.check_shoot_jump()

    def main_weapon_attack_stop(self):
        self.ev_g_try_exit(mecha_status_config.MC_SHOOT)

    def sub_weapon_attack_start(self, target_id, pos):
        if self._delay_exe_id:
            return
        self._attack_time = tutil.get_time()
        self.main_weapon_attack_stop()
        enemy_pos = self.ev_g_enemy_pos()
        if enemy_pos:
            self.send_event('E_CTRL_FACE_TO', enemy_pos, False)
        self.ev_g_try_enter(mecha_status_config.MC_SECOND_WEAPON_ATTACK)

    def jump_start(self):
        if self.unit_obj.ev_g_has_buff_by_id(bconst.BUFF_ID_8034_GROUNDED):
            return
        self.ev_g_try_enter(mecha_status_config.MC_JUMP_1)

    def dash_start(self, enemy_id):
        if self._delay_exe_id:
            return
        else:
            self.main_weapon_attack_stop()
            m_pos = self.ev_g_position()
            if enemy_id is not None:
                enemy = EntityManager.getentity(enemy_id)
                enemy = enemy.logic.ev_g_control_target() if enemy and enemy.logic.ev_g_is_in_mecha() else enemy
                if enemy:
                    enemy_pos = enemy.logic.ev_g_model_position()
                    dash_dir = enemy_pos - m_pos
                    agl_range = rand_by_weight({(-60, 60): 10,(60, 300): 90})
                    agl = math.radians(random.uniform(*agl_range))
                    dash_dir = dash_dir * math3d.matrix.make_rotation_y(agl)
                    yaw = dash_dir.yaw
                    self.send_event('E_CAM_YAW', yaw)
                    self.send_event('E_ACTION_SYNC_YAW', yaw)
            else:
                enemy_pos = self.ev_g_enemy_pos()
                if enemy_pos:
                    dash_dir = enemy_pos - m_pos
                    if enemy_id == -1:
                        agl_range = rand_by_weight({(-45, 45): 90,(45, 315): 10})
                    else:
                        agl_range = rand_by_weight({(-45, 45): 20,(45, 315): 80})
                    agl = math.radians(random.uniform(*agl_range))
                    dash_dir = dash_dir * math3d.matrix.make_rotation_y(agl)
                    yaw = dash_dir.yaw
                    self.send_event('E_CAM_YAW', yaw)
                    self.send_event('E_ACTION_SYNC_YAW', yaw)
            self.ev_g_try_enter(mecha_status_config.MC_DASH)
            return

    def on_get_weapon_type(self):
        wp = self.sd.ref_wp_bar_mp_weapons[1]
        return wp.get_id()

    def move_to(self, pos, move_syn=None):
        if random.randint(1, 100) <= 60:
            self.jump_start()

    def check_shoot_jump(self):
        now = tutil.get_time()
        if now < self._shoot_jump_time:
            return
        self._shoot_jump_time = now + random.uniform(1, 2)
        self.jump_start()

    def is_in_attack_time(self):
        if tutil.get_time() - self._attack_time <= 1:
            return True
        return False