# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivityPromare/ActivityPromareExchange.py
from __future__ import absolute_import
import cc
from common.uisys.basepanel import BasePanel
from common.const.uiconst import NORMAL_LAYER_ZORDER, UI_VKB_CLOSE
from logic.gcommon.time_utility import get_simply_time, get_time_string
from logic.gutils.item_utils import get_lobby_item_name
from logic.gcommon.time_utility import get_server_time
from common.cfg import confmgr
from common.utils.timer import CLOCK
from logic.gutils import mall_utils, item_utils
MATOI_ID = 201802151
BURNISH_ID = 201001943
LIODEGALON_ID = 201801151

class ActivityPromareExchange(BasePanel):
    DLG_ZORDER = NORMAL_LAYER_ZORDER
    UI_VKB_TYPE = UI_VKB_CLOSE
    NEED_HIDE_MAIN_UI = False
    PANEL_CONFIG_NAME = 'activity/activity_202203/promare/exchange/open_promare_exchange'
    UI_ACTION_EVENT = {'btn_close.OnClick': 'close'
       }
    GLOBAL_EVENT = {'player_item_update_event_with_id': 'update_all'
       }

    def on_init_panel(self, *args, **kwargs):
        super(ActivityPromareExchange, self).on_init_panel(*args, **kwargs)
        lottery_id = kwargs.get('lottery_id', '138')
        self.exchange_goods_id = kwargs.get('exchange_goods_id', '701700672')
        valid_time = confmgr.get('lottery_page_config', str(lottery_id), 'visible_ts', default=[1615996800, 1659628800, 1615996800])
        self.end_time = valid_time[1]
        left_time = self.end_time - get_server_time()
        self.panel.lab_time.SetString(get_text_by_id(609772, (get_simply_time(left_time),)))
        self.timer_id = None
        if left_time < 600:
            self.timer_id = global_data.game_mgr.register_logic_timer(self.update_left_time, interval=1, times=-1, mode=CLOCK)
        self.panel.btn_question.setVisible(False)
        nd_matoi = self.panel.list_item.GetItem(0)
        nd_matoi.lab_name.SetString(get_lobby_item_name(MATOI_ID))
        nd_matoi.btn_get.BindMethod('OnClick', self.close)
        nd_burnish = self.panel.list_item.GetItem(1)
        nd_burnish.lab_name.SetString(get_lobby_item_name(BURNISH_ID))
        nd_burnish.btn_get.BindMethod('OnClick', self.close)
        nd_liodegalon = self.panel.nd_reward.bar_bg
        nd_liodegalon.nd_lock.setVisible(not bool(global_data.player.get_item_num_by_no(LIODEGALON_ID)))
        nd_liodegalon.img_tag.lab_name.SetString(get_lobby_item_name(LIODEGALON_ID))

        @self.panel.btn_exchange.callback()
        def OnClick(*args):
            if get_server_time() > self.end_time:
                global_data.game_mgr.show_tip(12129)
                return
            try:
                prices = mall_utils.get_mall_item_price(self.exchange_goods_id)
                if not prices:
                    return
                price_info = prices[0]
                if not mall_utils.check_payment(price_info['goods_payment'], price_info['original_price']):
                    return
            except:
                pass

            from logic.gcommon.const import SHOP_PAYMENT_ITEM
            global_data.player.buy_goods(self.exchange_goods_id, 1, SHOP_PAYMENT_ITEM)

        self.update_all()
        return

    def update_all(self, item_id=None):
        if item_id == LIODEGALON_ID:
            self.close()
            return
        else:
            if item_id is not None and item_id not in (MATOI_ID, BURNISH_ID):
                return
            nd_matoi = self.panel.list_item.GetItem(0)
            not_own_matoi = not bool(global_data.player.get_item_num_by_no(MATOI_ID))
            nd_matoi.nd_lock.setVisible(not_own_matoi)
            nd_matoi.btn_get.SetEnable(not_own_matoi)
            nd_matoi.btn_get.SetText(82290 if not_own_matoi else 12136)
            nd_burnish = self.panel.list_item.GetItem(1)
            not_own_burnish = not bool(global_data.player.get_item_num_by_no(BURNISH_ID))
            nd_burnish.nd_lock.setVisible(not_own_burnish)
            nd_burnish.btn_get.SetEnable(not_own_burnish)
            nd_burnish.btn_get.SetText(82290 if not_own_burnish else 12136)
            can_buy = global_data.player.get_item_num_by_no(MATOI_ID) and global_data.player.get_item_num_by_no(BURNISH_ID)
            owned = global_data.player.get_item_num_by_no(LIODEGALON_ID)
            self.panel.btn_exchange.SetEnable(bool(can_buy and not owned))
            self.panel.btn_exchange.SetText(12136 if owned else 12074)
            if self.exchange_goods_id:
                price_info = mall_utils.get_mall_item_price(self.exchange_goods_id, 1)
                if price_info:
                    show_price = price_info[0]
                    goods_payment = show_price['goods_payment']
                    real_price = show_price['real_price']
                    money_icon = item_utils.get_money_icon(goods_payment)
                    self.panel.icon_card.SetDisplayFrameByPath('', money_icon)
                    self.panel.lab_value.SetString(str(real_price))
            return

    def update_left_time(self):
        left_time = self.end_time - get_server_time()
        self.panel.lab_time.SetString(get_text_by_id(609772, (get_simply_time(left_time),)))

    def on_finalize_panel(self):
        if self.timer_id:
            global_data.game_mgr.unregister_logic_timer(self.timer_id)
            self.timer_id = None
        return