# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/behavior/PVEMonsterEvadeLogic.py
from __future__ import absolute_import
from .MonsterStateBase import MonsterStateBase
import math3d
from logic.gcommon.common_const.character_anim_const import LOW_BODY
from common.utils.timer import LOGIC
from logic.gutils.pve_utils import get_aim_pos
from math import pi

class MonsterEvadeBase(MonsterStateBase):
    BIND_EVENT = {'E_ACTIVE_PARAM_STATE': 'pre_check_param'
       }
    econf = {}
    S_END = -1
    S_PRE = 1
    S_EVD = 2
    S_LAND = 3
    S_BAC = 4
    AIM_GAP = 0.05 * pi

    def pre_check_param(self, state, *args):
        if state != self.sid:
            return
        if self.is_active:
            return False
        if not self.check_can_active():
            return False
        self.editor_handle()
        self.skill_id, self.target_id, self.target_pos = args
        if self.target_pos:
            self.target_pos = math3d.vector(*self.target_pos)
        self.active_self()

    def init_from_dict(self, unit_obj, bdict, sid, info):
        super(MonsterEvadeBase, self).init_from_dict(unit_obj, bdict, sid, info)
        self.init_params()
        self.process_event(True)
        self.sub_state = self.S_END

    def init_params(self):
        self.target_id = None
        self.target_pos = None
        self.dash_time = 0
        self.turn_ts = 0
        self.turn_timer = None
        self.turn_tag = False
        self.next_state = 0
        return

    def editor_handle(self):
        pass

    def process_event(self, is_bind):
        emgr = global_data.emgr
        if is_bind:
            emgr.bind_events(self.econf)
        else:
            emgr.unbind_events(self.econf)

    def on_init_complete(self):
        super(MonsterEvadeBase, self).on_init_complete()
        self.register_evade_callbacks()

    def register_evade_callbacks(self):
        self.register_substate_callback(self.S_PRE, 0, self.start_pre)
        self.register_substate_callback(self.S_PRE, self.pre_anim_dur / self.pre_anim_rate, self.end_pre)
        self.register_substate_callback(self.S_EVD, 0, self.start_evd)
        self.register_substate_callback(self.S_EVD, self.max_evd_time, self.end_evd)
        self.register_substate_callback(self.S_BAC, 0, self.start_bac)
        self.register_substate_callback(self.S_BAC, self.bac_anim_dur / self.bac_anim_rate, self.end_bac)

    def start_pre(self):
        self.send_event('E_DO_SKILL', self.skill_id)
        self.send_event('E_ANIM_RATE', LOW_BODY, self.pre_anim_rate)
        self.send_event('E_POST_ACTION', self.pre_anim, LOW_BODY, 1)
        self.calc_dash_time()

    def end_pre(self):
        self.reset_sub_states_callback()
        self.register_evade_callbacks()
        start_land_ts = self.dash_time - self.land_anim_dur / self.land_anim_rate
        if start_land_ts > 0:
            self.register_substate_callback(self.S_EVD, start_land_ts, self.start_land)
        self.sub_state = self.S_EVD

    def start_evd(self):
        self.send_event('E_ANIM_RATE', LOW_BODY, self.evd_anim_rate)
        if self.evd_anim:
            self.send_event('E_POST_ACTION', self.evd_anim, LOW_BODY, 1, loop=True)
        self.init_dash()
        start_land_ts = self.dash_time - self.land_anim_dur / self.land_anim_rate
        if start_land_ts < 0:
            self.start_land()

    def end_evd(self):
        self.sub_state = self.S_BAC
        self.send_event('E_CLEAR_SPEED')
        self.unregist_event('E_ON_TOUCH_GROUND', self.on_ground)

    def start_land(self):
        self.send_event('E_ANIM_RATE', LOW_BODY, self.land_anim_rate)
        self.send_event('E_POST_ACTION', self.land_anim, LOW_BODY, 1)

    def start_bac(self):
        self.send_event('E_ANIM_RATE', LOW_BODY, self.bac_anim_rate)
        if self.bac_anim:
            self.send_event('E_POST_ACTION', self.bac_anim, LOW_BODY, 1)

    def end_bac(self):
        self.sub_state = self.S_END

    def init_dash(self):
        dash_dir = self.target_pos - self.ev_g_position()
        dash_hrz_dis = math3d.vector(dash_dir.x, 0, dash_dir.z).length
        dash_time = dash_hrz_dis / self.evd_speed
        if dash_time > self.max_evd_time:
            dash_time = self.max_evd_time
        air_time = dash_time * 0.5
        vertical_speed = abs(air_time * self.gravity)
        self.dash_time = dash_time
        dash_dir.normalize()
        tar_dir = dash_dir * self.evd_speed
        self.send_event('E_SET_WALK_DIRECTION', tar_dir)
        self.send_event('E_GRAVITY', self.gravity)
        self.send_event('E_JUMP', vertical_speed)
        self.unregist_event('E_ON_TOUCH_GROUND', self.on_ground)
        self.regist_event('E_ON_TOUCH_GROUND', self.on_ground)

    def calc_dash_time(self):
        pos = self.ev_g_position()
        dash_dir = self.target_pos - pos
        dash_hrz_dis = math3d.vector(dash_dir.x, 0, dash_dir.z).length
        dash_time = dash_hrz_dis / self.evd_speed
        if dash_time > self.max_evd_time:
            dash_time = self.max_evd_time
        self.dash_time = dash_time

    def on_ground(self, *args):
        self.end_evd()

    def enter(self, leave_states):
        super(MonsterEvadeBase, self).enter(leave_states)
        self.send_event('E_CALL_SYNC_METHOD', 'pve_enter_skill', (self.skill_id,), True)
        self.sub_state = self.S_PRE
        self.turn_ts = 0
        self.turn_tag = False

    def update(self, dt):
        super(MonsterEvadeBase, self).update(dt)
        if self.sub_state == self.S_END:
            self.disable_self()
        self.turn_ts += dt
        if not self.turn_tag:
            if self.turn_ts > self.turn_start_ts:
                self.init_turn()

    def exit(self, enter_states):
        super(MonsterEvadeBase, self).exit(enter_states)
        self.sub_state = self.S_END
        if self.next_state:
            self.send_event('E_PVE_SET_LEADER_STATE', self.next_state, self.sid, self.skill_id, self.target_id, self.target_pos)
            self.send_event('E_ACTIVE_STATE', self.next_state)
        else:
            self.send_event('E_CALL_SYNC_METHOD', 'pve_end_skill', (self.skill_id,), True)
        self.reset_turn_timer()

    def destroy(self):
        self.process_event(False)
        self.reset_turn_timer()
        super(MonsterEvadeBase, self).destroy()

    def init_turn(self):
        self.reset_turn_timer()
        self.turn_timer = global_data.game_mgr.register_logic_timer(self.tick_turn, 1, None, -1, LOGIC, True)
        self.turn_tag = True
        return

    def tick_turn(self, dt):
        target_pos = get_aim_pos(self.target_id, self.target_pos)
        ori_pos = self.ev_g_position()
        tar_dir = target_pos - ori_pos
        tar_yaw = tar_dir.yaw + 2 * pi
        ori_yaw = self.ev_g_forward().yaw + 2 * pi
        diff_yaw = tar_yaw - ori_yaw
        if diff_yaw < -pi:
            diff_yaw += 2 * pi
        else:
            if diff_yaw > pi:
                diff_yaw -= 2 * pi
            if abs(diff_yaw) < self.AIM_GAP:
                return
        if diff_yaw < 0:
            ret_yaw = ori_yaw - self.turn_speed * dt
        else:
            ret_yaw = ori_yaw + self.turn_speed * dt
        self.send_event('E_CAM_YAW', ret_yaw)
        self.send_event('E_ACTION_SYNC_YAW', ret_yaw)

    def reset_turn_timer(self):
        if self.turn_timer:
            global_data.game_mgr.unregister_logic_timer(self.turn_timer)
            self.turn_timer = None
        return


