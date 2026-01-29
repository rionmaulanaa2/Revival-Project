# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/lobby/LobbyBagUseUI.py
from __future__ import absolute_import
import cc
import collision
from common.uisys.basepanel import BasePanel
from common.utils.cocos_utils import neox_pos_to_cocos, cocos_pos_to_neox
from common.const.uiconst import NORMAL_LAYER_ZORDER, BG_ZORDER
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.comsys.login.LoginSetting import LoginSetting
from logic.gutils import role_head_utils
from common.platform.dctool import interface
from logic.gutils.item_utils import get_lobby_item_pic_by_item_no, get_lobby_item_name, get_lobby_item_desc, init_lobby_bag_item
from common.cfg import confmgr
from logic.comsys.common_ui.ItemNumBtnWidget import ItemNumBtnWidget
from logic.comsys.common_ui.WindowSmallBase import WindowSmallBase

class LobbyBagUseUI(WindowSmallBase):
    PANEL_CONFIG_NAME = 'bag/bag_use_confirm'
    DLG_ZORDER = NORMAL_LAYER_ZORDER
    TEMPLATE_NODE_NAME = 'temp_bar'
    UI_ACTION_EVENT = {'btn_use.btn_common.OnClick': 'on_click_use_btn'
       }

    def on_init_panel(self, *args, **kwargs):
        super(LobbyBagUseUI, self).on_init_panel()
        self.item_data = {}
        self._cur_sel_num = 0
        self.ItemNumBtnWidget = ItemNumBtnWidget(self.panel.temp_input_quantity)

    def on_finalize_panel(self):
        self.destroy_widget('ItemNumBtnWidget')

    def on_click_close_ui(self, *args):
        self.close()

    def on_click_recycle_btn(self, btn, touch):
        pass

    def init_use_item(self, item_data):
        content_nd = self.panel.nd_content
        item_no = item_data.get('item_no', None)
        quantity = item_data.get('quantity', 1)
        self.item_data = item_data
        init_lobby_bag_item(self.panel.temp_item, item_data)
        content_nd.lab_name.SetString(get_lobby_item_name(item_no))
        content_nd.lab_details.SetString(get_lobby_item_desc(item_no))
        self.ItemNumBtnWidget.init_item(self.item_data, self.on_num_changed)
        self.set_good_num(1)
        return

    def on_num_changed(self, item_data, num):
        self.set_good_num(num)
        self.update_button_show()

    def set_good_num(self, num):
        self._cur_sel_num = num
        quantity = self.item_data.get('quantity', 1)
        self.panel.temp_input_quantity.lab_num.SetString(str(num) + '/' + str(quantity))

    def update_button_show(self):
        pass

    def cal_price(self, good_data, num):
        diamond_consumed = good_data.get('diamond_consumed', 0)
        gold_consumed = good_data.get('gold_consumed', 0)
        return {'diamond_consumed': int(diamond_consumed * num),'gold_consumed': int(gold_consumed * num)}