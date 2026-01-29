# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/share/ComStatusHuman.py
from __future__ import absolute_import
import six
import copy
from .ComStatus import ComStatus
from logic.gcommon.cdata import status_config, status_forbid_config, status_cover_config
from logic.gcommon.common_utils import status_utils
if G_IS_CLIENT:
    from exception_hook import traceback_uploader

class ComStatusHuman(ComStatus):
    DEAD_STATE = status_config.ST_DEAD
    BIND_EVENT = ComStatus.BIND_EVENT.copy()
    BIND_EVENT.update({'E_RESET_STATE': 'reset_state',
       'E_SET_STATUS_CHECK_ENABLE': '_on_set_status_check_enable',
       'E_MOD_MP_ST': 'on_mod_mp_st',
       'G_TRANS_STATUS': '_try_trans_st'
       })

    def __init__(self):
        super(ComStatusHuman, self).__init__()
        npc_id = '10011'
        self.mp_st_forbid = status_utils.get_forbid_copy(npc_id)
        self.mp_st_cover = status_utils.get_cover_copy(npc_id)
        self.status_config = status_config

    def init_from_dict(self, unit_obj, bdict):
        super(ComStatusHuman, self).init_from_dict(unit_obj, bdict)
        from logic.units.LAvatar import LAvatar
        self._status_check_enable = isinstance(self.unit_obj, LAvatar) or self.unit_obj.is_robot()

    def _on_set_status_check_enable(self, enable):
        self._status_check_enable = enable

    def on_mod_mp_st(self, attr_map, oper, mod_st, oper_st):
        if attr_map not in ('mp_st_cover', 'mp_st_forbid'):
            return
        mp_st = getattr(self, attr_map)
        if isinstance(oper_st, int):
            oper_st = set([oper_st])
        oper_set = mp_st.get(mod_st)
        if oper == 'sub':
            oper_set -= oper_st
        elif oper == 'add':
            oper_set += oper_st

    def _try_trans_st(self, new_st, sync=False, force=False):
        if self.get_state(new_st):
            return True
        return super(ComStatusHuman, self)._try_trans_st(new_st, sync, force)

    def _check_pass(self, new_st, is_quiet=False, only_avatar=True):
        if not self._status_check_enable:
            if only_avatar and not self.get_state(status_config.ST_DOWN):
                return 1
        return super(ComStatusHuman, self)._check_pass(new_st, is_quiet, only_avatar)

    def remove_state(self, status):
        super(ComStatusHuman, self).remove_state(status)
        if isinstance(status, int):
            status = [
             status]
        for one_status in status:
            dest_white_state_list = self._white_state_to_cover.get(one_status, None)
            if dest_white_state_list:
                del self._white_state_to_cover[one_status]
                if one_status in self._white_state:
                    self._white_state.remove(one_status)
                for one_white_status in dest_white_state_list:
                    if one_white_status in self._white_state:
                        self._white_state.remove(one_white_status)

            del_status_list = []
            for needed_cover_state, new_states_list in six.iteritems(self._white_state_to_cover):
                if len(new_states_list) == 1 and one_status in new_states_list:
                    del_status_list.append(needed_cover_state)

            for del_status in del_status_list:
                del self._white_state_to_cover[del_status]
                if del_status in self._white_state:
                    self._white_state.remove(del_status)

        return

    def reset_state(self, *args, **kwargs):
        need_reserve_states = set([self.status_config.ST_EMPTY_HAND]) & self.set_st
        self.set_st = set([self.status_config.ST_STAND])
        self.set_st |= need_reserve_states