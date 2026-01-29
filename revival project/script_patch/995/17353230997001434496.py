# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/behavior/PVEMonsterEvadeMeleeLogic.py
from __future__ import absolute_import
import math3d
from logic.gcommon.common_const.character_anim_const import LOW_BODY
from common.utils.timer import LOGIC
from logic.gutils.pve_utils import get_aim_pos
from math import pi
from logic.gcommon.const import NEOX_UNIT_SCALE
from logic.gutils.slash_utils import SlashChecker
from .MonsterStateBase import MonsterStateBase
from logic.gcommon.cdata.pve_monster_status_config import MC_MONSTER_AIMTURN

class MonsterEvadeMeleeBase(MonsterStateBase):
    BIND_EVENT = {'E_ACTIVE_PARAM_STATE': 'pre_check_param'
       }
    econf = {}
    S_END = -1
    S_PRE = 1
    S_EVD = 2
    S_LAND = 3
    S_BAC = 4
    S_MELEE_PRE = 5
    S_MELEE_ATK = 6
    S_MELEE_BAC = 7
    AIM_GAP = 0.05 * pi

    def pre_check_param(self, state, *args):
        if state != self.sid:
            return
        else:
            if self.is_active:
                return False
            if not self.check_can_active():
                return False
            self.editor_handle()
            self.skill_id, self.target_id, self.target_pos = args
            self.hit_skill_id = self.skill_id
            self.target_pos = math3d.vector(*self.target_pos) if self.target_pos else None
            self.active_self()
            return

    def init_from_dict(self, unit_obj, bdict, sid, info):
        super(MonsterEvadeMeleeBase, self).init_from_dict(unit_obj, bdict, sid, info)
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
        self.slash_checker = None
        self.is_atking = False
        return

    def editor_handle(self):
        pass

    def process_event(self, is_bind):
        emgr = global_data.emgr
        is_bind and emgr.bind_events(self.econf) if 1 else emgr.unbind_events(self.econf)

    def on_init_complete(self):
        super(MonsterEvadeMeleeBase, self).on_init_complete()
        self.register_evade_callbacks()
        self.register_melee_callbacks()
        self.reset_hit_range()

    def register_evade_callbacks(self):
        self.register_substate_callback(self.S_PRE, 0, self.start_pre)
        self.register_substate_callback(self.S_PRE, self.pre_anim_dur / self.pre_anim_rate, self.end_pre)
        self.register_substate_callback(self.S_EVD, 0, self.start_evd)
        self.register_substate_callback(self.S_EVD, self.max_evd_time, self.end_evd)
        self.register_substate_callback(self.S_BAC, 0, self.start_bac)
        self.register_substate_callback(self.S_BAC, self.bac_anim_dur / self.bac_anim_rate, self.end_bac)

    def register_melee_callbacks(self):
        self.register_substate_callback(self.S_MELEE_PRE, 0, self.melee_start_pre)
        self.register_substate_callback(self.S_MELEE_PRE, self.melee_pre_anim_dur / self.melee_pre_anim_rate, self.melee_end_pre)
        self.register_substate_callback(self.S_MELEE_ATK, 0, self.melee_start_atk)
        self.register_substate_callback(self.S_MELEE_ATK, self.melee_atk_anim_dur / self.melee_atk_anim_rate, self.melee_end_atk)
        self.register_substate_callback(self.S_MELEE_BAC, 0, self.melee_start_bac)
        self.register_substate_callback(self.S_MELEE_BAC, self.melee_bac_anim_dur / self.melee_bac_anim_rate, self.melee_end_bac)

    def reset_hit_range(self):
        hit_width, hit_height, hit_depth = self.hit_range
        hit_width *= NEOX_UNIT_SCALE
        hit_height *= NEOX_UNIT_SCALE
        hit_depth *= NEOX_UNIT_SCALE
        if self.slash_checker:
            self.slash_checker.destroy()
        self.slash_checker = SlashChecker(self, self.hit_skill_id, (hit_width, hit_height, hit_depth), self.hit_bone, damage_settlement_always_on=True)

    def start_pre(self):
        if not self.pre_anim_dur:
            return
        self.send_event('E_ANIM_RATE', LOW_BODY, self.pre_anim_rate)
        if self.pre_anim:
            self.send_event('E_POST_ACTION', self.pre_anim, LOW_BODY, 1)
        self.calc_dash_time()

    def end_pre(self):
        self.reset_sub_state_callback(self.S_EVD)
        self.register_substate_callback(self.S_EVD, 0, self.start_evd)
        self.register_substate_callback(self.S_EVD, self.max_evd_time, self.end_evd)
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
        if self.land_anim:
            self.send_event('E_POST_ACTION', self.land_anim, LOW_BODY, 1)

    def start_bac(self):
        if not self.bac_anim_dur:
            return
        self.send_event('E_ANIM_RATE', LOW_BODY, self.bac_anim_rate)
        if self.bac_anim:
            self.send_event('E_POST_ACTION', self.bac_anim, LOW_BODY, 1)

    def end_bac(self):
        self.sub_state = self.S_MELEE_PRE

    def melee_start_pre(self):
        if not self.melee_pre_anim_dur:
            return
        self.send_event('E_ANIM_RATE', LOW_BODY, self.melee_pre_anim_rate)
        if self.melee_pre_anim:
            self.send_event('E_POST_ACTION', self.melee_pre_anim, LOW_BODY, 1)
        if not self.move_start_ts and not self.move_end_ts:
            self.send_event('E_CLEAR_SPEED')
        else:
            self.init_move()

    def melee_end_pre(self):
        self.sub_state = self.S_MELEE_ATK

    def melee_start_atk(self):
        if not self.melee_atk_anim_dur:
            return
        self.send_event('E_ANIM_RATE', LOW_BODY, self.melee_atk_anim_rate)
        if self.melee_atk_anim:
            self.send_event('E_POST_ACTION', self.melee_atk_anim, LOW_BODY, 1)
        self.is_atking = True
        self.slash_checker.begin_check()
        if global_data.is_inner_server and self.is_draw_col and not global_data.skip_pve_draw_col:
            self.draw_col()

    def melee_end_atk(self):
        self.sub_state = self.S_MELEE_BAC
        self.is_atking = False
        self.slash_checker.end_check()

    def melee_start_bac(self):
        if not self.melee_bac_anim_dur:
            return
        self.send_event('E_ANIM_RATE', LOW_BODY, self.melee_bac_anim_rate)
        if self.melee_bac_anim:
            self.send_event('E_POST_ACTION', self.melee_bac_anim, LOW_BODY, 1)
        if self.end_aoe_skill_id:
            self.send_event('E_DO_SKILL', self.end_aoe_skill_id)
        if self.end_aoe_skill_id_2:
            self.send_event('E_CALL_SYNC_METHOD', 'do_skill', (self.end_aoe_skill_id_2, self.post_data()), False, True)

    def melee_end_bac(self):
        self.sub_state = self.S_END

    def enter(self, leave_states):
        super(MonsterEvadeMeleeBase, self).enter(leave_states)
        self.send_event('E_CALL_SYNC_METHOD', 'pve_enter_skill', (self.skill_id,), True)
        self.send_event('E_DO_SKILL', self.skill_id)
        self.turn_ts = 0
        self.turn_tag = False
        self.is_atking = False
        self.sub_state = self.S_PRE

    def update(self, dt):
        super(MonsterEvadeMeleeBase, self).update(dt)
        if self.sub_state == self.S_END:
            self.disable_self()
        self.turn_ts += dt
        if not self.turn_tag:
            if self.turn_ts > self.turn_start_ts:
                self.init_turn()

    def exit(self, enter_states):
        super(MonsterEvadeMeleeBase, self).exit(enter_states)
        self.sub_state = self.S_END
        self.reset_turn_timer()
        if self.is_atking:
            self.is_atking = False
            self.slash_checker.end_check()
        if self.aim_turn:
            self.send_event('E_PVE_M_AIM_TURN', self.sid, self.skill_id, self.target_id, self.target_pos)
            self.send_event('E_ACTIVE_STATE', MC_MONSTER_AIMTURN)
        else:
            self.send_event('E_CALL_SYNC_METHOD', 'pve_end_skill', (self.skill_id,), True)
        if self.move_start_ts or self.move_end_ts:
            self.end_move()

    def destroy(self):
        self.process_event(False)
        self.reset_turn_timer()
        if self.slash_checker:
            self.slash_checker.destroy()
            self.slash_checker = None
        super(MonsterEvadeMeleeBase, self).destroy()
        return

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

    def post_data(self):
        model = self.ev_g_model()
        mat = model.get_socket_matrix(self.end_aoe_skill_socket, 1)
        pos = mat.translation
        data = ((pos.x, pos.y, pos.z),)
        return data

    def init_move(self):
        self.delay_call(self.move_start_ts, self.start_move)

    def start_move(self):
        forward = self.ev_g_forward()
        forward.normalize()
        self.send_event('E_SET_WALK_DIRECTION', forward * self.move_speed)
        self.delay_call(self.move_end_ts - self.move_start_ts, self.end_move)

    def end_move(self):
        self.send_event('E_CLEAR_SPEED')

    def draw_col(self):
        mat = self.ev_g_model().rotation_matrix
        hit_width, hit_height, hit_depth = self.hit_range
        hit_width *= NEOX_UNIT_SCALE
        hit_height *= NEOX_UNIT_SCALE
        hit_depth *= NEOX_UNIT_SCALE
        pos = self.ev_g_position() + math3d.vector(0, hit_height / 2.0 - NEOX_UNIT_SCALE, 0)
        global_data.emgr.scene_draw_wireframe_event.emit(pos, mat, 10, length=(hit_width, hit_height, hit_depth))


