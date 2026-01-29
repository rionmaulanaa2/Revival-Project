# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/common_const/rank_const.py
from __future__ import absolute_import
import six
import six_ex
from functools import cmp_to_key
from . import rank_mecha_const
from . import rank_battle_score_const
from . import rank_career_const
from . import rank_activity_const
from . import pve_const
from logic.gcommon import time_utility as tutil
RANK_SERVICE_DES_KEY = '20201207'
RANK_TYPE_SOLO_COMBAT_SCORE = '1'
RANK_TYPE_SOLO_SURVIVAL_SCORE = '2'
RANK_TYPE_SOLO_OVERALL_SCORE = '3'
RANK_TYPE_DUO_COMBAT_SCORE = '4'
RANK_TYPE_DUO_SURVIVAL_SCORE = '5'
RANK_TYPE_DUO_OVERALL_SCORE = '6'
RANK_TYPE_SQUAD_COMBAT_SCORE = '7'
RANK_TYPE_SQUAD_SURVIVAL_SCORE = '8'
RANK_TYPE_SQUAD_OVERALL_SCORE = '9'
RANK_TYPE_FASHION = '10'
RANK_TYPE_DAN_SURVIVAL = '13'
RANK_TYPE_DAN_DEATH = '14'
RANK_TYPE_ALPHA_KNIGHT_SURVIVAL = '15'
RANK_TYPE_ALPHA_KNIGHT_DEATH = '16'
RANK_TYPE_FRIEND_HELP = '21'
RANK_TYPE_DEATH_OVERALL_SCORE = '22'
RANK_TYPE_MATCH_SCORE = '23'
RANK_TYPE_BATTLEPASS = '24'
RANK_TYPE_CHARM = '25'
RANK_TYPE_MONTH_CHARM = '26'
RANK_TYPE_DUEL = '27'
RANK_TYPE_ASSAULT_DPM = '30'
RANK_TYPE_ASSAULT_KPM = '31'
RANK_TYPE_ASSAULT_SCORE = '32'
RANK_TYPE_LUCK_WEEK = 'luck_{}_week'
RANK_TYPE_LUCK_TOTAL = 'luck_{}_total'
RANK_TYPE_CLAN_WEEK_POINT = '1001'
RANK_TYPE_CLAN_SEASON_POINT = '1002'
RANK_TYPE_CLAN_FASHION = '1003'
MAIN_RANK_MODEL_CTRL = 0
PVE_RANK_MODEL_CTRL = 1
SEASON_REFRESH = 0
WEEK_REFRESH = 1
DAY_REFRESH = 2
NOT_FRESH = 3
MONTH_REFRESH = 4
RANK_TYPE_SVC = {}
RANK_TYPE_CS = {RANK_TYPE_SOLO_COMBAT_SCORE: (
                               'SoloCombatRankCenter', 'SoloCombatRankStub', 'SoloCombatRank', SEASON_REFRESH),
   RANK_TYPE_SOLO_SURVIVAL_SCORE: (
                                 'SoloSurvivalRankCenter', 'SoloSurvivalRankStub', 'SoloSurvivalRank', SEASON_REFRESH),
   RANK_TYPE_SOLO_OVERALL_SCORE: (
                                'SoloOverallRankCenter', 'SoloOverallRankStub', 'SoloOverallRank', SEASON_REFRESH),
   RANK_TYPE_DUO_COMBAT_SCORE: (
                              'DuoCombatRankCenter', 'DuoCombatRankStub', 'DuoCombatRank', SEASON_REFRESH),
   RANK_TYPE_DUO_SURVIVAL_SCORE: (
                                'DuoSurvivalRankCenter', 'DuoSurvivalRankStub', 'DuoSurvivalRank', SEASON_REFRESH),
   RANK_TYPE_DUO_OVERALL_SCORE: (
                               'DuoOverallRankCenter', 'DuoOverallRankStub', 'DuoOverallRank', SEASON_REFRESH),
   RANK_TYPE_SQUAD_COMBAT_SCORE: (
                                'SquadCombatRankCenter', 'SquadCombatRankStub', 'SquadCombatRank', SEASON_REFRESH),
   RANK_TYPE_SQUAD_SURVIVAL_SCORE: (
                                  'SquadSurvivalRankCenter', 'SquadSurvivalRankStub', 'SquadSurvivalRank', SEASON_REFRESH),
   RANK_TYPE_SQUAD_OVERALL_SCORE: (
                                 'SquadOverallRankCenter', 'SquadOverallRankStub', 'SquadOverallRank', SEASON_REFRESH),
   RANK_TYPE_FASHION: (
                     'FashionRankCenter', 'FashionRankStub', 'FashionRank', NOT_FRESH),
   RANK_TYPE_DAN_SURVIVAL: (
                          'SurvivalDanRankCenter', 'SurvivalDanRankStub', 'SurvivalDanRank', SEASON_REFRESH),
   RANK_TYPE_ALPHA_KNIGHT_SURVIVAL: (
                                   'SurvivalAlphaKnightRankCenter', 'SurvivalAlphaKnightRankStub', 'SurvivalAlphaKnightRank', DAY_REFRESH),
   RANK_TYPE_DEATH_OVERALL_SCORE: (
                                 'DeathOverallRankCenter', 'DeathOverallRankStub', 'DeathOverallRank', SEASON_REFRESH),
   RANK_TYPE_MATCH_SCORE: (
                         'MatchScoreRankCenter', 'MatchScoreRankStub', 'MatchScoreRank', NOT_FRESH),
   RANK_TYPE_BATTLEPASS: (
                        'BattlePassRankCenter', 'BattlePassRankStub', 'BattlePassRank', SEASON_REFRESH),
   RANK_TYPE_CHARM: (
                   'CharmRankCenter', 'CharmRankStub', 'CharmRank', NOT_FRESH),
   RANK_TYPE_MONTH_CHARM: (
                         'CharmMonthRankCenter', 'CharmMonthRankStub', 'CharmMonthRank', MONTH_REFRESH),
   RANK_TYPE_DUEL: (
                  'DuelRankCenter', 'DuelRankStub', 'DuelRank', NOT_FRESH)
   }

