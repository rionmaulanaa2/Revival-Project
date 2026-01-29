# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/mecha_display/MechaInscriptionChangeUI.py
from __future__ import absolute_import
import render
from common.cfg import confmgr
from common.uisys.basepanel import BasePanel
from common.const.uiconst import UI_TYPE_MESSAGE
from common.const.uiconst import NORMAL_LAYER_ZORDER_2
from logic.gutils import inscription_utils
EXCEPT_HIDE_UI_LIST = []
from common.const import uiconst

class MechaInscriptionChangeUI(BasePanel):
    PANEL_CONFIG_NAME = 'mech_display/inscription/inscription_change_result'
    DLG_ZORDER = NORMAL_LAYER_ZORDER_2
    UI_VKB_TYPE = uiconst.UI_VKB_CLOSE
    UI_ACTION_EVENT = {}
    GLOBAL_EVENT = {}

    def on_init_panel(self):
        pass

    def show_attr_change(self, attr_change_list):
        from common.utils.cocos_utils import ccc3FromHex, ccp, CCRect, CCSizeZero, ccc4FromHex
        import math
        self.panel.list_item.SetInitCount(len(attr_change_list))
        for idx, attr_change in enumerate(attr_change_list):
            attr_name, attr_value_change, attr_sign = attr_change
            ui_item = self.panel.list_item.GetItem(idx)
            if ui_item:
                ui_item.lab_rate.AddReordedNodeInfo('color')
                ui_item.lab_name.SetString(attr_name)
                ui_item.lab_rate.SetString(inscription_utils.format_buff_value(attr_value_change))
                if math.copysign(1, attr_value_change) == attr_sign:
                    ui_item.lab_rate.SetColor(16733945)
                    ui_item.lab_rate.EnableOutline(ccc4FromHex(4659808), 1)
                    ui_item.lab_rate.EnableShadow(7685776, 255, {'width': 2,'height': -2})
                else:
                    ui_item.lab_rate.disableEffect()
                    ui_item.lab_rate.ReConfColor()

        self.panel.PlayAnimation('appear')
        self.panel.SetTimeOut(self.panel.GetAnimationMaxRunTime('appear'), self.close)

    def on_finalize_panel(self):
        pass