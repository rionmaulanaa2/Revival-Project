# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/setting_ui/SettingWidget/SettingWidgetBase.py
from __future__ import absolute_import
from logic.comsys.battle.Death.TabBaseWidget import TabBaseWidget

class SettingWidgetBase(TabBaseWidget):

    def __init__(self, panel, parent):
        self.parent = parent
        self._add_reference_count = False
        super(SettingWidgetBase, self).__init__(panel)
        if self.panel.getReferenceCount() <= 1:
            self._add_reference_count = True
            self.panel.retain()

    def set_tab_text_id(self, tab_text_id):
        self.tab_text_id = tab_text_id

    def on_resolution_changed(self):
        pass

    def on_init_panel(self, **kwargs):
        pass

    def has_apply_btn(self):
        return False

    def destroy(self):
        self.on_before_destroy()
        if self._add_reference_count:
            if self.panel:
                self.panel.release()
                self._add_reference_count = False
        super(SettingWidgetBase, self).destroy()

    def on_enter_page(self, **kwargs):
        self.show()

    def on_exit_page(self, **kwargs):
        self.hide()

    def on_recover_default(self, **kwargs):
        pass

    def on_apply_all(self, **kwargs):
        pass

    def get_page_panel(self):
        return self.panel

    def on_before_destroy(self, **kwargs):
        pass

    def on_sync_to_server(self, **kwargs):
        pass

    def should_btn_sync_server_enabled(self):
        return False

    def _refresh_sync_server_btn_enable(self):
        if self.parent:
            self.parent.refresh_sync_server_btn_enable()

    def _set_apply_btn_enabled(self, enable):
        if self.parent:
            self.parent.set_apply_btn_enabled(enable)

    def _set_big_func_btn_enabled(self, btn_name, enable):
        btn = self
        if self.parent:
            btn = self.parent.get_big_func_btn(btn_name)
            if btn:
                btn.SetEnable(enable)