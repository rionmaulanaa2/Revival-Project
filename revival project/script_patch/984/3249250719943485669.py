# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/behavior/PVEMonsterDashLogic.py
from __future__ import absolute_import
from .MonsterStateBase import MonsterStateBase
from logic.gutils.character_ctrl_utils import AirWalkDirectionSetter
from logic.gcommon.common_const.character_anim_const import LOW_BODY
import math3d
from logic.gutils.scene_utils import dash_filtrate_hit
from logic.gcommon.cdata.pve_monster_status_config import MC_MONSTER_AIMTURN
from logic.gutils.pve_utils import get_aim_pos, get_bias_aim_pos

class MonsterDashBase(MonsterStateBase):
    BIND_EVENT = MonsterStateBase.BIND_EVENT.copy()
    BIND_EVENT.update({'E_ACTIVE_PARAM_STATE': 'pre_check_param'
       })
    econf = {}
    S_END = -1
    S_PRE = 1
    S_DASH = 2
    S_BAC = 3
    F_DIRE = 1
    F_GROUND = 2
    F_GROUND_TRACK = 3
    T_TARGET = 1
    T_POINT = 2

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
        super(MonsterDashBase, self).init_from_dict(unit_obj, bdict, sid, info)
        self.init_params()
        self.air_walk_direction_setter = AirWalkDirectionSetter(self)
        self.process_event(True)
        self.sub_state = self.S_END

    def init_params(self):
        self.target_id = None
        self.target_pos = None
        self.skill_id = 0
        self.last_position = math3d.vector(0, 0, 0)
        self.force_on_ground = False
        self.dash_count = 1
        self.dash_idx = 0
        self.dash_dur = 0
        self.dash_speed = 0
        self.dash_dire = None
        self.bias_dur = 0
        self.hit_id = set()
        self.check_hit_timer = None
        return

    def editor_handle(self):
        pass

    def process_event(self, is_bind):
        emgr = global_data.emgr
        is_bind and emgr.bind_events(self.econf) if 1 else emgr.unbind_events(self.econf)

    def on_init_complete(self):
        super(MonsterDashBase, self).on_init_complete()
        self.reset_dash_state()
        self.bias_dur = self.sd.ref_bias_dur

    def reset_dash_state(self):
        self.reset_sub_states_callback()
        self.pre_anim_dur = self.pre_anim_dur_list[self.dash_idx]
        self.pre_anim_rate = self.pre_anim_rate_list[self.dash_idx]
        self.dash_dur = self.dash_dur_list[self.dash_idx]
        self.bac_anim_dur = self.bac_anim_dur_list[self.dash_idx]
        self.bac_anim_rate = self.bac_anim_rate_list[self.dash_idx]
        self.register_dash_callbacks()

    def register_dash_callbacks(self):
        self.register_substate_callback(self.S_PRE, 0, self.start_pre)
        self.register_substate_callback(self.S_PRE, self.pre_anim_dur / self.pre_anim_rate, self.end_pre)
        self.register_substate_callback(self.S_DASH, 0, self.start_dash)
        self.register_substate_callback(self.S_DASH, self.dash_dur, self.end_dash)
        self.register_substate_callback(self.S_BAC, 0, self.start_bac)
        self.register_substate_callback(self.S_BAC, self.bac_anim_dur / self.bac_anim_rate, self.end_bac)

    def start_pre(self):
        self.send_event('E_CLEAR_SPEED')
        self.send_event('E_ANIM_RATE', LOW_BODY, self.pre_anim_rate)
        self.pre_anim = self.pre_anim_list[self.dash_idx]
        if self.pre_anim:
            self.send_event('E_POST_ACTION', self.pre_anim, LOW_BODY, 1)
        self.calc_dash_dire()

    def end_pre(self):
        if self.begin_aoe_skill_ids:
            skill_id = self.begin_aoe_skill_ids[self.dash_idx]
            skill_id and self.send_event('E_DO_SKILL', skill_id)
        self.sub_state = self.S_DASH

    def start_dash(self):
        self.start_check_hit()
        self.send_event('E_ANIM_RATE', LOW_BODY, self.dash_anim_rate)
        self.dash_anim = self.dash_anim_list[self.dash_idx]
        if self.dash_anim:
            self.send_event('E_POST_ACTION', self.dash_anim, LOW_BODY, 1, loop=True)
        self.dash_speed = self.dash_speed_list[self.dash_idx]
        if self.dash_form == self.F_DIRE:
            self.send_event('E_GRAVITY', 0)
            self.air_walk_direction_setter.execute(self.dash_dire * self.dash_speed)
        elif self.dash_form in (self.F_GROUND, self.F_GROUND_TRACK):
            self.send_event('E_SET_WALK_DIRECTION', self.dash_dire * self.dash_speed)

    def calc_dash_dire(self):
        if not self.target_id and not self.target_pos:
            self.disable_self()
            return False
        else:
            if self.target_scene_point_list:
                target_pos = math3d.vector(*self.target_scene_point_list[self.dash_idx])
                self.send_event('E_CTRL_FACE_TO', get_aim_pos(None, target_pos, True))
            else:
                target_pos = get_bias_aim_pos(self.target_id, self.target_pos, True, self.bias_dur)
                self.send_event('E_CTRL_FACE_TO', get_bias_aim_pos(self.target_id, self.target_pos, True, self.bias_dur), False)
            start_pos = self.ev_g_position()
            if not target_pos or not start_pos:
                self.disable_self()
                return False
            self.dash_dire = target_pos - start_pos
            self.start_pos = start_pos
            if not self.target_id or self.dash_type == self.T_POINT:
                self.dash_dur = self.dash_dire.length / self.dash_speed
            if self.dash_form == self.F_DIRE:
                self.dash_dire.y = self.fix_offset
                self.last_position = self.ev_g_position()
            elif self.dash_form in (self.F_GROUND, self.F_GROUND_TRACK):
                self.dash_dire.y = 0
            self.dash_dire.normalize()
            return True

    def end_dash(self):
        self.send_event('E_CLEAR_SPEED')
        if self.dash_form == self.F_DIRE:
            self.send_event('E_RESET_GRAVITY')
        self.sub_state = self.S_BAC

    def start_bac(self):
        self.send_event('E_ANIM_RATE', LOW_BODY, self.bac_anim_rate)
        self.bac_anim = self.bac_anim_list[self.dash_idx]
        if self.bac_anim:
            self.send_event('E_POST_ACTION', self.bac_anim, LOW_BODY, 1)
        self.stop_check_hit()
        if self.end_aoe_skill_ids:
            skill_id = self.end_aoe_skill_ids[self.dash_idx]
            skill_id and self.send_event('E_DO_SKILL', skill_id)

    def end_bac(self):
        if self.dash_idx < self.dash_count - 1:
            self.dash_idx += 1
            self.reset_dash_state()
            self.sub_state = self.S_PRE
        else:
            self.sub_state = self.S_END

    def enter(self, leave_states):
        super(MonsterDashBase, self).enter(leave_states)
        self.send_event('E_CALL_SYNC_METHOD', 'pve_enter_skill', (self.skill_id,), True)
        self.air_walk_direction_setter.reset()
        self.send_event('E_DO_SKILL', self.skill_id)
        self.send_event('E_DO_OXRUSH_MONSTER', True)
        self.dash_idx = 0
        self.reset_dash_state()
        self.sub_state = self.S_PRE

    def update(self, dt):
        super(MonsterDashBase, self).update(dt)
        if self.sub_state == self.S_END:
            self.disable_self()
        elif self.sub_state == self.S_PRE and self.elapsed_time < self.pre_face_to_dur:
            self.send_event('E_CTRL_FACE_TO', get_aim_pos(self.target_id, self.target_pos), False)
        if not self.target_id or self.dash_type == self.T_POINT:
            if self.elapsed_time > self.dash_dur and self.sub_state == self.S_DASH:
                self.sub_state = self.S_BAC
        if self.dash_form == self.F_GROUND_TRACK and self.sub_state == self.S_DASH:
            self.fix_dire()

    def fix_dire(self):
        if self.dash_form == self.F_GROUND_TRACK:
            if not self.dash_dire:
                return
            if not self.target_id or not self.target_pos:
                self.disable_self()
                return False
            tar_pos = get_aim_pos(self.target_id, self.target_pos)
            start_pos = self.ev_g_position()
            tar_dire = tar_pos - start_pos
            tar_dire.y = 0
            tar_dire.normalize()
            dash_dire = math3d.vector(0, 0, 0)
            dash_dire.intrp(self.dash_dire, tar_dire, self.track_ratio)
            dash_dire.normalize()
            self.dash_dire = dash_dire
            self.send_event('E_SET_WALK_DIRECTION', self.dash_dire * self.dash_speed)
            self.send_event('E_CTRL_FACE_TO', tar_pos, False)
            return True

    def exit(self, enter_states):
        self.clear_check_hit_timer()
        super(MonsterDashBase, self).exit(enter_states)
        self.send_event('E_DO_OXRUSH_MONSTER', False)
        if self.aim_turn:
            self.send_event('E_PVE_M_AIM_TURN', self.sid, self.skill_id, self.target_id, math3d.vector(0, 0, 0))
            self.send_event('E_ACTIVE_STATE', MC_MONSTER_AIMTURN)
        else:
            self.send_event('E_CALL_SYNC_METHOD', 'pve_end_skill', (self.skill_id,), True)

    def destroy(self):
        self.clear_check_hit_timer()
        self.process_event(False)
        if self.air_walk_direction_setter:
            self.air_walk_direction_setter.destroy()
            self.air_walk_direction_setter = None
        super(MonsterDashBase, self).destroy()
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
        if global_data.player and global_data.player.logic:
            pos = self.ev_g_position() + math3d.vector(0, height, 0)
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
                        temp_d = unit_pos - self.start_pos
                        temp_d.normalize()
                        cos_phi = self.dash_dire.dot(temp_d)
                        ret = self.start_pos + self.dash_dire * (unit_pos - self.start_pos).length * cos_phi
                        hit_ret[unit_id] = (ret.x, ret.y, ret.z)

        return hit_ret

    def clear_check_hit_timer(self):
        if self.check_hit_timer:
            global_data.game_mgr.get_logic_timer().unregister(self.check_hit_timer)
            self.check_hit_timer = None
        return


