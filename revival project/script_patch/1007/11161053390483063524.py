# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivityTemplate.py
from __future__ import absolute_import
from __future__ import print_function
import six
import six_ex
from six.moves import range
import random
from common.cfg import confmgr
from logic.gutils import task_utils
from logic.gutils import activity_utils
from logic.gutils.activity_utils import is_task_finished
from logic.gutils.new_template_utils import GlActiveBoxReward
from logic.gcommon.time_utility import get_readable_time
from logic.comsys.activity.NumberChangeWidget import NumberChangeWidget

class ActivityBase(object):

    @staticmethod
    def get_custom_template_info():
        return None

    def __init__(self, dlg, activity_type):
        self.panel = dlg
        self._activity_type = activity_type
        self._need_bg = True
        self._is_init_show = True
        self._dyn_param_dict = {}

    def exec_custom_func(self, index):
        func, param_dict = self.get_func_param(index)
        if not func:
            print('[ERROR] exec_custom_func activity_type[%s] index [%d]' % (self._activity_type, index))
            return
        dyn_param_dict = self._dyn_param_dict.get(index, {})
        param_dict.update(dyn_param_dict)
        activity_utils.exec_activity_custom_func(func, **param_dict)

    def get_func_param(self, index, func_key='arrParameter'):
        return activity_utils.get_func_param(self._activity_type, index, func_key)

    def exec_custom_condition(self, index):
        return activity_utils.exec_custom_condition(self._activity_type, index)

    def set_dyn_parameter(self, index, param_dict):
        if index not in self._dyn_param_dict:
            return
        self._dyn_param_dict[index].update(param_dict)

    def set_show(self, show, is_init=False):
        self._is_init_show = is_init
        self.panel.setVisible(show)

    def on_init_panel(self):
        if self.panel.HasAnimation('show'):
            self.panel.PlayAnimation('show')
        if self.panel.HasAnimation('loop'):
            self.panel.PlayAnimation('loop')

    def on_finalize_panel(self):
        self.panel = None
        return

    def on_resolution_changed(self):
        pass

    def refresh_panel(self):
        pass

    def set_tab_panel(self, tab_panel):
        pass

    def parent_refresh_page_tab(self):
        pass

    def play_panel_animation(self):
        pass

    def need_bg(self):
        return self._need_bg

    def on_main_ui_reshow(self):
        pass

    def on_main_ui_hide(self):
        pass

    def get_panel(self):
        return self.panel


class ActivityTemplate(ActivityBase):

    def __init__(self, dlg, activity_type):
        super(ActivityTemplate, self).__init__(dlg, activity_type)
        self.init_parameters()
        self.init_event()

    def on_finalize_panel(self):
        self.process_event(False)

    def init_parameters(self):
        pass

    def init_event(self):
        self.process_event(True)

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {}
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)


