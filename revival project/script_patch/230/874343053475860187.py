# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivityDailyPlan.py
from __future__ import absolute_import
import six
from six.moves import range
from functools import cmp_to_key
from common.cfg import confmgr
from logic.comsys.activity.ActivityTemplate import ActivityBase
from logic.gutils.item_utils import get_lobby_item_pic_by_item_no, get_lobby_item_name, get_item_rare_degree
from common.utils.cocos_utils import ccp
from logic.gutils import template_utils
from logic.gutils import item_utils
from logic.gutils import task_utils
from logic.gutils import activity_utils
ALL_TASK_INDEX = -1
MAX_DAILTY_COUNT = 8
ALL_REWARD_COUNT = 6
IMG_RHOMBUS_GRAY_PATH = 'gui/ui_res_2/activity/activity_new_domestic/activity_recruit/img_friendrecruit_rhombus_gray.png'
IMG_RHOMBUS_GOLD_PATH = 'gui/ui_res_2/activity/activity_new_domestic/activity_recruit/img_friendrecruit_rhombus_gold.png'
PIC0 = 'gui/ui_res_2/common/button/btn_secondary_minor.png'
PIC1 = 'gui/ui_res_2/common/button/btn_secondary_major.png'
PIC2 = 'gui/ui_res_2/common/button/btn_secondary_useless.png'
DAILY_TASK_MAP = {}
MAX_TASK_COUNT = 0

def get_tasks(daily_index):
    global MAX_TASK_COUNT
    global DAILY_TASK_MAP
    if not DAILY_TASK_MAP:
        for k, v in six.iteritems(confmgr.get('task/alpha_task_data')):
            unlock_day = v.get('UnlockDay')
            if unlock_day is not None:
                if unlock_day not in DAILY_TASK_MAP:
                    DAILY_TASK_MAP[unlock_day] = []
                task_id = v.get('task_id')
                if task_utils.check_task_server_limit(task_id):
                    DAILY_TASK_MAP[unlock_day].append(task_id)
                    if unlock_day != -1:
                        MAX_TASK_COUNT += 1

    return DAILY_TASK_MAP.get(daily_index, [])


def has_reward_get--- This code section failed: ---

  56       0  SETUP_LOOP           72  'to 75'
           3  LOAD_GLOBAL           0  'range'
           6  LOAD_GLOBAL           1  'MAX_DAILTY_COUNT'
           9  CALL_FUNCTION_1       1 
          12  GET_ITER         
          13  FOR_ITER             58  'to 74'
          16  STORE_FAST            0  'daily_index'

  57      19  LOAD_GLOBAL           2  'get_tasks'
          22  LOAD_GLOBAL           1  'MAX_DAILTY_COUNT'
          25  BINARY_ADD       
          26  CALL_FUNCTION_1       1 
          29  STORE_FAST            1  'children_tasks'

  58      32  SETUP_LOOP           36  'to 71'
          35  LOAD_FAST             1  'children_tasks'
          38  GET_ITER         
          39  FOR_ITER             28  'to 70'
          42  STORE_FAST            2  'task_id'

  59      45  LOAD_GLOBAL           3  'global_data'
          48  LOAD_ATTR             4  'player'
          51  LOAD_ATTR             5  'is_task_reward_receivable'
          54  LOAD_FAST             2  'task_id'
          57  CALL_FUNCTION_1       1 
          60  POP_JUMP_IF_FALSE    39  'to 39'

  60      63  LOAD_GLOBAL           6  'True'
          66  RETURN_END_IF    
        67_0  COME_FROM                '60'
          67  JUMP_BACK            39  'to 39'
          70  POP_BLOCK        
        71_0  COME_FROM                '32'
          71  JUMP_BACK            13  'to 13'
          74  POP_BLOCK        
        75_0  COME_FROM                '0'

  62      75  LOAD_GLOBAL           2  'get_tasks'
          78  LOAD_GLOBAL           7  'ALL_TASK_INDEX'
          81  CALL_FUNCTION_1       1 
          84  LOAD_CONST            2  ''
          87  BINARY_SUBSCR    
          88  STORE_FAST            3  'total_task_id'

  63      91  LOAD_GLOBAL           8  'task_utils'
          94  LOAD_ATTR             9  'get_prog_rewards'
          97  LOAD_FAST             3  'total_task_id'
         100  CALL_FUNCTION_1       1 
         103  STORE_FAST            4  'prog_rewards'

  64     106  SETUP_LOOP           61  'to 170'
         109  LOAD_GLOBAL          10  'enumerate'
         112  LOAD_FAST             4  'prog_rewards'
         115  CALL_FUNCTION_1       1 
         118  GET_ITER         
         119  FOR_ITER             47  'to 169'
         122  UNPACK_SEQUENCE_2     2 
         125  STORE_FAST            5  'i'
         128  STORE_FAST            6  'reward_data'

  65     131  LOAD_FAST             6  'reward_data'
         134  LOAD_CONST            2  ''
         137  BINARY_SUBSCR    
         138  STORE_FAST            7  'count'

  66     141  LOAD_GLOBAL           3  'global_data'
         144  LOAD_ATTR             4  'player'
         147  LOAD_ATTR            11  'is_prog_reward_receivable'
         150  LOAD_FAST             3  'total_task_id'
         153  LOAD_FAST             7  'count'
         156  CALL_FUNCTION_2       2 
         159  POP_JUMP_IF_FALSE   119  'to 119'

  67     162  LOAD_GLOBAL           6  'True'
         165  RETURN_END_IF    
       166_0  COME_FROM                '159'
         166  JUMP_BACK           119  'to 119'
         169  POP_BLOCK        
       170_0  COME_FROM                '106'

  69     170  LOAD_GLOBAL          12  'False'
         173  RETURN_VALUE     
          -1  RETURN_LAST      

