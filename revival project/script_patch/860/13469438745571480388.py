# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/lottery/LotteryValentineWidget.py
from __future__ import absolute_import
from logic.client.const.mall_const import SINGLE_LOTTERY_COUNT, CONTINUAL_LOTTERY_COUNT
from logic.gutils.mall_utils import check_payment, get_lottery_category_floor_data, get_mall_item_price
from .LotteryBaseWidget import LotteryBaseWidget
from .LotteryPreviewWidget import LotteryPreviewWidget
from .LotteryBuyWidget import LotteryBuyWidget
from .LotteryTurntableWidget import LotteryTurntableWidget, ITEM_PASS_STATE, ITEM_CHOSEN_STATE
from logic.gcommon.const import SHOP_PAYMENT_YUANBAO, SHOP_PAYMENT_VALENTINE_ROSE, SHOP_PAYMENT_VALENTINE_HEART, VALENTINE_ROSE
from logic.client.const.mall_const import DARK_PRICE_COLOR
from logic.gcommon.common_utils.local_text import get_cur_text_lang
from logic.gcommon.common_const.lang_data import LANG_CN, LANG_EN, LANG_ZHTW, LANG_JA
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gutils.template_utils import init_tempate_mall_i_item
from logic.gutils.lobby_click_interval_utils import global_unique_click
from common.cfg import confmgr
IGNORE_INIT_COMMON_ITEM_TEMPLATE = 'activity/activity_202101/valentine/i_activity_valentines_day_lottery_heart'
LANG_IN_ANIM_NAME_MAP = {LANG_CN: 'cn',
   LANG_EN: 'en',
   LANG_ZHTW: 'tw',
   LANG_JA: 'jp'
   }

