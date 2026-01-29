# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/pve/PVEMainUIWidgetUI/PVEKeyBuyUI.py
from __future__ import absolute_import
from common.const.uiconst import DIALOG_LAYER_BAN_ZORDER, UI_VKB_CLOSE
from logic.gcommon.item.item_const import ITEM_NO_PVE_KEY
from logic.comsys.common_ui.WindowSmallBase import WindowSmallBase
from logic.comsys.mall_ui.PriceUIWidget import PriceUIWidget
from logic.gcommon.const import SHOP_PAYMENT_YUANBAO, SHOP_PAYMENT_DIAMON, SHOP_PAYMENT_ITEM_PVE_KEY
from logic.gutils.template_utils import init_price_view
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gutils import mall_utils
from logic.client.const.mall_const import DARK_PRICE_COLOR
from logic.gcommon.common_const.pve_const import MAX_AUTO_RECEIVE_PVE_KEY_COUNT
from logic.comsys.charge_ui.ExchangeUI import ExchangeUI
import logic.gcommon.time_utility as tutils
from common.cfg import confmgr
import cc
PVE_KEY_DIAMON_GOODS_ID = '700200207'
PVE_KEY_YUANBAO_GOODS_ID = '700200208'
PVE_KEY_ITEM_PATH = 'gui/ui_res_2/item/groceries/50101015.png'

class PVEKeyBuyUI(WindowSmallBase):
    PANEL_CONFIG_NAME = 'pve/select_level_new/open_select_level_buy'
    DLG_ZORDER = DIALOG_LAYER_BAN_ZORDER
    UI_VKB_TYPE = UI_VKB_CLOSE
    TEMPLATE_NODE_NAME = 'pnl_content'
    UI_ACTION_EVENT = {}

    def on_init_panel(self):
        super(PVEKeyBuyUI, self).on_init_panel()
        self.process_event(True)
        self._init_params()
        self._init_ui_events()
        self._init_money_widget()
        self._init_lab_got()
        self._init_list_item()

    def _init_params(self):
        self._price_top_widget = None
        self._list_item = None
        self._time_label = None
        self._action = None
        return

    def _init_ui_events(self):

        @self.panel.btn_describe.callback()
        def OnClick(btn, touch):
            dlg = global_data.ui_mgr.show_ui('GameRuleDescUI', 'logic.comsys.common_ui')
            dlg.set_show_rule(447, 448)

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'player_item_update_event': self.player_item_update_event,
           'buy_good_success': self.player_item_update_event
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def player_item_update_event(self):
        self._init_money_widget()
        self._init_list_item()
        self._init_lab_got()

    def _init_money_widget--- This code section failed: ---

  71       0  LOAD_FAST             0  'self'
           3  LOAD_ATTR             0  '_price_top_widget'
           6  POP_JUMP_IF_TRUE     67  'to 67'

  72       9  LOAD_GLOBAL           1  'PriceUIWidget'
          12  LOAD_GLOBAL           1  'PriceUIWidget'
          15  LOAD_FAST             0  'self'
          18  LOAD_ATTR             2  'panel'
          21  LOAD_ATTR             3  'list_money'
          24  LOAD_CONST            2  'pnl_title'
          27  LOAD_GLOBAL           4  'False'
          30  CALL_FUNCTION_513   513 
          33  LOAD_FAST             0  'self'
          36  STORE_ATTR            0  '_price_top_widget'

  73      39  LOAD_FAST             0  'self'
          42  LOAD_ATTR             0  '_price_top_widget'
          45  LOAD_ATTR             5  'show_money_types'
          48  LOAD_GLOBAL           6  'SHOP_PAYMENT_YUANBAO'
          51  LOAD_GLOBAL           7  'SHOP_PAYMENT_DIAMON'
          54  LOAD_GLOBAL           8  'SHOP_PAYMENT_ITEM_PVE_KEY'
          57  BUILD_LIST_3          3 
          60  CALL_FUNCTION_1       1 
          63  POP_TOP          
          64  JUMP_FORWARD         13  'to 80'

  75      67  LOAD_FAST             0  'self'
          70  LOAD_ATTR             0  '_price_top_widget'
          73  LOAD_ATTR             9  '_on_player_info_update'
          76  CALL_FUNCTION_0       0 
          79  POP_TOP          
        80_0  COME_FROM                '64'

