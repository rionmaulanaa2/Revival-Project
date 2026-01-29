# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/behavior/PVEMonsterArrayBombLogic.py
from __future__ import absolute_import
from .MonsterStateBase import MonsterStateBase
from logic.gcommon.common_const.character_anim_const import LOW_BODY
import math3d
from logic.gutils.pve_utils import get_aim_pos
from math import pi, cos, sin
from common.utils.timer import CLOCK
from logic.gcommon.common_const.idx_const import ExploderID
from common.cfg import confmgr
from logic.gcommon.const import NEOX_UNIT_SCALE
from random import uniform
from logic.gcommon.common_utils.bcast_utils import E_PVE_BOSS_ARRAY_BOMB_WARN_SFX

class MonsterArrayBombBase(MonsterStateBase):
    BIND_EVENT = MonsterStateBase.BIND_EVENT.copy()
    BIND_EVENT.update({'E_ACTIVE_PARAM_STATE': 'pre_check_param',
       'E_PVE_BOSS_ARRAY_BOMB_WARN_SFX': 'create_warn_sfx'
       })
    econf = {}
    S_END = -1
    S_AIM = 0
    S_PRE = 1
    S_ATK = 2
    S_BAC = 3
    AIM_GAP = 0.1 * pi
    A_T = 0.033
    A_L = 1
    A_R = 2
    T_X = 1
    T_Z = 2
    UP = math3d.vector(0, 1, 0)

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
        super(MonsterArrayBombBase, self).init_from_dict(unit_obj, bdict, sid, info)
        self.init_params()
        self.process_event(True)
        self.sub_state = self.S_END

    def init_params(self):
        self.target_id = None
        self.target_pos = None
        self.skill_id = 0
        self.yaw_ts = 0
        self.aim_timer = None
        self.aim_lr = 0
        self.aim_left_anim = None
        self.aim_right_anim = None
        self.init_pos = math3d.vector(0, 0, 0)
        self.fire_ts = 0
        self.fire_idx = 0
        self.fire_timer = None
        return

    def editor_handle(self):
        pass

    def process_event(self, is_bind):
        emgr = global_data.emgr
        is_bind and emgr.bind_events(self.econf) if 1 else emgr.unbind_events(self.econf)

    def on_init_complete(self):
        super(MonsterArrayBombBase, self).on_init_complete()
        self.register_bomb_callbacks()

    def register_bomb_callbacks(self):
        self.register_substate_callback(self.S_PRE, 0, self.start_pre)
        self.register_substate_callback(self.S_PRE, self.pre_anim_dur / self.pre_anim_rate, self.end_pre)
        self.register_substate_callback(self.S_ATK, 0, self.start_atk)
        self.register_substate_callback(self.S_ATK, self.atk_dur, self.end_atk)
        self.register_substate_callback(self.S_BAC, 0, self.start_bac)
        self.register_substate_callback(self.S_BAC, self.bac_anim_dur / self.bac_anim_rate, self.end_bac)

    def start_pre(self):
        self.reset_aim_timer()
        self.send_event('E_ANIM_RATE', LOW_BODY, self.pre_anim_rate)
        if self.pre_anim:
            self.send_event('E_POST_ACTION', self.pre_anim, LOW_BODY, 1)

    def end_pre(self):
        self.sub_state = self.S_ATK

    def start_atk(self):
        self.init_fire()
        self.send_event('E_ANIM_RATE', LOW_BODY, self.atk_anim_rate)
        if self.atk_anim:
            self.send_event('E_POST_ACTION', self.atk_anim, LOW_BODY, 1, loop=True)

    def end_atk(self):
        self.sub_state = self.S_BAC

    def start_bac(self):
        self.send_event('E_ANIM_RATE', LOW_BODY, self.bac_anim_rate)
        if self.bac_anim:
            self.send_event('E_POST_ACTION', self.bac_anim, LOW_BODY, 1)

    def end_bac(self):
        self.sub_state = self.S_END

    def enter(self, leave_states):
        super(MonsterArrayBombBase, self).enter(leave_states)
        self.send_event('E_CALL_SYNC_METHOD', 'pve_enter_skill', (self.skill_id,), True)
        self.send_event('E_DO_SKILL', self.skill_id)
        self.sub_state = self.S_AIM
        self.init_aim()

    def update(self, dt):
        super(MonsterArrayBombBase, self).update(dt)
        if self.sub_state == self.S_END:
            self.disable_self()
        elif self.sub_state == self.S_PRE:
            self.send_event('E_CTRL_FACE_TO', get_aim_pos(self.target_id, self.target_pos), False)
        elif self.sub_state == self.S_AIM:
            self.update_aim_timer(dt)

    def exit(self, enter_states):
        super(MonsterArrayBombBase, self).exit(enter_states)
        self.reset_aim_timer()
        self.reset_fire_timer()
        self.send_event('E_CALL_SYNC_METHOD', 'pve_end_skill', (self.skill_id,), True)

    def destroy(self):
        self.process_event(False)
        self.reset_aim_timer()
        self.reset_fire_timer()
        super(MonsterArrayBombBase, self).destroy()

    def init_aim(self):
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
        if not ori_pos:
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

    def init_fire(self):
        self.fire_ts = 0
        self.fire_idx = 0
        self.calc_init_pos()
        self.reset_fire_timer()
        self.fire_timer = global_data.game_mgr.register_logic_timer(self.tick_fire, 1, timedelta=True)

    def calc_init_pos(self):
        forward = self.ev_g_forward()
        forward.y = 0
        forward.normalize()
        pos = self.ev_g_position()
        self.init_pos = pos + forward * self.init_offset
        self.forward = forward
        right = self.UP.cross(forward)
        right.y = 0
        right.normalize()
        self.right = right

    def tick_fire(self, dt):
        if self.fire_idx >= len(self.fire_seq):
            self.reset_fire_timer()
            return
        ts, seq_idx = self.fire_seq[self.fire_idx]
        seq_idx = int(seq_idx)
        if self.fire_ts >= ts:
            if self.array_type == self.T_X:
                for i in self.z_array:
                    self.open_fire(seq_idx, i)

            elif self.array_type == self.T_Z:
                for i in self.x_array:
                    self.open_fire(seq_idx, i)

            self.fire_idx += 1
        self.fire_ts += dt

    def open_fire(self, seq_idx, fix_gap):
        if not self.init_pos:
            return
        if self.array_type == self.T_X:
            x_gap = self.x_array[seq_idx]
            z_gap = fix_gap
        elif self.array_type == self.T_Z:
            x_gap = fix_gap
            z_gap = self.z_array[seq_idx]
        else:
            x_gap, z_gap = (0, 0)
        tar_pos = self.init_pos + self.right * x_gap + self.forward * z_gap
        pos = (tar_pos.x, self.ammo_height * NEOX_UNIT_SCALE, tar_pos.z)
        throw_item = {'uniq_key': self.get_uniq_key(),
           'item_itype': self.wp_type,
           'item_kind': self.wp_kind,
           'position': pos,
           'dir': (0, -1, 0),
           'sub_idx': 0
           }
        self.send_event('E_SHOOT_EXPLOSIVE_ITEM', throw_item, True)
        self.create_warn_sfx(self.sid, pos)
        self.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', [E_PVE_BOSS_ARRAY_BOMB_WARN_SFX, (self.sid, pos)], True)

    def reset_fire_timer(self):
        if self.fire_timer:
            global_data.game_mgr.unregister_logic_timer(self.fire_timer)
            self.fire_timer = None
        return

    def create_warn_sfx(self, sid, pos):
        if sid != self.sid:
            return
        pos = math3d.vector(*pos)

        def cb(sfx):
            sfx.scale = math3d.vector(self.warn_sfx_scale, self.warn_sfx_scale, self.warn_sfx_scale)
            sfx.frame_rate = self.warn_sfx_rate
            sfx.world_position += math3d.vector(0, self.warn_sfx_offset, 0)

        pos.y = self.get_surface_h(pos)
        global_data.sfx_mgr.create_sfx_in_scene(self.warn_sfx, pos, on_create_func=cb)

    def get_surface_h(self, pos):
        return self.ev_g_position().y

    def get_uniq_key(self):
        return ExploderID.gen(global_data.battle_idx)


