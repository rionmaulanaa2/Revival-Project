# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/behavior/PVEBossSecondStageLogic.py
from __future__ import absolute_import
from .MonsterStateBase import MonsterStateBase
from logic.gcommon.common_const.character_anim_const import LOW_BODY
import math3d
from logic.gutils.pve_utils import get_aim_pos
import game3d
from logic.gcommon.common_const.pve_const import TIP_TYPE_WARN
from logic.gcommon.common_utils.bcast_utils import E_PVE_BOSS_ENTER_INVINCIBLE, E_PVE_BOSS_EXIT_INVINCIBLE, E_PVE_BOSS_ENTER_SEC_STAGE
_HASH_DIFFUSE = game3d.calc_string_hash('Tex0')
_HASH_COLOR = game3d.calc_string_hash('emissive_color')
_HASH_COLOR_D = game3d.calc_string_hash('emissive_intensity')

class BossInvincibleBase(MonsterStateBase):
    BIND_EVENT = {'E_ACTIVE_PARAM_STATE': 'pre_check_param',
       'E_PVE_BOSS_ENTER_INVINCIBLE': 'start_invincible',
       'E_PVE_BOSS_EXIT_INVINCIBLE': 'end_invincible'
       }
    econf = {}
    SFX_PATH = 'effect/fx/monster/boss/boss_shader.sfx'
    SOCKET = 'fx_root'
    TEX_PATH = {90161: 'model_new/monster/pve_014/8008/textures/8008_mecha_2_d.tga',
       90261: 'model_new/monster/pve_219/8006_skin_s02a/textures/8006_skin_s02a_2_d.tga'
       }
    COLOR_D = {90161: 0.34,
       90261: 0.97
       }
    COLOR = {90161: (1.0, 0.08, 0.0, 1.0),
       90261: (0.066, 0.04, 1.0, 1.0)
       }

    def pre_check_param(self, state, *args):
        if state != self.sid:
            return
        if not self.check_can_active():
            return False
        self.editor_handle()
        switch = args[0]
        if switch:
            self.active_self()
        else:
            self.disable_self()

    def init_from_dict(self, unit_obj, bdict, sid, info):
        super(BossInvincibleBase, self).init_from_dict(unit_obj, bdict, sid, info)
        self.init_params()
        self.process_event(True)

    def init_params(self):
        self.sfx_id = None
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
        super(BossInvincibleBase, self).on_init_complete()

    def enter(self, leave_states):
        super(BossInvincibleBase, self).enter(leave_states)
        self.start_invincible(self.sid)
        self.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', [E_PVE_BOSS_ENTER_INVINCIBLE, (self.sid,)], True)

    def update(self, dt):
        super(BossInvincibleBase, self).update(dt)

    def exit(self, enter_states):
        super(BossInvincibleBase, self).exit(enter_states)
        self.end_invincible(self.sid)
        self.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', [E_PVE_BOSS_EXIT_INVINCIBLE, (self.sid,)], True)

    def start_invincible(self, sid):
        if sid != self.sid:
            return
        global_data.emgr.pve_boss_switch_invincible.emit(True)
        if self.sfx_id:
            global_data.sfx_mgr.remove_sfx_by_id(self.sfx_id)
        model = self.ev_g_model()
        if model and model.valid:
            self.sfx_id = global_data.sfx_mgr.create_sfx_on_model(self.SFX_PATH, model, self.SOCKET)

    def end_invincible(self, sid):
        if sid != self.sid:
            return
        else:
            global_data.emgr.pve_boss_switch_invincible.emit(False)
            model = self.ev_g_model()
            if model and model.valid:
                monster_id = self.sd.ref_monster_id
                tex_path = self.TEX_PATH.get(monster_id, None)
                tex_path and model.all_materials.set_texture(_HASH_DIFFUSE, 'Tex0', tex_path)
                color_d = self.COLOR_D.get(monster_id, None)
                color_d and model.all_materials.set_var(_HASH_COLOR_D, 'emissive_intensity', color_d)
                color = self.COLOR.get(monster_id, None)
                color and model.all_materials.set_var(_HASH_COLOR, 'emissive_color', color)
            if self.sfx_id:
                global_data.sfx_mgr.remove_sfx_by_id(self.sfx_id)
                self.sfx_id = None
            return

    def destroy(self):
        self.process_event(False)
        super(BossInvincibleBase, self).destroy()


class BossInvincible(BossInvincibleBase):

    def init_params(self):
        super(BossInvincible, self).init_params()

    def editor_handle(self):
        if global_data.use_sunshine:
            self.init_params()


