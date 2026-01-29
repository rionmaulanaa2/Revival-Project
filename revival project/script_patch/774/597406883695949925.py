# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/task/SeasonTaskWidget.py
from __future__ import absolute_import
import six
from six.moves import range
from functools import cmp_to_key
from .CommonTaskWidget import CommonTaskWidget
from common.const.uiconst import NORMAL_LAYER_ZORDER, BG_ZORDER
from common.framework import Functor
from common.cfg import confmgr
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gutils.template_utils import init_common_reward_list_simple
from logic.gcommon.item.item_const import ITEM_UNGAIN, ITEM_UNRECEIVED, ITEM_RECEIVED, ITEM_NO_TASK_CARD
from logic.gutils import task_utils
from logic.gutils import system_unlock_utils
from logic.gutils.battle_pass_utils import refresh_battlepass_lv_item
from logic.comsys.mall_ui.BuyConfirmUIInterface import groceries_buy_confirmUI
from logic.client.const.mall_const import TASK_CARD_GOODS_ID
from logic.gcommon import time_utility
from logic.gcommon.common_const import battlepass_const
from logic.comsys.common_ui.NormalConfirmUI import SecondConfirmDlg2
from logic.gutils.new_template_utils import CommonLeftTabList

class SeasonTaskWidget(CommonTaskWidget):
    TAB_WEEK_TASK = 1
    TAB_BATTLE_TIME_TASK = 2

    def __init__(self, parent, panel, task_type):
        super(SeasonTaskWidget, self).__init__(parent, panel, task_type)
        temp_content = getattr(self.panel.nd_cut, 'temp_content')
        pos = temp_content.GetPosition()
        self.nd_content = global_data.uisystem.load_template_create('task/i_battle_pass_task')
        self.panel.nd_cut.AddChild('season_task', self.nd_content)
        self.nd_content.setAnchorPoint(temp_content.getAnchorPoint())
        self.nd_content.SetPosition(*pos)
        self.sview_index_dict = {}
        self.sview_content_height_dict = {}
        self.bt_sview_index = 0
        self.bt_sview_content_height = 0
        self.is_bt_check_sview = False
        self.task_ids_dict = {}
        self.bt_task_ids = []
        self.cur_week_no = 0
        self.ui_view_list = None
        self.task_timers = {}
        self.cur_task_content = None
        self.cur_left_tab_type = None
        return

    def init_event(self):
        super(SeasonTaskWidget, self).init_event()
        global_data.emgr.start_new_season_week_event += self._start_new_season_week_task
        global_data.emgr.receive_task_reward_succ_event += self._refresh_red_point
        global_data.emgr.receive_task_reward_succ_event += self._refresh_receive_all_btn
        global_data.emgr.season_pass_update_lv += self._refresh_battlepass_lv
        global_data.emgr.season_pass_open_type += self._open_battlepass_type
        global_data.emgr.on_lobby_bag_item_changed_event += self._refresh_task_card_num

    def init_widget(self, need_hide=True):
        super(SeasonTaskWidget, self).init_widget(need_hide)
        self.init_battlepass_info()
        self.init_task_widget()
        self.init_left_tab_list()
        self._refresh_left_bt_tab_red_point()
        self._refresh_left_week_tab_red_point()
        self._refresh_receive_all_btn()

    def init_left_tab_list(self):
        list_tab = self.nd_content.list_tab
        week_tab = list_tab.GetItem(0)
        week_tab.lab_discard.SetString(602007)
        bt_tab = list_tab.GetItem(1)
        bt_tab.lab_discard.SetString(602046)

        @week_tab.unique_callback()
        def OnClick(btn, touch):
            self.is_bt_check_sview = True
            self.is_check_sview = False
            self.show_week_task()
            week_tab.SetSelect(True)
            week_tab.lab_discard.SetColor(16448250)
            bt_tab.lab_discard.SetColor(4409733)
            bt_tab.SetSelect(False)

        @bt_tab.unique_callback()
        def OnClick(btn, touch):
            self.is_bt_check_sview = False
            self.is_check_sview = True
            self.show_battle_time_task()
            week_tab.SetSelect(False)
            bt_tab.lab_discard.SetColor(16448250)
            week_tab.lab_discard.SetColor(4409733)
            bt_tab.SetSelect(True)

        from logic.vscene.parts.ctrl.InputMockHelper import TouchMock
        week_tab.OnClick(TouchMock())

    def init_battlepass_info(self):
        battle_season = global_data.player.get_battle_season()
        from logic.gcommon.cdata import season_data
        end_timestamp = season_data.get_end_timestamp(battle_season)
        if end_timestamp:
            end_date = time_utility.get_utc8_datetime(end_timestamp)
            self.nd_content.lab_date.SetString(get_text_by_id(80832).format(end_date.year, end_date.month, end_date.day))
        else:
            self.nd_content.lab_date.SetString('-')
        bp_lv, bp_point = global_data.player.get_battlepass_info()
        self._refresh_battlepass_lv(bp_lv, bp_point)

        @self.nd_content.btn_describe.unique_callback()
        def OnClick(btn, touch):
            from logic.comsys.common_ui.GameRuleDescUI import GameRuleDescUI
            dlg = GameRuleDescUI()
            dlg.set_show_rule(get_text_by_id(602019), get_text_by_id(602020))

        @self.nd_content.nd_pass_level.temp_btn_go.btn_common.unique_callback()
        def OnClick(btn, touch):
            from logic.gutils import jump_to_ui_utils
            jump_to_ui_utils.jump_to_season_pass(None)
            return

    def _open_battlepass_type(self, battlepass_type):
        for task_id, nd_task_item in six.iteritems(self.task_dict):
            if task_utils.need_active_high_battlepass(task_id):
                self._set_task_reward_status(nd_task_item)
                self.refresh_battlepass_status(nd_task_item)

        self._refresh_left_week_tab_red_point()
        self._refresh_all_week_task_red_point()

    def show_week_task(self):
        if self.cur_left_tab_type == self.TAB_WEEK_TASK:
            return
        else:
            self.cur_left_tab_type = self.TAB_WEEK_TASK
            total_week_num = global_data.player.get_season_task_week_num()
            if not self.cur_week_no:
                rp_week = None
                for week in range(1, total_week_num + 1):
                    if self.check_week_red_point(week):
                        rp_week = week
                        break

                if rp_week:
                    week_no = rp_week
                else:
                    week_no = global_data.player.get_cur_season_week_no()
                week_no = max(1, week_no)
                week_no = min(week_no, total_week_num)
                season_content = self.get_season_task_content(self.TAB_WEEK_TASK, week_no)
                if season_content and week_no and self.nd_content.pnl_list_top_tab.GetItemCount() >= week_no:
                    self.on_click_season_week(None, week_no - 1)
                    tab_item = self.nd_content.pnl_list_top_tab.GetItem(week_no - 1)
                    self.refresh_top_tab(week_no)
                    self.nd_content.pnl_list_top_tab.CenterWithNode(tab_item)
            else:
                self.on_click_season_week(None, self.cur_week_no - 1)
            self.nd_content.temp_week_task.setVisible(False)
            self.nd_content.img_week_task.setVisible(False)
            self.nd_content.pnl_list_top_tab.setVisible(True)
            self.nd_content.img_top_tab.setVisible(True)
            return

    def show_battle_time_task(self):
        if self.cur_left_tab_type == self.TAB_BATTLE_TIME_TASK:
            return
        self.cur_left_tab_type = self.TAB_BATTLE_TIME_TASK
        if self.cur_task_content:
            self.cur_task_content.setVisible(False)
        task_content = self.get_season_task_content(self.TAB_BATTLE_TIME_TASK)
        self.cur_task_content = task_content
        self.nd_content.task_list_content.SetContentSize(674, 489)
        self.nd_content.task_list_content.SetPosition('50%139', '50%174')
        self.nd_content.task_list_content.ChildResizeAndPosition()
        if task_content:
            task_content.setVisible(True)
            self.ui_view_list = task_content.list_task
        if not self.bt_task_ids:
            self.init_battle_task_content()
        self.nd_content.temp_week_task.setVisible(True)
        self.nd_content.img_week_task.setVisible(True)
        self.nd_content.pnl_list_top_tab.setVisible(False)
        self.nd_content.img_top_tab.setVisible(False)

    def init_task_widget(self):
        total_week_num = global_data.player.get_season_task_week_num()
        data_list = []
        for week in range(1, total_week_num + 1):
            data_list.append({'text': get_text_by_id(602016, (week,))})

        self.init_seasontask_top_tab_list(self.nd_content.pnl_list_top_tab, data_list, self.on_click_season_week)
        for week in range(1, total_week_num + 1):
            self.refresh_top_tab(week)

        @self.nd_content.temp_get_all.btn_common_big.callback()
        def OnClick(btn, touch):
            task_list = list(self.get_task_ids(self.TAB_BATTLE_TIME_TASK))
            season_bt_parent_task_id = global_data.player.get_season_bt_parent_task()
            task_list.append(season_bt_parent_task_id)
            for _week in range(1, global_data.player.get_cur_season_week_no() + 1):
                task_list.extend(self.get_task_ids(self.TAB_WEEK_TASK, _week))

            global_data.player.receive_tasks_reward(task_list)

    def init_seasontask_top_tab_list(self, nd_list, data_list, click_cb):
        nd_list.DeleteAllSubItem()
        nd_list.SetInitCount(len(data_list))
        for idx, item in enumerate(nd_list.GetAllItem()):
            info = data_list[idx]
            text = info.get('text', '')
            if text:
                item.lab_week_1.SetString(text)
                item.lab_week_2.SetString(text)
                item.lab_week_3.SetString(text)

            @item.btn_tab.callback()
            def OnClick(btn, touch, item=item, idx=idx):
                click_cb(item, idx)
                for _idx, _item in enumerate(nd_list.GetAllItem()):
                    self._refresh_week_tab(_idx, _item, idx)

    def _refresh_week_tab(self, idx, tab_item, cur_select):
        tab_item.lab_week_1.setVisible(False)
        tab_item.lab_week_2.setVisible(False)
        tab_item.lab_week_3.setVisible(False)
        tab_item.lab_schedule.setVisible(False)
        cur_season_week = global_data.player.get_cur_season_week_no()
        if idx >= cur_season_week:
            tab_item.lab_week_3.setVisible(True)
            tab_item.btn_tab.SetSelect(idx == cur_select)
        elif idx != cur_select:
            tab_item.lab_week_2.setVisible(True)
            tab_item.btn_tab.SetSelect(False)
        else:
            tab_item.lab_week_1.setVisible(True)
            tab_item.btn_tab.SetSelect(True)
            tab_item.lab_schedule.setVisible(True)

    def _start_new_season_week_task(self):
        week = global_data.player.get_cur_season_week_no()
        total_week_num = global_data.player.get_season_task_week_num()
        if week > total_week_num:
            return
        self.refresh_top_tab(week)
        if self.cur_week_no == week and self.cur_left_tab_type:
            self.init_week_task_content(week, False)

    def _refresh_battlepass_lv(self, lv, point):
        refresh_battlepass_lv_item(self.nd_content, lv, point)

    @staticmethod
    def get_task_ids(tab_type, week=0):
        if tab_type == SeasonTaskWidget.TAB_WEEK_TASK:
            return global_data.player.get_season_task_ids(week)
        if tab_type == SeasonTaskWidget.TAB_BATTLE_TIME_TASK:
            return global_data.player.get_season_battle_time_task_ids()

    def on_click_season_week(self, item, index):
        self.cur_week_no = index + 1
        if self.cur_task_content:
            self.cur_task_content.setVisible(False)
        season_week_content = self.get_season_task_content(self.TAB_WEEK_TASK, self.cur_week_no)
        if season_week_content:
            season_week_content.setVisible(True)
            self.ui_view_list = season_week_content.list_task
        self.cur_task_content = season_week_content
        self.nd_content.task_list_content.SetContentSize(674, 532)
        self.nd_content.task_list_content.SetPosition('50%139', '50%217')
        self.nd_content.task_list_content.ChildResizeAndPosition()
        if self.cur_week_no not in self.task_ids_dict:
            self.init_week_task_content(self.cur_week_no, False)

    def refresh_top_tab(self, week):
        cur_season_week = global_data.player.get_cur_season_week_no()
        tab_item = self.nd_content.pnl_list_top_tab.GetItem(week - 1)
        if week <= cur_season_week:
            if self.check_week_red_point(week):
                tab_item.img_red_dot.setVisible(True)
            else:
                tab_item.img_red_dot.setVisible(False)
            week_task_ids = global_data.player.get_season_task_ids(week)
            cnt, total_cnt = self.cal_finished_task_cnt(week_task_ids)
            tab_item.lab_schedule.SetString('{}/{}'.format(cnt, total_cnt))
        self._refresh_week_tab(week - 1, tab_item, self.cur_week_no - 1)

    def cal_finished_task_cnt(self, task_ids):
        cnt = 0
        toital_cnt = 0
        for task_id in task_ids:
            if task_utils.get_parent_task(task_id):
                return
            if global_data.player.is_task_finished(task_id):
                cnt += 1
            toital_cnt += 1

        return (
         cnt, toital_cnt)

    def init_battle_task_content(self):
        season_content = self.get_season_task_content(self.TAB_BATTLE_TIME_TASK)
        if not season_content:
            return
        bt_season_parent_task = global_data.player.get_season_bt_parent_task()
        if bt_season_parent_task:
            self.init_temp_week_task_item(self.nd_content.temp_week_task, bt_season_parent_task)
            self._refresh_temp_week_task()
        season_content.nd_empty.setVisible(False)
        season_content.list_task.setVisible(True)
        task_ids = self.get_task_ids(self.TAB_BATTLE_TIME_TASK)
        task_ids.sort(key=cmp_to_key(task_utils.sort_task_func))
        self.bt_task_ids = task_ids
        index = 0
        sview_height = season_content.list_task.getContentSize().height
        self.bt_sview_content_height = 0
        task_num = len(self.bt_task_ids)
        vert_indent = season_content.list_task.GetVertIndent()
        while self.bt_sview_content_height <= sview_height and index < task_num:
            task_id = self.bt_task_ids[index]
            nd_task_item = self.add_task_data(task_id, True, index, season_content.list_task)
            item_height = nd_task_item.getContentSize().height
            self.bt_sview_content_height += item_height
            index += 1

        self.bt_sview_index = index - 1
        season_content.list_task.addEventListener(self.bt_scroll_callback)

    def bt_scroll_callback(self, *args):
        if not self.is_bt_check_sview:
            self.is_bt_check_sview = True
            certificate_content = self.get_season_task_content(self.TAB_BATTLE_TIME_TASK)
            if certificate_content:
                certificate_content.SetTimeOut(0.021, self.check_bt_sview)

    def check_bt_sview(self, *args):
        task_num = len(self.bt_task_ids)
        self.bt_sview_index = self.ui_view_list.AutoAddAndRemoveItem_MulCol(self.bt_sview_index, self.bt_task_ids, task_num, self.add_task_data, 300, 300, self.on_del_task_item)
        self.is_bt_check_sview = False

    def add_task_data(self, task_id, is_back_item=True, index=-1, ui_list=None):
        if ui_list:
            view_list = ui_list if 1 else self.ui_view_list
            if is_back_item:
                nd_task_item = view_list.AddTemplateItem(bRefresh=True)
            else:
                nd_task_item = view_list.AddTemplateItem(0, bRefresh=True)
            return nd_task_item or None
        else:
            self.init_task_item(nd_task_item, task_id)
            return nd_task_item

    def init_week_task_content(self, week, need_hide=True):
        season_content = self.get_season_task_content(self.TAB_WEEK_TASK, week)
        if not season_content:
            return
        self.ui_view_list = season_content.list_task
        cur_season = global_data.player.get_battle_season()
        cur_season_week = global_data.player.get_cur_season_week_no()
        from logic.gcommon.cdata import season_data
        if week > cur_season_week:

            def show_count_down(seconds):
                left_time_str = time_utility.get_readable_time_day_hour_minitue(seconds)
                if seconds > 0:
                    season_content.DelayCall(1, lambda : show_count_down(seconds - 1))
                season_content.nd_empty.lab_unlock.SetString(get_text_by_id(602017, (left_time_str,)))

            season_content.nd_empty.setVisible(True)
            start_timestamp = season_data.get_start_timestamp(cur_season)
            start_datetime = time_utility.get_utc8_datetime(start_timestamp)
            now = time_utility.time()
            cur_fresh_time = time_utility.get_utc8_week_start_timestamp(now) + start_datetime.weekday() * time_utility.ONE_DAY_SECONDS + start_datetime.hour * time_utility.ONE_HOUR_SECONS
            if cur_fresh_time > now:
                seconds = (week - cur_season_week - 1) * time_utility.ONE_WEEK_SECONDS + cur_fresh_time - now
            else:
                seconds = (week - cur_season_week) * time_utility.ONE_WEEK_SECONDS + cur_fresh_time - now
            show_count_down(seconds)
            season_content.list_task.setVisible(False)
        else:
            season_content.nd_empty.setVisible(False)
            season_content.list_task.setVisible(True)
            task_ids = self.get_task_ids(self.TAB_WEEK_TASK, week)
            task_ids.sort(key=cmp_to_key(task_utils.sort_task_func))
            self.task_ids_dict[week] = task_ids
            index = 0
            if self.cur_left_tab_type == self.TAB_WEEK_TASK:
                self.nd_content.task_list_content.SetContentSize(674, 532)
                self.nd_content.task_list_content.SetPosition('50%139', '50%217')
                self.nd_content.task_list_content.ChildResizeAndPosition()
            sview_height = season_content.list_task.getContentSize().height
            self.sview_content_height_dict[week] = 0
            task_num = len(self.task_ids_dict[week])
            vert_indent = season_content.list_task.GetVertIndent()
            while self.sview_content_height_dict[week] <= sview_height and index < task_num:
                task_id = self.task_ids_dict[week][index]
                nd_task_item = self.add_task_data(task_id, True, season_content.list_task)
                item_height = nd_task_item.getContentSize().height
                self.sview_content_height_dict[week] += item_height
                index += 1

            self.sview_index_dict[week] = index - 1
            season_content.list_task.addEventListener(self.scroll_callback)
        if need_hide:
            season_content.setVisible(False)
        self._refresh_task_card_num()

    def cancel_unlock_timer(self, week):
        if week in self.task_timers:
            timer = self.task_timers[week]
            if timer:
                timer.cancel()

    def _on_update_task_prog(self, task_changes):
        super(SeasonTaskWidget, self)._on_update_task_prog(task_changes)
        for task_change in task_changes:
            task_id = task_change.task_id
            if task_id == global_data.player.get_season_bt_parent_task():
                self._refresh_temp_week_task()
            season_task_data = confmgr.get('task/season_task_data', default={})
            week_no = season_task_data.get(task_id, {}).get('season_week', None)
            if week_no:
                self.refresh_top_tab(week_no)

        self._refresh_receive_all_btn()
        return

    def _refresh_temp_week_task(self):
        season_bt_parent_task = global_data.player.get_season_bt_parent_task()
        last_bt_id = max(global_data.player.get_season_battle_time_task_ids())
        day_task_prog = global_data.player.get_task_day_prog(last_bt_id)
        self.nd_content.temp_week_task.lab_task_content.SetString(get_text_by_id(602047).format(day_task_prog))
        cur_prog = global_data.player.get_task_prog(season_bt_parent_task)
        total_prog = task_utils.get_total_prog(season_bt_parent_task)
        self.nd_content.temp_week_task.progress_exp.SetPercentage(cur_prog * 100.0 / total_prog)
        self.nd_content.temp_week_task.lab_num_exp.SetString(str(cur_prog))
        self.nd_content.temp_week_task.lab_num_exp_need.SetString('/' + str(total_prog))

    def resort_on_update_task_prog(self, task_id):
        season_task_data = confmgr.get('task/season_task_data', default={})
        week_no = season_task_data.get(task_id, {}).get('season_week', None)
        if week_no is None:
            return
        else:
            if week_no == 0:
                season_content = self.get_season_task_content(self.TAB_BATTLE_TIME_TASK)
            else:
                season_content = self.get_season_task_content(self.TAB_WEEK_TASK, week_no)
            if not season_content:
                return
            if week_no == 0:
                task_ids = self.bt_task_ids
            else:
                if week_no not in self.task_ids_dict:
                    return
                task_ids = self.task_ids_dict[week_no]
            if task_id not in task_ids:
                return
            list_task = season_content.list_task
            self._dynamic_ajust_task_list(list_task, task_ids, task_id)
            lst_task_id = list_task.GetItem(-1).task_id
            if lst_task_id not in task_ids:
                return
            if week_no == 0:
                self.bt_sview_index = task_ids.index(lst_task_id)
            else:
                self.sview_index_dict[week_no] = task_ids.index(lst_task_id)
            return

    def scroll_callback(self, *args):
        if not self.is_check_sview:
            self.is_check_sview = True
            certificate_content = self.get_season_task_content(self.TAB_WEEK_TASK, self.cur_week_no)
            if certificate_content:
                certificate_content.SetTimeOut(0.021, self.check_sview)

    def check_sview(self, *args):
        if self.cur_week_no not in self.task_ids_dict or self.cur_week_no not in self.sview_index_dict:
            return
        task_num = len(self.task_ids_dict[self.cur_week_no])
        self.sview_index_dict[self.cur_week_no] = self.ui_view_list.AutoAddAndRemoveItem(self.sview_index_dict[self.cur_week_no], self.task_ids_dict[self.cur_week_no], task_num, self.add_task_data, 300, 300, self.on_del_task_item)
        self.is_check_sview = False

    def get_season_task_content(self, tab_type, week=0):
        if tab_type == self.TAB_WEEK_TASK and week == 1:
            return self.nd_content.task_list_content.temp_content
        if tab_type == self.TAB_BATTLE_TIME_TASK:
            nd_name = 'nd_season_battle_time'
        else:
            nd_name = 'nd_season_%s' % week
        if not getattr(self.nd_content.task_list_content, nd_name):
            temp_content = self.nd_content.task_list_content.temp_content
            pos = temp_content.GetPosition()
            season_content = global_data.uisystem.load_template_create('task/i_task_season_content')
            self.nd_content.task_list_content.AddChild(nd_name, season_content)
            season_content.setAnchorPoint(temp_content.getAnchorPoint())
            season_content.ResizeAndPosition()
            season_content.SetPosition(*pos)
        return getattr(self.nd_content.task_list_content, nd_name)

    def init_temp_week_task_item(self, nd_task_item, task_id):
        task_conf = task_utils.get_task_conf_by_id(task_id)
        nd_task_item.lab_task_name.SetString(task_utils.get_task_name(task_id))
        self.task_dict[task_id] = nd_task_item
        nd_task_item.task_id = task_id
        reward_id = task_conf.get('reward', None)
        init_common_reward_list_simple(nd_task_item.list_award, reward_id)
        self._set_task_reward_status(nd_task_item)
        self._init_season_task_ui_event(nd_task_item)
        return

    def init_task_item(self, nd_task_item, task_id):
        task_conf = task_utils.get_task_conf_by_id(task_id)
        nd_task_item.lab_task_name.SetString(task_utils.get_task_name(task_id))
        self.task_dict[task_id] = nd_task_item
        nd_task_item.task_id = task_id
        self._set_task_item_progress(nd_task_item)
        reward_id = task_conf.get('reward', None)
        init_common_reward_list_simple(nd_task_item.list_award, reward_id)
        for reward_btn in nd_task_item.list_award.GetAllItem():
            reward_btn.SetClipObjectRecursion(self.ui_view_list)

        self._set_task_reward_status(nd_task_item)
        self._init_season_task_ui_event(nd_task_item)
        self._set_cost_card_num(nd_task_item)
        self.refresh_battlepass_status(nd_task_item)
        return

    def _set_cost_card_num(self, nd_task_item):
        cost_card_num = task_utils.get_cost_task_card_num(nd_task_item.task_id)
        has_card_num = global_data.player.get_item_num_by_no(ITEM_NO_TASK_CARD)
        num_str = get_text_by_id(602012) + str(task_utils.get_cost_task_card_num(nd_task_item.task_id))
        if not cost_card_num:
            return
        if cost_card_num > has_card_num:
            nd_task_item.lab_num.SetColor('#SR')
            nd_task_item.lab_num.SetString(num_str)
        else:
            nd_task_item.lab_num.SetColor('#SW')
            nd_task_item.lab_num.SetString(num_str)

    def _init_season_task_ui_event(self, nd_task_item):

        def active_high_battlepass():
            from logic.gutils import jump_to_ui_utils
            jump_to_ui_utils.jump_to_buy_season_pass_card()

        def buy_task_card():
            groceries_buy_confirmUI(goods_id=TASK_CARD_GOODS_ID)

        @nd_task_item.temp_btn_finish.btn_common.unique_callback()
        def OnClick(btn, touch):
            if task_utils.need_active_high_battlepass(nd_task_item.task_id) and not global_data.player.has_activate_battlepass_type():
                SecondConfirmDlg2().confirm(content=get_text_by_id(608055), confirm_callback=active_high_battlepass)
                return
            else:
                cost_card_num = task_utils.get_cost_task_card_num(nd_task_item.task_id)
                has_card_num = global_data.player.get_item_num_by_no(ITEM_NO_TASK_CARD)

                def use_task_card():
                    items = global_data.player.get_items_by_no(ITEM_NO_TASK_CARD)
                    for item in items:
                        item_num = item.get_current_stack_num()
                        if item_num < cost_card_num:
                            continue
                        else:
                            global_data.player.use_item(item.get_id(), cost_card_num, {'task_id': str(nd_task_item.task_id)})
                            break

                if cost_card_num <= has_card_num:
                    SecondConfirmDlg2().confirm(content=get_text_by_id(608056).format(cost_card_num, has_card_num), confirm_callback=use_task_card)
                    return
                SecondConfirmDlg2().confirm(content=get_text_by_id(608057).format(has_card_num), confirm_callback=buy_task_card)
                return

        @nd_task_item.temp_btn_get.btn_common.unique_callback()
        def OnClick(btn, touch):
            global_data.player.receive_task_reward(nd_task_item.task_id)

        @nd_task_item.btn_get_upgrade.unique_callback()
        def OnClick(btn, touch):
            SecondConfirmDlg2().confirm(content=get_text_by_id(608058), confirm_callback=active_high_battlepass)

    def refresh_battlepass_status(self, nd_task_item):
        task_id = nd_task_item.task_id
        task_conf = task_utils.get_task_conf_by_id(task_id)
        need_high_bp = bool(task_conf.get('need_high_battlepass', 0))
        if need_high_bp:
            nd_task_item.nd_elite.setVisible(True)
            active_high_bp = global_data.player.has_activate_battlepass_type()
            if active_high_bp:
                nd_task_item.img_icon.setVisible(True)
                nd_task_item.lab_num.setVisible(True)
                nd_task_item.lab_content.SetString(81081)
                nd_task_item.lab_content.SetPosition('50%26', '50%0')
            else:
                nd_task_item.img_icon.setVisible(False)
                nd_task_item.lab_num.setVisible(False)
                nd_task_item.lab_content.SetString(80937)
                nd_task_item.lab_content.SetPosition('50%0', '50%0')

    def _set_task_reward_status(self, nd_task_item):
        if not nd_task_item:
            return
        nd_task_item.temp_btn_get.setVisible(False)
        nd_task_item.nd_get.setVisible(False)
        nd_task_item.temp_btn_finish.setVisible(False)
        nd_task_item.btn_get_upgrade.setVisible(False)
        nd_task_item.lab_working.setVisible(False)
        status = global_data.player.get_task_reward_status(nd_task_item.task_id)
        if status == ITEM_UNGAIN:
            if task_utils.get_cost_task_card_num(nd_task_item.task_id) == 0:
                nd_task_item.lab_working.setVisible(True)
            else:
                nd_task_item.temp_btn_finish.setVisible(True)
        elif status == ITEM_UNRECEIVED:
            if task_utils.need_active_high_battlepass(nd_task_item.task_id) and not global_data.player.has_activate_battlepass_type():
                nd_task_item.btn_get_upgrade.setVisible(True)
            else:
                nd_task_item.temp_btn_get.setVisible(True)
        else:
            nd_task_item.nd_get.setVisible(True)

    def _refresh_task_card_num(self):
        for nd_task_item in six.itervalues(self.task_dict):
            self._set_cost_card_num(nd_task_item)

    def _refresh_all_week_task_red_point(self):
        cur_week = global_data.player.get_cur_season_week_no()
        for week in range(1, cur_week + 1):
            self._refresh_season_week_task_red_point(week)

    def _refresh_red_point(self, task_id):
        task_week = task_utils.get_season_task_week(task_id)
        if not task_week:
            self._refresh_left_bt_tab_red_point()
        else:
            self._refresh_season_week_task_red_point(task_week)
            self._refresh_left_week_tab_red_point()

    def _refresh_left_week_tab_red_point(self):
        cur_week = global_data.player.get_cur_season_week_no()
        left_tab_need_rp = False
        for week in range(1, cur_week + 1):
            rp = self.check_week_red_point(week)
            if rp:
                left_tab_need_rp = rp

        self.nd_content.list_tab.GetItem(0).temp_tip.setVisible(left_tab_need_rp)

    def _refresh_season_week_task_red_point(self, week):
        redpoint = self.check_week_red_point(week)
        tab_item = self.nd_content.pnl_list_top_tab.GetItem(week - 1)
        if tab_item:
            tab_item.img_red_dot.setVisible(redpoint)
        return redpoint

    def _refresh_left_bt_tab_red_point(self):
        show_bt_time_rp = self._check_all_bt_time_task_red_point()
        self.nd_content.list_tab.GetItem(1).temp_tip.setVisible(show_bt_time_rp)

    @staticmethod
    def check_red_point():
        has_unlock = system_unlock_utils.is_sys_unlocked(system_unlock_utils.SYSTEM_SEASON_TASK)
        if not has_unlock:
            return False
        if SeasonTaskWidget._check_all_week_task_red_point():
            return True
        if SeasonTaskWidget._check_all_bt_time_task_red_point():
            return True
        return False

    @staticmethod
    def _check_all_week_task_red_point--- This code section failed: ---

 790       0  LOAD_GLOBAL           0  'global_data'
           3  LOAD_ATTR             1  'player'
           6  LOAD_ATTR             2  'get_cur_season_week_no'
           9  CALL_FUNCTION_0       0 
          12  STORE_FAST            0  'season_week'

 791      15  SETUP_LOOP           43  'to 61'
          18  LOAD_GLOBAL           3  'range'
          21  LOAD_CONST            1  1
          24  LOAD_CONST            1  1
          27  BINARY_ADD       
          28  CALL_FUNCTION_2       2 
          31  GET_ITER         
          32  FOR_ITER             25  'to 60'
          35  STORE_FAST            1  'week'

 792      38  LOAD_GLOBAL           4  'SeasonTaskWidget'
          41  LOAD_ATTR             5  'check_week_red_point'
          44  LOAD_FAST             1  'week'
          47  CALL_FUNCTION_1       1 
          50  POP_JUMP_IF_FALSE    32  'to 32'

 793      53  LOAD_GLOBAL           6  'True'
          56  RETURN_END_IF    
        57_0  COME_FROM                '50'
          57  JUMP_BACK            32  'to 32'
          60  POP_BLOCK        
        61_0  COME_FROM                '15'

 795      61  LOAD_GLOBAL           7  'False'
          64  RETURN_VALUE     
          -1  RETURN_LAST      

