# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/behavior/PVEMonsterMortarLogic.py
from __future__ import absolute_import
from .MonsterStateBase import MonsterStateBase
import math3d
from logic.gcommon.common_const.character_anim_const import LOW_BODY
from logic.gcommon.const import NEOX_UNIT_SCALE
from logic.gutils.pve_utils import get_aim_pos, get_surface_pos
from logic.gcommon.common_utils.bcast_utils import E_PVE_MONSTER_MORTAR_START_PRE, E_PVE_MONSTER_MORTAR_START_ATK, E_PVE_MONSTER_MORTAR_SUB_WARN_SFX, E_PVE_MONSTER_MORTAR_EXIT
from math import pi
from common.utils.timer import CLOCK
from common.cfg import confmgr
from logic.gcommon.common_const.idx_const import ExploderID

class MonsterMortarBase(MonsterStateBase):
    BIND_EVENT = MonsterStateBase.BIND_EVENT
    BIND_EVENT.update({'E_ACTIVE_PARAM_STATE': 'pre_check_param',
       'E_PVE_MONSTER_MORTAR_START_PRE': 'do_start_pre',
       'E_PVE_MONSTER_MORTAR_START_ATK': 'do_start_atk',
       'E_PVE_MONSTER_MORTAR_SUB_WARN_SFX': 'create_sub_warn_sfx',
       'E_PVE_MONSTER_MORTAR_EXIT': 'do_exit'
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
    A_E = 3
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
        super(MonsterMortarBase, self).init_from_dict(unit_obj, bdict, sid, info)
        self.init_params()
        self.process_event(True)
        self.sub_state = self.S_END

    def init_params(self):
        self.target_id = None
        self.target_pos = None
        self.yaw_ts = 0
        self.aim_timer = None
        self.aim_lr = 0
        self.aim_left_anim = None
        self.aim_right_anim = None
        self.focus_pos = None
        self.focus_tag = False
        self.warn_sfx_ids = []
        self.warn_sfx_refs = []
        self.warn_sfx_timer = None
        self.link_sfx_ids = []
        self.link_sfx_refs = []
        self.link_sfx_timer = None
        self.fire_ts = 0
        self.fire_idx = 0
        self.fire_timer = None
        self.init_pos = math3d.vector(0, 0, 0)
        return

    def editor_handle(self):
        pass

    def process_event(self, is_bind):
        emgr = global_data.emgr
        is_bind and emgr.bind_events(self.econf) if 1 else emgr.unbind_events(self.econf)

    def on_init_complete(self):
        super(MonsterMortarBase, self).on_init_complete()
        self.register_mortar_callbacks()

    def register_mortar_callbacks(self):
        self.register_substate_callback(self.S_PRE, 0, self.start_pre)
        self.register_substate_callback(self.S_PRE, self.pre_anim_dur / self.pre_anim_rate, self.end_pre)
        self.register_substate_callback(self.S_ATK, 0, self.start_atk)
        self.register_substate_callback(self.S_ATK, self.atk_anim_dur / self.atk_anim_rate, self.end_atk)
        self.register_substate_callback(self.S_BAC, 0, self.start_bac)
        self.register_substate_callback(self.S_BAC, self.bac_anim_dur / self.bac_anim_rate, self.end_bac)

    def start_pre(self):
        self.reset_aim_timer()
        self.do_start_pre(self.sid)
        self.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', [E_PVE_MONSTER_MORTAR_START_PRE, (self.sid, True, self.target_id, self.target_pos)], True)
        if not self.pre_anim_dur:
            return
        self.send_event('E_ANIM_RATE', LOW_BODY, self.pre_anim_rate)
        if self.pre_anim:
            self.send_event('E_POST_ACTION', self.pre_anim, LOW_BODY, 1)

    def do_start_pre(self, sid, is_sync=False, target_id=None, target_pos=None):
        if sid != self.sid:
            return
        if is_sync:
            self.target_id = target_id
            self.target_pos = target_pos
        self.fire_idx = 0
        self.start_focus()
        self.delay_call(self.focus_time, self.end_focus)
        self.init_warn_sfx()

    def end_pre(self):
        self.sub_state = self.S_ATK

    def start_atk(self):
        self.do_start_atk(self.sid)
        self.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', [E_PVE_MONSTER_MORTAR_START_ATK, (self.sid, True, self.target_id, self.target_pos)], True)
        self.init_fire()
        if not self.atk_anim_dur:
            return
        self.send_event('E_ANIM_RATE', LOW_BODY, self.atk_anim_rate)
        if self.atk_anim:
            self.send_event('E_POST_ACTION', self.atk_anim, LOW_BODY, 1, loop=True)

    def do_start_atk(self, sid, is_sync=False, target_id=None, target_pos=None):
        if sid != self.sid:
            return
        if is_sync:
            self.target_id = target_id
            self.target_pos = target_pos
        if self.focus_tag:
            self.end_focus()
        self.clear_link_sfx()

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

    def enter(self, leave_states):
        super(MonsterMortarBase, self).enter(leave_states)
        self.send_event('E_DO_SKILL', self.skill_id)
        self.send_event('E_CALL_SYNC_METHOD', 'pve_enter_skill', (self.skill_id,), True)
        self.sub_state = self.S_AIM
        self.init_aim()
        self.fire_idx = 0

    def update(self, dt):
        super(MonsterMortarBase, self).update(dt)
        if self.sub_state == self.S_END:
            self.disable_self()
        elif self.sub_state == self.S_PRE and self.focus_tag:
            self.send_event('E_CTRL_FACE_TO', get_aim_pos(self.target_id, self.target_pos), False)
        elif self.sub_state == self.S_AIM:
            self.update_aim_timer(dt)

    def exit(self, enter_states):
        super(MonsterMortarBase, self).exit(enter_states)
        self.reset_aim_timer()
        self.reset_fire_timer()
        self.do_exit(self.sid)
        self.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', [E_PVE_MONSTER_MORTAR_EXIT, (self.sid,)], True)
        self.send_event('E_CALL_SYNC_METHOD', 'pve_end_skill', (self.skill_id,), True)

    def do_exit(self, sid):
        if sid != self.sid:
            return
        self.reset_warn_sfx_timer()
        self.reset_link_sfx_timer()
        self.clear_warn_sfx()
        self.clear_link_sfx()

    def destroy(self):
        self.process_event(False)
        self.reset_aim_timer()
        self.reset_warn_sfx_timer()
        self.reset_link_sfx_timer()
        self.reset_fire_timer()
        self.clear_warn_sfx()
        self.clear_link_sfx()
        super(MonsterMortarBase, self).destroy()

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
        if not ori_pos or not target_pos:
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
        diff = tar_pos - cur_pos
        tar_dir = diff
        tar_dir.normalize()
        self.focus_pos = tar_pos - tar_dir * self.focus_dis
        surface_pos = get_surface_pos(self.focus_pos)
        if surface_pos:
            self.focus_pos = surface_pos

    def init_warn_sfx(self):
        self.clear_warn_sfx()
        if self.fire_idx != 0:
            return
        else:
            self.calc_focus_pos()
            forward = self.ev_g_forward()
            forward.normalize()
            right = forward.cross(self.UP)
            right.normalize()
            for r_offset in self.fire_array:
                tar_pos = self.focus_pos + right * r_offset

                def cb(sfx):
                    sfx.scale = math3d.vector(self.warn_sfx_scale, self.warn_sfx_scale, self.warn_sfx_scale)
                    sfx.frame_rate = self.warn_sfx_rate
                    sfx.world_position += math3d.vector(0, self.warn_sfx_offset, 0)
                    self.warn_sfx_refs.append(sfx)

                sfx_id = global_data.sfx_mgr.create_sfx_in_scene(self.warn_sfx_res, tar_pos, on_create_func=cb)
                self.warn_sfx_ids.append(sfx_id)

            self.reset_warn_sfx_timer()
            self.warn_sfx_timer = global_data.game_mgr.register_logic_timer(self.tick_warn_sfx, 0.033, None, -1, mode=CLOCK)
            return

    def tick_warn_sfx(self):
        self.calc_focus_pos()
        forward = self.ev_g_forward()
        forward.normalize()
        right = forward.cross(self.UP)
        right.normalize()
        sfx_idx = 0
        for r_offset in self.fire_array:
            tar_pos = self.focus_pos + right * r_offset
            if sfx_idx < len(self.warn_sfx_refs):
                sfx = self.warn_sfx_refs[sfx_idx]
                sfx.world_position = tar_pos
                sfx.world_position += math3d.vector(0, self.warn_sfx_offset, 0)
            sfx_idx += 1

        if not self.focus_tag:
            self.reset_warn_sfx_timer()
            return

    def reset_warn_sfx_timer(self):
        if self.warn_sfx_timer:
            global_data.game_mgr.unregister_logic_timer(self.warn_sfx_timer)
            self.warn_sfx_timer = None
        return

    def clear_warn_sfx(self):
        for sfx_id in self.warn_sfx_ids:
            global_data.sfx_mgr.remove_sfx_by_id(sfx_id)

        self.warn_sfx_ids = []
        self.warn_sfx_refs = []

    def init_link_sfx(self):
        self.clear_link_sfx()
        if self.fire_idx != 0:
            return
        else:
            model = self.ev_g_model()
            if not model or not model.valid:
                return
            self.calc_focus_pos()
            forward = self.ev_g_forward()
            forward.normalize()
            right = forward.cross(self.UP)
            right.normalize()
            for r_offset in self.fire_array:
                tar_pos = self.focus_pos + right * r_offset
                cur_pos = self.ev_g_position()
                diff = tar_pos - cur_pos

                def cb(sfx):
                    scale_x = self.link_sfx_scale
                    scale_y = self.link_sfx_scale * self.link_sfx_y_scale
                    scale_z = self.link_sfx_scale * (diff.length / self.link_sfx_z_length)
                    sfx.scale = math3d.vector(scale_x, scale_y, scale_z)
                    sfx.frame_rate = self.link_sfx_rate
                    self.link_sfx_refs.append(sfx)

                sfx_id = global_data.sfx_mgr.create_sfx_for_model(self.link_sfx_res, model, on_create_func=cb)
                self.link_sfx_ids.append(sfx_id)

            self.reset_link_sfx_timer()
            self.link_sfx_timer = global_data.game_mgr.register_logic_timer(self.tick_link_sfx, 0.016, None, -1, mode=CLOCK)
            return

    def tick_link_sfx(self):
        self.calc_focus_pos()
        forward = self.ev_g_forward()
        forward.normalize()
        right = forward.cross(self.UP)
        right.normalize()
        sfx_idx = 0
        for r_offset in self.fire_array:
            tar_pos = self.focus_pos + right * r_offset
            cur_pos = self.ev_g_position()
            diff = tar_pos - cur_pos
            print diff.length
            print self.link_sfx_z_length
            if sfx_idx < len(self.link_sfx_refs):
                sfx = self.link_sfx_refs[sfx_idx]
                scale_x = self.link_sfx_scale
                scale_y = self.link_sfx_scale * self.link_sfx_y_scale
                scale_z = self.link_sfx_scale * (diff.length / self.link_sfx_z_length)
                sfx.scale = math3d.vector(scale_x, scale_y, scale_z)
            sfx_idx += 1

        if not self.focus_tag:
            self.reset_link_sfx_timer()
            return

    def reset_link_sfx_timer(self):
        if self.link_sfx_timer:
            global_data.game_mgr.unregister_logic_timer(self.link_sfx_timer)
            self.link_sfx_timer = None
        return

    def clear_link_sfx(self):
        for sfx_id in self.link_sfx_ids:
            global_data.sfx_mgr.remove_sfx_by_id(sfx_id)

        self.link_sfx_ids = []
        self.link_sfx_refs = []

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
        self.init_pos = pos
        self.forward = forward
        right = self.UP.cross(forward)
        right.y = 0
        right.normalize()
        self.right = right

    def tick_fire(self, dt):
        if self.fire_idx >= len(self.fire_seq):
            self.reset_fire_timer()
            return
        ts, forward_gap = self.fire_seq[self.fire_idx]
        if self.fire_ts >= ts:
            for r_offset in self.fire_array:
                tar_pos = self.focus_pos + self.right * r_offset + self.forward * forward_gap
                self.open_fire(tar_pos)

            self.fire_idx += 1
        self.fire_ts += dt

    def open_fire(self, tar_pos):
        ret_pos = tar_pos - self.forward * self.ammo_offset
        pos = (
         ret_pos.x, self.ammo_height, ret_pos.z)
        dire = tar_pos - math3d.vector(*pos)
        dire.normalize()
        throw_item = {'uniq_key': self.get_uniq_key(),
           'item_itype': self.wp_type,
           'item_kind': self.wp_kind,
           'position': pos,
           'dir': (
                 dire.x, dire.y, dire.z),
           'sub_idx': 0
           }
        self.send_event('E_SHOOT_EXPLOSIVE_ITEM', throw_item, True)
        if self.fire_idx != 0:
            self.create_sub_warn_sfx(tar_pos)
            self.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', [E_PVE_MONSTER_MORTAR_SUB_WARN_SFX, ((tar_pos.x, tar_pos.y, tar_pos.z), True)], True)

    def reset_fire_timer(self):
        if self.fire_timer:
            global_data.game_mgr.unregister_logic_timer(self.fire_timer)
            self.fire_timer = None
        return

    def create_sub_warn_sfx(self, pos, is_sync=False):
        pos = math3d.vector(*pos) if is_sync else pos

        def cb(sfx):
            sfx.scale = math3d.vector(self.sub_warn_sfx_scale, self.sub_warn_sfx_scale, self.sub_warn_sfx_scale)
            sfx.frame_rate = self.sub_warn_sfx_rate
            sfx.world_position += math3d.vector(0, self.sub_warn_sfx_offset, 0)

        global_data.sfx_mgr.create_sfx_in_scene(self.sub_warn_sfx_res, pos, on_create_func=cb)

    def get_uniq_key(self):
        return ExploderID.gen(global_data.battle_idx)


class MonsterMortar(MonsterMortarBase):

    def init_params(self):
        super(MonsterMortar, self).init_params()
        self.skill_id = self.custom_param.get('skill_id', 9015155)
        self.max_aim_dur = self.custom_param.get('max_aim_dur', 3.0)
        self.aim_speed = self.custom_param.get('aim_speed', 3.14)
        self.aim_left_anim = self.custom_param.get('aim_left_anim', None)
        self.aim_left_anim_rate = self.custom_param.get('aim_left_anim_rate', 1.0)
        self.aim_right_anim = self.custom_param.get('aim_right_anim', None)
        self.aim_right_anim_rate = self.custom_param.get('aim_right_anim_rate', 1.0)
        self.pre_anim = self.custom_param.get('pre_anim', '')
        self.pre_anim_dur = self.custom_param.get('pre_anim_dur', 0)
        self.pre_anim_rate = self.custom_param.get('pre_anim_rate', 1.0)
        self.atk_anim = self.custom_param.get('atk_anim', '')
        self.atk_anim_dur = self.custom_param.get('atk_anim_dur', 0)
        self.atk_anim_rate = self.custom_param.get('atk_anim_rate', 1.0)
        self.bac_anim = self.custom_param.get('bac_anim', '')
        self.bac_anim_dur = self.custom_param.get('bac_anim_dur', 0)
        self.bac_anim_rate = self.custom_param.get('bac_anim_rate', 1.0)
        self.wp_type = self.custom_param.get('wp_type', 0)
        self.wp_conf = confmgr.get('firearm_config', str(self.wp_type))
        self.wp_kind = self.wp_conf.get('iKind')
        self.focus_time = self.custom_param.get('focus_time', 0)
        self.focus_dis = self.custom_param.get('focus_dis', 0) * NEOX_UNIT_SCALE
        self.warn_sfx_res = self.custom_param.get('warn_sfx_res', '')
        self.warn_sfx_rate = self.custom_param.get('warn_sfx_rate', 1.0)
        self.warn_sfx_scale = self.custom_param.get('warn_sfx_scale', 1.0)
        self.warn_sfx_offset = self.custom_param.get('warn_sfx_offset', 0)
        self.link_sfx_res = self.custom_param.get('link_sfx_res', '')
        self.link_sfx_rate = self.custom_param.get('link_sfx_rate', 1.0)
        self.link_sfx_scale = self.custom_param.get('link_sfx_scale', 1.0)
        self.link_sfx_socket = self.custom_param.get('link_sfx_socket', '')
        self.link_sfx_y_scale = self.custom_param.get('link_sfx_y_scale', 3.0)
        self.link_sfx_z_length = self.custom_param.get('link_sfx_z_length', 15) * NEOX_UNIT_SCALE
        self.fire_array = self.custom_param.get('fire_array', [])
        self.fire_seq = self.custom_param.get('fire_seq', [])
        self.ammo_height = self.custom_param.get('ammo_height', 0) * NEOX_UNIT_SCALE
        self.ammo_offset = self.custom_param.get('ammo_offset', 0) * NEOX_UNIT_SCALE
        self.sub_warn_sfx_res = self.custom_param.get('sub_warn_sfx_res', '')
        self.sub_warn_sfx_rate = self.custom_param.get('sub_warn_sfx_rate', 1.0)
        self.sub_warn_sfx_scale = self.custom_param.get('sub_warn_sfx_scale', 1.0)
        self.sub_warn_sfx_offset = self.custom_param.get('sub_warn_sfx_offset', 0)
        return

    def editor_handle(self):
        if global_data.use_sunshine:
            self.init_params()
            self.reset_sub_states_callback()
            self.register_mortar_callbacks()