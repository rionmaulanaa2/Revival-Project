# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gutils/activity_check_handler.py
from __future__ import absolute_import
from logic.gutils import task_utils
from logic.gcommon import time_utility as tutil

def anniv_lucky_store_check_handler():
    discount_info = global_data.player.get_us_anniversary_discount_info()
    if discount_info:
        return True
    return False


def anniv_daily_gift_check_handler(*args):
    if not task_utils.is_task_open('1411068'):
        if not global_data.player.is_task_finished('1411068'):
            return False
        else:
            now = tutil.get_server_time()
            anniv_end_time = global_data.player.get_anniv_7day_task_end_time()
            if now > anniv_end_time:
                return False
            return True

    else:
        return True


def AliPay_HK_check_handler(*args):
    import game3d
    if game3d.get_platform() != game3d.PLATFORM_ANDROID:
        return False
    if global_data.player.get_login_country() != 'HK':
        return False
    if not global_data.channel.is_south_east_asia_server():
        return False
    return True


def bilibili_sdk_specific_version_check_handler(*args):
    try:
        channel_name = global_data.channel.get_name()
        if channel_name != 'bilibili_sdk':
            return True
        if global_data.feature_mgr.is_bilibili_sdk_specific_version(channel_name):
            return False
        return True
    except:
        log_error('bilibili_sdk_specific_version_check_handler error')
        return False


def weekend_welfare_check_handler(*args):
    from logic.gcommon.time_utility import get_utc8_weekday, get_server_time, get_utc8_hour
    BASE_TIME = tutil.BASE_TIME
    REFRESH_TYPE = tutil.CYCLE_DATA_REFRESH_TYPE_2
    WEEKEND_DAY_NO_SET = {6, 7}

    def _is_create_at_this_weekend():
        create_time = global_data.player.get_create_time()
        week_start_ts = tutil.get_week_start_time(tutil.get_server_time(), REFRESH_TYPE, BASE_TIME)
        if create_time > week_start_ts:
            create_day_no = tutil.get_rela_day_no(create_time, REFRESH_TYPE, week_start_ts)
            return create_day_no in WEEKEND_DAY_NO_SET
        return False

    cur_time = get_server_time()
    weekday = get_utc8_weekday(cur_time)
    if weekday not in (6, 7, 1):
        return False
    if weekday == 6:
        hour = get_utc8_hour(cur_time)
        if hour < 5:
            return False
    else:
        if weekday == 1:
            hour = get_utc8_hour(cur_time)
            if hour >= 5:
                return False
        if not global_data.player:
            return False
        if _is_create_at_this_weekend():
            return False
    return True


def can_open_friend_recruit_activity(*args):
    if global_data.player.is_enlist_reward_all_received():
        return False
    else:
        return True


def loop_activity_open_checker--- This code section failed: ---

 100       0  LOAD_CONST            1  ''
           3  LOAD_CONST            2  ('confmgr',)
           6  IMPORT_NAME           0  'common.cfg'
           9  IMPORT_FROM           1  'confmgr'
          12  STORE_FAST            1  'confmgr'
          15  POP_TOP          

 101      16  LOAD_CONST            1  ''
          19  LOAD_CONST            3  ('loop_lottery_utils',)
          22  IMPORT_NAME           2  'logic.gutils'
          25  IMPORT_FROM           3  'loop_lottery_utils'
          28  STORE_FAST            2  'loop_lottery_utils'
          31  POP_TOP          

 102      32  LOAD_FAST             1  'confmgr'
          35  LOAD_ATTR             4  'get'
          38  LOAD_CONST            4  'c_activity_config'
          41  LOAD_CONST            5  'cUiData'
          44  LOAD_CONST            6  'default'
          47  BUILD_MAP_0           0 
          50  CALL_FUNCTION_259   259 
          53  STORE_FAST            3  'ui_data'

 103      56  LOAD_FAST             3  'ui_data'
          59  LOAD_ATTR             4  'get'
          62  LOAD_CONST            7  'loop_lottery_id'
          65  CALL_FUNCTION_1       1 
          68  STORE_FAST            4  'loop_lottery_id'

 104      71  LOAD_FAST             4  'loop_lottery_id'
          74  POP_JUMP_IF_TRUE     81  'to 81'

 105      77  LOAD_GLOBAL           5  'False'
          80  RETURN_END_IF    
        81_0  COME_FROM                '74'

 106      81  LOAD_FAST             2  'loop_lottery_utils'
          84  LOAD_ATTR             6  'get_loop_lottery_open_info'
          87  LOAD_FAST             4  'loop_lottery_id'
          90  CALL_FUNCTION_1       1 
          93  UNPACK_SEQUENCE_2     2 
          96  STORE_FAST            5  'goods_open_info'
          99  STORE_FAST            6  'shop_open_info'

 107     102  LOAD_FAST             5  'goods_open_info'
         105  POP_JUMP_IF_TRUE    112  'to 112'

 108     108  LOAD_GLOBAL           5  'False'
         111  RETURN_END_IF    
       112_0  COME_FROM                '105'

 110     112  LOAD_FAST             5  'goods_open_info'
         115  LOAD_CONST            8  2
         118  BINARY_SUBSCR    
         119  LOAD_GLOBAL           7  'tutil'
         122  LOAD_ATTR             8  'time'
         125  CALL_FUNCTION_0       0 
         128  BINARY_SUBTRACT  
         129  STORE_FAST            7  'left_time'

 111     132  LOAD_FAST             7  'left_time'
         135  LOAD_CONST            9  0.15
         138  COMPARE_OP            0  '<'
         141  POP_JUMP_IF_FALSE   148  'to 148'

 112     144  LOAD_GLOBAL           5  'False'
         147  RETURN_END_IF    
       148_0  COME_FROM                '141'

 114     148  LOAD_GLOBAL           9  'True'
         151  RETURN_VALUE     
          -1  RETURN_LAST      

Parse error at or near `CALL_FUNCTION_259' instruction at offset 50