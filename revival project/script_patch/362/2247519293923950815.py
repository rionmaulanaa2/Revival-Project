# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/behavior/PVEMonsterLinkHealLogic.py
from __future__ import absolute_import
from .MonsterStateBase import MonsterStateBase
from logic.gcommon.common_const.character_anim_const import LOW_BODY
from math import pi, cos, radians
import math3d
import world
import collision
from logic.gcommon.cdata.pve_monster_status_config import MC_MONSTER_AIMTURN
from mobile.common.EntityManager import EntityManager
from logic.gcommon.common_const.collision_const import GROUP_CAMERA_COLL
from logic.gcommon.common_utils.bcast_utils import E_PVE_MONSTER_LINK_HEAL_START_HEAL, E_PVE_MONSTER_LINK_HEAL_END_HEAL
PI2 = 2 * pi

class MonsterLinkHealBase(MonsterStateBase):
    BIND_EVENT = MonsterStateBase.BIND_EVENT.copy()
    BIND_EVENT.update({'E_ACTIVE_PARAM_STATE': 'pre_check_param',
       'E_PVE_MONSTER_LINK_HEAL_START_HEAL': 'do_start_heal',
       'E_PVE_MONSTER_LINK_HEAL_END_HEAL': 'do_end_heal'
       })
    econf = {}
    S_END = -1
    S_PRE = 0
    S_HEAL = 1
    S_BAC = 2

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
        super(MonsterLinkHealBase, self).init_from_dict(unit_obj, bdict, sid, info)
        self.heal_timer = None
        self.heal_sfx_id = None
        self.heal_sfx = None
        self.heal_ts = 0
        self.is_sync = False
        self.init_params()
        self.process_event(True)
        self.sub_state = self.S_END
        return

    def init_params(self):
        pass

    def editor_handle(self):
        pass

    def process_event(self, is_bind):
        emgr = global_data.emgr
        is_bind and emgr.bind_events(self.econf) if 1 else emgr.unbind_events(self.econf)

    def on_init_complete(self):
        super(MonsterLinkHealBase, self).on_init_complete()
        self.register_substate_callbacks()

    def register_substate_callbacks(self):
        self.register_substate_callback(self.S_PRE, 0, self.start_pre)
        self.register_substate_callback(self.S_PRE, self.pre_anim_dur / self.pre_anim_rate, self.end_pre)
        self.register_substate_callback(self.S_HEAL, 0, self.start_heal)
        self.register_substate_callback(self.S_BAC, 0, self.start_bac)
        self.register_substate_callback(self.S_BAC, self.bac_anim_dur / self.bac_anim_rate, self.end_bac)

    def start_pre(self):
        self.reset_heal_timer()
        self.send_event('E_ANIM_RATE', LOW_BODY, self.pre_anim_rate)
        if self.pre_anim:
            self.send_event('E_POST_ACTION', self.pre_anim, LOW_BODY, 1)

    def end_pre(self):
        self.sub_state = self.S_HEAL

    def start_heal(self):
        self.send_event('E_ANIM_RATE', LOW_BODY, self.heal_anim_rate)
        if self.heal_anim:
            self.send_event('E_POST_ACTION', self.heal_anim, LOW_BODY, 1, loop=True)
        self.do_start_heal()
        self.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', [E_PVE_MONSTER_LINK_HEAL_START_HEAL, (self.target_id, True)], True)

    def do_start_heal(self, target_id=None, is_sync=False):
        self.is_sync = is_sync
        if target_id is not None:
            self.target = EntityManager.getentity(target_id)
            self.target_yaw = None
        self.reset_heal_timer()
        self.heal_ts = 0
        self.heal_timer = global_data.game_mgr.register_logic_timer(self.tick_heal, 1, timedelta=True)
        return

    def start_bac(self):
        self.send_event('E_ANIM_RATE', LOW_BODY, self.bac_anim_rate)
        if self.bac_anim:
            self.send_event('E_POST_ACTION', self.bac_anim, LOW_BODY, 1)
        self.do_end_heal()
        self.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', [E_PVE_MONSTER_LINK_HEAL_END_HEAL, ()], True)

    def do_end_heal(self):
        self.reset_heal_timer()
        if self.heal_sfx_id:
            global_data.sfx_mgr.remove_sfx_by_id(self.heal_sfx_id)
            self.heal_sfx_id = None
            self.heal_sfx = None
        return

    def end_bac(self):
        self.sub_state = self.S_END

    def enter(self, leave_states):
        super(MonsterLinkHealBase, self).enter(leave_states)
        self.send_event('E_CALL_SYNC_METHOD', 'pve_enter_skill', (self.skill_id,), True)
        self.target = EntityManager.getentity(self.target_id)
        self.target_yaw = None
        if not self.check_target_valid():
            self.disable_self()
            return
        else:
            self.sub_state = self.S_PRE
            return

    def update(self, dt):
        super(MonsterLinkHealBase, self).update(dt)
        if self.sub_state == self.S_END:
            self.disable_self()
        elif self.sub_state == self.S_PRE:
            if not self.check_target_valid(dt):
                self.sub_state = self.S_END

    def exit(self, enter_states):
        super(MonsterLinkHealBase, self).exit(enter_states)
        self.sub_state = self.S_END
        self.do_end_heal()
        self.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', [E_PVE_MONSTER_LINK_HEAL_END_HEAL, ()], True)
        if self.aim_turn:
            self.send_event('E_PVE_M_AIM_TURN', self.sid, self.skill_id, self.target_id, math3d.vector(0, 0, 0))
            self.send_event('E_ACTIVE_STATE', MC_MONSTER_AIMTURN)
        else:
            self.send_event('E_CALL_SYNC_METHOD', 'pve_end_skill', (self.skill_id,), True)

    def destroy(self):
        self.do_end_heal()
        self.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', [E_PVE_MONSTER_LINK_HEAL_END_HEAL, ()], True)
        self.process_event(False)
        super(MonsterLinkHealBase, self).destroy()

    def check_target_valid(self, dt=0):
        if not self.target or not self.target.logic:
            return False
        else:
            target_model = self.target.logic.ev_g_model()
            mat = None
            if target_model and target_model.valid:
                mat = target_model.get_socket_matrix('fx_buff', world.SPACE_TYPE_WORLD)
            if mat:
                self.target_pos = mat.translation
            else:
                self.target_pos = self.target.logic.ev_g_position() + math3d.vector(0, 25, 0)
            my_model = self.ev_g_model()
            mat = None
            if my_model and my_model.valid and my_model.has_socket(self.cast_skill_socket):
                mat = my_model.get_socket_matrix(self.cast_skill_socket, world.SPACE_TYPE_WORLD)
            if mat:
                my_pos = mat.translation
            else:
                my_pos = self.ev_g_position() + math3d.vector(0, 25, 0)
            target_dir = self.target_pos - my_pos
            dist = target_dir.length
            if dist > self.max_heal_dist or dist < self.min_heal_dist:
                return False
            ret = world.get_active_scene().scene_col.hit_by_ray(my_pos, self.target_pos, 0, GROUP_CAMERA_COLL, GROUP_CAMERA_COLL, collision.INCLUDE_FILTER, True)
            if ret and ret[0]:
                return False
            if not self.is_sync and dist > 0:
                target_yaw = target_dir.yaw % PI2
                if self.target_yaw is None or abs(self.target_yaw - target_yaw) > self.need_turn_angle:
                    self.target_yaw = target_yaw
                if dt > 0:
                    cur_yaw = self.ev_g_yaw() % PI2
                    diff = self.target_yaw - cur_yaw
                    if diff != 0:
                        turn_dir = 1 if diff > 0 else -1
                        turn_val = min(self.turn_speed * dt, abs(diff)) * turn_dir
                        new_yaw = cur_yaw + turn_val
                        self.send_event('E_CAM_YAW', new_yaw)
                        self.send_event('E_ACTION_SYNC_YAW', new_yaw)
            return True

    def reset_heal_timer(self):
        if self.heal_timer:
            global_data.game_mgr.unregister_logic_timer(self.heal_timer)
            self.heal_timer = None
        return

    def tick_heal(self, dt):
        self.heal_ts += dt
        if self.heal_ts > self.max_heal_time or not self.check_target_valid(dt):
            if self.is_sync:
                self.do_end_heal()
            else:
                self.disable_self()
            return
        if not self.heal_sfx_id:

            def cb(sfx):
                if self.heal_sfx_scale:
                    sfx.scale = math3d.vector(self.heal_sfx_scale, self.heal_sfx_scale, self.heal_sfx_scale)
                if self.heal_sfx_rate:
                    sfx.frame_rate = self.heal_sfx_rate
                self.heal_sfx = sfx
                sfx.end_pos = self.target_pos

            self.heal_sfx_id = global_data.sfx_mgr.create_sfx_on_model(self.heal_sfx_res, self.ev_g_model(), self.cast_skill_socket, on_create_func=cb)
        elif self.heal_sfx:
            self.heal_sfx.end_pos = self.target_pos