class MonsterEvadeMelee(MonsterEvadeMeleeBase):

    def init_params(self):
        super(MonsterEvadeMelee, self).init_params()
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
        self.turn_speed = self.custom_param.get('turn_speed', 8.0)
        self.hit_range = self.custom_param.get('hit_range', [8, 5, 4])
        self.hit_skill_id = self.skill_id
        self.melee_pre_anim = self.custom_param.get('melee_pre_anim', None)
        self.melee_pre_anim_dur = self.custom_param.get('melee_pre_anim_dur', 0)
        self.melee_pre_anim_rate = self.custom_param.get('melee_pre_anim_rate', 1.0)
        self.melee_atk_anim = self.custom_param.get('melee_atk_anim', None)
        self.melee_atk_anim_dur = self.custom_param.get('melee_atk_anim_dur', 0)
        self.melee_atk_anim_rate = self.custom_param.get('melee_atk_anim_rate', 1.0)
        self.melee_bac_anim = self.custom_param.get('melee_bac_anim', None)
        self.melee_bac_anim_dur = self.custom_param.get('melee_bac_anim_dur', 0)
        self.melee_bac_anim_rate = self.custom_param.get('melee_bac_anim_rate', 1.0)
        self.end_aoe_skill_id = self.custom_param.get('end_aoe_skill_id', 0)
        self.end_aoe_skill_id_2 = self.custom_param.get('end_aoe_skill_id_2', 0)
        self.end_aoe_skill_socket = self.custom_param.get('end_aoe_skill_socket', 'fx_root')
        self.aim_turn = self.custom_param.get('aim_turn', True)
        self.is_draw_col = self.custom_param.get('is_draw_col', False)
        self.hit_bone = ()
        self.need_stop = True
        self.move_start_ts = self.custom_param.get('move_start_ts', None)
        self.move_end_ts = self.custom_param.get('move_end_ts', None)
        self.move_speed = self.custom_param.get('move_speed', None)
        return

    def editor_handle(self):
        if global_data.use_sunshine:
            self.init_params()
            self.reset_sub_states_callback()
            self.register_evade_callbacks()
            self.register_melee_callbacks()
            self.reset_hit_range()