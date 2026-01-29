# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/behavior/PVEMonsterFlameLogic.py
from __future__ import absolute_import
from .MonsterStateBase import MonsterStateBase
from logic.gutils.slash_utils import SlashChecker
from logic.gcommon.const import NEOX_UNIT_SCALE
from logic.gcommon.common_const.character_anim_const import LOW_BODY
from logic.gcommon.cdata.pve_monster_status_config import MC_STAND, MC_MONSTER_AIMTURN
import math3d
from logic.gutils.pve_utils import get_aim_pos

class MonsterFlameBase(MonsterStateBase):
    BIND_EVENT = {'E_ACTIVE_PARAM_STATE': 'pre_check_param'
       }
    econf = {}
    S_END = -1
    S_PRE = 1
    S_ATK = 2
    S_BAC = 3

    def pre_check_param(self, state, *args):
        if state != self.sid:
            return
        else:
            self.editor_handle()
            self.skill_id, self.target_id, self.target_pos = args
            self.hit_skill_id = self.skill_id
            if self.target_pos:
                self.target_pos = math3d.vector(*self.target_pos) if 1 else None
                if self.is_active:
                    return False
                return self.check_can_active() or False
            self.active_self()
            return

    def init_from_dict(self, unit_obj, bdict, sid, info):
        super(MonsterFlameBase, self).init_from_dict(unit_obj, bdict, sid, info)
        self.init_params()
        self.process_event(True)

    def init_params(self):
        self.slash_checker = None
        self.hit_idx = 0
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
        super(MonsterFlameBase, self).on_init_complete()
        self.register_flame_callbacks()
        self.reset_hit_range()

    def register_flame_callbacks(self):
        self.register_substate_callback(self.S_PRE, 0, self.start_pre)
        self.register_substate_callback(self.S_PRE, self.pre_anim_dur / self.pre_anim_rate, self.end_pre)
        self.register_substate_callback(self.S_ATK, 0, self.start_atk)
        self.register_substate_callback(self.S_ATK, self.atk_anim_dur / self.atk_anim_rate, self.end_atk)
        self.register_substate_callback(self.S_BAC, 0, self.start_bac)
        self.register_substate_callback(self.S_BAC, self.bac_anim_dur / self.bac_anim_rate, self.end_bac)

    def reset_hit_range(self):
        hit_width, hit_height, hit_depth = self.hit_range
        hit_width *= NEOX_UNIT_SCALE
        hit_height *= NEOX_UNIT_SCALE
        hit_depth *= NEOX_UNIT_SCALE
        if self.slash_checker:
            self.slash_checker.destroy()
        self.slash_checker = SlashChecker(self, self.hit_skill_id, (hit_width, hit_height, hit_depth), self.hit_bone, damage_settlement_always_on=True)

    def start_pre(self):
        self.send_event('E_DO_SKILL', self.skill_id)
        if not self.pre_anim_dur:
            return
        self.send_event('E_ANIM_RATE', LOW_BODY, self.pre_anim_rate)
        if self.pre_anim:
            self.send_event('E_POST_ACTION', self.pre_anim, LOW_BODY, 1)
        if not self.move_start_ts and not self.move_end_ts:
            self.send_event('E_CLEAR_SPEED')
        self.send_event('E_CTRL_FACE_TO', get_aim_pos(self.target_id, self.target_pos), False)

    def end_pre(self):
        self.sub_state = self.S_ATK

    def start_atk(self):
        if not self.atk_anim_dur:
            return
        self.send_event('E_ANIM_RATE', LOW_BODY, self.atk_anim_rate)
        if self.atk_anim:
            self.send_event('E_POST_ACTION', self.atk_anim, LOW_BODY, 1, loop=True)
        self.init_flame()

    def init_flame(self):
        if self.sub_state != self.S_ATK:
            return
        if self.hit_idx < len(self.hit_seq):
            forward = self.ev_g_forward()
            forward_bias = forward * self.forward_offset * NEOX_UNIT_SCALE
            right_fix = self.hit_seq[self.hit_idx]
            right = self.ev_g_rotation().get_right()
            right_bias = right * right_fix * NEOX_UNIT_SCALE
            height_bias = math3d.vector(0, 1, 0) * self.height_offset * NEOX_UNIT_SCALE
            pos_bias = right_bias + forward_bias + height_bias
            self.slash_checker.update_pos_bias(pos_bias)
            self.slash_checker.begin_check()
            self.delay_call(self.hit_interval, self.apply_flame)

    def apply_flame(self):
        self.slash_checker.end_check()
        if global_data.is_inner_server and self.is_draw_col and not global_data.skip_pve_draw_col:
            self.draw_col()
        if self.sub_state != self.S_ATK:
            return
        self.hit_idx += 1
        if self.hit_idx < len(self.hit_seq):
            self.init_flame()

    def end_atk(self):
        self.sub_state = self.S_BAC

    def start_bac(self):
        if not self.bac_anim_dur:
            return
        self.send_event('E_ANIM_RATE', LOW_BODY, self.bac_anim_rate)
        if self.bac_anim:
            self.send_event('E_POST_ACTION', self.bac_anim, LOW_BODY, 1)

    def end_bac(self):
        self.sub_state = self.S_END

    def enter(self, *args):
        super(MonsterFlameBase, self).enter(*args)
        self.send_event('E_CALL_SYNC_METHOD', 'pve_enter_skill', (self.skill_id,), True)
        self.sub_state = self.S_PRE
        self.hit_idx = 0
        if self.move_start_ts or self.move_end_ts:
            self.init_move()

    def update(self, dt):
        super(MonsterFlameBase, self).update(dt)
        if self.sub_state == self.S_END:
            self.disable_self()

    def exit(self, *args):
        super(MonsterFlameBase, self).exit(*args)
        self.slash_checker.end_check()
        if self.aim_turn:
            self.send_event('E_PVE_M_AIM_TURN', self.sid, self.skill_id, self.target_id, self.target_pos)
            self.send_event('E_ACTIVE_STATE', MC_MONSTER_AIMTURN)
        else:
            self.send_event('E_CALL_SYNC_METHOD', 'pve_end_skill', (self.skill_id,), True)
        if self.move_start_ts or self.move_end_ts:
            self.end_move()

    def destroy(self):
        if self.slash_checker:
            self.slash_checker.destroy()
            self.slash_checker = None
        super(MonsterFlameBase, self).destroy()
        return

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
        forward = self.ev_g_forward()
        forward_bias = forward * self.forward_offset * NEOX_UNIT_SCALE
        right_fix = self.hit_seq[self.hit_idx]
        right = self.ev_g_rotation().get_right()
        right_bias = right * right_fix * NEOX_UNIT_SCALE
        height_bias = math3d.vector(0, 1, 0) * self.height_offset * NEOX_UNIT_SCALE
        pos_bias = right_bias + forward_bias + height_bias
        mat = self.ev_g_model().rotation_matrix
        hit_width, hit_height, hit_depth = self.hit_range
        hit_width *= NEOX_UNIT_SCALE
        hit_height *= NEOX_UNIT_SCALE
        hit_depth *= NEOX_UNIT_SCALE
        pos = pos_bias + self.ev_g_position() + math3d.vector(0, hit_height / 2.0 - NEOX_UNIT_SCALE, 0)
        global_data.emgr.scene_draw_wireframe_event.emit(pos, mat, 10, length=(hit_width, hit_height, hit_depth))


