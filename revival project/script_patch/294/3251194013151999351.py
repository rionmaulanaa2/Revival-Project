# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/setting_ui/LanguageSettingUI.py
from __future__ import absolute_import
import six_ex
from common.const.uiconst import NORMAL_LAYER_ZORDER
from common.uisys.basepanel import BasePanel
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gcommon.common_const.lang_data import code_2_showname, lang_data, LANG_CN, LANG_KO
from logic.gcommon.common_const.voice_lang_data import voice_lang_data, VOICE_JA
from logic.gcommon.common_utils.local_text import get_cur_text_lang, get_cur_voice_lang
from logic.comsys.common_ui.NormalConfirmUI import SecondConfirmDlg2
from logic.comsys.common_ui.WindowMediumBase import WindowMediumBase
from common.uisys.font_utils import GetLowMemFontName
from common.cfg import confmgr

class LanguageSettingUI(WindowMediumBase):
    PANEL_CONFIG_NAME = 'setting/setting_language'
    DLG_ZORDER = NORMAL_LAYER_ZORDER
    TEMPLATE_NODE_NAME = 'pnl_content'
    UI_ACTION_EVENT = {'pnl_close.OnClick': 'on_click_close_btn'
       }

    def on_init_panel(self):
        super(LanguageSettingUI, self).on_init_panel()
        self._selected_lang_code = None
        self.init_language_list()
        return

    def init_language_list(self):
        show_lang_list = []
        support_lang_code_list = six_ex.keys(code_2_showname)
        for lang_id in support_lang_code_list:
            is_enable = lang_data.get(lang_id, {}).get('cLangEnable', False)
            if is_enable:
                show_lang_list.append(lang_id)

        self.panel.lv_lang_list.SetInitCount(len(show_lang_list))
        allItems = self.panel.lv_lang_list.GetAllItem()
        cur_code = get_cur_text_lang()
        self._selected_lang_code = cur_code
        for i, item in enumerate(allItems):
            lang_code = show_lang_list[i]
            lang_name = code_2_showname.get(lang_code, '')
            item.tf_lang.SetString(lang_name)
            font_name = confmgr.get('lang_conf', str(lang_code), default={}).get('bShowFont', 'gui/fonts/fzdys.ttf')
            if font_name:
                item.tf_lang.setFontName(GetLowMemFontName(font_name))
            item.setTag(lang_code)
            if cur_code == lang_code:
                item.btn_language.SetSelect(True)

            @item.btn_language.callback()
            def OnClick(btn, touch, lang_code=lang_code):
                if lang_code != self._selected_lang_code:
                    last_item = self.panel.lv_lang_list.GetItemByTag(self._selected_lang_code)
                    if last_item:
                        last_item.btn_language.SetSelect(False)
                    new_item = self.panel.lv_lang_list.GetItemByTag(lang_code)
                    if new_item:
                        new_item.btn_language.SetSelect(True)
                    self._selected_lang_code = lang_code
                    self.refresh_voice_list_text()

        if hasattr(self.panel.temp_btn_confirm, 'btn_common') and self.panel.temp_btn_confirm.btn_common:
            click_btn = self.panel.temp_btn_confirm.btn_common
        elif hasattr(self.panel.temp_btn_confirm, 'btn_major') and self.panel.temp_btn_confirm.btn_major:
            click_btn = self.panel.temp_btn_confirm.btn_major
        else:
            click_btn = None
        if click_btn:

            @click_btn.callback()
            def OnClick(btn, touch):
                global_data.emgr.should_login_channel_event.emit()
                if self._selected_lang_code == get_cur_text_lang():
                    self.close()
                    return

                def cb():
                    self.switch_to_lang()
                    global_data.emgr.language_select_event.emit()

                player = global_data.player
                if player and not player.in_local_battle():
                    SecondConfirmDlg2().confirm(content=get_text_by_id(3107), confirm_text=get_text_local_content(3108), confirm_callback=cb)
                else:
                    self.close()
                    cb()

        return

    def refresh_voice_list_text(self):
        pass

    def switch_to_lang(self):
        global_data.ui_mgr.change_lang(self._selected_lang_code, get_cur_voice_lang())

    def on_click_close_btn(self, *args):
        global_data.emgr.should_login_channel_event.emit()
        self.close()

    def hide_close_btn(self):
        self.panel.pnl_content.btn_close.setVisible(False)