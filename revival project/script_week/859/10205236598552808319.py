# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gutils/loop_lottery_utils.py
from __future__ import absolute_import
from logic.gcommon.cdata import loop_lottery_collection, loop_lottery_turntable
from logic.gcommon.cdata import lottery_collection_template, lottery_single_turntable_template, lottery_double_turntable_template
from logic.gcommon.cdata import loop_lottery_reward_list, loop_lottery_goods_list, loop_lottery_exchange_list
from logic.gcommon import time_utility as tutil
import copy
import six
LOOP_LOTTERY_IDS = ('157', '158', '159', '160')
COLLECTION_LOTTERY_1_ID = '157'
COLLECTION_LOTTERY_2_ID = '158'

def get_loop_lottery_open_info(lottery_id):
    lottery_id = str(lottery_id)
    now = tutil.time()
    goods_open_info = None
    shop_open_info = None
    if lottery_id in loop_lottery_collection.format_data:
        goods_open_info = get_template_id_in_time_range(loop_lottery_collection.format_data.get(lottery_id).get('lottery_open_time', []), now)
        shop_open_info = get_template_id_in_time_range(loop_lottery_collection.format_data.get(lottery_id).get('shop_open_time', []), now)
    elif lottery_id in loop_lottery_turntable.format_data:
        goods_open_info = get_template_id_in_time_range(loop_lottery_turntable.format_data.get(lottery_id).get('lottery_open_time', []))
    return (
     goods_open_info, shop_open_info)


def get_template_id_in_time_range(time_range_list, timestamp=None):
    if not time_range_list:
        return
    else:
        if timestamp is None:
            timestamp = tutil.time()
        for time_range in time_range_list:
            if time_range[1] <= timestamp < time_range[2]:
                return time_range

        return


def get_loop_lottery_template_id(lottery_id, use_shop=False):
    lottery_id = str(lottery_id)
    goods_open_info, shop_open_info = get_loop_lottery_open_info(lottery_id)
    if goods_open_info:
        return goods_open_info[0]
    else:
        if use_shop and shop_open_info:
            return shop_open_info[0]
        return None


def get_loop_lottery_collect_activity_data(lottery_id):
    lottery_id = str(lottery_id)
    template_id = get_loop_lottery_template_id(lottery_id)
    if not template_id:
        return {}
    ui_data = lottery_collection_template.data[template_id].get('activity_data', {}).get('cUiData', {})
    return ui_data


def get_loop_lottery_reward_list(reward_id, lottery_id, template_id):
    template_id = int(template_id)
    lottery_id = str(lottery_id)
    reward_id = int(reward_id)
    reward_ids = list(loop_lottery_reward_list.data.get(lottery_id, {}).get('reward_list'))
    if not reward_ids or reward_id not in reward_ids:
        return []
    reward_idx = reward_ids.index(reward_id)
    if template_id in lottery_collection_template.data:
        reward_list = lottery_collection_template.data[template_id]['rewards_data'][reward_idx][1]
    else:
        reward_list = []
    return reward_list