def mecha_region_rank_valid():
    from logic.gcommon.const import SERVER_PRC_PC
    inner_invalid_hostnums = frozenset((91, ))
    try:
        from mobile.distserver.game import GameServerRepo
        hostnum = GameServerRepo.hostnum
        is_inner_server = GameServerRepo.is_inner_server()
    except:
        try:
            hostnum = global_data.channel.get_host_num()
        except:
            hostnum = 0

        is_inner_server = global_data.is_inner_server

    if is_inner_server:
        return hostnum not in inner_invalid_hostnums
    else:
        return hostnum != SERVER_PRC_PC


def is_world_mecha_region_rank():
    try:
        from mobile.distserver.game import GameServerRepo
        project_id = GameServerRepo.game_id
    except:
        from common.platform.dctool.interface import get_project_id
        project_id = get_project_id()

    return project_id.endswith('na')


if mecha_region_rank_valid():
    for mecha_id_str in rank_mecha_const.mecha_rank_list:
        RANK_TYPE_SVC[mecha_id_str] = (
         'MechaRegionRankService', 'Mecha%sRegionRank' % mecha_id_str, SEASON_REFRESH)

else:
    for mecha_id_str in rank_mecha_const.mecha_rank_list:
        RANK_TYPE_CS[mecha_id_str] = (
         'MechaRankCenter', 'MechaRankStub', 'Mecha%sRank' % mecha_id_str, SEASON_REFRESH)

for battle_type in rank_battle_score_const.OVERALL_BATTLE_TYPES:
    rank_type = rank_battle_score_const.battle_type_2_overall_rank_type[battle_type]
    RANK_TYPE_CS[rank_type] = ('OverallRankCenter', 'OverallRankStub', 'Overall%sRank' % battle_type, SEASON_REFRESH)

