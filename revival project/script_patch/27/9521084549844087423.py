# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/clan/ClanInActiveConfirm.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
from common.const.uiconst import BG_ZORDER, DIALOG_LAYER_ZORDER, UI_VKB_CLOSE
from logic.gutils import clan_utils
from logic.gcommon.time_utility import get_rela_month_no

class ClanInActiveConfirm(BasePanel):
    PANEL_CONFIG_NAME = 'crew/bg_crew_confirm_small'
    DLG_ZORDER = DIALOG_LAYER_ZORDER
    UI_VKB_TYPE = UI_VKB_CLOSE
    UI_ACTION_EVENT = {'btn_close.OnClick': 'on_click_think',
       'temp_btn_1.btn_common_big.OnClick': 'on_click_think',
       'temp_btn_2.btn_common_big.OnClick': 'on_click_quit',
       'temp_check_box.btn.OnClick': 'on_click_choose_btn'
       }

    def on_init_panel(self, *args, **kwargs):
        self.init_parameters()
        self.init_panel()

    def init_panel(self):
        self.panel.temp_check_box.choose.setVisible(self.is_check_not_tips)

    def init_parameters(self):
        self.is_check_not_tips = False

    def close(self, *args):
        super(ClanInActiveConfirm, self).close(*args)

    def on_click_choose_btn(self, *args):
        self.is_check_not_tips = not self.is_check_not_tips
        self.panel.temp_check_box.choose.setVisible(self.is_check_not_tips)

    def on_click_quit(self, *args):
        global_data.player.request_quit_clan(True)
        global_data.player.search_clan_by_limit(1, 99999, 99999, 0, open_ui=True)
        self.close()

    def on_click_think(self, *args):
        if self.is_check_not_tips:
            global_data.achi_mgr.set_cur_user_archive_data('ignore_clan_inactive_confirm', get_rela_month_no())
        self.close()