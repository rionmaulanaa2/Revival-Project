# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/lottery/LotteryActivityChooseUI.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
from common.const.uiconst import NORMAL_LAYER_ZORDER
from common.cfg import confmgr
from common.const import uiconst
from logic.gcommon.common_const import activity_const
from logic.gutils import template_utils
from logic.gutils import activity_utils
from logic.gutils.mall_utils import get_lottery_exchange_list
import logic.gcommon.time_utility as tutil
from logic.gutils import task_utils

class LotteryActivityChooseUI(BasePanel):
    PANEL_CONFIG_NAME = 'mall/activity_choose'
    DLG_ZORDER = NORMAL_LAYER_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    UI_ACTION_EVENT = {'btn_close.OnClick': '_on_click_close'
       }

    def on_init_panel(self, activity_types=None, **kwargs):
        self.init_parameters(activity_types)
        self._init_left_time()
        self._init_activity_list()
        self.process_event(True)
        self._play_appear_animation()

    def init_parameters(self, activity_types):
        if not activity_types:
            activity_types = activity_utils.get_lottery_activity_types()
        self._activity_types = activity_types
        self._activity_handlers = {activity_const.ACTIVITY_LOTTERY_TASK: self._init_lottery_task_item,
           activity_const.ACTIVITY_LOTTERY_EXCHANGE: self._init_lottery_exchange_item,
           activity_const.ACTIVITY_LOTTERY_GIFT: self._init_global_gift_item
           }
        self._types_2_ui_order = [
         activity_const.ACTIVITY_LOTTERY_TASK,
         activity_const.ACTIVITY_LOTTERY_EXCHANGE,
         activity_const.ACTIVITY_LOTTERY_GIFT]
        self._cur_activity_index = 0

    def process_event(self, flag):
        emgr = global_data.emgr
        econf = {'message_update_global_stat': self._on_message_update_global_stat,
           'message_update_global_reward_receive': self.update_redpoint,
           'receive_task_reward_succ_event': self.update_redpoint,
           'buy_good_success': self.update_redpoint
           }
        if flag:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def on_finalize_panel(self):
        self.process_event(False)
        self.panel.StopTimerAction()

    def update_redpoint(self, *args):
        for activity_type in self._activity_types:
            ui_item = self._get_ui_item(activity_type)
            if not ui_item:
                continue
            show_red_point = activity_utils.get_redpoint_count_by_type(activity_type) > 0
            ui_item.red_point.setVisible(show_red_point)

    def _init_activity_list(self):
        list_activity = self.panel.list_activity
        list_activity.DeleteAllSubItem()
        list_activity.SetInitCount(len(self._types_2_ui_order))
        for activity_type in self._types_2_ui_order:
            ui_item = self._get_ui_item(activity_type)
            if not ui_item:
                continue
            ui_item.RecordAnimationNodeState('show')
            handler = self._activity_handlers.get(activity_type)
            if handler:
                handler(activity_type, ui_item)
                continue

    def _get_ui_item(self, activity_type):
        if activity_type not in self._types_2_ui_order:
            return None
        else:
            index = self._types_2_ui_order.index(activity_type)
            return self.panel.list_activity.GetItem(index)

    def _on_click_close(self, *args):
        self.close()

    def _init_lottery_task_item(self, activity_type, ui_item):
        if activity_type not in self._activity_types:
            widget_index = self._types_2_ui_order.index(activity_type) + 1
            template_utils.init_mall_activity_item(ui_item, widget_index, get_text_by_id(12141), activity_opened=False)
            return
        conf = confmgr.get('c_activity_config', activity_type, default={})
        cUiData = conf.get('cUiData', {})
        tips_text = ''
        task_list = activity_utils.parse_task_list(conf['cTask'])
        if task_list:
            parent_task_id = task_list[0]
            children_task_list = task_utils.get_children_task(parent_task_id)
            if children_task_list:
                total_prog = task_utils.get_total_prog(children_task_list[-1])
                cur_prog = global_data.player.get_task_prog(children_task_list[-1])
                tips_text = get_text_by_id(cUiData.get('format_text_id')).format(cur_prog, total_prog)
        show_red_point = activity_utils.get_redpoint_count_by_type(activity_type) > 0
        widget_index = self._types_2_ui_order.index(activity_type) + 1
        template_utils.init_mall_activity_item(ui_item, widget_index, get_text_by_id(conf.get('cNameTextID')), tips_text, show_red_point)

        @ui_item.btn_bar.unique_callback()
        def OnClick(btn, touch, item_widget=ui_item):
            self._check_activity_click_red_point(item_widget, activity_type)
            from logic.comsys.lottery.LotteryTaskUI import LotteryTaskUI
            if activity_utils.is_activity_finished(activity_const.ACTIVITY_LOTTERY_TASK):
                global_data.game_mgr.show_tip(get_text_by_id(607177))
                return
            else:
                LotteryTaskUI(None, activity_const.ACTIVITY_LOTTERY_TASK)
                return

    def _init_lottery_exchange_item(self, activity_type, ui_item):
        if activity_type not in self._activity_types:
            widget_index = self._types_2_ui_order.index(activity_type) + 1
            template_utils.init_mall_activity_item(ui_item, widget_index, get_text_by_id(12125), activity_opened=False)
            return
        conf = confmgr.get('c_activity_config', activity_type, default={})
        cUiData = conf.get('cUiData', {})
        from logic.gcommon.const import SHOP_PAYMENT_LOTTERY_EXCHANGE
        item_amount = global_data.player.get_item_num_by_no(SHOP_PAYMENT_LOTTERY_EXCHANGE)
        tips_text = get_text_by_id(cUiData.get('format_text_id')).format(item_amount)
        show_red_point = activity_utils.get_redpoint_count_by_type(activity_type) > 0
        widget_index = self._types_2_ui_order.index(activity_type) + 1
        template_utils.init_mall_activity_item(ui_item, widget_index, get_text_by_id(conf.get('cNameTextID')), tips_text, show_red_point)

        @ui_item.btn_bar.unique_callback()
        def OnClick(btn, touch, item_widget=ui_item, act_type=activity_type):
            if activity_utils.is_activity_finished(act_type):
                global_data.game_mgr.show_tip(get_text_by_id(607177))
                return
            else:
                self._check_activity_click_red_point(item_widget, activity_type)
                exchange_lottery_list, _ = get_lottery_exchange_list()
                if not exchange_lottery_list:
                    global_data.game_mgr.show_tip(get_text_by_id(12128))
                    return
                from logic.comsys.lottery.LotteryExchangeMallUI import LotteryExchangeMallUI
                LotteryExchangeMallUI(None, exchange_lottery_list)
                return

    def _init_global_gift_item(self, activity_type, ui_item):
        if activity_type not in self._activity_types:
            widget_index = self._types_2_ui_order.index(activity_type) + 1
            template_utils.init_mall_activity_item(ui_item, widget_index, get_text_by_id(12131), activity_opened=False)
            return
        conf = confmgr.get('c_activity_config', activity_type, default={})
        cUiData = conf.get('cUiData', {})
        format_text_id = cUiData.get('format_text_id')
        conf = confmgr.get('c_activity_config', activity_type)
        tips_text = get_text_by_id(format_text_id).format(self._get_global_gift_progress())
        show_red_point = activity_utils.get_redpoint_count_by_type(activity_type) > 0
        widget_index = self._types_2_ui_order.index(activity_type) + 1
        template_utils.init_mall_activity_item(ui_item, widget_index, get_text_by_id(conf.get('cNameTextID')), tips_text, show_red_point)
        ui_item.lab_tips.setVisible(False)

        @ui_item.btn_bar.unique_callback()
        def OnClick(btn, touch, item_widget=ui_item, act_type=activity_type):
            if activity_utils.is_activity_finished(act_type):
                global_data.game_mgr.show_tip(get_text_by_id(607177))
                return
            else:
                self._check_activity_click_red_point(item_widget, activity_type)
                from logic.comsys.lottery.LotteryGiftsUI import LotteryGiftsUI
                LotteryGiftsUI(None, activity_const.ACTIVITY_LOTTERY_GIFT)
                return

    def _get_global_gift_progress(self):
        parent_id = '990018'
        global_stat_data = global_data.player or {} if 1 else global_data.player.get_global_stat_data()
        if global_stat_data:
            children_achieves = activity_utils.get_child_achieves_from_parent(parent_id)
            if children_achieves:
                achieve_name = confmgr.get('global_achieve_data', str(children_achieves[0]), 'cGStatName', default='')
                latest_num = global_stat_data.get(str(parent_id), {}).get(achieve_name, 0)
                return latest_num
        return 0

    def _on_message_update_global_stat(self, *args):
        latest_num = self._get_global_gift_progress()
        ui_item = self.panel.list_activity.GetItem(self._activity_types.index(activity_const.ACTIVITY_LOTTERY_GIFT))
        if not ui_item:
            return
        ui_item.lab_tips.setVisible(False)

    def _init_left_time(self):
        conf = confmgr.get('c_activity_config', activity_const.ACTIVITY_LOTTERY_EXCHANGE)
        start_date = tutil.get_date_str('%Y.%m.%d', conf.get('cBeginTime', 0))
        finish_date = tutil.get_date_str('%m.%d', conf.get('cEndTime', 0))
        self.panel.lab_time.SetString(get_text_by_id(604006).format(start_date, finish_date))

    def _play_appear_animation(self):

        def reset():
            if self and self.is_valid():
                self._play_loop_animation()
                self.panel.StopTimerAction()

        def tick_callback(delta, from_timer=True):
            if self and self.is_valid():
                if from_timer and self._cur_activity_index == 0:
                    return
                ui_item = self.panel.list_activity.GetItem(self._cur_activity_index)
                if ui_item:
                    ui_item.PlayAnimation('show')
                self._cur_activity_index = (self._cur_activity_index + 1) % len(self._types_2_ui_order)

        self.panel.PlayAnimation('appear')
        tick_callback(0, from_timer=False)
        ui_item = self.panel.list_activity.GetItem(0)
        animation_duration = ui_item.GetAnimationMaxRunTime('show')
        self.panel.TimerAction(tick_callback, animation_duration * len(self._types_2_ui_order), reset, interval=0.2)

    def _play_loop_animation(self):

        def big_loop_callback(*args):
            if self and self.is_valid():
                self.panel.PlayAnimation('loop')
                self.panel.SetTimeOut(self.panel.GetAnimationMaxRunTime('loop'), big_loop_callback)
                small_loop_callback()

        def small_loop_callback(*args):
            if self and self.is_valid():
                ui_item = self.panel.list_activity.GetItem(self._cur_activity_index)
                if ui_item:
                    activity_type = self._types_2_ui_order[self._cur_activity_index]
                    if activity_type in self._activity_types:
                        animation_name = 'loop_%d' % (self._cur_activity_index + 1)
                        ui_item.PlayAnimation(animation_name)
                        self._cur_activity_index = (self._cur_activity_index + 1) % len(self._types_2_ui_order)
                        if self._cur_activity_index == 0:
                            return
                        self.panel.SetTimeOut(ui_item.GetAnimationMaxRunTime(animation_name), small_loop_callback)
                    else:
                        self._cur_activity_index = (self._cur_activity_index + 1) % len(self._types_2_ui_order)
                        if self._cur_activity_index == 0:
                            return
                        small_loop_callback()

        big_loop_callback()

    def _check_activity_click_red_point(self, item_widget, activity_type):
        if not global_data.player or not item_widget:
            return
        if activity_type not in self._activity_types:
            item_widget.red_point.setVisible(False)
            return
        global_data.player.save_activity_click_data(activity_type)
        show_red_point = activity_utils.get_redpoint_count_by_type(activity_type) > 0
        item_widget.red_point.setVisible(show_red_point)
        global_data.emgr.refresh_activity_redpoint.emit()