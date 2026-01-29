# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/lobby/NewSystemOpenMgr.py
from __future__ import absolute_import
import six_ex
from functools import cmp_to_key
from common.framework import Singleton
from logic.gutils import new_sys_prompt_utils

class NewSystemOpenMgr(Singleton):
    ALIAS_NAME = 'new_sys_open_mgr'

    def init(self):
        self._cur_promp_list = []

    def on_finalize(self):
        pass

    def peek_next_prompt(self):
        if len(self._cur_promp_list) > 0:
            return self._cur_promp_list[0]
        else:
            return None
            return None

    def pop_next_prompt(self):
        if len(self._cur_promp_list) > 0:
            return self._cur_promp_list.pop(0)
        else:
            return None
            return None

    def mark_sys_prompt_read(self, sys_type):
        global_data.player and global_data.player.mark_sys_prompt_read(sys_type)

    def has_read_sys_prompt(self, sys_type):
        if not global_data.player:
            return True
        return global_data.player.has_read_sys_prompt(sys_type)

    def _try_add_prompt(self, sys_type, sort=True):
        if not isinstance(sys_type, int):
            return
        if new_sys_prompt_utils.is_sys_blocked(sys_type):
            return
        if self.has_read_sys_prompt(sys_type):
            return
        if not self._special_condition_check(sys_type):
            return
        if sys_type in self._cur_promp_list:
            return
        self._cur_promp_list.append(sys_type)
        if sort:
            self.sort_cur_prompts()

    @staticmethod
    def prompt_sorter(a_sys_type, b_sys_type):
        from logic.gcommon.common_const import new_system_prompt_data as sp_const
        a_prio = sp_const.cfg_data.get(a_sys_type, {}).get('show_priority', -1)
        b_prio = sp_const.cfg_data.get(b_sys_type, {}).get('show_priority', -1)
        return six_ex.compare(b_prio, a_prio)

    def sort_cur_prompts(self):
        self._cur_promp_list.sort(key=cmp_to_key(self.prompt_sorter))

    def _gen_in_promotion_sys_types(self):
        ret_set = set()
        from logic.gcommon.common_const import new_system_prompt_data as sp_const
        for sys_type in sp_const.SYS_TYPES:
            if new_sys_prompt_utils.in_promotion_time_range(sys_type):
                ret_set.add(sys_type)

        ret_list = list(ret_set)
        return ret_list

    def get_sp_check_func_name(self, sys_type):
        from logic.gcommon.common_const import new_system_prompt_data as sp_const
        return sp_const.cfg_data.get(sys_type, {}).get('sp_check_func_name', '')

    @staticmethod
    def inscription_check():
        if not global_data.player:
            return False
        return global_data.player.has_open_inscription()

    def _special_condition_check(self, sys_type):
        func_name = self.get_sp_check_func_name(sys_type)
        if not func_name:
            return True
        else:
            func = getattr(NewSystemOpenMgr, func_name, None)
            if not callable(func):
                return False
            return func()

    def active_check_addition(self):
        lst = self._gen_in_promotion_sys_types()
        for sys in lst:
            if not self.meet_lv_condition(sys):
                continue
            self._try_add_prompt(sys, sort=False)

        lst and self.sort_cur_prompts()

    def level_check(self, old_lv, new_lv):
        lst = self.gen_level_change_check_result(old_lv, new_lv)
        for sys in lst:
            self._try_add_prompt(sys, sort=False)

        lst and self.sort_cur_prompts()

    def meet_lv_condition(self, sys_type):
        has, prompt_level = new_sys_prompt_utils.get_sys_prompt_level(sys_type)
        if not has:
            return False
        sub_player = global_data.player
        if not sub_player:
            return False
        lv = sub_player.get_lv()
        return lv >= prompt_level

    @staticmethod
    def gen_level_change_check_result(old_lv, new_lv):
        if not isinstance(old_lv, int) or not isinstance(new_lv, int):
            return []
        ret_set = set()
        from logic.gcommon.common_const import new_system_prompt_data as sp_const
        for sys_type in sp_const.SYS_TYPES:
            has, prompt_level = new_sys_prompt_utils.get_sys_prompt_level(sys_type)
            if not has:
                continue
            if old_lv < prompt_level and new_lv >= prompt_level:
                ret_set.add(sys_type)

        return list(ret_set)

    def check_show_ui(self):
        prompt = self.peek_next_prompt()
        if prompt is None:
            return
        else:
            if global_data.player and global_data.player.is_running_show_advance():
                if not global_data.player.has_advance_callback('NewSystemPromptCommonUI'):

                    def callback():
                        global_data.ui_mgr.show_ui('NewSystemPromptCommonUI', 'logic.comsys.lobby.NewSysPrompt')

                    global_data.player.add_advance_callback('NewSystemPromptCommonUI', callback, hide_lobby_ui=False)
            else:
                global_data.ui_mgr.show_ui('NewSystemPromptCommonUI', 'logic.comsys.lobby.NewSysPrompt')
            return

    def set_debug_prompts(self, prompts):
        if global_data.is_inner_server:
            self._cur_promp_list = prompts