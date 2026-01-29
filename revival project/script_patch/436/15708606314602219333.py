# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle_pass/SmallBpLevelBuyWidget.py
from __future__ import absolute_import
from six.moves import range
from common.uisys.BaseUIWidget import BaseUIWidget
from logic.client.const.mall_const import DARK_PRICE_COLOR
from logic.gutils import item_utils
from logic.gutils.mall_utils import check_yuanbao
from logic.gutils.template_utils import init_price_template
from logic.gutils.template_utils import init_setting_slider3
from logic.gutils.template_utils import init_tempate_mall_i_item
from logic.gcommon.cdata import secret_order_conf
from logic.gcommon.item.item_const import RARE_DEGREE_4
from logic.gcommon.common_const.battlepass_const import SEASON_CARD

class SmallBpLevelBuyWidget(BaseUIWidget):

    def __init__(self, parent_ui, panel, close_call_back):
        self.global_events = {'small_bp_update_lv': self.init_show,
           'player_money_info_update_event': self.update_price
           }
        self._close_call_back = close_call_back
        super(SmallBpLevelBuyWidget, self).__init__(parent_ui, panel)
        self.init_show()

    def init_show(self, *args):
        sp_lv = global_data.player.secretorder_lv
        self._now_lv = sp_lv
        self._des_lv = sp_lv
        self._last_des_lv = sp_lv
        self._item_no_to_item = {}
        self._rare_to_idx = {}
        self._max_level = len(secret_order_conf.lv_reward_data)
        self.panel.list_buy_award.DeleteAllSubItem()
        self._init_price()
        self._update_preview(1)
        self._init_ui_event()
        self.panel.PlayAnimation('appear')
        init_setting_slider3(self.panel.temp_slider, 1, self._max_level - self._now_lv, 608021, self._update_preview)

    def _init_price(self):
        from logic.gcommon.const import SHOP_PAYMENT_YUANBAO
        price_info = {'original_price': secret_order_conf.YUANBAO_TO_UPGRADE,
           'discount_price': None,
           'goods_payment': SHOP_PAYMENT_YUANBAO
           }
        price_node = self.panel.temp_price_special
        init_price_template(price_info, price_node, DARK_PRICE_COLOR)
        return

    def _init_ui_event(self):

        def _on_click_buy(*args):
            total_price = secret_order_conf.YUANBAO_TO_UPGRADE * (self._des_lv - self._now_lv)
            if check_yuanbao(total_price, True):
                global_data.player.activate_small_bp_lv(str(self._des_lv - self._now_lv))

        self.panel.btn_close.BindMethod('OnClick', self.on_click_close)
        self.panel.btn_buy_level.btn_major.BindMethod('OnClick', _on_click_buy)

    def on_click_close(self, *args):
        if self._close_call_back:
            self._close_call_back(False)
        self._close_call_back = None
        self.destroy()
        return

    def _update_preview(self, add_lv):
        self._des_lv = add_lv + self._now_lv
        if self._des_lv > self._max_level:
            self._des_lv = self._max_level
        if self._des_lv < self._now_lv + 1:
            self._des_lv = self._now_lv + 1
        self.panel.lab_buy_title.SetString('LV.{}'.format(self._des_lv))
        self.panel.lab_level_now.SetString('LV.{}'.format(self._now_lv))
        self.update_price()
        if self._des_lv > self._last_des_lv:
            XRANGE_END = self._des_lv
            XRANGE_BEG = self._last_des_lv
            SHOW = True
        else:
            XRANGE_END = self._last_des_lv
            XRANGE_BEG = self._des_lv
            SHOW = False
        has_buy_card = global_data.player.has_buy_higher_small_bp()
        from common.cfg import confmgr
        for lv in range(XRANGE_BEG + 1, XRANGE_END + 1):
            reward_id_lst = []
            reward_list = []
            low_reward_id, high_reward_id = secret_order_conf.get_secretorder_reward(global_data.player.secretorder_period, lv)
            if has_buy_card:
                reward_id_lst.append(low_reward_id)
                reward_id_lst.append(high_reward_id)
            else:
                reward_id_lst.append(low_reward_id)
            for reward_id in reward_id_lst:
                if not reward_id:
                    continue
                reward_conf = confmgr.get('common_reward_data', str(reward_id))
                if not reward_conf:
                    continue
                for item_no, num in reward_conf.get('reward_list', []):
                    reward_list.append((item_no, num))

            if not reward_list:
                continue
            for item_id, num in reward_list:
                if SHOW:
                    item_info = self._item_no_to_item.setdefault(item_id, {})
                    if not item_info:
                        rare_degree = item_utils.get_item_rare_degree(item_id, num)
                        if rare_degree == RARE_DEGREE_4:
                            item = self.panel.list_buy_award.AddTemplateItem(index=0)
                        else:
                            item = self.panel.list_buy_award.AddTemplateItem()
                        self._item_no_to_item[item_id] = {'item': item,'num': num}
                        init_tempate_mall_i_item(item, item_id, num, show_rare_degree=True, show_tips=True)
                    else:
                        self._item_no_to_item[item_id]['num'] += num
                        now_number = self._item_no_to_item[item_id]['num']
                        if now_number > 1:
                            lab_nd = self._item_no_to_item[item_id]['item'].lab_quantity
                            lab_nd.setVisible(True)
                            lab_nd.SetString(str(now_number))
                else:
                    self._item_no_to_item[item_id]['num'] -= num
                    now_number = self._item_no_to_item[item_id]['num']
                    item = self._item_no_to_item[item_id]['item']
                    if now_number <= 0:
                        self._item_no_to_item.pop(item_id)
                        idx = self.panel.list_buy_award.getIndexByItem(item)
                        if idx is not None:
                            self.panel.list_buy_award.DeleteItemIndex(idx)
                    elif now_number > 1:
                        item.lab_quantity.setVisible(True)
                        item.lab_quantity.SetString(str(now_number))
                    else:
                        item.lab_quantity.setVisible(False)

        self._last_des_lv = self._des_lv
        return

    def update_price(self):
        price_node = self.panel.temp_price_special
        total_price = secret_order_conf.YUANBAO_TO_UPGRADE * (self._des_lv - self._now_lv)
        price_node.lab_price.SetString(str(total_price))
        txt_color = '#SS' if check_yuanbao(total_price, pay_tip=False) else '#SR'
        price_node.lab_price.SetColor(txt_color)

    def destroy(self):
        if self.panel and self.panel.isValid():
            self.panel.Destroy()
        self.panel = None
        self._sp_data = None
        super(SmallBpLevelBuyWidget, self).destroy()
        return