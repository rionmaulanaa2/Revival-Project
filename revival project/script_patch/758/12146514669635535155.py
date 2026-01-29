# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/behavior/PVEMonsterSummonLogic.py
from __future__ import absolute_import
from .MonsterStateBase import MonsterStateBase
import math3d
from logic.gcommon.common_const.character_anim_const import LOW_BODY
from math import pi
from common.utils.timer import CLOCK
from logic.gutils.pve_utils import get_aim_pos

class MonsterSummonBase(MonsterStateBase):
    BIND_EVENT = {'E_ACTIVE_PARAM_STATE': 'pre_check_param'
       }
    econf = {}
    S_END = -1
    S_AIM = 1
    S_PRE = 2
    S_SUM = 3
    S_BAC = 4
    AIM_GAP = 0.1 * pi
    A_T = 0.033
    A_L = 1
    A_R = 2

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
            self.target_pos = math3d.vector(*self.target_pos) if self.target_pos else None
            self.active_self()
            return

    def init_from_dict(self, unit_obj, bdict, sid, info):
        super(MonsterSummonBase, self).init_from_dict(unit_obj, bdict, sid, info)
        self.init_params()
        self.process_event(True)
        self.sub_state = self.S_END

    def init_params(self):
        self.target_id = None
        self.target_pos = None
        self.fire_count = self.custom_param.get('fire_count', 1)
        self.fire_idx = 0
        self.yaw_ts = 0
        self.aim_timer = None
        self.aim_lr = 0
        self.aim_left_anim = None
        self.aim_right_anim = None
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
        super(MonsterSummonBase, self).on_init_complete()
        self.register_summon_callbacks()

    def reset_summon_state(self):
        self.reset_sub_states_callback()
        self.pre_anim_dur = self.pre_anim_dur_list[self.fire_idx]
        self.pre_anim_rate = self.pre_anim_rate_list[self.fire_idx]
        self.sum_anim_dur = self.sum_anim_dur_list[self.fire_idx]
        self.sum_anim_rate = self.sum_anim_rate_list[self.fire_idx]
        self.bac_anim_dur = self.bac_anim_dur_list[self.fire_idx]
        self.bac_anim_rate = self.bac_anim_rate_list[self.fire_idx]
        self.register_summon_callbacks()

    def register_summon_callbacks(self):
        self.register_substate_callback(self.S_PRE, 0, self.start_pre)
        self.register_substate_callback(self.S_PRE, self.pre_anim_dur / self.pre_anim_rate, self.end_pre)
        self.register_substate_callback(self.S_SUM, 0, self.start_sum)
        self.register_substate_callback(self.S_SUM, self.sum_anim_dur / self.sum_anim_rate, self.end_sum)
        self.register_substate_callback(self.S_BAC, 0, self.start_bac)
        self.register_substate_callback(self.S_BAC, self.bac_anim_dur / self.bac_anim_rate, self.end_bac)

    def start_pre(self):
        self.reset_aim_timer()
        if not self.pre_anim_dur:
            return
        self.send_event('E_ANIM_RATE', LOW_BODY, self.pre_anim_rate)
        self.send_event('E_POST_ACTION', self.pre_anim, LOW_BODY, 1)

    def end_pre(self):
        self.sub_state = self.S_SUM

    def start_sum(self):
        self.send_event('E_CALL_SYNC_METHOD', 'do_skill', (self.skill_id, self.post_data()), False, True)
        if not self.sum_anim_dur:
            return
        self.send_event('E_ANIM_RATE', LOW_BODY, self.sum_anim_rate)
        self.send_event('E_POST_ACTION', self.sum_anim, LOW_BODY, 1)

    def end_sum(self):
        self.sub_state = self.S_BAC

    def start_bac(self):
        if not self.bac_anim_dur:
            return
        self.send_event('E_ANIM_RATE', LOW_BODY, self.bac_anim_rate)
        self.send_event('E_POST_ACTION', self.bac_anim, LOW_BODY, 1)

    def end_bac(self):
        if self.fire_idx < self.fire_count - 1:
            self.fire_idx += 1
            self.reset_summon_state()
            self.sub_state = self.S_PRE
        else:
            self.sub_state = self.S_END

    def post_data(self):
        model = self.ev_g_model()
        mat = model.get_socket_matrix(self.fire_socket, 1)
        pos = mat.translation
        dire = mat.forward
        data = ((pos.x, pos.y, pos.z), (dire.x, dire.y, dire.z), self.target_id, (self.target_pos.x, self.target_pos.y, self.target_pos.z))
        return data

    def enter(self, leave_states):
        super(MonsterSummonBase, self).enter(leave_states)
        self.send_event('E_CALL_SYNC_METHOD', 'pve_enter_skill', (self.skill_id,), True)
        if self.sub_state == self.S_END:
            self.reset_summon_state()
            self.fire_idx = 0
            self.sub_state = self.S_AIM
            self.init_aim()

    def update(self, dt):
        super(MonsterSummonBase, self).update(dt)
        if self.sub_state == self.S_END:
            self.disable_self()
        elif self.sub_state in (self.S_PRE, self.S_SUM):
            self.send_event('E_CTRL_FACE_TO', get_aim_pos(self.target_id, self.target_pos), False)
        elif self.sub_state == self.S_AIM:
            self.update_aim_timer(dt)

    def init_aim(self):
        if not self.max_aim_dur:
            return
        else:
            self.yaw_ts = 0
            self.aim_lr = 0
            self.reset_aim_timer()
            self.aim_timer = global_data.game_mgr.register_logic_timer(self.update_aim, self.A_T, None, -1, CLOCK, True)
            return

    def update_aim_timer(self, dt):
        self.yaw_ts += dt
        if self.yaw_ts > self.max_aim_dur:
            self.sub_state = self.S_PRE
            self.reset_aim_timer()

    def update_aim(self, dt):
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
                self.sub_state = self.S_PRE
                self.reset_aim_timer()
                return
        if diff_yaw < 0:
            ret_yaw = ori_yaw - self.aim_speed * dt
            lr_tag = self.A_L
        else:
            ret_yaw = ori_yaw + self.aim_speed * dt
            lr_tag = self.A_R
        self.send_event('E_CAM_YAW', ret_yaw)
        self.send_event('E_ACTION_SYNC_YAW', ret_yaw)
        if self.aim_left_anim and self.aim_lr != lr_tag:
            anim = self.aim_left_anim if lr_tag == self.A_L else self.aim_right_anim
            rate = self.aim_left_anim_rate if lr_tag == self.A_L else self.aim_right_anim_rate
            self.send_event('E_ANIM_RATE', LOW_BODY, rate)
            self.send_event('E_POST_ACTION', anim, LOW_BODY, 1, loop=True)
            self.aim_lr = lr_tag

    def reset_aim_timer(self):
        if self.aim_timer:
            global_data.game_mgr.unregister_logic_timer(self.aim_timer)
            self.aim_timer = None
        return

    def exit(self, enter_states):
        super(MonsterSummonBase, self).exit(enter_states)
        self.sub_state = self.S_END
        self.fire_idx = 0
        self.reset_aim_timer()
        self.send_event('E_CALL_SYNC_METHOD', 'pve_end_skill', (self.skill_id,), True)

    def destroy(self):
        self.process_event(False)
        self.reset_aim_timer()
        super(MonsterSummonBase, self).destroy()


