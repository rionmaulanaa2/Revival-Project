# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/mall_ui/PCScanPaySelectUI.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
from common.const.uiconst import SECOND_CONFIRM_LAYER, UI_TYPE_CONFIRM
from common.const import uiconst

class PCScanPaySelectUI(BasePanel):
    PANEL_CONFIG_NAME = 'common/pay_pc'
    DLG_ZORDER = SECOND_CONFIRM_LAYER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    UI_TYPE = UI_TYPE_CONFIRM
    IS_FULLSCREEN = True
    MOUSE_CURSOR_TRIGGER_SHOW = True
    UI_ACTION_EVENT = {'container_node.temp_btn_1.btn_common_big.OnClick': 'choose_ios',
       'container_node.temp_btn_2.btn_common_big.OnClick': 'choose_android',
       'container_node.btn_close.OnClick': 'click_close'
       }

    def on_init_panel(self, **kwargs):
        self.init_widget(**kwargs)

    def init_widget(self, **kwargs):
        self.on_confirm = kwargs.get('on_confirm', None)
        return

    def choose_ios(self, *args):
        self.do_confirm('ios')

    def choose_android(self, *args):
        self.do_confirm('ad')

    def click_close(self, *args):
        self.do_confirm(None)
        return

    def do_confirm(self, pay_type=None):
        self.close()
        if self.on_confirm:
            self.on_confirm(pay_type)
            self.on_confirm = None
        return