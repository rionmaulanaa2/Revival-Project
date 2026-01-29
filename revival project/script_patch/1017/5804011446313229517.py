# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/behavior/PVEBossMultiLaserLogic.py
from __future__ import absolute_import
import six_ex
from .MonsterStateBase import MonsterStateBase
import math3d
from logic.gcommon.common_const.character_anim_const import LOW_BODY
import collision
from logic.gcommon.const import NEOX_UNIT_SCALE
from logic.gutils.pve_utils import get_aim_pos
from math import radians
from logic.gcommon.common_utils.bcast_utils import E_PVE_BOSS_MULTI_LASER_START_PRE, E_PVE_BOSS_MULTI_LASER_INIT_SINGLE, E_PVE_BOSS_MULTI_LASER_START_BAC, E_PVE_BOSS_MULTI_LASER_EXIT, E_PVE_BOSS_MULTI_LASER_INIT_SPOT
from common.cfg import confmgr
import world
from common.utils.timer import CLOCK
from math import pi, sin, cos

class BossMultiLaserBase(MonsterStateBase):
    BIND_EVENT = {'E_ACTIVE_PARAM_STATE': 'pre_check_param',
       'E_PVE_BOSS_MULTI_LASER_START_PRE': 'do_start_pre',
       'E_PVE_BOSS_MULTI_LASER_INIT_SPOT': 'sync_init_single_spot_sfx',
       'E_PVE_BOSS_MULTI_LASER_INIT_SINGLE': 'sync_init_single_laser',
       'E_PVE_BOSS_MULTI_LASER_START_BAC': 'do_start_bac',
       'E_PVE_BOSS_MULTI_LASER_EXIT': 'do_exit',
       'E_PVE_ALL_TRACK_MISSILE_END': 'on_end_lead'
       }
    econf = {}
    S_END = 0
    S_PRE = 1
    S_RISE = 2
    S_AIM = 3
    S_LEAD = 4
    S_BAC = 5
    AIM_GAP = 0.1 * pi
    A_T = 0.033
    UP = math3d.vector(0, 1, 0)

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
        super(BossMultiLaserBase, self).init_from_dict(unit_obj, bdict, sid, info)
        self.init_params()
        self.process_event(True)
        self.sub_state = self.S_END

    def init_params(self):
        self.target_id = None
        self.target_pos = None
        self.is_sync = False
        self._col_ids = []
        self.spot_idx = 0
        self.laser_idx = 0
        self.laser_ts_seq = []
        self.laser_angle_seq = []
        self.laser_timer = {}
        self.hit_point_dict = {}
        self.hit_target_dict = {}
        self.hit_ts_dict = {}
        self.aim_timer = None
        self.spot_sfx_dict = {}
        self.spot_sfx_id_dict = {}
        self.atk_sfx_dict = {}
        self.atk_sfx_id_dict = {}
        self.hit_sfx_dict = {}
        self.hit_sfx_id_dict = {}
        return

    def editor_handle(self):
        pass

    def process_event(self, is_bind):
        emgr = global_data.emgr
        is_bind and emgr.bind_events(self.econf) if 1 else emgr.unbind_events(self.econf)

    def on_init_complete(self):
        super(BossMultiLaserBase, self).on_init_complete()
        self.register_multi_laser_callbacks()

    def register_multi_laser_callbacks(self):
        self.register_substate_callback(self.S_PRE, 0, self.start_pre)
        self.register_substate_callback(self.S_PRE, self.pre_anim_dur / self.pre_anim_rate, self.end_pre)
        self.register_substate_callback(self.S_RISE, 0, self.start_rise)
        self.register_substate_callback(self.S_RISE, self.rise_dur, self.end_rise)
        self.register_substate_callback(self.S_AIM, 0, self.start_aim)
        self.register_substate_callback(self.S_AIM, self.aim_anim_dur / self.aim_anim_rate, self.end_aim)
        self.register_substate_callback(self.S_LEAD, 0, self.start_lead)
        self.register_substate_callback(self.S_LEAD, self.lead_dur, self.end_lead)
        self.register_substate_callback(self.S_BAC, 0, self.start_bac)
        self.register_substate_callback(self.S_BAC, self.bac_anim_dur / self.bac_anim_rate, self.end_bac)

    def start_pre(self):
        self.send_event('E_ANIM_RATE', LOW_BODY, self.pre_anim_rate)
        if self.pre_anim:
            self.send_event('E_POST_ACTION', self.pre_anim, LOW_BODY, 1)
        self.reset_aim_timer()
        self.do_start_pre(self.sid)
        self.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', [E_PVE_BOSS_MULTI_LASER_START_PRE, (self.sid, True)], True)
        self.init_multi_laser()

    def do_start_pre(self, sid, is_sync=False):
        if sid != self.sid:
            return
        self.is_sync = is_sync
        self.update_col_ids()
        self.reset_all_laser_timer()
        self.spot_idx = 0
        self.laser_idx = 0
        self.hit_ts_dict = {}
        self.hit_point_dict = {}
        self.hit_target_dict = {}

    def end_pre(self):
        self.sub_state = self.S_RISE

    def start_rise(self):
        self.send_event('E_ANIM_RATE', LOW_BODY, self.rise_anim_rate)
        if self.rise_anim:
            self.send_event('E_POST_ACTION', self.rise_anim, LOW_BODY, 1, loop=True)

    def end_rise(self):
        self.sub_state = self.S_AIM

    def start_aim(self):
        self.send_event('E_ANIM_RATE', LOW_BODY, self.aim_anim_rate)
        if self.aim_anim:
            self.send_event('E_POST_ACTION', self.aim_anim, LOW_BODY, 1)
        self.init_aim()
        self.init_summon()

    def end_aim(self):
        self.sub_state = self.S_LEAD

    def start_lead(self):
        self.send_event('E_ANIM_RATE', LOW_BODY, self.lead_anim_rate)
        if self.lead_anim:
            self.send_event('E_POST_ACTION', self.lead_anim, LOW_BODY, 1, loop=True)
        self.reset_aim_timer()

    def end_lead(self):
        self.sub_state = self.S_BAC

    def on_end_lead(self):
        if self.is_sync:
            return
        self.end_lead()

    def start_bac(self):
        self.send_event('E_ANIM_RATE', LOW_BODY, self.bac_anim_rate)
        if self.bac_anim:
            self.send_event('E_POST_ACTION', self.bac_anim, LOW_BODY, 1)
        self.do_start_bac(self.sid)
        self.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', [E_PVE_BOSS_MULTI_LASER_START_BAC, (self.sid,)], True)

    def do_start_bac(self, sid):
        if sid != self.sid:
            return
        self.end_multi_laser()
        self.gen_all_end_sfx()

    def end_bac(self):
        self.sub_state = self.S_END

    def enter(self, *args):
        super(BossMultiLaserBase, self).enter(*args)
        self.send_event('E_CALL_SYNC_METHOD', 'pve_enter_skill', (self.skill_id,), True)
        self.send_event('E_DO_SKILL', self.skill_id)
        self.sub_state = self.S_PRE

    def update(self, dt):
        super(BossMultiLaserBase, self).update(dt)
        if self.sub_state == self.S_END:
            self.disable_self()
        elif self.sub_state == self.S_LEAD:
            self.send_event('E_CTRL_FACE_TO', get_aim_pos(self.target_id, self.target_pos), False)

    def exit(self, *args):
        super(BossMultiLaserBase, self).exit(*args)
        self.sub_state = self.S_END
        self.reset_aim_timer()
        self.do_exit(self.sid)
        self.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', [E_PVE_BOSS_MULTI_LASER_EXIT, (self.sid,)], True)
        self.send_event('E_CALL_SYNC_METHOD', 'pve_end_skill', (self.skill_id,), True)

    def do_exit(self, sid):
        if sid != self.sid:
            return
        self.end_multi_laser()

    def destroy(self):
        self.process_event(False)
        self.reset_aim_timer()
        self.end_multi_laser()
        super(BossMultiLaserBase, self).destroy()

    def init_aim(self):
        self.reset_aim_timer()
        self.aim_timer = global_data.game_mgr.register_logic_timer(self.update_aim, self.A_T, None, -1, CLOCK, True)
        return

    def reset_aim_timer(self):
        if self.aim_timer:
            global_data.game_mgr.unregister_logic_timer(self.aim_timer)
            self.aim_timer = None
        return

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
                return
        if diff_yaw < 0:
            ret_yaw = ori_yaw - self.aim_speed * dt
        else:
            ret_yaw = ori_yaw + self.aim_speed * dt
        self.send_event('E_CAM_YAW', ret_yaw)
        self.send_event('E_ACTION_SYNC_YAW', ret_yaw)

    def init_multi_laser(self):
        self.update_col_ids()
        self.reset_all_laser_timer()
        for ts in self.laser_ts_seq:
            self.delay_call(ts, self.init_single_spot_sfx)

        for ts in self.laser_ts_seq:
            self.delay_call(ts + self.laser_delay, self.init_single_laser)

    def end_multi_laser(self):
        self.reset_all_laser_timer()
        self.clear_all_sfx()

    def init_single_spot_sfx(self):
        pos_fix = self.laser_pos_seq[self.spot_idx]
        pos = self.ev_g_position()
        start_pos = pos + math3d.vector(*pos_fix) * NEOX_UNIT_SCALE
        angle = self.laser_angle_seq[self.spot_idx]
        rad = radians(angle)
        dire = math3d.matrix.make_rotation_y(rad).forward
        self.gen_spot_sfx(self.spot_idx, start_pos, dire)
        self.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', [E_PVE_BOSS_MULTI_LASER_INIT_SPOT, (self.sid, self.spot_idx)], True)
        self.spot_idx += 1

    def sync_init_single_spot_sfx(self, sid, spot_idx):
        if sid != self.sid:
            return
        pos_fix = self.laser_pos_seq[spot_idx]
        pos = self.ev_g_position()
        start_pos = pos + math3d.vector(*pos_fix) * NEOX_UNIT_SCALE
        angle = self.laser_angle_seq[spot_idx]
        rad = radians(angle)
        dire = math3d.matrix.make_rotation_y(rad).forward
        self.gen_spot_sfx(spot_idx, start_pos, dire)

    def init_single_laser(self):
        timer_id = None
        model = self.ev_g_model()
        if model and model.valid:
            pos_fix = self.laser_pos_seq[self.laser_idx]
            pos = self.ev_g_position()
            start_pos = pos + math3d.vector(*pos_fix) * NEOX_UNIT_SCALE
            angle = self.laser_angle_seq[self.laser_idx]
            rad = radians(angle)
            dire = math3d.matrix.make_rotation_y(rad).forward
            timer_id = global_data.game_mgr.register_logic_timer(lambda _dt=1, _idx=self.laser_idx, _pos=start_pos, _dire=dire: self.tick_laser(_dt, _idx, _pos, _dire), 1, timedelta=True)
        self.laser_timer[self.laser_idx] = timer_id
        self.hit_point_dict[self.laser_idx] = None
        self.hit_target_dict[self.laser_idx] = None
        self.hit_ts_dict[self.laser_idx] = 0
        self.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', [E_PVE_BOSS_MULTI_LASER_INIT_SINGLE, (self.sid, self.laser_idx)], True)
        self.laser_idx += 1
        return

    def sync_init_single_laser(self, sid, laser_idx):
        if sid != self.sid:
            return
        else:
            timer_id = None
            model = self.ev_g_model()
            if model and model.valid:
                pos_fix = self.laser_pos_seq[laser_idx]
                pos = self.ev_g_position()
                start_pos = pos + math3d.vector(*pos_fix) * NEOX_UNIT_SCALE
                angle = self.laser_angle_seq[laser_idx]
                rad = radians(angle)
                dire = math3d.matrix.make_rotation_y(rad).forward
                timer_id = global_data.game_mgr.register_logic_timer(lambda _dt=1, _idx=laser_idx, _pos=start_pos, _dire=dire: self.tick_laser(_dt, _idx, _pos, _dire), 1, timedelta=True)
            self.laser_timer[laser_idx] = timer_id
            self.hit_point_dict[laser_idx] = None
            self.hit_target_dict[laser_idx] = None
            self.hit_ts_dict[laser_idx] = 0
            return

    def reset_all_laser_timer(self):
        for slot in self.laser_timer:
            timer = self.laser_timer[slot]
            timer and global_data.game_mgr.unregister_logic_timer(timer)

        self.laser_timer = {}

    def tick_laser(self, dt, idx, start_pos, dire):
        end_pos = start_pos + dire * self.max_laser_dis * NEOX_UNIT_SCALE
        hit_target = None
        hit_point = None
        result = global_data.game_mgr.scene.scene_col.hit_by_ray(start_pos, end_pos, 0, -1, -1, collision.INCLUDE_FILTER, True)
        if result[0]:
            for t in result[1]:
                if t[4].cid in self._col_ids:
                    continue
                hit_point = t[0]
                hit_target = global_data.emgr.scene_find_unit_event.emit(t[4].cid)[0]
                if not hit_target:
                    continue
                else:
                    break

        if not hit_point:
            hit_point = end_pos
        self.hit_target_dict[idx] = hit_target
        self.hit_point_dict[idx] = hit_point
        self.hit_ts_dict[idx] += dt
        if self.is_active and not self.is_sync:
            if self.hit_ts_dict[idx] > self.hit_interval and hit_target:
                self.send_event('E_CALL_SYNC_METHOD', 'skill_hit_on_target', (self.skill_id, [[hit_target.id]]), False, True)
                self.hit_ts_dict[idx] = 0
        if not self.atk_sfx_id_dict.get(idx, None):
            self.gen_atk_sfx(idx, start_pos, hit_point)
        if not self.hit_sfx_id_dict.get(idx, None):
            self.gen_hit_sfx(idx, hit_point)
        self.tick_atk_sfx(idx, hit_point)
        self.tick_hit_sfx(idx, hit_point)
        return

    def gen_spot_sfx(self, idx, start_pos, dire):
        if self.spot_sfx_id_dict.get(idx, None):
            global_data.sfx_mgr.remove_sfx_by_id(self.spot_sfx_id_dict[idx])

        def cb(sfx):
            if self.spot_sfx_scale:
                sfx.scale = math3d.vector(self.spot_sfx_scale, self.spot_sfx_scale, self.spot_sfx_scale)
            if self.spot_sfx_rate:
                sfx.frame_rate = self.spot_sfx_rate
            sfx.rotation_matrix = math3d.matrix.make_orient(dire, self.UP)
            sfx.position = start_pos
            self.spot_sfx_dict[idx] = sfx

        spot_sfx_id = global_data.sfx_mgr.create_sfx_in_scene(self.spot_sfx_res, on_create_func=cb)
        self.spot_sfx_id_dict[idx] = spot_sfx_id
        return

    def gen_atk_sfx(self, idx, start_pos, hit_point):
        if self.atk_sfx_id_dict.get(idx, None):
            global_data.sfx_mgr.remove_sfx_by_id(self.atk_sfx_id_dict[idx])

        def cb(sfx):
            if self.atk_sfx_scale:
                sfx.scale = math3d.vector(self.atk_sfx_scale, self.atk_sfx_scale, self.atk_sfx_scale)
            if self.atk_sfx_rate:
                sfx.frame_rate = self.atk_sfx_rate
            sfx.position = start_pos
            sfx.end_pos = hit_point
            self.atk_sfx_dict[idx] = sfx

        atk_sfx_id = global_data.sfx_mgr.create_sfx_in_scene(self.atk_sfx_res, on_create_func=cb)
        self.atk_sfx_id_dict[idx] = atk_sfx_id
        return

    def gen_hit_sfx(self, idx, hit_point):
        if self.hit_sfx_id_dict.get(idx, None):
            global_data.sfx_mgr.remove_sfx_by_id(self.hit_sfx_id_dict[idx])

        def cb(sfx):
            if self.hit_sfx_scale:
                sfx.scale = math3d.vector(self.hit_sfx_scale, self.hit_sfx_scale, self.hit_sfx_scale)
            if self.hit_sfx_rate:
                sfx.frame_rate = self.hit_sfx_rate
            sfx.position = hit_point
            self.hit_sfx_dict[idx] = sfx

        hit_sfx_id = global_data.sfx_mgr.create_sfx_in_scene(self.hit_sfx_res, on_create_func=cb)
        self.hit_sfx_id_dict[idx] = hit_sfx_id
        return

    def tick_atk_sfx(self, idx, hit_point):
        atk_sfx = self.atk_sfx_dict.get(idx, None)
        if atk_sfx:
            atk_sfx.end_pos = hit_point
        return

    def tick_hit_sfx(self, idx, hit_point):
        hit_sfx = self.hit_sfx_dict.get(idx, None)
        if hit_sfx:
            hit_sfx.position = hit_point
        return

    def clear_all_sfx(self):
        self.clear_all_spot_sfx()
        self.clear_all_atk_sfx()
        self.clear_all_hit_sfx()

    def clear_all_spot_sfx(self):
        for slot in self.spot_sfx_id_dict:
            spot_sfx_id = self.spot_sfx_id_dict[slot]
            if spot_sfx_id:
                global_data.sfx_mgr.remove_sfx_by_id(spot_sfx_id)

        self.spot_sfx_id_dict = {}
        self.spot_sfx_dict = {}

    def clear_all_atk_sfx(self):
        for slot in self.atk_sfx_id_dict:
            atk_sfx_id = self.atk_sfx_id_dict[slot]
            if atk_sfx_id:
                global_data.sfx_mgr.remove_sfx_by_id(atk_sfx_id)

        self.atk_sfx_id_dict = {}
        self.atk_sfx_dict = {}

    def clear_all_hit_sfx(self):
        for slot in self.hit_sfx_id_dict:
            hit_sfx_id = self.hit_sfx_id_dict[slot]
            if hit_sfx_id:
                global_data.sfx_mgr.remove_sfx_by_id(hit_sfx_id)

        self.hit_sfx_id_dict = {}
        self.hit_sfx_dict = {}

    def gen_all_end_sfx(self):
        for slot in self.hit_point_dict:
            hit_point = self.hit_point_dict[slot]
            self.gen_end_sfx(slot, hit_point)

    def gen_end_sfx(self, idx, hit_point):
        if not self.end_sfx_res:
            return
        pos_fix = self.laser_pos_seq[idx]
        pos = self.ev_g_position()
        start_pos = pos + math3d.vector(*pos_fix) * NEOX_UNIT_SCALE

        def cb(sfx):
            if self.end_sfx_scale:
                sfx.scale = math3d.vector(self.end_sfx_scale, self.end_sfx_scale, self.end_sfx_scale)
            if self.end_sfx_rate:
                sfx.frame_rate = self.end_sfx_rate
            sfx.position = start_pos
            if hit_point:
                sfx.end_pos = hit_point

        global_data.sfx_mgr.create_sfx_in_scene(self.end_sfx_res, on_create_func=cb)

    def init_summon(self):
        for i in range(0, len(self.summon_socket_list)):
            self.send_event('E_CALL_SYNC_METHOD', 'do_skill', (self.summon_skill_id, self.post_data(i)), False, True)

    def update_col_ids(self):
        self._col_ids = self.ev_g_human_col_id()

    def post_data(self, idx):
        model = self.ev_g_model()
        mat = model.get_socket_matrix(self.summon_socket_list[idx], 1)
        pos = mat.translation
        dire = mat.forward
        data = ((pos.x, pos.y, pos.z), (dire.x, dire.y, dire.z), self.target_id, (self.target_pos.x, self.target_pos.y, self.target_pos.z))
        return data


