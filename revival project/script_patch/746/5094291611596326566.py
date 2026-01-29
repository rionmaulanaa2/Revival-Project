# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/lottery/LotteryTicketChargeUI.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
from common.const.uiconst import DIALOG_LAYER_ZORDER, UI_VKB_CLOSE
from logic.gutils.activity_utils import get_activity_cls

class LotteryTicketChargeUI(BasePanel):
    DLG_ZORDER = DIALOG_LAYER_ZORDER
    NEED_HIDE_MAIN_UI = False
    PANEL_CONFIG_NAME = ''
    UI_CLASS = ''
    ACTIVITY_TYPE = None
    UI_VKB_TYPE = UI_VKB_CLOSE
    UI_ACTION_EVENT = {'btn_close.OnClick': 'close'
       }

    @staticmethod
    def set_ui_info(template, ui_class, activity_type):
        LotteryTicketChargeUI.PANEL_CONFIG_NAME = template
        LotteryTicketChargeUI.UI_CLASS = ui_class
        LotteryTicketChargeUI.ACTIVITY_TYPE = activity_type

    def on_init_panel(self, *args, **kwargs):
        cls = get_activity_cls(LotteryTicketChargeUI.UI_CLASS)
        self.charge_widget = cls(self.panel, self.ACTIVITY_TYPE)
        self.charge_widget.on_init_panel()

    def on_finalize_panel(self):
        self.charge_widget.on_finalize_panel()
        self.charge_widget = None
        return