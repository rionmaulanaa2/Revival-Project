# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/behavior/PVEMonsterSweepLogic.py
from __future__ import absolute_import
import six_ex
from .MonsterStateBase import MonsterStateBase
import math3d
from logic.gcommon.common_const.character_anim_const import LOW_BODY
import collision
from logic.gcommon.const import NEOX_UNIT_SCALE
from logic.gutils.pve_utils import get_aim_pos, get_bias_aim_pos
from math import radians
from logic.gcommon.common_utils.bcast_utils import E_PVE_MONSTER_SWEEP_START_ATK, E_PVE_MONSTER_SWEEP_START_BAC, E_PVE_MONSTER_SWEEP_EXIT
import world

class MonsterSweepBase(MonsterStateBase):
    BIND_EVENT = {'E_ACTIVE_PARAM_STATE': 'pre_check_param',
       'E_PVE_MONSTER_SWEEP_START_ATK': 'do_start_atk',
       'E_PVE_MONSTER_SWEEP_START_BAC': 'do_start_bac',
       'E_PVE_MONSTER_SWEEP_EXIT': 'do_exit'
       }
    econf = {}
    S_END = 0
    S_PRE = 1
    S_ATK = 2
    S_BAC = 3
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
        super(MonsterSweepBase, self).init_from_dict(unit_obj, bdict, sid, info)
        self.init_params()
        self.process_event(True)
        self.sub_state = self.S_END

    def init_params(self):
        self.target_id = None
        self.target_pos = None
        self.bias_dur = 0
        self.is_sync = False
        self.sweep_timer = None
        self.start_angle = 0
        self.end_angle = 0
        self.hit_point = None
        self.height_offset = 0
        self._col_ids = []
        self._hit_set = {}
        self.sweep_ts = 0
        self.atk_sfx = None
        self.atk_sfx_id = None
        self.hit_sfx = None
        self.hit_sfx_id = None
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
        super(MonsterSweepBase, self).on_init_complete()
        self.register_sweep_callbacks()
        self.bias_dur = self.sd.ref_bias_dur

    def register_sweep_callbacks(self):
        self.register_substate_callback(self.S_PRE, 0, self.start_pre)
        self.register_substate_callback(self.S_PRE, self.pre_anim_dur / self.pre_anim_rate, self.end_pre)
        self.register_substate_callback(self.S_ATK, 0, self.start_atk)
        self.register_substate_callback(self.S_ATK, self.atk_anim_dur / self.atk_anim_rate, self.end_atk)
        self.register_substate_callback(self.S_BAC, 0, self.start_bac)
        self.register_substate_callback(self.S_BAC, self.bac_anim_dur / self.bac_anim_rate, self.end_bac)

    def start_pre(self):
        self.send_event('E_ANIM_RATE', LOW_BODY, self.pre_anim_rate)
        if self.pre_anim:
            self.send_event('E_POST_ACTION', self.pre_anim, LOW_BODY, 1)

    def end_pre(self):
        self.sub_state = self.S_ATK

    def start_atk(self):
        self.send_event('E_ANIM_RATE', LOW_BODY, self.atk_anim_rate)
        if self.atk_anim:
            self.send_event('E_POST_ACTION', self.atk_anim, LOW_BODY, 1, loop=True)
        if not self.target_pos:
            self.target_pos = math3d.vector(0, 0, 0)
        self.do_start_atk(self.sid)
        self.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', [E_PVE_MONSTER_SWEEP_START_ATK, (self.sid, self.target_id, (self.target_pos.x, self.target_pos.y, self.target_pos.z), True)], True)

    def do_start_atk(self, sid, target_id=None, target_pos=None, is_sync=False):
        if sid != self.sid:
            return
        if target_id:
            self.target_id = target_id
        if target_pos and is_sync:
            self.target_pos = math3d.vector(*target_pos)
        self.is_sync = is_sync
        self.init_sweep()

    def end_atk(self):
        self.sub_state = self.S_BAC

    def start_bac(self):
        self.send_event('E_ANIM_RATE', LOW_BODY, self.bac_anim_rate)
        if self.bac_anim:
            self.send_event('E_POST_ACTION', self.bac_anim, LOW_BODY, 1)
        self.do_start_bac(self.sid)
        self.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', [E_PVE_MONSTER_SWEEP_START_BAC, (self.sid,)], True)

    def do_start_bac(self, sid):
        if sid != self.sid:
            return
        self.end_sweep()
        self.gen_end_sfx(self.hit_point)

    def end_bac(self):
        self.sub_state = self.S_END

    def enter(self, *args):
        super(MonsterSweepBase, self).enter(*args)
        self.send_event('E_CALL_SYNC_METHOD', 'pve_enter_skill', (self.skill_id,), True)
        self.send_event('E_DO_SKILL', self.skill_id)
        self.send_event('E_CTRL_FACE_TO', get_aim_pos(self.target_id, self.target_pos), False)
        self.sub_state = self.S_PRE

    def update(self, dt):
        super(MonsterSweepBase, self).update(dt)
        if self.sub_state == self.S_END:
            self.disable_self()
        elif self.sub_state == self.S_PRE:
            self.send_event('E_CTRL_FACE_TO', get_bias_aim_pos(self.target_id, self.target_pos, True, self.bias_dur), False)

    def exit(self, *args):
        super(MonsterSweepBase, self).exit(*args)
        self.sub_state = self.S_END
        self.do_exit(self.sid)
        self.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', [E_PVE_MONSTER_SWEEP_EXIT, (self.sid,)], True)
        self.send_event('E_CALL_SYNC_METHOD', 'pve_end_skill', (self.skill_id,), True)

    def do_exit(self, sid):
        if sid != self.sid:
            return
        self.end_sweep()

    def destroy(self):
        self.end_sweep()
        self.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', [E_PVE_MONSTER_SWEEP_EXIT, ()], True)
        self.process_event(False)
        super(MonsterSweepBase, self).destroy()

    def init_sweep(self):
        self.update_col_ids()
        self.reset_sweep_timer()
        self.sweep_ts = 0
        self._hit_set = {}
        self.forward_mat = None
        self.fix_forward()
        self.sweep_timer = global_data.game_mgr.register_logic_timer(self.tick_sweep, 1, timedelta=True)
        return

    def reset_sweep_timer(self):
        if self.sweep_timer:
            global_data.game_mgr.unregister_logic_timer(self.sweep_timer)
            self.sweep_timer = None
        return

    def fix_forward(self):
        model = self.ev_g_model()
        if not model or not model.valid:
            return
        mat = model.get_socket_matrix(self.atk_socket, world.SPACE_TYPE_WORLD)
        self.start_pos = mat.translation
        target_pos = get_bias_aim_pos(self.target_id, self.target_pos, True, self.bias_dur)
        target_dire = target_pos - self.start_pos
        target_dire.normalize()
        forward_mat = math3d.matrix.make_orient(target_dire, self.UP)
        self.forward_mat = forward_mat

    def tick_sweep(self, dt):
        total_dur = self.atk_anim_dur / self.atk_anim_rate
        tar_angle = self.start_angle + self.sweep_ts / total_dur * (self.end_angle - self.start_angle)
        forward_mat = self.forward_mat
        if not forward_mat:
            self.reset_sweep_timer()
            return
        else:
            up = forward_mat.up
            tar_mat = forward_mat * math3d.matrix.make_rotation(up, -radians(tar_angle))
            tar_dire = tar_mat.forward
            tar_dire.normalize()
            end_pos = self.start_pos + tar_dire * self.max_sweep_dis * NEOX_UNIT_SCALE
            hit_target = None
            hit_point = None
            result = global_data.game_mgr.scene.scene_col.hit_by_ray(self.start_pos, end_pos, 0, -1, -1, collision.INCLUDE_FILTER, True)
            if result[0]:
                for t in result[1]:
                    if t[4].cid in self._col_ids:
                        continue
                    hit_point = t[0]
                    hit_target = global_data.emgr.scene_find_unit_event.emit(t[4].cid)[0]
                    if not hit_target:
                        continue
                    else:
                        if hit_target.ev_g_is_campmate(self.ev_g_camp_id()):
                            continue
                        if hit_target.id not in self._hit_set:
                            self._hit_set[hit_target.id] = 1
                            if self.is_sync:
                                pass
                            else:
                                self.send_event('E_CALL_SYNC_METHOD', 'skill_hit_on_target', (
                                 self.skill_id, [six_ex.keys(self._hit_set)]), False, True)
                        break

            if not hit_point:
                hit_point = end_pos
            self.hit_point = hit_point
            if self.sub_state == self.S_ATK or self.is_sync:
                if not self.atk_sfx_id:
                    self.gen_atk_sfx(hit_point)
                if not self.hit_sfx_id:
                    self.gen_hit_sfx(hit_point)
                self.tick_atk_sfx(hit_point)
                self.tick_hit_sfx(hit_point)
            self.sweep_ts += dt
            if self.sweep_ts > total_dur:
                self.reset_sweep_timer()
            return

    def end_sweep(self):
        self.reset_sweep_timer()
        self.clear_sfx()

    def update_col_ids(self):
        self._col_ids = self.ev_g_human_col_id()

    def gen_atk_sfx(self, hit_point):
        if self.atk_sfx_id:
            global_data.sfx_mgr.remove_sfx_by_id(self.atk_sfx_id)

        def cb(sfx):
            if self.atk_sfx_scale:
                sfx.scale = math3d.vector(self.atk_sfx_scale, self.atk_sfx_scale, self.atk_sfx_scale)
            if self.atk_sfx_rate:
                sfx.frame_rate = self.atk_sfx_rate
            self.atk_sfx = sfx
            sfx.end_pos = hit_point

        self.atk_sfx_id = global_data.sfx_mgr.create_sfx_on_model(self.atk_sfx_res, self.ev_g_model(), self.atk_socket, on_create_func=cb)

    def gen_hit_sfx(self, hit_point):
        if self.hit_sfx_id:
            global_data.sfx_mgr.remove_sfx_by_id(self.hit_sfx_id)

        def cb(sfx):
            if self.hit_sfx_scale:
                sfx.scale = math3d.vector(self.hit_sfx_scale, self.hit_sfx_scale, self.hit_sfx_scale)
            if self.hit_sfx_rate:
                sfx.frame_rate = self.hit_sfx_rate
            self.hit_sfx = sfx
            sfx.position = hit_point

        self.hit_sfx_id = global_data.sfx_mgr.create_sfx_in_scene(self.hit_sfx_res, on_create_func=cb)

    def tick_atk_sfx(self, hit_point):
        if self.atk_sfx:
            self.atk_sfx.end_pos = hit_point

    def tick_hit_sfx(self, hit_point):
        if self.hit_sfx:
            self.hit_sfx.position = hit_point

    def clear_atk_sfx(self):
        if self.atk_sfx_id:
            global_data.sfx_mgr.remove_sfx_by_id(self.atk_sfx_id)
            self.atk_sfx_id = None
            self.atk_sfx = None
        return

    def clear_hit_sfx(self):
        if self.hit_sfx_id:
            global_data.sfx_mgr.remove_sfx_by_id(self.hit_sfx_id)
            self.hit_sfx_id = None
            self.hit_sfx = None
        return

    def clear_sfx(self):
        self.clear_atk_sfx()
        self.clear_hit_sfx()

    def gen_end_sfx(self, hit_point):
        if not self.end_sfx_res:
            return

        def cb(sfx):
            if self.end_sfx_scale:
                sfx.scale = math3d.vector(self.end_sfx_scale, self.end_sfx_scale, self.end_sfx_scale)
            if self.end_sfx_rate:
                sfx.frame_rate = self.end_sfx_rate
            sfx.end_pos = hit_point

        global_data.sfx_mgr.create_sfx_on_model(self.end_sfx_res, self.ev_g_model(), self.end_socket, on_create_func=cb)


