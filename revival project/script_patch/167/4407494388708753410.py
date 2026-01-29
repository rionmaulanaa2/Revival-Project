# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/avatarmembers/impAssessTask.py
from __future__ import absolute_import
import six
import six_ex
from six.moves import range
from common.cfg import confmgr
from logic.gutils.task_utils import get_assess_unlock_vitality

class impAssessTask(object):

    def _init_assesstask_from_dict(self, bdict):
        self._unlock_lvs = None
        self._assess_task_ids_dict = None
        return

    def get_assess_task_ids(self, unlock_level):
        if self._assess_task_ids_dict is None:
            self._assess_task_ids_dict = {}
            task_data = confmgr.get('task/assess_task_data', 'TaskData', default={})
            for task_id, task_conf in six.iteritems(task_data):
                lv = task_conf['unlock_level']
                self._assess_task_ids_dict.setdefault(lv, [])
                self._assess_task_ids_dict[lv].append(task_id)

        return self._assess_task_ids_dict.get(unlock_level, [])

    def get_assess_unlock_levels(self):
        if self._unlock_lvs is None:
            assess_task_conf = confmgr.get('task/assess_task_data', 'AssessLevelConf')
            unlock_lvs = six_ex.keys(assess_task_conf)
            unlock_lvs.sort()
            self._unlock_lvs = [ int(x) for x in unlock_lvs ]
        return self._unlock_lvs

    def try_unlock_assess_task(self, old_vitality, new_vitality):
        levels = self.get_assess_unlock_levels()
        for lv in range(1, len(levels) + 1):
            unlock_vitality = get_assess_unlock_vitality(lv)
            if unlock_vitality > new_vitality:
                break
            if old_vitality < unlock_vitality <= new_vitality:
                global_data.emgr.unlock_assess_task_event.emit(lv)