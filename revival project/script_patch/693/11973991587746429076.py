# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/common_ui/ItemPreviewUI.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
import common.const.uiconst

class ItemPreviewUI(BasePanel):
    PANEL_CONFIG_NAME = 'activity/activity_202206/bp/open_window_bp_skin'
    DLG_ZORDER = common.const.uiconst.DIALOG_LAYER_ZORDER_2
    UI_VKB_TYPE = common.const.uiconst.UI_VKB_CLOSE
    UI_ACTION_EVENT = {'temp_window.btn_close.OnClick': 'close'
       }

    def on_init_panel(self, *args, **kwargs):
        title = kwargs.get('title', '')
        item_list = kwargs.get('item_list', [])
        self.set_content(title, item_list)

    def set_content(self, title, item_list):
        self.panel.temp_window.lab_title.SetString(title)
        from logic.gutils.template_utils import init_mall_item
        self.panel.list_item.SetInitCount(len(item_list))
        for i, item_id in enumerate(item_list):
            item_widget = self.panel.list_item.GetItem(i)
            init_mall_item(item_widget, str(item_id))
            item_widget.nd_price.setVisible(False)