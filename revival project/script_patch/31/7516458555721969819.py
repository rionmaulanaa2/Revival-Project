# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/cdata/limited_time_free_mecha_data.py
_reload_all = True
if G_IS_NA_PROJECT:
    from .na_limited_time_free_mecha_data import *
else:
    WEEK_FREE_MECHA_DATA = (101008010, 101008016, 101008023, 101008019, 101008025,
                            101008018, 101008020, 101008021, 101008024, 101008012,
                            101008017, 101008009, 101008026, 101008013, 101008007,
                            101008014, 101008022, 101008008, 101008011, 101008003,
                            101008025, 101008015, 101008007, 101008023, 101008013,
                            101008012, 101008015, 101008021, 101008018, 101008024,
                            101008016, 101008026, 101008017, 101008003, 101008020,
                            101008022, 101008010, 101008008, 101008011, 101008014,
                            101008009, 101008019, 101008003, 101008016, 101008025,
                            101008018, 101008008, 101008021, 101008012, 101008023,
                            101008011, 101008024, 101008026, 101008009, 101008007,
                            101008020, 101008017, 101008015, 101008010, 101008022,
                            101008014, 101008013, 101008019)
    FRAME_FREE_MECHA_DATA = {2: {'start_ts': 1643558400,
           'end_ts': 1644508800,
           'mechas': (101008001, 101008002, 101008003, 101008004, 101008005, 101008006, 101008007, 101008008,
 101008009, 101008010, 101008011, 101008012, 101008013, 101008014, 101008015, 101008016,
 101008017, 101008018, 101008019, 101008020, 101008021),
           'tips_id': 601098
           },
       3: {'start_ts': 1674230400,
           'end_ts': 1674835200,
           'mechas': (101008001, 101008002, 101008003, 101008004, 101008005, 101008006, 101008007, 101008008,
 101008009, 101008010, 101008011, 101008012, 101008013, 101008014, 101008015, 101008016,
 101008017, 101008018, 101008019, 101008020, 101008021, 101008022, 101008023, 101008024,
 101008025, 101008026, 101008027, 101008028),
           'tips_id': 601098
           },
       4: {'start_ts': 1707321600,
           'end_ts': 1707926400,
           'mechas': (101008001, 101008002, 101008003, 101008004, 101008005, 101008006, 101008007, 101008008,
 101008009, 101008010, 101008011, 101008012, 101008013, 101008014, 101008015, 101008016,
 101008017, 101008018, 101008019, 101008020, 101008021, 101008022, 101008023, 101008024,
 101008025, 101008026, 101008027, 101008028, 101008029, 101008030, 101008031, 101008032,
 101008033, 101008034, 101008035),
           'tips_id': 601098
           }
       }
import six
from logic.gcommon import time_utility as tutil
LIMITED_DAY_REFRESH_TYPE = tutil.CYCLE_DATA_REFRESH_TYPE_2
LIMITED_TIME_FREE_MECHA_DATA = (-1, None)
SP_FRAME_ID_WEEKLY_PLACEHOLDER = -1

def get_limited_time_free_mecha_dict():
    global LIMITED_TIME_FREE_MECHA_DATA
    now = tutil.time()
    refresh_type = LIMITED_DAY_REFRESH_TYPE
    day_no = tutil.get_rela_day_no(now, refresh_type)
    if LIMITED_TIME_FREE_MECHA_DATA[0] != day_no:
        free_dict = {}
        week_ts = tutil.get_week_start_timestamp(now)
        refresh_time = tutil.CYCLE_DATA_REFRESH_TIME[refresh_type]
        last_week_start_ts = week_ts
        last_week_end_ts = week_ts + refresh_time
        this_week_start_ts = week_ts + 4 * tutil.ONE_DAY_SECONDS + refresh_time
        this_week_end_ts = week_ts + tutil.ONE_WEEK_SECONDS
        this_week_real_end_ts = week_ts + tutil.ONE_WEEK_SECONDS + refresh_time
        weekly_week_no = tutil.get_rela_week_no(now, refresh_type)
        weekly_end_ts = None
        if last_week_start_ts <= now <= last_week_end_ts:
            weekly_end_ts = last_week_end_ts
        elif this_week_start_ts <= now <= this_week_end_ts:
            weekly_end_ts = this_week_real_end_ts
        if weekly_end_ts is not None:
            week_idx = weekly_week_no % len(WEEK_FREE_MECHA_DATA)
            mecha_item_id = WEEK_FREE_MECHA_DATA[week_idx]
            free_dict[mecha_item_id] = (
             weekly_end_ts, SP_FRAME_ID_WEEKLY_PLACEHOLDER)
        for _id, conf in six.iteritems(FRAME_FREE_MECHA_DATA):
            start_ts = conf.get('start_ts', 0)
            end_ts = conf.get('end_ts', 0)
            mecha_item_ids = conf.get('mechas', tuple())
            start_ts += refresh_time
            end_ts += refresh_time
            if start_ts <= now <= end_ts:
                for mecha_item_id in mecha_item_ids:
                    furthest_end_ts = end_ts
                    data = free_dict.get(mecha_item_id, None)
                    if data:
                        another_end_ts = data[0]
                        furthest_end_ts = max(furthest_end_ts, another_end_ts)
                    free_dict[mecha_item_id] = (
                     furthest_end_ts, _id)

        LIMITED_TIME_FREE_MECHA_DATA = (
         day_no, free_dict)
    else:
        free_dict = LIMITED_TIME_FREE_MECHA_DATA[1]
    return free_dict


def is_sp_frame(sp_frame_id):
    return sp_frame_id != SP_FRAME_ID_WEEKLY_PLACEHOLDER and sp_frame_id in FRAME_FREE_MECHA_DATA


def get_sp_frame_tips_id(sp_frame_id):
    if SP_FRAME_ID_WEEKLY_PLACEHOLDER == sp_frame_id:
        return 601095
    return FRAME_FREE_MECHA_DATA.get(sp_frame_id, {}).get('tips_id', 0)


def get_sp_frame_end_ts(sp_frame_id):
    zero_time = FRAME_FREE_MECHA_DATA.get(sp_frame_id, {}).get('end_ts', 0)
    refresh_time = tutil.CYCLE_DATA_REFRESH_TIME[LIMITED_DAY_REFRESH_TYPE]
    return zero_time + refresh_time


def is_mecha_limited_free_now(mecha_lobby_id):
    free_dict = get_limited_time_free_mecha_dict()
    if mecha_lobby_id not in free_dict:
        return False
    end_ts, _ = free_dict[mecha_lobby_id]
    now = tutil.time()
    return now < end_ts


def is_mecha_limited_free_now_by_mecha_id(mecha_id):
    try:
        from logic.gutils.dress_utils import battle_id_to_mecha_lobby_id as bml
    except:
        from data.mecha_conf import battle_mecha_2_lobby_mecha as bml

    mecha_lobby_id = bml(mecha_id)
    if mecha_lobby_id:
        return is_mecha_limited_free_now(mecha_lobby_id)
    else:
        return False