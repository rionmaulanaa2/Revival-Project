# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivitySpark.py
from __future__ import absolute_import
from six.moves import range
from logic.comsys.activity.ActivityTemplate import ActivityBase
from logic.comsys.mall_ui.BuyConfirmUIInterface import groceries_buy_confirmUI
from logic.gutils.template_utils import init_price_view
from logic.client.const.mall_const import NO_RED_DARK_PRICE_COLOR
from logic.comsys.lottery.LotteryPreviewWidget import LotteryPreviewWidget
from logic.gutils.mall_utils import get_lottery_widgets_info
from logic.comsys.effect import ui_effect

class ActivitySpark(ActivityBase):

    def on_init_panel(self):
        self._preview_widget = None
        self._refresh_widget = False
        self.lottery_id = '0'
        self._data = {}
        self.init_widget()
        self.set_content()
        global_data.emgr.buy_good_success += self.set_content
        return

    def set_content(self):
        goods_ids = ('50500025', '50500026', '50500027')
        goods_num = ('X10', 'X20', 'X30')
        discount = ('15%', '20%', '25%')
        for i in range(3):
            goods_id = goods_ids[i]
            nd = getattr(self.panel, 'nd_reward_' + str(i + 1), None)
            if not nd:
                continue
            nd.lab_title.lab_num.SetString(goods_num[i])
            nd.nd_discount.lab_discount.SetString(discount[i])
            init_price_view(nd.temp_price, goods_id, NO_RED_DARK_PRICE_COLOR, ['yuanbao'])
            btn = nd.btn_go_buy
            has_buy = False
            if global_data.player and global_data.player.get_buy_num_all(goods_id):
                has_buy = True
            if has_buy:
                btn.SetText(12014)
                btn.SetEnable(False)
                ui_effect.set_gray(btn.img_btn, True, False)
            else:

                @btn.callback()
                def OnClick(btn, touch, goods_id=goods_id):
                    if self._preview_widget:
                        self._preview_widget.hide()
                    groceries_buy_confirmUI(goods_id)

        return

    def init_widget(self):
        widgets_map, _ = get_lottery_widgets_info()
        self._data = widgets_map[self.lottery_id]
        on_change_show_reward = lambda *args, **kwargs: 0
        self._preview_widget = LotteryPreviewWidget(self.panel.temp_preview, self.panel, self.lottery_id, on_change_show_reward)
        self._preview_widget.hide()

        @self.panel.btn_preview.callback()
        def OnClick(*args):
            if not self._refresh_widget:
                self._preview_widget.refresh_preview_list(self.lottery_id, self._data.get('limited_item_id_list'), self._data.get('percent_up_item_id_dict', {}))
                self._refresh_widget = True
            self._preview_widget.show()

    def on_finalize_panel(self):
        if self._preview_widget:
            self._preview_widget.hide()
            self._preview_widget.on_finalize_panel()
        self._preview_widget = None
        global_data.emgr.buy_good_success -= self.set_content
        return