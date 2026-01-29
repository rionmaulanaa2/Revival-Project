# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/avatarmembers/impWeekTask.py
from __future__ import absolute_import
import six
from common.cfg import confmgr
from mobile.common.rpcdecorator import rpc_method, CLIENT_STUB
from mobile.common.RpcMethodArgs import Str, Int, Bool, List, Dict

class impWeekTask(object):

    def _init_weektask_from_dict(self, bdict):
        self.week_no = bdict.get('week_no', 1)
        self.is_week_task_closed = bdict.get('is_week_task_closed', False)

    def get_week_task_ids(self, week_no):
        task_data = confmgr.get('task/week_task_data', default={})
        ids = []
        for task_id, task_conf in six.iteritems(task_data):
            if task_conf['week'] == week_no:
                ids.append(task_id)

        return ids

    def get_cur_task_week_no(self):
        return self.week_no

    def has_week_task_closed(self):
        return self.is_week_task_closed

    @rpc_method(CLIENT_STUB, (Int('week_no'),))
    def reset_week_task_content(self, week_no):
        self.week_no = week_no
        global_data.emgr.reset_week_task_content_event.emit()

    @rpc_method(CLIENT_STUB, ())
    def on_week_task_closed(self):
        self.is_week_task_closed = True