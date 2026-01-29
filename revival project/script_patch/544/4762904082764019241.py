# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/Activity202203/ActivityOutingSevenDaysLogin.py
from __future__ import absolute_import
from common.cfg import confmgr
from logic.gutils import task_utils
from logic.gutils.item_utils import get_lobby_item_name
from logic.gutils import activity_utils
from logic.comsys.activity.ActivityCollect import ActivityCollect
from logic.gcommon.time_utility import get_day_hour_minute_second, get_readable_time, get_readable_time_day_hour_minitue, ONE_HOUR_SECONS
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gutils.item_utils import get_lobby_item_name, get_lobby_item_pic_by_item_no
import cc
from logic.gutils import template_utils

class ActivityOutingSevenDaysLogin(ActivityCollect):

    def init_parameters(self):
        super(ActivityOutingSevenDaysLogin, self).init_parameters()
        self._task_id = confmgr.get('c_activity_config', self._activity_type, 'cTask', default='')

    def on_init_panel(self):
        activity_type = self._activity_type
        conf = confmgr.get('c_activity_config', activity_type)
        act_name_id = conf['cNameTextID']
        self.panel.lab_tdescribe and self.panel.lab_tdescribe.SetString(get_text_by_id(conf.get('cDescTextID', '')))
        btn_describe = self.panel.btn_christmas_question
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
        self._timer_cb[0] = lambda : self.refresh_time(parent_task)
        self.refresh_time(parent_task)
        sub_act_list = self.panel.list_all
        sub_act_list.SetInitCount(0)
        sub_act_list.SetInitCount(len(children_tasks))
        ui_data = conf.get('cUiData', {})
        for idx, task_id in enumerate(children_tasks):
            item_widget = sub_act_list.GetItem(idx)
            reward_id = task_utils.get_task_reward(task_id)
            r_list = confmgr.get('common_reward_data', str(reward_id), 'reward_list', default=[])
            item_no, item_num = r_list[0]
            item_name = get_lobby_item_name(item_no)
            item_widget.lab_sign.SetString(item_name)
            day_text_1 = '<fontname="gui/fonts/g93_en.otf"><size=34><color=0X2A4B73FF>{}</color></size></fontname>'.format(idx + 1)
            item_widget.lab_days.SetString(get_text_by_id(604041).format(day_text_1))
            item_widget.temp_items.lab_quantity.setVisible(True)
            item_widget.temp_items.lab_quantity.SetString(str(item_num))

        self.refresh_list()
        self._init_get_all()

    def refresh_list(self):
        conf = confmgr.get('c_activity_config', self._activity_type)
        sub_act_list = self.panel.list_all
        task_list = activity_utils.parse_task_list(conf['cTask'])
        par_task = task_list[0]
        par_prog = global_data.player.get_task_prog(par_task)
        for i, task_id in enumerate(self._children_tasks):
            item_widget = sub_act_list.GetItem(i)
            reward_id = task_utils.get_task_reward(task_id)
            r_list = confmgr.get('common_reward_data', str(reward_id), 'reward_list', default=[])
            item_no, item_num = r_list[0]
            item_name = get_lobby_item_name(item_no)
            item_path = get_lobby_item_pic_by_item_no(item_no)
            item_widget.temp_items.item.SetDisplayFrameByPath('', item_path)
            total_times = task_utils.get_total_prog(task_id)
            jump_conf = task_utils.get_jump_conf(task_id)
            cur_times = global_data.player.get_task_prog(task_id)
            btn = item_widget.temp_items.btn_choose
            btn_bar = item_widget.btn_bar
            day_text_1 = '<fontname="gui/fonts/g93_en.otf"><outline=1 color = 0xF4FCFAAA><size=28><color=0x2B6F7DFF>{}</color></size></outline></fontname>'.format(' ' + str(i + 1) + ' ')
            day_text_2 = '<fontname="gui/fonts/g93_en.otf"><outline=1 color = 0x1C4240AA><size=28><color=0xA0FFEEFF>{}</color></size></outline></fontname>'.format(' ' + str(i + 1) + ' ')

            def check_btn(btn=btn_bar):
                has_rewarded = global_data.player.has_receive_reward(task_id)
                if has_rewarded:
                    item_widget.lab_state.SetString(get_text_by_id(604010))
                    item_widget.lab_sign.SetString(item_name)
                    item_widget.img_received.setVisible(True)
                    btn.SetEnable(False)
                elif cur_times < total_times:
                    item_widget.lab_state.SetString(get_text_by_id(604026))
                    item_widget.lab_sign.SetString(item_name)
                    item_widget.img_received.setVisible(False)
                    btn.SetEnable(False)
                else:
                    item_widget.lab_state.SetString(get_text_by_id(607961))
                    item_widget.lab_sign.SetString(item_name)
                    item_widget.img_received.setVisible(False)
                    btn.SetEnable(False)
                if par_prog == i + 1:
                    item_widget.lab_days.SetString(get_text_by_id(610722).format(day_text_1))
                    item_widget.lab_state.SetColor(5673080)
                    item_widget.lab_sign.SetColor(16776945)
                    item_widget.btn_bar.SetSelect(True)
                else:
                    item_widget.lab_days.SetString(get_text_by_id(610721).format(day_text_2))
                    item_widget.btn_bar.SetSelect(False)

            @btn.unique_callback()
            def OnClick(btn, touch, task_id=task_id):
                x, y = btn.GetPosition()
                w, h = btn.GetContentSize()
                x += w * 0.5
                wpos = btn.ConvertToWorldSpace(x, y)
                extra_info = {'show_jump': False}
                reward_id = task_utils.get_task_reward(task_id)
                r_list = confmgr.get('common_reward_data', str(reward_id), 'reward_list', default=[])
                item_no, item_num = r_list[0]
                global_data.emgr.show_item_desc_ui_event.emit(item_no, None, wpos, extra_info=extra_info, item_num=item_num)
                return

            check_btn()

    def refresh_time(self, parent_task):
        left_time = task_utils.get_raw_left_open_time(parent_task)
        if left_time > 0:
            day, _, _, _ = get_day_hour_minute_second(left_time)
            day = day + 1
            day_text = '<fontname="gui/fonts/fzdys.ttf"><size=28><color=0XFFE402FF>{}</color></size></fontname>'.format(day)
            self.panel.lab_end_time.SetString(get_text_by_id(607969).format('20', '0XFFFFFFFF', day_text))
        else:
            close_left_time = 0
            self.panel.lab_end_time.SetString(get_readable_time(close_left_time))

    def _init_get_all(self):
        player = global_data.player
        if not player:
            return
        if player.has_unreceived_task_reward(self._task_id):
            self.panel.btn_christmas_receive.lab_get.SetString(get_text_by_id(610637))
            self.panel.btn_christmas_receive.SetEnable(True)

            @self.panel.btn_christmas_receive.unique_callback()
            def OnClick(btn, touch):
                global_data.player.receive_all_task_reward(self._task_id)

        else:
            self.panel.btn_christmas_receive.SetEnable(False)
            if player.has_receive_all_rewards(self._task_id):
                self.panel.btn_christmas_receive.lab_get.SetString(get_text_by_id(604029))
            else:
                self.panel.btn_christmas_receive.lab_get.SetString(get_text_by_id(606046))