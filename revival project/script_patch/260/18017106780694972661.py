# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/behavior/PVEMonsterObliqueLogic.py
from __future__ import absolute_import
from .MonsterStateBase import MonsterStateBase
import math3d
from logic.gcommon.common_const.character_anim_const import LOW_BODY
from logic.gcommon.const import NEOX_UNIT_SCALE
from logic.gutils.pve_utils import get_aim_pos
from logic.gcommon.cdata.pve_monster_status_config import MC_MONSTER_AIMTURN

class MonsterObliqueBase(MonsterStateBase):
    BIND_EVENT = {'E_ACTIVE_PARAM_STATE': 'pre_check_param'
       }
    econf = {}
    S_END = -1
    S_PRE = 1
    S_IDL = 2
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
        super(MonsterObliqueBase, self).init_from_dict(unit_obj, bdict, sid, info)
        self.init_params()
        self.process_event(True)
        self.sub_state = self.S_END

    def init_params(self):
        self.target_id = None
        self.target_pos = None
        self.focus_pos = None
        self.focus_tag = False
        self.dash_dire = None
        self.end_aoe_skill_id = 0
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
        super(MonsterObliqueBase, self).on_init_complete()
        self.register_oblique_callbacks()

    def register_oblique_callbacks(self):
        self.register_substate_callback(self.S_PRE, 0, self.start_pre)
        self.register_substate_callback(self.S_PRE, self.pre_anim_dur / self.pre_anim_rate, self.end_pre)
        self.register_substate_callback(self.S_IDL, 0, self.start_idl)
        self.register_substate_callback(self.S_IDL, self.idl_anim_dur / self.idl_anim_rate, self.end_idl)
        self.register_substate_callback(self.S_ATK, 0, self.start_atk)
        self.register_substate_callback(self.S_ATK, self.atk_anim_dur / self.atk_anim_rate, self.end_atk)
        self.register_substate_callback(self.S_BAC, 0, self.start_bac)
        self.register_substate_callback(self.S_BAC, self.bac_anim_dur / self.bac_anim_rate, self.end_bac)

    def start_pre(self):
        self.start_focus()
        self.delay_call(self.focus_time, self.end_focus)
        if not self.pre_anim_dur:
            return
        self.send_event('E_ANIM_RATE', LOW_BODY, self.pre_anim_rate)
        if self.pre_anim:
            self.send_event('E_POST_ACTION', self.pre_anim, LOW_BODY, 1)

    def end_pre(self):
        self.sub_state = self.S_IDL

    def start_idl(self):
        if not self.idl_anim_dur:
            return
        self.send_event('E_ANIM_RATE', LOW_BODY, self.idl_anim_rate)
        if self.idl_anim:
            self.send_event('E_POST_ACTION', self.idl_anim, LOW_BODY, 1, loop=True)

    def end_idl(self):
        self.sub_state = self.S_ATK

    def start_atk(self):
        if self.focus_tag:
            self.end_focus()
        self.init_dash()
        if not self.atk_anim_dur:
            return
        self.send_event('E_ANIM_RATE', LOW_BODY, self.atk_anim_rate)
        if self.atk_anim:
            self.send_event('E_POST_ACTION', self.atk_anim, LOW_BODY, 1)

    def end_atk(self):
        self.sub_state = self.S_BAC
        self.send_event('E_CLEAR_SPEED')
        if self.end_aoe_skill_id:
            self.send_event('E_DO_SKILL', self.end_aoe_skill_id)

    def start_bac(self):
        if not self.bac_anim_dur:
            return
        self.send_event('E_ANIM_RATE', LOW_BODY, self.bac_anim_rate)
        if self.bac_anim:
            self.send_event('E_POST_ACTION', self.bac_anim, LOW_BODY, 1)

    def end_bac(self):
        self.sub_state = self.S_END

    def init_dash(self):
        cur_pos = self.ev_g_position()
        dash_dire = self.focus_pos - cur_pos
        dash_dire.y = 0
        dash_dis = dash_dire.length
        if dash_dis > self.max_dash_dis:
            dash_dis = self.max_dash_dis
        dash_time = self.atk_anim_dur / self.atk_anim_rate
        dash_speed = dash_dis / dash_time
        dash_dire.normalize()
        self.dash_dire = dash_dire * dash_speed
        self.send_event('E_SET_WALK_DIRECTION', self.dash_dire)

    def enter(self, *args):
        super(MonsterObliqueBase, self).enter(*args)
        self.send_event('E_CALL_SYNC_METHOD', 'pve_enter_skill', (self.skill_id,), True)
        self.send_event('E_DO_SKILL', self.skill_id)
        self.sub_state = self.S_PRE

    def update(self, dt):
        super(MonsterObliqueBase, self).update(dt)
        if self.sub_state == self.S_END:
            self.disable_self()
        elif self.focus_tag and self.sub_state in (self.S_PRE, self.S_IDL):
            self.send_event('E_CTRL_FACE_TO', get_aim_pos(self.target_id, self.target_pos), False)

    def exit(self, *args):
        super(MonsterObliqueBase, self).exit(*args)
        self.sub_state = self.S_END
        if self.aim_turn:
            self.send_event('E_PVE_M_AIM_TURN', self.sid, self.skill_id, self.target_id, self.target_pos)
            self.send_event('E_ACTIVE_STATE', MC_MONSTER_AIMTURN)
        else:
            self.send_event('E_CALL_SYNC_METHOD', 'pve_end_skill', (self.skill_id,), True)

    def destroy(self):
        self.process_event(False)
        super(MonsterObliqueBase, self).destroy()

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


class MonsterOblique(MonsterObliqueBase):

    def init_params(self):
        super(MonsterOblique, self).init_params()
        self.skill_id = self.custom_param.get('skill_id', None)
        self.focus_time = self.custom_param.get('focus_time', 0)
        self.focus_dis = self.custom_param.get('focus_dis', 0) * NEOX_UNIT_SCALE
        self.max_dash_dis = self.custom_param.get('max_dash_dis', 1000) * NEOX_UNIT_SCALE
        self.pre_anim = self.custom_param.get('pre_anim', '')
        self.pre_anim_dur = self.custom_param.get('pre_anim_dur', 0)
        self.pre_anim_rate = self.custom_param.get('pre_anim_rate', 1.0)
        self.idl_anim = self.custom_param.get('idl_anim', '')
        self.idl_anim_dur = self.custom_param.get('idl_anim_dur', 0)
        self.idl_anim_rate = self.custom_param.get('idl_anim_rate', 1.0)
        self.atk_anim = self.custom_param.get('atk_anim', '')
        self.atk_anim_dur = self.custom_param.get('atk_anim_dur', 0)
        self.atk_anim_rate = self.custom_param.get('atk_anim_rate', 1.0)
        self.bac_anim = self.custom_param.get('bac_anim', '')
        self.bac_anim_dur = self.custom_param.get('bac_anim_dur', 0)
        self.bac_anim_rate = self.custom_param.get('bac_anim_rate', 1.0)
        self.end_aoe_skill_id = self.custom_param.get('end_aoe_skill_id', None)
        self.aim_turn = self.custom_param.get('aim_turn', True)
        return

    def editor_handle(self):
        if global_data.use_sunshine:
            self.init_params()
            self.reset_sub_states_callback()
            self.register_oblique_callbacks()