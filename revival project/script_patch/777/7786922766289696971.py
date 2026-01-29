# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/behavior/PVEMonsterSnipeLogic.py
from __future__ import absolute_import
from .MonsterStateBase import MonsterStateBase
import math3d
from logic.gcommon.common_const.character_anim_const import LOW_BODY
from math import pi
from logic.gcommon.common_const.idx_const import ExploderID
from common.utils.timer import CLOCK
import world
from common.cfg import confmgr
import collision
from logic.gutils.pve_utils import get_aim_pos
from logic.gcommon.common_utils.bcast_utils import E_PVE_MONSTER_SNIPE_START_PRE, E_PVE_MONSTER_SNIPE_END_PRE, E_PVE_MONSTER_SNIPE_EXIT
from logic.gcommon.common_const.collision_const import S_GROUP_SCENE

class MonsterSnipeBase(MonsterStateBase):
    BIND_EVENT = {'E_ACTIVE_PARAM_STATE': 'pre_check_param',
       'E_PVE_MONSTER_SNIPE_START_PRE': 'do_start_pre',
       'E_PVE_MONSTER_SNIPE_END_PRE': 'do_end_pre',
       'E_PVE_MONSTER_SNIPE_EXIT': 'do_exit'
       }
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
        super(MonsterSnipeBase, self).init_from_dict(unit_obj, bdict, sid, info)
        self.init_params()
        self.process_event(True)
        self.sub_state = self.S_END

    def init_params(self):
        self.target_id = None
        self.target_pos = None
        self.wp_pos = 0
        self.yaw_ts = 0
        self.aim_timer = None
        self.aim_lr = 0
        self.aim_left_anim = None
        self.aim_right_anim = None
        self.pre_sfx_timer = None
        self.pre_sfx_id = None
        self.pre_link_sfx_id = None
        self.pre_link_sfx = None
        self.trace_dur = 0
        self.trace_tag = False
        self.hit_point = None
        self._col_ids = []
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
        super(MonsterSnipeBase, self).on_init_complete()
        self.register_snipe_callbacks()

    def register_snipe_callbacks(self):
        self.register_substate_callback(self.S_PRE, 0, self.start_pre)
        self.register_substate_callback(self.S_PRE, self.pre_anim_dur / self.pre_anim_rate, self.end_pre)
        self.register_substate_callback(self.S_ATK, 0, self.start_atk)
        self.register_substate_callback(self.S_ATK, self.atk_anim_dur / self.atk_anim_rate, self.end_atk)
        self.register_substate_callback(self.S_BAC, 0, self.start_bac)
        self.register_substate_callback(self.S_BAC, self.bac_anim_dur / self.bac_anim_rate, self.end_bac)

    def start_pre(self):
        self.trace_tag = True
        if self.trace_dur:
            self.delay_call(self.trace_dur, self.end_trace)
        self.reset_aim_timer()
        if not self.pre_anim_dur:
            return
        self.send_event('E_DO_SKILL', self.skill_id)
        self.send_event('E_ANIM_RATE', LOW_BODY, self.pre_anim_rate)
        self.send_event('E_POST_ACTION', self.pre_anim, LOW_BODY, 1)
        if not self.target_pos:
            self.target_pos = math3d.vector(0, 0, 0)
        self.do_start_pre(self.sid)
        self.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', [E_PVE_MONSTER_SNIPE_START_PRE, (self.sid, self.target_id, (self.target_pos.x, self.target_pos.y, self.target_pos.z), True)], True)

    def do_start_pre(self, sid, target_id=None, target_pos=None, is_sync=False):
        if sid != self.sid:
            return
        if target_id:
            self.target_id = target_id
        if is_sync:
            self.trace_tag = True
            if target_pos:
                self.target_pos = math3d.vector(*target_pos)
        self.update_col_ids()
        self.start_pre_sfx()

    def end_trace(self):
        self.trace_tag = False

    def end_pre(self):
        self.sub_state = self.S_ATK
        self.do_end_pre(self.sid)
        self.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', [E_PVE_MONSTER_SNIPE_END_PRE, (self.sid,)], True)

    def do_end_pre(self, sid):
        if sid != self.sid:
            return
        self.end_pre_sfx()

    def start_atk(self):
        if not self.atk_anim_dur:
            return
        self.send_event('E_ANIM_RATE', LOW_BODY, self.atk_anim_rate)
        self.send_event('E_POST_ACTION', self.atk_anim, LOW_BODY, 1)
        self.init_fire()

    def end_atk(self):
        self.sub_state = self.S_BAC

    def start_bac(self):
        if not self.bac_anim_dur:
            return
        self.send_event('E_ANIM_RATE', LOW_BODY, self.bac_anim_rate)
        self.send_event('E_POST_ACTION', self.bac_anim, LOW_BODY, 1)

    def end_bac(self):
        self.sub_state = self.S_END

    def start_pre_sfx(self):
        self.reset_sfx_timer()
        model = self.ev_g_model()
        if not model or not model.valid:
            return
        else:
            if self.pre_sfx_res:

                def cb(sfx):
                    sfx.scale = math3d.vector(self.pre_sfx_scale, self.pre_sfx_scale, self.pre_sfx_scale)
                    sfx.frame_rate = self.pre_sfx_rate

                self.pre_sfx_id = global_data.sfx_mgr.create_sfx_on_model(self.pre_sfx_res, model, self.pre_sfx_socket, on_create_func=cb)

            def cb_link(sfx):
                sfx.scale = math3d.vector(self.pre_link_sfx_scale, self.pre_link_sfx_scale, self.pre_link_sfx_scale)
                sfx.frame_rate = self.pre_link_sfx_rate
                sfx.visible = False
                self.pre_link_sfx = sfx

            self.pre_link_sfx_id = global_data.sfx_mgr.create_sfx_on_model(self.pre_link_sfx_res, model, self.pre_link_sfx_socket, on_create_func=cb_link)
            self.pre_sfx_timer = global_data.game_mgr.register_logic_timer(self.tick_sfx, self.A_T, None, -1, CLOCK)
            return

    def tick_sfx(self, *args):
        if not self.trace_tag:
            self.reset_sfx_timer()
            return
        else:
            hit_point = None
            if self.pre_link_sfx:
                self.pre_link_sfx.visible = True
                model = self.ev_g_model()
                if not model or not model.valid:
                    return
                start_pos = model.get_socket_matrix(self.pre_link_sfx_socket, world.SPACE_TYPE_WORLD).translation
                target_pos = get_aim_pos(self.target_id, self.target_pos)
                if not start_pos or not target_pos:
                    return
                result = global_data.game_mgr.scene.scene_col.hit_by_ray(start_pos, target_pos, 0, -1, -1, collision.INCLUDE_FILTER, True)
                if result[0]:
                    for t in result[1]:
                        if t[4].cid in self._col_ids:
                            continue
                        hit_point = t[0]
                        break

                if not hit_point:
                    hit_point = target_pos
                self.hit_point = hit_point
                self.pre_link_sfx.end_pos = hit_point
            return

    def end_pre_sfx(self):
        self.reset_sfx_timer()

    def reset_sfx_timer(self):
        if self.pre_sfx_timer:
            global_data.game_mgr.unregister_logic_timer(self.pre_sfx_timer)
            self.pre_sfx_timer = None
        if self.pre_sfx_id:
            global_data.sfx_mgr.remove_sfx_by_id(self.pre_sfx_id)
            self.pre_sfx_id = None
        if self.pre_link_sfx_id:
            global_data.sfx_mgr.remove_sfx_by_id(self.pre_link_sfx_id)
            self.pre_link_sfx_id = None
            self.pre_link_sfx = None
        return

    def init_fire(self):
        model = self.ev_g_model()
        if not model or not model.valid:
            return
        if self.sub_state != self.S_ATK:
            return
        mat = model.get_socket_matrix(self.fire_socket, world.SPACE_TYPE_WORLD)
        start_pos = mat.translation
        if self.hit_point:
            target_pos = self.hit_point if 1 else get_aim_pos(self.target_id, self.target_pos)
            return self.check_fire_pos(start_pos) or None
        direction = target_pos - start_pos
        if direction.is_zero:
            direction = self.ev_g_forward()
        direction.normalize()
        self.open_fire(start_pos, direction)

    def open_fire(self, start_pos, dire):
        if not self or not self.is_valid():
            return
        throw_item = {'uniq_key': self.get_uniq_key(),
           'item_itype': self.wp_type,
           'item_kind': self.wp_kind,
           'position': (
                      start_pos.x, start_pos.y, start_pos.z),
           'dir': (
                 dire.x, dire.y, dire.z)
           }
        self.send_event('E_SHOOT_EXPLOSIVE_ITEM', throw_item, True)

    def enter(self, leave_states):
        super(MonsterSnipeBase, self).enter(leave_states)
        self.send_event('E_CALL_SYNC_METHOD', 'pve_enter_skill', (self.skill_id,), True)
        if self.sub_state == self.S_END:
            self.sub_state = self.S_AIM
            self.init_aim()

    def update(self, dt):
        super(MonsterSnipeBase, self).update(dt)
        if self.sub_state == self.S_END:
            self.disable_self()
        elif self.sub_state in (self.S_PRE, self.S_ATK) and self.trace_tag:
            self.send_event('E_CTRL_FACE_TO', get_aim_pos(self.target_id, self.target_pos), False)
        elif self.sub_state == self.S_AIM:
            self.update_aim_timer(dt)

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
        if not target_pos or not ori_pos:
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

    def exit(self, enter_states):
        super(MonsterSnipeBase, self).exit(enter_states)
        self.sub_state = self.S_END
        self.reset_aim_timer()
        self.do_exit(self.sid)
        self.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', [E_PVE_MONSTER_SNIPE_EXIT, (self.sid,)], True)
        self.send_event('E_CALL_SYNC_METHOD', 'pve_end_skill', (self.skill_id,), True)

    def do_exit(self, sid):
        if sid != self.sid:
            return
        self.reset_sfx_timer()

    def destroy(self):
        self.process_event(False)
        self.reset_aim_timer()
        self.reset_sfx_timer()
        self.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', [E_PVE_MONSTER_SNIPE_EXIT, ()], True)
        super(MonsterSnipeBase, self).destroy()

    def get_uniq_key(self):
        return ExploderID.gen(global_data.battle_idx)

    def update_col_ids(self):
        self._col_ids = self.ev_g_human_col_id()

    def check_fire_pos(self, fire_pos):
        start_pos = self.ev_g_position()
        if not start_pos:
            return False
        else:
            start_pos.y = fire_pos.y
            end_pos = fire_pos
            result = global_data.game_mgr.scene.scene_col.hit_by_ray(start_pos, end_pos, 0, S_GROUP_SCENE, S_GROUP_SCENE, collision.EQUAL_FILTER, True)
            if not result[0]:
                return True
            return False


