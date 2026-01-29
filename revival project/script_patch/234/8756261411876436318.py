# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivityS7MonthLogin.py
from __future__ import absolute_import
from six.moves import range
from logic.gcommon import time_utility as tutil
from common.cfg import confmgr
from logic.gutils import task_utils
from logic.gutils.item_utils import get_lobby_item_name, get_lobby_item_pic_by_item_no
from logic.gutils import activity_utils
from logic.gutils import template_utils
from logic.comsys.activity.ActivityCollect import ActivityCollect
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gcommon.common_const.activity_const import ACTIVITY_WEEKEND_LOGIN_PERIOD_DAYS, ACTIVITY_WEEKEND_LOGIN_BASETIME
import cc
import time
WEEK_TEXT = (610345, 610346, 610347)

def get_task_time(task_id, start):
    conf = task_utils.get_task_conf_by_id(task_id)
    arg = conf.get('arg', {})
    period_days = global_data.player.get_weekend_login_period() * ACTIVITY_WEEKEND_LOGIN_PERIOD_DAYS
    bias = 1 if start else 0
    start_time = ACTIVITY_WEEKEND_LOGIN_BASETIME + (period_days + arg.get('weekend_day_no', 0) - bias) * tutil.ONE_DAY_SECONDS
    return start_time