class ActivityGlobalTemplate(ActivityBase):
    INTERVAL_TIMES = 15
    SIMULATE_TIMES = 20
    TIMES_SUFFIX = ''
    ACTIVITY_TYPE = ''
    GLOBAL_EVENT = {'message_update_global_stat': 'up_tick_goal_num',
       'message_update_global_reward_receive': '_update_gl_receive_state',
       'receive_task_reward_succ_event': '_init_my_task'
       }

    def __init__(self, dlg, activity_type):
        super(ActivityGlobalTemplate, self).__init__(dlg, activity_type)
        self._times = 0
        self._timer = None
        self.init_parameters()
        self.process_global_event(True)
        self._init_global_achieve_base()
        self.init_left_time()
        return

    def init_left_time(self):
        self.register_timer()
        self.second_callback()

    def init_parameters(self):
        self.ui_data = confmgr.get('c_activity_config', self._activity_type, 'cUiData')
        self._achieve_id_lst = self.ui_data.get('global_achieve_id')
        self._achieve_nodes = self.get_achieve_reward_nodes()
        self._num_widget = None
        self._gl_box_widget = {}
        self._des_num_lst = []
        self._tick_goal_num = None
        self._tick_now_num = None
        self._second_tick_increase_num = 0
        self._is_first_open = True
        fist_achieve_id = self._achieve_id_lst[0]
        self._achieve_name = confmgr.get('global_achieve_data', str(fist_achieve_id), 'cGStatName')
        self._parent_achieve = confmgr.get('global_achieve_data', str(self._achieve_id_lst[0]), 'cParentID')
        return

    def _init_global_achieve_base(self):
        for x in range(0, len(self._achieve_id_lst)):
            achieve_id = self._achieve_id_lst[x]
            des_num = confmgr.get('global_achieve_data', str(achieve_id), 'iCondValue')
            reward_id = confmgr.get('global_achieve_data', str(achieve_id), 'iRewardID')
            reward_nd, time_nd = self._achieve_nodes[x]
            self._des_num_lst.append(des_num)
            if time_nd:
                if isinstance(self.TIMES_SUFFIX, int):
                    suffix = get_text_by_id(self.TIMES_SUFFIX) if 1 else self.TIMES_SUFFIX
                    time_nd.lab_number.SetString(str(des_num) + suffix)
                box_widget = GlActiveBoxReward(reward_nd, self.on_click_global_reward, reward_id, achieve_id)
                self._gl_box_widget[achieve_id] = box_widget

        last_achieve_id = self._achieve_id_lst[-1]
        self.final_goal_num = confmgr.get('global_achieve_data', str(last_achieve_id), 'iCondValue')
        self._num_widget = NumberChangeWidget(self, self.panel.lab_number_change)
        self._init_global_achieve_sp(self.final_goal_num)
        self._update_gl_receive_state()
        self.up_tick_goal_num()

    def on_click_global_reward(self, btn, touch, data):
        archive_id = data
        global_data.player.try_get_global_achieve(archive_id)

    def _init_global_achieve_sp(self, final_goal_num):
        pass

    def _update_gl_receive_state(self):
        global_data.player.read_activity_list(self._activity_type)
        for a_id in self._achieve_id_lst:
            global_stat = global_data.player.get_gl_reward_receive_state(a_id)
            box_widget = self._gl_box_widget.get(a_id, None)
            if box_widget:
                box_widget.update_state(global_stat)

        return

    def get_achieve_reward_nodes(self):
        ret = []
        for x in range(1, len(self._achieve_id_lst) + 1):
            nd_reward = getattr(self.panel, 'temp_reward_%s' % x)
            nd_times = getattr(self.panel, 'temp_times_%s' % x)
            ret.append([nd_reward, nd_times])

        return ret

    def second_simulate_up(self, *args):
        if self._tick_goal_num is None or self._tick_now_num is None:
            return
        else:
            self._tick_now_num += self._second_tick_increase_num
            if self._tick_now_num >= self._tick_goal_num:
                self._tick_now_num = self._tick_goal_num
            self._num_widget.set_number(int(self._tick_now_num))
            self.update_progress(self.panel.nd_process, 'prog_all', self._des_num_lst, self._tick_now_num)
            return

    def up_tick_goal_num(self, *args):
        global_stat_data = global_data.player or None if 1 else global_data.player.get_global_stat_data()
        if global_stat_data is None:
            self.update_progress(self.panel.nd_process, 'prog_all', self._des_num_lst, 0)
            return
        else:
            latest_num = global_stat_data.get(str(self._parent_achieve), {}).get(self._achieve_name, 0)
            if latest_num < 0:
                return
            if self._is_first_open:
                last_cache = global_data.player or 0 if 1 else global_data.player.get_simulate_cache(self._achieve_name)
                if last_cache >= latest_num:
                    last_cache = latest_num
                self._tick_now_num = max(int(last_cache), int(latest_num * 0.99))
                random_num = random.uniform(5000, 15000)
                if latest_num - random_num > 0:
                    self._tick_now_num = max(self._tick_now_num, random_num)
                self._is_first_open = False
            if self._tick_goal_num == latest_num:
                return
            self._tick_goal_num = latest_num
            self._tick_now_num = min(self._tick_goal_num, self._tick_now_num)
            self._second_tick_increase_num = (self._tick_goal_num - self._tick_now_num) / self.SIMULATE_TIMES
            return

    def register_timer(self):
        from common.utils.timer import CLOCK
        self.unregister_timer()
        self._timer = global_data.game_mgr.get_logic_timer().register(func=self.second_callback, interval=1, mode=CLOCK)

    def unregister_timer(self):
        if self._timer:
            global_data.game_mgr.get_logic_timer().unregister(self._timer)
        self._timer = 0

    def second_callback(self):
        from logic.gutils.activity_utils import get_left_time
        left_time = get_left_time(self._activity_type)
        self.panel.lab_time.SetString(get_text_by_id(607014).format(get_readable_time(left_time)))
        self.second_simulate_up()
        self._times += 1
        if self._times > self.INTERVAL_TIMES:
            self.interval_update()
            self._times = 0

    def interval_update(self):
        self.up_tick_goal_num()

    def on_finalize_panel(self):
        self._is_first_open = True
        if self._tick_now_num > self._tick_goal_num:
            self._tick_now_num = self._tick_goal_num
        if self._tick_now_num is not None:
            global_data.player and global_data.player.set_simulate_cache(self._achieve_name, self._tick_now_num)
        self.unregister_timer()
        self.process_global_event(False)
        self._achieve_id_lst = []
        self._achieve_nodes = []
        if self._num_widget:
            self._num_widget.destroy()
            self._num_widget = None
        if self._gl_box_widget:
            for a_id, widget in six_ex.items(self._gl_box_widget):
                widget.destroy()

            self._gl_box_widget = None
        self._des_num_lst = []
        super(ActivityGlobalTemplate, self).on_finalize_panel()
        return

    def update_progress(self, parent_nd, progress_nd_name, data_lst, now_times):
        nd = getattr(parent_nd, progress_nd_name)
        if nd:
            if now_times >= data_lst[-1]:
                nd.SetPercentage(100)
            elif now_times <= data_lst[0]:
                nd.SetPercentage(0)
            else:
                interval_num = 0
                small_num = data_lst[0]
                bigger_num = data_lst[0]
                for num in data_lst:
                    if num > now_times:
                        bigger_num = num
                        break
                    else:
                        small_num = num
                        interval_num += 1

                internal_percent = 100.0 / (len(data_lst) - 1)
                percent = internal_percent * (interval_num - 1) + float(now_times - small_num) / float(bigger_num - small_num) * internal_percent
                nd.SetPercentage(percent)

    def process_global_event(self, is_bind):
        emgr = global_data.emgr
        econf = {}
        for event, func_name in six.iteritems(self.GLOBAL_EVENT):
            func = getattr(self, func_name)
            if func and callable(func):
                econf[event] = func

        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def _init_my_task(self, *args):
        pass


