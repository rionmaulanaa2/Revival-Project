# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivityHalloweenBuy.py
from __future__ import absolute_import
from common.cfg import confmgr
from logic.comsys.activity.ActivityTemplate import ActivityBase
from logic.gutils.template_utils import init_price_template
from logic.gutils.mall_utils import get_mall_item_price, buy_num_limit_by_all, get_goods_item_reward_id
from logic.comsys.lottery.LotteryNewPreviewWidget import LotteryNewPreviewWidget

class ActivityHalloweenBuy(ActivityBase):

    def __init__(self, dlg, activity_type):
        super(ActivityHalloweenBuy, self).__init__(dlg, activity_type)
        self.preview_widget = None
        self.init_panel()
        global_data.emgr.buy_good_success += self.update_show
        return

    def init_panel(self):
        ui_data = confmgr.get('c_activity_config', self._activity_type, 'cUiData')
        self.goods_id_lst = ui_data.get('goods_id_list', [])
        for idx, goods_id in enumerate(self.goods_id_lst):
            idx_number = idx + 1
            node = getattr(self.panel.nd_content.nd_right, 'btn_right%s' % idx_number)
            discount_lab_node = getattr(node, 'lab_number%s' % idx_number)
            price_node = getattr(node, 'list_price%s' % idx_number)
            reward_id = get_goods_item_reward_id(goods_id)
            reward_conf = confmgr.get('common_reward_data', str(reward_id))
            item_no, item_num = reward_conf.get('reward_list', [])[0]
            lab_text = '<size=20>' + get_text_by_id(81372) + '<size=31><fontname=gui/fonts/g93_num.ttf>X%s' % item_num
            node.lab_liquan_number.setString(lab_text)
            price_info = get_mall_item_price(str(goods_id), 1)
            discount_lab = 100 - int(price_info[0].get('discount') * 100)
            discount_lab_node.SetString(str(discount_lab))
            init_price_template(price_info[0], price_node)
            limit_by_all, _, _ = buy_num_limit_by_all(str(goods_id))
            useless_node = getattr(node, 'btn_useless_%s' % idx_number)
            if limit_by_all:
                node.SetEnable(False)
                useless_node.setVisible(True)
            else:
                node.SetEnable(True)
                useless_node.setVisible(False)

                @node.unique_callback()
                def OnClick(btn, touch, goods_id=goods_id):
                    from logic.comsys.mall_ui.GroceriesBuyConfirmUI import GroceriesBuyConfirmUI
                    GroceriesBuyConfirmUI(goods_id=str(goods_id))

        def cb(*args):
            pass

        @self.panel.nd_content.btn_view.unique_callback()
        def OnClick(*args):
            if self.preview_widget is None:
                from logic.gutils.mall_utils import get_lottery_widgets_info
                widgets_map, _ = get_lottery_widgets_info()
                widget = global_data.uisystem.load_template_create('mall/lottery_review', self.panel.nd_review)
                self.preview_widget = LotteryNewPreviewWidget(widget.list_review_all, self.panel, '10', cb, None)

                @widget.btn_close.unique_callback()
                def OnClick(*args):
                    self.close_review()

            self.panel.nd_block.setVisible(True)
            self.panel.nd_review.setVisible(True)
            self.preview_widget.show()
            return

    def set_show(self, show, is_init=False):
        super(ActivityHalloweenBuy, self).set_show(show)
        self.close_review()

    def update_show(self):
        for idx, goods_id in enumerate(self.goods_id_lst):
            idx_number = idx + 1
            node = getattr(self.panel.nd_content.nd_right, 'btn_right%s' % idx_number)
            limit_by_all, _, _ = buy_num_limit_by_all(str(goods_id))
            useless_node = getattr(node, 'btn_useless_%s' % idx_number)
            if limit_by_all:
                node.SetEnable(False)
                useless_node.setVisible(True)

    def close_review(self):
        self.panel.nd_review.setVisible(False)
        self.panel.nd_block.setVisible(False)

    def on_finalize_panel(self):
        super(ActivityHalloweenBuy, self).on_finalize_panel()
        global_data.emgr.buy_good_success -= self.update_show
        if self.preview_widget:
            self.preview_widget.on_finalize_panel()
        self.preview_widget = None
        return