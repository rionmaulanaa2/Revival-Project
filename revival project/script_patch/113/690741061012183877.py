# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComStatusMechaClient.py
from __future__ import absolute_import
from __future__ import print_function
import six
from ..share.ComStatus import ComStatus
from ...cdata import mecha_status_config
from logic.gcommon.common_utils import status_utils
import time
import traceback

class ComStatusMechaClient(ComStatus):
    BIND_EVENT = ComStatus.BIND_EVENT.copy()
    BIND_EVENT.update({'E_SWITCH_BEHAVIOR': 'on_switch_behavior',
       'E_ADD_WHITE_STATE': 'on_add_white_state',
       'E_MOD_MP_ST': 'on_mod_mp_st',
       'E_CLEAR_WHITE_STATE': 'on_clear_mecha_white_state',
       'G_TRANS_STATUS': '_try_trans_st_mecha',
       'E_LEAVE_MECHA_SENT': 'leave_mecha_sent'
       })

    def __init__(self):
        super(ComStatusMechaClient, self).__init__()
        self.status_config = mecha_status_config

    def init_from_dict(self, unit_obj, bdict):
        super(ComStatusMechaClient, self).init_from_dict(unit_obj, bdict)
        self._mecha_id = bdict['mecha_id']
        self._white_state = {}
        self._white_state_of_owner = {}
        self._white_state_to_cover = {}
        self._black_state = set([])
        self.on_leave_mecha_sent = False

    def destroy(self):
        self._white_state = None
        self._white_state_of_owner = None
        self._white_state_to_cover = None
        self._black_state = None
        super(ComStatusMechaClient, self).destroy()
        return

    def reset(self):
        self.set_st = set()
        self._white_state = {}
        self._white_state_of_owner = {}
        self._white_state_to_cover = {}
        self._black_state = set([])

    def on_mod_mp_st(self, attr_map, oper, mod_st, oper_st):
        if attr_map not in ('mp_st_cover', 'mp_st_forbid'):
            return
        mp_st = getattr(self, attr_map) or {}
        if isinstance(oper_st, int):
            oper_st = set([oper_st])
        oper_set = mp_st.get(mod_st, set([]))
        if oper == 'sub':
            oper_set -= oper_st
        elif oper == 'add':
            oper_set += oper_st

    def get_all_state_desc(self):
        desc = super(ComStatusMechaClient, self).get_all_state_desc()
        white_state_of_owner = {}
        for key, value in six.iteritems(self._white_state_of_owner):
            key_desc = self._get_nulm_state_2_str(key)
            white_state_of_owner[key_desc] = self._get_nulm_state_2_str(value)

        desc = desc + '--white_state_of_owner = ' + str(white_state_of_owner)
        with_num_white_state = {}
        for key, value in six.iteritems(self._white_state):
            key_desc = self._get_nulm_state_2_str(key)
            with_num_white_state[key_desc] = self._get_nulm_state_2_str(value)

        desc = desc + '--with_num_white_state = ' + str(with_num_white_state)
        return desc

    def on_mod_mp_st(self, attr_map, oper, mod_st, oper_st):
        if attr_map not in ('mp_st_cover', 'mp_st_forbid'):
            return
        mp_st = getattr(self, attr_map) or {}
        if isinstance(oper_st, int):
            oper_st = set([oper_st])
        oper_set = mp_st.get(mod_st, set([]))
        if oper == 'sub':
            oper_set -= oper_st
        elif oper == 'add':
            oper_set = oper_set.union(oper_st)

    def remove_state(self, status):
        super(ComStatusMechaClient, self).remove_state(status)
        self.on_clear_mecha_white_state(status)

    def get_client_dict(self):
        return {'set_st': self.set_st
           }

    def on_init_complete(self):
        shape_shift = self.ev_g_shape_shift()
        mecha_id = self._mecha_id
        if shape_shift:
            mecha_id = '{}_{}'.format(mecha_id, shape_shift)
        self.on_switch_behavior(mecha_id)

    def on_switch_behavior(self, npc_id, *args, **kwargs):
        npc_id = str(npc_id)
        self.mp_st_forbid = status_utils.get_forbid_copy(npc_id)
        self.mp_st_cover = status_utils.get_cover_copy(npc_id)
        if mecha_status_config.MC_SHOOT in self.mp_st_forbid:
            self.mp_st_forbid[mecha_status_config.MC_SHOOT].add(mecha_status_config.MC_IMMOBILIZE)
        if mecha_status_config.MC_SECOND_WEAPON_ATTACK in self.mp_st_forbid:
            self.mp_st_forbid[mecha_status_config.MC_SECOND_WEAPON_ATTACK].add(mecha_status_config.MC_IMMOBILIZE)

    def on_add_white_state(self, state, to_cover_state_list=None):
        if to_cover_state_list:
            if isinstance(to_cover_state_list, int):
                to_cover_state_list = [
                 to_cover_state_list]
            for owner in to_cover_state_list:
                if owner not in self._white_state_of_owner:
                    self._white_state_of_owner[owner] = set()
                cross_set = state & self._white_state_of_owner[owner]
                diff_set = state - cross_set
                for one_state in diff_set:
                    if one_state in self._white_state:
                        self._white_state[one_state] += 1
                    else:
                        self._white_state[one_state] = 1

                self._white_state_of_owner[owner] |= state

            for one_state in state:
                if one_state not in self._white_state_to_cover:
                    self._white_state_to_cover[one_state] = set(to_cover_state_list)
                else:
                    self._white_state_to_cover[one_state] |= set(to_cover_state_list)

        else:
            log_error('Mecha using white_state without posting owner_state_id!!!!!!')

    def on_clear_mecha_white_state(self, owner_states):
        if isinstance(owner_states, int):
            owner_states = [
             owner_states]
        owner_states = list(owner_states)
        for owner in owner_states:
            if owner not in self._white_state_of_owner:
                self._white_state_of_owner[owner] = set()
            for w_state in self._white_state_of_owner.get(owner, set()):
                if w_state in self._white_state:
                    if self._white_state[w_state] > 0:
                        self._white_state[w_state] -= 1
                        if w_state in self._white_state_to_cover:
                            self._white_state_to_cover[w_state].remove(owner)
                            if not self._white_state_to_cover[w_state]:
                                del self._white_state_to_cover[w_state]

            self._white_state_of_owner[owner] = set()

    def get_status_max_duration(self, status):
        data = status_utils.get_behavior_config(str(self.sd.ref_mecha_id))
        behavior_info = data.get_behavior(str(self.sd.ref_mecha_id))
        state_info = behavior_info.get(status, {})
        max_duration = state_info.get('max_duration', 0)
        if max_duration:
            return
        return super(ComStatusMechaClient, self).get_status_max_duration(status)

    def _check_pass(self, new_st, is_quiet=False, only_avatar=True):
        if G_IS_CLIENT:
            if not self.ev_g_is_avatar() and not self.sd.ref_is_agent:
                if only_avatar:
                    return True
        if self.on_leave_mecha_sent and new_st not in (mecha_status_config.MC_DRIVER_LEAVING, mecha_status_config.MC_STAND):
            return False
        else:
            can_cover_states = None
            if self.check_white_state(new_st):
                can_cover_states = self._white_state_to_cover.get(new_st, None)
                if not can_cover_states:
                    return True
            if self.check_black_state(new_st):
                return False
            return super(ComStatusMechaClient, self)._check_pass(new_st, is_quiet, only_avatar, ignore_st=can_cover_states)

    def _cover_state(self, new_st):
        sync = False
        if self.check_white_state(new_st):
            can_cover_states = self._white_state_to_cover.get(new_st, None)
            if not can_cover_states:
                sync = True
        need_cover_old_states = super(ComStatusMechaClient, self)._cover_state(new_st)
        if sync and need_cover_old_states:
            for one_state in need_cover_old_states:
                print('test--_cover_state--step2--try_cancel_status--one_state =', one_state)
                import traceback
                traceback.print_stack()
                self.send_event('E_CALL_SYNC_METHOD', 'try_cancel_status', (one_state,), True)

        return need_cover_old_states

    def check_white_state(self, new_st):
        if isinstance(new_st, int):
            return self._white_state.get(new_st, 0) > 0
        else:
            for st in new_st:
                if self._white_state.get(st, 0) <= 0:
                    return False

            return True

    def check_black_state(self, new_st):
        return new_st in self._black_state

    def reset_state(self, is_vehicle=False, state_id=None):
        if state_id:
            self.set_st = set([state_id])
        else:
            self.set_st = set([self.status_config.MC_STAND])

    def _try_trans_st(self, new_st, sync=False, force=False):
        return True

    def _try_trans_st_mecha(self, new_st, sync=False, force=False):
        if self.check_white_state(new_st):
            can_cover_states = self._white_state_to_cover.get(new_st, None)
            if can_cover_states:
                need_cover_old_states = can_cover_states & self.set_st
                if self.ev_g_is_avatar() and need_cover_old_states:
                    for one_state in need_cover_old_states:
                        self.send_event('E_CALL_SYNC_METHOD', 'try_cancel_status', (one_state,), True)

                if need_cover_old_states:
                    self.remove_state(can_cover_states)
                for one_simple_state in need_cover_old_states:
                    self._cancel_combine_state(one_simple_state)

                need_cover_old_states |= self._cover_state(new_st)
            else:
                need_cover_old_states = self.set_st.copy()
                self.reset()
        else:
            if not force and not self._check_pass(new_st):
                return False
            need_cover_old_states = self._cover_state(new_st)
        if sync:
            self.send_event('E_CALL_SYNC_METHOD', 'try_trans_status', (new_st,), True)
        self.set_st.add(new_st)
        now_time = time.time()
        self._status_start_time[new_st] = now_time
        for one_old_state in need_cover_old_states:
            self.send_event('E_LEAVE_STATE', one_old_state, new_st)

        self.send_event('E_ENTER_STATE', new_st)
        if self._is_debug_mode:
            stack = traceback.format_stack()
            self._debug_status_stack[new_st] = ''.join(stack)
        return True

    def leave_mecha_sent(self, sent):
        self.on_leave_mecha_sent = sent