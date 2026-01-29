# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivityChristmas/ActivityChristmas7DLogin.py
from __future__ import absolute_import
from common.cfg import confmgr
from logic.gutils import task_utils
from logic.gutils.item_utils import get_lobby_item_name, get_lobby_item_pic_by_item_no
from logic.gutils import activity_utils
from logic.gutils import template_utils
from logic.comsys.activity.ActivityCollect import ActivityCollect
from logic.gcommon.time_utility import get_day_hour_minute_second, get_readable_time, get_readable_time_day_hour_minitue, ONE_HOUR_SECONS, get_date_str
from logic.gcommon.common_utils.local_text import get_text_by_id
import cc

class ActivityChristmas7DLogin(ActivityCollect):

    def init_parameters(self):
        super(ActivityChristmas7DLogin, self).init_parameters()
        self._task_id = confmgr.get('c_activity_config', self._activity_type, 'cTask', default='')
        self.panel.RecordAnimationNodeState('loop')

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'receive_task_reward_succ_event': self._on_update_reward,
           'receive_task_prog_reward_succ_event': self._on_update_reward
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def _on_update_reward(self, *args):
        global_data.player.read_activity_list(self._activity_type)
        self.show_list()

    def on_init_panel(self):
        activity_type = self._activity_type
        conf = confmgr.get('c_activity_config', activity_type)
        self.panel.lab_time_1.SetString('%s-%s' % (
         get_date_str('%Y.%m.%d', conf['cBeginTime']),
         get_date_str('%Y.%m.%d', conf['cEndTime'])))
        btn_question = self.panel.btn_christmas_question
        if btn_question:

            @btn_question.unique_callback()
            def OnClick(btn, touch):
                dlg = global_data.ui_mgr.show_ui('GameRuleDescUI', 'logic.comsys.common_ui')
                dlg.set_show_rule(get_text_by_id(607171), get_text_by_id(conf.get('cDescTextID', '')))
                x, y = btn_question.GetPosition()
                wpos = btn_question.GetParent().ConvertToWorldSpace(x, y)
                dlg.panel.nd_game_describe.setAnchorPoint(cc.Vec2(1.0, 1.0))
                template_utils.set_node_position_in_screen(dlg.panel.nd_game_describe, dlg.panel, wpos)

        self.show_list()
        if self.panel.HasAnimation('show'):
            self.panel.PlayAnimation('show')

    def reorder_task_list(self, tasks):
        ret_list = sorted(tasks)
        return ret_list

    def show_list(self):
        activity_type = self._activity_type
        conf = confmgr.get('c_activity_config', activity_type)
        if not conf['cTask']:
            return
        task_list = activity_utils.parse_task_list(conf['cTask'])
        if len(task_list) <= 0:
            return
        self._timer_cb[0] = lambda : self.refresh_time(self._task_id)
        self.refresh_time(self._task_id)
        parent_task = task_list[0]
        children_tasks = task_utils.get_children_task(parent_task)
        children_tasks = self.reorder_task_list(children_tasks)
        self._children_tasks = children_tasks
        sub_act_list = self.panel.list_all
        sub_act_list.SetInitCount(0)
        sub_act_list.SetInitCount(len(children_tasks))
        ui_data = conf.get('cUiData', {})
        for idx, task_id in enumerate(children_tasks):
            item_widget = sub_act_list.GetItem(idx)
            reward_id = task_utils.get_task_reward(task_id)
            r_list = confmgr.get('common_reward_data', str(reward_id), 'reward_list', default=[])
            item_no, item_num = r_list[0]
            item_path = get_lobby_item_pic_by_item_no(item_no)
            item_widget.temp_items.item.SetDisplayFrameByPath('', item_path)
            item_widget.temp_items.lab_quantity.setVisible(True)
            item_widget.temp_items.lab_quantity.SetString(str(item_num))

        self.refresh_list()

    def refresh_list(self):
        player = global_data.player
        has_unreceived = False
        all_received = True
        sub_act_list = self.panel.list_all
        for idx, task_id in enumerate(self._children_tasks):
            day = idx + 1
            item_widget = sub_act_list.GetItem(idx)
            reward_id = task_utils.get_task_reward(task_id)
            r_list = confmgr.get('common_reward_data', str(reward_id), 'reward_list', default=[])
            item_no, item_num = r_list[0]
            item_name = get_lobby_item_name(item_no)
            item_widget.lab_sign.SetString(item_name)
            item_widget.lab_days.SetString(get_text_by_id(604004).format(day))
            item_widget.img_received.setVisible(False)
            btn_bar = item_widget.btn_bar
            cur_times = player.get_task_prog(task_id)
            total_times = task_utils.get_total_prog(task_id)
            can_receive = not player.has_receive_reward(task_id) and cur_times >= total_times
            is_received = player.has_receive_reward(task_id)
            btn_bar.SetEnable(False)
            btn_bar.SetSelect(can_receive)
            item_widget.lab_sign.SetColor(15548754 if can_receive else 16777215)
            if is_received:
                item_widget.img_received.setVisible(True)
            else:
                all_received = False
                if can_receive:
                    has_unreceived = True

            @item_widget.temp_items.btn_choose.unique_callback()
            def OnClick(btn, touch, reward_id=reward_id):
                x, y = btn.GetPosition()
                w, h = btn.GetContentSize()
                x += w * 0.5
                wpos = btn.ConvertToWorldSpace(x, y)
                extra_info = {'show_jump': False}
                r_list = confmgr.get('common_reward_data', str(reward_id), 'reward_list', default=[])
                item_no, item_num = r_list[0]
                global_data.emgr.show_item_desc_ui_event.emit(item_no, None, wpos, extra_info=extra_info, item_num=item_num)
                return

        self.panel.btn_christmas_receive.SetEnable(False)
        self.panel.StopAnimation('loop')
        self.panel.RecoverAnimationNodeState('loop')
        if has_unreceived:
            self.panel.lab_get.SetString(get_text_by_id(604030))
            self.panel.btn_christmas_receive.SetEnable(True)

            @self.panel.btn_christmas_receive.unique_callback()
            def OnClick(btn, touch):
                player.receive_all_task_reward(self._task_id)

            self.panel.PlayAnimation('loop')
        elif all_received:
            self.panel.lab_get.SetString(get_text_by_id(80866))
        else:
            self.panel.lab_get.SetString(get_text_by_id(606046))

    def refresh_time(self, parent_task):
        left_time = task_utils.get_raw_left_open_time(parent_task)
        if left_time > 0:
            day, _, _, _ = get_day_hour_minute_second(left_time)
            day = day + 1
            day_text = '<fontname=gui/fonts/fzy4jw.ttf><size=18><color=0XF9DD49FF>{}</color></size></fontname>'.format(day)
            self.panel.lab_end_time.SetString(get_text_by_id(607969).format('16', '0XFFFFFFFF', day_text))
        else:
            close_left_time = 0
            self.panel.lab_end_time.SetString(get_readable_time(close_left_time))