# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/behavior/PVEBossFlashDashLogic.py
from __future__ import absolute_import
from .MonsterStateBase import MonsterStateBase
from logic.gcommon.common_const.character_anim_const import LOW_BODY
import math3d
from logic.gutils.scene_utils import dash_filtrate_hit
from logic.gcommon.cdata.pve_monster_status_config import MC_MONSTER_AIMTURN
from logic.gutils.pve_utils import get_aim_pos
from math import radians, cos, sin
from logic.gcommon.const import NEOX_UNIT_SCALE

class BossFlashDashBase(MonsterStateBase):
    BIND_EVENT = MonsterStateBase.BIND_EVENT.copy()
    BIND_EVENT.update({'E_ACTIVE_PARAM_STATE': 'pre_check_param'
       })
    econf = {}
    S_END = -1
    S_PRE = 1
    S_DASH = 2
    S_BAC = 3

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
        super(BossFlashDashBase, self).init_from_dict(unit_obj, bdict, sid, info)
        self.init_params()
        self.process_event(True)
        self.sub_state = self.S_END

    def init_params(self):
        self.target_id = None
        self.target_pos = None
        self.skill_id = 0
        self.dash_count = 3
        self.dash_idx = 0
        self.dash_dur = 0
        self.dash_speed = 0
        self.dash_dire = None
        self.tick_dur = 0
        self.hit_id = set()
        self.check_hit_timer = None
        return

    def editor_handle(self):
        pass

    def process_event(self, is_bind):
        emgr = global_data.emgr
        is_bind and emgr.bind_events(self.econf) if 1 else emgr.unbind_events(self.econf)

    def on_init_complete(self):
        super(BossFlashDashBase, self).on_init_complete()
        self.reset_dash_state()

    def reset_dash_state(self):
        self.reset_sub_states_callback()
        self.pre_anim_dur = self.pre_anim_dur_list[self.dash_idx]
        self.pre_anim_rate = self.pre_anim_rate_list[self.dash_idx]
        self.bac_anim_dur = self.bac_anim_dur_list[self.dash_idx]
        self.bac_anim_rate = self.bac_anim_rate_list[self.dash_idx]
        self.tick_dur = 0
        self.register_dash_callbacks()

    def register_dash_callbacks(self):
        self.register_substate_callback(self.S_PRE, 0, self.start_pre)
        self.register_substate_callback(self.S_PRE, self.pre_anim_dur / self.pre_anim_rate, self.end_pre)
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

    def calc_dash_dire(self):
        if not self.target_id and not self.target_pos:
            self.disable_self()
            return False
        else:
            target_pos = get_aim_pos(self.target_id, self.target_pos)
            start_pos = self.ev_g_position()
            if not target_pos or not start_pos:
                self.disable_self()
                return False
            self.start_pos = start_pos
            angle, dis = self.dash_seq[self.dash_idx]
            dis = dis * NEOX_UNIT_SCALE
            ori_vec = start_pos - target_pos
            ori_vec.y = 0
            ori_vec.normalize()
            x, z = ori_vec.x, ori_vec.z
            rad = radians(angle)
            tar_vec = math3d.vector(x * cos(rad) - z * sin(rad), 0, x * sin(rad) + z * cos(rad))
            tar_vec.normalize()
            final_pos = target_pos + tar_vec * dis
            self.dash_dire = final_pos - start_pos
            self.dash_dire.y = 0
            self.dash_dur = self.dash_dire.length / self.dash_speed
            self.dash_dur = max(self.min_dash_dur, min(self.max_dash_dur, self.dash_dur))
            self.reset_sub_state_callback(self.S_DASH)
            self.register_substate_callback(self.S_DASH, 0, self.start_dash)
            self.register_substate_callback(self.S_DASH, self.dash_dur, self.end_dash)
            self.dash_dire.normalize()
            self.send_event('E_CTRL_FACE_TO', get_aim_pos(None, final_pos), False)
            return True

    def start_dash(self):
        self.start_check_hit()
        self.send_event('E_ANIM_RATE', LOW_BODY, self.dash_anim_rate)
        self.dash_anim = self.dash_anim_list[self.dash_idx]
        if self.dash_anim:
            self.send_event('E_POST_ACTION', self.dash_anim, LOW_BODY, 1, loop=True)
        self.dash_speed = self.dash_speed_list[self.dash_idx]
        self.send_event('E_SET_WALK_DIRECTION', self.dash_dire * self.dash_speed)

    def end_dash(self):
        self.send_event('E_CLEAR_SPEED')
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
        super(BossFlashDashBase, self).enter(leave_states)
        self.send_event('E_CALL_SYNC_METHOD', 'pve_enter_skill', (self.skill_id,), True)
        self.send_event('E_DO_SKILL', self.skill_id)
        self.send_event('E_DO_OXRUSH_MONSTER', True)
        self.dash_idx = 0
        self.reset_dash_state()
        self.sub_state = self.S_PRE

    def update(self, dt):
        super(BossFlashDashBase, self).update(dt)
        if self.sub_state == self.S_END:
            self.disable_self()

    def exit(self, enter_states):
        self.clear_check_hit_timer()
        super(BossFlashDashBase, self).exit(enter_states)
        self.send_event('E_DO_OXRUSH_MONSTER', False)
        if self.aim_turn:
            self.send_event('E_PVE_M_AIM_TURN', self.sid, self.skill_id, self.target_id, math3d.vector(0, 0, 0))
            self.send_event('E_ACTIVE_STATE', MC_MONSTER_AIMTURN)
        else:
            self.send_event('E_CALL_SYNC_METHOD', 'pve_end_skill', (self.skill_id,), True)

    def destroy(self):
        self.clear_check_hit_timer()
        self.process_event(False)
        super(BossFlashDashBase, self).destroy()

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


class BossFlashDash(BossFlashDashBase):

    def init_params(self):
        super(BossFlashDash, self).init_params()
        self.skill_id = self.custom_param.get('skill_id', 0)
        self.dash_speed_list = self.custom_param.get('dash_speed_list', [0])
        self.dash_speed = self.dash_speed_list[self.dash_idx]
        self.min_dash_dur = self.custom_param.get('min_dash_dur', 0)
        self.max_dash_dur = self.custom_param.get('max_dash_dur', 0)
        self.dash_seq = self.custom_param.get('dash_seq', [])
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

    def editor_handle(self):
        if global_data.use_sunshine:
            self.init_params()
            self.reset_sub_states_callback()
            self.register_dash_callbacks()