class MonsterSweep(MonsterSweepBase):

    def init_params(self):
        super(MonsterSweep, self).init_params()
        self.skill_id = self.custom_param.get('skill_id', None)
        self.start_angle = self.custom_param.get('start_angle', 0)
        self.end_angle = self.custom_param.get('end_angle', 0)
        self.height_offset = self.custom_param.get('height_offset', 25)
        self.max_sweep_dis = self.custom_param.get('max_sweep_dis')
        self.pre_anim = self.custom_param.get('pre_anim', '')
        self.pre_anim_dur = self.custom_param.get('pre_anim_dur', 0)
        self.pre_anim_rate = self.custom_param.get('pre_anim_rate', 1.0)
        self.atk_anim = self.custom_param.get('atk_anim', '')
        self.atk_anim_dur = self.custom_param.get('atk_anim_dur', 0)
        self.atk_anim_rate = self.custom_param.get('atk_anim_rate', 1.0)
        self.bac_anim = self.custom_param.get('bac_anim', '')
        self.bac_anim_dur = self.custom_param.get('bac_anim_dur', 0)
        self.bac_anim_rate = self.custom_param.get('bac_anim_rate', 1.0)
        self.atk_socket = self.custom_param.get('atk_socket', 'fx_kaihuo')
        self.atk_sfx_res = self.custom_param.get('atk_sfx_res', '')
        self.atk_sfx_rate = self.custom_param.get('atk_sfx_rate', None)
        self.atk_sfx_scale = self.custom_param.get('atk_sfx_scale', None)
        self.end_socket = self.custom_param.get('end_socket', 'fx_kaihuo')
        self.end_sfx_res = self.custom_param.get('end_sfx_res', '')
        self.end_sfx_rate = self.custom_param.get('end_sfx_rate', None)
        self.end_sfx_scale = self.custom_param.get('end_sfx_scale', None)
        self.hit_sfx_res = self.custom_param.get('hit_sfx_res', '')
        self.hit_sfx_rate = self.custom_param.get('hit_sfx_rate', None)
        self.hit_sfx_scale = self.custom_param.get('hit_sfx_scale', None)
        return

    def editor_handle(self):
        if global_data.use_sunshine:
            self.init_params()
            self.bias_dur = self.sd.ref_bias_dur
            self.reset_sub_states_callback()
            self.register_sweep_callbacks()