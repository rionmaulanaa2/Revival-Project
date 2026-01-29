# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/lottery/LotteryGiftsBuyConfirmUI.py
from __future__ import absolute_import
import six
from six.moves import range
from common.uisys.basepanel import BasePanel
from common.const.uiconst import DIALOG_LAYER_BAN_ZORDER
from common.const import uiconst
from logic.comsys.common_ui.ItemNumBtnWidget import ItemNumBtnWidget
from logic.gcommon.item import item_const
from logic.gutils import mall_utils
from logic.gutils import item_utils
from logic.gutils import template_utils
from logic.gutils import activity_utils
from logic.client.const import mall_const
from common.cfg import confmgr
from logic.comsys.common_ui.WindowSmallBase import WindowSmallBase
from logic.comsys.common_ui.JapanShoppingTips import show_with_japan_shopping_tips

@show_with_japan_shopping_tips
class LotteryGiftsBuyConfirmUI(WindowSmallBase):
    PANEL_CONFIG_NAME = 'mall/buy_confirm_gifts'
    DLG_ZORDER = DIALOG_LAYER_BAN_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_CLOSE
    TEMPLATE_NODE_NAME = 'temp_bg'
    UI_ACTION_EVENT = {'temp_btn_buy1.btn_common.OnClick': 'on_buy'
       }

    def on_init_panel(self, achieve_id, goods_id):
        super(LotteryGiftsBuyConfirmUI, self).on_init_panel()
        self.achieve_id = achieve_id
        self.goods_id = goods_id
        self._reward_id_lst = []
        self._timer = 0
        self._timer_cb = {}
        self.register_timer()
        self.init_widget()
        self.process_event(True)

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'buy_good_success': self.on_close
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def on_finalize_panel(self):
        self.process_event(False)
        self.unregister_timer()

    def on_close(self, *args):
        self.close()

    def register_timer(self):
        from common.utils.timer import CLOCK
        self.unregister_timer()
        self._timer = global_data.game_mgr.get_logic_timer().register(func=self.second_callback, interval=1, mode=CLOCK)

    def unregister_timer(self):
        if self._timer > 0:
            global_data.game_mgr.get_logic_timer().unregister(self._timer)
        self._timer = 0
        self._timer_cb = {}

    def second_callback(self):
        for key, cb in six.iteritems(self._timer_cb):
            cb()

    def on_buy(self, *args):
        import logic.gcommon.const as gconst
        limit = mall_utils.limite_pay(self.goods_id)
        if limit:
            global_data.game_mgr.show_tip(get_text_by_id(602011))
            return
        prices = mall_utils.get_mall_item_price(self.goods_id)
        if not prices:
            global_data.player.buy_goods(self.goods_id, 1, gconst.SHOP_PAYMENT_YUANBAO)
            self.close()
            return
        price_info = prices[0]
        goods_payment = price_info.get('goods_payment')
        real_price = price_info.get('real_price')

        def _pay():
            global_data.player.buy_goods(self.goods_id, 1, goods_payment)
            self.close()

        if not mall_utils.check_payment(goods_payment, real_price, cb=_pay):
            return
        from logic.gutils.mall_buy_confirm_func import goods_buy_need_confirm
        if goods_buy_need_confirm(self.goods_id, call_back=_pay):
            return
        _pay()

    def init_widget(self):
        iTextID = confmgr.get('global_achieve_data', str(self.achieve_id), 'iTextID', default='')
        self.panel.temp_bg.lab_title.SetString(iTextID)
        children_achieves = activity_utils.get_child_achieves_from_parent(self.achieve_id)
        count = len(children_achieves) + 1
        list_reward = self.panel.list_reward
        list_reward.SetInitCount(count)
        total_width = 0
        for i in range(count):
            gift_item = list_reward.GetItem(i)
            self.show_stage_reward(gift_item.list_item_1, i)
            inner_size = gift_item.list_item_1.GetContentSize()
            cur_width = inner_size[0] + 13
            total_width += cur_width
            gift_item.SetContentSize(cur_width, gift_item.GetContentSize()[1])
            gift_item.list_item_1.ResizeAndPosition(include_self=False)

        old_inner_size = list_reward.GetInnerContentSize()
        list_reward.SetInnerContentSize(total_width, old_inner_size.height)
        list_reward.GetContainer()._refreshItemPos()
        list_reward._refreshItemPos()
        limite_by_all, _, num_info = mall_utils.buy_num_limit_by_all(self.goods_id)
        self.panel.lab_num.SetString('{}/{}'.format(num_info[1] - num_info[0], num_info[1]))
        price_info = mall_utils.get_mall_item_price(self.goods_id)
        if price_info:
            self.panel.temp_btn_buy1.btn_common.SetText('')
            template_utils.init_price_view(self.panel.temp_price, self.goods_id, color=mall_const.DARK_PRICE_COLOR)
        else:
            self.panel.temp_btn_buy1.btn_common.SetText(81025)
            self.panel.temp_price.setVisible(False)
        self.panel.temp_btn_buy1.btn_common.SetEnable(not limite_by_all)
        open_date_range = mall_utils.get_goods_item_open_date(self.goods_id)

        def second_cb(no_close=False):
            opening, left_time = mall_utils.check_limit_time_lottery_open_info(open_date_range)
            self.panel.lab_time.SetString('{}:{}'.format(get_text_by_id(18031), mall_utils.get_remain_time_txt(left_time)))
            if not opening and not no_close:
                self.close()

        self._timer_cb['second_cb'] = second_cb
        second_cb(no_close=True)

    def show_stage_reward(self, list_item, index):
        if index == 0:
            item_no = mall_utils.get_goods_item_no(self.goods_id)
            reward_id = confmgr.get('lobby_item', str(item_no), 'use_params', 'reward_id')
            reward_list = confmgr.get('common_reward_data', str(reward_id), 'reward_list', default=[])
            count = len(reward_list)
        else:
            children_achieves = activity_utils.get_child_achieves_from_parent(self.achieve_id)
            child_achieve_id = children_achieves[index - 1]
            achieve_conf = confmgr.get('global_achieve_data', str(child_achieve_id))
            reward_id = achieve_conf.get('iRewardID', None)
            reward_list = confmgr.get('common_reward_data', str(reward_id), 'reward_list', default=[])
            count = len(reward_list)
            iTextID = achieve_conf.get('iTextID', '')
            list_item.lab_title_1.SetString(iTextID)
        list_item.SetInitCount(count)
        for i, item_info in enumerate(reward_list):
            item_widget = list_item.GetItem(i)
            item_no, item_num = item_info
            template_utils.init_tempate_mall_i_item(item_widget.temp_item, item_no, item_num, show_tips=True)
            item_widget.lab_name.SetString(item_utils.get_lobby_item_name(item_no))

        return