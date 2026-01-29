# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/common_const/chat_const.py
from __future__ import absolute_import
_reload_all = True
CHAT_STATE_INVALID = -1
CHAT_STATE_VALID = 0
CHAT_STATE_FORBID = 1
CHAT_STATE_SLIENT = 2
CHAT_VALID_STATES = {
 CHAT_STATE_VALID, CHAT_STATE_SLIENT}
CHAT_WORLD = 0
CHAT_TEAM = 1
CHAT_CLAN = 2
CHAT_SYS = 3
CHAT_PIGEON = 4
CHAT_FRIEND = 5
CHAT_NOTICE = 6
CHAT_WORLD_BROADCAST = 7
CHAT_ROOM = 8
CHAT_NOTICE_BROADCAST = 9
CHAT_BATTLE_WORLD = 10
CHAT_MATCH_QUEUE = 11
CHAT_VISIT = 12
CHAT_ROOM_SHARE = 13
CHAT_CHANNEL_NUM = 14
POP_OUT_CHAT = set([CHAT_TEAM, CHAT_VISIT])
MODERATION_CHANNEL_SET = {
 CHAT_WORLD, CHAT_CLAN, CHAT_PIGEON}
CHAT_REGION_MAINLAND = 'CN'
CHAT_REGION_MACAO = 'MO'
CHAT_REGION_HK = 'HK'
CHAT_REGION_TW = 'TW'
MODERATION_CHAT_REGION_SET = {
 CHAT_REGION_MAINLAND, CHAT_REGION_MACAO, CHAT_REGION_HK, CHAT_REGION_TW}
MSG_TYPE_TEAM_INVITE = 0
MSG_TYPE_CLAN_CARD = 1
MSG_TYPE_ROOM_CARD = 2
MSG_TYPE_SKIN_DEFINE = 3
MSG_TYPE_VIDEO_SHARE = 4
MSG_TYPE_TEAM_RECRUIT = 5
MSG_TYPE_CONCERT_FIREWORK = 6
MSG_TYPE_CONCERT_BULLET = 7
MSG_TYPE_ACHIEVEMENT_SEASON_MEMORY = 8
MSG_TYPE_MECHA_SEASON_MEMORY = 9
MSG_TYPE_FRIEND_SEASON_MEMORY = 10
MSG_TYPE_LUCKY_LOTTERY = 11
CHAT_CHANNEL_NAME = {CHAT_WORLD: 'world',
   CHAT_TEAM: 'team',
   CHAT_CLAN: 'clan',
   CHAT_SYS: 'sys',
   CHAT_PIGEON: 'pigeon',
   CHAT_FRIEND: 'friend',
   CHAT_BATTLE_WORLD: 'battle_world',
   CHAT_VISIT: 'visit'
   }
CHAT_MIN_INTERVAL = 10
CHAT_TEAM_INVITE_INTERVAL = 10
CHAT_CLAN_INTERVAL = 2
CHAT_ROOM_INTERVAL = 2
CHAT_VISIT_INTERVAL = 2
CHAT_UPDATE_LOAD_TIME = 2
CHAT_INVITE_GAME_MODE_LIST = ({'name': 19341}, {'name': 19345})
CHAT_INVITE_PLAYER_COUNT_LIST = ({'num': 3,'name': 19007},)
CHAT_INVITE_TAB_LIST = (11023, 11024, 11025, 11026, 11027, 11028, 11029, 11030)
CHAT_INVITE_MSG_MAX_BYTE_COUNT = 30
WINNING_STREAK_CHANNEL = [
 CHAT_WORLD, CHAT_CLAN]
LINK_INVITE_TEAM = 0
CHAT_PIGEON_MIN_LEVEL = 10
CHAT_PIGEON_COST_ITEM_NO = 50500001
CHAT_PIGEON_COST_ITEM_AMOUNT_PER_TIME = 1
VOICE_NONE_MAX_TIME = 0.2
SEND_WORLD_MSG_MIN_LV = 5
SEND_NON_FRD_MSG_MIN_LV = 5
CHAT_ROOM_TYPE_WORLD = 1
CHAT_ROOM_TYPE_CLAN = 2
CHAT_ROOM_TYPE_LOBBY = 3
CHAT_ROOM_TYPE_TOWN = 4
CHAT_ROOM_TYPE_CUSTOM_ROOM = 5
CHAT_ROOM_TYPE_BATTLE = 6
VIST_ROOM_TYPE = frozenset((CHAT_ROOM_TYPE_LOBBY,))
FACEBOOK_ICON = 'gui/ui_res_2/icon/icon_btn_fb.png'
TWITTER_ICON = 'gui/ui_res_2/icon/icon_btn_twitter.png'
MESSENGER_ICON = 'gui/ui_res_2/icon/icon_btn_messenger.png'
LINE_ICON = 'gui/ui_res_2/icon/icon_btn_line.png'
SHARE_LINE_ICON = 'gui/ui_res_2/share/line.png'
CHAT_WORLD_EN = 1000
CHAT_WORLD_TW = 1001
CHAT_WORLD_JP = 1002
CHAT_WORLD_TH = 1003
CHAT_WORLD_ID = 1004
CHAT_WORLD_KO = 1005
CHAT_WORLD_OTHER = 1006
from . import lang_data
SHORTHAND_2_CHATH_WORLD_LANG = {lang_data.LANG_EN: CHAT_WORLD_EN,
   lang_data.LANG_CN: CHAT_WORLD_TW,
   lang_data.LANG_ZHTW: CHAT_WORLD_TW,
   lang_data.LANG_JA: CHAT_WORLD_JP,
   lang_data.LANG_TH: CHAT_WORLD_TH,
   lang_data.LANG_ID: CHAT_WORLD_ID,
   lang_data.LANG_KO: CHAT_WORLD_KO
   }
WORLD_SHARE_SKIN_INTERVAL = 300
WORLD_SHARE_SKIN_INTERVAL_FRD = 5
PIGEON_NORMAL = 1
PIGEON_RED_PACKET = 2
winning_streak_bgs = {'3': [
       'gui/ui_res_2/common_new/chat/chat_new/pnl_talk_s_purple.png',
       'gui/ui_res_2/common_new/chat/chat_new/icon_search_s_purple.png'],
   '5': [
       'gui/ui_res_2/common_new/chat/chat_new/pnl_talk_s.png',
       'gui/ui_res_2/common_new/chat/chat_new/icon_search_s.png'],
   '10': [
        'gui/ui_res_2/common_new/chat/chat_new/pnl_talk_s_red.png',
        'gui/ui_res_2/common_new/chat/chat_new/icon_search_s_red.png'],
   '20': [
        'gui/ui_res_2/common_new/chat/chat_new/pnl_talk_ss.png',
        'gui/ui_res_2/common_new/chat/chat_new/icon_search_ss.png']
   }
DANMU_TYPE_NORMAL = 1
DANMU_TYPE_SEND_RED = 2
DANMU_TYPE_REVC_RED = 3