class ActivityGlTaskTemplate(ActivityGlobalTemplate):
    TASK_SUFFIX = ''
    MY_DATA_SUFFIX = ''
    MY_DATA_PREFIX = ''

    def __init__(self, dlg, activity_type):
        super(ActivityGlTaskTemplate, self).__init__(dlg, activity_type)
        self._init_my_task()

    def init_parameters(self):
        super(ActivityGlTaskTemplate, self).init_parameters()
        self._task_id_mine = self.ui_data.get('personal_task')
        self._children_tasks = self.ui_data.get('task_id')
        self._task_id_to_widget = {}
        self._task_des_num_lst = []

    def _init_my_task(self, *args):
        global_data.player.read_activity_list(self._activity_type)
        self._task_des_num_lst = []
        for idx, task_id in enumerate(self._children_tasks):
            total_times = task_utils.get_total_prog(task_id)
            self._task_des_num_lst.append(total_times)
            nd_times = getattr(self.panel, 'temp_times_%s' % (idx + 1))
            if isinstance(self.TASK_SUFFIX, int):
                suffix = get_text_by_id(self.TASK_SUFFIX) if 1 else self.TASK_SUFFIX
                nd_times.times_nd.SetString(str(total_times) + suffix)
                reward_id = task_utils.get_task_reward(task_id)
                nd_reward = getattr(self.panel, 'temp_reward_%s' % (idx + 1))
                if task_id in self._task_id_to_widget:
                    box_widget = self._task_id_to_widget.get(task_id)
                else:
                    box_widget = GlActiveBoxReward(nd_reward, self.on_click_my_task_reward, reward_id, task_id)
                if is_task_finished(task_id):
                    nd_times.btn_complete.SetSelect(True)
                task_reward_stat = global_data.player.get_task_reward_status(task_id)
                box_widget.update_state(task_reward_stat)
                self._task_id_to_widget[task_id] = box_widget

        self.update_my_data()

    def interval_update(self):
        super(ActivityGlTaskTemplate, self).interval_update()
        self.update_my_data()

    def update_my_data(self):
        my_times = global_data.player.get_task_prog(str(self._task_id_mine))
        suffix = get_text_by_id(self.MY_DATA_SUFFIX) if isinstance(self.MY_DATA_SUFFIX, int) else self.MY_DATA_SUFFIX
        prefix = get_text_by_id(self.MY_DATA_PREFIX) if isinstance(self.MY_DATA_PREFIX, int) else self.MY_DATA_PREFIX
        self.panel.lab_my_num.setString(prefix + str(my_times) + suffix)
        self.update_progress(self.panel, 'prog_myself', self._task_des_num_lst, my_times)

    def on_click_my_task_reward(self, btn, touch, data):
        task_id = data
        global_data.player.receive_task_reward(task_id)

    def on_finalize_panel(self):
        self._task_des_num_lst = []
        for widget in six_ex.values(self._task_id_to_widget):
            widget.destroy()

        self._task_id_to_widget = {}
        super(ActivityGlTaskTemplate, self).on_finalize_panel()