class LotteryValentineWidget(LotteryBaseWidget):

    def init_parameters(self):
        super(LotteryValentineWidget, self).init_parameters()
        self.category_floor = get_lottery_category_floor_data(self.lottery_id)
        self.common_turntable_item_count = len(confmgr.get('preview_1401230520')['turntable_goods_info'])
        self.continual_turntable_lottery_ret = []
        self.continual_buying = False
        self.need_skip_anim = False
        self.all_round_finished = False
        self.cur_single_goods_id = self.data['single_goods_id']
        self.single_goods_id_list = [self.cur_single_goods_id]
        self.single_goods_id_list.extend(self.data['extra_single_goods_id'])
        self.single_goods_id_list.append(self.single_goods_id_list[-1])

    def init_panel(self):
        super(LotteryValentineWidget, self).init_panel()

        @global_unique_click(self.panel.btn_detail)
        def OnClick(btn, touch):
            self.preview_widget.show()

        @global_unique_click(self.panel.btn_skip)
        def OnClick(btn, touch):
            self.need_skip_anim = not self.need_skip_anim
            btn.SetSelect(self.need_skip_anim)

        @global_unique_click(self.panel.btn_help)
        def OnClick(btn, touch):
            from logic.comsys.common_ui.GameRuleDescUI import GameRuleDescUI
            dlg = GameRuleDescUI()
            title, content = (82221, 82219)
            dlg.set_show_rule(title, content)

        self._init_turntable_widget()
        self._init_preview_widget()
        self._init_buy_widget()
        self.refresh_turntable_round_data()
        self.panel.RecordAnimationNodeState('frame_reward')
        if global_data.player.get_item_money(SHOP_PAYMENT_VALENTINE_HEART):
            self._use_ticket_buy_lottery(CONTINUAL_LOTTERY_COUNT)

    def get_event_conf(self):
        econf = {'on_lottery_ended_event': self.on_lottery_ended,
           'net_login_reconnect_event': self.on_reconnect_event
           }
        return econf

    def play_common_turntable_item_chosen_anim(self, nd, anim_name, item_id):
        if isinstance(anim_name, list) and anim_name:
            anim_name = anim_name[0]
        nd.PlayAnimation(anim_name)
        if int(item_id) == SHOP_PAYMENT_VALENTINE_HEART:

            def play_anim():
                if not self.panel or not self.panel.isValid():
                    return
                self.panel.PlayAnimation('streamer')
                self.panel.PlayAnimation('frame_reward')

            global_data.game_mgr.register_logic_timer(play_anim, times=1, interval=14)

    def refresh_common_turntable_nd_got(self, nd, item_id, item_count):
        if nd.GetTemplatePath() != IGNORE_INIT_COMMON_ITEM_TEMPLATE:
            got = global_data.player.get_reward_intervene_count(self.data['table_id']).get(item_id, 0) > 0
            nd.temp_reward.nd_get.setVisible(got)

    def _use_ticket_buy_lottery(self, lottery_count):
        goods_id = self.cur_single_goods_id if lottery_count == SINGLE_LOTTERY_COUNT else self.data['continual_goods_id']
        price_info = get_mall_item_price(goods_id)[0]
        price_info['goods_id'] = goods_id
        self.buy_widget.do_use_ticket_buy_lottery(price_info, lottery_count)

    def common_turntable_block_show_lottery_result_callback(self):
        if self.continual_buying:
            cur_ticket_count = global_data.player.get_item_money(SHOP_PAYMENT_VALENTINE_ROSE)
            single_goods_price = get_mall_item_price(self.cur_single_goods_id)[0]['real_price']
            if cur_ticket_count >= single_goods_price:
                self._use_ticket_buy_lottery(SINGLE_LOTTERY_COUNT)
            else:
                global_data.player.buy_goods(self.data['ticket_goods_id'], single_goods_price - cur_ticket_count, SHOP_PAYMENT_YUANBAO, need_show=False)
                self._use_ticket_buy_lottery(SINGLE_LOTTERY_COUNT)
        else:
            self.common_turntable_widget.max_delighted_time = 2
            self.common_turntable_widget.max_single_interval = 0.8
            self.common_turntable_widget.med_single_interval = 0.1
            self._use_ticket_buy_lottery(CONTINUAL_LOTTERY_COUNT)

    def _init_turntable_widget(self):

        def init_common_turntable_item_data(nd, item_id, item_count):
            if nd.GetTemplatePath() != IGNORE_INIT_COMMON_ITEM_TEMPLATE:
                init_tempate_mall_i_item(nd.temp_reward, item_id, item_count)

        def check_common_item_got_func(nd, item_id, item_idx):
            return nd.GetTemplatePath() != IGNORE_INIT_COMMON_ITEM_TEMPLATE and global_data.player and global_data.player.get_reward_intervene_count(self.data['table_id']).get(item_id, 0) > 0

        def get_nd_got_func(nd, idx):
            if nd.GetTemplatePath() != IGNORE_INIT_COMMON_ITEM_TEMPLATE:
                return nd.temp_reward.nd_get
            else:
                return None
                return None

        self.common_turntable_widget = LotteryTurntableWidget(self, self.panel, self.lottery_id, turntable_item_list=confmgr.get('preview_1401230520')['turntable_goods_info'], nd_item_format='temp_item_small_{}', item_anim_name_map={ITEM_PASS_STATE: 'select',
           ITEM_CHOSEN_STATE: 'selected'
           }, play_item_anim_func_map={ITEM_CHOSEN_STATE: self.play_common_turntable_item_chosen_anim
           }, init_item_data_func=init_common_turntable_item_data, need_show_got=True, get_nd_got_func=get_nd_got_func, check_item_got_func=check_common_item_got_func, refresh_nd_got_func=self.refresh_common_turntable_nd_got, block_show_lottery_result_callback=self.common_turntable_block_show_lottery_result_callback, continual_count_reserve_anim=True, get_last_clicked_lottery_count=self.get_last_clicked_lottery_count)

        def init_precious_turntable_item_data(nd, item_id, item_count):
            pass

        def check_precious_item_got_func(nd, item_id, item_idx):
            if not global_data.player:
                return False
            else:
                intervene_count = global_data.player.get_reward_intervene_count(140123052001L)
                if global_data.player.get_item_num_by_no(int(item_id)) > 0 and isinstance(intervene_count, dict) and str(item_id) in intervene_count:
                    return True
                return False

        self.precious_turntable_item_list = confmgr.get('preview_140123052001')['turntable_goods_info']
        self.precious_turntable_widget = LotteryTurntableWidget(self, self.panel, self.lottery_id, turntable_item_list=self.precious_turntable_item_list, item_anim_name_map={ITEM_PASS_STATE: 'select',
           ITEM_CHOSEN_STATE: 'selected'
           }, init_item_data_func=init_precious_turntable_item_data, max_single_interval=0.8, med_single_interval=0.15, min_single_interval=0.07, high_speed_count_percent=0.8, max_delighted_time=3, need_show_got=True, get_nd_got_func=lambda nd, idx: nd.nd_get, check_item_got_func=check_precious_item_got_func, continual_count_reserve_anim=True, get_last_clicked_lottery_count=self.get_last_clicked_lottery_count)
        self.turntable_widget = self.common_turntable_widget

    def _init_preview_widget(self):

        def show_callback():
            global_data.emgr.hide_lottery_main_ui_elements.emit(True, ('top', 'lab_num_times'))
            self.panel.node_1.setVisible(False)
            self.panel.node_2.setVisible(True)
            self.refresh_preview()

        def close_callback():
            global_data.emgr.hide_lottery_main_ui_elements.emit(False, ('top', 'lab_num_times'))
            self.panel.node_1.setVisible(True)
            self.panel.node_2.setVisible(False)

        self.preview_widget = LotteryPreviewWidget(self.panel.temp_preview, self.panel, self.lottery_id, self.on_change_show_reward, show_callback=show_callback, close_callback=close_callback, item_lab_rate_color='#SW')
        self.preview_widget.enable_scroll_view(False)

    def check_buy_action_disabled(self, lottery_count):
        if self.all_round_finished:
            global_data.game_mgr.show_tip(get_text_by_id(82220))
            return True
        return False

    def _init_buy_widget(self):

        def get_special_price_info(price_info, lottery_count):
            if lottery_count == CONTINUAL_LOTTERY_COUNT:
                common_item_got_count = len(global_data.player.get_reward_intervene_count(self.data['table_id']))
                guarantee_round = self.common_turntable_item_count - common_item_got_count
                cur_ticket_count = global_data.player.get_item_money(SHOP_PAYMENT_VALENTINE_ROSE)
                single_goods_price = get_mall_item_price(self.cur_single_goods_id)[0]['real_price']
                cost_ticket_count = guarantee_round * single_goods_price
                need_buy_ticket_count = cost_ticket_count - cur_ticket_count
                final_price_info = []
                if cur_ticket_count > 0:
                    if need_buy_ticket_count > 0:
                        show_ticket_count = cur_ticket_count
                    else:
                        show_ticket_count = cost_ticket_count
                    ticket_price_info = {'goods_payment': VALENTINE_ROSE,'original_price': show_ticket_count,
                       'real_price': show_ticket_count
                       }
                    final_price_info.append(ticket_price_info)
                if need_buy_ticket_count > 0:
                    money_price_info = get_mall_item_price(self.data['ticket_goods_id'])[0]
                    money_price_info['original_price'] *= need_buy_ticket_count
                    money_price_info['real_price'] *= need_buy_ticket_count
                    final_price_info.append(money_price_info)
                return (final_price_info, False)
            return False

        def special_buy_logic_func(price_info, lottery_count):
            self.continual_turntable_lottery_ret = []
            if lottery_count == CONTINUAL_LOTTERY_COUNT:
                common_item_got_count = len(global_data.player.get_reward_intervene_count(self.data['table_id']))
                guarantee_round = self.common_turntable_item_count - common_item_got_count
                cur_ticket_count = global_data.player.get_item_money(SHOP_PAYMENT_VALENTINE_ROSE)
                single_goods_price = get_mall_item_price(self.cur_single_goods_id)[0]['real_price']
                cost_ticket_count = guarantee_round * single_goods_price
                need_buy_ticket_count = cost_ticket_count - cur_ticket_count
                if need_buy_ticket_count > 0:
                    money_price_info = get_mall_item_price(self.data['ticket_goods_id'])[0]
                    money_price_info['real_price'] *= need_buy_ticket_count
                    if not check_payment(money_price_info['goods_payment'], money_price_info['real_price']):
                        return True
                self.common_turntable_widget.max_delighted_time = 2
                self.common_turntable_widget.max_single_interval = 0.05
                self.common_turntable_widget.med_single_interval = 0.05
                if cur_ticket_count >= single_goods_price:
                    self._use_ticket_buy_lottery(SINGLE_LOTTERY_COUNT)
                else:
                    global_data.player.buy_goods(self.data['ticket_goods_id'], single_goods_price - cur_ticket_count, SHOP_PAYMENT_YUANBAO, need_show=False)
                    self._use_ticket_buy_lottery(SINGLE_LOTTERY_COUNT)
                self.continual_buying = True
                return True
            return False

        def buying_callback(lottery_count):
            self.turntable_widget = self.common_turntable_widget if lottery_count == SINGLE_LOTTERY_COUNT else self.precious_turntable_widget
            self.turntable_widget.play_turntable_animation(SINGLE_LOTTERY_COUNT)

        def lottery_data_ready_callback(bought_successfully):
            if not bought_successfully:
                self.turntable_widget.lottery_failed()

        self.buy_widget = LotteryBuyWidget(self, self.panel, self.lottery_id, buy_button_info={SINGLE_LOTTERY_COUNT: self.panel.temp_start_btn_1.btn,
           CONTINUAL_LOTTERY_COUNT: self.panel.temp_start_btn_2.btn
           }, buy_price_info={SINGLE_LOTTERY_COUNT: self.panel.temp_start_btn_1.temp_price,
           CONTINUAL_LOTTERY_COUNT: self.panel.temp_start_btn_2.temp_price
           }, price_color=DARK_PRICE_COLOR, get_special_price_info=get_special_price_info, special_buy_logic_func=special_buy_logic_func, buying_callback=buying_callback, lottery_data_ready_callback=lottery_data_ready_callback)

    def on_finalize_panel(self):
        super(LotteryValentineWidget, self).on_finalize_panel()
        if self.buy_widget:
            self.buy_widget.destroy()
            self.buy_widget = None
        if self.preview_widget:
            self.preview_widget.destroy()
            self.preview_widget = None
        if self.common_turntable_widget:
            self.common_turntable_widget.destroy()
            self.common_turntable_widget = None
        if self.precious_turntable_widget:
            self.precious_turntable_widget.destroy()
            self.precious_turntable_widget = None
        return

    def show(self):
        self.panel.setVisible(True)
        self.panel.PlayAnimation('into')

        def delay_play_anim():
            if not self.panel or not self.panel.isValid():
                return
            self.precious_turntable_widget.play_turntable_item_special_animation('light')

        global_data.game_mgr.register_logic_timer(delay_play_anim, times=1, interval=12)
        self.preview_widget.parent_show()
        self.refresh_turntable_round_data()

    def hide(self):
        self.panel.setVisible(False)
        self.panel.StopAnimation('show')
        self.panel.StopAnimation('loop')

    def refresh(self):
        self.buy_widget.refresh()
        self.refresh_lottery_limit_count()

    def refresh_show_model(self, show_model_id=None):
        self.on_change_show_reward(show_model_id)

    def refresh_preview(self):
        self.preview_widget.refresh_preview_list(self.lottery_id, self.data.get('limited_item_id_list', None), self.data.get('percent_up_item_id_dict', {}))
        return

    def _cache_continual_turntable_lottery_ret(self, item_list, origin_list):
        if self.continual_turntable_lottery_ret:
            self.continual_turntable_lottery_ret[0].extend(item_list)
            self.continual_turntable_lottery_ret[1].extend(origin_list)
        else:
            self.continual_turntable_lottery_ret = (
             item_list, origin_list)

    def on_receive_lottery_result(self, item_list, origin_list):
        receiving_valentine_heart = False
        for item_id, item_count in item_list:
            if item_id == SHOP_PAYMENT_VALENTINE_HEART:
                receiving_valentine_heart = True
                self.continual_buying = False
                break

        if self.continual_buying:
            self._cache_continual_turntable_lottery_ret(item_list, origin_list)
        if self.turntable_widget == self.precious_turntable_widget:
            self._cache_continual_turntable_lottery_ret(item_list, origin_list)
            self.turntable_widget.set_turntable_items_got(*self.continual_turntable_lottery_ret)
        else:
            self.turntable_widget.enable_show_lottery_result(not receiving_valentine_heart and not self.continual_buying)
            self.turntable_widget.set_turntable_items_got(item_list, origin_list, force_play_chosen_anim_when_skip=receiving_valentine_heart)

    def refresh_turntable_round_data(self):
        max_round_count = 0
        for index, (item_id, item_count) in enumerate(self.precious_turntable_item_list):
            max_round_count = index

        owned_count = global_data.player.get_buy_num_all(self.data['continual_goods_id'])
        max_round_count += 1
        self.cur_single_goods_id = self.single_goods_id_list[owned_count]
        self.buy_widget.update_lottery_price_info(SINGLE_LOTTERY_COUNT, self.cur_single_goods_id)
        self.all_round_finished = max_round_count == owned_count
        owned_count = min(owned_count + 1, max_round_count)
        self.panel.lab_rounds.SetString('{}/{}'.format(owned_count, max_round_count))

    def on_lottery_ended(self):
        self.refresh_turntable_round_data()
        self.panel.StopAnimation('frame_reward')
        self.panel.RecoverAnimationNodeState('frame_reward')

    def on_reconnect_event(self):
        if global_data.ui_mgr.get_ui('ScreenLockerUI'):
            global_data.emgr.lottery_data_ready.emit(False)
            global_data.ui_mgr.close_ui('LotteryMainUI')

    def get_last_clicked_lottery_count(self):
        if self.buy_widget:
            return self.buy_widget.last_clicked_lottery_count
        else:
            return None
            return None