# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/mecha_display/MechaInscriptionStoreWidget.py
from __future__ import absolute_import
from __future__ import print_function
import render
from common.cfg import confmgr
from common.uisys.basepanel import BasePanel
from common.const.uiconst import UI_TYPE_MESSAGE
from common.const.uiconst import NORMAL_LAYER_ZORDER_2
EXCEPT_HIDE_UI_LIST = []
from common.const import uiconst
from logic.gutils import item_utils, inscription_utils
import logic.gcommon.item.item_const as item_const
from logic.comsys.common_ui.ItemNumBtnWidget import ItemNumBtnWidget
from logic.gutils import mall_utils
from logic.comsys.common_ui.WindowCommonComponent import WindowCommonComponent
from logic.gcommon.cdata.mecha_component_data import COMPONENT_ATK, COMPONENT_DEFENSE
from logic.gcommon.item.item_const import INSCR_ATK, INSCR_FAULT_TOL, INSCR_SURVIVAL, INSCR_MOB, INSCR_RECOVER, INSCR_TACTICAL
from logic.gutils.InfiniteScrollWidget import InfiniteScrollWidget
from logic.comsys.mecha_display.InscriptionUpgradeUI import InscriptionLevelUpgradeUI
from logic.gcommon.cdata.mecha_component_data import get_component_list_by_type, get_component_all_list
from logic.comsys.mall_ui.PriceUIWidget import PriceUIWidget
import logic.gcommon.const as gconst
from common.uisys.BaseUIWidget import BaseUIWidget
from logic.gutils.template_utils import init_common_choose_list_2
from logic.gutils.new_template_utils import init_top_tab_list
from logic.client.const import mall_const
from logic.gutils import template_utils
GIFT_BOX_GOODS_ID_1 = '50400053'
GIFT_BOX_GOODS_ID_2 = '50400055'

class MechaInscriptionStoreWidget(BaseUIWidget):

    def __init__(self, parent, panel, mecha_type):
        self.global_events = {'player_item_update_event_with_id': self.on_buy_good_success,
           'player_money_info_update_event': self._on_player_info_update
           }
        super(MechaInscriptionStoreWidget, self).__init__(parent, panel, mecha_type)
        self.init_ui_show()

    def init_ui_show(self):
        self.init_package_one()
        self.init_package_two()
        from common.utils.redpoint_check_func import check_inscription_store_red_point
        if check_inscription_store_red_point():
            import time
            achi_mgr = global_data.achi_mgr
            if achi_mgr:
                achi_mgr.set_cur_user_archive_data('inscription_store_open_time', time.time())
            global_data.emgr.mecha_component_store_rp_event.emit()

    def init_package_one(self):
        from logic.gutils import mall_utils
        goods_id = GIFT_BOX_GOODS_ID_1
        template_utils.init_price_view(self.panel.btn_buy_1.temp_price, goods_id, mall_const.DARK_PRICE_COLOR)
        is_can_buy = mall_utils.check_payment_by_goods_id(goods_id, pay_tip=False)
        print(mall_utils.get_mall_item_price(goods_id))
        item_no = mall_utils.get_goods_item_no(goods_id)
        self.panel.btn_buy_1.SetText('')

        @self.panel.btn_buy_1.callback()
        def OnClick(btn, touch):
            is_can_buy = mall_utils.check_payment_by_goods_id(goods_id, pay_tip=False)
            if is_can_buy:
                from logic.comsys.mall_ui.BuyConfirmUIInterface import groceries_buy_confirmUI
                groceries_buy_confirmUI(goods_id)
            elif item_utils.can_jump_to_ui(item_no):
                item_utils.jump_to_ui(item_no)

    def on_switch_to_mecha_type(self, mecha_type):
        pass

    def init_package_two(self):
        goods_id = GIFT_BOX_GOODS_ID_2
        template_utils.init_price_view(self.panel.btn_buy_2.temp_price, goods_id, mall_const.DARK_PRICE_COLOR)

        @self.panel.btn_buy_2.callback()
        def OnClick(btn, touch):
            from logic.comsys.mall_ui.BuyConfirmUIInterface import groceries_buy_confirmUI
            groceries_buy_confirmUI(goods_id)

    def destroy(self):
        super(MechaInscriptionStoreWidget, self).destroy()

    def refresh_ui_show(self):
        self.init_ui_show()

    def on_buy_good_success(self, item_no):
        self.refresh_ui_show()

    def _on_player_info_update(self, *args):
        self.refresh_ui_show()