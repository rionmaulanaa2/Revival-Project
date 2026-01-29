# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivityS14CollectionBuy.py
from __future__ import absolute_import
import six_ex
from logic.comsys.activity.ActivityCollect import ActivityBase
from common.cfg import confmgr
from logic.gutils import task_utils, mall_utils
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gutils import jump_to_ui_utils
from logic.gutils.template_utils import init_tempate_mall_i_simple_item

class ActivityS14CollectionBuy(ActivityBase):

    def __init__(self, dlg, activity_type):
        super(ActivityS14CollectionBuy, self).__init__(dlg, activity_type)
        self.init_parameters()
        self.init_widget()
        self.process_events(True)

    def on_finalize_panel(self):
        self.process_events(False)
        super(ActivityS14CollectionBuy, self).on_finalize_panel()

    def init_parameters(self):
        conf = confmgr.get('c_activity_config', str(self._activity_type), 'cUiData', default={})
        self.goods_id = conf.get('goods_id')
        self.goods_info = None
        self.is_pc_global_pay = mall_utils.is_pc_global_pay()
        if global_data.lobby_mall_data and global_data.player:
            self.goods_info = global_data.lobby_mall_data.get_activity_sale_info('ACTIVITY_S14_COLLECTION_PACKET')
            if self.goods_info:
                key = self.goods_info['goodsid']
                goods_id = global_data.player.get_goods_info(key).get('cShopGoodsId')
                if goods_id:
                    self.goods_id = goods_id
        self.reward_id = mall_utils.get_goods_item_reward_id(str(self.goods_id))
        self.jump_item_no = conf.get('jump_item_no')
        return

    def process_events(self, is_bind):
        emgr = global_data.emgr
        econf = {'buy_good_success': self.update_widget
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def init_widget(self):

        @self.panel.btn_show.unique_callback()
        def OnClick(*args):
            self.on_click_btn_show()

        @self.panel.btn_buy.unique_callback()
        def OnClick(*args):
            self.on_click_btn_buy()

        self.init_item_list()
        self.init_btn_buy()

    def init_item_list(self):
        reward_conf = confmgr.get('common_reward_data', str(self.reward_id))
        reward_list = reward_conf.get('reward_list', [])
        item_no, item_num = reward_list[0]
        init_tempate_mall_i_simple_item(self.panel.temp_item, item_no, item_num, show_tips=True)
        item_no, item_num = reward_list[1]
        init_tempate_mall_i_simple_item(self.panel.temp_item2, item_no, item_num, show_tips=True)

    def update_item_list(self):
        has_bought = mall_utils.limite_pay(self.goods_id)
        self.panel.temp_item.nd_get.setVisible(has_bought)
        self.panel.temp_item2.nd_get.setVisible(has_bought)

    def init_btn_buy(self):
        btn_buy = self.panel.btn_buy
        has_bought = mall_utils.limite_pay(self.goods_id)
        if not self.goods_info:
            btn_buy.SetEnable(False)
            btn_buy.SetText('******')
            return
        if self.is_pc_global_pay or mall_utils.is_steam_pay():
            price_txt = mall_utils.get_pc_charge_price_str(self.goods_info)
        else:
            price_txt = mall_utils.get_charge_price_str(self.goods_info['goodsid'])
        btn_buy.SetEnable(not has_bought)
        if not has_bought:
            btn_buy.SetText(mall_utils.adjust_price(str(price_txt)))
        else:
            btn_buy.SetText(12014)

    def on_click_btn_show(self, *args):
        jump_to_ui_utils.jump_to_display_detail_by_item_no(self.jump_item_no)

    def on_click_btn_buy(self, *args):
        has_bought = mall_utils.limite_pay(self.goods_id)
        if has_bought:
            global_data.game_mgr.show_tip(get_text_by_id(607175))
            return
        if self.is_pc_global_pay:
            jump_to_ui_utils.jump_to_web_charge()
        elif self.goods_info:
            global_data.player and global_data.player.pay_order(self.goods_info['goodsid'])

    def update_widget(self, *args):
        self.init_btn_buy()
        self.update_item_list()