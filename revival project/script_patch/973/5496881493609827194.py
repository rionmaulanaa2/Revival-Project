# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/lottery/LotteryKizunaAIWidget.py
from __future__ import absolute_import
import six
from logic.client.const.mall_const import SINGLE_LOTTERY_COUNT, CONTINUAL_LOTTERY_COUNT
from logic.gutils.mall_utils import get_lottery_category_floor_data
from logic.gutils.item_utils import get_item_rare_degree, get_lobby_item_type
from logic.gutils.lobby_click_interval_utils import global_unique_click
from .LotteryBaseWidget import LotteryBaseWidget
from .LotteryBuyWidget import LotteryBuyWidget
from .LotteryTurntableWidget import LotteryTurntableWidget, ITEM_DEFAULT_STATE, ITEM_PASS_STATE, ITEM_CHOSEN_STATE, ITEM_LOOP_STATE
from .LotteryExchangeRewardWidget import LotteryExchangeRewardWidget
from logic.gcommon.item.item_const import RARE_DEGREE_1, RARE_DEGREE_2, RARE_DEGREE_3, RARE_DEGREE_4, RARE_DEGREE_6
from logic.gcommon.const import SHOP_PAYMENT_KIZUNA_AI_EXCHANGE
from logic.client.const.mall_const import DARK_PRICE_COLOR
from logic.gcommon.item.lobby_item_type import RP_SKIN_TYPE
from common.platform.dctool.interface import is_mainland_package

