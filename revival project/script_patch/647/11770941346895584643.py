# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/share/ComStatusMonster.py
from __future__ import absolute_import
from .ComStatus import ComStatus
from ...cdata import pve_monster_status_config
import time
import traceback
from logic.gcommon.common_utils import status_utils

class ComStatusMonster(ComStatus):
    BIND_EVENT = ComStatus.BIND_EVENT.copy()
    BIND_EVENT.update({'E_RESET_STATE': 'reset_state',
       'G_TRANS_STATUS': '_try_trans_st_mecha'
       })

    def __init__(self):
        super(ComStatusMonster, self).__init__()
        self.status_config = pve_monster_status_config

    def init_from_dict(self, unit_obj, bdict):
        super(ComStatusMonster, self).init_from_dict(unit_obj, bdict)
        self._npc_id = bdict['npc_id']

    def on_init_complete(self):
        npc_id = str(self._npc_id)
        data = status_utils.get_behavior_config(npc_id)
        self.mp_st_forbid = data.get_forbid(npc_id)
        self.mp_st_cover = data.get_cover(npc_id)

    def reset_state(self, is_vehicle=False, state_id=None):
        state_id = state_id or self.status_config.MC_STAND
        self.set_st = set([state_id])

    def _try_trans_st_mecha(self, new_st, sync=False, force=False):
        if not force and not self._check_pass(new_st):
            return False
        if sync:
            self.send_event('E_CALL_SYNC_METHOD', 'try_trans_status', (new_st,), True)
        now_time = time.time()
        need_cover_old_states = self._cover_state(new_st)
        self.set_st.add(new_st)
        self._status_start_time[new_st] = now_time
        for one_old_state in need_cover_old_states:
            self.send_event('E_LEAVE_STATE', one_old_state, new_st)

        self.send_event('E_ENTER_STATE', new_st)
        if self._is_debug_mode:
            stack = traceback.format_stack()
            self._debug_status_stack[new_st] = ''.join(stack)
        return True