class MonsterFlame(MonsterFlameBase):

    def init_params(self):
        super(MonsterFlame, self).init_params()
        self.hit_range = self.custom_param.get('hit_range', [8, 5, 4])
        self.forward_offset = self.custom_param.get('forward_offset', [0, 0, 0])
        self.height_offset = self.custom_param.get('height_offset', 0)
        self.hit_seq = self.custom_param.get('hit_seq', [-20, -10, 10, 20])
        self.hit_interval = self.custom_param.get('hit_interval', 0.5)
        self.hit_idx = 0
        self.skill_id = self.custom_param.get('skill_id', 9025163)
        self.hit_skill_id = self.skill_id
        self.pre_anim = self.custom_param.get('pre_anim', 'skill_4_1')
        self.pre_anim_dur = self.custom_param.get('pre_anim_dur', 1.6)
        self.pre_anim_rate = self.custom_param.get('pre_anim_rate', 1.0)
        self.atk_anim = self.custom_param.get('atk_anim', '')
        self.atk_anim_dur = self.custom_param.get('atk_anim_dur', 1.4)
        self.atk_anim_rate = self.custom_param.get('atk_anim_rate', 1.0)
        self.bac_anim = self.custom_param.get('bac_anim', '')
        self.bac_anim_dur = self.custom_param.get('bac_anim_dur', 0.5)
        self.bac_anim_rate = self.custom_param.get('bac_anim_rate', 1.0)
        self.is_draw_col = self.custom_param.get('is_draw_col', False)
        self.aim_turn = self.custom_param.get('aim_turn', True)
        self.hit_bone = ()
        self.need_stop = True
        self.move_start_ts = self.custom_param.get('move_start_ts', 1.6)
        self.move_end_ts = self.custom_param.get('move_end_ts', 3.0)
        self.move_speed = self.custom_param.get('move_speed', 50)

    def editor_handle(self):
        if global_data.use_sunshine:
            self.init_params()
            self.reset_sub_states_callback()
            self.register_flame_callbacks()
            self.reset_hit_range()