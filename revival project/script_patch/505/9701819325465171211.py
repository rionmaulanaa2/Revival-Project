# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/behavior/PVEMonsterRoarLogic.py
from __future__ import absolute_import
from .MonsterStateBase import MonsterStateBase
from logic.gcommon.common_const.character_anim_const import LOW_BODY
from logic.gcommon.cdata.pve_monster_status_config import MC_STAND
import math3d
from logic.gutils.pve_utils import get_aim_pos

class MonsterRoarBase(MonsterStateBase):
    BIND_EVENT = {'E_ACTIVE_PARAM_STATE': 'pre_check_param'
       }
    econf = {}
    ROAR_END = -1
    ROAR_ON = 0

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
        super(MonsterRoarBase, self).init_from_dict(unit_obj, bdict, sid, info)
        self.init_params()
        self.process_event(True)
        self.sub_state = self.ROAR_END

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
        super(MonsterRoarBase, self).on_init_complete()
        self.register_roar_callbacks()

    def register_roar_callbacks(self):
        self.register_substate_callback(self.ROAR_ON, 0, self.start_roar)
        self.register_substate_callback(self.ROAR_ON, self.anim_dur / self.anim_rate, self.end_roar)

    def start_roar(self):
        self.send_event('E_DO_SKILL', self.skill_id)
        self.send_event('E_CTRL_FACE_TO', get_aim_pos(self.target_id, self.target_pos), False)
        self.send_event('E_ANIM_RATE', LOW_BODY, self.anim_rate)
        self.send_event('E_POST_ACTION', self.anim_name, LOW_BODY, 1)

    def end_roar(self):
        self.send_event('E_ACTIVE_STATE', MC_STAND)
        self.sub_state = self.ROAR_END

    def enter(self, leave_states):
        super(MonsterRoarBase, self).enter(leave_states)
        self.send_event('E_CALL_SYNC_METHOD', 'pve_enter_skill', (self.skill_id,), True)
        if self.sub_state == self.ROAR_END:
            self.sub_state = self.ROAR_ON

    def update(self, dt):
        super(MonsterRoarBase, self).update(dt)
        if self.sub_state == self.ROAR_END:
            self.disable_self()

    def exit(self, enter_states):
        super(MonsterRoarBase, self).exit(enter_states)
        if self.sub_state == self.ROAR_ON:
            self.sub_state = self.ROAR_END
        self.send_event('E_CALL_SYNC_METHOD', 'pve_end_skill', (self.skill_id,), True)

    def destroy(self):
        self.process_event(False)
        super(MonsterRoarBase, self).destroy()


class MonsterRoar(MonsterRoarBase):

    def init_params(self):
        super(MonsterRoar, self).init_params()
        self.skill_id = self.custom_param.get('skill_id', 9010154)
        self.anim_name = self.custom_param.get('anim_name', 'attack_03')
        self.anim_rate = self.custom_param.get('anim_rate', 1.0)
        self.anim_dur = self.custom_param.get('anim_dur', 2.9)

    def editor_handle(self):
        if global_data.use_sunshine:
            self.init_params()
            self.reset_sub_states_callback()
            self.register_roar_callbacks()


class MonsterScoutBase(MonsterRoarBase):

    def pre_check_param(self, state, *args):
        if state != self.sid:
            return
        if self.is_active:
            return False
        if not self.check_can_active():
            return False
        self.editor_handle()
        self.skill_id, self.target_id, self.target_pos = args
        self.active_self()

    def start_roar(self):
        self.skill_id and self.send_event('E_DO_SKILL', self.skill_id)
        self.send_event('E_ANIM_RATE', LOW_BODY, self.anim_rate)
        self.send_event('E_POST_ACTION', self.anim_name, LOW_BODY, 1, loop=self.need_loop_anim)


class MonsterScout(MonsterScoutBase):

    def init_params(self):
        super(MonsterScout, self).init_params()
        self.skill_id = self.custom_param.get('skill_id', None)
        self.anim_name = self.custom_param.get('anim_name')
        self.anim_rate = self.custom_param.get('anim_rate', 1.0)
        self.anim_dur = self.custom_param.get('anim_dur')
        self.need_loop_anim = self.custom_param.get('need_loop_anim', False)
        return

    def editor_handle(self):
        if global_data.use_sunshine:
            self.init_params()
            self.reset_sub_states_callback()
            self.register_roar_callbacks()