# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/behavior/PVEMonsterStunLogic.py
from __future__ import absolute_import
from .MonsterStateBase import MonsterStateBase
from logic.gcommon.common_const.character_anim_const import LOW_BODY

class MonsterStunBase(MonsterStateBase):
    BIND_EVENT = {'E_ACTIVE_PARAM_STATE': 'pre_check_param'
       }
    econf = {}
    S_END = 0
    S_PRE = 1
    S_STUN = 2
    S_BAC = 3

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
            self.end_stun()

    def init_from_dict(self, unit_obj, bdict, sid, info):
        super(MonsterStunBase, self).init_from_dict(unit_obj, bdict, sid, info)
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
        super(MonsterStunBase, self).on_init_complete()
        self.register_stun_callbacks()

    def register_stun_callbacks(self):
        self.register_substate_callback(self.S_PRE, 0, self.start_pre)
        self.register_substate_callback(self.S_PRE, self.pre_anim_dur / self.pre_anim_rate, self.end_pre)
        self.register_substate_callback(self.S_STUN, 0, self.start_stun)
        self.register_substate_callback(self.S_BAC, 0, self.start_bac)
        self.register_substate_callback(self.S_BAC, self.bac_anim_dur / self.bac_anim_rate, self.end_bac)

    def start_pre(self):
        self.send_event('E_ANIM_RATE', LOW_BODY, self.pre_anim_rate)
        self.send_event('E_POST_ACTION', self.pre_anim, LOW_BODY, 1)

    def end_pre(self):
        self.sub_state = self.S_STUN

    def start_stun(self):
        self.send_event('E_ANIM_RATE', LOW_BODY, self.stun_anim_rate)
        self.send_event('E_POST_ACTION', self.stun_anim, LOW_BODY, 1)

    def end_stun(self):
        self.sub_state = self.S_BAC

    def start_bac(self):
        self.send_event('E_ANIM_RATE', LOW_BODY, self.bac_anim_rate)
        self.send_event('E_POST_ACTION', self.bac_anim, LOW_BODY, 1)

    def end_bac(self):
        self.sub_state = self.S_END

    def enter(self, leave_states):
        super(MonsterStunBase, self).enter(leave_states)
        self.send_event('E_CLEAR_SPEED')
        self.sub_state = self.S_PRE

    def update(self, dt):
        super(MonsterStunBase, self).update(dt)
        if self.sub_state == self.S_END:
            self.disable_self()

    def exit(self, enter_states):
        super(MonsterStunBase, self).exit(enter_states)
        self.send_event('E_CALL_SYNC_METHOD', 'pve_end_stun', (), True)

    def destroy(self):
        self.process_event(False)
        super(MonsterStunBase, self).destroy()


class MonsterStun(MonsterStunBase):

    def init_params(self):
        super(MonsterStun, self).init_params()
        self.pre_anim = self.custom_param.get('pre_anim', 'hit')
        self.pre_anim_dur = self.custom_param.get('pre_anim_dur', 0.7)
        self.pre_anim_rate = self.custom_param.get('pre_anim_rate', 1.0)
        self.stun_anim = self.custom_param.get('stun_anim', 'die')
        self.stun_anim_rate = self.custom_param.get('stun_anim_rate', 1.0)
        self.bac_anim = self.custom_param.get('bac_anim', 'hit')
        self.bac_anim_dur = self.custom_param.get('bac_anim_dur', 0.7)
        self.bac_anim_rate = self.custom_param.get('bac_anim_rate', 1.0)

    def editor_handle(self):
        if global_data.use_sunshine:
            self.init_params()
            self.reset_sub_states_callback()
            self.register_stun_callbacks()