class BossMultiLaser(BossMultiLaserBase):

    def init_params(self):
        super(BossMultiLaser, self).init_params()
        self.skill_id = self.custom_param.get('skill_id', None)
        self.summon_skill_id = self.custom_param.get('summon_skill_id', None)
        self.laser_ts_seq = self.custom_param.get('laser_ts_seq', [])
        self.laser_pos_seq = self.custom_param.get('laser_pos_seq', [])
        self.laser_angle_seq = self.custom_param.get('laser_angle_seq', [])
        self.laser_delay = self.custom_param.get('laser_delay', 0)
        self.max_laser_dis = self.custom_param.get('max_laser_dis', 0)
        self.hit_interval = self.custom_param.get('hit_interval', 0.5)
        self.pre_anim = self.custom_param.get('pre_anim', '')
        self.pre_anim_dur = self.custom_param.get('pre_anim_dur', 0)
        self.pre_anim_rate = self.custom_param.get('pre_anim_rate', 1.0)
        self.rise_anim = self.custom_param.get('rise_anim', '')
        self.rise_dur = self.custom_param.get('rise_dur', 0)
        self.rise_anim_rate = self.custom_param.get('rise_anim_rate', 1.0)
        self.aim_anim = self.custom_param.get('aim_anim', '')
        self.aim_anim_dur = self.custom_param.get('aim_anim_dur', 0)
        self.aim_anim_rate = self.custom_param.get('aim_anim_rate', 1.0)
        self.aim_speed = self.custom_param.get('aim_speed', 0)
        self.lead_anim = self.custom_param.get('lead_anim', '')
        self.lead_dur = self.custom_param.get('lead_dur', 0)
        self.lead_anim_rate = self.custom_param.get('lead_anim_rate', 1.0)
        self.bac_anim = self.custom_param.get('bac_anim', '')
        self.bac_anim_dur = self.custom_param.get('bac_anim_dur', 0)
        self.bac_anim_rate = self.custom_param.get('bac_anim_rate', 1.0)
        self.spot_sfx_res = self.custom_param.get('spot_sfx_res', '')
        self.spot_sfx_rate = self.custom_param.get('spot_sfx_rate', None)
        self.spot_sfx_scale = self.custom_param.get('spot_sfx_scale', None)
        self.atk_sfx_res = self.custom_param.get('atk_sfx_res', '')
        self.atk_sfx_rate = self.custom_param.get('atk_sfx_rate', None)
        self.atk_sfx_scale = self.custom_param.get('atk_sfx_scale', None)
        self.end_sfx_res = self.custom_param.get('end_sfx_res', '')
        self.end_sfx_rate = self.custom_param.get('end_sfx_rate', None)
        self.end_sfx_scale = self.custom_param.get('end_sfx_scale', None)
        self.hit_sfx_res = self.custom_param.get('hit_sfx_res', '')
        self.hit_sfx_rate = self.custom_param.get('hit_sfx_rate', None)
        self.hit_sfx_scale = self.custom_param.get('hit_sfx_scale', None)
        self.summon_socket_list = self.custom_param.get('summon_socket_list', [])
        return

    def editor_handle(self):
        if global_data.use_sunshine:
            self.init_params()
            self.reset_sub_states_callback()
            self.register_multi_laser_callbacks()