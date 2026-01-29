# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/cdata/meow_capacity_config.py
_reload_all = True
data = {1: {'lv': 1,
       'mail_box_price': 0,
       'mail_box_size': 8,
       'bag_price': 0,
       'bag_size': 60,
       'safe_box_price': 0,
       'safe_box_size': 8
       },
   2: {'lv': 2,
       'mail_box_price': 500,
       'mail_box_size': 9,
       'bag_price': 1000,
       'bag_size': 70,
       'safe_box_price': 500,
       'safe_box_size': 10
       },
   3: {'lv': 3,
       'mail_box_price': 1000,
       'mail_box_size': 10,
       'bag_price': 1200,
       'bag_size': 80,
       'safe_box_price': 1000,
       'safe_box_size': 12
       },
   4: {'lv': 4,
       'mail_box_price': 0,
       'mail_box_size': 0,
       'bag_price': 1500,
       'bag_size': 90,
       'safe_box_price': 0,
       'safe_box_size': 0
       },
   5: {'lv': 5,
       'mail_box_price': 0,
       'mail_box_size': 0,
       'bag_price': 2000,
       'bag_size': 100,
       'safe_box_price': 0,
       'safe_box_size': 0
       }
   }
import six
capacity_lv_data = {}
capacity_max_lvs = {}
capacity_type_bag = 'bag'
capacity_type_mail_box = 'mail_box'
capacity_type_safe_box = 'safe_box'
capacity_type_set = {capacity_type_bag, capacity_type_mail_box, capacity_type_safe_box}
capacity_init_lv = 1
meow_coin_drop_factor = 0.5
battle_carry_all_max_rank = 5
meow_mail_max_times = 3
meow_coin_one_battle_carry_max_num = 140

def __init_data():
    global capacity_max_lvs
    global capacity_lv_data
    for lv, lv_conf in six.iteritems(data):
        if lv_conf.get('bag_size', 0) > 0 and lv_conf.get('bag_price', 0) >= 0:
            capacity_lv_data.setdefault(capacity_type_bag, {})
            capacity_lv_data[capacity_type_bag][lv] = {'size': lv_conf['bag_size'],'price': lv_conf['bag_price']}
            if lv > capacity_max_lvs.get(capacity_type_bag, 0):
                capacity_max_lvs[capacity_type_bag] = lv
        if lv_conf.get('mail_box_size', 0) > 0 and lv_conf.get('mail_box_price', 0) >= 0:
            capacity_lv_data.setdefault(capacity_type_mail_box, {})
            capacity_lv_data[capacity_type_mail_box][lv] = {'size': lv_conf['mail_box_size'],'price': lv_conf['mail_box_price']}
            if lv > capacity_max_lvs.get(capacity_type_mail_box, 0):
                capacity_max_lvs[capacity_type_mail_box] = lv
        if lv_conf.get('safe_box_size', 0) > 0 and lv_conf.get('safe_box_price', 0) >= 0:
            capacity_lv_data.setdefault(capacity_type_safe_box, {})
            capacity_lv_data[capacity_type_safe_box][lv] = {'size': lv_conf['safe_box_size'],'price': lv_conf['safe_box_price']}
            if lv > capacity_max_lvs.get(capacity_type_safe_box, 0):
                capacity_max_lvs[capacity_type_safe_box] = lv


def get_capacity_size(capacity_type, lv):
    capacity_data = capacity_lv_data.get(capacity_type, {})
    if not capacity_data:
        return 0
    return capacity_data.get(lv, {}).get('size', 0)


def get_capacity_price(capacity_type, lv):
    capacity_data = capacity_lv_data.get(capacity_type, {})
    if not capacity_data:
        return -1
    return capacity_data.get(lv, {}).get('price', -1)


def get_capacity_max_lv--- This code section failed: ---

 106       0  LOAD_GLOBAL           0  'capacity_max_lvs'
           3  LOAD_ATTR             1  'get'
           6  LOAD_ATTR             1  'get'
           9  CALL_FUNCTION_2       2 
          12  RETURN_VALUE     
          -1  RETURN_LAST      

Parse error at or near `CALL_FUNCTION_2' instruction at offset 9


__init_data()