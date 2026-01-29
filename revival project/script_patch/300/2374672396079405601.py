# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivityMonthCardNew.py
from __future__ import absolute_import
import copy
from logic.client.const import mall_const
from logic.gutils import jump_to_ui_utils
from common.cfg import confmgr
from logic.gcommon.common_const import activity_const
from logic.gcommon.time_utility import get_day_hour_minute_second, get_month, get_now_struct_time
from logic.gutils import template_utils
from logic.gutils import mall_utils
from logic.gcommon import time_utility
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.comsys.activity.ActivityTemplate import ActivityBase
from logic.gutils.activity_utils import need_remain_yueka_renewal, save_yueka_tab_open_time
from logic.gcommon.common_const import shop_const

class ActivityMonthCardNew(ActivityBase):

    def __init__(self, dlg, activity_type):
        super(ActivityMonthCardNew, self).__init__(dlg, activity_type)
        self.init_parameters()
        self.process_event(True)

    def on_finalize_panel(self):
        self.process_event(False)
        if global_data.ui_lifetime_log_mgr:
            global_data.ui_lifetime_log_mgr.finish_record_ui_page_life_time('ChargeUINew', self.__class__.__name__)

    def set_show(self, show, is_init=False):
        self.panel.setVisible(show)

    def init_parameters(self):
        self.is_pc_global_pay = mall_utils.is_pc_global_pay()
        self._day_item_widget = None
        self._ticket_item_widget = None
        return

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'update_charge_info': self.refresh_panel,
           'update_month_card_info': self.refresh_panel
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def refresh_panel(self):
        from logic.gcommon.common_utils.local_text import get_cur_text_lang
        from logic.gcommon.common_const.lang_data import LANG_CN
        player = global_data.player
        can_buy = not player.has_yueka()
        can_can_advance = self.check_can_advance_renewal()
        self.panel.nd_before.setVisible(False)
        self.panel.nd_after.setVisible(False)
        self.panel.nd_renew.setVisible(False)
        self.panel.img_card_1.setVisible(False)
        self.panel.img_card_2.setVisible(False)
        if can_buy:
            self.panel.img_card_1.setVisible(True)
            self.panel.nd_before.setVisible(True)
            self.panel.lab_tips.setVisible(get_cur_text_lang() == LANG_CN)
        else:
            self.panel.nd_after.setVisible(True)
            if can_can_advance:
                self.panel.img_card_1.setVisible(True)
                self.panel.nd_renew.setVisible(True)
            else:
                self.panel.img_card_2.setVisible(True)
            time = player.get_yueka_time()
            time -= time_utility.get_server_time()
            day, _, _, _ = get_day_hour_minute_second(time)
            self.panel.lab_get_today.SetString(get_text_by_id(606009, [get_text_by_id(556684, [day])]))
            can_get = player.yueka_daily_yuanbao()
            self.panel.btn_get.SetEnable(can_get)
            self.panel.btn_get.SetText(get_text_by_id(606010) if can_get else get_text_by_id(606011))
        now_datetime = get_now_struct_time()
        month = now_datetime.tm_mon

        def add_reward_to_dict(reward_list, dict, num=1):
            for reward_item_no, reward_num in reward_list:
                dict[reward_item_no] = dict.get(reward_item_no, 0) + reward_num * num

        total_reward_dict = {}
        buy_reward_list = confmgr.get('common_reward_data', str(activity_const.MONTHCARD_FIRST_BUY_REWARD), 'reward_list', default=[])
        add_reward_to_dict(buy_reward_list, total_reward_dict)
        if len(buy_reward_list) > 0:
            reward_item_no, reward_num = buy_reward_list[0]
            temp_item = self.panel.temp_item_1
            if can_can_advance:
                temp_item = self.panel.temp_item_3
            template_utils.init_tempate_mall_i_item(temp_item, reward_item_no, item_num=300, show_tips=True)
        show_first_time_buy = self.is_show_first_buy_info()
        if show_first_time_buy:
            buy_reward_key = str(activity_const.MONTHCARD_FIRST_BUY_REWARD)
        else:
            buy_reward_key = str(activity_const.MONTHCARD_NOT_FIRST_BUY_REWARD)
        buy_reward_list = confmgr.get('common_reward_data', buy_reward_key, 'reward_list', default=[])
        add_reward_to_dict(buy_reward_list, total_reward_dict)
        temp_item = self.panel.temp_item_2
        if can_can_advance:
            temp_item = self.panel.temp_item_4
        visible = len(buy_reward_list) > 0
        temp_item.setVisible(visible)
        if visible:
            reward_item_no, reward_num = buy_reward_list[0]
            template_utils.init_tempate_mall_i_item(temp_item, reward_item_no, item_num=reward_num, show_tips=True)
        self.update_day_reward()
        self.update_free_ticket()
        self.update_advance_renewal_nd()

    def on_init_panel(self):

        @self.panel.btn_buy.unique_callback()
        def OnClick(btn, touch):
            if self.is_pc_global_pay:
                jump_to_ui_utils.jump_to_web_charge()
            else:
                goods_info = global_data.lobby_mall_data.get_activity_sale_info('MONTH_CARD_GOODS')
                if goods_info:
                    global_data.player and global_data.player.pay_order(goods_info['goodsid'])

        @self.panel.btn_renew.unique_callback()
        def OnClick(btn, touch):
            if self.check_can_advance_renewal():
                buy_count = global_data.player.get_yueka_buy_count()
                if buy_count <= 0:
                    goods_info = global_data.lobby_mall_data.get_activity_sale_info('MONTH_CARD_GOODS')
                else:
                    goods_info = global_data.lobby_mall_data.get_activity_sale_info('ADVANCE_RENEWAL_MONTH_CARD_GOODS')
                if goods_info:
                    global_data.player and global_data.player.pay_order(goods_info['goodsid'])

        @self.panel.btn_get.unique_callback()
        def OnClick(btn, touch):
            global_data.player and global_data.player.try_get_yueka_daily_reward()

        self.refresh_panel()
        self.refresh_goods()
        self.show_list()
        player = global_data.player
        can_buy = not player.has_yueka()
        can_can_advance = self.check_can_advance_renewal()
        ani_name = 'vx_show_once'
        self.panel.PlayAnimation(ani_name)
        max_time = self.panel.GetAnimationMaxRunTime(ani_name)

        def callback():
            self.panel.PlayAnimation('vx_stars_loop')

        self.panel.SetTimeOut(max_time, callback)
        if global_data.ui_lifetime_log_mgr:
            global_data.ui_lifetime_log_mgr.start_record_ui_page_life_time('ChargeUINew', self.__class__.__name__)
        if need_remain_yueka_renewal():
            save_yueka_tab_open_time()
            global_data.player.read_activity_list(self._activity_type)

    def refresh_goods(self):
        goods_info = global_data.lobby_mall_data.get_activity_sale_info('MONTH_CARD_GOODS')
        if not goods_info:
            self.panel.btn_buy.SetText('******')
            return
        if self.is_pc_global_pay or mall_utils.is_steam_pay():
            price_txt = mall_utils.get_pc_charge_price_str(goods_info)
        else:
            key = goods_info['goodsid']
            price_txt = mall_utils.get_charge_price_str(key)
        self.panel.btn_buy.SetText(mall_utils.adjust_price(str(price_txt)))

    def update_advance_renewal_nd(self):
        goods_info = global_data.lobby_mall_data.get_activity_sale_info('MONTH_CARD_GOODS')
        advance_renewal_goods_info = global_data.lobby_mall_data.get_activity_sale_info('ADVANCE_RENEWAL_MONTH_CARD_GOODS')
        temp_price = self.panel.temp_price.temp_price.GetItem(0)
        if not goods_info or not advance_renewal_goods_info:
            temp_price.lab_price_before.SetString('****')
            temp_price.lab_price.SetString('****')
            return
        buy_count = global_data.player.get_yueka_buy_count()
        key = goods_info['goodsid']
        advance_key = advance_renewal_goods_info['goodsid']
        if buy_count <= 0:
            if self.is_pc_global_pay or mall_utils.is_steam_pay():
                price_txt_before = mall_utils.get_pc_charge_price_str(goods_info)
            else:
                price_txt_before = mall_utils.get_charge_price_str(key)
            temp_price.lab_price.SetStringWithAdapt(mall_utils.adjust_price(str(price_txt_before)))
            temp_price.lab_price_before.setVisible(False)
            self.panel.img_discount.setVisible(False)
        else:
            if self.is_pc_global_pay or mall_utils.is_steam_pay():
                price_txt_before = mall_utils.get_pc_charge_price_str(goods_info)
                price_txt_now = mall_utils.get_pc_charge_price_str(advance_renewal_goods_info)
            else:
                price_txt_before = mall_utils.get_charge_price_str(key)
                price_txt_now = mall_utils.get_charge_price_str(advance_key)
            temp_price.lab_price_before.SetString(mall_utils.adjust_price(str(price_txt_before)))
            temp_price.lab_price.SetStringWithAdapt(mall_utils.adjust_price(str(price_txt_now)))
            temp_price.lab_price_before.setVisible(True)
            self.panel.img_discount.setVisible(True)

    def check_can_advance_renewal(self):
        if self.is_pc_global_pay:
            return False
        else:
            time = global_data.player.get_yueka_time()
            time -= time_utility.get_server_time()
            buy_count = global_data.player.get_yueka_buy_count()
            if time > 0 and buy_count <= 0:
                return True
            if 0 <= time <= 10 * time_utility.ONE_DAY_SECONDS:
                return True
            return False

    def is_show_first_buy_info(self):
        buy_count = global_data.player.get_yueka_buy_count()
        can_renewal = self.check_can_advance_renewal()
        if buy_count < 1:
            return True
        if buy_count == 1:
            if global_data.player.has_yueka() and not can_renewal:
                return True
        return False

    def update_day_reward(self, item_widget=None):
        if item_widget:
            self._day_item_widget = item_widget
        else:
            item_widget = self._day_item_widget
        if not item_widget:
            return
        else:
            reward_cnt = global_data.player.get_yueka_yuanbao_cnt()
            if reward_cnt is not None:
                item_widget.nd_extra_info.setVisible(True)
                if reward_cnt > 0:
                    text = get_text_by_id(609983).format(reward_cnt)
                else:
                    text = get_text_by_id(609982).format(7)
                item_widget.lab_save_info.SetString(text)
            can_get = global_data.player.yueka_daily_yuanbao()
            item_widget.nd_common.setVisible(not can_get)
            item_widget.nd_get.setVisible(can_get)
            if can_get:
                template_path = 'charge/i_month_item_0'
            else:
                template_path = 'charge/i_month_item_1'
            item_widget.temp_item = global_data.uisystem.re_create_item(item_widget.temp_item, root=item_widget, tmp_path=template_path)
            item_widget.temp_item.PlayAnimation('month_loop')

            @item_widget.btn_get.unique_callback()
            def OnClick(btn, touch):
                global_data.player and global_data.player.try_get_yueka_daily_reward()

            return

    def update_free_ticket(self, item_widget=None):
        if item_widget:
            self._ticket_item_widget = item_widget
        else:
            item_widget = self._ticket_item_widget
        if not item_widget:
            return
        can_get = global_data.player.has_yueka() and not global_data.player.yueka_daily
        item_widget.nd_common.setVisible(not can_get)
        item_widget.nd_get.setVisible(can_get)

        @item_widget.btn_get.unique_callback()
        def OnClick(btn, touch):
            global_data.player and global_data.player.try_get_yueka_daily_reward()

    def goto_free_ticket(self):
        if global_data.player and global_data.player.is_yueka_test():
            lottery_ids = mall_utils.get_all_valid_art_lottery_id()
            lottery_id = None
            if lottery_ids:
                lottery_id = lottery_ids[-1]
            jump_to_ui_utils.jump_to_lottery(lottery_id=lottery_id)
        else:
            from logic.client.const.mall_const import MODE_SPECIAL, MODE_SPECIAL_2
            jump_mode = G_IS_NA_PROJECT or MODE_SPECIAL if 1 else MODE_SPECIAL_2
            jump_to_ui_utils.jump_to_lottery(lottery_id=jump_mode)
        return

    def goto_double_season_score(self):
        jump_to_ui_utils.jump_to_season_pass()

    def goto_vip_emote(self):
        from logic.comsys.charge_ui import PreviewEmoteList
        ui = PreviewEmoteList.PreviewEmoteList(None, emote_key='riko_month_card')
        return

    def goto_mall_discount(self):
        global_data.ui_mgr.close_ui('ChargeUINew')
        jump_to_ui_utils.jump_to_mall(None, (mall_const.RECOMMEND_ID, mall_const.RECOMMEND_DISCOUNT_ID))
        return

    def show_list(self):
        from common.platform.dctool import interface
        list_node = self.panel.list_rights.GetItem(0)
        list_rights = list_node.list_item
        items = [{'text': 607413,'desc': 607420,'template': 'charge/i_month_item_1','loop': 'month_loop','init_func': self.update_day_reward}, {'text': 607471,'desc': 607473,'template': 'charge/i_month_item_8','goto': self.goto_free_ticket}, {'text': 607414,'desc': 607422,'template': 'charge/i_month_item_3','loop': 'loop','goto': self.goto_double_season_score}, {'text': 607415,'desc': 607424,'tips': 607450,'template': 'charge/i_month_item_5'}, {'text': 607416,'desc': 607425,'template': 'charge/i_month_item_6'}, {'text': 607417,'desc': 607438,'template': 'charge/i_month_item_7','goto': self.goto_mall_discount}, {'text': 607419,'desc': 607423,'template': 'charge/i_month_item_4','goto': self.goto_vip_emote}]
        if global_data.player and global_data.player.is_yueka_test():
            items[1] = {'text': 607471,'desc': 633829,'tips': 633830,'template': 'charge/i_month_item_10','goto': self.goto_free_ticket}
        count = len(items)
        self.panel.lab_rights.SetString(get_text_by_id(607470, [count]))

        @list_rights.callback()
        def OnCreateItem(lv, index, item_widget):
            self.set_up_item(item_widget, index, items[index])

        list_rights.setTouchEnabled(False)
        list_rights.SetInitCount(count)
        new_size = list_rights.GetContentSize()
        old_size = self.panel.list_rights.GetInnerContentSize()
        self.panel.list_rights.SetInnerContentSize(new_size[0], old_size.height)

    def set_up_item(self, item_widget, i, info):
        item_widget.temp_item = global_data.uisystem.re_create_item(item_widget.temp_item, tmp_path=info['template'])
        if 'loop' in info:
            item_widget.temp_item.PlayAnimation(info['loop'])
        ani_name = 'jump_once'
        item_widget.PlayAnimation(ani_name)
        max_time = item_widget.GetAnimationMaxRunTime(ani_name)

        def callback(_item_widget=item_widget):
            _item_widget.StopAnimation(ani_name)
            _item_widget.PlayAnimation('get_loop')

        item_widget.SetTimeOut(max_time, callback)
        item_widget.lab_name.SetString(info['text'])
        item_widget.lab_name_get.SetString(info['text'])
        desc = info.get('desc', '')
        if desc:
            item_widget.lab_des.SetString(desc)
        tips = info.get('tips', '')
        if tips:
            item_widget.lab_tips_up.setVisible(True)
            item_widget.lab_tips_up.SetString(tips)
        init_func = info.get('init_func', None)
        if init_func:
            init_func(item_widget=item_widget)
        item_widget.btn_go.setVisible('goto' in info)

        @item_widget.btn_go.unique_callback()
        def OnClick(btn, touch, _info=info):
            _info['goto']()

        return