# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/avatarmembers/impTask.py
from __future__ import absolute_import
import six
import six_ex
from mobile.common.rpcdecorator import rpc_method, CLIENT_STUB
from mobile.common.RpcMethodArgs import Str, Int, Bool, List, Dict
from logic.gcommon.item.item_const import ITEM_UNRECEIVED, ITEM_RECEIVED, ITEM_UNGAIN
from common.cfg import confmgr
from logic.gcommon.ctypes.Record import Record
from logic.gcommon.common_const import task_const
from logic.gutils import task_utils

class impTask(object):

    def _init_task_from_dict(self, bdict):
        day_task_data = bdict.get('day_task_data', {})
        day5_task_data = bdict.get('day5_task_data', {})
        week_task_data = bdict.get('week_task_data', {})
        week5_task_data = bdict.get('week5_task_data', {})
        thursday_task_data = bdict.get('thursday_task_data', {})
        season_task_data = bdict.get('season_task_data', {})
        battle_season_task_data = bdict.get('battle_season_task_data', {})
        notfresh_task_data = bdict.get('notfresh_task_data', {})
        self._unlocked_retrospect_tasks = bdict.get('unlocked_retrospect_tasks', [])
        self._frtype2task_dict = {task_const.DAYLY_FRESH: day_task_data,
           task_const.DAYLY5_FRESH: day5_task_data,
           task_const.WEEKLY_FRESH: week_task_data,
           task_const.WEEKLY5_FRESH: week5_task_data,
           task_const.WEEKLY_THURSDAY_5_FRESH: thursday_task_data,
           task_const.SEASON_FRESH: season_task_data,
           task_const.BATTLE_SEASON_FRESH: battle_season_task_data,
           task_const.NOT_FRESH: notfresh_task_data
           }
        self._anniv_7day_task_end_time = bdict.get('anniv_7day_task_end_time', 0)

    def is_retrospect_task_unlocked(self, task_id):
        return task_id in self._unlocked_retrospect_tasks

    def get_task_prog(self, task_id):
        task_id = str(task_id)
        fresh_type = task_utils.get_task_fresh_type(task_id)
        task_data_dict = self._frtype2task_dict[fresh_type]
        return task_data_dict.get(task_id, {}).get('prog', 0)

    def get_task_day_prog(self, task_id):
        task_id = str(task_id)
        fresh_type = task_utils.get_task_fresh_type(task_id)
        task_data_dict = self._frtype2task_dict[fresh_type]
        return task_data_dict.get(task_id, {}).get('day_prog', 0)

    def get_task_reward_status(self, task_id):
        task_id = str(task_id)
        fresh_type = task_utils.get_task_fresh_type(task_id)
        task_data_dict = self._frtype2task_dict[fresh_type]
        if self.is_task_finished(task_id) and not task_utils.get_task_reward(task_id) and not task_utils.get_select_rewards(task_id):
            return ITEM_RECEIVED
        else:
            if task_utils.get_task_reward_lv(task_id) > self.get_lv():
                return ITEM_UNGAIN
            return task_data_dict.get(task_id, {}).get('reward_st', ITEM_UNGAIN)

    def get_task_select_reward_id(self, task_id):
        task_id = str(task_id)
        fresh_type = task_utils.get_task_fresh_type(task_id)
        task_data_dict = self._frtype2task_dict[fresh_type]
        return task_data_dict.get(task_id, {}).get('reward_id', 0)

    def get_task_children_idx(self, task_id):
        fresh_type = task_utils.get_task_fresh_type(task_id)
        task_data_dict = self._frtype2task_dict[fresh_type]
        return task_data_dict.get(task_id, {}).get('cur_idx', 0)

    def get_task_finished_child_count(self, task_id):
        fresh_type = task_utils.get_task_fresh_type(task_id)
        task_data_dict = self._frtype2task_dict[fresh_type]
        return task_data_dict.get(task_id, {}).get('finished_child_count', 0)

    def get_task_max_prog(self, task_id):
        fresh_type = task_utils.get_task_fresh_type(task_id)
        task_data_dict = self._frtype2task_dict[fresh_type]
        return task_data_dict.get(task_id, {}).get('max_prog', 0)

    def get_task_content(self, task_id, content_key, default=None):
        task_id = str(task_id)
        fresh_type = task_utils.get_task_fresh_type(task_id)
        task_data_dict = self._frtype2task_dict[fresh_type]
        return task_data_dict.get(task_id, {}).get(content_key, default)

    def get_task_reward_rec_time(self, task_id):
        task_id = str(task_id)
        fresh_type = task_utils.get_task_fresh_type(task_id)
        task_data_dict = self._frtype2task_dict[fresh_type]
        return task_data_dict.get(task_id, {}).get('reward_rec_time', 0)

    def get_task_prog_rec_time_dict(self, task_id):
        task_id = str(task_id)
        fresh_type = task_utils.get_task_fresh_type(task_id)
        task_data_dict = self._frtype2task_dict[fresh_type]
        return task_data_dict.get(task_id, {}).get('prog_rec_time', {})

    def get_task_prog_rec_time(self, task_id, prog):
        task_id = str(task_id)
        return self.get_task_prog_rec_time_dict(task_id).get(str(prog), 0)

    def update_task_data(self, task_id, key, value):
        fresh_type = task_utils.get_task_fresh_type(task_id)
        task_data_dict = self._frtype2task_dict[fresh_type]
        task_data_dict.setdefault(task_id, {})
        task_data_dict[task_id][key] = value

    def is_task_finished(self, task_id):
        prog = self.get_task_prog(task_id)
        return prog >= task_utils.get_total_prog(task_id)

    def has_unreceived_task_reward(self, task_id):
        if self.get_task_reward_status(task_id) == ITEM_UNRECEIVED:
            return True
        children_task = task_utils.get_task_conf_by_id(task_id).get('children_task', [])
        for child_task in children_task:
            if self.has_unreceived_task_reward(child_task):
                return True

        return False

    def has_receive_all_rewards(self, task_id):
        if self.get_task_reward_status(task_id) == ITEM_UNRECEIVED:
            return False
        children_task = task_utils.get_task_conf_by_id(task_id).get('children_task', [])
        for child_task in children_task:
            if not self.has_receive_reward(child_task):
                return False

        return True

    def is_task_reward_receivable(self, task_id):
        return self.get_task_reward_status(task_id) == ITEM_UNRECEIVED

    def is_all_received_reward(self, task_id):
        if not self.has_receive_reward(task_id):
            return False
        children_task = task_utils.get_task_conf_by_id(task_id).get('children_task', [])
        for child_task in children_task:
            if not self.is_all_received_reward(child_task):
                return False

        return True

    def has_receive_reward(self, task_id):
        if self.get_task_reward_status(task_id) < ITEM_RECEIVED:
            return False
        return True

    def has_receive_prog_reward(self, task_id, prog):
        fresh_type = task_utils.get_task_fresh_type(task_id)
        task_data_dict = self._frtype2task_dict[fresh_type].get(task_id, {})
        return prog in task_data_dict.get('prog_rewards', {})

    def is_prog_reward_receivable(self, task_id, prog, check_exist=False):
        if self.has_receive_prog_reward(task_id, prog):
            return False
        if check_exist and not task_utils.has_prog_reward(task_id, prog):
            return False
        cur_prog = self.get_task_prog(task_id)
        return cur_prog >= prog

    @rpc_method(CLIENT_STUB, (Dict('tasks_data'),))
    def update_tasks_data(self, tasks_data):
        prog_changes = []
        max_prog_changes = []
        for task_id, task_data in six.iteritems(tasks_data):
            fresh_type = task_utils.get_task_fresh_type(task_id)
            self._frtype2task_dict[fresh_type].setdefault(task_id, {'prog': 0,'reward_st': ITEM_UNGAIN})
            task_data_dict = self._frtype2task_dict[fresh_type][task_id]
            prev_prog = task_data_dict.get('prog', 0)
            prev_max_prog = task_data_dict.get('max_prog', 0)
            task_data_dict.update(task_data)
            cur_prog = task_data_dict.get('prog', 0)
            cur_max_prog = task_data_dict.get('max_prog', 0)
            if prev_prog != cur_prog:
                prog_changes.append(TaskAttrChange(task_id, prev_prog, cur_prog))
            if prev_max_prog != cur_max_prog:
                max_prog_changes.append(TaskAttrChange(task_id, prev_max_prog, cur_max_prog))

        if prog_changes:
            global_data.emgr.task_prog_changed.emit(prog_changes)
        if max_prog_changes:
            global_data.emgr.task_max_prog_changed.emit(max_prog_changes)

    @rpc_method(CLIENT_STUB, (Int('task_id'),))
    def unlock_retrospect_task_succeed(self, task_id):
        self._unlocked_retrospect_tasks.append(task_id)
        global_data.emgr.retrospect_task_unlocked.emit()
        global_data.game_mgr.show_tip(18294)

    def update_task_prog_data(self, task_id, data, prog_changes_out=None, max_prog_changes_out=None):
        fresh_type = task_utils.get_task_fresh_type(task_id)
        self._frtype2task_dict[fresh_type].setdefault(task_id, {'prog': 0,'reward_st': ITEM_UNGAIN})
        task_data_dict = self._frtype2task_dict[fresh_type][task_id]
        prev_prog = task_data_dict.get('prog', 0)
        prev_max_prog = task_data_dict.get('max_prog', 0)
        task_data_dict.update(data)
        cur_prog = task_data_dict.get('prog', 0)
        cur_max_prog = task_data_dict.get('max_prog', 0)
        if self.is_task_finished(task_id):
            has_reward = bool(task_utils.get_task_reward(task_id)) or bool(task_utils.get_select_rewards(task_id))
            if has_reward and self.get_task_reward_status(task_id) != ITEM_RECEIVED:
                task_data_dict['reward_st'] = ITEM_UNRECEIVED
            else:
                task_data_dict['reward_st'] = ITEM_RECEIVED
        else:
            task_data_dict['reward_st'] = ITEM_UNGAIN
        if prev_prog != cur_prog:
            if isinstance(prog_changes_out, list):
                prog_changes_out.append(TaskAttrChange(task_id, prev_prog, cur_prog))
        if prev_max_prog != cur_max_prog:
            if isinstance(max_prog_changes_out, list):
                max_prog_changes_out.append(TaskAttrChange(task_id, prev_max_prog, cur_max_prog))
        global_data.emgr.on_task_finished.emit(task_id)

    @rpc_method(CLIENT_STUB, (Dict('changed_data'),))
    def togather_update_task_prog(self, changed_data):
        if not changed_data:
            return
        prog_changes = []
        max_prog_changes = []
        for task_id, data in six.iteritems(changed_data):
            self.update_task_prog_data(task_id, data, prog_changes_out=prog_changes, max_prog_changes_out=max_prog_changes)

        if prog_changes:
            global_data.emgr.task_prog_changed.emit(prog_changes)
        if max_prog_changes:
            global_data.emgr.task_max_prog_changed.emit(max_prog_changes)

    @rpc_method(CLIENT_STUB, (Str('task_id'), Dict('update_dict')))
    def update_task_content(self, task_id, update_dict):
        fresh_type = task_utils.get_task_fresh_type(task_id)
        self._frtype2task_dict[fresh_type].setdefault(task_id, {'prog': 0,'reward_st': ITEM_UNGAIN,'day_prog': 0})
        task_data_dict = self._frtype2task_dict[fresh_type][task_id]
        prev_prog = task_data_dict.get('prog', 0)
        prev_max_prog = task_data_dict.get('max_prog', 0)
        task_data_dict.update(update_dict)
        cur_prog = task_data_dict.get('prog', 0)
        cur_max_prog = task_data_dict.get('max_prog', 0)
        global_data.emgr.update_task_content_event.emit(task_id)
        if prev_prog != cur_prog:
            global_data.emgr.task_prog_changed.emit((TaskAttrChange(task_id, prev_prog, cur_prog),))
        if prev_max_prog != cur_max_prog:
            global_data.emgr.task_max_prog_changed.emit((TaskAttrChange(task_id, prev_max_prog, cur_max_prog),))

    def receive_task_reward(self, task_id, params=None):
        task_id = str(task_id)
        fresh_type = task_utils.get_task_fresh_type(task_id)
        task_data_dict = self._frtype2task_dict[fresh_type].get(task_id, {})
        if task_data_dict.get('reward_st', ITEM_UNGAIN) != ITEM_UNRECEIVED:
            return
        params = params or {} if 1 else params
        self.call_server_method('receive_task_reward', (task_id, False, params))

    def receive_all_task_reward(self, parent_task_id):
        parent_task_id = str(parent_task_id)
        if not self.has_unreceived_task_reward(parent_task_id):
            return
        self.call_server_method('receive_task_reward', (parent_task_id, True, {}))

    def receive_tasks_reward(self, task_id_list):
        self.call_server_method('receive_tasks_reward', (task_id_list,))

    @rpc_method(CLIENT_STUB, (List('task_ids'),))
    def receive_tasks_reward_ret(self, task_ids):
        for task_id in task_ids:
            if isinstance(task_id, list):
                task_id, task_progs = task_id
                self.receive_task_prog_reward_ret_imp(task_id, task_progs)
            else:
                self.receive_task_reward_ret_imp(task_id)

    @rpc_method(CLIENT_STUB, (Str('task_id'), Bool('ret')))
    def receive_task_reward_ret(self, task_id, ret):
        if ret:
            self.receive_task_reward_ret_imp(task_id)

    def receive_task_reward_ret_imp(self, task_id):
        fresh_type = task_utils.get_task_fresh_type(task_id)
        self._frtype2task_dict[fresh_type].setdefault(task_id, {'prog': 0,'reward_st': ITEM_UNGAIN})
        task_data_dict = self._frtype2task_dict[fresh_type][task_id]
        task_data_dict['reward_st'] = ITEM_RECEIVED
        self._call_meta_member_func('_on_receive_@_task_reward', task_id)
        global_data.emgr.receive_task_reward_succ_event.emit(task_id)

    def receive_task_prog_reward(self, task_id, prog):
        fresh_type = task_utils.get_task_fresh_type(task_id)
        task_data_dict = self._frtype2task_dict[fresh_type].get(task_id, {})
        if prog > task_data_dict.get('prog', 0):
            return False
        if prog in task_data_dict.get('prog_rewards', {}):
            return False
        self.call_server_method('receive_task_prog_reward', (task_id, prog))
        return True

    def update_task_extra_info(self, task_id, extra_info):
        fresh_type = task_utils.get_task_fresh_type(task_id)
        self.call_server_method('update_task_extra_info', (task_id, extra_info))

    def receive_all_task_prog_reward(self, task_id):
        self.call_server_method('receive_all_task_prog_reward', (task_id,))
        return True

    @rpc_method(CLIENT_STUB, (Str('task_id'), Int('prog')))
    def receive_task_prog_reward_ret(self, task_id, prog):
        self.receive_task_prog_reward_ret_imp(task_id, (prog,))

    def receive_task_prog_reward_ret_imp(self, task_id, progs):
        fresh_type = task_utils.get_task_fresh_type(task_id)
        task_data_dict = self._frtype2task_dict[fresh_type].setdefault(task_id, {})
        prog_rewards = task_data_dict.setdefault('prog_rewards', {})
        for prog in progs:
            prog_rewards[prog] = ITEM_RECEIVED

        global_data.emgr.receive_task_prog_reward_succ_event.emit(task_id, prog)

    @rpc_method(CLIENT_STUB, (Str('task_id'), Int('reward_rec_time')))
    def refresh_task_reward_rec_time(self, task_id, reward_rec_time):
        fresh_type = task_utils.get_task_fresh_type(task_id)
        task_data_dict = self._frtype2task_dict[fresh_type].setdefault(task_id, {})
        task_data_dict['reward_rec_time'] = reward_rec_time

    @rpc_method(CLIENT_STUB, (Str('task_id'), Dict('prog_rec_time')))
    def refresh_task_prog_rec_time(self, task_id, prog_rec_time):
        fresh_type = task_utils.get_task_fresh_type(task_id)
        task_data_dict = self._frtype2task_dict[fresh_type].setdefault(task_id, {})
        task_data_dict['prog_rec_time'] = prog_rec_time

    @rpc_method(CLIENT_STUB, (Str('refresh_type'), Dict('day_task_data')))
    def reset_task_by_refresh_type(self, refresh_type, day_task_data):
        task_ids = six_ex.keys(self._frtype2task_dict[refresh_type])
        prev_progs = [ self._frtype2task_dict[refresh_type][task_id].get('prog', 0) for task_id in task_ids ]
        prev_max_progs = [ self._frtype2task_dict[refresh_type][task_id].get('max_prog', 0) for task_id in task_ids ]
        self._frtype2task_dict[refresh_type] = day_task_data
        prog_changes = []
        max_prog_changes = []
        for idx, task_id in enumerate(task_ids):
            prev_prog = prev_progs[idx]
            prev_max_prog = prev_max_progs[idx]
            task_data_dict = self._frtype2task_dict[refresh_type].get(task_id, {})
            cur_prog = task_data_dict.get('prog', 0)
            cur_max_prog = task_data_dict.get('max_prog', 0)
            if prev_prog != cur_prog:
                prog_changes.append(TaskAttrChange(task_id, prev_prog, cur_prog))
            if prev_max_prog != cur_max_prog:
                max_prog_changes.append(TaskAttrChange(task_id, prev_max_prog, cur_max_prog))

        if prog_changes:
            global_data.emgr.task_prog_changed.emit(prog_changes)
        if max_prog_changes:
            global_data.emgr.task_max_prog_changed.emit(max_prog_changes)

    @rpc_method(CLIENT_STUB, (Int('cur_season'),))
    def reset_season_task(self, cur_season):
        self._frtype2task_dict[task_const.SEASON_FRESH] = {}

    @rpc_method(CLIENT_STUB, ())
    def clear_all_task_data(self):
        self._frtype2task_dict[task_const.DAYLY_FRESH] = {}
        self._frtype2task_dict[task_const.DAYLY5_FRESH] = {}
        self._frtype2task_dict[task_const.WEEKLY_FRESH] = {}
        self._frtype2task_dict[task_const.WEEKLY5_FRESH] = {}
        self._frtype2task_dict[task_const.SEASON_FRESH] = {}

    @rpc_method(CLIENT_STUB, (Str('task_id'),))
    def clear_task(self, task_id):
        fresh_type = task_utils.get_task_fresh_type(task_id)
        task_data_dict = self._frtype2task_dict[fresh_type]
        task_data_dict.pop(task_id, None)
        return

    @rpc_method(CLIENT_STUB, (List('task_id_list'),))
    def on_task_registed(self, task_id_list):
        pass

    def get_anniv_7day_task_end_time(self):
        return self._anniv_7day_task_end_time

    @rpc_method(CLIENT_STUB, (Int('anniv_7day_end_time'),))
    def update_anniv_7day_task_end_time(self, end_time):
        self._anniv_7day_task_end_time = end_time
        global_data.emgr.anniv_charge_task_finished_event.emit()


class TaskAttrChange(object):

    def __init__(self, task_id, prev_val, cur_val):
        self.task_id = task_id
        self.pre_val = prev_val
        self.cur_val = cur_val