# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/common_const/spectate_const.py
from __future__ import absolute_import
_reload_all = True
SPECTATE_LIST_RECOMMEND = 1
SPECTATE_LIST_FRIEND = 2
SPECTATE_LIST_FOLLOW = 3
SPECTATE_LIST_TEAM = 4
SPECTATE_LIST_CC_LIVE = 5
SPECTATE_LIST_SEARCH = 6
SPECTATE_LIVE_MIRRATIV = 7
SPECTATE_LIST_CLAN = 8
SPECTATE_LIST_COMPETITION = 9
SPECTATE_LIST_OB = 10
SPECTATE_LIST_YOUTUBE = 11
GLOBAL_SPECTATE_SYNC_SNAPSHOT = 1
GLOBAL_SPECTATE_SYNC_METHOD = 2
GLOBAL_SPECTATE_SWITCH_OBJ = 3
GLOBAL_SPECTATE_BATTLE_FINISH = 4
GLOBAL_SPECTATE_BATTLE_RPC = 5
GLOBAL_SPECTATE_BATTLE_START = 6
GLOBAL_SPECTATE_SYNC_CANDIDATES = 7
GLOBAL_SPECTATE_SYNC_PLAYER_INFO_FOR_OB = 8
GLOBAL_SPECTATE_OB_BATTLE_FINISH = 9
GLOBAL_SPECTATE_UPDATE_PLAYER_INFO_FOR_OB = 10
GLOBAL_SPECTATE_OB_ENTER_GOD_CAMERA = 11
GLOBAL_SPECTATE_SOUL_DIRECT_SYNC = 12
GLOBAL_SPECTATE_SNAPSHOT_INTERVAL = 20
SPECTATE_SAME_PLAYER_LIKE_MAX_NUM_PER_DAY = 3
SPECTATE_CLIENT_DELAY_TIME = 30
SPECTATE_DELAY_PUBLISH_TICK_INTERVAL = 0.2
GLOBAL_SPECTATE_MAX_INIT_TIME = SPECTATE_CLIENT_DELAY_TIME + 5
CLIENT_LOADING_SPECTATE_TIME = 8
GLOBAL_SPECTATE_WAIT_PARACHUTE_MAX_TIME = 60
GLOBAL_SPECTATE_CANDIDATES_MAX_NUM = 3
GLOBAL_SPECTATE_SWITCH_NEED_MIN_MESSAGE_NUM_LEFT = 1
GLOBAL_SPECTATE_BATTLE_MAX_SPECTATOR_NUM = 2500
GLOBAL_SPECTATE_SHORT_SNAPSHOT_INTERVAL = 10
GLOBAL_SPECTATE_SWITCH_MIN_INTERVAL = GLOBAL_SPECTATE_SHORT_SNAPSHOT_INTERVAL
GLOBAL_SPECTATE_MANUAL_SWITCH_MAX_WAIT_TIME = GLOBAL_SPECTATE_SHORT_SNAPSHOT_INTERVAL + 5
SPECTATE_OB_PLAYER_INFO_KEYS = ('uid', 'role_name', 'role_id', 'head_photo', 'head_frame',
                                'group_id', 'eid', 'is_alive')
SPECTATE_OB_MAX_TRY_TIMES = 10
GLOBAL_SPECTATE_OB_SWITCH_MIN_INTERVAL = 3
GLOBAL_SPECTATE_OB_BROADCAST_PLAYER_INFO_INTERVAL = 1
GLOBAL_SPECTATE_OB_TAKE_SNAPSHOT_DELAY = 2
GLOBAL_SPECTATE_OB_SWITCH_DELAY = 1
SPECTATE_OB_UPDATE_PLAYER_INFO_KEYS = ('mecha_id', 'position', 'in_mecha', 'yaw', 'recall_cd',
                                       'recall_left_time', 'recall_cd_type', 'recall_cd_rate',
                                       'in_mecha_type', 'mecha_dict', 'is_attacking')
GLOBAL_SPECTATE_RESTORE_TIMEOUT = 5
GLOBAL_SPECTATE_SPEC_INFO_EXPIRE_SECONDS = 5400
GLOBAL_SPECTATE_RECORD_CLEAR_TRY_INTERVAL = 2
GLOBAL_SPECTATE_KEY_RECORDS_RECOMMEND = 'recommend'
GLOBAL_SPECTATE_KEY_RECORDS_UID_SET = 'uid_set'
GLOBAL_SPECTATE_OB_GOD_CAMERA_OPER_ENTER = 1
GLOBAL_SPECTATE_OB_GOD_CAMERA_OPER_LEAVE = 2
GLOBAL_SPECTATE_OB_GOD_CAMERA_OPER_MOVE = 3
SPECTATE_COMPETITION_REWARD_MIN_TIME_SECONDS = 300
SPECTATE_COMPETITION_REWARD_ID = 12300410
if G_IS_SERVER:
    from mobile.distserver.game import GameServerRepo
    SPECRECOM = lambda key: 'SpecRecom:%s:%s:%s' % (GameServerRepo.hostnum, GameServerRepo.version, key)
    SPECINFO = lambda uid: 'SpecInfo:%s:%s:%s' % (GameServerRepo.hostnum, GameServerRepo.version, uid)
    SPECBRIEF = lambda uid: 'SpecBrief:%s:%s:%s' % (GameServerRepo.hostnum, GameServerRepo.version, uid)
    SPECCOMP = lambda : 'SpecComp:%s:%s' % (GameServerRepo.hostnum, GameServerRepo.version)
    SPECWEEKCOMP = lambda : 'SpecWeekComp:%s:%s' % (GameServerRepo.hostnum, GameServerRepo.version)
    SPECOB = lambda battle_id: 'SpecOb:%s:%s:%s' % (GameServerRepo.hostnum, GameServerRepo.version, battle_id)
    OB_SPECTATE_CHANNEL_NAME = lambda battle_id, uid: 'ob_%s_%s' % (battle_id, uid)
    SPEC_BATTLE_PLAYERS = lambda battle_id: 'SpecBat:%s:%s' % (GameServerRepo.hostnum, battle_id)
    SPECKEYRECORDS = lambda : 'SpecKeyRecords:%s:%s:%s' % (GameServerRepo.hostnum, GameServerRepo.version, GameServerRepo.game_server_name)