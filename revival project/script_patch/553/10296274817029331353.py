# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/lobby/SysUnlock/SystemUnlockMgr.py
from __future__ import absolute_import
import six_ex
from functools import cmp_to_key
from common.framework import Singleton
from logic.gutils import system_unlock_utils

class SystemUnlockMgr(Singleton):
    ALIAS_NAME = 'sys_unlock_mgr'

    def init(self):
        self._cur_unlock_msg_list = []

    def on_finalize(self):
        pass

    def peek_next_msg(self):
        if len(self._cur_unlock_msg_list) > 0:
            return self._cur_unlock_msg_list[0]
        else:
            return None
            return None

    def pop_next_msg(self):
        if len(self._cur_unlock_msg_list) > 0:
            return self._cur_unlock_msg_list.pop(0)
        else:
            return None
            return None

    def _try_add_unlock_msg(self, sys_type, sort=True):
        if sys_type is None:
            log_error('try_add_unlock_msg sys_type None')
            return
        else:
            if sys_type in self._cur_unlock_msg_list:
                return
            if system_unlock_utils.is_sys_no_prompt(sys_type):
                return
            self._cur_unlock_msg_list.append(sys_type)
            if sort:
                self.sort_cur_msgs()
            return

    @staticmethod
    def msg_sorter(a_sys_type, b_sys_type):
        from logic.gcommon.cdata import sys_unlock_data as su_data
        a_prio = su_data.cfg_data.get(a_sys_type, {}).get('show_priority', -1)
        b_prio = su_data.cfg_data.get(b_sys_type, {}).get('show_priority', -1)
        return six_ex.compare(b_prio, a_prio)

    def sort_cur_msgs(self):
        self._cur_unlock_msg_list.sort(key=cmp_to_key(self.msg_sorter))

    def level_check(self, old_lv, new_lv):
        lst = self.gen_level_change_check_result(old_lv, new_lv)
        for sys in lst:
            self._try_add_unlock_msg(sys, sort=False)

        lst and self.sort_cur_msgs()

    @staticmethod
    def gen_level_change_check_result(old_lv, new_lv):
        if not isinstance(old_lv, int) or not isinstance(new_lv, int):
            return []
        ret_set = set()
        from logic.gcommon.cdata import sys_unlock_data as su_data
        for sys_type in su_data.SYS_TYPES:
            if not system_unlock_utils.has_sys_unlock_mechanics(sys_type):
                continue
            has, unlock_lv = system_unlock_utils.get_sys_unlock_level(sys_type)
            if not has:
                continue
            if old_lv < unlock_lv and new_lv >= unlock_lv:
                ret_set.add(sys_type)

        return list(ret_set)

    def check_show_ui(self):
        msg = self.peek_next_msg()
        if msg is None:
            return
        else:
            if global_data.player and global_data.player.is_running_show_advance():
                if not global_data.player.has_advance_callback('SysUnlockUI'):

                    def callback():
                        global_data.ui_mgr.show_ui('SysUnlockUI', 'logic.comsys.lobby.NewSysPrompt')

                    global_data.player.add_advance_callback('SysUnlockUI', callback, hide_lobby_ui=False)
            else:
                global_data.ui_mgr.show_ui('SysUnlockUI', 'logic.comsys.lobby.NewSysPrompt')
            return

    def set_debug_msgs(self, msgs):
        if global_data.is_inner_server:
            self._cur_unlock_msg_list = msgs