class MonsterSnipe(MonsterSnipeBase):

    def init_params(self):
        super(MonsterSnipe, self).init_params()
        self.wp_list = self.custom_param.get('wp_list', (9010503, ))
        self.wp_pos = self.custom_param.get('wp_pos', 1)
        self.wp_type = self.wp_list[self.wp_pos - 1]
        self.wp_conf = confmgr.get('firearm_config', str(self.wp_type))
        self.wp_kind = self.wp_conf.get('iKind')
        self.skill_id = self.custom_param.get('skill_id', 9010555)
        self.max_aim_dur = self.custom_param.get('max_aim_dur', 3.0)
        self.aim_speed = self.custom_param.get('aim_speed', 3.14)
        self.aim_left_anim = self.custom_param.get('aim_left_anim', None)
        self.aim_left_anim_rate = self.custom_param.get('aim_left_anim_rate', 1.0)
        self.aim_right_anim = self.custom_param.get('aim_right_anim', None)
        self.aim_right_anim_rate = self.custom_param.get('aim_right_anim_rate', 1.0)
        self.pre_anim = self.custom_param.get('pre_anim', 'idle_01')
        self.pre_anim_dur = self.custom_param.get('pre_anim_dur', 2.0)
        self.pre_anim_rate = self.custom_param.get('pre_anim_rate', 1.0)
        self.atk_anim = self.custom_param.get('atk_anim', 'attack_05')
        self.atk_anim_dur = self.custom_param.get('atk_anim_dur', 1.0)
        self.atk_anim_rate = self.custom_param.get('atk_anim_rate', 1.0)
        self.bac_anim = self.custom_param.get('bac_anim', '')
        self.bac_anim_dur = self.custom_param.get('bac_anim_dur', 0)
        self.bac_anim_rate = self.custom_param.get('bac_anim_rate', 1.0)
        self.pre_sfx_socket = self.custom_param.get('pre_sfx_socket', 'part_point1')
        self.pre_sfx_res = self.custom_param.get('pre_sfx_res', '')
        self.pre_sfx_scale = self.custom_param.get('pre_sfx_scale', 1.0)
        self.pre_sfx_rate = self.custom_param.get('pre_sfx_rate', 1.0)
        self.pre_link_sfx_socket = self.custom_param.get('pre_link_sfx_socket', 'part_point1')
        self.pre_link_sfx_res = self.custom_param.get('pre_link_sfx_res', 'effect/fx/mecha/8008/8008_aux_aim.sfx')
        self.pre_link_sfx_scale = self.custom_param.get('pre_link_sfx_scale', 1.0)
        self.pre_link_sfx_rate = self.custom_param.get('pre_link_sfx_rate', 1.0)
        self.fire_socket = self.custom_param.get('fire_socket', 'part_point1')
        self.trace_dur = self.custom_param.get('trace_dur', 0)
        return

    def editor_handle(self):
        if global_data.use_sunshine:
            self.init_params()
            self.reset_sub_states_callback()
            self.register_snipe_callbacks()