for rank_type in rank_career_const.CAREER_RANK_LIST:
    RANK_TYPE_CS[rank_type] = (
     'CareerRankCenter', 'CareerRankStub', 'Career%sRank' % rank_type, NOT_FRESH)

for rank_type, rank_center, rank_stub, rank_name in rank_activity_const.ACTIVITY_RANK_LIST:
    RANK_TYPE_CS[rank_type] = (
     rank_center, rank_stub, rank_name, NOT_FRESH)

RANK_TYPE_2_TYPE = {rank_info[2]:rank_type for rank_type, rank_info in six.iteritems(RANK_TYPE_CS)}
RANK_SVC_NAMES = set([ rank_info[0] for rank_info in six.itervalues(RANK_TYPE_SVC) ])

def get_rank_center_name(rank_type):
    if rank_type in RANK_TYPE_CS:
        return RANK_TYPE_CS[rank_type][0]
    else:
        return None


def get_rank_stub_name(rank_type):
    if rank_type in RANK_TYPE_CS:
        return RANK_TYPE_CS[rank_type][1]
    else:
        return None


def get_rank_redis_name(rank_type):
    if rank_type in RANK_TYPE_CS:
        return RANK_TYPE_CS[rank_type][2]
    else:
        return None


def get_rank_service_name(rank_type):
    if rank_type in RANK_TYPE_SVC:
        return RANK_TYPE_SVC[rank_type][0]
    else:
        return None


def get_rank_service_redis_name(rank_type):
    if rank_type in RANK_TYPE_SVC:
        return RANK_TYPE_SVC[rank_type][1]
    else:
        return None


def get_rank_type_by_name(rank_name):
    return RANK_TYPE_2_TYPE.get(rank_name, None)


def get_rank_name_by_center(center_name):
    rank_name = []
    for rank_type, center_stub_name in six.iteritems(RANK_TYPE_CS):
        if center_stub_name[0] == center_name:
            rank_name.append(center_stub_name[2])

    return rank_name


def get_rank_refresh_type_by_stub(stub_name):
    for rank_type, center_stub_name in six.iteritems(RANK_TYPE_CS):
        if center_stub_name[1] == stub_name:
            return center_stub_name[3]

    return NOT_FRESH


def is_rank_type_season_settle(rank_type):
    if rank_type in RANK_TYPE_CS:
        return RANK_TYPE_CS[rank_type][3] == SEASON_REFRESH
    else:
        if rank_type in RANK_TYPE_SVC:
            return RANK_TYPE_SVC[rank_type][2] == SEASON_REFRESH
        return False


def is_rank_type_week_fresh(rank_type):
    if rank_type in RANK_TYPE_CS:
        return RANK_TYPE_CS[rank_type][3] == WEEK_REFRESH
    return False


def is_rank_type_day_fresh(rank_type):
    if rank_type in RANK_TYPE_CS:
        return RANK_TYPE_CS[rank_type][3] == DAY_REFRESH
    return False


def is_rank_type_month_fresh(rank_type):
    if rank_type in RANK_TYPE_CS:
        return RANK_TYPE_CS[rank_type][3] == MONTH_REFRESH
    return False


def is_rank_season_settle(rank_name):
    rank_type = get_rank_type_by_name(rank_name)
    return is_rank_type_season_settle(rank_type)


def is_rank_week_fresh(rank_name):
    rank_type = get_rank_type_by_name(rank_name)
    return is_rank_type_week_fresh(rank_type)


def is_rank_day_fresh(rank_name):
    rank_type = get_rank_type_by_name(rank_name)
    return is_rank_type_day_fresh(rank_type)


def is_rank_month_fresh(rank_name):
    rank_type = get_rank_type_by_name(rank_name)
    return is_rank_type_month_fresh(rank_type)


def get_rank_refresh_type(rank_name):
    rank_type = get_rank_type_by_name(rank_name)
    return RANK_TYPE_CS[rank_type][3]


