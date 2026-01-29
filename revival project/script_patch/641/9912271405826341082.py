# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/behavior/PVEMonsterLaserLogic.py
from __future__ import absolute_import
from .MonsterStateBase import MonsterStateBase
import math3d
from logic.gcommon.common_const.character_anim_const import LOW_BODY
import collision
from logic.gcommon.const import NEOX_UNIT_SCALE
from logic.gutils.pve_utils import get_aim_pos

class MonsterLaserBase(MonsterStateBase):
    BIND_EVENT = {'E_ACTIVE_PARAM_STATE': 'pre_check_param'
       }
    econf = {}
    S_END = 0
    S_INT = 1
    S_PRE = 2
    S_ATK = 3
    S_BAC = 4

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
        super(MonsterLaserBase, self).init_from_dict(unit_obj, bdict, sid, info)
        self.init_params()
        self.process_event(True)
        self.sub_state = self.S_END

    def init_params(self):
        self.aim_timer = None
        self._col_ids = []
        self.hit_ts = 0
        self.hit_target = None
        self.pre_sfx_id = None
        self.atk_sfx_id = None
        self.pre_sfx = None
        self.atk_sfx = None
        self.hit_point = None
        self.face_to = True
        self.target_forward = None
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
        super(MonsterLaserBase, self).on_init_complete()
        self.register_laser_callbacks()

    def register_laser_callbacks(self):
        self.register_substate_callback(self.S_INT, 0, self.start_int)
        self.register_substate_callback(self.S_INT, self.int_anim_dur / self.int_anim_rate, self.end_int)
        self.register_substate_callback(self.S_PRE, 0, self.start_pre)
        self.register_substate_callback(self.S_PRE, self.pre_anim_dur / self.pre_anim_rate, self.end_pre)
        self.register_substate_callback(self.S_ATK, 0, self.start_atk)
        self.register_substate_callback(self.S_ATK, self.max_atk_dur, self.end_atk)
        self.register_substate_callback(self.S_BAC, 0, self.start_bac)
        self.register_substate_callback(self.S_BAC, self.bac_anim_dur / self.bac_anim_rate, self.end_bac)

    def start_int(self):
        self.send_event('E_DO_SKILL', self.skill_id)
        self.send_event('E_ANIM_RATE', LOW_BODY, self.int_anim_rate)
        self.send_event('E_POST_ACTION', self.int_anim, LOW_BODY, 1)

    def end_int(self):
        self.sub_state = self.S_PRE

    def start_pre(self):
        self.send_event('E_ANIM_RATE', LOW_BODY, self.pre_anim_rate)
        self.send_event('E_POST_ACTION', self.pre_anim, LOW_BODY, 1)
        self.start_aim()

    def end_pre(self):
        self.sub_state = self.S_ATK
        self.clear_pre_sfx()

    def start_atk(self):
        self.send_event('E_ANIM_RATE', LOW_BODY, self.atk_anim_rate)
        self.send_event('E_POST_ACTION', self.atk_anim, LOW_BODY, 1, loop=True)

    def end_atk(self):
        self.sub_state = self.S_BAC
        self.end_aim()

    def start_bac(self):
        self.send_event('E_ANIM_RATE', LOW_BODY, self.bac_anim_rate)
        self.send_event('E_POST_ACTION', self.bac_anim, LOW_BODY, 1)

    def end_bac(self):
        self.sub_state = self.S_END

    def enter(self, leave_states):
        super(MonsterLaserBase, self).enter(leave_states)
        self.send_event('E_CALL_SYNC_METHOD', 'pve_enter_skill', (self.skill_id,), True)
        self.sub_state = self.S_INT

    def update(self, dt):
        super(MonsterLaserBase, self).update(dt)
        self.hit_ts += dt
        if self.sub_state == self.S_END:
            self.disable_self()
        if self.sub_state == self.S_INT and self.face_to:
            self.send_event('E_CTRL_FACE_TO', get_aim_pos(self.target_id, self.target_pos), False)
        if self.hit_ts > self.hit_interval and self.hit_target and self.sub_state == self.S_ATK:
            self.send_event('E_CALL_SYNC_METHOD', 'skill_hit_on_target', (self.skill_id, [[self.hit_target.id]]), False, True)
            self.hit_ts = 0

    def exit(self, enter_states):
        super(MonsterLaserBase, self).exit(enter_states)
        self.sub_state = self.S_END
        self.end_aim()
        self.send_event('E_CALL_SYNC_METHOD', 'pve_end_skill', (self.skill_id,), True)

    def destroy(self):
        self.end_aim()
        self.process_event(False)
        super(MonsterLaserBase, self).destroy()

    def reset_aim_timer(self):
        if self.aim_timer:
            global_data.game_mgr.unregister_logic_timer(self.aim_timer)
            self.aim_timer = None
        return

    def start_aim(self):
        self.update_col_ids()
        self.reset_aim_timer()
        self.aim_timer = global_data.game_mgr.register_logic_timer(self.tick_aim, 1, timedelta=True)

    def tick_aim(self, dt):
        target_pos = get_aim_pos(self.target_id, self.target_pos)
        start_pos = self.ev_g_position()
        start_pos.y += 25
        start_pos.y += self.height_offset
        tar_dir = target_pos - start_pos
        tar_dir.normalize()
        if self.face_to:
            forward = self.ev_g_forward()
        else:
            forward = self.target_forward if self.target_forward else tar_dir
        forward.normalize()
        diff = tar_dir - forward
        if diff.is_zero:
            pass
        tar_forward = math3d.vector(0, 0, 0)
        if self.sub_state == self.S_PRE:
            track_ratio = self.pre_track_ratio if 1 else self.atk_track_ratio
            tar_forward.intrp(forward, tar_dir, track_ratio)
            tar_forward.normalize()
            tar_forward.y = tar_dir.y
            end_pos = start_pos + tar_forward * self.max_laser_dis * NEOX_UNIT_SCALE
            self.hit_target = None
            hit_point = None
            result = global_data.game_mgr.scene.scene_col.hit_by_ray(start_pos, end_pos, 0, -1, -1, collision.INCLUDE_FILTER, True)
            if result[0]:
                for t in result[1]:
                    if t[4].cid in self._col_ids:
                        continue
                    hit_point = t[0]
                    self.hit_target = global_data.emgr.scene_find_unit_event.emit(t[4].cid)[0]
                    if not self.hit_target:
                        continue
                    else:
                        break

            if not hit_point:
                hit_point = end_pos
            self.hit_point = hit_point
            if self.face_to:
                self.send_event('E_CTRL_FACE_TO', hit_point, False)
            else:
                self.target_forward = tar_forward
            if self.sub_state == self.S_PRE:
                self.pre_sfx_id or self.gen_pre_sfx(hit_point)
            self.tick_pre_sfx(hit_point)
        elif self.sub_state == self.S_ATK:
            if not self.atk_sfx_id:
                self.gen_atk_sfx(hit_point)
            self.tick_atk_sfx(hit_point)
        return

    def end_aim(self):
        self.reset_aim_timer()
        self.gen_end_sfx(self.hit_point)
        self.clear_sfx()

    def update_col_ids(self):
        self._col_ids = self.ev_g_human_col_id()

    def gen_pre_sfx(self, hit_point):
        if self.pre_sfx_id:
            global_data.sfx_mgr.remove_sfx_by_id(self.pre_sfx_id)
        if not self.pre_sfx_res:
            return

        def cb(sfx):
            sfx.scale = math3d.vector(self.pre_sfx_scale, self.pre_sfx_scale, self.pre_sfx_scale)
            sfx.frame_rate = self.pre_sfx_rate
            self.pre_sfx = sfx
            sfx.end_pos = hit_point

        self.pre_sfx_id = global_data.sfx_mgr.create_sfx_on_model(self.pre_sfx_res, self.ev_g_model(), self.pre_socket, on_create_func=cb)

    def gen_atk_sfx(self, hit_point):
        if self.atk_sfx_id:
            global_data.sfx_mgr.remove_sfx_by_id(self.atk_sfx_id)

        def cb(sfx):
            sfx.scale = math3d.vector(self.atk_sfx_scale, self.atk_sfx_scale, self.atk_sfx_scale)
            self.atk_sfx = sfx
            sfx.end_pos = hit_point

        self.atk_sfx_id = global_data.sfx_mgr.create_sfx_on_model(self.atk_sfx_res, self.ev_g_model(), self.atk_socket, on_create_func=cb)

    def tick_pre_sfx(self, hit_point):
        if self.pre_sfx:
            self.pre_sfx.end_pos = hit_point

    def tick_atk_sfx(self, hit_point):
        if self.atk_sfx:
            self.atk_sfx.end_pos = hit_point

    def clear_pre_sfx(self):
        if self.pre_sfx_id:
            global_data.sfx_mgr.remove_sfx_by_id(self.pre_sfx_id)
            self.pre_sfx_id = None
            self.pre_sfx = None
        return

    def clear_atk_sfx(self):
        if self.atk_sfx_id:
            global_data.sfx_mgr.remove_sfx_by_id(self.atk_sfx_id)
            self.atk_sfx_id = None
            self.atk_sfx = None
        return

    def clear_sfx(self):
        self.clear_pre_sfx()
        self.clear_atk_sfx()

    def gen_hit_sfx(self):
        pass

    def gen_end_sfx(self, hit_point):
        if not self.end_sfx_res:
            return
        if not hit_point:
            return

        def cb(sfx):
            sfx.scale = math3d.vector(self.end_sfx_scale, self.end_sfx_scale, self.end_sfx_scale)
            sfx.end_pos = hit_point
            self.hit_point = None
            return

        global_data.sfx_mgr.create_sfx_on_model(self.end_sfx_res, self.ev_g_model(), self.end_socket, on_create_func=cb)


