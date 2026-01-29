# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/behavior/PVEMonsterBombLogic.py
from __future__ import absolute_import
from six.moves import range
from .MonsterStateBase import MonsterStateBase
from logic.gcommon.common_const.character_anim_const import LOW_BODY
import math3d
from logic.gutils.pve_utils import get_aim_pos, get_surface_pos
from math import pi, cos, sin
from common.utils.timer import CLOCK
from logic.gcommon.common_const.idx_const import ExploderID
from common.cfg import confmgr
from logic.gcommon.const import NEOX_UNIT_SCALE
from random import uniform
from logic.gcommon.common_utils.bcast_utils import E_PVE_BOSS_BOMB_WARN_SFX

class MonsterBombBase(MonsterStateBase):
    BIND_EVENT = MonsterStateBase.BIND_EVENT.copy()
    BIND_EVENT.update({'E_ACTIVE_PARAM_STATE': 'pre_check_param',
       'E_PVE_BOSS_BOMB_WARN_SFX': 'create_warn_sfx'
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
    R_COUNT = 3

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
        super(MonsterBombBase, self).init_from_dict(unit_obj, bdict, sid, info)
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
        self.focus_tag = False
        self.focus_pos = None
        self.fire_ts = 0
        self.fire_idx = 0
        self.sub_idx = 0
        self.fire_timer = None
        self.bomb_pos = []
        return

    def editor_handle(self):
        pass

    def process_event(self, is_bind):
        emgr = global_data.emgr
        is_bind and emgr.bind_events(self.econf) if 1 else emgr.unbind_events(self.econf)

    def on_init_complete(self):
        super(MonsterBombBase, self).on_init_complete()
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
        self.start_focus()
        self.delay_call(self.focus_time, self.end_focus)
        self.send_event('E_ANIM_RATE', LOW_BODY, self.pre_anim_rate)
        if self.pre_anim:
            self.send_event('E_POST_ACTION', self.pre_anim, LOW_BODY, 1)

    def end_pre(self):
        self.sub_state = self.S_ATK

    def start_atk(self):
        if self.focus_tag:
            self.end_focus()
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
        super(MonsterBombBase, self).enter(leave_states)
        self.send_event('E_CALL_SYNC_METHOD', 'pve_enter_skill', (self.skill_id,), True)
        self.send_event('E_DO_SKILL', self.skill_id)
        self.sub_state = self.S_AIM
        self.init_aim()

    def update(self, dt):
        super(MonsterBombBase, self).update(dt)
        if self.sub_state == self.S_END:
            self.disable_self()
        elif self.sub_state == self.S_PRE and self.focus_tag:
            self.send_event('E_CTRL_FACE_TO', get_aim_pos(self.target_id, self.target_pos), False)
        elif self.sub_state == self.S_AIM:
            self.update_aim_timer(dt)

    def exit(self, enter_states):
        super(MonsterBombBase, self).exit(enter_states)
        self.reset_aim_timer()
        self.reset_fire_timer()
        self.send_event('E_CALL_SYNC_METHOD', 'pve_end_skill', (self.skill_id,), True)

    def destroy(self):
        self.process_event(False)
        self.reset_aim_timer()
        self.reset_fire_timer()
        super(MonsterBombBase, self).destroy()

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

    def start_focus(self):
        self.focus_tag = True

    def end_focus(self):
        self.calc_focus_pos()
        self.focus_tag = False

    def calc_focus_pos(self):
        cur_pos = self.ev_g_position()
        tar_pos = get_aim_pos(self.target_id, self.target_pos, False)
        if self.get_real_surface_tag:
            surface_pos = get_surface_pos(tar_pos)
            if surface_pos:
                tar_pos = surface_pos
            tar_dire = tar_pos - cur_pos
            tar_dire.y = 0
        else:
            tar_dire = tar_pos - cur_pos
        tar_dire.normalize()
        self.focus_pos = tar_pos - tar_dire * self.focus_dis

    def init_fire(self):
        self.fire_ts = 0
        self.fire_idx = 0
        self.sub_idx = 0
        self.bomb_pos = []
        self.reset_fire_timer()
        self.fire_timer = global_data.game_mgr.register_logic_timer(self.tick_fire, 1, timedelta=True)

    def tick_fire(self, dt):
        if self.fire_idx >= len(self.fire_seq):
            self.reset_fire_timer()
            return
        ts, radius, count = self.fire_seq[self.fire_idx]
        if self.fire_ts >= ts:
            for i in range(int(count)):
                self.open_fire(radius)

            self.fire_idx += 1
        self.fire_ts += dt

    def open_fire(self, radius):
        if not self.focus_pos:
            return
        self.random_pos(radius)
        fix_pos = self.bomb_pos[self.sub_idx]
        fix_x, fix_z = fix_pos.x, fix_pos.y
        pos = [
         self.focus_pos.x + fix_x, self.ammo_height * NEOX_UNIT_SCALE, self.focus_pos.z + fix_z]
        if self.get_real_surface_tag:
            pos[1] += self.focus_pos.y
            sfx_pos = (self.focus_pos.x + fix_x, self.focus_pos.y, self.focus_pos.z + fix_z)
        else:
            sfx_pos = (
             self.focus_pos.x + fix_x, self.get_surface_h(pos), self.focus_pos.z + fix_z)
        throw_item = {'uniq_key': self.get_uniq_key(),
           'item_itype': self.wp_type,
           'item_kind': self.wp_kind,
           'position': pos,
           'dir': (0, -1, 0),
           'sub_idx': 0
           }
        self.sub_idx += 1
        self.send_event('E_SHOOT_EXPLOSIVE_ITEM', throw_item, True)
        self.create_warn_sfx(self.sid, sfx_pos)
        self.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', [E_PVE_BOSS_BOMB_WARN_SFX, (self.sid, sfx_pos)], True)

    def random_pos(self, radius):
        r_count = 0
        while 1:
            if r_count < self.R_COUNT:
                pos = self.generate_random_pos(radius)
                for i in range(self.sub_idx):
                    if (pos - self.bomb_pos[i]).length < self.min_gap:
                        r_count += 1
                        break
                else:
                    self.bomb_pos.append(pos)
                    break

        else:
            self.bomb_pos.append(self.generate_random_pos(radius))

    def generate_random_pos(self, radius):
        theta = uniform(0, 2 * pi)
        r = radius * uniform(0, 1)
        pos = math3d.vector2(r * cos(theta), r * sin(theta))
        return pos

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

        global_data.sfx_mgr.create_sfx_in_scene(self.warn_sfx, pos, on_create_func=cb)

    def get_surface_h(self, pos):
        return self.ev_g_position().y

    def get_uniq_key(self):
        return ExploderID.gen(global_data.battle_idx)


class MonsterBomb(MonsterBombBase):

    def init_params(self):
        super(MonsterBomb, self).init_params()
        self.skill_id = self.custom_param.get('skill_id', 0)
        self.max_aim_dur = self.custom_param.get('max_aim_dur', 3.0)
        self.aim_speed = self.custom_param.get('aim_speed', 3.14)
        self.aim_left_anim = self.custom_param.get('aim_left_anim', None)
        self.aim_left_anim_rate = self.custom_param.get('aim_left_anim_rate', 1.0)
        self.aim_right_anim = self.custom_param.get('aim_right_anim', None)
        self.aim_right_anim_rate = self.custom_param.get('aim_right_anim_rate', 1.0)
        self.focus_time = self.custom_param.get('focus_time', 0.6)
        self.focus_dis = self.custom_param.get('focus_dis', 7.0) * NEOX_UNIT_SCALE
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
        self.ammo_height = self.custom_param.get('ammo_height', 0)
        self.fire_seq = self.custom_param.get('fire_seq', 0)
        self.min_gap = self.custom_param.get('min_gap', 0)
        self.get_real_surface_tag = self.custom_param.get('get_real_surface_tag', False)
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