class MonsterLinkHeal(MonsterLinkHealBase):

    def init_params(self):
        super(MonsterLinkHeal, self).init_params()
        self.skill_id = self.custom_param.get('skill_id', 9034951)
        self.max_heal_time = self.custom_param.get('max_heal_time', 1)
        self.max_heal_dist = self.custom_param.get('max_heal_dist', 1000)
        self.min_heal_dist = self.custom_param.get('min_heal_dist', 10)
        self.need_turn_angle = radians(self.custom_param.get('need_turn_angle', 30))
        self.turn_speed = radians(self.custom_param.get('turn_speed', 90))
        self.heal_sfx_res = self.custom_param.get('heal_sfx_res', '')
        self.heal_sfx_rate = self.custom_param.get('heal_sfx_rate', None)
        self.heal_sfx_scale = self.custom_param.get('heal_sfx_scale', None)
        self.cast_skill_socket = self.custom_param.get('cast_skill_socket', '')
        self.pre_anim = self.custom_param.get('pre_anim', '')
        self.pre_anim_dur = self.custom_param.get('pre_anim_dur', 0)
        self.pre_anim_rate = self.custom_param.get('pre_anim_rate', 1.0)
        self.heal_anim = self.custom_param.get('heal_anim', '')
        self.heal_anim_dur = self.custom_param.get('heal_anim_dur', 0)
        self.heal_anim_rate = self.custom_param.get('heal_anim_rate', 1.0)
        self.bac_anim = self.custom_param.get('bac_anim', '')
        self.bac_anim_dur = self.custom_param.get('bac_anim_dur', 0)
        self.bac_anim_rate = self.custom_param.get('bac_anim_rate', 1.0)
        self.aim_turn = self.custom_param.get('aim_turn', False)
        return

    def editor_handle(self):
        if not global_data.use_sunshine:
            return
        self.init_params()
        self.reset_sub_states_callback()
        self.register_substate_callbacks()