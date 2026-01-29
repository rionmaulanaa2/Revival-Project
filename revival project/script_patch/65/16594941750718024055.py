# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/guide_ui/GuideAppComment.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
from common.const.uiconst import DIALOG_LAYER_ZORDER_2
import game3d
from common.const import uiconst
from logic.gutils.ui_salog_utils import add_uiclick_salog_lobby

class GuideAppComment(BasePanel):
    PANEL_CONFIG_NAME = 'guide/guide_comment'
    DLG_ZORDER = DIALOG_LAYER_ZORDER_2
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    UI_ACTION_EVENT = {'temp_never.btn.OnClick': '_on_click_never_btn',
       'temp_btn_quit.btn_common.OnClick': '_on_click_later_btn',
       'temp_btn_comment.btn_common.OnClick': '_on_click_confirm_btn',
       'temp_btn_roast.btn_common.OnClick': '_on_click_gm_web_btn'
       }

    def on_init_panel(self):
        self.disappearing = False
        self.never_remind = False

    def _on_click_never_btn(self, *args):
        click_result = not self.never_remind
        self.panel.temp_never.btn.bar.choose.setVisible(click_result)
        self.never_remind = click_result
        if self.never_remind:
            add_uiclick_salog_lobby('ac_never_remind')

    def _on_click_confirm_btn(self, *args):
        if self.disappearing:
            return
        global_data.channel.app_comment()
        if global_data.player:
            global_data.player.update_comment_to_server(self.never_remind, True)
        add_uiclick_salog_lobby('ac_ok')
        self.close()

    def _on_click_later_btn(self, *args):
        if self.disappearing:
            return
        self.disappearing = True
        if global_data.player:
            global_data.player.update_comment_to_server(self.never_remind, False)
        add_uiclick_salog_lobby('ac_quit')
        self.close()

    def _on_click_gm_web_btn(self, *args):
        import game3d
        if self.disappearing:
            return
        self.disappearing = True
        if global_data.player:
            global_data.player.update_comment_to_server(self.never_remind, True)
        if hasattr(game3d, 'open_gm_web_view'):
            global_data.player.get_custom_service_token()
            game3d.open_gm_web_view('')
        else:
            data = {'methodId': 'ntOpenGMPage',
               'refer': ''
               }
            global_data.channel.extend_func_by_dict(data)
        add_uiclick_salog_lobby('ac_gm_web')
        self.close()

    def on_finalize_panel(self):
        self.disappearing = False