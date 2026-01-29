# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/avatarmembers/impSeasonTask.py
from __future__ import absolute_import
import six
from common.cfg import confmgr
from mobile.common.rpcdecorator import rpc_method, CLIENT_STUB
from mobile.common.RpcMethodArgs import Str, Int, Bool, List, Dict
from logic.gutils import task_utils

class impSeasonTask(object):

    def _init_seasontask_from_dict(self, bdict):
        self._total_season_week = 0
        self._season_task_ids_dict = {}
        self._season_bt_task_ids_dict = {}
        self._season_bt_parent_task = {}
        task_data = confmgr.get('task/season_task_data', default={})
        for task_id, season_task_conf in six.iteritems(task_data):
            season = season_task_conf['season']
            week = season_task_conf['season_week']
            if week == 0:
                if task_utils.get_children_task(task_id):
                    self._season_bt_parent_task[season] = task_id
                else:
                    self._season_bt_task_ids_dict.setdefault(season, [])
                    self._season_bt_task_ids_dict[season].append(task_id)
            else:
                self._season_task_ids_dict.setdefault(season, {})
                self._season_task_ids_dict[season].setdefault(week, [])
                self._season_task_ids_dict[season][week].append(task_id)

    def get_season_task_ids(self, season_week_no):
        season = self.get_battle_season()
        return self._season_task_ids_dict.get(season, {}).get(season_week_no, [])

    def get_season_bt_parent_task(self):
        season = self.get_battle_season()
        return self._season_bt_parent_task.get(season, None)

    def get_season_task_week_num(self):
        season = self.get_battle_season()
        return len(self._season_task_ids_dict.get(season, {}))

    def get_season_battle_time_task_ids(self):
        season = self.get_battle_season()
        return self._season_bt_task_ids_dict.get(season, [])