class LotteryKizunaAIWidget(LotteryBaseWidget):

    def init_parameters(self):
        super(LotteryKizunaAIWidget, self).init_parameters()
        self.category_floor = get_lottery_category_floor_data(self.lottery_id)
        self.category_node_map = {RARE_DEGREE_6: self.panel.nd_schedule_s_plus,
           RARE_DEGREE_4: self.panel.nd_schedule_s
           }
        self.btn_click_anim_timer = None
        self.need_skip_anim = False
        self.is_visible_close = False
        self.has_bought_first_continual_lottery = global_data.player.get_reward_count(self.data['table_id']) >= 10
        return

    def init_panel(self):
        super(LotteryKizunaAIWidget, self).init_panel()

        @global_unique_click(self.panel.btn_history)
        def OnClick(btn, touch):
            global_data.emgr.lottery_history_open.emit()

        @global_unique_click(self.panel.btn_help)
        def OnClick(btn, touch):
            from logic.comsys.common_ui.GameRuleDescUI import GameRuleDescUI
            dlg = GameRuleDescUI()
            title, content = self.data.get('rule_desc', [608080, 608081])
            dlg.set_lottery_rule(title, content)

        @global_unique_click(self.panel.btn_back)
        def OnClick(btn, touch):
            global_data.ui_mgr.close_ui('LotteryMainUI')

        @global_unique_click(self.panel.btn_skip)
        def OnClick(btn, touch):
            self.need_skip_anim = not self.need_skip_anim
            btn.SetSelect(self.need_skip_anim)

        @global_unique_click(self.panel.btn_reward_center)
        def OnClick(btn, touch):
            global_data.ui_mgr.show_ui('ActivityKizunaAiMainUI2', 'logic.comsys.activity')

        @global_unique_click(self.panel.btn_shop)
        def OnClick(btn, touch):
            self.exchange_reward_widget.visible = True

        self._init_turntable_widget()
        self._init_buy_widget()
        self._init_exchange_reward_widget()
        self.panel.btn_skip.SetSelect(self.need_skip_anim)
        self.update_guarantee_lottery_info()
        self.update_coin_num()
        self.update_reward_red_point()
        if G_IS_NA_PROJECT:
            self.panel.nd_title.lab_num.SetString(609527)

    def get_event_conf(self):
        econf = {'on_lottery_ended_event': self.on_lottery_ended,
           'net_login_reconnect_event': self.on_reconnect_event,
           'refresh_lottery_limited_guarantee_round': self.refresh_limited_item_guarantee_round,
           'message_update_global_stat': self.update_reward_red_point,
           'message_update_global_reward_receive': self.update_reward_red_point,
           'receive_task_prog_reward_succ_event': self.update_reward_red_point,
           'task_prog_changed': self.update_reward_red_point
           }
        return econf

    def _init_turntable_widget(self):

        def play_item_default_anim(nd, anim_name, item_id):
            if item_id not in ('201011151', '201800142', '201011100'):
                return
            for name in anim_name:
                nd.PlayAnimation(name)

        def play_item_chosen_anim(nd, anim_name, item_id):
            nd.PlayAnimation(anim_name)
            if item_id not in ('201011151', '201800142', '201011100', '208105625',
                               '208200328', '208200224'):
                return
            self.panel.PlayAnimation('ten_bg_receive_s')

        self.turntable_widget = LotteryTurntableWidget(self, self.panel, self.lottery_id, nd_click_name='btn_item_bg', item_anim_name_map={ITEM_DEFAULT_STATE: ('circulation', 'circulation_show'),
           ITEM_PASS_STATE: 'pass',
           ITEM_CHOSEN_STATE: 'choosed',
           ITEM_LOOP_STATE: 'loop'
           }, play_item_anim_func_map={ITEM_DEFAULT_STATE: play_item_default_anim,
           ITEM_CHOSEN_STATE: play_item_chosen_anim
           })

    def _init_exchange_reward_widget(self):

        def _check_need_anim(item_no):
            rare_degree = get_item_rare_degree(item_no)
            if rare_degree not in (RARE_DEGREE_4, RARE_DEGREE_6):
                return False
            item_type = get_lobby_item_type(item_no)
            if item_type not in RP_SKIN_TYPE:
                return False
            return True

        def pre_init_display_item(item_widget, item_no=None):
            if _check_need_anim(item_no):
                item_widget.RecordAnimationNodeState('show')
                item_widget.RecordAnimationNodeState('loop')

        def play_display_item_anim(item_widget, flag, item_no=None):
            item_widget.img_choose.setVisible(flag)
            if _check_need_anim(item_no):
                if flag:
                    item_widget.PlayAnimation('show')
                    item_widget.PlayAnimation('loop')
                else:
                    item_widget.StopAnimation('show')
                    item_widget.RecoverAnimationNodeState('show')
                    item_widget.StopAnimation('loop')
                    item_widget.RecoverAnimationNodeState('loop')

        self.exchange_reward_widget = LotteryExchangeRewardWidget(self, self.panel.node_2.temp_exchange, self.panel.node_2, self.panel.node_1, self.lottery_id, self.on_change_show_reward, nd_visibility_opposite_relatively=[
         'list_bar', 'lab_num_times'], pre_init_display_item=pre_init_display_item, play_display_item_anim=play_display_item_anim, nd_directly_show_visible=('img_title_1',
                                                                                                                                                             'nd_name_1'), nd_directly_show_invisible=('img_title',
                                                                                                                                                                                                       'nd_name'), nd_kind=('nd_name.temp_kind',
                                                                                                                                                                                                                            'nd_name_1.temp_kind'), nd_lab_name=('nd_name.lab_name',
                                                                                                                                                                                                                                                                 'nd_name_1.lab_name'), nd_btn_detail=('nd_name.lab_name.nd_auto_fit.btn_detail',
                                                                                                                                                                                                                                                                                                       'nd_name_1.lab_name.nd_auto_fit.btn_detail'))
        self.exchange_reward_widget.panel.PlayAnimation('bg_loop')
        return

    def _init_buy_widget(self):

        def buying_callback(lottery_count):
            self.turntable_widget.stop_turntable_item_state_anim(ITEM_DEFAULT_STATE)
            self.turntable_widget.play_turntable_animation(lottery_count)
            btn_anim_name = 'btn_once_click' if lottery_count == SINGLE_LOTTERY_COUNT else 'btn_repeat_click'
            if self.btn_click_anim_timer:
                global_data.game_mgr.unregister_logic_timer(self.btn_click_anim_timer)

            def play_btn_click_anim():
                self.panel.PlayAnimation(btn_anim_name)
                self.btn_click_anim_timer = None
                return

            self.btn_click_anim_timer = global_data.game_mgr.register_logic_timer(play_btn_click_anim, interval=3, times=1)

        def lottery_data_ready_callback(bought_successfully):
            if not bought_successfully:
                self.turntable_widget.lottery_failed()

        self.buy_widget = LotteryBuyWidget(self, self.panel, self.lottery_id, buy_button_info={SINGLE_LOTTERY_COUNT: self.panel.btn_once,
           CONTINUAL_LOTTERY_COUNT: self.panel.btn_repeat
           }, buy_price_info={SINGLE_LOTTERY_COUNT: self.panel.btn_once.temp_price,
           CONTINUAL_LOTTERY_COUNT: self.panel.btn_repeat.temp_price
           }, price_color=DARK_PRICE_COLOR, buying_callback=buying_callback, lottery_data_ready_callback=lottery_data_ready_callback)

    def on_finalize_panel(self):
        super(LotteryKizunaAIWidget, self).on_finalize_panel()
        if self.buy_widget:
            self.buy_widget.destroy()
            self.buy_widget = None
        if self.turntable_widget:
            self.turntable_widget.destroy()
            self.turntable_widget = None
        if self.exchange_reward_widget:
            self.exchange_reward_widget.destroy()
            self.exchange_reward_widget = None
        if self.btn_click_anim_timer:
            global_data.game_mgr.unregister_logic_timer(self.btn_click_anim_timer)
            self.btn_click_anim_timer = None
        return

    def show(self):
        self.panel.setVisible(True)
        global_data.emgr.set_lottery_reward_info_label_visible.emit(False)
        global_data.emgr.set_price_widget_close_btn_visible.emit('LotteryMainUI', False)
        if not self.exchange_reward_widget.visible and not self.is_visible_close:
            self.panel.PlayAnimation('show')
            self.panel.PlayAnimation('bg_loop')
            self.turntable_widget.play_turntable_item_state_anim(ITEM_DEFAULT_STATE)
        if self.is_visible_close:
            self.exchange_reward_widget.visible = True
        self.update_guarantee_lottery_info()

    def hide(self):
        self.panel.setVisible(False)
        global_data.emgr.set_lottery_reward_info_label_visible.emit(True)
        global_data.emgr.set_price_widget_close_btn_visible.emit('LotteryMainUI', True)
        self.panel.StopAnimation('show')
        self.panel.StopAnimation('bg_loop')

    def refresh(self):
        self.buy_widget.refresh()
        self.refresh_limited_item_guarantee_round()
        self.refresh_lottery_limit_count()
        self.update_guarantee_lottery_info()
        self.update_coin_num()

    def refresh_show_model(self, show_model_id=None):
        self.exchange_reward_widget.refresh_show_model(show_model_id)

    def on_receive_lottery_result(self, item_list, origin_list):
        self.turntable_widget.set_turntable_items_got(item_list, origin_list)

    def update_guarantee_lottery_info(self):
        self.has_bought_first_continual_lottery = global_data.player.get_reward_count(self.data['table_id']) >= 10
        self.panel.img_diban.setVisible(not self.has_bought_first_continual_lottery)
        self.turntable_widget.turntable_item_node_list[0].img_choujiang.setVisible(global_data.player.get_item_num_by_no(201011100) <= 0)

    def update_coin_num(self):
        self.panel.btn_shop.lab_num.SetString(str(global_data.player.get_item_num_by_no(SHOP_PAYMENT_KIZUNA_AI_EXCHANGE)))

    def set_visible_close(self, is_visible_close):
        self.is_visible_close = is_visible_close
        self.exchange_reward_widget.set_directly_show(is_visible_close, ('list_bar', ))

    def refresh_lottery_limit_count(self):
        if not is_mainland_package():
            return
        self.cur_lottery_count = global_data.player.get_lottery_per_day_num(self.lottery_id)
        global_data.emgr.refresh_lottery_limit_count.emit(self.lottery_id, self.max_lottery_count - self.cur_lottery_count, color=1248270)

    def on_lottery_ended(self):
        self.turntable_widget.play_turntable_item_state_anim(ITEM_DEFAULT_STATE)
        if self.turntable_widget.cur_draw_lottery_count == CONTINUAL_LOTTERY_COUNT:
            if self.btn_click_anim_timer:
                global_data.game_mgr.unregister_logic_timer(self.btn_click_anim_timer)
                self.btn_click_anim_timer = None
            self.panel.StopAnimation('btn_repeat_click')
            self.panel.PlayAnimation('ten_bg_hide')
        self.update_guarantee_lottery_info()
        self.refresh_limited_item_guarantee_round()
        self.update_coin_num()
        return

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
        from logic.gutils import activity_utils
        from logic.gcommon.common_const.activity_const import WIDGET_LOTTERY_KIZUNA_AI
        count = activity_utils.get_activity_red_point_count_by_widget_type(WIDGET_LOTTERY_KIZUNA_AI)
        self.panel.btn_reward_center.temp_new.setVisible(count > 0)