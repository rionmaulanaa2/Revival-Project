# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivityNile/ActivityWeekendBank.py
from __future__ import absolute_import
from logic.comsys.activity.ActivityTemplate import ActivityTemplate
from common.cfg import confmgr
from logic.gutils import task_utils
from logic.gutils.item_utils import get_lobby_item_name, get_lobby_item_pic_by_item_no, get_lobby_item_type
from logic.gcommon.time_utility import get_server_time, ONE_WEEK_SECONDS, ONE_DAY_SECONDS, get_utc8_week_start_timestamp, ONE_HOUR_SECONS
from logic.gcommon.common_const import ui_operation_const as uoc

class ActivityWeekendBank(ActivityTemplate):

    def on_init_panel(self):
        super(ActivityWeekendBank, self).on_init_panel()
        self.init_list()
        self.init_weekend_btn()
        self._init_season_time()
        conf = confmgr.get('c_activity_config', self._activity_type, default={})
        act_name_id = conf.get('iCatalogID', '')

        @self.panel.btn_describe.unique_callback()
        def OnClick(btn, touch):
            dlg = global_data.ui_mgr.show_ui('GameRuleDescUI', 'logic.comsys.common_ui')
            dlg.set_show_rule(get_text_by_id(act_name_id), get_text_by_id(conf.get('cRuleTextID', '')))

    def init_parameters(self):
        super(ActivityWeekendBank, self).init_parameters()
        self._task_id = confmgr.get('c_activity_config', self._activity_type, 'cTask', default='')
        conf = confmgr.get('c_activity_config', self._activity_type, 'cUiData', default={})
        self._one_task_points = conf.get('one_task_points', 10)
        self._points_item_id = conf.get('points_item_id', 50102006)

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'player_money_info_update_event': self.refresh_all,
           'task_prog_changed': self.refresh_all,
           'receive_task_reward_succ_event': self.refresh_all,
           'receive_task_prog_reward_succ_event': self.refresh_all
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def refresh_all(self, *args):
        self.init_list()
        self.init_weekend_btn()
        global_data.emgr.refresh_activity_redpoint.emit()

    def init_list(self):
        if not global_data.player:
            return
        _task_id = self._task_id
        children_tasks = task_utils.get_children_task(_task_id)
        total_cur_prog = global_data.player.get_task_prog(_task_id)
        total_prog = task_utils.get_total_prog(_task_id)
        self.panel.list_item.SetInitCount(len(children_tasks))
        for idx, task in enumerate(children_tasks):
            item_widget = self.panel.list_item.GetItem(idx)
            self.init_task_widget(item_widget, task)

    def init_task_widget(self, item_widget, task_id):
        has_unreceived_reward = global_data.player.has_unreceived_task_reward(task_id)
        reward_id = task_utils.get_task_reward(task_id)
        reward_conf = confmgr.get('common_reward_data', str(reward_id))
        reward_list = reward_conf.get('reward_list', [])
        reward_count = len(reward_list)
        for idx in range(reward_count):
            item_no, item_num = reward_list[idx]
            pic = get_lobby_item_pic_by_item_no(item_no)
            item_widget.img_item.SetDisplayFrameByPath('', get_lobby_item_pic_by_item_no(item_no))
            item_widget.lab_quantity.SetString(str(item_num))

        item_widget.bar_name.EnableCustomState(True)
        item_widget.bar_bg.EnableCustomState(True)
        has_rewarded = global_data.player.has_receive_reward(task_id)
        if has_rewarded:
            item_widget.nd_got.setVisible(True)
        else:
            item_widget.nd_got.setVisible(False)
        if has_unreceived_reward:
            item_widget.bar_name.SetSelect(True)
            item_widget.bar_bg.SetSelect(True)
            item_widget.lab_name.SetColor('#SW')
            item_widget.lab_quantity.SetColor('#SW')
            item_widget.lab_name.EnableShadow(12404505, 130, {'width': 1,'height': -1})
            item_widget.lab_quantity.SetOutLineColor(14062146)
        elif has_rewarded:
            item_widget.bar_name.SetShowEnable(True)
            item_widget.bar_bg.SetShowEnable(True)
            item_widget.lab_name.SetColor(15199231)
            item_widget.lab_quantity.SetColor(13884414)
            item_widget.lab_name.EnableShadow(3686569, 130, {'width': 1,'height': -1})
            item_widget.lab_quantity.SetOutLineColor(5002718)
        else:
            item_widget.bar_name.SetShowEnable(False)
            item_widget.bar_bg.SetShowEnable(False)
            item_widget.lab_name.SetColor(15199231)
            item_widget.lab_quantity.SetColor(13884414)
            item_widget.lab_name.EnableShadow(3686569, 130, {'width': 1,'height': -1})
            item_widget.lab_quantity.SetOutLineColor(5002718)

        @item_widget.bar_name.callback()
        def OnClick(btn, touch):
            if not global_data.player:
                return
            has_unreceived_reward = global_data.player.has_unreceived_task_reward(task_id)
            if has_unreceived_reward:
                global_data.player.receive_task_reward(task_id)

    def init_weekend_btn(self):
        is_enable = ActivityWeekendBank.is_at_weekend()
        _task_id = self._task_id
        finished_tasks_count = ActivityWeekendBank.get_signed_weekday_task_count(_task_id)
        cur_time = get_server_time()
        pass_time_since_last_received = cur_time - global_data.player.get_last_weekend_bank_reward_get_ts()
        can_received_weekend_bank = pass_time_since_last_received > 3 * ONE_DAY_SECONDS
        self.panel.temp_btn.btn_major.SetEnable(is_enable)
        if is_enable:
            if can_received_weekend_bank:
                if finished_tasks_count > 0:
                    self.panel.temp_btn.btn_major.SetText(80930)
                    self.panel.temp_btn.btn_major.SetEnable(True)
                else:
                    self.panel.temp_btn.btn_major.SetText(80930)
                    self.panel.temp_btn.btn_major.SetEnable(False)
            else:
                self.panel.temp_btn.btn_major.SetText(604029)
                self.panel.temp_btn.btn_major.SetEnable(False)
        else:
            self.panel.temp_btn.btn_major.SetText(80930)
            self.panel.temp_btn.btn_major.SetEnable(False)

        @self.panel.temp_btn.btn_major.callback()
        def OnClick(btn, touch):
            is_enable = self.is_at_weekend()
            if not is_enable:
                return
            if not finished_tasks_count > 0:
                return
            cur_time = get_server_time()
            pass_time_since_last_received = cur_time - global_data.player.get_last_weekend_bank_reward_get_ts()
            can_received_weekend_bank = pass_time_since_last_received > 3 * ONE_DAY_SECONDS
            if not can_received_weekend_bank:
                return
            global_data.player.set_last_weekend_bank_reward_get_ts(cur_time)
            global_data.player.call_server_method('req_weekend_bank_reward', ())
            self.panel.temp_btn.btn_major.SetText(604029)
            self.panel.temp_btn.btn_major.SetEnable(False)
            global_data.emgr.refresh_activity_redpoint.emit()

        from logic.gcommon.const import SHOP_PAYMENT_ITEM
        from logic.gutils.template_utils import init_price_template
        item_id = self._points_item_id
        bank_balance_info = '{}_{}'.format(SHOP_PAYMENT_ITEM, item_id)
        price_info = {'goods_payment': bank_balance_info,
           'original_price': finished_tasks_count * self._one_task_points,
           'real_price': finished_tasks_count * self._one_task_points
           }
        init_price_template(price_info, self.panel.nd_content.pnl_content.bar_price.temp_price, '#SW')

    @staticmethod
    def get_signed_weekday_task_count(_task_id):
        children_tasks = task_utils.get_children_task(_task_id)
        finished_tasks_count = 0
        for task in children_tasks[:5]:
            has_rewarded = global_data.player.has_receive_reward(task) or global_data.player.is_task_reward_receivable(task)
            if has_rewarded:
                finished_tasks_count += 1

        return finished_tasks_count

    @staticmethod
    def is_at_weekend():
        cur_time = get_server_time()
        cur_week_start = get_utc8_week_start_timestamp(cur_time)
        sat_5_am = cur_week_start + 5 * ONE_DAY_SECONDS + 5 * ONE_HOUR_SECONS
        mon_5_am = cur_week_start + 7 * ONE_DAY_SECONDS + 5 * ONE_HOUR_SECONS
        return mon_5_am > cur_time > sat_5_am

    def _init_season_time(self):
        from logic.gcommon.cdata import season_data
        from logic.gcommon import time_utility
        cur_season = global_data.player.get_battle_season()
        start_timestamp = season_data.get_start_timestamp(cur_season)
        end_timestamp = season_data.get_end_timestamp(cur_season)
        now = time_utility.time()
        if now < start_timestamp:
            self.panel.lab_time.SetString(608052)
        elif now > end_timestamp:
            self.panel.lab_time.SetString(608051)
        else:
            day, _, _, _ = time_utility.get_day_hour_minute_second(end_timestamp - now)
            self.panel.lab_time.SetString(get_text_by_id(608050).format(day))

    @staticmethod
    def show_tab_rp(activity_type):
        if not global_data.player:
            return False
        _task_id = confmgr.get('c_activity_config', str(activity_type), 'cTask', default='')
        finished_tasks_count = ActivityWeekendBank.get_signed_weekday_task_count(_task_id)
        if finished_tasks_count == 0:
            return False
        is_enable = ActivityWeekendBank.is_at_weekend()
        cur_time = get_server_time()
        pass_time_since_last_received = cur_time - global_data.player.get_last_weekend_bank_reward_get_ts()
        can_received_weekend_bank = pass_time_since_last_received > 3 * ONE_DAY_SECONDS
        return is_enable and can_received_weekend_bank