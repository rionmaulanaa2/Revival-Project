# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/setting_ui/UnderageSettingUI.py
from __future__ import absolute_import
from six.moves import range
from common.const.uiconst import DIALOG_LAYER_ZORDER
from logic.comsys.common_ui.WindowMediumBase import WindowMediumBase
from logic.comsys.setting_ui.SettingWidget.BaseSettingWidget import FAQ_TITLE_ID
from logic.gutils.template_utils import init_radio_group, init_radio_group_new, attach_radio_group_data, set_radio_group_item_select, set_radio_group_item_select_new, set_radio_group_enable_state, init_checkbox_group, attach_checkbox_group_data, set_check_box_group_item_select, set_radio_group_enable_state_new
import cc
from logic.gutils.dress_utils import default_shadow_path
from logic.gcommon.common_const import ui_operation_const as uoc
from logic.gutils.setting_utils import init_one_setting_list_choose
FAQ_PRIVILIGE_TITLE = 2293

class UnderageSettingUI(WindowMediumBase):
    PANEL_CONFIG_NAME = 'setting/i_setting_window_minor'
    DLG_ZORDER = DIALOG_LAYER_ZORDER
    UI_ACTION_EVENT = {'nd_window.btn_close.OnClick': 'on_click_close_btn'
       }

    def on_init_panel(self):
        super(UnderageSettingUI, self).on_init_panel()
        self.confirm_cb = None
        self.cancel_cb = None
        self.panel.nd_window.lab_title.SetString(get_text_by_id(610196))
        self.init_underage_setting()
        return

    def on_finalize_panel(self):
        super(UnderageSettingUI, self).on_finalize_panel()
        self.confirm_cb = None
        self.cancel_cb = None
        return

    def init_underage_setting(self):
        if not global_data.player:
            return

        def select_cb(key, value):
            global_data.emgr.update_underage_sub_setting.emit(key, value)

        old_value_dict = {}
        setting_keys = [
         uoc.TEAM_ONLY_FRIEND_KEY, uoc.SHIELD_STRANGER_MSG_KEY, uoc.MALL_RECOMMEND]
        for key in setting_keys:
            old_value_dict[key] = global_data.player.get_setting_2(key)

        init_one_setting_list_choose(self.panel.list_tab, 0, uoc.TEAM_ONLY_FRIEND_KEY, select_cb, True)
        init_one_setting_list_choose(self.panel.list_tab, 1, uoc.SHIELD_STRANGER_MSG_KEY, select_cb, True)
        init_one_setting_list_choose(self.panel.list_tab, 2, uoc.MALL_RECOMMEND, select_cb, True)

        @self.panel.temp_btn_2.btn_common_big.callback()
        def OnClick(btn, touch):
            self.confirm_cb and self.confirm_cb()
            self.close()

        @self.panel.temp_btn_1.btn_common_big.callback()
        def OnClick(btn, touch):
            for key in setting_keys:
                global_data.player and global_data.player.write_setting_2(key, old_value_dict[key], True)

            self.cancel_cb and self.cancel_cb()
            self.close()

    def on_click_close_btn(self, touch, btn):
        self.close()

    def set_callback(self, confirm_cb, cancel_cb):
        self.confirm_cb = confirm_cb
        self.cancel_cb = cancel_cb