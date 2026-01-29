# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/behavior/PVEMonsterMultiMeleeLogic.py
from __future__ import absolute_import
from .MonsterStateBase import MonsterStateBase
from logic.gutils.slash_utils import SlashChecker
from logic.gcommon.const import NEOX_UNIT_SCALE
from logic.gcommon.common_const.character_anim_const import LOW_BODY
from logic.gcommon.cdata.pve_monster_status_config import MC_MONSTER_AIMTURN
import math3d
import world
from logic.gutils.pve_utils import get_aim_pos

class MonsterMultiMeleeBase(MonsterStateBase):
    BIND_EVENT = {'E_PVE_SET_LEADER_STATE': 'set_leader_state',
       'E_ACTIVE_PARAM_STATE': 'pre_check_param'
       }
    econf = {}
    S_END = -1
    S_PRE = 1
    S_ATK = 2
    S_BAC = 3

    def set_leader_state(self, t_state, l_state, skill_id, *args):
        if t_state != self.sid:
            return
        self.leader_state = l_state
        self.leader_skill_id = skill_id
        self.target_id, self.target_pos = args

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
            self.leader_state = None
            self.leader_skill_id = None
            self.active_self()
            return

    def init_from_dict(self, unit_obj, bdict, sid, info):
        super(MonsterMultiMeleeBase, self).init_from_dict(unit_obj, bdict, sid, info)
        self.init_params()
        self.process_event(True)

    def init_params(self):
        self.leader_state = None
        self.leader_skill_id = None
        self.slash_checker = None
        self.is_atking = False
        self.fire_count = 1
        self.fire_idx = 0
        self.pre_face_to_ts = 0
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
        super(MonsterMultiMeleeBase, self).on_init_complete()
        self.reset_melee_state()

    def reset_melee_state(self):
        self.reset_sub_states_callback()
        self.pre_anim = self.pre_anim_list[self.fire_idx]
        self.pre_anim_dur = self.pre_anim_dur_list[self.fire_idx]
        self.pre_anim_rate = self.pre_anim_rate_list[self.fire_idx]
        self.atk_anim = self.atk_anim_list[self.fire_idx]
        self.atk_anim_dur = self.atk_anim_dur_list[self.fire_idx]
        self.atk_anim_rate = self.atk_anim_rate_list[self.fire_idx]
        self.bac_anim = self.bac_anim_list[self.fire_idx]
        self.bac_anim_dur = self.bac_anim_dur_list[self.fire_idx]
        self.bac_anim_rate = self.bac_anim_rate_list[self.fire_idx]
        self.register_melee_callbacks()
        self.reset_hit_range()

    def register_melee_callbacks(self):
        self.register_substate_callback(self.S_PRE, 0, self.start_pre)
        self.register_substate_callback(self.S_PRE, self.pre_anim_dur / self.pre_anim_rate, self.end_pre)
        self.register_substate_callback(self.S_ATK, 0, self.start_atk)
        self.register_substate_callback(self.S_ATK, self.atk_anim_dur / self.atk_anim_rate, self.end_atk)
        self.register_substate_callback(self.S_BAC, 0, self.start_bac)
        self.register_substate_callback(self.S_BAC, self.bac_anim_dur / self.bac_anim_rate, self.end_bac)

    def reset_hit_range(self):
        self.hit_range = self.hit_range_list[self.fire_idx]
        hit_width, hit_height, hit_depth = self.hit_range
        hit_width *= NEOX_UNIT_SCALE
        hit_height *= NEOX_UNIT_SCALE
        hit_depth *= NEOX_UNIT_SCALE
        if self.slash_checker:
            self.slash_checker.refresh_hit_range(hit_width, hit_height, hit_depth)
        else:
            self.slash_checker = SlashChecker(self, self.hit_skill_id, (hit_width, hit_height, hit_depth), self.hit_bone, damage_settlement_always_on=True)

    def start_pre(self):
        re_aim = self.re_aim_list[self.fire_idx]
        if re_aim:
            self.send_event('E_CTRL_FACE_TO', get_aim_pos(self.target_id, self.target_pos), False)
        self.pre_face_to_ts = 0
        if self.move_start_ts_list and self.move_end_ts_list:
            self.move_start_ts = self.move_start_ts_list[self.fire_idx]
            self.move_end_ts = self.move_end_ts_list[self.fire_idx]
            if not self.move_start_ts and not self.move_end_ts:
                self.send_event('E_CLEAR_SPEED')
            else:
                self.init_move()
        else:
            self.send_event('E_CLEAR_SPEED')
        if not self.pre_anim_dur:
            return
        self.send_event('E_ANIM_RATE', LOW_BODY, self.pre_anim_rate)
        if self.pre_anim:
            self.send_event('E_POST_ACTION', self.pre_anim, LOW_BODY, 1)

    def end_pre(self):
        self.sub_state = self.S_ATK

    def start_atk(self):
        if not self.atk_anim_dur:
            return
        self.send_event('E_ANIM_RATE', LOW_BODY, self.atk_anim_rate)
        if self.atk_anim:
            self.send_event('E_POST_ACTION', self.atk_anim, LOW_BODY, 1)
        self.is_atking = True
        self.slash_checker.begin_check()
        if global_data.is_inner_server and self.is_draw_col and not global_data.skip_pve_draw_col:
            self.draw_col()

    def end_atk(self):
        self.sub_state = self.S_BAC
        self.is_atking = False
        self.slash_checker.end_check()

    def start_bac(self):
        if not self.bac_anim_dur:
            return
        self.send_event('E_ANIM_RATE', LOW_BODY, self.bac_anim_rate)
        if self.bac_anim:
            self.send_event('E_POST_ACTION', self.bac_anim, LOW_BODY, 1)
        if self.end_aoe_skill_id_list:
            self.end_aoe_skill_id = self.end_aoe_skill_id_list[self.fire_idx]
            if self.end_aoe_skill_id:
                self.send_event('E_DO_SKILL', self.end_aoe_skill_id)
        if self.end_aoe_skill_id_2_list:
            self.end_aoe_skill_id_2 = self.end_aoe_skill_id_2_list[self.fire_idx]
            if self.end_aoe_skill_id_2:
                self.send_event('E_CALL_SYNC_METHOD', 'do_skill', (self.end_aoe_skill_id_2, self.post_data()), False, True)

    def end_bac(self):
        if self.fire_idx < self.fire_count - 1:
            self.fire_idx += 1
            self.reset_melee_state()
            self.sub_state = self.S_PRE
        else:
            self.sub_state = self.S_END

    def enter(self, leave_states):
        super(MonsterMultiMeleeBase, self).enter(leave_states)
        if self.leader_state:
            pass
        else:
            self.send_event('E_CALL_SYNC_METHOD', 'pve_enter_skill', (self.skill_id,), True)
        self.send_event('E_DO_SKILL', self.skill_id)
        self.fire_idx = 0
        self.is_atking = False
        self.reset_melee_state()
        self.sub_state = self.S_PRE

    def update(self, dt):
        super(MonsterMultiMeleeBase, self).update(dt)
        if self.sub_state == self.S_END:
            self.disable_self()
        elif self.sub_state == self.S_PRE and self.pre_face_to_ts < self.pre_face_to_dur:
            self.send_event('E_CTRL_FACE_TO', get_aim_pos(self.target_id, self.target_pos), False)
            self.pre_face_to_ts += dt

    def exit(self, enter_states):
        super(MonsterMultiMeleeBase, self).exit(enter_states)
        if self.is_atking:
            self.is_atking = False
            self.slash_checker.end_check()
        if self.next_state:
            self.send_event('E_PVE_SET_LEADER_STATE', self.next_state, self.sid, self.skill_id, self.target_id, self.target_pos)
            self.send_event('E_ACTIVE_STATE', self.next_state)
        elif self.aim_turn:
            if self.leader_state:
                self.send_event('E_PVE_M_AIM_TURN', self.leader_state, self.leader_skill_id, self.target_id, self.target_pos)
            else:
                self.send_event('E_PVE_M_AIM_TURN', self.sid, self.skill_id, self.target_id, self.target_pos)
            self.send_event('E_ACTIVE_STATE', MC_MONSTER_AIMTURN)
        else:
            self.send_event('E_CALL_SYNC_METHOD', 'pve_end_skill', (self.skill_id,), True)
        if self.move_start_ts_list or self.move_end_ts_list:
            self.end_move()

    def destroy(self):
        self.process_event(False)
        if self.slash_checker:
            self.slash_checker.destroy()
            self.slash_checker = None
        super(MonsterMultiMeleeBase, self).destroy()
        return

    def post_data(self):
        self.end_aoe_skill_socket = self.end_aoe_skill_socket_list[self.fire_idx]
        model = self.ev_g_model()
        mat = model.get_socket_matrix(self.end_aoe_skill_socket, world.SPACE_TYPE_WORLD)
        pos = mat.translation
        data = ((pos.x, pos.y, pos.z),)
        return data

    def init_move(self):
        self.delay_call(self.move_start_ts, self.start_move)

    def start_move(self):
        self.move_speed = self.move_speed_list[self.fire_idx]
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


