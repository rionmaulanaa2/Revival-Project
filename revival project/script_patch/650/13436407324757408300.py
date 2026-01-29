# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/lobby/NewSysPrompt/NewSystemPromptCommonUI.py
from __future__ import absolute_import
from logic.comsys.lobby.NewSystemPromptUI import NewSystemPromptUIBase
from logic.comsys.lobby.NewSysPrompt.NewSysPromptViewData import NewSysPromptProviderFactory, NewSysPromptProvider
from logic.gcommon.common_const import new_system_prompt_data as sp_const
from logic.comsys.lobby.CareerIconOutMotion import CareerIconOutMotion
ON_CLICK_GOTO_BTN_HIDE_KEY = '_on_click_goto_btn_k'

class NewSystemPromptCommonUI(NewSystemPromptUIBase):

    def _gen_view_content_provider_factory(self):
        return NewSysPromptProviderFactory()

    def _on_play_single(self, vcp):
        if not isinstance(vcp, NewSysPromptProvider):
            return
        sys_type = vcp.get_system_type()
        global_data.new_sys_open_mgr.mark_sys_prompt_read(sys_type)

    def _get_fly_anim_params_core(self, vcp, fly_src_wpos):
        if not isinstance(vcp, NewSysPromptProvider):
            return (None, None)
        else:
            sys_type = vcp.get_system_type()
            lobby_ui = global_data.ui_mgr.get_ui('LobbyUI')
            if lobby_ui is not None:
                if sys_type == sp_const.SYSTEM_CAREER:
                    dst_wpos = lobby_ui.get_career_icon_cocos_wpos()
                    motion = CareerIconOutMotion(fly_src_wpos, dst_wpos)
                    return (
                     dst_wpos, motion)
                if sys_type == sp_const.SYSTEM_BATTLE_FLAG:
                    dst_wpos = lobby_ui.get_avatar_frame_cocos_wpos()
                    motion = CareerIconOutMotion(fly_src_wpos, dst_wpos)
                    return (
                     dst_wpos, motion)
            return (None, None)

    def _on_click_goto_btn(self, *args, **kw):
        vcp = self._cur_vcp
        if not isinstance(vcp, NewSysPromptProvider):
            self._defautl_on_click_goto_btn()
            return
        sys_type = vcp.get_system_type()
        if sys_type == sp_const.SYSTEM_CAREER:
            hide_key = ON_CLICK_GOTO_BTN_HIDE_KEY + str(sp_const.SYSTEM_CAREER)
            self.add_hide_count(hide_key)

            @self._exec_only_valid
            def close_cb():
                self.add_show_count(hide_key)
                self._try_close(False)

            from logic.gutils.jump_to_ui_utils import jump_to_career
            if not jump_to_career(close_cb=close_cb):
                close_cb()
        elif sys_type == sp_const.SYSTEM_BATTLE_FLAG:
            hide_key = ON_CLICK_GOTO_BTN_HIDE_KEY + str(sp_const.SYSTEM_BATTLE_FLAG)
            self.add_hide_count(hide_key)

            @self._exec_only_valid
            def close_cb():
                self.add_show_count(hide_key)
                self._try_close(False)

            from logic.gutils.jump_to_ui_utils import jump_to_player_info
            from logic.comsys.role.PlayerInfoUI import TAB_BATTLE_FLAG
            jump_to_player_info(TAB_BATTLE_FLAG, close_cb)
        elif sys_type == sp_const.SYSTEM_INSCRIPTION:
            hide_key = ON_CLICK_GOTO_BTN_HIDE_KEY + str(sp_const.SYSTEM_INSCRIPTION)
            self.add_hide_count(hide_key)

            @self._exec_only_valid
            def close_cb():
                self.add_show_count(hide_key)
                self._try_close(False)

            from logic.gutils.jump_to_ui_utils import jump_to_inscription
            if not jump_to_inscription(close_cb=close_cb):
                close_cb()
        else:
            self._defautl_on_click_goto_btn()