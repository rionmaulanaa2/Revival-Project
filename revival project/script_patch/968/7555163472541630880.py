# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/behavior/PVEMonsterRaiseShieldLogic.py
from __future__ import absolute_import
from .MonsterStateBase import MonsterStateBase
import world
import math3d
import collision
from logic.gcommon.common_const.character_anim_const import UP_BODY, LOW_BODY
from logic.gcommon.common_utils.bcast_utils import E_PVE_MONSTER_RAISE_SHIELD_START, E_PVE_MONSTER_RAISE_SHIELD_END
from logic.gcommon.cdata.pve_monster_status_config import MC_MONSTER_AIMTURN, MC_RUN
from logic.gcommon.common_const.collision_const import GROUP_GRENADE, GROUP_SHOOTUNIT, GROUP_MECHA_BALL
from logic.gcommon.const import NEOX_UNIT_SCALE

class MonsterRaiseShieldBase(MonsterStateBase):
    BIND_EVENT = MonsterStateBase.BIND_EVENT.copy()
    BIND_EVENT.update({'E_ACTIVE_PARAM_STATE': 'pre_check_param',
       'E_PVE_MONSTER_RAISE_SHIELD_START': 'do_start_shield',
       'E_PVE_MONSTER_RAISE_SHIELD_END': 'do_end_shield',
       'E_MODEL_LOADED': 'on_model_loaded'
       })
    econf = {}
    S_END = -1
    S_PRE = 0
    S_SHIELD = 1
    S_BAC = 2
    SFX_ORI_SIZE = [
     19, 30, 4]

    def pre_check_param(self, state, *args):
        if state != self.sid:
            return
        else:
            if len(args) == 3:
                self.skill_id, self.target_id, self.target_pos = args
                do_skill = True
            else:
                self.skill_id, self.target_id, self.target_pos, do_skill = args
            self.target_pos = math3d.vector(*self.target_pos) if self.target_pos else None
            if do_skill:
                self.editor_handle()
                self.active_self()
            elif self.is_active:
                self.end_shield()
            return

    def init_from_dict(self, unit_obj, bdict, sid, info):
        super(MonsterRaiseShieldBase, self).init_from_dict(unit_obj, bdict, sid, info)
        self.model = None
        self.shield_collision = None
        self.shield_sfx_id = None
        self.init_params()
        self.process_event(True)
        self.sub_state = self.S_END
        return

    def init_params(self):
        pass

    def process_event(self, is_bind):
        emgr = global_data.emgr
        is_bind and emgr.bind_events(self.econf) if 1 else emgr.unbind_events(self.econf)

    def on_init_complete(self):
        super(MonsterRaiseShieldBase, self).on_init_complete()
        self.register_substate_callbacks()
        self.init_shield_col()

    def register_substate_callbacks(self):
        self.register_substate_callback(self.S_PRE, 0, self.start_pre)
        self.register_substate_callback(self.S_PRE, self.pre_anim_dur / self.pre_anim_rate, self.end_pre)
        self.register_substate_callback(self.S_SHIELD, 0, self.start_shield)
        self.register_substate_callback(self.S_SHIELD, self.max_shield_time, self.end_shield)
        self.register_substate_callback(self.S_BAC, 0, self.start_bac)
        self.register_substate_callback(self.S_BAC, self.bac_anim_dur / self.bac_anim_rate, self.end_bac)

    def on_model_loaded(self, model):
        self.model = model

    def init_shield_col(self):
        collision_size = [
         self.shield_col_size[2] * NEOX_UNIT_SCALE,
         self.shield_col_size[1] * NEOX_UNIT_SCALE,
         self.shield_col_size[0] * NEOX_UNIT_SCALE]
        self.shield_collision = collision.col_object(collision.BOX, math3d.vector(*collision_size), 0, 0, False)
        self.shield_collision.mask = GROUP_SHOOTUNIT | GROUP_GRENADE & ~GROUP_MECHA_BALL
        self.shield_collision.group = GROUP_SHOOTUNIT
        self.shield_collision.is_force_callback = True
        self.shield_collision.car_undrivable = True
        if self.sub_state == self.S_SHIELD:
            self.create_shield()

    def start_pre(self):
        self.send_event('E_ANIM_RATE', UP_BODY, self.pre_anim_rate)
        if self.pre_anim:
            self.send_event('E_POST_ACTION', self.pre_anim, UP_BODY, 7)

    def end_pre(self):
        self.sub_state = self.S_SHIELD

    def start_shield(self):
        self.do_start_shield()
        self.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', [E_PVE_MONSTER_RAISE_SHIELD_START, (True,)], True)

    def do_start_shield(self, is_sync=False):
        self.is_sync = is_sync
        self.create_shield()

    def end_shield(self):
        self.send_event('E_REPLACE_RUN_ANIM', None)
        self.sub_state = self.S_BAC
        self.do_end_shield()
        self.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', [E_PVE_MONSTER_RAISE_SHIELD_END, ()], True)
        return

    def do_end_shield(self):
        self.clear_shield()

    def start_bac(self):
        self.send_event('E_ANIM_RATE', UP_BODY, self.bac_anim_rate)
        if self.bac_anim:
            self.send_event('E_POST_ACTION', self.bac_anim, UP_BODY, 7)

    def end_bac(self):
        self.sub_state = self.S_END
        self.disable_self()

    def enter(self, leave_states):
        super(MonsterRaiseShieldBase, self).enter(leave_states)
        self.send_event('E_CALL_SYNC_METHOD', 'pve_enter_skill', (self.skill_id,), True)
        self.sub_state = self.S_PRE

    def update(self, dt):
        super(MonsterRaiseShieldBase, self).update(dt)
        if self.model and self.model.valid:
            m = self.model.get_socket_matrix(self.shield_sfx_socket, 1)
            self.shield_collision.position = m.translation + m.forward * self.shield_col_offset[0] + m.up * self.shield_col_offset[1]
            self.shield_collision.rotation_matrix = m.rotation

    def exit(self, enter_states):
        super(MonsterRaiseShieldBase, self).exit(enter_states)
        self.sub_state = self.S_END
        self.send_event('E_CLEAR_UP_BODY_ANIM')
        self.do_end_shield()
        self.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', [E_PVE_MONSTER_RAISE_SHIELD_END, ()], True)
        if self.aim_turn:
            self.send_event('E_PVE_M_AIM_TURN', self.sid, self.skill_id, self.target_id, math3d.vector(0, 0, 0))
            self.send_event('E_ACTIVE_STATE', MC_MONSTER_AIMTURN)
        else:
            self.send_event('E_CALL_SYNC_METHOD', 'pve_end_skill', (self.skill_id,), True)

    def create_shield(self):
        model = self.ev_g_model()
        if not model or not model.valid:
            return
        else:
            need_create_sfx = True
            if self.shield_sfx_id:
                sfx = global_data.sfx_mgr.get_sfx_by_id(self.shield_sfx_id)
                if not sfx or not sfx.valid:
                    global_data.sfx_mgr.remove_sfx_by_id(self.shield_sfx_id)
                    self.shield_sfx_id = None
                    need_create_sfx = True
                else:
                    need_create_sfx = False
            if need_create_sfx:

                def on_create(sfx):
                    sfx_scale = [self.shield_col_size[1] * NEOX_UNIT_SCALE / self.SFX_ORI_SIZE[0],
                     self.shield_col_size[2] * NEOX_UNIT_SCALE / self.SFX_ORI_SIZE[1],
                     self.shield_col_size[0] * NEOX_UNIT_SCALE / self.SFX_ORI_SIZE[2]]
                    sfx.scale = math3d.vector(*sfx_scale)

                def on_remove(*args):
                    pass

                self.shield_sfx_id = global_data.sfx_mgr.create_sfx_on_model(self.shield_sfx_res, model, self.shield_sfx_socket, on_create_func=on_create, on_remove_func=on_remove)
            if self.shield_collision:
                world.get_active_scene().scene_col.add_object(self.shield_collision)
                global_data.emgr.scene_add_common_shoot_obj.emit(self.shield_collision.cid, self.unit_obj)
                self.send_event('E_ADD_HANDY_SHIELD_COL', self.shield_collision)
            return

    def clear_shield(self):
        if self.shield_sfx_id:
            global_data.sfx_mgr.remove_sfx_by_id(self.shield_sfx_id)
        self.shield_sfx_id = None
        if self.shield_collision:
            world.get_active_scene().scene_col.remove_object(self.shield_collision)
            global_data.emgr.scene_remove_common_shoot_obj.emit(self.shield_collision.cid)
            self.send_event('E_REMOVE_HANDY_SHIELD_COL')
        return


