# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/common_ui/UserVerifyCodeUI.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
import common.const.uiconst
import common.utilities
from common.const import uiconst

class UserVerifyCodeUI(BasePanel):
    PANEL_CONFIG_NAME = 'activity/activity_202201/spring_shout_friends/open_acticity_binding'
    DLG_ZORDER = common.const.uiconst.DIALOG_LAYER_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_CLOSE
    UI_ACTION_EVENT = {'btn_copy.OnClick': 'on_click_btn_copy',
       'btn_close.OnClick': 'on_click_close_btn',
       'btn_question.OnClick': 'on_click_btn_question'
       }
    GLOBAL_EVENT = {}

    def on_init_panel(self, *args, **kargs):
        self.panel.btn_question.setVisible(False)
        self.panel.lab_user_name.SetString(str(global_data.player.uid))
        self.panel.lab_user_pass_word.SetString(global_data.player.get_verifycode())

    def on_click_btn_copy(self, btn, touch):
        self.set_text_to_clipboard(str(global_data.player.uid) + '|' + self.panel.lab_user_pass_word.getString())

    def set_text_to_clipboard(self, text):
        import game3d
        game3d.set_clipboard_text(text)
        global_data.game_mgr.show_tip(get_text_by_id(610583))

    def on_click_close_btn(self, btn, touch):
        self.close()

    def on_click_btn_question(self, btn, touch):
        from logic.comsys.common_ui.GameRuleDescUI import GameRuleDescUI
        dlg = GameRuleDescUI()
        dlg.set_show_rule(get_text_by_id(610298), get_text_by_id(int(610584)))