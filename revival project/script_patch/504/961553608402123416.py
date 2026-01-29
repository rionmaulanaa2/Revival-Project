# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/common_ui/NormalInputUI.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
from common.const.uiconst import NORMAL_LAYER_ZORDER_2
from common.cfg import confmgr
from logic.gutils import item_utils
from logic.gcommon.common_utils.local_text import get_text_by_id
from common.const import uiconst

class NormalInputUI(BasePanel):
    DLG_ZORDER = NORMAL_LAYER_ZORDER_2
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    PANEL_CONFIG_NAME = 'common/normal_input'

    def on_init_panel(self, **kwargs):
        self.init_widget(**kwargs)
        need_pwd = kwargs.get('need_pwd')
        max_word = kwargs.get('max_word', 20)
        place_holder = kwargs.get('place_holder', get_text_by_id(2138))
        self.init_botom(need_pwd, max_word, place_holder)

    def init_botom(self, is_password, max_word, place_holder):
        import logic.comsys.common_ui.InputBox as InputBox
        self._input_box = InputBox.InputBox(self.panel.input_box, max_length=max_word, placeholder=place_holder)
        self._input_box.setPasswordEnabled(is_password)
        self._input_box.set_rise_widget(self.panel)

    def init_widget(self, **kwrags):
        confirm_callback = kwrags.get('confirm_cb', None)
        cancel_callback = kwrags.get('cancel_cb', None)

        @self.panel.confirm.unique_callback()
        def OnClick(btn, touch):
            if confirm_callback and callable(confirm_callback):
                confirm_callback(self._input_box.get_text())
            self.close()

        @self.panel.cancle.unique_callback()
        def OnClick(btn, touch):
            if cancel_callback and callable(cancel_callback):
                cancel_callback(self._input_box.get_text())
            self.close()

        return

    def on_finalize_panel(self):
        if self._input_box:
            self._input_box.destroy()
            self._input_box = None
        return