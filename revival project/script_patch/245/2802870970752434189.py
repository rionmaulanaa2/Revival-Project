# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/behavior/PVEMonsterAimTurnLogic.py
from __future__ import absolute_import
from .MonsterStateBase import MonsterStateBase
from logic.gcommon.common_const.character_anim_const import LOW_BODY
import math3d
from math import pi
from common.utils.timer import CLOCK
from logic.gutils.pve_utils import get_aim_pos

class MonsterFocusSwagBase(MonsterStateBase):
    pass


class MonsterFocusSwag(MonsterFocusSwagBase):
    pass


class MonsterAimTurnBase(MonsterStateBase):
    BIND_EVENT = {'E_PVE_M_AIM_TURN': 'set_leader_state',
       'E_ACTIVE_PARAM_STATE': 'pre_check_param'
       }
    econf = {}
    AIM_GAP = 0.1 * pi
    A_T = 0.033
    A_L = 1
    A_R = 2

    def __init__(self):
        super(MonsterAimTurnBase, self).__init__()
        self.aim_timer = None
        return

    def set_leader_state(self, state, skill_id, *args):
        self.leader_state = state
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
            self.target_pos = math3d.vector(*self.target_pos) if self.target_pos else None
            self.leader_state = None
            self.leader_skill_id = None
            self.active_self()
            return

    def init_from_dict(self, unit_obj, bdict, sid, info):
        super(MonsterAimTurnBase, self).init_from_dict(unit_obj, bdict, sid, info)
        self.init_params()
        self.process_event(True)

    def init_params(self):
        self.leader_state = None
        self.leader_skill_id = None
        self.target_id = None
        self.target_pos = None
        self.skill_id = None
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
        super(MonsterAimTurnBase, self).on_init_complete()

    def enter(self, leave_states):
        super(MonsterAimTurnBase, self).enter(leave_states)
        if self.leader_state:
            pass
        else:
            self.send_event('E_CALL_SYNC_METHOD', 'pve_enter_skill', (self.skill_id,), True)
        self.init_aim()

    def update(self, dt):
        super(MonsterAimTurnBase, self).update(dt)

    def init_aim(self):
        self.yaw_ts = 0
        self.aim_lr = 0
        self.reset_aim_timer()
        self.aim_timer = global_data.game_mgr.register_logic_timer(self.update_aim, self.A_T, None, -1, CLOCK, True)
        return

    def update_aim_timer(self, dt):
        self.yaw_ts += dt
        if self.yaw_ts > self.max_aim_dur:
            self.reset_aim_timer()
            self.disable_self()

    def update_aim(self, dt):
        target_pos = get_aim_pos(self.target_id, self.target_pos)
        ori_pos = self.ev_g_position()
        if not target_pos or not ori_pos:
            self.reset_aim_timer()
            self.disable_self()
            return
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
                self.reset_aim_timer()
                self.disable_self()
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
        self.update_aim_timer(dt)

    def reset_aim_timer(self):
        if self.aim_timer:
            global_data.game_mgr.unregister_logic_timer(self.aim_timer)
            self.aim_timer = None
        return

    def exit(self, enter_states):
        self.reset_aim_timer()
        if self.leader_state:
            self.send_event('E_CALL_SYNC_METHOD', 'pve_end_skill', (self.leader_skill_id,), True)
        else:
            self.send_event('E_CALL_SYNC_METHOD', 'pve_end_skill', (self.skill_id,), True)
        super(MonsterAimTurnBase, self).exit(enter_states)

    def destroy(self):
        self.process_event(False)
        self.reset_aim_timer()
        super(MonsterAimTurnBase, self).destroy()


class MonsterAimTurn(MonsterAimTurnBase):

    def init_params(self):
        super(MonsterAimTurn, self).init_params()
        self.skill_id = self.custom_param.get('skill_id', 0)
        self.max_aim_dur = self.custom_param.get('max_aim_dur', 3.0)
        self.aim_speed = self.custom_param.get('aim_speed', 3.14)
        self.aim_left_anim = self.custom_param.get('aim_left_anim', None)
        self.aim_left_anim_rate = self.custom_param.get('aim_left_anim_rate', 1.0)
        self.aim_right_anim = self.custom_param.get('aim_right_anim', None)
        self.aim_right_anim_rate = self.custom_param.get('aim_right_anim_rate', 1.0)
        return

    def editor_handle(self):
        if global_data.use_sunshine:
            self.init_params()