class MonsterArrayBomb(MonsterArrayBombBase):

    def init_params(self):
        super(MonsterArrayBomb, self).init_params()
        self.skill_id = self.custom_param.get('skill_id', 0)
        self.max_aim_dur = self.custom_param.get('max_aim_dur', 3.0)
        self.aim_speed = self.custom_param.get('aim_speed', 3.14)
        self.aim_left_anim = self.custom_param.get('aim_left_anim', None)
        self.aim_left_anim_rate = self.custom_param.get('aim_left_anim_rate', 1.0)
        self.aim_right_anim = self.custom_param.get('aim_right_anim', None)
        self.aim_right_anim_rate = self.custom_param.get('aim_right_anim_rate', 1.0)
        self.pre_anim = self.custom_param.get('pre_anim', '')
        self.pre_anim_dur = self.custom_param.get('pre_anim_dur', 0.0)
        self.pre_anim_rate = self.custom_param.get('pre_anim_rate', 1.0)
        self.atk_anim = self.custom_param.get('atk_anim', '')
        self.atk_dur = self.custom_param.get('atk_dur', 0)
        self.atk_anim_rate = self.custom_param.get('atk_anim_rate', 1.0)
        self.bac_anim = self.custom_param.get('bac_anim', '')
        self.bac_anim_dur = self.custom_param.get('bac_anim_dur', 0.0)
        self.bac_anim_rate = self.custom_param.get('bac_anim_rate', 1.0)
        self.wp_type = self.custom_param.get('wp_type', 0)
        self.wp_conf = confmgr.get('firearm_config', str(self.wp_type))
        self.wp_kind = self.wp_conf.get('iKind')
        self.init_offset = self.custom_param.get('init_offset')
        self.array_type = self.custom_param.get('array_type', 1)
        self.x_array = self.custom_param.get('x_array', [])
        self.z_array = self.custom_param.get('z_array', [])
        self.fire_seq = self.custom_param.get('fire_seq', 0)
        self.ammo_height = self.custom_param.get('ammo_height', 0)
        self.warn_sfx = self.custom_param.get('warn_sfx', '')
        self.warn_sfx_rate = self.custom_param.get('warn_sfx_rate', 1.0)
        self.warn_sfx_scale = self.custom_param.get('warn_sfx_scale', 1.0)
        self.warn_sfx_offset = self.custom_param.get('warn_sfx_offset', 0)
        return

    def editor_handle(self):
        if global_data.use_sunshine:
            self.init_params()
            self.reset_sub_states_callback()
            self.register_bomb_callbacks()