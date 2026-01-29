# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivityDecemberEightDayLogin.py
from __future__ import absolute_import
from common.cfg import confmgr
from logic.gutils import task_utils
from logic.gutils.item_utils import get_lobby_item_name, get_lobby_item_pic_by_item_no
from logic.gutils import activity_utils
from logic.gutils import template_utils
from logic.comsys.activity.ActivityCollect import ActivityCollect
from logic.gcommon.time_utility import get_day_hour_minute_second, get_readable_time, get_readable_time_day_hour_minitue, ONE_HOUR_SECONS, get_simply_time
from logic.gcommon.common_utils.local_text import get_text_by_id
import cc
PIC0 = 'gui/ui_res_2/activity/activity_202201/seven_login/bar_seven_login_1.png'
PIC1 = 'gui/ui_res_2/activity/activity_202201/seven_login/bar_seven_login_2.png'
PIC2 = 'gui/ui_res_2/activity/activity_202201/seven_login/bar_seven_login_3.png'

class ActivityDecemberEightDayLogin(ActivityCollect):

    def init_parameters(self):
        super(ActivityDecemberEightDayLogin, self).init_parameters()
        self.conf = confmgr.get('c_activity_config', self._activity_type, default={})
        self.common_reward_data = confmgr.get('common_reward_data', default={})
        self._task_id = str(self.conf.get('cTask', ''))
        children_tasks = task_utils.get_children_task(self._task_id)
        self._children_tasks = self.reorder_prog_list(children_tasks)
        self.panel.RecordAnimationNodeState('btn_loop')

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
        btn_question = self.panel.btn_question
        if btn_question:

            @btn_question.unique_callback()
            def OnClick(btn, touch):
                dlg = global_data.ui_mgr.show_ui('GameRuleDescUI', 'logic.comsys.common_ui')
                dlg.set_show_rule(get_text_by_id(607171), get_text_by_id(self.conf.get('cDescTextID', '')))
                x, y = btn_question.GetPosition()
                wpos = btn_question.GetParent().ConvertToWorldSpace(x, y)
                dlg.panel.nd_game_describe.setAnchorPoint(cc.Vec2(0.0, 1.0))
                template_utils.set_node_position_in_screen(dlg.panel.nd_game_describe, dlg.panel, wpos)

        self.show_list()
        if self.panel.HasAnimation('show'):
            self.panel.PlayAnimation('show')

    def reorder_prog_list(self, progs):
        ret_list = sorted(progs)
        return ret_list

    def show_list(self):
        if not self.conf['cTask']:
            return
        task_list = activity_utils.parse_task_list(self.conf['cTask'])
        if len(task_list) <= 0:
            return
        self._timer_cb[0] = lambda : self.refresh_time(self._task_id)
        self.refresh_time(self._task_id)
        sub_act_list = self.panel.list_items
        sub_act_list.SetInitCount(0)
        sub_act_list.SetInitCount(len(self._children_tasks))
        for idx, task in enumerate(self._children_tasks):
            item_widget = sub_act_list.GetItem(idx)
            reward_id = task_utils.get_task_reward(str(task))
            r_list = self.common_reward_data.get(str(reward_id), {}).get('reward_list', [])
            item_no, item_num = r_list[0]
            item_name = get_lobby_item_name(item_no)
            item_widget.lab_sign.SetString(item_name)
            item_path = get_lobby_item_pic_by_item_no(item_no)
            item_widget.temp_items.item.SetDisplayFrameByPath('', item_path)
            item_widget.temp_items.lab_quantity.setVisible(True)
            item_widget.temp_items.lab_quantity.SetString(str(item_num))

        self.refresh_list()
        self._init_get_all()

    def refresh_list(self):
        player = global_data.player
        sub_act_list = self.panel.list_items
        task_len = len(self._children_tasks)
        for idx, task_id in enumerate(self._children_tasks):
            day = idx + 1
            item_widget = sub_act_list.GetItem(idx)
            reward_id = task_utils.get_task_reward(str(task_id))
            btn = item_widget.temp_items.btn_choose
            btn_bar = item_widget.btn_bar
            is_received = player.has_receive_reward(str(task_id))
            can_receive = player.is_task_reward_receivable(str(task_id)) and not is_received
            item_widget.lab_num.SetString('DAY{}'.format(day))
            if is_received:
                item_widget.img_blue_check.setVisible(True)
                if idx == task_len - 1:
                    btn_bar.SetFrames('', [PIC2, PIC2, PIC2])
                    self.set_item_widget_color(item_widget, 9613046, 15856639, 5462937, 5397425)
                    item_widget.lab_days.SetString('<color=0xF1F3FFFF>' + get_text_by_id(610373).format(day) + '</color>')
                else:
                    self.set_item_widget_color(item_widget, 9613046, 5462937, 5462937, 6333925)
                    item_widget.lab_days.SetString('<color=0x535B99FF>' + get_text_by_id(610373).format(day) + '</color>')
            elif can_receive:
                btn_bar.SetFrames('', [PIC1, PIC1, PIC1])
                item_widget.img_blue_check.setVisible(False)
                self.set_item_widget_color(item_widget, 14461308, 7298117, 9729358, 11437902)
                item_widget.lab_days.SetString('<color=0x6F5C45FF>' + get_text_by_id(610373).format(day) + '</color>')
            else:
                item_widget.img_blue_check.setVisible(False)
                if idx == task_len - 1:
                    btn_bar.SetFrames('', [PIC2, PIC2, PIC2])
                    self.set_item_widget_color(item_widget, 9613046, 15856639, 5462937, 5397425)
                    item_widget.lab_days.SetString('<color=0xF1F3FFFF>' + get_text_by_id(610373).format(day) + '</color>')
                else:
                    self.set_item_widget_color(item_widget, 9613046, 5462937, 5462937, 6333925)
                    item_widget.lab_days.SetString('<color=0x535B99FF>' + get_text_by_id(610373).format(day) + '</color>')
            btn_bar.SetEnable(False)

            @btn.unique_callback()
            def OnClick(btn, touch, reward_id=reward_id):
                x, y = btn.GetPosition()
                w, h = btn.GetContentSize()
                x += w * 0.5
                wpos = btn.ConvertToWorldSpace(x, y)
                extra_info = {'show_jump': False}
                r_list = self.common_reward_data.get(str(reward_id), {}).get('reward_list', [])
                item_no, item_num = r_list[0]
                global_data.emgr.show_item_desc_ui_event.emit(item_no, None, wpos, extra_info=extra_info, item_num=item_num)
                return

    def set_item_widget_color(self, item_widget, lab_quantity_color, lab_days_color, lab_sign_color, lab_num_color):
        item_widget.temp_items.lab_quantity.SetColor(lab_quantity_color)
        item_widget.lab_sign.SetColor(lab_sign_color)
        item_widget.lab_num.SetColor(lab_num_color)

    def refresh_time(self, parent_task):
        left_time = task_utils.get_raw_left_open_time(parent_task)
        if left_time > 0:
            day, hour, minute, second = get_day_hour_minute_second(left_time)
            if day > 0:
                day += 1
                self.panel.lab_rest_time.SetString(get_text_by_id(610354).format('18', '0xFBFBFFFF', '20', '0xFFFB8AFF', str(day)))
            else:
                hour += 1
                self.panel.lab_rest_time.SetString(get_text_by_id(610355).format('18', '0xFBFBFFFF', '20', '0xFFFB8AFF', str(hour)))
        else:
            close_left_time = 0
            self.panel.lab_rest_time.SetString(get_readable_time(close_left_time))

    def _init_get_all(self):
        player = global_data.player
        if not player:
            return
        has_unreceived = False
        all_received = True
        for task_id in self._children_tasks:
            is_received = player.has_receive_reward(task_id)
            can_receive = player.is_task_reward_receivable(task_id) and not is_received
            if can_receive:
                has_unreceived = True
            if not is_received:
                all_received = False

        if has_unreceived:
            self.panel.btn_get.SetText(get_text_by_id(604030))
            self.panel.btn_get.SetEnable(True)

            @self.panel.btn_get.unique_callback()
            def OnClick(btn, touch):
                player.receive_all_task_reward(self._task_id)

            if self.panel.HasAnimation('btn_loop'):
                self.panel.PlayAnimation('btn_loop')
        elif all_received:
            self.panel.btn_get.SetText(get_text_by_id(80866))
            self.panel.btn_get.SetEnable(False)
            self.panel.StopAnimation('btn_loop')
            self.panel.RecoverAnimationNodeState('btn_loop')
        else:
            self.panel.btn_get.SetText(get_text_by_id(606046))
            self.panel.btn_get.SetEnable(False)
            self.panel.StopAnimation('btn_loop')
            self.panel.RecoverAnimationNodeState('btn_loop')