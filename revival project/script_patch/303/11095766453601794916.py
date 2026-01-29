# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/cdata/intimacy_data.py
_reload_all = True
data = {0: (100, None),
   1: (100, None),
   2: (100, None),
   3: (200, None),
   4: (200, None),
   5: (
     300, (10, )),
   6: (500, None),
   7: (500, None),
   8: (1000, None),
   9: (
     1000, (11, )),
   10: (1000, None)
   }
LV_CAP = 10
LV_CAP_EXP = 1000
LV_CAP_REWARD_LV = 5
LV_CAP_REWARD = 11
INTIMACY_WEEK_LIMIT_PER_FRD = 150
INTIMACY_DAY_GIFT_NUM_LIMIT_PER_FRD = 40
NON_SHARE_MECHA_LIST = []
UNLOCK_MEMORY_LV = 6
from six.moves import range
from logic.gcommon.cdata.intimacy_reward_data import get_reward_id_by_intimacy_type
from logic.gcommon.const import IDX_INTIMACY_PT, IDX_INTIMACY_LV

def get_lv_data(lv):
    return data.get(lv, (None, None))


def get_unreceived_intimacy_rewards(intimacy_type, old_lv, new_lv):
    reward_ids = []
    for lv in range(old_lv + 1, new_lv + 1):
        if lv <= LV_CAP:
            reward_data = data[lv][-1] or ()
            for reward_type in reward_data:
                reward_id = get_reward_id_by_intimacy_type(reward_type, intimacy_type)
                reward_ids.append(reward_id)

        else:
            reward_id = get_reward_id_by_intimacy_type(LV_CAP_REWARD, intimacy_type)
            for _lv in range(lv, new_lv + 1):
                if divmod(_lv, 5)[-1] == 0:
                    reward_ids.append(reward_id)

            break

    return reward_ids


def get_intimacy_pt(intimacy_data):
    try:
        lv = intimacy_data[IDX_INTIMACY_LV]
        pt = intimacy_data[IDX_INTIMACY_PT]
        for _lv in range(0, lv):
            if _lv <= LV_CAP:
                pt += data[_lv][0]
            else:
                pt += max(0, lv - LV_CAP - 1) * LV_CAP_EXP
                break

        return pt
    except:
        return 0


def get_upgrade_intimacy_pt(intimacy_data):
    lv = intimacy_data[IDX_INTIMACY_LV]
    data = get_lv_data(lv)
    if data[0]:
        return data[0]
    else:
        return LV_CAP_EXP