class MonsterMultiMelee(MonsterMultiMeleeBase):

    def init_params(self):
        super(MonsterMultiMelee, self).init_params()
        self.skill_id = self.custom_param.get('skill_id', 9010151)
        self.hit_skill_id = self.skill_id
        self.fire_count = self.custom_param.get('fire_count', 1)
        self.hit_range_list = self.custom_param.get('hit_range_list', [])
        self.re_aim_list = self.custom_param.get('re_aim_list', [])
        self.pre_anim_list = self.custom_param.get('pre_anim_list', [''])
        self.pre_anim_dur_list = self.custom_param.get('pre_anim_dur_list', [0])
        self.pre_anim_rate_list = self.custom_param.get('pre_anim_rate_list', [1.0])
        self.atk_anim_list = self.custom_param.get('atk_anim_list', [''])
        self.atk_anim_dur_list = self.custom_param.get('atk_anim_dur_list', [0])
        self.atk_anim_rate_list = self.custom_param.get('atk_anim_rate_list', [1.0])
        self.bac_anim_list = self.custom_param.get('bac_anim_list', [''])
        self.bac_anim_dur_list = self.custom_param.get('bac_anim_dur_list', [0])
        self.bac_anim_rate_list = self.custom_param.get('bac_anim_rate_list', [1.0])
        self.end_aoe_skill_id_list = self.custom_param.get('end_aoe_skill_id_list', [])
        self.end_aoe_skill_id_2_list = self.custom_param.get('end_aoe_skill_id_2_list', [])
        self.end_aoe_skill_socket_list = self.custom_param.get('end_aoe_skill_socket_list', [])
        self.aim_turn = self.custom_param.get('aim_turn', True)
        self.is_draw_col = self.custom_param.get('is_draw_col', False)
        self.hit_bone = ()
        self.move_start_ts_list = self.custom_param.get('move_start_ts_list', [])
        self.move_end_ts_list = self.custom_param.get('move_end_ts_list', [])
        self.move_speed_list = self.custom_param.get('move_speed_list', [])
        self.pre_face_to_dur = self.custom_param.get('pre_face_to_dur', 0)
        self.next_state = self.custom_param.get('next_state', 0)

    def editor_handle(self):
        if global_data.use_sunshine:
            self.init_params()
            self.reset_melee_state()