class MonsterRaiseShield(MonsterRaiseShieldBase):

    def init_params(self):
        super(MonsterRaiseShield, self).init_params()
        self.skill_id = self.custom_param.get('skill_id', 9034951)
        self.max_shield_time = self.custom_param.get('max_shield_time', 1)
        self.pre_anim = self.custom_param.get('pre_anim', '')
        self.pre_anim_dur = self.custom_param.get('pre_anim_dur', 0)
        self.pre_anim_rate = self.custom_param.get('pre_anim_rate', 1.0)
        self.shield_anim = self.custom_param.get('shield_anim', '')
        self.bac_anim = self.custom_param.get('bac_anim', '')
        self.bac_anim_dur = self.custom_param.get('bac_anim_dur', 0)
        self.bac_anim_rate = self.custom_param.get('bac_anim_rate', 1.0)
        self.aim_turn = self.custom_param.get('aim_turn', False)
        self.shield_sfx_res = self.custom_param.get('shield_sfx_res', '')
        self.shield_sfx_socket = self.custom_param.get('shield_sfx_socket', '')
        self.shield_col_size = self.custom_param.get('shield_col_size', (1.0, 1.0,
                                                                         1.0))
        self.shield_col_offset = self.custom_param.get('shield_col_offset', (0, 0))

    def editor_handle(self):
        if not global_data.use_sunshine:
            return
        self.init_params()
        self.reset_sub_states_callback()
        self.register_substate_callbacks()
        self.init_shield_col()