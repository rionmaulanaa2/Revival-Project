# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/cdata/mecha_component_conf.py
_reload_all = True
if G_IS_NA_PROJECT:
    from .na_mecha_component_conf import *
else:
    from logic.gcommon import const
    lv_unlock_data = {15: (const.MECHA_PART_HEAD, 0),18: (
          const.MECHA_PART_BODY, 0),
       22: (
          const.MECHA_PART_RIGHT_ARM, 0),
       26: (
          const.MECHA_PART_LOWER_BODY, 0),
       30: (
          const.MECHA_PART_LEFT_ARM, 0),
       34: (
          const.MECHA_PART_PROPELLER, 0)
       }
    lv_tech_data = {15: 0,
       18: 0,
       22: 0,
       26: 0,
       30: 0,
       34: 0,
       36: 0,
       38: 0,
       40: 0,
       42: 0,
       44: 0,
       46: 0,
       48: 0,
       50: 0,
       54: 0,
       58: 0,
       62: 0,
       66: 0,
       70: 0,
       74: 0,
       78: 0,
       82: 0,
       86: 0,
       90: 0,
       94: 0,
       100: 0
       }
    lv_give_com_data = {26: 48000225,
       30: 48000127,
       34: 48000212
       }
    UNLOCK_PAGE_PRICE = 200
    GIVE_CNT = 6
    UNLOCK_SLOT_PRICE = 300
    MAX_PAGE_NUM = 3
    GIVE_COM_LIST = (48000116, 48000119, 48000213)
import six
import six_ex
EVENT_INIT_AVATAR = 'EVENT_INIT_AVATAR'
EVENT_JOIN_MECHA_FOR_AVATAR = 'EVENT_JOIN_MECHA_FOR_AVATAR'
EVENT_INIT_MECHA = 'EVENT_INIT_MECHA'
EVENT_JOIN_MECHA_FOR_MECHA = 'EVENT_JOIN_MECHA_FOR_MECHA'
reward_unlock_lvs = []
part2_unlock_lv_mp = {}

def _init_data():
    global reward_unlock_lvs
    global part2_unlock_lv_mp
    for lv, unlock_data in six.iteritems(lv_unlock_data):
        if unlock_data[0] is not None:
            part2_unlock_lv_mp[unlock_data[0]] = lv

    reward_unlock_lvs = six_ex.keys(lv_tech_data)
    reward_unlock_lvs.sort()
    return


_init_data()

def get_reward_lvs():
    return reward_unlock_lvs


def get_part_unlock_lv(part, idx):
    return part2_unlock_lv_mp.get(int(part))


def get_tech_cnt(lv):
    return lv_tech_data.get(int(lv), 0)


def get_give_com_level(com_id):
    for lv, _com_id in six.iteritems(lv_give_com_data):
        if com_id == _com_id:
            return lv

    return 0