CLAN_RANK_TYPE_CS = {RANK_TYPE_CLAN_WEEK_POINT: ('ClanWeekPointRankCenter', 'ClanWeekPointRankStub', 'ClanWeekPointRank'),
   RANK_TYPE_CLAN_SEASON_POINT: ('ClanSeasonPointRankCenter', 'ClanSeasonPointRankStub', 'ClanSeasonPointRank'),
   RANK_TYPE_CLAN_FASHION: ('ClanFashionRankCenter', 'ClanFashionRankStub', 'ClanFashionRank')
   }

def get_clan_rank_stub_name(rank_type):
    return CLAN_RANK_TYPE_CS.get(rank_type, (None, None, None))[1]


def get_clan_rank_redis_name(rank_type):
    return CLAN_RANK_TYPE_CS.get(rank_type, (None, None, None))[2]


def get_clan_rank_name_by_center(center_name):
    rank_name = []
    for rank_type, center_stub_name in six.iteritems(CLAN_RANK_TYPE_CS):
        if center_stub_name[0] == center_name:
            rank_name.append(center_stub_name[2])

    return rank_name


RANK_STUB_NAMES = tuple(set([ stub_name for _, stub_name, _, _ in six.itervalues(RANK_TYPE_CS) ])) + tuple(set([ stub_name for _, stub_name, _ in six.itervalues(CLAN_RANK_TYPE_CS) ]))
RANK_CENTER_NAMES = tuple(set([ center_name for center_name, _, _, _ in six.itervalues(RANK_TYPE_CS) ])) + tuple(set([ center_name for center_name, _, _ in six.itervalues(CLAN_RANK_TYPE_CS) ]))
RANK_TYPE_FRIEND = 0
RANK_TYPE_DAN_SURVIVAL_C = 1
RANK_TYPE_MECHA = 2
RANK_TYPE_OVERALL = 3
RANK_TYPE_SURVIVAL = 4
RANK_TYPE_COMBAT = 5
RANK_TYPE_FASHION_C = 6
RANK_MECHA_READ_RECORD_KEY = 'rank_mecha_last_read'
RANK_TYPE_MAX_COUNT = 7
RANK_ONE_REQUEST_MAX_COUNT = 20
RANK_DATA_CACHE_MAX_TIME = 120
client_to_server_map = {'1_0': RANK_TYPE_DAN_SURVIVAL,
   '3_0': RANK_TYPE_SOLO_OVERALL_SCORE,
   '3_1': RANK_TYPE_DUO_OVERALL_SCORE,
   '3_2': RANK_TYPE_SQUAD_OVERALL_SCORE,
   '4_0': RANK_TYPE_SOLO_SURVIVAL_SCORE,
   '4_1': RANK_TYPE_DUO_SURVIVAL_SCORE,
   '4_2': RANK_TYPE_SQUAD_SURVIVAL_SCORE,
   '5_0': RANK_TYPE_SOLO_COMBAT_SCORE,
   '5_1': RANK_TYPE_DUO_COMBAT_SCORE,
   '5_2': RANK_TYPE_SQUAD_COMBAT_SCORE,
   '6_0': RANK_TYPE_FASHION
   }
server_to_client_map = {RANK_TYPE_DAN_SURVIVAL: (1, 0),
   RANK_TYPE_SOLO_OVERALL_SCORE: (3, 0),
   RANK_TYPE_DUO_OVERALL_SCORE: (3, 1),
   RANK_TYPE_SQUAD_OVERALL_SCORE: (3, 2),
   RANK_TYPE_SOLO_SURVIVAL_SCORE: (4, 0),
   RANK_TYPE_DUO_SURVIVAL_SCORE: (4, 1),
   RANK_TYPE_SQUAD_SURVIVAL_SCORE: (4, 2),
   RANK_TYPE_SOLO_COMBAT_SCORE: (5, 0),
   RANK_TYPE_DUO_COMBAT_SCORE: (5, 1),
   RANK_TYPE_SQUAD_COMBAT_SCORE: (5, 2),
   RANK_TYPE_FASHION: (6, 0)
   }

