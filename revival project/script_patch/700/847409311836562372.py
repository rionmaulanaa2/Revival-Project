# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/com_ai_ctrl/ComRemoteControl8021.py
from __future__ import absolute_import
from logic.gcommon.component.UnitCom import UnitCom
from logic.gcommon.common_const import ai_const
from logic.gcommon.cdata import mecha_status_config
import math3d
import random
import math
from logic.gcommon.const import NEOX_UNIT_SCALE
from collision import INCLUDE_FILTER
from logic.gcommon.common_const.collision_const import LAND_GROUP
from logic.gutils import detection_utils
from logic.gcommon.common_const.skill_const import SKILL_SHOCK_WAVE
from logic.gcommon import time_utility as tutil
from math3d import matrix
import logic.gutils.delay as delay
from logic.gcommon.common_const import buff_const as bconst

class ComRemoteControl8021(UnitCom):
    BIND_EVENT = {'E_CTRL_ACTION_START': 'on_action_start',
       'E_CTRL_ACTION_STOP': 'on_action_stop',
       'G_WEAPON_TYPE': 'on_get_weapon_type',
       'E_ENTER_STATE': 'on_enter_state',
       'G_ROCKET_JUMP_POS': 'get_rocket_jump_pos',
       'E_ENTER_SLASH_HOLD': 'end_button_down',
       'E_CTRL_MOVE_TO': 'move_to'
       }
    ACTION_MAP = {ai_const.CTRL_ACTION_MAIN: 'main_weapon_attack',
       ai_const.CTRL_ACTION_SUB: 'sub_weapon_attack',
       ai_const.CTRL_ACTION_JUMP: 'jump',
       ai_const.CTRL_ACTION_RUSH: 'dash'
       }

    def __init__(self):
        super(ComRemoteControl8021, self).__init__()
        self._delay_exe_id = None
        return

    def init_from_dict(self, unit_obj, bdict):
        super(ComRemoteControl8021, self).init_from_dict(unit_obj, bdict)
        self._rocket_jump_pos = None
        self._is_second_weapon_need_hold = True
        self._shoot_jump_time = 0
        return

    def destroy(self):
        if self._delay_exe_id:
            delay.cancel(self._delay_exe_id)
            self._delay_exe_id = None
        super(ComRemoteControl8021, self).destroy()
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
        if self._delay_exe_id:
            return
        self.ev_g_try_enter(mecha_status_config.MC_SHOOT)
        self.check_shoot_jump()

    def main_weapon_attack_stop(self):
        self.ev_g_try_exit(mecha_status_config.MC_SHOOT)

    def on_enter_state(self, sid):
        pass

    def sub_weapon_attack_start(self, target_id, pos):
        if self._delay_exe_id:
            return
        if pos == -1:
            self._is_second_weapon_need_hold = False
        self.main_weapon_attack_stop()
        self.ev_g_try_enter(mecha_status_config.MC_SECOND_WEAPON_ATTACK)

    def jump_start(self):
        if self.unit_obj.ev_g_has_buff_by_id(bconst.BUFF_ID_8034_GROUNDED):
            return
        self.ev_g_try_enter(mecha_status_config.MC_JUMP_1)

    def on_get_weapon_type(self):
        wp = self.sd.ref_wp_bar_mp_weapons[1]
        return wp.get_id()

    def get_dash_pos_1(self):
        enemy_pos = self.ev_g_enemy_pos()
        m_pos = self.ev_g_position()
        if m_pos is None:
            return
        else:
            s_pos = math3d.vector(m_pos.x, m_pos.y + 7.5 * NEOX_UNIT_SCALE, m_pos.z)
            direction = m_pos - enemy_pos
            if direction is None:
                return
            agl = random.uniform(-15.0, 15.0)
            agl = math.radians(agl)
            direction = direction * matrix.make_rotation_y(agl)
            if direction.is_zero:
                return
            direction.normalize()
            r = random.uniform(0, 5) * NEOX_UNIT_SCALE
            e_pos = enemy_pos + direction * r
            if e_pos.x - s_pos.x == 0 and e_pos.z - s_pos.z == 0:
                return
            tp1 = math3d.vector(e_pos.x, 4000, e_pos.z)
            tp2 = math3d.vector(e_pos.x, -4000, e_pos.z)
            ret = self.scene.scene_col.hit_by_ray(tp1, tp2, 0, LAND_GROUP, LAND_GROUP, INCLUDE_FILTER)
            if ret and ret[0]:
                e_pos.y = ret[1].y
            else:
                return
            valid_start = math3d.vector(m_pos.x, m_pos.y + NEOX_UNIT_SCALE, m_pos.z)
            valid_end = math3d.vector(e_pos.x, m_pos.y + NEOX_UNIT_SCALE, e_pos.z)
            valid_ret = self.scene.scene_col.hit_by_ray(valid_start, valid_end, 0, LAND_GROUP, LAND_GROUP, INCLUDE_FILTER, False)
            if not valid_ret[0]:
                return e_pos
            point = detection_utils.get_no_obstacle(self.scene, e_pos, s_pos)
            if point:
                return point
            return
            return

    def get_dash_pos_2(self):
        cur_yaw = self.ev_g_yaw()
        if cur_yaw is None:
            return
        else:
            m_pos = self.ev_g_position()
            if m_pos is None:
                return
            s_pos = math3d.vector(m_pos.x, m_pos.y + 7.5 * NEOX_UNIT_SCALE, m_pos.z)
            direction = self.ev_g_forward()
            if direction is None:
                return
            agl = random.uniform(-15.0, 15.0)
            agl = math.radians(agl)
            direction = direction * matrix.make_rotation_y(agl)
            r = random.uniform(1, 40.0) * NEOX_UNIT_SCALE
            e_pos = m_pos + direction * r
            tp1 = math3d.vector(e_pos.x, 4000, e_pos.z)
            tp2 = math3d.vector(e_pos.x, -4000, e_pos.z)
            ret = self.scene.scene_col.hit_by_ray(tp1, tp2, 0, LAND_GROUP, LAND_GROUP, INCLUDE_FILTER)
            if ret and ret[0]:
                e_pos.y = ret[1].y
            else:
                return
            valid_start = math3d.vector(m_pos.x, m_pos.y + NEOX_UNIT_SCALE, m_pos.z)
            valid_end = math3d.vector(e_pos.x, m_pos.y + NEOX_UNIT_SCALE, e_pos.z)
            valid_ret = self.scene.scene_col.hit_by_ray(valid_start, valid_end, 0, LAND_GROUP, LAND_GROUP, INCLUDE_FILTER, False)
            if not valid_ret[0]:
                return e_pos
            point = detection_utils.get_no_obstacle(self.scene, e_pos, s_pos)
            if point:
                return point
            return
            return

    def dash_start(self, dash_dir):
        if self._delay_exe_id:
            return
        else:
            if self._rocket_jump_pos:
                return
            if len(dash_dir) == 3:
                self.send_event('E_CTRL_FACE_TO', dash_dir)
                self._rocket_jump_pos = math3d.vector(*dash_dir)
            else:
                enemy_pos = self.ev_g_enemy_pos()
                m_pos = self.ev_g_position()
                if enemy_pos and (enemy_pos - m_pos).length / NEOX_UNIT_SCALE <= 70:
                    pos = self.get_dash_pos_1()
                else:
                    pos = self.get_dash_pos_2()
                if pos is None:
                    return
                if pos.y - m_pos.y > 45 * NEOX_UNIT_SCALE:
                    return
                self._rocket_jump_pos = pos
            self.ev_g_try_enter(mecha_status_config.MC_DASH)
            global_data.game_mgr.delay_exec(random.uniform(0, 0.4), self.exec_dash)
            return

    def exec_dash(self):
        self.ev_g_try_exit(mecha_status_config.MC_DASH)
        if self._rocket_jump_pos:
            self.regist_event('E_ON_TOUCH_GROUND', self.exec_dash_callback)

    def exec_dash_callback(self, *_):
        self.unregist_event('E_ON_TOUCH_GROUND', self.exec_dash_callback)
        self._rocket_jump_pos = None
        self.send_event('E_SYNC_STATE_DATA', 'arrive_suc', True)
        return

    def get_rocket_jump_pos(self):
        return self._rocket_jump_pos

    def end_button_down(self, *args):

        def cast_skill():
            if not self or not self.is_valid():
                return
            else:
                self._delay_exe_id = None
                model = self.ev_g_model()
                if model and model.valid:
                    self.ev_g_try_exit(mecha_status_config.MC_SECOND_WEAPON_ATTACK)
                    self._is_second_weapon_need_hold = True
                return

        delay_time = random.uniform(0.2, 0.5) if self._is_second_weapon_need_hold else 0
        self._delay_exe_id = delay.call(delay_time, lambda : cast_skill())

    def move_to(self, pos, move_syn=None):
        if random.randint(1, 100) <= 60:
            self.jump_start()

    def check_shoot_jump(self):
        now = tutil.get_time()
        if now < self._shoot_jump_time:
            return
        self._shoot_jump_time = now + random.uniform(1.5, 3)
        self.jump_start()