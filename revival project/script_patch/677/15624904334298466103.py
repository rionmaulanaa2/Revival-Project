# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivityS8S13SeasonLogin.py
from __future__ import absolute_import
from six.moves import range
from common.cfg import confmgr
from logic.gutils import task_utils
from logic.gutils.item_utils import get_lobby_item_name
from logic.gutils import activity_utils
from logic.comsys.activity.ActivityCollect import ActivityCollect
from logic.gcommon.time_utility import get_day_hour_minute_second, get_readable_time, get_readable_time_day_hour_minitue, ONE_HOUR_SECONS
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gutils.item_utils import get_lobby_item_name, get_lobby_item_pic_by_item_no
from logic.gutils import template_utils
from logic.gcommon import time_utility as tutil
import cc

class ActivityS8S13SeasonLogin(ActivityCollect):
    NORMAL_TEMPLATE = 'activity/activity_202206/bp_login/i_bp_login_item'
    TODAY_TEMPLATE = 'activity/activity_202206/bp_login/i_bp_login_item2'

    def init_parameters(self):
        super(ActivityS8S13SeasonLogin, self).init_parameters()
        self._task_id = confmgr.get('c_activity_config', self._activity_type, 'cTask', default='')
        self._today_idx = -1
        self.panel.RecordAnimationNodeState('btn_loop')
        self.common_reward_data = confmgr.get('common_reward_data')

    def on_init_panel(self):
        activity_type = self._activity_type
        conf = confmgr.get('c_activity_config', activity_type)
        act_name_id = conf['cNameTextID']
        self.panel.lab_tdescribe and self.panel.lab_tdescribe.SetString(get_text_by_id(conf.get('cDescTextID', '')))
        btn_describe = self.panel.btn_question
        if btn_describe:

            @btn_describe.unique_callback()
            def OnClick(btn, touch):
                dlg = global_data.ui_mgr.show_ui('GameRuleDescUI', 'logic.comsys.common_ui')
                dlg.set_show_rule(get_text_by_id(act_name_id), get_text_by_id(conf.get('cRuleTextID', '')))
                x, y = btn_describe.GetPosition()
                wpos = btn_describe.GetParent().ConvertToWorldSpace(x, y)
                dlg.panel.nd_game_describe.setAnchorPoint(cc.Vec2(1.0, 1.0))
                template_utils.set_node_position_in_screen(dlg.panel.nd_game_describe, dlg.panel, wpos)

        if not conf['cTask']:
            return
        task_list = activity_utils.parse_task_list(conf['cTask'])
        if len(task_list) <= 0:
            return
        self.show_list()
        if self.panel.HasAnimation('show'):
            self.panel.PlayAnimation('show')

    def show_list(self):
        player = global_data.player
        activity_type = self._activity_type
        conf = confmgr.get('c_activity_config', activity_type)
        if not conf['cTask']:
            return
        task_list = activity_utils.parse_task_list(conf['cTask'])
        if len(task_list) <= 0:
            return
        time_delta = 86400
        parent_task = task_list[0]
        children_tasks = task_utils.get_children_task(parent_task)
        self._children_tasks = children_tasks
        sub_act_list = self.panel.list_item
        sub_act_list.SetContentSize(938, 154)
        sub_act_list.SetInitCount(0)
        for i in range(len(children_tasks)):
            if task_utils.is_task_open(str(children_tasks[i])):
                self._today_idx = i

        for i in range(len(children_tasks)):
            if i == self._today_idx:
                sub_act_list.AddItem(global_data.uisystem.load_template(self.TODAY_TEMPLATE))
            else:
                sub_act_list.AddItem(global_data.uisystem.load_template(self.NORMAL_TEMPLATE))

        for idx, task_id in enumerate(children_tasks):
            item_widget = sub_act_list.GetItem(idx)
            is_open = task_utils.is_task_open(str(task_id))
            is_received = player.has_receive_reward(str(task_id))
            can_receive = player.is_task_reward_receivable(str(task_id)) and not is_received
            reward_id = task_utils.get_task_reward(str(task_id))
            r_list = self.common_reward_data.get(str(reward_id), {}).get('reward_list', [])
            if not r_list:
                continue
            item_no, item_num = r_list[0]
            item_name = get_lobby_item_name(item_no)
            item_path = get_lobby_item_pic_by_item_no(item_no)
            item_widget.img_item.SetDisplayFrameByPath('', item_path)
            conf = task_utils.get_task_conf_by_id(task_id)
            start_time = conf.get('start_time', 0)
            if start_time:
                tmp_time = tutil.get_date_str('%Y.%m.%d', start_time)
                item_widget.lab_time.SetString(tmp_time)

            @item_widget.btn_choose.unique_callback()
            def OnClick(btn, touch, tmp_task_id=task_id):
                player.receive_all_task_reward(tmp_task_id)

        self._init_get_all()
        self.refresh_list()

    def refresh_list(self):
        player = global_data.player
        parent_task = self._task_id
        children_tasks = task_utils.get_children_task(parent_task)
        self._children_tasks = children_tasks
        sub_act_list = self.panel.list_item
        for idx, task_id in enumerate(children_tasks):
            item_widget = sub_act_list.GetItem(idx)
            if idx == self._today_idx:
                item_widget.setLocalZOrder(1)
            else:
                item_widget.setLocalZOrder(0)
            is_open = task_utils.is_task_open(str(task_id))
            is_received = player.has_receive_reward(str(task_id))
            can_receive = player.is_task_reward_receivable(str(task_id)) and not is_received
            if is_received:
                item_widget.nd_got.setVisible(True)
                item_widget.nd_miss.setVisible(False)
                item_widget.frame_get.setVisible(False)
                item_widget.StopAnimation('get_tips')
            elif not is_received and can_receive:
                item_widget.nd_got.setVisible(False)
                item_widget.nd_miss.setVisible(False)
                item_widget.frame_get.setVisible(True)
                item_widget.PlayAnimation('get_tips')
            elif is_open and not can_receive:
                item_widget.nd_got.setVisible(False)
                item_widget.nd_miss.setVisible(True)
                item_widget.frame_get.setVisible(False)
                item_widget.StopAnimation('get_tips')
            else:
                item_widget.nd_got.setVisible(False)
                item_widget.nd_miss.setVisible(False)
                item_widget.frame_get.setVisible(False)
                item_widget.StopAnimation('get_tips')

    def refresh_time(self, parent_task):
        pass

    def _init_get_all(self):
        player = global_data.player
        if not player:
            return
        count = 0
        for child_task in self._children_tasks:
            if task_utils.is_task_open(child_task) and player.has_unreceived_task_reward(child_task):
                count += 1

        if count >= 2:
            self.panel.btn_get.setVisible(True)

            @self.panel.btn_get.unique_callback()
            def OnClick(btn, touch):
                player.receive_all_task_reward(self._task_id)

        else:
            self.panel.btn_get.setVisible(False)