class MonsterDash(MonsterDashBase):

    def init_params(self):
        super(MonsterDash, self).init_params()
        self.skill_id = self.custom_param.get('skill_id', 0)
        self.dash_form = self.custom_param.get('dash_form', 1)
        self.fix_offset = self.custom_param.get('fix_offset', 0)
        self.track_ratio = self.custom_param.get('track_ratio', 0)
        self.dash_type = self.custom_param.get('dash_type', 1)
        self.dash_count = self.custom_param.get('dash_count', 1)
        self.dash_dur_list = self.custom_param.get('dash_dur_list', [0])
        self.dash_dur = self.dash_dur_list[self.dash_idx]
        self.dash_speed_list = self.custom_param.get('dash_speed_list', [0])
        self.dash_speed = self.dash_speed_list[self.dash_idx]
        self.target_scene_point_list = self.custom_param.get('target_scene_point_list', [])
        self.pre_anim_list = self.custom_param.get('pre_anim_list', [''])
        self.pre_anim = self.pre_anim_list[self.dash_idx]
        self.pre_anim_dur_list = self.custom_param.get('pre_anim_dur_list', [0])
        self.pre_anim_dur = self.pre_anim_dur_list[self.dash_idx]
        self.pre_anim_rate_list = self.custom_param.get('pre_anim_rate_list', [1.0])
        self.pre_anim_rate = self.pre_anim_rate_list[self.dash_idx]
        self.dash_anim_list = self.custom_param.get('dash_anim_list', [''])
        self.dash_anim = self.dash_anim_list[self.dash_idx]
        self.dash_anim_rate_list = self.custom_param.get('dash_anim_rate_list', [1.0])
        self.dash_anim_rate = self.dash_anim_rate_list[self.dash_idx]
        self.bac_anim_list = self.custom_param.get('bac_anim_list', [''])
        self.bac_anim = self.bac_anim_list[self.dash_idx]
        self.bac_anim_dur_list = self.custom_param.get('bac_anim_dur_list', [0])
        self.bac_anim_dur = self.bac_anim_dur_list[self.dash_idx]
        self.bac_anim_rate_list = self.custom_param.get('bac_anim_rate_list', [1.0])
        self.bac_anim_rate = self.bac_anim_rate_list[self.dash_idx]
        self.begin_aoe_skill_ids = self.custom_param.get('begin_aoe_skill_ids', [])
        self.end_aoe_skill_ids = self.custom_param.get('end_aoe_skill_ids', [])
        self.col_info = self.custom_param.get('col_info', [30, 100])
        self.is_draw_col = self.custom_param.get('is_draw_col', False)
        self.aim_turn = self.custom_param.get('aim_turn', False)
        self.pre_face_to_dur = self.custom_param.get('pre_face_to_dur', 0)

    def editor_handle(self):
        if global_data.use_sunshine:
            self.init_params()
            self.bias_dur = self.sd.ref_bias_dur
            self.reset_sub_states_callback()
            self.register_dash_callbacks()