def client_to_server_rank(rank_type, sub_rank):
    return client_to_server_map.get('%d_%d' % (rank_type, sub_rank), None)


def server_to_client_rank(server_rank_type):
    return server_to_client_map.get(str(server_rank_type), None)


friend_sub_rank_to_server_rank_map = {0: RANK_TYPE_SOLO_OVERALL_SCORE,
   1: RANK_TYPE_DUO_OVERALL_SCORE,
   2: RANK_TYPE_SQUAD_OVERALL_SCORE
   }
server_rank_to_sub_rank_map = {RANK_TYPE_SOLO_OVERALL_SCORE: 0,
   RANK_TYPE_DUO_OVERALL_SCORE: 1,
   RANK_TYPE_SQUAD_OVERALL_SCORE: 2
   }
RANK_DATA_OUTSIDE = -1
RANK_DATA_NONE = -2
KING_BATTLE_RANK_ENTITY_STATUS_HUMAN = 1
KING_BATTLE_RANK_ENTITY_STATUS_MECHA = 2
KING_BATTLE_RANK_ENTITY_STATUS_DIE = 3
from logic.gcommon.cdata.dan_data import DAN_SURVIVAL, DAN_DEATH
DAN_2_KNIGHTRANK_TYPE = {DAN_SURVIVAL: RANK_TYPE_ALPHA_KNIGHT_SURVIVAL
   }
KNIGHTRANK_2_DAN_TYPE = {RANK_TYPE_ALPHA_KNIGHT_SURVIVAL: DAN_SURVIVAL
   }
RANK_TYPE_2_DAN = {RANK_TYPE_DAN_SURVIVAL: DAN_SURVIVAL
   }
DAN_2_RANK_TYPE = {DAN_SURVIVAL: RANK_TYPE_DAN_SURVIVAL
   }
SPECTATE_RECOMMEND_RANKS = {RANK_TYPE_DAN_SURVIVAL: {'priority': 1,'min_rank': 200,'cnt': 4,'text_id': 19441},RANK_TYPE_FASHION: {'priority': 12,'min_rank': 200,'cnt': 2,'text_id': 19442},RANK_TYPE_MATCH_SCORE: {'priority': 13,'min_rank': 1500,'cnt': 12,'text_id': 19444}}
if mecha_region_rank_valid():
    SPECTATE_RECOMMEND_RANKS[RANK_TYPE_DAN_SURVIVAL]['cnt'] += len(rank_mecha_const.mecha_ob_list)
    SPECTATE_RECOMMEND_THRESHOLD = len(SPECTATE_RECOMMEND_RANKS) + len(rank_mecha_const.mecha_ob_list)
else:
    for mecha_id_str in rank_mecha_const.mecha_ob_list:
        SPECTATE_RECOMMEND_RANKS[mecha_id_str] = {'priority': 2,'min_rank': 200,'cnt': 1,'text_id': 19443,'need_mecha_name': True}

    SPECTATE_RECOMMEND_THRESHOLD = len(SPECTATE_RECOMMEND_RANKS)
SORTED_SPECTATE_RECOMMEND_RANKS = sorted(six_ex.keys(SPECTATE_RECOMMEND_RANKS), key=cmp_to_key(lambda x, y: six_ex.compare(SPECTATE_RECOMMEND_RANKS[x]['priority'], SPECTATE_RECOMMEND_RANKS[y]['priority'])))
FRIEND_RANK = 0
ALL_AREA_RANK = 1
LINE_FRIEND_RANK = 2
REGION_CITY_RANK = 3
REGION_PROVINCE_RANK = 4
REGION_COUNTRY_RANK = 5
ALPHA_KINIGHT_LIMIT_NUM = 200
ALPHA_KINIGHT_MAIL_NUM = 50
NORMAL_PERIOD_SETTLE_RANK_NUM = 200
SCORE_PER_MINUTE = '1'
ASSIST_PER_MINUTE = '2'
DAMAGE_PER_MINUTE = '3'
HURT_PER_MINUTE = '4'
RANK_TITLE_MECHA_REGION = '1'
RANK_TITLE_MATCH_REGION = '2'
RANK_TITLE_CHARM = '3'
RANK_TITLE_ITEM = '4'
RANK_TITLE_PVE = '5'
NEED_CHECK_EXPIRE_TIME_TITLES = [
 33765006, 33765007, 33765008, 33765009, 33765015, 33765017]

