# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/role/PlayerIntimacyWidget.py
from __future__ import absolute_import
from six.moves import range
from .PlayerTabBaseWidget import PlayerTabBaseWidget
from common.const.property_const import *
from logic.comsys.intimacy.IntimacyPanel import *

class PlayerIntimacyWidget(PlayerTabBaseWidget, IntimacyPanel):
    PANEL_CONFIG_NAME = 'friend/i_intimacy_main'

    def __init__(self, panel):
        PlayerTabBaseWidget.__init__(self, panel)
        IntimacyPanel.__init__(self, self.panel)

    def on_refresh_player_detail_inf(self, player_inf):
        self.set_player_inf(player_inf)

    def init_panel(self):
        self.panel.img_bg.setVisible(True)
        self.panel.lab_describe.SetColor(14936317)
        self.panel.nd_tab.setVisible(False)
        self.panel.pnl_list_top_tab.setVisible(True)
        self.nd_tab_list = self.panel.pnl_list_top_tab
        super(PlayerIntimacyWidget, self).init_panel()

    def touch_tab_by_index(self, tab_item, tab_index):
        tab_item = self.nd_tab_list.GetItem(self._cur_tab_index)
        if tab_item:
            tab_item.btn_tab.SetSelect(False)
        tab_item = self.nd_tab_list.GetItem(tab_index)
        if tab_item:
            tab_item.btn_tab.SetSelect(True)
        self._cur_tab_index = tab_index
        for idx in range(INTIMACY_LIST_COUNT):
            self.set_tab_visible(idx, idx == self._cur_tab_index)

        self.panel.btn_remove.setVisible(self._cur_tab_index == INTIMACY_LIST_TAB_REQUEST)
        self.panel.btn_sort.setVisible(self.is_mine and self._cur_tab_index == INTIMACY_LIST_TAB_MY)

    def destroy(self):
        super(PlayerIntimacyWidget, self).destroy()
        IntimacyPanel.destroy(self)