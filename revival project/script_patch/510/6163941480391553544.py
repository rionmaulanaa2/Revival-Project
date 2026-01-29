# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/common_const/liveshow_const.py
NOT_LIVE = 0
CC_LIVE = 1
HUYA_LIVE = 2
DOUYU_LIVE = 3
BILIBILI_LIVE = 4
KUAISHOU_LIVE = 5
CC_GAME_ID = 10192
TAG_ALL = 1
TAG_PLATFORM_LABEL = 2
TAG_FOLLOW = 3
CC_GAME_SRC = CC_GAME_PLATFORM = 'g93'
CC_IOS_CLIENT_TYPE = 1255
CC_ANDROID_CLIENT_TYPE = 1254
CC_WINDOWS_CLIENT_TYPE = 126
LIVE_TYPE_RECOMMEND = 1
LIVE_TYPE_FRIENDS = 2
LIVE_TYPE_FOLLOW = 3
LIVE_TYPE_TEAM = 4
LIVE_TYPE_CC_LIVE = 4
FOLLOWED_ANCHOR_MAX_NUM = 15
REQUEST_ANCHOR_LIST_CD = 300
REQUEST_ANCHOR_STATUS_CD = 60
PAGE_REQUEST_CD = 10
LIVE_LIST_EXPIRE_TIME = 300
DANMU_CD = 5
OPEN_HOST_CN = [
 10000, 15000, 9010, 125, 156, 202, 179, 178]
OPEN_HOST_NA = [20000, 21000, 24000, 402, 128]
OPEN_HOST_US = [30000, 32000, 401, 127]
WINTER_CUP_OPEN_TIME = None
WINTER_CUP_OPEN_TIME_CN = (1703865600, 1705507199)
WINTER_CUP_OPEN_TIME_NA = (1703862000, 1705503599)
WINTER_CUP_OPEN_TIME_US = (1703908800, 1705550399)

def load_winter_cup_open_time():
    global WINTER_CUP_OPEN_TIME
    hostnum = global_data.channel._hostnum
    if hostnum in OPEN_HOST_CN:
        WINTER_CUP_OPEN_TIME = WINTER_CUP_OPEN_TIME_CN
    elif hostnum in OPEN_HOST_NA:
        WINTER_CUP_OPEN_TIME = WINTER_CUP_OPEN_TIME_NA
    elif hostnum in OPEN_HOST_US:
        WINTER_CUP_OPEN_TIME = WINTER_CUP_OPEN_TIME_US
    else:
        print (
         'load_winter_cup_open_time____error_hostnum:', hostnum)
        WINTER_CUP_OPEN_TIME = WINTER_CUP_OPEN_TIME_CN


def get_winter_cup_open_time():
    if WINTER_CUP_OPEN_TIME is None:
        load_winter_cup_open_time()
    return WINTER_CUP_OPEN_TIME


PROMOTION_MATCH_OPEN_HOST_CN = [
 10000, 125]
PROMOTION_MATCH_OPEN_HOST_NA = []
PROMOTION_MATCH_OPEN_HOST_US = []
PROMOTION_MATCH_OPEN_TIME = None
PROMOTION_MATCH_OPEN_TIME_CN = (1705680000, 1705852799)
PROMOTION_MATCH_OPEN_TIME_NA = (1705680000, 1705852799)
PROMOTION_MATCH_OPEN_TIME_US = (1705593600, 1705766399)

def load_winter_cup_promotion_match_open_time():
    global PROMOTION_MATCH_OPEN_TIME
    hostnum = global_data.channel._hostnum
    if hostnum in PROMOTION_MATCH_OPEN_HOST_CN:
        PROMOTION_MATCH_OPEN_TIME = PROMOTION_MATCH_OPEN_TIME_CN
    elif hostnum in PROMOTION_MATCH_OPEN_HOST_NA:
        PROMOTION_MATCH_OPEN_TIME = PROMOTION_MATCH_OPEN_TIME_NA
    elif hostnum in PROMOTION_MATCH_OPEN_HOST_US:
        PROMOTION_MATCH_OPEN_TIME = PROMOTION_MATCH_OPEN_TIME_US
    else:
        print (
         'load_promotion_match_open_time____error_hostnum:', hostnum)
        PROMOTION_MATCH_OPEN_TIME = (-1, -1)


def get_promotion_match_open_time():
    if PROMOTION_MATCH_OPEN_TIME is None:
        load_winter_cup_promotion_match_open_time()
    return PROMOTION_MATCH_OPEN_TIME


SUMMER_FINAL_LIVE_RED_POINT = 'winter_cup_23_final_live_red_point'
SUMMER_FINAL_URL_DICT = {CC_LIVE: '\xe6\x9c\xba\xe5\x8a\xa8\xe9\x83\xbd\xe5\xb8\x82\xe9\x98\xbf\xe5\xb0\x94\xe6\xb3\x95',
   HUYA_LIVE: '\xe6\x9c\xba\xe5\x8a\xa8\xe9\x83\xbd\xe5\xb8\x82\xe9\x98\xbf\xe5\xb0\x94\xe6\xb3\x95',
   BILIBILI_LIVE: '\xe6\x9c\xba\xe5\x8a\xa8\xe9\x83\xbd\xe5\xb8\x82\xe9\x98\xbf\xe5\xb0\x94\xe6\xb3\x95',
   KUAISHOU_LIVE: '\xe6\x9c\xba\xe5\x8a\xa8\xe9\x83\xbd\xe5\xb8\x82\xe9\x98\xbf\xe5\xb0\x94\xe6\xb3\x95'
   }