def get_loop_lottery_lucky_house_info--- This code section failed: ---

  85       0  LOAD_GLOBAL           0  'str'
           3  LOAD_FAST             0  'lottery_id'
           6  CALL_FUNCTION_1       1 
           9  STORE_FAST            0  'lottery_id'

  86      12  LOAD_GLOBAL           1  'get_loop_lottery_template_id'
          15  LOAD_GLOBAL           1  'get_loop_lottery_template_id'
          18  LOAD_GLOBAL           2  'True'
          21  CALL_FUNCTION_257   257 
          24  STORE_FAST            2  'template_id'

  87      27  LOAD_FAST             2  'template_id'
          30  POP_JUMP_IF_TRUE     37  'to 37'

  88      33  BUILD_MAP_0           0 
          36  RETURN_END_IF    
        37_0  COME_FROM                '30'

  90      37  LOAD_FAST             2  'template_id'
          40  LOAD_GLOBAL           3  'lottery_collection_template'
          43  LOAD_ATTR             4  'data'
          46  COMPARE_OP            6  'in'
          49  POP_JUMP_IF_FALSE    82  'to 82'

  91      52  LOAD_GLOBAL           3  'lottery_collection_template'
          55  LOAD_ATTR             4  'data'
          58  LOAD_ATTR             5  'get'
          61  LOAD_FAST             2  'template_id'
          64  CALL_FUNCTION_1       1 
          67  LOAD_ATTR             5  'get'
          70  LOAD_CONST            2  'lottery_data'
          73  CALL_FUNCTION_1       1 
          76  STORE_FAST            3  'info'
          79  JUMP_FORWARD         96  'to 178'

  92      82  LOAD_FAST             2  'template_id'
          85  LOAD_GLOBAL           6  'lottery_single_turntable_template'
          88  LOAD_ATTR             4  'data'
          91  COMPARE_OP            6  'in'
          94  POP_JUMP_IF_FALSE   127  'to 127'

  93      97  LOAD_GLOBAL           6  'lottery_single_turntable_template'
         100  LOAD_ATTR             4  'data'
         103  LOAD_ATTR             5  'get'
         106  LOAD_FAST             2  'template_id'
         109  CALL_FUNCTION_1       1 
         112  LOAD_ATTR             5  'get'
         115  LOAD_CONST            2  'lottery_data'
         118  CALL_FUNCTION_1       1 
         121  STORE_FAST            3  'info'
         124  JUMP_FORWARD         51  'to 178'

  94     127  LOAD_FAST             2  'template_id'
         130  LOAD_GLOBAL           7  'lottery_double_turntable_template'
         133  LOAD_ATTR             4  'data'
         136  COMPARE_OP            6  'in'
         139  POP_JUMP_IF_FALSE   172  'to 172'

  95     142  LOAD_GLOBAL           7  'lottery_double_turntable_template'
         145  LOAD_ATTR             4  'data'
         148  LOAD_ATTR             5  'get'
         151  LOAD_FAST             2  'template_id'
         154  CALL_FUNCTION_1       1 
         157  LOAD_ATTR             5  'get'
         160  LOAD_CONST            2  'lottery_data'
         163  CALL_FUNCTION_1       1 
         166  STORE_FAST            3  'info'
         169  JUMP_FORWARD          6  'to 178'

  97     172  BUILD_MAP_0           0 
         175  STORE_FAST            3  'info'
       178_0  COME_FROM                '169'
       178_1  COME_FROM                '124'
       178_2  COME_FROM                '79'

  99     178  LOAD_FAST             1  'key_list'
         181  POP_JUMP_IF_TRUE    197  'to 197'

 100     184  LOAD_GLOBAL           8  'copy'
         187  LOAD_ATTR             9  'deepcopy'
         190  LOAD_FAST             3  'info'
         193  CALL_FUNCTION_1       1 
         196  RETURN_END_IF    
       197_0  COME_FROM                '181'

 102     197  BUILD_MAP_0           0 
         200  STORE_FAST            4  'simple_info'

 103     203  SETUP_LOOP           28  'to 234'
         206  LOAD_FAST             1  'key_list'
         209  GET_ITER         
         210  FOR_ITER             20  'to 233'
         213  STORE_FAST            5  'k'

 104     216  LOAD_FAST             3  'info'
         219  LOAD_FAST             5  'k'
         222  BINARY_SUBSCR    
         223  LOAD_FAST             4  'simple_info'
         226  LOAD_FAST             5  'k'
         229  STORE_SUBSCR     
         230  JUMP_BACK           210  'to 210'
         233  POP_BLOCK        
       234_0  COME_FROM                '203'

 105     234  LOAD_FAST             4  'simple_info'
         237  RETURN_VALUE     
          -1  RETURN_LAST      