class BossSecondStageBase(MonsterStateBase):
    BIND_EVENT = {'E_ACTIVE_PARAM_STATE': 'pre_check_param',
       'E_PVE_BOSS_ENTER_SEC_STAGE': 'enter_sec_stage'
       }
    econf = {}
    S_END = -1
    S_PRE = 1
    S_ATK = 2
    S_BAC = 3

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
        super(BossSecondStageBase, self).init_from_dict(unit_obj, bdict, sid, info)
        self.init_params()
        self.process_event(True)
        self.sub_state = self.S_END

    def init_params(self):
        self.target_id = None
        self.target_pos = None
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
        super(BossSecondStageBase, self).on_init_complete()
        self.register_state_callbacks()

    def register_state_callbacks(self):
        self.register_substate_callback(self.S_PRE, 0, self.start_pre)
        self.register_substate_callback(self.S_PRE, self.pre_anim_dur / self.pre_anim_rate, self.end_pre)
        self.register_substate_callback(self.S_ATK, 0, self.start_atk)
        self.register_substate_callback(self.S_ATK, self.atk_anim_dur / self.atk_anim_rate, self.end_atk)
        self.register_substate_callback(self.S_BAC, 0, self.start_bac)
        self.register_substate_callback(self.S_BAC, self.bac_anim_dur / self.bac_anim_rate, self.end_bac)

    def start_pre(self):
        if not self.pre_anim_dur:
            return
        self.send_event('E_ANIM_RATE', LOW_BODY, self.pre_anim_rate)
        self.send_event('E_POST_ACTION', self.pre_anim, LOW_BODY, 1)
        if not self.move_start_ts and not self.move_end_ts:
            self.send_event('E_CLEAR_SPEED')

    def end_pre(self):
        self.sub_state = self.S_ATK

    def start_atk(self):
        if not self.atk_anim_dur:
            return
        self.send_event('E_ANIM_RATE', LOW_BODY, self.atk_anim_rate)
        self.send_event('E_POST_ACTION', self.atk_anim, LOW_BODY, 1)

    def end_atk(self):
        self.sub_state = self.S_BAC

    def start_bac(self):
        if not self.bac_anim_dur:
            return
        self.send_event('E_ANIM_RATE', LOW_BODY, self.bac_anim_rate)
        self.send_event('E_POST_ACTION', self.bac_anim, LOW_BODY, 1)

    def end_bac(self):
        self.sub_state = self.S_END

    def enter(self, leave_states):
        super(BossSecondStageBase, self).enter(leave_states)
        self.send_event('E_CALL_SYNC_METHOD', 'pve_enter_skill', (self.skill_id,), True)
        self.sub_state = self.S_PRE
        if self.summon_skill_id:
            self.send_event('E_DO_SKILL', self.summon_skill_id)
        self.enter_sec_stage(self.sid)
        self.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', [E_PVE_BOSS_ENTER_SEC_STAGE, (self.sid,)], True)

    def enter_sec_stage(self, sid):
        if sid != self.sid:
            return
        else:
            if self.move_start_ts or self.move_end_ts:
                self.init_move()
            global_data.emgr.pve_boss_enter_sec_stage.emit(TIP_TYPE_WARN, 1100017, None)
            return

    def update(self, dt):
        super(BossSecondStageBase, self).update(dt)
        if self.sub_state == self.S_END:
            self.disable_self()

    def exit(self, enter_states):
        super(BossSecondStageBase, self).exit(enter_states)
        self.send_event('E_CALL_SYNC_METHOD', 'pve_end_skill', (self.skill_id,), True)
        if self.move_start_ts or self.move_end_ts:
            self.end_move()

    def destroy(self):
        self.process_event(False)
        super(BossSecondStageBase, self).destroy()

    def init_move(self):
        self.delay_call(self.move_start_ts, self.start_move)

    def start_move(self):
        forward = self.ev_g_forward()
        forward.normalize()
        self.send_event('E_SET_WALK_DIRECTION', forward * self.move_speed * self.move_direction)
        self.delay_call(self.move_end_ts - self.move_start_ts, self.end_move)

    def end_move(self):
        self.send_event('E_CLEAR_SPEED')


class BossSecondStage(BossSecondStageBase):

    def init_params(self):
        super(BossSecondStage, self).init_params()
        self.pre_anim = self.custom_param.get('pre_anim', None)
        self.pre_anim_rate = self.custom_param.get('pre_anim_rate', 1.0)
        self.pre_anim_dur = self.custom_param.get('pre_anim_dur', 0)
        self.atk_anim = self.custom_param.get('atk_anim', None)
        self.atk_anim_rate = self.custom_param.get('atk_anim_rate', 1.0)
        self.atk_anim_dur = self.custom_param.get('atk_anim_dur', 0)
        self.bac_anim = self.custom_param.get('bac_anim', None)
        self.bac_anim_rate = self.custom_param.get('bac_anim_rate', 1.0)
        self.bac_anim_dur = self.custom_param.get('bac_anim_dur', 0)
        self.summon_skill_id = self.custom_param.get('summon_skill_id', 0)
        self.move_start_ts = self.custom_param.get('move_start_ts', None)
        self.move_end_ts = self.custom_param.get('move_end_ts', None)
        self.move_speed = self.custom_param.get('move_speed', None)
        self.move_direction = self.custom_param.get('move_direction', None)
        return

    def editor_handle(self):
        if global_data.use_sunshine:
            self.init_params()
            self.reset_sub_states_callback()
            self.register_state_callbacks()