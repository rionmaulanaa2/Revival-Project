# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/setting_ui/SettingWidget/ParentCareSettingWidget.py
from __future__ import absolute_import
from six.moves import range
from logic.gcommon.common_utils.local_text import get_text_by_id
from .SettingWidgetBase import SettingWidgetBase

class ParentCareSettingWidget(SettingWidgetBase):

    def __init__(self, panel, parent):
        super(ParentCareSettingWidget, self).__init__(panel, parent)

    def on_init_panel(self, **kwargs):
        self.init_setting(self.panel)

    def on_exit_page(self, **kwargs):
        super(ParentCareSettingWidget, self).on_exit_page()

    def on_recover_default(self, **kwargs):
        pass

    def init_setting(self, page):
        self.panel.btn_more.btn_common_big.BindMethod('OnClick', self.on_click_btn_more)
        self.panel.btn_go.btn_common_big.BindMethod('OnClick', self.on_click_btn_go)

    def on_click_btn_more(self, *args):
        import game3d
        game3d.open_url('https://jiazhang.gm.163.com/convoy/')

    def on_click_btn_go(self, *args):
        import game3d
        game3d.open_url('https://jiazhang.gm.163.com/jz/')