Parse error at or near `CALL_FUNCTION_257' instruction at offset 21


def fill_loop_lottery_info(origin_info, lottery_id):
    loop_info = get_loop_lottery_lucky_house_info(lottery_id)
    origin_info.update(loop_info)


def is_loop_lottery(lottery_id):
    return str(lottery_id) in LOOP_LOTTERY_IDS


def get_loop_lottery_exchange_goods_list(lottery_id, template_id):
    template_id = int(template_id)
    lottery_id = str(lottery_id)
    exchange_list = []
    if template_id in lottery_collection_template.data:
        goods_info_list = lottery_collection_template.data[template_id]['goods_data']
        goods_list = loop_lottery_goods_list.data[lottery_id]['goods_list']
        for idx, goods_info in enumerate(goods_info_list):
            if not goods_info.get('goods_no') or not goods_info.get('item_consumed'):
                continue
            exchange_list.append(str(goods_list[idx]))

        fix_exchange_list = loop_lottery_exchange_list.data[lottery_id]['fix_exchange_list']
        for goods_id in fix_exchange_list:
            if str(goods_id) not in exchange_list:
                exchange_list.append(str(goods_id))

    elif template_id in lottery_double_turntable_template.data:
        fix_exchange_list = loop_lottery_exchange_list.data[lottery_id]['fix_exchange_list']
        for goods_id in fix_exchange_list:
            if str(goods_id) not in exchange_list:
                exchange_list.append(str(goods_id))

    return exchange_list


def is_loop_lottery_goods(goods_id):
    goods_id = int(goods_id)
    for goods_info in six.itervalues(loop_lottery_goods_list.data):
        if goods_id in goods_info.get('goods_list', []):
            return True

    return False


def get_loop_lottery_goods_info_by_key(goods_id, lottery_id, template_id=None, key=None):
    if not template_id:
        template_id = get_loop_lottery_template_id(lottery_id, use_shop=True)
    if not template_id:
        return None
    else:
        lottery_id = str(lottery_id)
        template_id = int(template_id)
        goods_id = int(goods_id)
        goods_list = list(loop_lottery_goods_list.data.get(lottery_id, {}).get('goods_list', []))
        if not goods_list or goods_id not in goods_list:
            return None
        goods_idx = goods_list.index(goods_id)
        if template_id in lottery_collection_template.data:
            goods_info = lottery_collection_template.data[template_id]['goods_data'][goods_idx]
        elif template_id in lottery_single_turntable_template.data:
            goods_info = lottery_single_turntable_template.data[template_id]['goods_data'][goods_idx]
        elif template_id in lottery_double_turntable_template.data:
            goods_info = lottery_double_turntable_template.data[template_id]['goods_data'][goods_idx]
        else:
            goods_info = {}
        if not key:
            return copy.deepcopy(goods_info)
        if isinstance(key, (list, tuple)):
            new_goods_info = {}
            for k in key:
                new_goods_info[k] = goods_info[k]

            return new_goods_info
        return goods_info.get(key)
        return None


def is_loop_collection_lottery(lottery_id):
    return str(lottery_id) in (COLLECTION_LOTTERY_1_ID, COLLECTION_LOTTERY_2_ID)


def is_loop_lottery_open(lottery_id):
    goods_open_info, shop_open_info = get_loop_lottery_open_info(lottery_id)
    if not goods_open_info and not shop_open_info:
        return False
    return True


def is_loop_lottery_activity_open(lottery_id):
    goods_open_info, shop_open_info = get_loop_lottery_open_info(lottery_id)
    if goods_open_info:
        return True
    else:
        return False


def is_loop_lottery_activity_closed_for_ui(activity_id):
    from common.cfg import confmgr
    ui_data = confmgr.get('c_activity_config', str(activity_id), 'cUiData', default={})
    loop_lottery_id = ui_data.get('loop_lottery_id')
    if not loop_lottery_id:
        return False
    goods_open_info, shop_open_info = get_loop_lottery_open_info(loop_lottery_id)
    if not goods_open_info:
        return True
    left_time = goods_open_info[2] - tutil.time()
    if left_time < 0.15:
        return True
    return False