class MonsterEvade(MonsterEvadeBase):

    def init_params(self):
        super(MonsterEvade, self).init_params()
        self.skill_id = self.custom_param.get('skill_id', 9011355)
        self.evd_speed = self.custom_param.get('evd_speed', 800)
        self.max_evd_time = self.custom_param.get('max_evd_time', 0.5)
        self.gravity = self.custom_param.get('gravity', 1000)
        self.pre_anim = self.custom_param.get('pre_anim', 'jump_02')
        self.pre_anim_dur = self.custom_param.get('pre_anim_dur', 0.667)
        self.pre_anim_rate = self.custom_param.get('pre_anim_rate', 2.0)
        self.evd_anim = self.custom_param.get('evd_anim', 'jump_04')
        self.evd_anim_rate = self.custom_param.get('evd_anim_rate', 1.0)
        self.land_anim = self.custom_param.get('land_anim', None)
        self.land_anim_dur = self.custom_param.get('land_anim_dur', 0)
        self.land_anim_rate = self.custom_param.get('land_anim_rate', 1.0)
        self.bac_anim = self.custom_param.get('bac_anim', 'jump_05')
        self.bac_anim_dur = self.custom_param.get('bac_anim_dur', 0.9)
        self.bac_anim_rate = self.custom_param.get('bac_anim_rate', 1.0)
        self.turn_start_ts = self.custom_param.get('turn_start_ts', 0.5)
        self.turn_speed = self.custom_param.get('turn_speed', 3 * pi)
        self.next_state = self.custom_param.get('next_state', 0)
        return

    def editor_handle(self):
        if global_data.use_sunshine:
            self.init_params()
            self.reset_sub_states_callback()
            self.register_evade_callbacks()