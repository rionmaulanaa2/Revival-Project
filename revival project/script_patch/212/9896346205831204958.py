# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/com_character_ctrl/ComHumanBehavior.py
from __future__ import absolute_import
from logic.gcommon.component.UnitCom import UnitCom
from common.cfg import confmgr
from logic.gcommon.common_utils import status_utils
from ....cdata.status_config import *
import sys
import os
import copy
from logic.gcommon.common_const import buff_const as bconst
from .ComBehavior import ComBehavior
HUMAN_ID_BASE = 10000

class ComHumanBehavior(ComBehavior):
    JUMP_STATE = (
     ST_JUMP_1, ST_JUMP_2, ST_JUMP_3, ST_SUPER_JUMP)
    DASH_STATE = (
     ST_RUSH,)
    BIND_EVENT = ComBehavior.BIND_EVENT.copy()
    BIND_EVENT.update({'E_ON_LEAVE_MECHA': '_on_leave_mecha',
       'E_ON_LEAVE_VEHICLE': '_on_leave_mecha',
       'E_ON_ACTION_LEAVE_VEHICLE': '_on_leave_mecha'
       })

    def __init__(self):
        super(ComHumanBehavior, self).__init__()

    def init_from_dict(self, unit_obj, bdict):
        bdict['npc_id'] = 11 + HUMAN_ID_BASE
        super(ComHumanBehavior, self).init_from_dict(unit_obj, bdict)

    def on_init_complete(self):
        super(ComHumanBehavior, self).on_init_complete()

    def on_load_animator_complete(self, *args):
        if self.ev_g_is_agent():
            self.need_update = True
        cur_states = self.ev_g_get_all_state()
        if not cur_states or len(cur_states) == 1 and ST_STAND in cur_states:
            self.set_default_state(self._default_state)
        if not self.ev_g_is_in_mecha() and not self.ev_g_ctrl_mecha():
            self.send_event('E_ENABLE_BEHAVIOR')

    def on_lose_connect(self):
        if not self.ev_g_is_in_any_state((ST_MECHA_BOARDING, ST_MECHA_DRIVER, ST_DOWN)):
            if self.ev_g_get_buff(bconst.BUFF_GLOBAL_KEY, bconst.BUFF_ID_BALL_STATE):
                pass
            elif self.status_config.MC_STAND in self._states:
                self._states[self.status_config.MC_STAND].enter(set())
                self._states[self.status_config.MC_STAND].update(0.01)
                self.send_event('E_CLEAR_UP_BODY_ANIM')

    def _on_leave_mecha(self):
        self.on_enable_behavior()

    def leave_states(self, leave_state, new_state=None):
        state_id = leave_state
        if state_id not in self._cur_state:
            return
        else:
            self._cur_state.remove(state_id)
            if state_id not in self._states:
                return
            if new_state is None:
                new_state = set()
            else:
                new_state = set([new_state])
            self._states[state_id].exit(new_state)
            return