Parse error at or near `CALL_FUNCTION_513' instruction at offset 30

    def _init_lab_got(self):
        item_amount = global_data.player.get_item_num_by_no(ITEM_NO_PVE_KEY)
        self.panel.lab_got.setString(get_text_by_id(406).format(item_amount))

    def _init_list_item(self):
        self._list_item = self.panel.list_item
        self._add_money_buy_item(0, PVE_KEY_YUANBAO_GOODS_ID)
        self._add_money_buy_item(1, PVE_KEY_DIAMON_GOODS_ID)
        item = self._list_item.GetItem(2)
        btn_get = item.btn_get
        btn_get.SetText(get_text_by_id(402))
        btn_get.temp_price.setVisible(False)
        item.img_item.SetDisplayFrameByPath('', PVE_KEY_ITEM_PATH)
        item.lab_num.setString('x1')
        self._time_label = item.bar_tips.lab_tips
        self.add_action()

    def _add_money_buy_item(self, index, goods_id):
        item = self._list_item.GetItem(index)
        conf = confmgr.get('mall_config', goods_id)
        item.img_item.SetDisplayFrameByPath('', PVE_KEY_ITEM_PATH)
        item.lab_num.setString('x{}'.format(conf.get('num', 1)))
        self._check_limit(conf, goods_id, item.bar_tips.lab_tips)
        btn_get = item.btn_get
        btn_get.SetText('')
        init_price_view(btn_get.temp_price, goods_id, DARK_PRICE_COLOR)

        @btn_get.unique_callback()
        def OnClick(btn, touch, goods_id=goods_id):
            from_payment = SHOP_PAYMENT_DIAMON if goods_id == PVE_KEY_DIAMON_GOODS_ID else SHOP_PAYMENT_YUANBAO
            ExchangeUI(from_payment=from_payment, to_payment=SHOP_PAYMENT_ITEM_PVE_KEY, buy_goods_id=goods_id, keyboard_for_from_payment=False, default_value=20)

    def _check_limit(self, conf, goods_id, lab_tips):
        max_buy_num_per_day = conf.get('max_buy_num_per_day')
        if max_buy_num_per_day:
            _, _, num_info = mall_utils.buy_num_limite_by_day(goods_id)
            remain_num, max_num = num_info
            lab_tips.setString(get_text_by_id(401).format(int(remain_num)))
        else:
            lab_tips.setString(get_text_by_id(400))

    def add_action(self):
        self.clear_action()
        if global_data.player.get_next_free_add_key_ts() == -1:
            self._time_label.setString(get_text_by_id(435))
            return
        self._action = self.panel.runAction(cc.RepeatForever.create(cc.Sequence.create([
         cc.CallFunc.create(self.set_time_label),
         cc.DelayTime.create(1)])))

    def set_time_label(self):
        if not global_data.player:
            return
        next_ts = global_data.player.get_next_free_add_key_ts()
        if next_ts == -1:
            self.clear_action()
            self._time_label.setString(get_text_by_id(435))
            return
        remain_time = int(next_ts - tutils.get_server_time())
        time_str = tutils.get_delta_time_str(remain_time)
        self._time_label.setString(time_str)

    def clear_action(self):
        if self._action is not None:
            self.panel.stopAction(self._action)
            self._action = None
        return

    def on_finalize_panel(self):
        self.process_event(False)
        self.clear_action()
        if self._price_top_widget:
            self._price_top_widget.destroy()
            self._price_top_widget = None
        return