# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/setting_ui/SettingPasswordUI.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
from common.const.uiconst import NORMAL_LAYER_ZORDER_2
from common.cfg import confmgr
from logic.gutils import item_utils
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.comsys.common_ui.WindowSmallBase import WindowSmallBase
from common.const import uiconst

class SettingPasswordUI(WindowSmallBase):
    TEMPLATE_NODE_NAME = 'panel'
    DLG_ZORDER = NORMAL_LAYER_ZORDER_2
    PANEL_CONFIG_NAME = 'common/open_input_password'

    def on_init_panel(self, **kwargs):
        super(SettingPasswordUI, self).on_init_panel(**kwargs)
        need_pwd = kwargs.get('need_pwd')
        max_word = kwargs.get('max_word', 20)
        input_type = kwargs.get('input_type', 0)
        place_holder = kwargs.get('place_holder', get_text_by_id(2138))
        self.init_botom(need_pwd, max_word, place_holder, input_type)
        self.init_widget(**kwargs)

    def init_botom(self, is_password, max_word, place_holder, input_type):
        import logic.comsys.common_ui.InputBox as InputBox
        self._input_box = InputBox.InputBox(self.panel.inputbox, max_length=max_word, placeholder=place_holder)
        self._input_box.setPasswordEnabled(is_password)
        self._input_box.set_rise_widget(self.panel)
        self._input_box.set_input_type(input_type)

    def init_widget(self, **kwrags):
        confirm_callback = kwrags.get('confirm_cb', None)

        @self.panel.confirm.btn_common_big.unique_callback()
        def OnClick(btn, touch):
            if confirm_callback and callable(confirm_callback):
                confirm_callback(self._input_box.get_text())

        title = kwrags.get('title', '')
        desc = kwrags.get('desc', '')
        lab_forget = kwrags.get('forget_text', '')
        forget_cb = kwrags.get('forget_cb', None)
        text = kwrags.get('text', '')
        self._input_box.set_text(text)
        self.panel.panel.lab_title.SetString(title)
        self.panel.lab_desc.SetString(desc)
        self.panel.lab_forget.SetString(lab_forget)

        @self.panel.panel.callback()
        def OnClick(btn, touch):
            if forget_cb and callable(forget_cb):
                pos = touch.getLocation()
                if self.panel.lab_forget.IsPointIn(pos):
                    forget_cb()

        return

    def on_finalize_panel(self):
        super(SettingPasswordUI, self).on_finalize_panel()
        if self._input_box:
            self._input_box.destroy()
            self._input_box = None
        return