def is_rank_title_valid(rank_title_dict, title_type, title_data, check_title=True):
    try:
        if check_title and title_type not in rank_title_dict:
            return (False, None)
        if title_type == RANK_TITLE_MECHA_REGION:
            region_type, mecha_type, rank_adcode, rank, rank_expire = title_data
            if check_title:
                if region_type not in rank_title_dict[title_type]:
                    return (False, None)
                if mecha_type not in rank_title_dict[title_type][region_type]:
                    return (False, None)
                rank_adcode, rank, rank_expire = rank_title_dict[title_type][region_type][mecha_type]
            if tutil.time() > rank_expire:
                return (False, None)
            return (
             True, (region_type, mecha_type, rank_adcode, rank, rank_expire))
        if title_type == RANK_TITLE_MATCH_REGION:
            match_adcode, rank, rank_expire = title_data
            if check_title:
                if match_adcode not in rank_title_dict[title_type]:
                    return (False, None)
                rank, rank_expire = rank_title_dict[title_type][match_adcode]
            if tutil.time() > rank_expire:
                return (False, None)
            return (
             True, (match_adcode, rank, rank_expire))
        if title_type == RANK_TITLE_CHARM:
            title_text, rank, rank_expire = title_data
            if check_title:
                if title_text not in rank_title_dict[title_type]:
                    return (False, None)
                rank, rank_expire = rank_title_dict[title_type][title_text]
            if tutil.time() > rank_expire:
                return (False, None)
            return (
             True, (title_text, rank, rank_expire))
        if title_type == RANK_TITLE_ITEM:
            title_id, rank_expire = title_data
            if check_title:
                if title_id not in rank_title_dict[title_type]:
                    return (False, None)
                rank_expire = rank_title_dict[title_type][title_id]
            if rank_expire > 0 and tutil.time() > rank_expire:
                return (False, None)
            return (
             True, (title_id, rank_expire))
        if title_type == RANK_TITLE_PVE:
            from logic.comsys.battle.pve.rank.PVERankDataObj import PVERankDataObj
            rank_type_data, rank, rank_expire = title_data
            data_obj = PVERankDataObj(rank_type_data) if isinstance(rank_type_data, str) else rank_type_data
            rank_type = data_obj.to_server()
            if check_title:
                if rank_type not in rank_title_dict[title_type]:
                    return (False, None)
                rank, rank_expire = rank_title_dict[title_type][rank_type]
            difficulty = data_obj.get_difficulty()
            refresh_type = data_obj.get_list_type()
            if difficulty == pve_const.HELL_DIFFICUTY and refresh_type == SEASON_REFRESH:
                from logic.gcommon.cdata import season_data
                if season_data.get_cur_battle_season() > rank_expire:
                    return (False, None)
            elif tutil.time() > rank_expire:
                return (False, None)
            return (
             True, (rank_type, rank, rank_expire))
    except:
        return (
         False, None)

    return None


def is_mecha_region_rank_title_valid(title_data):
    return is_rank_title_valid(None, RANK_TITLE_MECHA_REGION, title_data, False)


def is_match_region_rank_title_valid(title_data):
    return is_rank_title_valid(None, RANK_TITLE_MATCH_REGION, title_data, False)


def get_rank_use_title(rank_use_title_dict):
    for title_type, title_data in six.iteritems(rank_use_title_dict):
        if is_rank_title_valid(None, title_type, title_data, False):
            return title_data

    return


def get_rank_use_title_type(rank_use_title_dict):
    for title_type, title_data in six.iteritems(rank_use_title_dict):
        if is_rank_title_valid(None, title_type, title_data, False):
            return title_type

    return