Parse error at or near `CALL_FUNCTION_2' instruction at offset 28

    @staticmethod
    def _check_all_bt_time_task_red_point():
        task_ids = global_data.player.get_season_battle_time_task_ids()
        season_bt_parent_task_id = global_data.player.get_season_bt_parent_task()
        for task_id in task_ids:
            if global_data.player.get_task_reward_status(task_id) == ITEM_UNRECEIVED:
                return True

        if global_data.player.get_task_reward_status(season_bt_parent_task_id) == ITEM_UNRECEIVED:
            return True
        return False

    @staticmethod
    def check_week_red_point(week):
        has_unlock = system_unlock_utils.is_sys_unlocked(system_unlock_utils.SYSTEM_SEASON_TASK)
        if not has_unlock:
            return False
        for task_id in SeasonTaskWidget.get_task_ids(SeasonTaskWidget.TAB_WEEK_TASK, week):
            if global_data.player.get_task_reward_status(task_id) == ITEM_UNRECEIVED:
                if task_utils.need_active_high_battlepass(task_id):
                    if global_data.player.has_activate_battlepass_type():
                        return True
                else:
                    return True

        return False

    def _refresh_receive_all_btn(self, *args):
        if self.check_red_point():
            self.nd_content.temp_get_all.setVisible(True)
            self.nd_content.pnl_get_all.setVisible(True)
        else:
            self.nd_content.temp_get_all.setVisible(False)
            self.nd_content.pnl_get_all.setVisible(False)

    def destroy(self):
        self.sview_index_dict = None
        self.sview_content_height_dict = None
        self.ui_view_list = None
        self.sview_index_dict = {}
        self.sview_content_height_dict = {}
        self.bt_sview_index = 0
        self.bt_sview_content_height = 0
        self.is_bt_check_sview = False
        self.task_ids_dict = {}
        self.bt_task_ids = []
        self.cur_week_no = 0
        self.ui_view_list = None
        global_data.emgr.start_new_season_week_event -= self._start_new_season_week_task
        global_data.emgr.receive_task_reward_succ_event -= self._refresh_red_point
        global_data.emgr.receive_task_reward_succ_event -= self._refresh_receive_all_btn
        global_data.emgr.season_pass_update_lv -= self._refresh_battlepass_lv
        global_data.emgr.season_pass_open_type -= self._open_battlepass_type
        global_data.emgr.on_lobby_bag_item_changed_event -= self._refresh_task_card_num
        super(SeasonTaskWidget, self).destroy()
        return