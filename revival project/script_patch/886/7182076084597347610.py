# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/behavior/PetLogic.py
import world
import math3d
from logic.gcommon import editor
from .StateBase import StateBase
from common.cfg import confmgr
import logic.gcommon.common_utils.bcast_utils as bcast
from logic.gcommon.cdata.pet_status_config import PT_IDLE, PT_MOVE, PT_HIDE, PT_SHOW

class PetShow(StateBase):

    def enter(self, leave_states):
        super(PetShow, self).enter(leave_states)
        self.send_event('E_SHOW_MODEL')


class PetHide(StateBase):
    BIND_EVENT = {}

    def enter(self, leave_states):
        super(PetHide, self).enter(leave_states)
        self.send_event('E_HIDE_MODEL')


@editor.state_exporter({('spec_inter', 'param'): {'zh_name': '\xe8\xa1\xa8\xe6\x83\x85\xe5\x8a\xa8\xe4\xbd\x9c\xe6\x92\xad\xe6\x94\xbe\xe9\x97\xb4\xe9\x9a\x94(\xe7\xa7\x92)'}})
class PetIdle(StateBase):
    BIND_EVENT = {'E_PLAY_INTERACT_ANIM': 'play_interact_anim',
       'E_MODEL_LOADED': ('on_model_loaded', 99),
       'E_ANIM_CHANGED': 'on_anim_changed',
       'E_BUFF_FROM_ME_TO_TARGET': 'on_do_skill'
       }
    STATE_IDLE = 0
    STATE_SPEC = 1
    STATE_INTERACT = 2
    IDLE_ANIM_KEY = 'idle_anim'
    IDLE_ANIM2_KEY = 'idle_anim2'
    SKILL_ANIM_KEY = 'skill_anim'

    def init_from_dict(self, unit_obj, bdict, sid, state_info):
        super(PetIdle, self).init_from_dict(unit_obj, bdict, sid, state_info)
        skin_id = bdict['pet_id']
        self.spec_inter = confmgr.get('c_pet_info', str(skin_id), 'idle_anim2_inter', default=5.0)
        self.spec_anim_timer = 0.0
        self.on_enter = None
        return

    def on_model_loaded(self, model):
        self._register_callbacks()

    def _register_callbacks(self):
        self.reset_sub_states_callback()
        self.register_substate_callback(self.STATE_IDLE, 0.0, self.start_idle)
        self.register_substate_callback(self.STATE_IDLE, self.spec_inter, lambda *args: setattr(self, 'sub_state', self.STATE_SPEC))
        self.register_substate_callback(self.STATE_SPEC, 0.0, self.start_spec)
        self.register_substate_callback(self.STATE_SPEC, self.ev_g_anim_len_by_key(self.IDLE_ANIM2_KEY), lambda *args: setattr(self, 'sub_state', self.STATE_IDLE))

    def on_anim_changed(self, *args):
        self._register_callbacks()
        self.reset_sub_state_timer()

    def start_idle(self, *args):
        self.ev_g_play_anim(self.IDLE_ANIM_KEY)

    def start_spec(self, *args):
        self.ev_g_play_anim(self.IDLE_ANIM2_KEY)

    def play_interact_anim(self, idx):
        anim_key = 'interact_anim{}'.format(idx)
        anim_len = self.ev_g_anim_len_by_key(anim_key)
        if not anim_len:
            return
        self.ev_g_play_anim(anim_key)
        self.sub_state = self.STATE_INTERACT
        self.reset_sub_state_timer()
        self.delay_call(anim_len, lambda *args: setattr(self, 'sub_state', self.STATE_IDLE))

    def on_do_skill(self, *args):
        if not self.is_active:
            self.on_enter = self.on_do_skill
            self.send_event('E_ACTIVE_STATE', self.sid)
            return
        anim_len = self.ev_g_play_anim(self.SKILL_ANIM_KEY, ret_len=True)
        if not anim_len:
            return
        self.sub_state = self.STATE_INTERACT
        self.reset_sub_state_timer()
        self.send_event('E_ADD_BLACK_STATE', {PT_MOVE})
        self.delay_call(anim_len, self.on_skill_end)

    def on_skill_end(self):
        self.send_event('E_CLEAR_BLACK_STATE')
        self.sub_state = self.STATE_IDLE

    def enter(self, leave_states):
        super(PetIdle, self).enter(leave_states)
        if callable(self.on_enter):
            self.on_enter()
        else:
            self.sub_state = self.STATE_IDLE
        self.on_enter = None
        return


class PetMove(StateBase):
    BIND_EVENT = {'E_ANIM_CHANGED': 'on_anim_changed'
       }
    PRE_MOVE_ANIM_KEY = 'pre_move_anim'
    MOVE_ANIM_KEY = 'move_anim'

    def init_from_dict(self, unit_obj, bdict, sid, state_info):
        super(PetMove, self).init_from_dict(unit_obj, bdict, sid, state_info)

    def enter(self, leave_states):
        super(PetMove, self).enter(leave_states)
        if getattr(self, 'has_pre_move_anim', True) and self.ev_g_pet_anim_dir()[0] < -0.7:
            anim_len = self.ev_g_play_anim(self.PRE_MOVE_ANIM_KEY, ret_len=True)
            self.has_pre_move_anim = bool(anim_len)
            if anim_len:
                self.delay_call(anim_len, lambda : self.ev_g_play_anim(self.MOVE_ANIM_KEY))
                return
        self.ev_g_play_anim(self.MOVE_ANIM_KEY)

    def on_anim_changed(self, *args):
        self.ev_g_play_anim(self.MOVE_ANIM_KEY)