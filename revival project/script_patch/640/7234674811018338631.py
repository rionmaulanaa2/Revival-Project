# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/lottery/LotteryTenTryResult.py
from __future__ import absolute_import
from six.moves import range
from common.uisys.basepanel import BasePanel
from common.const.uiconst import NORMAL_LAYER_ZORDER, UI_VKB_CLOSE
from logic.gutils.reward_item_ui_utils import refresh_item_info, smash_item_info, play_item_appear_to_idle_animation
import cc
from .LotteryBuyWidget import LotteryBuyWidget
from logic.client.const.mall_const import CONTINUAL_LOTTERY_COUNT
from logic.gutils import mall_utils
from logic.client.const.mall_const import DARK_PRICE_COLOR
from logic.gcommon.const import SHOP_PAYMENT_YUANBAO

class LotteryTenTryResult(BasePanel):
    PANEL_CONFIG_NAME = 'mall/open_lottery_results'
    DLG_ZORDER = NORMAL_LAYER_ZORDER
    UI_VKB_TYPE = UI_VKB_CLOSE
    UI_ACTION_EVENT = {'btn_close.OnClick': 'close'
       }

    def on_init_panel(self, *args, **kwargs):
        self.lottery_id = None
        self.items = []
        self.ori_items = []
        self.buy_widget = None
        if global_data.player:
            global_data.player.click_lottery_10_try_result()
        return

    def on_finalize_panel(self):
        if self.buy_widget:
            self.buy_widget.destroy()
            self.buy_widget = None
        return

    def set_reward_result(self, lottery_id, items, origin_items):
        self.lottery_id = lottery_id
        self.items = items
        self.ori_items = origin_items
        self._init_buy_widget()
        for i in range(len(self.items)):
            self.add_one_item(i)

    def add_one_item(self, i):
        widget = self.panel.list_item.AddTemplateItem()
        item_result = self.ori_items[i] if self.ori_items[i] else self.items[i]
        refresh_item_info(widget, *item_result)
        widget.lab_item_name.SetColor('#BK')
        if item_result == self.items[i]:
            return

        def play_smash_scale():
            item_id, item_num = self.items[i]
            smash_item_info(widget, item_id, item_num)
            play_item_appear_to_idle_animation(widget, item_id, item_num, callback=lambda : widget.PlayAnimation('smash_scale'), need_reset_node=True, after_smash=True)

        action_list = [
         cc.DelayTime.create(0.5),
         cc.CallFunc.create(lambda : widget.PlayAnimation('smash')),
         cc.DelayTime.create(widget.GetAnimationMaxRunTime('smash') + 0.1),
         cc.CallFunc.create(play_smash_scale)]
        widget.runAction(cc.Sequence.create(action_list))

    def _init_buy_widget(self):

        def get_special_price_info(price_info, lottery_count):
            if lottery_count == CONTINUAL_LOTTERY_COUNT:
                from common.cfg import confmgr
                goods_id = confmgr.get('lottery_page_config', str(self.lottery_id), 'try_params', 'goods_id', default=None)
                price = mall_utils.get_mall_item_price(goods_id)
                return (
                 price, False)
            else:
                return False

        def special_buy_logic_func(price_info, lottery_count):
            if self.buy_widget.do_buy_10_try():
                self.close()
            return True

        self.buy_widget = LotteryBuyWidget(self, self.panel, self.lottery_id, buy_button_info={CONTINUAL_LOTTERY_COUNT: self.panel.temp_btn.btn_common_big}, buy_price_info={CONTINUAL_LOTTERY_COUNT: self.panel.temp_price}, price_color=DARK_PRICE_COLOR, get_special_price_info=get_special_price_info, special_buy_logic_func=special_buy_logic_func)