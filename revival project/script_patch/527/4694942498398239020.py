# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/lottery/LotterySpringFestivalWidget.py
from __future__ import absolute_import
import six
from logic.client.const.mall_const import SINGLE_LOTTERY_COUNT, CONTINUAL_LOTTERY_COUNT
from logic.gutils.mall_utils import get_lottery_category_floor_data
from logic.gutils.lobby_click_interval_utils import global_unique_click
from common.platform.dctool.interface import get_project_id
from .LotteryBaseWidget import LotteryBaseWidget
from .LotteryBuyWidget import LotteryBuyWidget
from .LotteryTurntableWidget import LotteryTurntableWidget, ITEM_DEFAULT_STATE, ITEM_PASS_STATE, ITEM_CHOSEN_STATE, ITEM_LOOP_STATE
from .LotteryExchangeRewardWidget import LotteryExchangeRewardWidget
from logic.gcommon.item.item_const import RARE_DEGREE_1, RARE_DEGREE_2, RARE_DEGREE_3, RARE_DEGREE_4, RARE_DEGREE_6
from logic.gcommon.const import SHOP_PAYMENT_VALUABLE_CATTLE_COIN
from logic.client.const.mall_const import DARK_PRICE_COLOR
import logic.gcommon.time_utility as tutil
import time
NEED_ADJUST_RARE_DEGREE_PIC_TEMPLATE = 'activity/activity_202101/lottery/i_activity_spring_festival_lottery_item_1'
RARE_DEGREE_PIC_PREFIX = 'gui/ui_res_2/activity/activity_202101/lottery/'
RARE_DEGREE_PIC_MAP = {RARE_DEGREE_1: RARE_DEGREE_PIC_PREFIX + 'icon_spring_c.png',
   RARE_DEGREE_2: RARE_DEGREE_PIC_PREFIX + 'icon_spring_b.png',
   RARE_DEGREE_3: RARE_DEGREE_PIC_PREFIX + 'icon_spring_a.png',
   RARE_DEGREE_4: RARE_DEGREE_PIC_PREFIX + 'icon_spring_s_little.png'
   }

def reward_center_closed--- This code section failed: ---

  30       0  LOAD_GLOBAL           0  'get_project_id'
           3  CALL_FUNCTION_0       0 
           6  LOAD_CONST            1  'g93'
           9  COMPARE_OP            2  '=='
          12  POP_JUMP_IF_FALSE    24  'to 24'

  31      15  LOAD_CONST            2  '2021-02-25 05:00:00'
          18  STORE_FAST            0  'deadline'
          21  JUMP_FORWARD          6  'to 30'

  33      24  LOAD_CONST            3  '2021-03-18 05:00:00'
          27  STORE_FAST            0  'deadline'
        30_0  COME_FROM                '21'

  34      30  LOAD_GLOBAL           1  'tutil'
          33  LOAD_ATTR             2  'get_server_time'
          36  CALL_FUNCTION_0       0 
          39  LOAD_GLOBAL           3  'time'
          42  LOAD_ATTR             4  'mktime'
          45  LOAD_GLOBAL           3  'time'
          48  LOAD_ATTR             5  'strptime'
          51  LOAD_ATTR             4  'mktime'
          54  CALL_FUNCTION_2       2 
          57  CALL_FUNCTION_1       1 
          60  COMPARE_OP            5  '>='
          63  RETURN_VALUE     
          -1  RETURN_LAST      

