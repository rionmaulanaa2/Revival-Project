# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/lobby/NewSysPrompt/NewSysMechaSkinDefinePromptUI.py
from __future__ import absolute_import
from logic.comsys.lobby.NewSystemPromptUI import NewSystemPromptUIBase
from logic.comsys.lobby.NewSysPrompt.NewSysPromptViewData import NewSysMSDPromptProviderFactory, NewSysMechaSkinDefinePromptProvider
from logic.comsys.lobby.CareerIconOutMotion import CareerIconOutMotion
ON_CLICK_GOTO_BTN_HIDE_KEY = '_on_click_goto_btn_k'

class NewSysMechaSkinDefinePromptUI(NewSystemPromptUIBase):

    def _gen_view_content_provider_factory(self):
        return NewSysMSDPromptProviderFactory()

    def _get_fly_anim_params_core(self, vcp, fly_src_wpos):
        if not isinstance(vcp, NewSysMechaSkinDefinePromptProvider):
            return (None, None)
        else:
            lobby_ui = global_data.ui_mgr.get_ui('LobbyUI')
            if lobby_ui is not None:
                dst_wpos = lobby_ui.get_mecha_icon_cocos_wpos()
                motion = CareerIconOutMotion(fly_src_wpos, dst_wpos)
                return (
                 dst_wpos, motion)
            return (None, None)

    def _on_click_goto_btn(self, *args, **kw):
        vcp = self._cur_vcp
        if not isinstance(vcp, NewSysMechaSkinDefinePromptProvider):
            self._defautl_on_click_goto_btn()
            return
        hide_key = ON_CLICK_GOTO_BTN_HIDE_KEY + NewSysMechaSkinDefinePromptProvider.__name__
        self.add_hide_count(hide_key)

        @self._exec_only_valid
        def close_cb():
            self.add_show_count(hide_key)
            self._try_close(False)

        from logic.gutils.jump_to_ui_utils import jump_to_skin_define
        jump_to_skin_define(8001, 201800100, close_cb)