class ActivityS7MonthLogin(ActivityCollect):

    def init_parameters(self):
        super(ActivityS7MonthLogin, self).init_parameters()
        self._task_id = confmgr.get('c_activity_config', self._activity_type, 'cTask', default='')

    def on_init_panel(self):
        activity_type = self._activity_type
        conf = confmgr.get('c_activity_config', activity_type)
        btn_help = self.panel.btn_help
        if btn_help:

            @btn_help.unique_callback()
            def OnClick(btn, touch):
                dlg = global_data.ui_mgr.show_ui('GameRuleDescUI', 'logic.comsys.common_ui')
                dlg.set_show_rule(get_text_by_id(607171), get_text_by_id(conf.get('cDescTextID', '')))
                x, y = btn_help.GetPosition()
                wpos = btn_help.GetParent().ConvertToWorldSpace(x, y)
                dlg.panel.nd_game_describe.setAnchorPoint(cc.Vec2(1.0, 1.0))
                template_utils.set_node_position_in_screen(dlg.panel.nd_game_describe, dlg.panel, wpos)

        self.show_list()
        if self.panel.HasAnimation('show'):
            self.panel.PlayAnimation('show')
        if self.panel.HasAnimation('loop'):
            self.panel.PlayAnimation('loop')

    def show_list(self):
        activity_type = self._activity_type
        conf = confmgr.get('c_activity_config', activity_type)
        if not conf['cTask']:
            return
        task_list = activity_utils.parse_task_list(conf['cTask'])
        if len(task_list) <= 0:
            return
        parent_task = task_list[0]
        children_tasks = task_utils.get_children_task(parent_task)
        self._children_tasks = children_tasks
        activity_duration_text = get_text_by_id(609202)
        for i in range(3):
            sub_task = self._children_tasks[i * 3:(i + 1) * 3]
            sub_act_list = getattr(self.panel, 'list_time_%s' % (i + 1))
            sub_act_list.SetInitCount(0)
            sub_act_list.SetInitCount(len(sub_task))
            for idx, task_id in enumerate(sub_task):
                item_widget = sub_act_list.GetItem(idx)
                reward_id = task_utils.get_task_reward(task_id)
                r_list = confmgr.get('common_reward_data', str(reward_id), 'reward_list', default=[])
                item_no, item_num = r_list[0]
                item_path = get_lobby_item_pic_by_item_no(item_no)
                item_name = get_lobby_item_name(item_no)
                item_widget.item.SetDisplayFrameByPath('', item_path)
                item_widget.lab_quantity.setVisible(True)
                item_widget.lab_quantity.SetString(str(item_num))
                item_widget.lab_name_1.SetString(item_name)
                item_widget.lab_days.SetString(get_text_by_id(WEEK_TEXT[idx]))
                start_time = get_task_time(task_id, True)
                tt = tutil.get_utc8_datetime(start_time)
                day_text = '{}.{}'.format(tt.month, tt.day)
                item_widget.lab_time.SetString(day_text)
                if i == 0 and idx == 0:
                    activity_duration_text += day_text + ' - '
                elif i == 2 and idx == 2:
                    activity_duration_text += day_text

        self.panel.lab_title.SetString(activity_duration_text)
        self.refresh_list()
        self._init_get_all()

    def refresh_list(self):
        player = global_data.player
        now = tutil.get_server_time()
        for i in range(3):
            sub_task = self._children_tasks[i * 3:(i + 1) * 3]
            task_start, task_end = sub_task[0], sub_task[-1]
            week_start, week_end = get_task_time(task_start, True), get_task_time(task_end, False)
            week_node = getattr(self.panel, 'bar_weekend_%s_1' % (i + 1))
            if week_start <= now <= week_end:
                week_node.SetDisplayFrameByPath('', 'gui/ui_res_2/activity/activity_202204/weekends_sign_in/bar_weekends_sign_in_week2.png')
                week_node.lab_week.SetColor(6566707)
            else:
                week_node.SetDisplayFrameByPath('', 'gui/ui_res_2/activity/activity_202204/weekends_sign_in/bar_weekends_sign_in_week1.png')
                week_node.lab_week.SetColor(15791358)
            sub_act_list = getattr(self.panel, 'list_time_%s' % (i + 1))
            for idx, task_id in enumerate(sub_task):
                item_widget = sub_act_list.GetItem(idx)
                reward_id = task_utils.get_task_reward(task_id)
                btn = item_widget.btn_choose
                has_rewarded = player.has_receive_reward(task_id)
                can_receive = player.is_task_reward_receivable(task_id)
                end_time = get_task_time(task_id, False)
                if has_rewarded:
                    item_widget.nd_get.setVisible(True)
                    item_widget.StopAnimation('selected_loop')
                elif can_receive:
                    item_widget.nd_get.setVisible(False)
                    item_widget.img_get.setVisible(True)
                    item_widget.PlayAnimation('selected_loop')
                elif now > end_time:
                    item_widget.nd_get.setVisible(True)
                    item_widget.lab_overdue.setVisible(True)
                    item_widget.icon_tick.setVisible(False)
                    item_widget.StopAnimation('selected_loop')
                else:
                    item_widget.nd_get.setVisible(False)
                    item_widget.lab_overdue.setVisible(False)
                    item_widget.icon_tick.setVisible(True)
                    item_widget.StopAnimation('selected_loop')
                item_widget.btn_bar.SetFrames('', ['', '', ''], False, None)
                item_widget.btn_bar.SetEnable(False)

                @btn.unique_callback()
                def OnClick(btn, touch, reward_id=reward_id, can_receive=can_receive, task_id=task_id):
                    if can_receive:
                        global_data.player.receive_task_reward(task_id)
                    else:
                        x, y = btn.GetPosition()
                        w, h = btn.GetContentSize()
                        x += w * 0.5
                        wpos = btn.ConvertToWorldSpace(x, y)
                        extra_info = {'show_jump': False}
                        r_list = confmgr.get('common_reward_data', str(reward_id), 'reward_list', default=[])
                        item_no, item_num = r_list[0]
                        global_data.emgr.show_item_desc_ui_event.emit(item_no, None, wpos, extra_info=extra_info, item_num=item_num)
                    return

        return

    def _init_get_all(self):
        player = global_data.player
        if not player:
            return
        can_receive = False
        for idx, task_id in enumerate(self._children_tasks):
            sub_can_receive = player.is_task_reward_receivable(task_id)
            if sub_can_receive:
                can_receive = True

        if can_receive:
            self.panel.btn_get.setVisible(True)
            self.panel.lab_get.SetString(get_text_by_id(80834))

            @self.panel.btn_get.unique_callback()
            def OnClick(btn, touch):
                player.receive_all_task_reward(self._task_id)
                self.panel.lab_get.SetString(get_text_by_id(604029))
                self.panel.btn_get.SetEnable(False)

        else:
            self.panel.btn_get.setVisible(False)