class MonsterSummon(MonsterSummonBase):

    def init_params(self):
        super(MonsterSummon, self).init_params()
        self.fire_count = self.custom_param.get('fire_count', 1)
        self.skill_id = self.custom_param.get('skill_id', 9015156)
        self.max_aim_dur = self.custom_param.get('max_aim_dur', 3.0)
        self.aim_speed = self.custom_param.get('aim_speed', 3.14)
        self.aim_left_anim = self.custom_param.get('aim_left_anim', None)
        self.aim_left_anim_rate = self.custom_param.get('aim_left_anim_rate', 1.0)
        self.aim_right_anim = self.custom_param.get('aim_right_anim', None)
        self.aim_right_anim_rate = self.custom_param.get('aim_right_anim_rate', 1.0)
        self.pre_anim_name_list = self.custom_param.get('pre_anim_name_list', ('', ))
        self.pre_anim = self.pre_anim_name_list[self.fire_idx]
        self.pre_anim_rate_list = self.custom_param.get('pre_anim_rate_list', (1.0, ))
        self.pre_anim_rate = self.pre_anim_rate_list[self.fire_idx]
        self.pre_anim_dur_list = self.custom_param.get('pre_anim_dur_list', (0, ))
        self.pre_anim_dur = self.pre_anim_dur_list[self.fire_idx]
        self.sum_anim_name_list = self.custom_param.get('sum_anim_name_list', ('attack01', ))
        self.sum_anim = self.sum_anim_name_list[self.fire_idx]
        self.sum_anim_rate_list = self.custom_param.get('sum_anim_rate_list', (1.0, ))
        self.sum_anim_rate = self.sum_anim_rate_list[self.fire_idx]
        self.sum_anim_dur_list = self.custom_param.get('sum_anim_dur_list', (1.0, ))
        self.sum_anim_dur = self.sum_anim_dur_list[self.fire_idx]
        self.bac_anim_name_list = self.custom_param.get('bac_anim_name_list', ('', ))
        self.bac_anim = self.bac_anim_name_list[self.fire_idx]
        self.bac_anim_rate_list = self.custom_param.get('bac_anim_rate_list', (1.0, ))
        self.bac_anim_rate = self.bac_anim_rate_list[self.fire_idx]
        self.bac_anim_dur_list = self.custom_param.get('bac_anim_dur_list', (0, ))
        self.bac_anim_dur = self.bac_anim_dur_list[self.fire_idx]
        self.fire_socket_list = self.custom_param.get('fire_socket_list', ('fx_kaihuo', ))
        self.fire_socket = self.fire_socket_list[self.fire_idx]
        return

    def editor_handle(self):
        if global_data.use_sunshine:
            self.init_params()
            self.reset_sub_states_callback()
            self.register_summon_callbacks()