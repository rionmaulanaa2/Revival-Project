# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/cdata/privilege_data.py
_reload_all = True
data = {1: (6, 12110122),
   2: (68, 12110123),
   3: (100, 12110124),
   4: (200, 12110125),
   5: (500, 12110126),
   6: (1000, 12110127),
   7: (2500, 12110128),
   8: (5000, 12110129),
   9: (10000, 12110429),
   10: (18000, 12110430),
   11: (28000, 12110673),
   12: (40000, 12110674)
   }
week_reward_data = {1: 12110130,
   2: 12110131,
   3: 12110132,
   4: 12110133,
   5: 12110134,
   6: 12110135,
   7: 12110136,
   8: 12110137,
   9: 12110431,
   10: 12110432,
   11: 12110675,
   12: 12110676
   }
handler_data = {5: 'colorful_font',
   7: 'gold_bonus',
   8: 'purple_id',
   10: 'share_mecha_fashion',
   12: 'red_packet'
   }
display_reward_data = {1: [
     (70400010, 1), (30170114, 1), (30500011, 1), (50101003, 500)],
   2: [
     (70400011, 1), (30710030, 1)],
   3: [
     (70400012, 1), (30620023, 1), (50101010, 1)],
   4: [
     (70400013, 1), (30170115, 1), (30500012, 1), (30140051, 1), (50101010, 1)],
   5: [
     (70400014, 1), (70400005, 1), (70400006, 1)],
   6: [
     (70400015, 1), (203800018, 1), (31000029, 1), (50101010, 5)],
   7: [
     (70400016, 1), (70400008, 1), (30170116, 1), (30500013, 1), (50101010, 8)],
   8: [
     (70400017, 1), (70400007, 1), (50101010, 8)],
   9: [
     (70400074, 1), (201800154, 1), (50101101, 10)],
   10: [
      (70400075, 1), (70400073, 1), (50101101, 10)],
   11: [
      (70400158, 1), (603000019, 1), (50101101, 10)],
   12: [
      (70400159, 1), (30170135, 1), (70400157, 1), (50101101, 10)]
   }
PAY_TASK_ID = 1301000
LV_CAP = 12
LV_UP_NOTICE = 1034
COLOR_FONT = 16740864
COLOR_NAME = 16740864
NOTICE_START_LV = 8
PRIV_RED_PACKET_TYPE = 5

def get_lv_data(lv):
    return data.get(lv, (None, None))


def get_lv_reward(lv):
    if lv <= LV_CAP:
        return data[lv][-1]
    else:
        return 0


def get_lv_week_reward(lv):
    if lv <= LV_CAP:
        return week_reward_data.get(lv)
    else:
        return 0


def get_handler_data():
    return handler_data


def get_lv_handler(lv):
    return handler_data.get(lv)