Parse error at or near `CALL_FUNCTION_1' instruction at offset 26


class ActivityDailyPlan(ActivityBase):

    def __init__(self, dlg, activity_type):
        ActivityBase.__init__(self, dlg, activity_type)
        self.daily_task_map = {}
        self.tab_panel = None
        self.total_task_id = None
        self.progress_weights = [
         33.0 / 541, 130.0 / 541, (33.0 + 194.0) / 541, (33.0 + 291.0) / 541, (33.0 + 388.0) / 541, (33.0 + 485.0) / 541]
        return

    def set_tab_panel(self, tab_panel):
        self.tab_panel = tab_panel

    def play_panel_animation(self):
        self.panel.StopAnimation('show')
        self.panel.PlayAnimation('show')

    def parent_refresh_page_tab(self):
        if self.tab_panel.temp_tab_list.list_tab.GetItemCount() < MAX_DAILTY_COUNT and self.sub_tabs:
            self.sub_tabs = {}
            self.cur_sub_tab = None
            self.init_left_tab()
        return

    def on_init_panel(self):
        self.daily_index = 1
        self.sub_tabs = {}
        self.cur_sub_tab = None
        self.train_day_index = global_data.player.get_alpha_train_history_attend_days()
        self.init_left_tab()
        self.init_all_reward()

        @self.panel.btn_get.btn_common_big.unique_callback()
        def OnClick(btn, touch):
            self.get_all_reward()

        has_reward = has_reward_get()
        self.panel.btn_get.btn_common_big.SetEnable(has_reward)
        self.process_event(True)
        return

    def on_finalize_panel(self):
        if self.sub_tabs and self.tab_panel:
            for index, item in six.iteritems(self.sub_tabs):
                self.tab_panel.temp_tab_list.list_tab.DeleteItemByTag(index)

        self.sub_tabs = {}
        self.cur_sub_tab = None
        left_item_list = self.panel.list_item
        left_item_list.SetInitCount(0)
        self.process_event(False)
        self.panel.FastForwardToAnimationTime('show', 0)
        return

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'task_prog_changed': self.on_update_task_progress,
           'receive_task_reward_succ_event': self.on_update_task_progress,
           'receive_task_prog_reward_succ_event': self.on_update_task_progress
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def on_update_task_progress(self, *args):
        self.refresh_list()
        self.refresh_all_reward_list()
        self.refresh_left_tab()
        self.refresh_daily(self.daily_index)
        has_reward = has_reward_get()
        self.panel.btn_get.btn_common_big.SetEnable(has_reward)
        global_data.emgr.refresh_activity_redpoint.emit()

    def init_left_tab(self):
        self.default_tab_index = self.get_goto_dailty_index()
        sub_menu_tpl = global_data.uisystem.load_template('common/i_left_second_tab_dark_list_item')
        for index in range(MAX_DAILTY_COUNT):
            item = self.tab_panel.temp_tab_list.list_tab.AddItem(sub_menu_tpl, None, bRefresh=True)
            item.button.SetText(get_text_by_id(604004).format(index + 1))
            item.img_red.setVisible(False)
            item.setTag(index)
            self.sub_tabs[index] = item
            self.add_sub_tab(item, index)

        self.tab_panel.temp_tab_list.list_tab._container._refreshItemPos()
        self.tab_panel.temp_tab_list.list_tab._refreshItemPos()
        self.refresh_left_tab()
        return

    def is_dailty_task_reward(self, daily_index):
        children_tasks = get_tasks(daily_index)
        for task in children_tasks:
            if global_data.player.is_task_reward_receivable(task):
                return True

        return False

    def is_dailty_has_receive_reward(self, daily_index):
        children_tasks = get_tasks(daily_index)
        for task in children_tasks:
            if not global_data.player.has_receive_reward(task):
                return False

        return True

    def is_task_unfinished(self, daily_index):
        children_tasks = get_tasks(daily_index)
        for task in children_tasks:
            if not global_data.player.is_task_finished(task):
                return True

        return False

    def refresh_left_tab(self):
        for index in range(MAX_DAILTY_COUNT):
            self.sub_tabs[index].img_red.setVisible(self.is_dailty_task_reward(index + 1))
            self.sub_tabs[index].img_lock.setVisible(bool(index + 1 > self.train_day_index))
            self.sub_tabs[index].img_tick.setVisible(self.is_dailty_has_receive_reward(index + 1))

    def add_sub_tab(self, item, index):

        @item.button.unique_callback()
        def OnClick(*args):
            self.refresh_daily(index + 1)
            if self.cur_sub_tab:
                self.cur_sub_tab.button.SetSelect(False)
            item.button.SetSelect(True)
            self.cur_sub_tab = item

        if index == self.default_tab_index:
            OnClick()

    def refresh_daily(self, daily_index):
        self.daily_index = daily_index
        self.panel.lab_task_title.SetString(get_text_by_id(604004).format(daily_index))
        self.show_list(daily_index)

    def show_list(self, daily_index):
        children_tasks = get_tasks(daily_index)
        children_tasks = self.reorder_task_list(children_tasks)
        self._children_tasks = children_tasks
        sub_act_list = self.panel.list_task
        sub_act_list.SetInitCount(len(children_tasks))
        for i, task_id in enumerate(children_tasks):
            item_widget = sub_act_list.GetItem(i)
            item_widget.lab_name.SetString(task_utils.get_task_name(task_id))
            reward_id = task_utils.get_task_reward(task_id)
            template_utils.init_common_reward_list_autopool(item_widget.list_reward, reward_id)

        self.refresh_list()

    def refresh_list(self):
        sub_act_list = self.panel.list_task
        for i, task_id in enumerate(self._children_tasks):
            item_widget = sub_act_list.GetItem(i)
            total_times = task_utils.get_total_prog(task_id)
            jump_conf = task_utils.get_jump_conf(task_id)
            cur_times = global_data.player.get_task_prog(task_id)
            if total_times > 1:
                item_widget.lab_num.SetString('{0}/{1}'.format(cur_times, total_times))
            else:
                item_widget.lab_num.SetString('')
            btn = item_widget.temp_btn_get.btn_common
            item_widget.nd_get.setVisible(False)

            def check_btn(btn=btn):
                has_rewarded = global_data.player.has_receive_reward(task_id)
                if has_rewarded:
                    item_widget.nd_get.setVisible(True)
                    btn.setVisible(False)
                elif cur_times < total_times:
                    btn.setVisible(True)
                    if self.daily_index > self.train_day_index:
                        btn.SetTextColor('#SK', '#SK', '#SK')
                        btn.SetText(870022)
                        btn.SetEnable(False)
                    elif jump_conf:
                        btn.SetText(80284)
                        btn.SetTextColor('#SW', '#SW', '#SW')
                        btn.SetFrames('', [PIC0, PIC0, PIC2], False, None)
                        btn.SetEnable(True)
                    else:
                        btn.SetTextColor('#SK', '#SK', '#SK')
                        btn.SetEnable(False)
                        btn.SetText(604030)
                else:
                    btn.SetTextColor('#SK', '#SK', '#SK')
                    btn.SetFrames('', [PIC1, PIC1, PIC2], False, None)
                    btn.setVisible(True)
                    btn.SetEnable(True)
                    btn.SetText(604030)
                return

            @btn.unique_callback()
            def OnClick(btn, touch, task_id=task_id):
                if not activity_utils.is_activity_in_limit_time(self._activity_type):
                    return
                _total_times = task_utils.get_total_prog(task_id)
                _cur_times = global_data.player.get_task_prog(task_id)
                jump_conf = task_utils.get_jump_conf(task_id)
                if _cur_times < _total_times:
                    item_utils.exec_jump_to_ui_info(jump_conf)
                else:
                    global_data.player.receive_task_reward(task_id)
                    btn.SetText(80866)
                    btn.SetEnable(False)

            check_btn()

    def reorder_task_list(self, tasks):

        def cmp_func(task_id_a, task_id_b):
            has_rewarded_a = global_data.player.has_receive_reward(task_id_a)
            has_rewarded_b = global_data.player.has_receive_reward(task_id_b)
            total_times_a = task_utils.get_total_prog(task_id_a)
            cur_times_a = global_data.player.get_task_prog(task_id_a)
            total_times_b = task_utils.get_total_prog(task_id_b)
            cur_times_b = global_data.player.get_task_prog(task_id_b)
            finish_a = cur_times_a >= total_times_a
            finish_b = cur_times_b >= total_times_b
            if has_rewarded_a != has_rewarded_b:
                if has_rewarded_a:
                    return 1
                if has_rewarded_b:
                    return -1
            if finish_a != finish_b:
                if finish_a:
                    return -1
                if finish_b:
                    return 1
            return 0

        ret_list = sorted(tasks, key=cmp_to_key(cmp_func))
        return ret_list

    def init_all_reward(self):
        self.total_task_id = get_tasks(ALL_TASK_INDEX)[0]
        prog_rewards = task_utils.get_prog_rewards(self.total_task_id)
        left_item_list = self.panel.list_item
        left_item_list.SetInitCount(len(prog_rewards))
        self.refresh_all_reward_list()

    def refresh_all_reward_list(self):
        finish_task_count = global_data.player.get_task_prog(self.total_task_id)
        progress_index = 0
        progress_sub_percent = 0.0
        temp_task_count = finish_task_count
        pre_reward_task_count = 0
        left_item_list = self.panel.list_item
        prog_rewards = task_utils.get_prog_rewards(self.total_task_id)
        self.panel.lab_finish_task.SetString(get_text_by_id(607701).format(finish_task_count, prog_rewards[-1][0]))
        task_count = len(prog_rewards)
        for i, reward_data in enumerate(prog_rewards):
            count = reward_data[0]
            reward_id = reward_data[1]
            item_widget = left_item_list.GetItem(i)
            item_widget.lab_node_num.SetString(str(count))
            if finish_task_count >= count:
                progress_index += 1
                item_widget.img_node.SetDisplayFrameByPath('', IMG_RHOMBUS_GOLD_PATH)
            else:
                item_widget.img_node.SetDisplayFrameByPath('', IMG_RHOMBUS_GRAY_PATH)
                if finish_task_count > pre_reward_task_count:
                    progress_sub_percent = float(finish_task_count - pre_reward_task_count) / (count - pre_reward_task_count)
            pre_reward_task_count = count
            has_receive_prog_reward = global_data.player.has_receive_prog_reward(self.total_task_id, count)
            item_widget.img_get.setVisible(has_receive_prog_reward)
            if has_receive_prog_reward:
                item_widget.temp_item.item.SetColor('#SH')
            reward_conf = confmgr.get('common_reward_data', str(reward_id))
            if not reward_conf:
                log_error('reward_id is not exist in common_reward_data', reward_id)
                continue
            reward_list = reward_conf.get('reward_list', [])
            if len(reward_list) != 1:
                log_error('reward_id count errr')
                continue
            item_no, item_num = reward_list[0]
            if global_data.player.is_prog_reward_receivable(self.total_task_id, count):
                item_widget.temp_item.PlayAnimation('get_tips')
                callback = self.get_touch_callback(self.total_task_id, count)
                template_utils.init_tempate_mall_i_item(item_widget.temp_item, item_no, item_num, show_tips=True, callback=callback)
            else:
                item_widget.temp_item.StopAnimation('get_tips')
                item_widget.temp_item.nd_get_tips.setVisible(False)
                template_utils.init_tempate_mall_i_item(item_widget.temp_item, item_no, item_num, show_tips=True)

        self.panel.progress_bar.SetPercentage(self.get_precent(progress_index, progress_sub_percent))

    def get_touch_callback(self, total_task_id, count):

        def callback():
            global_data.player.receive_task_prog_reward(total_task_id, count)

        return callback

    def get_precent(self, progress_index, progress_sub_percent):
        percent = 0.0
        if progress_index >= ALL_REWARD_COUNT:
            percent = 1
        elif progress_index == 0:
            percent = self.progress_weights[progress_index] * progress_sub_percent
        else:
            percent = self.progress_weights[progress_index - 1] + (self.progress_weights[progress_index] - self.progress_weights[progress_index - 1]) * progress_sub_percent
        return int(percent * 100)

    def get_all_reward(self):
        global_data.player.receive_all_task_reward(self.total_task_id)
        total_task_id = get_tasks(ALL_TASK_INDEX)[0]
        prog_rewards = task_utils.get_prog_rewards(total_task_id)
        for i, reward_data in enumerate(prog_rewards):
            count = reward_data[0]
            if global_data.player.is_prog_reward_receivable(total_task_id, count):
                global_data.player.receive_task_prog_reward(total_task_id, count)

    def get_goto_dailty_index(self):
        for index in range(MAX_DAILTY_COUNT):
            if self.is_dailty_task_reward(index + 1):
                return index

        if self.is_task_unfinished(self.train_day_index):
            return self.train_day_index - 1
        return 0