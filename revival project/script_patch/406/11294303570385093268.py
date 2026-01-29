# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/common_ui/BagUseConfirm.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
import time
from cocosui import cc, ccui, ccs
import common.const.uiconst
from common.const.property_const import *
import common.utilities
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gutils.item_utils import get_lobby_item_name, get_lobby_item_desc, init_lobby_bag_item
from logic.comsys.lobby.LobbyBagRecycleUI import ItemNumBtnWidget
from logic.comsys.common_ui.WindowSmallBase import WindowSmallBase

class BagUseConfirm(WindowSmallBase):
    PANEL_CONFIG_NAME = 'bag/bag_use_confirm'
    TEMPLATE_NODE_NAME = 'temp_bar'
    DLG_ZORDER = common.const.uiconst.NORMAL_LAYER_ZORDER_1
    UI_ACTION_EVENT = {'btn_use.btn_common.OnClick': 'on_use',
       'input_quantity.btn_minus.OnClick': 'on_minus',
       'input_quantity.btn_plus.OnClick': 'on_plus',
       'input_quantity.btn_increase_max.OnClick': 'on_max'
       }

    def on_init_panel(self, *args, **kargs):
        super(BagUseConfirm, self).on_init_panel()
        self._cur_count = 1
        self._item_data = {}

    def set_use_params(self, item_data, *args, **kwargs):
        self._item_data = item_data
        self._cur_count = 1
        item_no = item_data.get('item_no', None)
        self._all_count = item_data.get('quantity', 1)
        self.panel.lab_name.SetString(get_lobby_item_name(item_no))
        self.panel.lab_details.SetString(get_lobby_item_desc(item_no))
        self.refresh()
        init_lobby_bag_item(self.panel.temp_item, self._item_data)
        return

    def on_close(self, *args):
        self.close()

    def on_use(self, *args):
        global_data.player.use_item(self._item_data['id'], self._cur_count)
        self.close()

    def on_minus(self, *args):
        self._cur_count -= 1
        if self._cur_count < 1:
            self._cur_count = 1
        self.refresh()

    def on_plus(self, *args):
        self._cur_count += 1
        if self._cur_count > self._all_count:
            self._cur_count = self._all_count
        self.refresh()

    def on_max(self, *args):
        self._cur_count = self._all_count
        self.refresh()

    def refresh(self, *args):
        self.panel.input_quantity.lab_num.SetString('%d/%d' % (self._cur_count, self._all_count))