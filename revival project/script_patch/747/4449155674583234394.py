# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/avatarmembers/impDayTask.py
from __future__ import absolute_import
import six
from common.cfg import confmgr
from mobile.common.rpcdecorator import rpc_method, CLIENT_STUB
from mobile.common.RpcMethodArgs import Int, Bool, Str, List
from logic.gcommon.item import item_const
from logic.gutils import task_utils
from logic.gcommon.common_const.task_const import FIX_TASK

class impDayTask(object):

    def _init_daytask_from_dict(self, bdict):
        all_day_task_ids = confmgr.get('task/day_task_data', default={})
        day_task_ids = []
        for task_id, task_conf in six.iteritems(all_day_task_ids):
            if task_utils.check_task_server_limit(task_id) and not task_conf.get('need_hide', False) and task_conf.get('is_stable', False) == FIX_TASK:
                day_task_ids.append(task_id)

        self.day_task_ids = day_task_ids
        self.random_day_task_ids = bdict.get('random_day_task_ids', [])
        self.changed_day_tasks = set(bdict.get('changed_day_tasks', []))

    def get_day_task_ids(self):
        return self.day_task_ids

    def get_random_day_task_ids(self):
        return self.random_day_task_ids

    def get_changed_day_tasks(self):
        return self.changed_day_tasks

    def change_random_day_task(self, task_id):
        if task_id not in self.random_day_task_ids:
            return
        if task_id in self.changed_day_tasks:
            return
        self.call_server_method('change_random_day_task', (task_id,))

    @rpc_method(CLIENT_STUB, (Str('old_task'), Str('new_task')))
    def change_random_day_task_succ(self, old_task, new_task):
        self.changed_day_tasks.add(old_task)
        self.changed_day_tasks.add(new_task)
        if old_task in self.random_day_task_ids:
            pos = self.random_day_task_ids.index(old_task)
            self.random_day_task_ids[pos] = new_task
        else:
            self.random_day_task_ids.append(new_task)
        global_data.emgr.refresh_day_random_task.emit()

    @rpc_method(CLIENT_STUB, (List('random_task_ids'),))
    def refresh_day_random_task(self, random_task_ids):
        self.random_day_task_ids = random_task_ids
        self.changed_day_tasks = set()