# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivityWeeklyCard.py
from __future__ import absolute_import
from common.cfg import confmgr
from logic.gcommon.common_const import activity_const
from logic.gcommon.time_utility import get_day_hour_minute_second, get_now_struct_time
from logic.gutils import template_utils
from logic.gutils import mall_utils
from logic.gcommon import time_utility
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.comsys.activity.ActivityTemplate import ActivityBase
from logic.gutils.activity_utils import need_remain_weekly_card_renewal, save_weekly_card_tab_open_time
from logic.gutils import jump_to_ui_utils

class ActivityWeeklyCard(ActivityBase):

    def __init__(self, dlg, activity_type):
        super(ActivityWeeklyCard, self).__init__(dlg, activity_type)
        self.init_parameters()
        self.init_event()

    def on_finalize_panel(self):
        self.process_event(False)
        self.reward_item_no = None
        return

    def set_show(self, show, is_init=False):
        self.panel.setVisible(show)

    def init_parameters(self):
        self.is_pc_global_pay = mall_utils.is_pc_global_pay()
        self.reward_item_no = None
        return

    def init_event(self):
        self.process_event(True)

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'update_charge_info': self.refresh_goods,
           'update_weekly_card_info': self.update_weekly_card_info
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def on_init_panel(self):
        self.panel.lab_charge_tips.setVisible(self.is_pc_global_pay)

        @self.panel.temp_buy.btn_common.unique_callback()
        def OnClick(btn, touch):
            if self.is_pc_global_pay:
                jump_to_ui_utils.jump_to_web_charge()
            else:
                goods_info = global_data.lobby_mall_data.get_activity_sale_info('WEEKLY_CARD_GOODS')
                if goods_info:
                    global_data.player and global_data.player.pay_order(goods_info['goodsid'])

        @self.panel.temp_get.btn_common.unique_callback()
        def OnClick(btn, touch):
            global_data.player and global_data.player.try_get_weeklycard_daily_reward()

        buy_reward_list = confmgr.get('common_reward_data', str(activity_const.WEEKLYCARD_FIRST_BUY_REWARD), 'reward_list', default=[])
        if len(buy_reward_list) > 0:
            reward_item_no, reward_num = buy_reward_list[0]
            self.reward_item_no = reward_item_no
            template_utils.init_tempate_mall_i_item(self.panel.nd_reward1.temp_reward, reward_item_no, item_num=1, show_tips=True)
            self.panel.nd_reward1.lab_num.setString('x%s' % str(reward_num))
        day_reward_list = confmgr.get('common_reward_data', str(activity_const.WEEKLYCARD_DAY_REWARD), 'reward_list', default=[])
        if day_reward_list:
            if len(day_reward_list) >= 2:
                reward_item_no, reward_num = day_reward_list[0]
                template_utils.init_tempate_mall_i_item(self.panel.nd_benifit.temp_reward_1, reward_item_no, item_num=reward_num, show_tips=True)
                reward_item_no, reward_num = day_reward_list[1]
                template_utils.init_tempate_mall_i_item(self.panel.nd_benifit.temp_reward_2, reward_item_no, item_num=reward_num, show_tips=True)
        self.panel.lab_benifit_1.SetString(get_text_by_id(606013).format(num=10))
        self.refresh_ui()
        self.refresh_goods()
        if need_remain_weekly_card_renewal():
            save_weekly_card_tab_open_time()
            global_data.player.read_activity_list(self._activity_type)

    def refresh_goods(self):
        goods_info = global_data.lobby_mall_data.get_activity_sale_info('WEEKLY_CARD_GOODS')
        if not goods_info:
            self.panel.temp_buy.btn_common.SetEnable(False)
            self.panel.lab_price.SetString('******')
            return
        self.panel.temp_buy.btn_common.SetEnable(True)
        if self.is_pc_global_pay or mall_utils.is_steam_pay():
            price_txt = mall_utils.get_pc_charge_price_str(goods_info)
        else:
            key = goods_info['goodsid']
            price_txt = mall_utils.get_charge_price_str(key)
        self.panel.lab_price.SetString(mall_utils.adjust_price(str(price_txt)))

    def update_weekly_card_info(self):
        self.refresh_ui()
        global_data.player.read_activity_list(self._activity_type)

    def refresh_ui(self):
        player = global_data.player
        can_buy = not player.has_weeklycard()
        is_first_time_buy = player.is_first_time_buy_weeklycard()
        if not can_buy:
            time = player.get_weeklycard_time()
            time -= time_utility.get_server_time()
            day, _, _, _ = get_day_hour_minute_second(time)
            self.panel.lab_time.SetString(get_text_by_id(606009, [time_utility.get_readable_time_day_hour_minitue(time)]))
        own_state_text = 80976 if can_buy else ''
        self.panel.own_state.SetString(own_state_text)
        self.panel.temp_buy.setVisible(can_buy)
        self.panel.temp_get.setVisible(not can_buy)
        self.panel.lab_first_tips.setVisible(is_first_time_buy)
        reward_owned = False
        if self.reward_item_no:
            reward_owned = mall_utils.item_has_owned_by_item_no(self.reward_item_no)
        self.panel.nd_have.setVisible(not can_buy or reward_owned)
        self.panel.nd_activate.setVisible(not can_buy)
        if player:
            self.panel.temp_get.btn_common.SetEnable(not player._weeklycard_daily)
            self.panel.img_red.setVisible(not player._weeklycard_daily)
            self.panel.nd_value.setVisible(not player._weeklycard_daily)
            self.panel.lab_value.setString('<size=40>2.1<size=24><align=0>' + get_text_by_id(81225).format(''))
            self.panel.temp_get.btn_common.SetText(get_text_by_id(606011) if player._weeklycard_daily else get_text_by_id(606010))