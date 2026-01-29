# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/clan/ClanCardUI.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
from common.const.uiconst import NORMAL_LAYER_ZORDER, UI_VKB_CLOSE

class ClanCardUI(BasePanel):
    PANEL_CONFIG_NAME = 'crew/crew_card'
    DLG_ZORDER = NORMAL_LAYER_ZORDER
    UI_ACTION_EVENT = {'temp_btn_close.btn_back.OnClick': '_on_click_back',
       'btn_apply.btn_major.OnClick': '_on_click_apply'
       }
    GLOBAL_EVENT = {'create_join_success': '_on_create_clan_success'
       }
    OPEN_SOUND_NAME = 'menu_shop'
    UI_VKB_TYPE = UI_VKB_CLOSE

    def on_init_panel(self, clan_id):
        self._clan_id = clan_id
        self._closing = False
        self.hide_main_ui()
        self.init_widget()
        if global_data.player and not global_data.player.is_in_clan():
            self.panel.btn_apply.setVisible(True)
        else:
            self.panel.btn_apply.setVisible(False)

    def init_widget(self):
        from .ClanCardWidget import ClanCardWidget
        self._card_widget = ClanCardWidget(self, self.panel.temp_crew_card, self._clan_id)

    def _on_click_back(self, *args):
        if self._closing:
            return
        self._closing = True
        self.close()

    def _on_click_apply(self, *args):
        if not global_data.player:
            return
        apply_window = global_data.ui_mgr.show_ui('ClanApplyJoinUI', 'logic.comsys.clan')
        apply_window.set_clan_id_list([self._clan_id])
        apply_window.set_apply_cb(lambda : self.apply_join_cb())

    def apply_join_cb(self):
        if not self.panel:
            return
        if global_data.player.has_requested_join(self._clan_id):
            self.panel.btn_apply.btn_major.SetText(800033)
            self.panel.btn_apply.btn_major.SetEnable(False)

    def _on_create_clan_success(self, *args):
        self.panel.btn_apply.btn_major.SetEnable(False)
        self.panel.btn_apply.btn_major.SetText(800148)

    def on_finalize_panel(self):
        self.destroy_widget('_card_widget')
        self.show_main_ui()