Parse error at or near `CALL_FUNCTION_1' instruction at offset 57


class LotterySpringFestivalWidget(LotteryBaseWidget):

    def init_parameters(self):
        super(LotterySpringFestivalWidget, self).init_parameters()
        self.category_floor = get_lottery_category_floor_data(self.lottery_id)
        self.category_node_map = {RARE_DEGREE_6: self.panel.nd_schedule_s_plus,
           RARE_DEGREE_4: self.panel.nd_schedule_s
           }
        self.need_skip_anim = False
        self.has_bought_first_continual_lottery = global_data.player.get_reward_count(self.data['table_id']) >= 10
        self._do_open_RewardUI = False

    def init_panel(self):
        super(LotterySpringFestivalWidget, self).init_panel()

        @global_unique_click(self.panel.btn_history)
        def OnClick(btn, touch):
            global_data.emgr.lottery_history_open.emit()

        @global_unique_click(self.panel.btn_help)
        def OnClick(btn, touch):
            from logic.comsys.common_ui.GameRuleDescUI import GameRuleDescUI
            dlg = GameRuleDescUI()
            title, content = self.data.get('rule_desc', [608080, 608081])
            dlg.set_lottery_rule(title, content)

        @global_unique_click(self.panel.btn_back.btn_back)
        def OnClick(btn, touch):
            global_data.ui_mgr.close_ui('LotteryMainUI')

        @global_unique_click(self.panel.btn_skip)
        def OnClick(btn, touch):
            self.need_skip_anim = not self.need_skip_anim
            btn.SetSelect(self.need_skip_anim)

        @global_unique_click(self.panel.btn_reward_center)
        def OnClick(btn, touch):
            self._do_open_RewardUI = True
            global_data.player.get_opened_activities()

        self.panel.btn_reward_center.setVisible(not reward_center_closed())

        @global_unique_click(self.panel.btn_shop)
        def OnClick(btn, touch):
            if not self.exchange_reward_widget:
                self._init_exchange_reward_widget()
            self.exchange_reward_widget.visible = True

        self._init_turntable_widget()
        self._init_buy_widget()
        self.exchange_reward_widget = None
        self.panel.btn_skip.SetSelect(self.need_skip_anim)
        self.update_first_continual_lottery_info()
        self.update_coin_num()
        self.update_reward_red_point()
        if G_IS_NA_PROJECT:
            self.panel.nd_title.lab_num.SetString(609527)
        return

    def get_event_conf(self):
        econf = {'on_lottery_ended_event': self.on_lottery_ended,
           'net_login_reconnect_event': self.on_reconnect_event,
           'refresh_lottery_limited_guarantee_round': self.refresh_limited_item_guarantee_round,
           'receive_task_prog_reward_succ_event': self.update_reward_red_point,
           'refresh_activity_list': self.refresh_activity_list
           }
        return econf

    def _init_turntable_widget(self):

        def play_item_default_anim(nd, anim_name, item_id):
            if item_id not in ('201800543', '201801141', '208200326', '201001547'):
                return
            for name in anim_name:
                nd.PlayAnimation(name)

        self.turntable_widget = LotteryTurntableWidget(self, self.panel, self.lottery_id, nd_click_name='btn_item_bg', need_adjust_rare_degree_pic_template=NEED_ADJUST_RARE_DEGREE_PIC_TEMPLATE, rare_degree_pic_map=RARE_DEGREE_PIC_MAP, item_anim_name_map={ITEM_DEFAULT_STATE: ('circulation', 'circulation_show'),
           ITEM_PASS_STATE: 'pass',
           ITEM_CHOSEN_STATE: 'choosed',
           ITEM_LOOP_STATE: 'loop'
           }, play_item_anim_func_map={ITEM_DEFAULT_STATE: play_item_default_anim
           })

    def _init_exchange_reward_widget(self):
        self.exchange_reward_widget = LotteryExchangeRewardWidget(self, self.panel.node_2.nd_exchange, self.panel.node_2, self.panel.node_1, self.lottery_id, self.on_change_show_reward, nd_visibility_opposite_relatively=[
         'list_bar', 'lab_num_times'])

    def _init_buy_widget(self):

        def buying_callback(lottery_count):
            self.turntable_widget.stop_turntable_item_state_anim(ITEM_DEFAULT_STATE)
            self.turntable_widget.play_turntable_animation(lottery_count)
            btn_anim_name = 'btn_once_click' if lottery_count == SINGLE_LOTTERY_COUNT else 'btn_repeat_click'
            self.panel.PlayAnimation(btn_anim_name)
            self.panel.btn_once.img_btn_light_1.setVisible(False)
            self.panel.btn_once.img_btn_light_2.setVisible(False)
            self.panel.btn_repeat.img_btn_light_1.setVisible(False)
            self.panel.btn_repeat.img_btn_light_2.setVisible(False)

        def lottery_data_ready_callback(bought_successfully):
            if not bought_successfully:
                self.turntable_widget.lottery_failed()

        self.buy_widget = LotteryBuyWidget(self, self.panel, self.lottery_id, buy_button_info={SINGLE_LOTTERY_COUNT: self.panel.btn_once,
           CONTINUAL_LOTTERY_COUNT: self.panel.btn_repeat
           }, buy_price_info={SINGLE_LOTTERY_COUNT: self.panel.btn_once.temp_price,
           CONTINUAL_LOTTERY_COUNT: self.panel.btn_repeat.temp_price
           }, price_color=DARK_PRICE_COLOR, buying_callback=buying_callback, lottery_data_ready_callback=lottery_data_ready_callback)

    def on_finalize_panel(self):
        super(LotterySpringFestivalWidget, self).on_finalize_panel()
        if self.buy_widget:
            self.buy_widget.destroy()
            self.buy_widget = None
        if self.turntable_widget:
            self.turntable_widget.destroy()
            self.turntable_widget = None
        if self.exchange_reward_widget:
            self.exchange_reward_widget.destroy()
            self.exchange_reward_widget = None
        return

    def show(self):
        self.panel.setVisible(True)
        self.panel.PlayAnimation('show')
        self.panel.PlayAnimation('loop')
        self.turntable_widget.play_turntable_item_state_anim(ITEM_DEFAULT_STATE)
        self.update_first_continual_lottery_info()
        global_data.emgr.set_price_widget_close_btn_visible.emit('LotteryMainUI', False)

    def hide(self):
        self.panel.setVisible(False)
        self.panel.StopAnimation('show')
        self.panel.StopAnimation('loop')
        global_data.emgr.set_price_widget_close_btn_visible.emit('LotteryMainUI', True)

    def refresh(self):
        self.buy_widget.refresh()
        self.update_first_continual_lottery_info()
        self.refresh_limited_item_guarantee_round()
        self.refresh_lottery_limit_count()
        self.update_coin_num()

    def refresh_show_model(self, show_model_id=None):
        self.exchange_reward_widget and self.exchange_reward_widget.refresh_show_model(show_model_id)

    def on_receive_lottery_result(self, item_list, origin_list):
        self.turntable_widget.set_turntable_items_got(item_list, origin_list)

    def update_first_continual_lottery_info(self):
        self.has_bought_first_continual_lottery = global_data.player.get_reward_count(self.data['table_id']) >= 10
        self.panel.img_repeat_tips.setVisible(not self.has_bought_first_continual_lottery)

    def update_coin_num(self):
        self.panel.btn_shop.lab_num.SetString(str(global_data.player.get_item_num_by_no(SHOP_PAYMENT_VALUABLE_CATTLE_COIN)))

    def on_lottery_ended(self):
        self.turntable_widget.play_turntable_item_state_anim(ITEM_DEFAULT_STATE)
        self.update_first_continual_lottery_info()
        self.refresh_limited_item_guarantee_round()
        self.update_coin_num()
        self.panel.btn_once.img_btn_light_1.setVisible(True)
        self.panel.btn_once.img_btn_light_2.setVisible(True)
        self.panel.btn_repeat.img_btn_light_1.setVisible(True)
        self.panel.btn_repeat.img_btn_light_2.setVisible(True)

    def on_reconnect_event(self):
        if global_data.ui_mgr.get_ui('ScreenLockerUI'):
            global_data.emgr.lottery_data_ready.emit(False)
            global_data.ui_mgr.close_ui('LotteryMainUI')

    def refresh_limited_item_guarantee_round(self):
        for rare_degree, nd in six.iteritems(self.category_node_map):
            max_count, line_no = self.category_floor[str(rare_degree)]
            has_bought_count = global_data.player.get_reward_category_floor(self.data['table_id'], line_no)
            nd.lab_tag_num.SetString('{}/{}'.format(has_bought_count, max_count))
            nd.nd_prog.prog_tag.SetPercentage(100.0 * has_bought_count / max_count)

    def update_reward_red_point(self, *args, **kwargs):
        from logic.gutils.activity_utils import can_receive_task_prog_reward
        count = can_receive_task_prog_reward('1411369') + can_receive_task_prog_reward('1411370')
        self.panel.btn_reward_center.temp_new.setVisible(count > 0)

    def refresh_activity_list(self):
        if reward_center_closed():
            self.panel.btn_reward_center.setVisible(False)
            return
        if self._do_open_RewardUI:
            global_data.ui_mgr.show_ui('ActivitySpringFestivalRewardUI', 'logic.comsys.activity.SpringFestival')
        self._do_open_RewardUI = False