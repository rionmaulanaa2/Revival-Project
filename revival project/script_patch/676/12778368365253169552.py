# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/behavior/PVEMonsterSuicideLogic.py
from __future__ import absolute_import
from .MonsterStateBase import MonsterStateBase
from logic.gcommon.common_const.character_anim_const import LOW_BODY
from logic.gcommon.cdata.pve_monster_status_config import MC_STAND

class MonsterSuicideBase(MonsterStateBase):
    BIND_EVENT = {'E_ACTIVE_PARAM_STATE': 'pre_check_param'
       }
    econf = {}
    S_END = -1
    S_PRE = 0
    S_ON = 1

    def pre_check_param(self, state, *args):
        if state != self.sid:
            return
        if self.is_active:
            return False
        if not self.check_can_active():
            return False
        self.editor_handle()
        self.skill_id, self.target_id = args
        self.active_self()

    def init_from_dict(self, unit_obj, bdict, sid, info):
        super(MonsterSuicideBase, self).init_from_dict(unit_obj, bdict, sid, info)
        self.init_params()
        self.process_event(True)
        self.sub_state = self.S_END

    def init_params(self):
        pass

    def editor_handle(self):
        pass

    def process_event(self, is_bind):
        emgr = global_data.emgr
        if is_bind:
            emgr.bind_events(self.econf)
        else:
            emgr.unbind_events(self.econf)

    def on_init_complete(self):
        super(MonsterSuicideBase, self).on_init_complete()
        self.register_suicide_callbacks()

    def register_suicide_callbacks(self):
        self.register_substate_callback(self.S_PRE, 0, self.start_pre)
        self.register_substate_callback(self.S_PRE, self.pre_anim_dur / self.pre_anim_rate, self.end_pre)

    def start_pre(self):
        self.send_event('E_ANIM_RATE', LOW_BODY, self.pre_anim_rate)
        self.send_event('E_POST_ACTION', self.pre_anim, LOW_BODY, 1)

    def end_pre(self):
        self.send_event('E_DO_SKILL', self.skill_id)
        self.send_event('E_ACTIVE_STATE', MC_STAND)
        self.sub_state = self.S_END

    def enter(self, leave_states):
        super(MonsterSuicideBase, self).enter(leave_states)
        self.send_event('E_CALL_SYNC_METHOD', 'pve_enter_skill', (self.skill_id,), True)
        if self.sub_state == self.S_END:
            self.sub_state = self.S_PRE

    def update(self, dt):
        super(MonsterSuicideBase, self).update(dt)
        if self.sub_state == self.S_END:
            self.disable_self()

    def exit(self, enter_states):
        super(MonsterSuicideBase, self).exit(enter_states)
        self.send_event('E_CALL_SYNC_METHOD', 'pve_end_skill', (self.skill_id,), True)

    def destroy(self):
        self.process_event(False)
        super(MonsterSuicideBase, self).destroy()


class MonsterSuicide(MonsterSuicideBase):

    def init_params(self):
        super(MonsterSuicide, self).init_params()
        self.skill_id = self.custom_param.get('skill_id')
        self.pre_anim = self.custom_param.get('pre_anim', 'skill_ready')
        self.pre_anim_rate = self.custom_param.get('pre_anim_rate', 1.0)
        self.pre_anim_dur = self.custom_param.get('pre_anim_dur', 1.833)

    def editor_handle(self):
        if global_data.use_sunshine:
            self.init_params()
            self.reset_sub_states_callback()
            self.register_suicide_callbacks()