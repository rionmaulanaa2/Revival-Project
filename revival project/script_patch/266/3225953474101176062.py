# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/clan/ClanLangSettingWidget.py
from __future__ import absolute_import
import six_ex
from common.uisys.BaseUIWidget import BaseUIWidget

class ClanLangSettingWidget(BaseUIWidget):

    def get_value(self):
        return self._apply_lang_limit

    def __init__(self, panel_cls, ui_panel, lang_limit, select_cb=None, reverse=False):
        super(ClanLangSettingWidget, self).__init__(panel_cls, ui_panel)
        self._apply_lang_limit = lang_limit
        self._select_cb = select_cb
        self._reverse = reverse
        self._init_panel()

    def _init_panel(self):

        @self.panel.unique_callback()
        def OnClick(btn, touch):
            self.reverse_lang_list_show()

        from common.cfg import confmgr
        from logic.gcommon.common_const.lang_data import code_2_showname
        self.panel.language_list.setVisible(False)
        self.panel.img_icon.setScaleY(1)
        lang_name = code_2_showname.get(self._apply_lang_limit, get_text_by_id(860016))
        lang_font = confmgr.get('lang_conf', str(self._apply_lang_limit), default={}).get('bShowFont', 'gui/fonts/fzdys.ttf')
        self.panel.SetText(lang_name, font_name=lang_font)
        lang_codes = six_ex.keys(code_2_showname)
        lang_codes.sort()
        lang_limit = [{'name': 860016,'val': -1,'font': None}]
        for lang_code in lang_codes:
            lang_name = code_2_showname.get(lang_code)
            lang_font = confmgr.get('lang_conf', str(lang_code), default={}).get('bShowFont', 'gui/fonts/fzdys.ttf')
            lang_limit.append({'name': lang_name,'val': lang_code,'font': lang_font})

        def callback(index):
            info = lang_limit[index]
            self._apply_lang_limit = info['val']
            self.panel.SetText(info['name'], font_name=info.get('font', None))
            if self.panel.language_list.isVisible():
                self.reverse_lang_list_show()
            if self._select_cb:
                self._select_cb()
            return

        def close_cb(*args):
            self.panel.img_icon.setScaleY(1)

        from logic.gutils.template_utils import init_common_choose_list
        init_common_choose_list(self.panel.language_list, lang_limit, callback, max_height=350, close_cb=close_cb, reverse=self._reverse)
        return

    def reverse_lang_list_show(self):
        now_vis = self.panel.language_list.isVisible()
        self.panel.language_list.setVisible(not now_vis)
        self.panel.img_icon.setScaleY(1 if now_vis else -1)