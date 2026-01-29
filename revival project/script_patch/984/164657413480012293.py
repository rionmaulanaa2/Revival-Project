# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/avatarmembers/impRandomTask.py
from __future__ import absolute_import
from mobile.common.rpcdecorator import rpc_method, CLIENT_STUB
from mobile.common.RpcMethodArgs import Str, Int, Bool, List, Dict

class impRandomTask(object):

    def _init_randomtask_from_dict(self, bdict):
        self._random_children_tasks = bdict.get('random_children_tasks', {})
        self._task_random_cnt_data = bdict.get('task_random_cnt_data', {})

    @rpc_method(CLIENT_STUB, (Dict('tasks_data'),))
    def refresh_random_tasks(self, tasks_data):
        self._random_children_tasks = tasks_data

    def get_random_children_tasks(self, task_refresh_type, parent_task_id):
        return self._random_children_tasks.get(task_refresh_type, {}).get(parent_task_id)

    @rpc_method(CLIENT_STUB, (Str('task_id'), Int('reward_cnt')))
    def update_random_cnt_data(self, task_id, reward_cnt):
        self._task_random_cnt_data[task_id] = reward_cnt
        global_data.emgr.refresh_random_task.emit()

    def get_random_task_reward_cnt(self, task_id):
        return self._task_random_cnt_data.get(task_id, 0)