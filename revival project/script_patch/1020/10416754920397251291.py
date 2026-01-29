# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gutils/new_sys_prompt_utils.py
from __future__ import absolute_import

def in_promotion_time_range(sys_type):
    if sys_type is None:
        return False
    else:
        from logic.gcommon.common_const import new_system_prompt_data as sp_const
        begin_ts = sp_const.cfg_data.get(sys_type, {}).get('promotion_begin_ts', None)
        end_ts = sp_const.cfg_data.get(sys_type, {}).get('promotion_end_ts', None)
        has_valid_time_range = isinstance(begin_ts, int) and isinstance(end_ts, int) and begin_ts <= end_ts
        if not has_valid_time_range:
            return True
        from logic.gcommon import time_utility as tutil
        cur_time = tutil.time()
        return cur_time >= begin_ts and cur_time <= end_ts


def is_sys_blocked(sys_type):
    from logic.gcommon.common_const import new_system_prompt_data as sp_const
    return bool(sp_const.cfg_data.get(sys_type, {}).get('skipped', 0))


def get_sys_prompt_level(sys_type):
    from logic.gcommon.common_const import new_system_prompt_data as sp_const
    lv = sp_const.cfg_data.get(sys_type, {}).get('prompt_lv', None)
    return (
     lv is not None, lv)