# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/avatarmembers/impCorpTask.py
from __future__ import absolute_import
from common.cfg import confmgr
from mobile.common.rpcdecorator import rpc_method, CLIENT_STUB
from mobile.common.RpcMethodArgs import Int, List, Str, Dict
from logic.gcommon.item import item_const
from logic.gcommon import time_utility as tutil
from logic.gcommon.common_const import task_const
from common.utils.timer import CLOCK

class impCorpTask(object):

    def _init_corptask_from_dict(self, bdict):
        self._corp_task_ids = bdict.get('corp_task_ids', [])
        self._free_chg_times = bdict.get('free_chg_times', 0)
        self._vacancy_seq = bdict.get('vacancy_seq', [])
        self._new_corp_task_ids = bdict.get('new_corp_task_ids', [])

    def get_free_chg_times(self):
        return self._free_chg_times

    def get_corp_task_ids(self):
        return self._corp_task_ids

    def get_vacancy_seq(self):
        return self._vacancy_seq

    @rpc_method(CLIENT_STUB, (Int('change_type'), Str('old_task_id'), Str('new_task_id'), Int('corp_lv'), Int('reward_id'), Dict('extra_data')))
    def on_corp_task_changed(self, change_type, old_task_id, new_task_id, corp_lv, reward_id, extra_data):
        if not old_task_id:
            self._corp_task_ids.append(new_task_id)
        else:
            idx = self._corp_task_ids.index(old_task_id)
            if idx >= 0:
                self._corp_task_ids[idx] = new_task_id
        task_dict = {'corp_lv': corp_lv,'reward_id': reward_id
           }
        if 'custom_total_prog' in extra_data:
            task_dict['custom_total_prog'] = extra_data['custom_total_prog']
        self.update_task_content((new_task_id, task_dict))
        if change_type == task_const.FREE_CHANGE_CORP:
            self._free_chg_times = 0
        elif change_type == task_const.AUTO_CHANGE_CORP and self._vacancy_seq:
            self._new_corp_task_ids.append(new_task_id)
            self._vacancy_seq.pop(0)
        global_data.emgr.corp_task_changed_event.emit(old_task_id, new_task_id)

    def change_corp_task(self, change_type, old_task_id):
        if old_task_id is None:
            old_task_id = ''
        self.call_server_method('change_corp_task', (change_type, old_task_id))
        return

    @rpc_method(CLIENT_STUB, ())
    def reset_free_chg_times(self):
        self._free_chg_times = 1

    def is_corp_task_full(self):
        if len(self._corp_task_ids) < task_const.CORP_TASK_MAX_NUM:
            return False
        for task_id in self._corp_task_ids:
            if self.has_receive_reward(task_id):
                return False

        return True

    def get_corp_task_num(self):
        count = 0
        for task_id in self._corp_task_ids:
            if not self.has_receive_reward(task_id):
                count += 1

        return count

    def _on_receive_corptask_task_reward(self, task_id):
        if task_id in self._corp_task_ids:
            self._vacancy_seq.append(self._corp_task_ids.index(task_id))

    def get_new_corp_task_ids(self):
        return self._new_corp_task_ids

    @rpc_method(CLIENT_STUB, (List('vacancy_seq'),))
    def on_vacancy_changed(self, vacancy_seq):
        self._vacancy_seq = vacancy_seq

    def read_new_corp_task(self):
        self._new_corp_task_ids = []
        self.call_server_method('read_new_corp_task', ())