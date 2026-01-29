# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/clan/ClanSettingUI.py
from __future__ import absolute_import
from logic.comsys.common_ui.WindowMediumBase import WindowMediumBase
from logic.gutils.template_utils import update_badge_show, update_badge_node
from common.const.uiconst import NORMAL_LAYER_ZORDER_1
from logic.gcommon.common_const.clan_const import pack_badge

class ClanSettingUI(WindowMediumBase):
    PANEL_CONFIG_NAME = 'crew/i_crew_set_up'
    DLG_ZORDER = NORMAL_LAYER_ZORDER_1
    TEMPLATE_NODE_NAME = 'temp_bg'
    UI_ACTION_EVENT = {'btn_confirm.btn_common_big.OnClick': '_on_confirm',
       'btn_diy_logo.btn_common.OnClick': '_on_click_badge_btn'
       }
    GLOBAL_EVENT = {'net_login_reconnect_event': '_on_login_reconnected'
       }
    OPEN_SOUND_NAME = 'menu_shop'

    def on_init_panel(self):
        super(ClanSettingUI, self).on_init_panel()
        info = global_data.player.get_clan_info()
        self._apply_reject_limit = 0 if info['apply_reject_limit'] <= 0 else 1
        self._apply_approval_limit = 0 if info['apply_approval_limit'] <= 0 else 1
        self._badge = info.get('badge', 0)
        update_badge_node(self._badge, self.panel.temp_crew_logo)
        self._init_widget(info)

    def do_show_panel(self):
        super(ClanSettingUI, self).do_show_panel()

    def _on_login_reconnected(self, *args):
        self.close()

    def _init_widget(self, info):
        self._show_apply_setting()
        from .ClanLevelSettingUI import ClanLevelSettingUI
        from .ClanDanSettingWidget import ClanDanSettingWidget
        from .ClanLangSettingWidget import ClanLangSettingWidget
        if G_IS_NA_USER:
            self._lang_widget = ClanLangSettingWidget(self, self.panel.btn_language, info.get('lang', -1))
        else:
            self.panel.btn_language.setVisible(False)
        self._level_widget = ClanLevelSettingUI(self, self.panel.btn_level, info.get('apply_lv_limit', 0))
        self._dan_widget = ClanDanSettingWidget(self, self.panel.btn_tier, info.get('apply_dan_limit', -1))

    def _show_apply_setting(self):
        item_widget0 = self.panel.list_permission.GetItem(0)

        def set_apply_reject_limit(flag):
            self._apply_reject_limit = flag
            item_widget0.choose.setVisible(self._apply_reject_limit == 0)

        @item_widget0.btn.unique_callback()
        def OnClick(btn, touch):
            flag = 0 if self._apply_reject_limit > 0 else 1
            set_apply_reject_limit(flag)

        set_apply_reject_limit(self._apply_reject_limit)
        item_widget0.text.SetString(800062)
        item_widget1 = self.panel.list_permission.GetItem(1)

        def set_apply_approval_limit(flag):
            self._apply_approval_limit = flag
            item_widget1.choose.setVisible(self._apply_approval_limit == 1)

        @item_widget1.btn.unique_callback()
        def OnClick(btn, touch):
            flag = 0 if self._apply_approval_limit > 0 else 1
            set_apply_approval_limit(flag)

        set_apply_approval_limit(self._apply_approval_limit)
        item_widget1.text.SetString(800063)

    def _on_confirm(self, *args):
        lv_limit = self._level_widget.get_value()
        dan_limit = self._dan_widget.get_value()
        global_data.player.change_clan_setup(self._apply_reject_limit, self._apply_approval_limit, dan_limit, lv_limit)
        if G_IS_NA_USER:
            lang_limit = self._lang_widget.get_value()
            global_data.player.change_clan_lang(lang_limit)
        global_data.player.change_clan_badge(self._badge)
        self.close()

    def _on_click_badge_btn(self, *args):

        def badge_set_cb(pattern, frame, floor):
            self._badge = pack_badge(floor, frame, pattern)
            update_badge_show(pattern, frame, floor, self.panel.temp_crew_logo)

        from .ClanBadgeSetUI import ClanBadgeSetUI
        ClanBadgeSetUI(sel_cb=badge_set_cb, init_badge=self._badge)

    def on_finalize_panel(self):
        self.destroy_widget('_lang_widget')
        self.destroy_widget('_level_widget')
        self.destroy_widget('_dan_widget')