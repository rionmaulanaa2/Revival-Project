# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/behavior/PVEMonsterRollDashLogic.py
from __future__ import absolute_import
from .MonsterStateBase import MonsterStateBase
from logic.gcommon.common_const.character_anim_const import LOW_BODY
import math3d
from logic.gutils.scene_utils import dash_filtrate_hit
from logic.gcommon.cdata.pve_monster_status_config import MC_MONSTER_AIMTURN
from logic.gutils.pve_utils import get_aim_pos
from math import radians
from logic.gcommon.const import NEOX_UNIT_SCALE
from math import pi
from common.utils.timer import CLOCK

class MonsterRollDashBase(MonsterStateBase):
    BIND_EVENT = MonsterStateBase.BIND_EVENT.copy()
    BIND_EVENT.update({'E_ACTIVE_PARAM_STATE': 'pre_check_param'
       })
    econf = {}
    S_END = -1
    S_PRE = 1
    S_DASH = 2
    S_BAC = 3
    A_T = 0.033
    T_M = 0
    T_L = 1
    T_R = 2
    T_ANIM = {T_M: 'dash_anim',
       T_L: 'track_left_anim',
       T_R: 'track_right_anim'
       }

    def pre_check_param(self, state, *args):
        if state != self.sid:
            return
        if self.is_active:
            return False
        if not self.check_can_active():
            return False
        self.editor_handle()
        self.skill_id, self.target_id, self.target_pos = args
        self.target_pos = math3d.vector(*self.target_pos)
        self.active_self()

    def init_from_dict(self, unit_obj, bdict, sid, info):
        super(MonsterRollDashBase, self).init_from_dict(unit_obj, bdict, sid, info)
        self.init_params()
        self.process_event(True)
        self.sub_state = self.S_END

    def init_params(self):
        self.target_id = None
        self.target_pos = None
        self.skill_id = 0
        self.dash_speed = 0
        self.track_timer = None
        self.tick_dur = 0
        self.check_dur = 0
        self.hit_id = set()
        self.check_hit_timer = None
        self.track_lr = self.T_M
        return

    def editor_handle(self):
        pass

    def process_event(self, is_bind):
        emgr = global_data.emgr
        is_bind and emgr.bind_events(self.econf) if 1 else emgr.unbind_events(self.econf)

    def on_init_complete(self):
        super(MonsterRollDashBase, self).on_init_complete()
        self.register_roll_dash_callbacks()

    def register_roll_dash_callbacks(self):
        self.register_substate_callback(self.S_PRE, 0, self.start_pre)
        self.register_substate_callback(self.S_PRE, self.pre_anim_dur / self.pre_anim_rate, self.end_pre)
        self.register_substate_callback(self.S_DASH, 0, self.start_dash)
        self.register_substate_callback(self.S_DASH, self.max_dash_dur, self.end_dash)
        self.register_substate_callback(self.S_BAC, 0, self.start_bac)
        self.register_substate_callback(self.S_BAC, self.bac_anim_dur / self.bac_anim_rate, self.end_bac)

    def start_pre(self):
        self.send_event('E_CLEAR_SPEED')
        self.send_event('E_ANIM_RATE', LOW_BODY, self.pre_anim_rate)
        if self.pre_anim:
            self.send_event('E_POST_ACTION', self.pre_anim, LOW_BODY, 1)

    def end_pre(self):
        if self.begin_aoe_skill_id:
            self.send_event('E_DO_SKILL', self.begin_aoe_skill_id)
        self.sub_state = self.S_DASH

    def start_dash(self):
        self.init_track()
        self.last_pos = self.ev_g_position()
        self.start_check_hit()
        self.send_event('E_ANIM_RATE', LOW_BODY, self.dash_anim_rate)
        if self.dash_anim:
            self.send_event('E_POST_ACTION', self.dash_anim, LOW_BODY, 1, loop=True)

    def end_dash(self):
        self.reset_track_timer()
        self.send_event('E_CLEAR_SPEED')
        self.sub_state = self.S_BAC

    def start_bac(self):
        self.send_event('E_ANIM_RATE', LOW_BODY, self.bac_anim_rate)
        if self.bac_anim:
            self.send_event('E_POST_ACTION', self.bac_anim, LOW_BODY, 1)
        self.stop_check_hit()
        if self.end_aoe_skill_id:
            self.send_event('E_DO_SKILL', self.end_aoe_skill_id)

    def end_bac(self):
        self.sub_state = self.S_END

    def enter(self, leave_states):
        super(MonsterRollDashBase, self).enter(leave_states)
        self.send_event('E_CALL_SYNC_METHOD', 'pve_enter_skill', (self.skill_id,), True)
        self.send_event('E_DO_SKILL', self.skill_id)
        self.send_event('E_DO_OXRUSH_MONSTER', True)
        self.last_pos = self.ev_g_position()
        self.case_exit_tag = False
        self.sub_state = self.S_PRE

    def update(self, dt):
        super(MonsterRollDashBase, self).update(dt)
        if self.sub_state == self.S_END:
            self.disable_self()
        if self.sub_state == self.S_DASH:
            cur_pos = self.ev_g_position()
            if (cur_pos - self.last_pos).length < 2.0 * NEOX_UNIT_SCALE:
                self.tick_dur += dt
            else:
                self.tick_dur = 0
            if self.tick_dur > self.stuck_stop_dur:
                self.sub_state = self.S_BAC
            self.last_pos = cur_pos
            self.check_dur += dt
            if self.check_dur > self.hit_check_dur:
                self.hit_id = set()
                self.check_dur = 0
            if self.case_trans_dis:
                target_pos = get_aim_pos(self.target_id, self.target_pos)
                if (target_pos - cur_pos).length < self.case_trans_dis:
                    self.sub_state = self.S_END
                    self.case_exit_tag = True

    def exit(self, enter_states):
        self.stop_check_hit()
        self.reset_track_timer()
        super(MonsterRollDashBase, self).exit(enter_states)
        self.send_event('E_DO_OXRUSH_MONSTER', False)
        if self.case_exit_tag:
            self.send_event('E_PVE_SET_LEADER_STATE', self.case_trans_state, self.sid, self.skill_id, self.target_id, self.target_pos)
            self.send_event('E_ACTIVE_STATE', self.case_trans_state)
        elif self.aim_turn:
            self.send_event('E_PVE_M_AIM_TURN', self.sid, self.skill_id, self.target_id, math3d.vector(0, 0, 0))
            self.send_event('E_ACTIVE_STATE', MC_MONSTER_AIMTURN)
        else:
            self.send_event('E_CALL_SYNC_METHOD', 'pve_end_skill', (self.skill_id,), True)

    def destroy(self):
        self.stop_check_hit()
        self.reset_track_timer()
        self.process_event(False)
        super(MonsterRollDashBase, self).destroy()

    def init_track(self):
        self.reset_track_timer()
        self.tick_dur = 0
        self.check_dur = 0
        self.last_pos = self.ev_g_position()
        self.track_lr = self.T_M
        self.track_timer = global_data.game_mgr.register_logic_timer(self.tick_track, self.A_T, None, -1, CLOCK, True)
        return

    def tick_track(self, dt):
        target_pos = get_aim_pos(self.target_id, self.target_pos)
        ori_pos = self.ev_g_position()
        if not target_pos or not ori_pos:
            self.reset_track_timer()
            self.disable_self()
            return
        tar_dir = target_pos - ori_pos
        tar_yaw = tar_dir.yaw + 2 * pi
        ori_yaw = self.ev_g_forward().yaw + 2 * pi
        diff_yaw = tar_yaw - ori_yaw
        if diff_yaw < -pi:
            diff_yaw += 2 * pi
        elif diff_yaw > pi:
            diff_yaw -= 2 * pi
        if diff_yaw < 0:
            ret_yaw = ori_yaw - self.track_speed * dt
            if self.track_left_trigger_angle and abs(diff_yaw) > self.track_left_trigger_angle:
                lr_tag = self.T_L
            else:
                lr_tag = self.T_M
        else:
            ret_yaw = ori_yaw + self.track_speed * dt
            if self.track_right_trigger_angle and abs(diff_yaw) > self.track_right_trigger_angle:
                lr_tag = self.T_R
            else:
                lr_tag = self.T_M
        if lr_tag != self.track_lr:
            key = self.T_ANIM[lr_tag]
            anim = getattr(self, key)
            rate = getattr(self, key + '_rate')
            self.send_event('E_ANIM_RATE', LOW_BODY, rate)
            self.send_event('E_POST_ACTION', anim, LOW_BODY, 1, loop=True)
            self.track_lr = lr_tag
        self.send_event('E_CAM_YAW', ret_yaw)
        self.send_event('E_ACTION_SYNC_YAW', ret_yaw)
        forward = self.ev_g_forward()
        self.send_event('E_SET_WALK_DIRECTION', forward * self.dash_speed)

    def reset_track_timer(self):
        if self.track_timer:
            global_data.game_mgr.unregister_logic_timer(self.track_timer)
            self.track_timer = None
        return

    def start_check_hit(self):
        self.clear_check_hit_timer()
        self.check_hit_timer = global_data.game_mgr.get_logic_timer().register(func=self._check_hit, mode=2, interval=0.1)

    def stop_check_hit(self):
        self.clear_check_hit_timer()
        self.hit_id = set()

    def _check_hit(self):
        ret_dict = self.get_hit_ret()
        if ret_dict:
            self.send_event('E_CALL_SYNC_METHOD', 'skill_hit_on_target', (self.skill_id, ret_dict), False, True)

    def get_hit_ret(self):
        height, radius = self.col_info
        hit_ret = {}
        cur_pos = self.ev_g_position()
        forward = self.ev_g_forward()
        if global_data.player and global_data.player.logic:
            pos = cur_pos + math3d.vector(0, height, 0)
            if global_data.is_inner_server and self.is_draw_col and not global_data.skip_pve_draw_col:
                global_data.emgr.scene_draw_wireframe_event.emit(pos, math3d.matrix(), 10, length=(radius * 2, radius * 2, radius * 2))
            hit_units = global_data.emgr.scene_get_hit_all_enemy_unit.emit(self.unit_obj.ev_g_camp_id(), pos, radius)
            if hit_units and hit_units[0]:
                for unit in hit_units[0]:
                    unit_id = unit.id
                    if unit_id not in self.hit_id:
                        if dash_filtrate_hit(self.unit_obj, unit):
                            continue
                        self.hit_id.add(unit_id)
                        unit_pos = unit.ev_g_position()
                        temp_d = unit_pos - cur_pos
                        temp_d.normalize()
                        cos_phi = forward.dot(temp_d)
                        ret = cur_pos + forward * (unit_pos - cur_pos).length * cos_phi
                        hit_ret[unit_id] = (ret.x, ret.y, ret.z)

        return hit_ret

    def clear_check_hit_timer(self):
        if self.check_hit_timer:
            global_data.game_mgr.get_logic_timer().unregister(self.check_hit_timer)
            self.check_hit_timer = None
        return


