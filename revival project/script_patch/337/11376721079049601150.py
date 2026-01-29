# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivityS6MonthLogin.py
from __future__ import absolute_import
from six.moves import range
from logic.gcommon import time_utility as tutil
from common.cfg import confmgr
from logic.gutils import task_utils
from logic.gutils.item_utils import get_lobby_item_name, get_lobby_item_pic_by_item_no
from logic.gutils import activity_utils
from logic.gutils import template_utils
from logic.comsys.activity.ActivityCollect import ActivityCollect
from logic.gcommon.time_utility import get_day_hour_minute_second, get_readable_time, get_readable_time_day_hour_minitue, ONE_HOUR_SECONS
from logic.gcommon.common_utils.local_text import get_text_by_id
import cc
import time
PIC0 = 'gui/ui_res_2/activity/activity_202201/waste_soil_sign_in/pnl_waste_soil_choose.png'
PIC1 = 'gui/ui_res_2/activity/activity_202201/waste_soil_sign_in/pnl_waste_soil_dark.png'
GET_PIC0 = 'gui/ui_res_2/activity/activity_202201/waste_soil_sign_in/btn_waste_soil.png'
GET_PIC1 = 'gui/ui_res_2/battle_pass/normal/btn_bp_normal_2_1.png'
WEEK_TEXT = (610345, 610346, 610347)

class ActivityS6MonthLogin(ActivityCollect):

    def init_parameters(self):
        super(ActivityS6MonthLogin, self).init_parameters()
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
                conf = task_utils.get_task_conf_by_id(task_id)
                start_time = conf.get('start_time', 0)
                tt = time.localtime(start_time)
                day_text = '{}.{}'.format(tt[1], tt[2])
                item_widget.lab_time.SetString(day_text)

        self.refresh_list()
        self._init_get_all()

    def refresh_list(self):
        player = global_data.player
        now = tutil.get_server_time()
        for i in range(3):
            sub_task = self._children_tasks[i * 3:(i + 1) * 3]
            task_start, task_end = sub_task[0], sub_task[-1]
            week_start, week_end = task_utils.get_task_conf_by_id(task_start).get('start_time', 0), task_utils.get_task_conf_by_id(task_end).get('end_time', 0)
            week_node = getattr(self.panel, 'bar_blue_%s' % (i + 1))
            if week_start <= now <= week_end:
                week_node.SetDisplayFrameByPath('', 'gui/ui_res_2/activity/activity_202201/waste_soil_sign_in/pnl_top_waste_soil_2.png')
            else:
                week_node.SetDisplayFrameByPath('', 'gui/ui_res_2/activity/activity_202201/waste_soil_sign_in/pnl_top_waste_soil_1.png')
            sub_act_list = getattr(self.panel, 'list_time_%s' % (i + 1))
            for idx, task_id in enumerate(sub_task):
                item_widget = sub_act_list.GetItem(idx)
                reward_id = task_utils.get_task_reward(task_id)
                btn = item_widget.btn_choose
                has_rewarded = player.has_receive_reward(task_id)
                can_receive = player.is_task_reward_receivable(task_id)
                conf = task_utils.get_task_conf_by_id(task_id)
                end_time = conf.get('end_time', now + 1)
                if has_rewarded:
                    item_widget.btn_bar.SetFrames('', ['', PIC0, ''], False, None)
                    item_widget.nd_get.setVisible(True)
                    item_widget.StopAnimation('selected_loop')
                elif can_receive:
                    item_widget.btn_bar.SetFrames('', ['', PIC0, PIC0], False, None)
                    item_widget.nd_get.setVisible(False)
                    item_widget.PlayAnimation('selected_loop')
                elif now > end_time:
                    item_widget.btn_bar.SetFrames('', ['', PIC0, ''], False, None)
                    item_widget.nd_get.setVisible(True)
                    item_widget.lab_overdue.setVisible(True)
                    item_widget.icon_tick.setVisible(False)
                    item_widget.StopAnimation('selected_loop')
                else:
                    item_widget.btn_bar.SetFrames('', ['', PIC0, ''], False, None)
                    item_widget.nd_get.setVisible(False)
                    item_widget.lab_overdue.setVisible(False)
                    item_widget.icon_tick.setVisible(True)
                    item_widget.StopAnimation('selected_loop')
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
        else:
            can_receive = False
            for idx, task_id in enumerate(self._children_tasks):
                sub_can_receive = player.is_task_reward_receivable(task_id)
                if sub_can_receive:
                    can_receive = True

            if can_receive:
                self.panel.btn_get.setVisible(True)
                self.panel.lab_get.SetString(get_text_by_id(80834))
                self.panel.btn_get.SetFrames('', [GET_PIC0, GET_PIC0, GET_PIC0], False, None)

                @self.panel.btn_get.unique_callback()
                def OnClick(btn, touch):
                    player.receive_all_task_reward(self._task_id)
                    self.panel.lab_get.SetString(get_text_by_id(604029))
                    self.panel.btn_get.SetFrames('', [GET_PIC1, GET_PIC1, GET_PIC1], False, None)
                    return

            else:
                self.panel.btn_get.setVisible(False)
            return