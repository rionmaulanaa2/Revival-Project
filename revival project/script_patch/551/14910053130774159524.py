# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivityMonthCard.py
from __future__ import absolute_import
from logic.client.const import mall_const
from logic.gutils import item_utils
from common.cfg import confmgr
from logic.gcommon.item import item_const
from logic.gcommon.common_const import activity_const
from logic.gcommon.time_utility import get_day_hour_minute_second, get_month, get_now_struct_time
from logic.gutils import template_utils
from logic.gutils import mall_utils
from logic.gcommon import time_utility
from logic.gcommon.common_utils.local_text import get_text_by_id
import logic.gcommon.const as gconst
from logic.comsys.activity.ActivityTemplate import ActivityBase
from logic.gcommon.common_const import shop_const

class ActivityMonthCard(ActivityBase):

    def __init__(self, dlg, activity_type):
        super(ActivityMonthCard, self).__init__(dlg, activity_type)
        self.init_parameters()
        self.init_event()

    def on_finalize_panel(self):
        self.process_event(False)
        self.buy_reward_3 = None
        self.detail_widget = None
        self.reward_item_no = None
        return

    def set_show(self, show, is_init=False):
        self.panel.setVisible(show)

    def init_parameters(self):
        self.reward_item_no = None
        self.buy_reward_3 = None
        self.detail_widget = None
        return

    def init_event(self):
        self.process_event(True)

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'update_charge_info': self.refresh_goods,
           'update_month_card_info': self.update_month_card_info
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def refresh_panel(self):

        @self.panel.btn_go.unique_callback()
        def OnClick(btn, touch):
            from logic.gutils import jump_to_ui_utils
            jump_to_ui_utils.jump_to_lottery('0')

        if not global_data.player.has_yueka():
            self.panel.btn_go.SetEnable(True)
            self.panel.btn_go.img_red.setVisible(False)
            self.panel.nd_go_already.setVisible(False)
        elif mall_utils.has_yueka_lottery_discount('0', shop_const.GOOD_ID_LOTTERY_HALF_PRICE):
            self.panel.btn_go.SetEnable(True)
            self.panel.btn_go.img_red.setVisible(True)
            self.panel.nd_go_already.setVisible(False)
        else:
            self.panel.btn_go.SetEnable(False)
            self.panel.btn_go.img_red.setVisible(False)
            self.panel.nd_go_already.setVisible(True)

    def on_init_panel(self):

        @self.panel.temp_buy.btn_common.unique_callback()
        def OnClick(btn, touch):
            goods_info = global_data.lobby_mall_data.get_activity_sale_info('MONTH_CARD_GOODS')
            if goods_info:
                global_data.player and global_data.player.pay_order(goods_info['goodsid'])

        @self.panel.temp_get.btn_common.unique_callback()
        def OnClick(btn, touch):
            global_data.player and global_data.player.try_get_yueka_daily_reward()

        self.refresh_panel()
        now_datetime = get_now_struct_time()
        month, day = now_datetime.tm_mon, now_datetime.tm_mday
        if day < 10:
            month = 12 if month == 1 else month - 1
        buy_reward_list = confmgr.get('common_reward_data', str(activity_const.MONTHCARD_BUY_REWARD_BY_MONTH[month]), 'reward_list', default=[])
        if len(buy_reward_list) > 0:
            reward_item_no, reward_num = buy_reward_list[0]
            self.reward_item_no = reward_item_no
            template_utils.init_tempate_mall_i_item(self.panel.nd_reward1.temp_reward, reward_item_no, item_num=reward_num, show_tips=True)
        if len(buy_reward_list) > 1:
            reward_item_no, reward_num = buy_reward_list[1]
            template_utils.init_tempate_mall_i_item(self.panel.nd_reward2.temp_reward, reward_item_no, item_num=reward_num, show_tips=True)
            self.buy_reward_3 = buy_reward_list[1]
            self._refresh_buy_reward_add()
        day_reward_list = confmgr.get('common_reward_data', str(activity_const.MONTHCARD_DAY_REWARD), 'reward_list', default=[])
        if day_reward_list:
            if len(day_reward_list) >= 2:
                crystal_item_no, crystal_num = day_reward_list[0]
                diamond_item_no, diamond_num = day_reward_list[1]
                crystal_img_res_path = item_utils.get_lobby_item_pic_by_item_no(crystal_item_no)
                diamond_img_res_path = item_utils.get_lobby_item_pic_by_item_no(diamond_item_no)
                crystal_img_txt = '<color=0XFFFFFFFF><img ="%s",scale=0.0></color>' % crystal_img_res_path
                diamond_img_txt = '<color=0XFFFFFFFF><img ="%s",scale=0.0></color>' % diamond_img_res_path
                self.panel.lab_benifit_1.SetString(get_text_by_id(606012).format(crystal_img=crystal_img_txt, crystal_num=crystal_num, diamond_img=diamond_img_txt, diamond_num=diamond_num))
                self.panel.nd_today_reward.img_reward.SetDisplayFrameByPath('', crystal_img_res_path)
                self.panel.nd_today_reward.lab_num.SetString(str(crystal_num))
                self.panel.nd_today_reward.img_reward2.SetDisplayFrameByPath('', diamond_img_res_path)
                self.panel.nd_today_reward.lab_num2.SetString(str(diamond_num))
            self.panel.lab_benifit_2.SetString(get_text_by_id(606013).format(num=10))
            self.panel.lab_benifit_3.SetString(get_text_by_id(606031))
        self.refresh_ui()
        self.refresh_goods()

    def _refresh_buy_reward_add(self, is_init=True):
        if not self.buy_reward_3:
            return
        nd_reward = self.panel.nd_reward3
        is_first_time_buy = global_data.player and global_data.player.is_first_time_buy_yueka()
        nd_reward.setVisible(is_first_time_buy)
        self.panel.nd_first.setVisible(is_first_time_buy)
        if not is_init:
            return
        reward_item_no, reward_num = self.buy_reward_3
        template_utils.init_tempate_mall_i_item(nd_reward.temp_reward, reward_item_no, item_num=reward_num, show_tips=True)

    def refresh_goods(self):
        goods_info = global_data.lobby_mall_data.get_activity_sale_info('MONTH_CARD_GOODS')
        if not goods_info:
            self.panel.temp_buy.btn_common.SetEnable(False)
            self.panel.lab_price.SetString('******')
            return
        self.panel.temp_buy.btn_common.SetEnable(True)
        key = goods_info['goodsid']
        price_txt = mall_utils.get_charge_price_str(key)
        self.panel.lab_price.SetString(mall_utils.adjust_price(str(price_txt)))

    def _on_item_update(self):
        self.refresh_ui()

    def update_month_card_info(self):
        self.refresh_ui()
        global_data.player.read_activity_list(self._activity_type)

    def refresh_ui(self):
        player = global_data.player
        can_buy = not player.has_yueka()
        is_first_time_buy = player.is_first_time_buy_yueka()
        if not can_buy:
            time = player.get_yueka_time()
            time -= time_utility.get_server_time()
            day, _, _, _ = get_day_hour_minute_second(time)
            self.panel.lab_time.SetString(get_text_by_id(606009, [get_text_by_id(556684, [day])]))
        own_state_text = 80976 if can_buy else ''
        self.panel.own_state.SetString(own_state_text)
        self.panel.temp_buy.setVisible(can_buy)
        self.panel.temp_get.setVisible(not can_buy)
        self.panel.lab_first_tips.setVisible(is_first_time_buy)
        self._refresh_buy_reward_add(is_init=False)
        self.panel.nd_have.setVisible(not can_buy)
        self.panel.nd_activate.setVisible(not can_buy)
        if player:
            self.panel.temp_get.btn_common.SetEnable(not player.yueka_daily)
            self.panel.temp_get.nd_today_reward.setVisible(not player.yueka_daily)
            self.panel.img_red.setVisible(not player.yueka_daily)
            self.panel.nd_value.setVisible(not player.yueka_daily)
            self.panel.temp_get.btn_common.SetText(get_text_by_id(606011) if player.yueka_daily else get_text_by_id(606010))