class MonsterRollDash(MonsterRollDashBase):

    def init_params(self):
        super(MonsterRollDash, self).init_params()
        self.skill_id = self.custom_param.get('skill_id', 0)
        self.dash_speed = self.custom_param.get('dash_speed', 0)
        self.max_dash_dur = self.custom_param.get('max_dash_dur', 0)
        self.track_speed = self.custom_param.get('track_speed', 0)
        self.stuck_stop_dur = self.custom_param.get('stuck_stop_dur', 0)
        self.hit_check_dur = self.custom_param.get('hit_check_dur', 0)
        self.case_trans_dis = self.custom_param.get('case_trans_dis', 0) * NEOX_UNIT_SCALE
        self.case_trans_state = self.custom_param.get('case_trans_state', 0)
        self.pre_anim = self.custom_param.get('pre_anim', '')
        self.pre_anim_dur = self.custom_param.get('pre_anim_dur', 0)
        self.pre_anim_rate = self.custom_param.get('pre_anim_rate', 1.0)
        self.dash_anim = self.custom_param.get('dash_anim', '')
        self.dash_anim_rate = self.custom_param.get('dash_anim_rate', 1.0)
        self.bac_anim = self.custom_param.get('bac_anim', '')
        self.bac_anim_dur = self.custom_param.get('bac_anim_dur', 0)
        self.bac_anim_rate = self.custom_param.get('bac_anim_rate', 1.0)
        self.track_left_anim = self.custom_param.get('track_left_anim', '')
        self.track_left_anim_rate = self.custom_param.get('track_left_anim_rate', 1.0)
        self.track_left_trigger_angle = radians(self.custom_param.get('track_left_trigger_angle', 0))
        self.track_right_anim = self.custom_param.get('track_right_anim', '')
        self.track_right_anim_rate = self.custom_param.get('track_right_anim_rate', 1.0)
        self.track_right_trigger_angle = radians(self.custom_param.get('track_right_trigger_angle', 0))
        self.begin_aoe_skill_id = self.custom_param.get('begin_aoe_skill_id', None)
        self.end_aoe_skill_id = self.custom_param.get('end_aoe_skill_id', None)
        self.col_info = self.custom_param.get('col_info', [30, 100])
        self.is_draw_col = self.custom_param.get('is_draw_col', False)
        self.aim_turn = self.custom_param.get('aim_turn', False)
        return

    def editor_handle(self):
        if global_data.use_sunshine:
            self.init_params()
            self.reset_sub_states_callback()
            self.register_roll_dash_callbacks()