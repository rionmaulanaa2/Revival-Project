# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/lobby/NewSysPrompt/SysUnlockUI.py
from __future__ import absolute_import
from logic.comsys.lobby.NewSystemPromptUI import NewSystemPromptUIBase
from logic.comsys.lobby.NewSysPrompt.NewSysPromptViewData import SysSysUnlockProviderFactory, SysUnlockProvider
from logic.gutils import system_unlock_utils
from logic.gutils import jump_to_ui_utils
from logic.comsys.lobby.CareerIconOutMotion import CareerIconOutMotion
ON_CLICK_GOTO_BTN_HIDE_KEY = '_on_click_goto_btn_k'

class SysUnlockUI(NewSystemPromptUIBase):

    def _gen_view_content_provider_factory(self):
        return SysSysUnlockProviderFactory()

    def _on_play_single(self, vcp):
        if not isinstance(vcp, SysUnlockProvider):
            return
        sys_type = vcp.get_system_type()
        global_data.emgr.system_unlocked.emit(sys_type)

    def _gen_inbetween_blocking_action(self, vcp, resume_cb):
        if not isinstance(vcp, SysUnlockProvider):
            return None
        else:
            sys_type = vcp.get_system_type()
            if sys_type == system_unlock_utils.SYSTEM_CAREER:
                has_m = system_unlock_utils.has_sys_unlock_mechanics(system_unlock_utils.SYSTEM_CAREER)
                if has_m:
                    from logic.gutils.career_utils import gen_cur_non_medal_badge_prompt_data_list
                    lst = gen_cur_non_medal_badge_prompt_data_list()
                    if lst:

                        def action_func(lst=lst):
                            global_data.career_badge_prompt_mgr.push(lst)
                            global_data.career_badge_prompt_mgr.play(finish_cb=resume_cb)

                        return action_func
            return None

    def _get_fly_anim_params_core(self, vcp, fly_src_wpos):
        if not isinstance(vcp, SysUnlockProvider):
            return (None, None)
        else:
            sys_type = vcp.get_system_type()
            func_info = system_unlock_utils.get_sys_unlock_fly_func_info(sys_type)
            if not func_info:
                return (None, None)
            func_name = func_info.get('func')
            func = getattr(self, func_name)
            if not callable(func):
                return (None, None)
            args = func_info.get('args', [])
            kargs = func_info.get('kargs', {})
            dst_wpos = func(*args, **kargs)
            if not dst_wpos:
                return (None, None)
            motion = CareerIconOutMotion(fly_src_wpos, dst_wpos)
            return (
             dst_wpos, motion)

    @staticmethod
    def lobby_fly(lobby_ui_get_dst_wpos_func_name):
        lobby_ui = global_data.ui_mgr.get_ui('LobbyUI')
        if not lobby_ui:
            return
        else:
            dst_wpos_getter = getattr(lobby_ui, lobby_ui_get_dst_wpos_func_name, None)
            if not callable(dst_wpos_getter):
                return
            return dst_wpos_getter()

    def _on_click_goto_btn(self, *args, **kw):
        vcp = self._cur_vcp
        if not isinstance(vcp, SysUnlockProvider):
            self._defautl_on_click_goto_btn()
            return
        else:
            sys_type = vcp.get_system_type()
            if sys_type == system_unlock_utils.SYSTEM_CAREER:
                hide_key = ON_CLICK_GOTO_BTN_HIDE_KEY + str(system_unlock_utils.SYSTEM_CAREER)
                self.add_hide_count(hide_key)

                @self._exec_only_valid
                def close_cb():
                    self.add_show_count(hide_key)
                    self._try_close(False)

                from logic.comsys.career.CareerMainUI import CareerMainUI
                CareerMainUI(None, close_cb)
                has_m = system_unlock_utils.has_sys_unlock_mechanics(system_unlock_utils.SYSTEM_CAREER)
                if has_m:
                    from logic.gutils.career_utils import gen_cur_non_medal_badge_prompt_data_list
                    lst = gen_cur_non_medal_badge_prompt_data_list()
                    if lst:
                        global_data.career_badge_prompt_mgr.push(lst)
                        global_data.career_badge_prompt_mgr.play()
            elif sys_type == system_unlock_utils.SYSTEM_CLAN:
                from logic.gutils.jump_to_ui_utils import jump_to_clan_main
                jump_to_clan_main()
                self._try_close(False)
            elif sys_type == system_unlock_utils.SYSTEM_BOND:
                from logic.gutils.jump_to_ui_utils import try_jump_to_bond
                try_jump_to_bond(global_data.player.get_role())
                self._try_close(False)
            elif sys_type == system_unlock_utils.SYSTEM_CORP_TASK:
                from logic.gutils.jump_to_ui_utils import jump_to_task_ui
                from logic.gcommon.common_const.task_const import TASK_TYPE_CORP
                jump_to_task_ui(TASK_TYPE_CORP)
                self._try_close(False)
            else:
                jump_info = system_unlock_utils.get_sys_jump_info(sys_type)
                func_name = jump_info.get('func')
                if not func_name:
                    self._defautl_on_click_goto_btn()
                    return
                jump_func = getattr(jump_to_ui_utils, func_name)
                if not jump_func:
                    self._defautl_on_click_goto_btn()
                    return
                hide_key = ON_CLICK_GOTO_BTN_HIDE_KEY + str(sys_type)
                self.add_hide_count(hide_key)
                play_out_anim = jump_info.get('out_anim', False)

                @self._exec_only_valid
                def close_cb(play_out_anim=play_out_anim):
                    self.add_show_count(hide_key)
                    self._try_close(play_out_anim)

                try:
                    if not jump_func(close_cb=close_cb):
                        close_cb()
                except TypeError as e:
                    close_cb()

            return