class MonsterLaser(MonsterLaserBase):

    def init_params(self):
        super(MonsterLaser, self).init_params()
        self.skill_id = self.custom_param.get('skill_id', 9015155)
        self.max_atk_dur = self.custom_param.get('max_atk_dur', 5.0)
        self.pre_track_ratio = self.custom_param.get('pre_track_ratio', 0.05)
        self.atk_track_ratio = self.custom_param.get('atk_track_ratio', 0.05)
        self.max_laser_dis = self.custom_param.get('max_laser_dis', 100)
        self.hit_interval = self.custom_param.get('hit_interval', 0.5)
        self.pre_socket = self.custom_param.get('pre_socket', 'fx_kaihuo1')
        self.pre_sfx_res = self.custom_param.get('pre_sfx_res', 'effect/fx/mecha/8008/8008_aux_aim.sfx')
        self.pre_sfx_scale = self.custom_param.get('pre_sfx_scale', 1.0)
        self.pre_sfx_rate = self.custom_param.get('pre_sfx_rate', 1.0)
        self.atk_socket = self.custom_param.get('atk_socket', 'fx_kaihuo1')
        self.atk_sfx_res = self.custom_param.get('atk_sfx_res', 'effect/fx/mecha/8008/8008_aux_aim.sfx')
        self.atk_sfx_scale = self.custom_param.get('atk_sfx_scale', 4.0)
        self.end_socket = self.custom_param.get('end_socket', 'fx_kaihuo1')
        self.end_sfx_res = self.custom_param.get('end_sfx_res', 'effect/fx/mecha/8008/8008_aux_aim.sfx')
        self.end_sfx_scale = self.custom_param.get('end_sfx_scale', 1.0)
        self.int_anim = self.custom_param.get('int_anim', 'attack_03')
        self.int_anim_dur = self.custom_param.get('int_anim_dur', 1.4)
        self.int_anim_rate = self.custom_param.get('int_anim_rate', 1.0)
        self.pre_anim = self.custom_param.get('pre_anim', 'hit')
        self.pre_anim_dur = self.custom_param.get('pre_anim_dur', 0.7)
        self.pre_anim_rate = self.custom_param.get('pre_anim_rate', 1.0)
        self.atk_anim = self.custom_param.get('atk_anim', 'run')
        self.atk_anim_rate = self.custom_param.get('atk_anim_rate', 1.0)
        self.bac_anim = self.custom_param.get('bac_anim', 'hit')
        self.bac_anim_dur = self.custom_param.get('bac_anim_dur', 0.7)
        self.bac_anim_rate = self.custom_param.get('bac_anim_rate', 1.0)
        self.face_to = self.custom_param.get('face_to', True)
        self.height_offset = self.custom_param.get('height_offset', 25.0)

    def editor_handle(self):
        if global_data.use_sunshine:
            self.init_params()
            self.reset_sub_states_callback()
            self.register_laser_callbacks()