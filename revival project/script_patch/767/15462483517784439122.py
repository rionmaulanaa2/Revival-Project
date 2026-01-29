# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/common_const/rank_pve_activity_const.py
_reload_all = True
from logic.gcommon.common_const import statistics_const as sconst
from logic.gcommon.time_utility import time, ONE_WEEK_SECONDS
data = {'pve_act_20240425': {'time_data': {'end_time': 1716739140,'settle_delay': 30,'reward_delay': 60,'pull_interval': 300},'task_id': 1452008,
                        'reward_data': (
                                      [
                                       1, 12303066], [2, 12303067], [3, 12303068], [4, 12303069], [5, 12303070], [6, 12303071], [7, 12303072], [8, 12303073], [9, 12303074]),
                        'report_cond': lambda avatar: avatar.get_task_progress(1452008) > 0,
                        'grade_percent': (
                                        [
                                         1, 0.01], [2, 0.05], [3, 0.1], [4, 0.2], [5, 0.3], [6, 0.4], [7, 0.5], [8, 0.6], [9, 0.8])
                        }
   }

def get_pve_activity_data_by_rank_type(rank_type):
    return data.get(rank_type)