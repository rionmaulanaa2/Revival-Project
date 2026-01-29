# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/ctypes/TaskStatistics.py
from __future__ import absolute_import
import six
from six.moves import range
from data.task import task_data
from data.task.task_const_template import parse_tmp_const_value
from logic.gcommon import time_utility as tutil
from logic.gutils.task.task_factory import get_task_class
import logic.gcommon.common_const.task_const as tconst
from logic.gcommon.item import item_const
from mobile.distserver.game import GameServerRepo
from logic.gcommon.cdata import season_data
from data.task import season_task_data

class TaskStatistics(object):

    def __init__(self, logger, owner):
        self._owner = owner
        self._sprop_tasks = {}
        self._ordered_tasks = {}
        self._multi_stat_tasks = set([])
        self._id2tasks = {}
        self._logger = logger
        self._get_task_func = {tconst.DAYLY_FRESH: self.get_day_tasks,
           tconst.DAYLY5_FRESH: self.get_day5_tasks,
           tconst.WEEKLY_FRESH: self.get_week_tasks,
           tconst.WEEKLY5_FRESH: self.get_week5_tasks,
           tconst.WEEKLY_THURSDAY_5_FRESH: self.get_week_thursday_5_tasks,
           tconst.SEASON_FRESH: self.get_season_tasks,
           tconst.BATTLE_SEASON_FRESH: self.get_battle_season_tasks,
           tconst.NOT_FRESH: self.get_notfresh_tasks
           }
        self._notfresh_tasks = {}
        self.changed_data = {}
        self._day_prog_limit_tasks = set()
        self._deleted_task_data = {}

    def destroy(self):
        for task_func in six.itervalues(self._get_task_func):
            task_data = task_func()
            for task in six.itervalues(task_data):
                task.destroy()

        self._logger = None
        self._sprop_tasks = None
        self._ordered_tasks = None
        self._multi_stat_tasks = None
        self._owner = None
        self._get_task_func = None
        self._notfresh_tasks = None
        return

    def init_from_dict(self, bdict):
        self._notfresh_tasks = bdict.get('notfresh_task_data', {})
        self._deleted_task_data = bdict.get('deleted_task_data', {})
        for task_func in six.itervalues(self._get_task_func):
            task_data_dict = task_func()
            self.load_task_obj(task_data_dict)

        now = tutil.time()
        real_del_task_ids = []
        for task_id, task_info in six.iteritems(self._deleted_task_data):
            if now - task_info.get('delete_time', 0) > tutil.ONE_DAY_SECONDS * 30:
                real_del_task_ids.append(task_id)

        for task_id in real_del_task_ids:
            del self._deleted_task_data[task_id]

    def load_task_obj(self, task_data):
        del_task_ids = []
        for task_id, task_info in six.iteritems(task_data):
            task = self.load_task_class(task_id)
            if task:
                task.init_from_dict(task_info)
                task_data[task_id] = task
            else:
                self._deleted_task_data[task_id] = task_info
                self._deleted_task_data[task_id]['delete_time'] = tutil.time()
                del_task_ids.append(task_id)

        for del_task_id in del_task_ids:
            del task_data[del_task_id]

    def load_task_class(self, task_id):
        if not task_data.check_has_task(task_id):
            return None
        else:
            task_template_conf = task_data.get_task_template_conf(task_id)
            cls_name = task_template_conf.get('class_type', 'CommonTask')
            task_class = get_task_class(cls_name)
            task = task_class(self._owner, task_id)
            task.init_from_dict({})
            return task

    def get_client_dict(self):
        cdict = {'day_task_data': {task.task_id:task.get_client_dict() for task in six.itervalues(self.get_day_tasks())},'day5_task_data': {task.task_id:task.get_client_dict() for task in six.itervalues(self.get_day5_tasks())},'week_task_data': {task.task_id:task.get_client_dict() for task in six.itervalues(self.get_week_tasks())},'week5_task_data': {task.task_id:task.get_client_dict() for task in six.itervalues(self.get_week5_tasks())},'thursday_task_data': {task.task_id:task.get_client_dict() for task in six.itervalues(self.get_week_thursday_5_tasks())},'season_task_data': {task.task_id:task.get_client_dict() for task in six.itervalues(self.get_season_tasks())},'battle_season_task_data': {task.task_id:task.get_client_dict() for task in six.itervalues(self.get_battle_season_tasks())},'notfresh_task_data': {task.task_id:task.get_client_dict() for task in six.itervalues(self.get_notfresh_tasks())}}
        return cdict

    def get_persistent_dict(self):
        pdict = {'notfresh_task_data': {task.task_id:task.get_persistent_dict() for task in six.itervalues(self.get_notfresh_tasks())},'deleted_task_data': self._deleted_task_data
           }
        return pdict

    def init_tasks(self):
        self._sprop_tasks.clear()

    def register_task(self, task_id):
        task_id = str(task_id)
        task_conf = task_data.get_task_conf(task_id)
        if not task_conf:
            return
        else:
            children_task = task_conf.get('children_task', [])
            parent_task = task_conf.get('parent_task', None)
            is_order = task_conf.get('is_order', 0)
            if not task_data.check_server_limit(task_id):
                return
            init_finish = task_conf.get('init_finish', 0)
            task = self.get_task_by_id(task_id, False)
            day_limit_prog = task_conf.get('day_limit_prog', 0)
            if day_limit_prog:
                self._day_prog_limit_tasks.add(task_id)
            if not task and init_finish and self._check_task_active(task_id):
                task = self.get_task_by_id(task_id, True)
                if not task.is_finished():
                    self.set_task_finished(task_id)
                children_task = task_data.get_children_task(task_id)
                for child_task_id in children_task:
                    child_task = self.get_task_by_id(child_task_id, True)
                    if not child_task.is_finished():
                        self.set_task_finished(child_task_id)

            if children_task:
                if is_order:
                    self._ordered_tasks[task_id] = children_task
                    return
                else:
                    auto_regist_children = task_conf.get('manual_regist_children', 0) <= 0
                    if auto_regist_children:
                        for child in children_task:
                            self.register_task(child)

                    return

            elif parent_task and is_order:
                return
            task_template_conf = task_data.get_task_template_conf(task_id)
            statistics_types = task_template_conf.get('statistics_type', [])
            if len(statistics_types) > 1:
                self._multi_stat_tasks.add(task_id)
            elif len(statistics_types) == 1:
                st_prop = statistics_types[0]
                self._sprop_tasks.setdefault(st_prop, set([]))
                if task_id not in self._sprop_tasks[st_prop]:
                    self._sprop_tasks[st_prop].add(task_id)
            init_func = task_template_conf.get('init_func', None)
            arg = task_data.get_arg(task_id)
            arg = parse_tmp_const_value(arg)
            if init_func:
                task = self.get_task_by_id(task_id, True)
                if task:
                    self.update_task_prog_by_id(task_id, init_func(self._owner, arg), None, True)
            return

    def reset_task_prog(self, task_id):
        task = self.get_task_by_id(task_id)
        if task:
            task.set_task_progress(0)

    def unregister_task(self, task_id):
        task_conf = task_data.get_task_conf(task_id)
        children_task = task_conf.get('children_task', [])
        parent_task = task_conf.get('parent_task', None)
        is_order = task_conf.get('is_order', 0)
        if task_id in self._day_prog_limit_tasks:
            self._day_prog_limit_tasks.remove(task_id)
        if children_task:
            if is_order:
                self._ordered_tasks.pop(task_id, None)
                return
            for child in children_task:
                self.unregister_task(child)

        elif parent_task and is_order:
            return
        task_template_conf = task_data.get_task_template_conf(task_id)
        statistic_types = task_template_conf.get('statistics_type', [])
        if len(statistic_types) > 1 and task_id in self._multi_stat_tasks:
            self._multi_stat_tasks.remove(task_id)
        elif len(statistic_types) == 1:
            st_prop = statistic_types[0]
            prop_tasks = self._sprop_tasks.get(st_prop, set([]))
            if prop_tasks and task_id in prop_tasks:
                prop_tasks.remove(task_id)
        return

    def clear_task_data(self, task_id):
        fresh_type = task_data.get_fresh_type(task_id)
        tasks = self._get_task_func[fresh_type]()
        if tasks:
            task = tasks.pop(task_id, None)
            task and task.destroy()
            self._owner.call_client_method('clear_task', (task_id,))
        task_conf = task_data.get_task_conf(task_id)
        children_task = task_conf.get('children_task', [])
        for child in children_task:
            self.clear_task_data(child)

        return

    def get_day_tasks(self):
        return self._owner.get_day_cycle_data('day_task', tutil.CYCLE_DATA_REFRESH_TYPE_1)

    def get_day5_tasks(self):
        return self._owner.get_day_cycle_data('day5_task', tutil.CYCLE_DATA_REFRESH_TYPE_2)

    def get_week_tasks(self):
        return self._owner.get_week_cycle_data('week_task', tutil.CYCLE_DATA_REFRESH_TYPE_1)

    def get_week5_tasks(self):
        return self._owner.get_week_cycle_data('week_task', tutil.CYCLE_DATA_REFRESH_TYPE_2)

    def get_week_thursday_5_tasks(self):
        return self._owner.get_thursday_cycle_data('week_task', tutil.CYCLE_DATA_REFRESH_TYPE_2)

    def get_season_tasks(self):
        return self._owner.get_season_cycle_data('season_task', tutil.CYCLE_DATA_REFRESH_TYPE_1)

    def get_battle_season_tasks(self):
        return self._owner.get_season_cycle_data('battle_season_task', tutil.CYCLE_DATA_REFRESH_TYPE_1)

    def get_notfresh_tasks(self):
        return self._notfresh_tasks

    def get_task_by_id(self, task_id, create=False):
        if not task_data.check_has_task(task_id):
            return None
        else:
            fresh_type = task_data.get_fresh_type(task_id)
            tasks = self._get_task_func[fresh_type]()
            if task_id not in tasks:
                if create:
                    task = self.load_task_class(task_id)
                    tasks[task_id] = task
                    return task
                return None
            return tasks[task_id]

    def _check_battle_type(self, map_type, task_id):
        task_conf = task_data.get_task_conf(task_id)
        map_type_const = task_conf.get('map_type', None)
        if map_type_const is None:
            return True
        else:
            map_types = parse_tmp_const_value(map_type_const)
            if map_types is None:
                return True
            if map_type not in map_types:
                return False
            return True

    def update_normal_task_prog(self, st_key, value, battle_type=None):
        task_list = self._sprop_tasks.get(st_key, set([]))
        for task_id in task_list:
            self.update_task_prog_by_id(task_id, value, battle_type)

    def update_task_prog_by_id(self, task_id, value, battle_type=None, is_init=False):
        if battle_type and not self._check_battle_type(battle_type, task_id):
            return
        if not self._check_task_active(task_id):
            return
        task = self.get_task_by_id(task_id, True)
        if not self.need_continue_update_prog(task_id):
            return
        try:
            self.update_task_prog(task, value, is_init)
        except Exception as e:
            import traceback
            self._logger.log_last_except()
            log_error('[Avatar %s-%s]Failed to update the progress of task, task_id=%s, exception=%s', self._owner.uid, self._owner.id, task_id, str(e))
            return

    def update_ordered_task_prog(self, statistics, battle_type=None):
        for parent_task_id, children_task in six.iteritems(self._ordered_tasks):
            if battle_type and not self._check_battle_type(battle_type, parent_task_id):
                continue
            if not self.need_continue_update_prog(parent_task_id):
                continue
            if not self._check_task_active(parent_task_id):
                continue
            parent_task = self.get_task_by_id(parent_task_id, True)
            cur_idx = parent_task.get_idx()
            for idx in range(cur_idx, len(children_task)):
                child_task_id = children_task[idx]
                task_tempate_conf = task_data.get_task_template_conf(child_task_id)
                statistic_types = task_tempate_conf.get('statistics_type', set([]))
                if self._task_has_finished(child_task_id):
                    continue
                for st_prop in statistic_types:
                    st_value = statistics.get(st_prop, None)
                    if st_value:
                        self.update_task_prog_by_id(child_task_id, st_value, battle_type)
                        if self._task_has_finished(child_task_id):
                            break

                break

        return

    def update_multi_stat_task_prog(self, statistics, battle_type=None):
        for task_id in self._multi_stat_tasks:
            task_tempate_conf = task_data.get_task_template_conf(task_id)
            statistic_types = task_tempate_conf.get('statistics_type', set([]))
            need_update = False
            for st_prog in statistic_types:
                if st_prog in statistics:
                    need_update = True

            if need_update:
                self.update_task_prog_by_id(task_id, statistics, battle_type)

    def update_task_prog(self, task, st_value, is_init=False):
        old_prog = task.prog
        old_max_prog = task.max_prog
        task.update_prog(st_value, is_init)
        self.handle_task_prog_updated(task, old_prog, old_max_prog)

    def handle_task_prog_updated(self, task, old_prog, old_max_prog):
        if not task:
            return
        if task.prog == old_prog:
            return
        task_id = task.task_id
        if task.is_finished():
            self._owner._call_meta_member_func('on_@_task_finished', task_id)
            parent_task_id = task_data.get_parent_task(task_id)
            if parent_task_id and parent_task_id in self._ordered_tasks:
                parent_task = self.get_task_by_id(parent_task_id, True)
                idx = self._ordered_tasks[parent_task_id].index(task_id)
                parent_task.update_idx(idx + 1)
        self.on_task_prog_updated(task, old_prog, old_max_prog)

    def update_parent_task_prog(self, parent_task_id, prod_add=None, is_child_finished=False):
        parent_task = self.get_task_by_id(parent_task_id, True)
        parent_task_conf = task_data.get_task_conf(parent_task_id)
        if parent_task and parent_task.prog >= parent_task.get_total_prog():
            return
        st_value = {'prog': prod_add,
           'is_child_finished': is_child_finished
           }
        self.update_task_prog(parent_task, st_value, False)

    def _check_task_active(self, task_id):
        task_conf = task_data.get_task_conf(task_id)
        if not task_conf:
            return False
        start_time = task_data.get_start_time(task_id)
        end_time = task_data.get_end_time(task_id)
        if not start_time and not end_time:
            parent_task_id = task_data.get_parent_task(task_id)
            if parent_task_id:
                start_time = task_data.get_start_time(parent_task_id)
                end_time = task_data.get_end_time(parent_task_id)
            if task_id in season_task_data.data:
                season_task_conf = season_task_data.data[task_id]
                limit_cur_week = season_task_conf.get('limit_cur_week', 0)
                if limit_cur_week:
                    season = season_task_conf['season']
                    season_week = season_task_conf['season_week']
                    start_time = season_data.get_start_timestamp(season) + (season_week - 1) * tutil.ONE_WEEK_SECONDS
                    end_time = start_time + tutil.ONE_WEEK_SECONDS
        if start_time and end_time:
            now = tutil.time()
            if now < start_time or now >= end_time:
                return False
        week_limit_time_conf = task_conf.get('week_time_limit', [])
        if week_limit_time_conf:
            is_active = False if 1 else True
            for start_weekday, start_hour, end_weekday, end_hour in week_limit_time_conf:
                cur_week_day_no = tutil.get_weekday()
                cur_hour = tutil.get_hour()
                if start_weekday < cur_week_day_no < end_weekday:
                    is_active = True
                    break
                elif cur_week_day_no == start_weekday:
                    if cur_hour >= start_hour:
                        if end_weekday > cur_week_day_no:
                            is_active = True
                            break
                        elif cur_hour < end_hour:
                            is_active = True
                            break
                elif cur_week_day_no == end_weekday and cur_hour < end_hour:
                    is_active = True
                    break

            return is_active or False
        active_lv = task_data.get_active_lv(task_id)
        if active_lv and self._owner.get_lv() < active_lv:
            return False
        return True

    def set_task_progress(self, task_id, progress, need_check_active=True, notify_client=True):
        task_conf = task_data.get_task_conf(task_id)
        task = self.get_task_by_id(task_id, True)
        old_prog = task.prog
        old_max_prog = task.max_prog
        task.set_prog(min(progress, task.get_total_prog()))
        self.handle_task_prog_updated(task, old_prog, old_max_prog)
        if notify_client:
            self.notify_client()

    def need_handle_finished(self, task_id):
        task = self.get_task_by_id(task_id, False)
        if not task:
            return False
        return self._task_has_finished(task_id)

    def need_continue_update_prog(self, task_id):
        return not self._task_has_finished(task_id) or task_data.has_virtual_prog(task_id)

    def set_task_finished(self, task_id):
        task = self.get_task_by_id(task_id, True)
        if not task:
            return
        old_prog = task.prog
        old_max_prog = task.max_prog
        task.set_prog(task.get_total_prog())
        self.handle_task_prog_updated(task, old_prog, old_max_prog)

    def set_all_task_finished(self):
        for task_id in six.iterkeys(task_data.data):
            self.set_task_finished(task_id)

    def on_task_prog_updated(self, task, old_prog, old_max_prog):
        task.on_prog_updated()
        if task.prog != old_prog:
            self._owner.sa_log_update_task_prog(task.task_id, old_prog, task.prog)
            self.changed_data[task.task_id] = task.get_prog_update_dict()
        if task.prog > old_prog:
            task_conf = task_data.get_task_conf(task.task_id)
            parent_task_id = task_conf.get('parent_task', None)
            child_add_parent_prog_conf = task_data.get_child_add_parent_prog_conf(task.task_id)
            if parent_task_id and child_add_parent_prog_conf and task.prog > old_max_prog:
                parent_add_prog = 0
                prog_conf_idx = 0
                start_prog = max(old_max_prog, old_prog)
                for prog in range(start_prog + 1, task.prog + 1):
                    for conf_idx in range(prog_conf_idx, len(child_add_parent_prog_conf)):
                        b_child_prog, e_child_prog, add_prog = child_add_parent_prog_conf[conf_idx]
                        if b_child_prog <= prog <= e_child_prog:
                            parent_add_prog += add_prog
                            prog_conf_idx = conf_idx
                            break

                self.update_parent_task_prog(parent_task_id, parent_add_prog)
            if parent_task_id and self._task_has_finished(task.task_id):
                parent_add_prog = task_data.get_parent_prog_addition(task.task_id)
                if parent_add_prog is None:
                    parent_add_prog = 1
                self.update_parent_task_prog(parent_task_id, parent_add_prog, True)
            if task.reward_st == item_const.ITEM_UNRECEIVED and task_data.is_auto_receive_reward(task.task_id):
                self._owner.receive_reward_by_id(task.task_id)
            if task_data.is_auto_receive_prog_reward(task.task_id):
                self._owner.receive_task_prog_reward_by_id(task.task_id, task.prog)
        return

    def notify_client(self):
        if self.changed_data:
            self._owner.call_client_method('togather_update_task_prog', (self.changed_data,))
        self.changed_data = {}

    def get_task_progress(self, task_id):
        task = self.get_task_by_id(task_id)
        if not task:
            return 0
        return task.prog

    def get_task_max_progress(self, task_id):
        task = self.get_task_by_id(task_id)
        if not task:
            return 0
        return task.max_prog

    def get_task_virtual_prog(self, task_id):
        task = self.get_task_by_id(task_id)
        if not task:
            return 0
        return task.virtual_prog

    def _task_has_finished(self, task_id):
        task = self.get_task_by_id(task_id)
        if not task:
            return False
        return task.is_finished()

    def get_task_order_idx(self, task_id):
        task = self.get_task_by_id(task_id)
        if not task:
            return 0
        return task.get_idx()

    def get_badge_level(self, task_id):
        task = self.get_task_by_id(task_id)
        if not task:
            return 0
        return task.get_badge_level()