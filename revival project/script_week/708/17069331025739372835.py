# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/common_const/rank_activity_const.py
_reload_all = True
from logic.gcommon.common_const import statistics_const as sconst
from logic.gcommon.time_utility import time, ONE_WEEK_SECONDS
data = {'act_20210520_1': {'time_data': {'end_time': 1622628000,'settle_delay': 300,'reward_delay': 600,'pull_interval': 600},'reward_data': (
                                    (5, 12002711), (20, 12002712), (100, 12002713), (200, 12002714), (1000, 12002715), (10000000, 12002716)),
                      'battle_types': frozenset([4, 6]),'props': (sconst.KILL_HUMAN, sconst.KILL_MECHA)},
   'act_20210520_2': {'time_data': {'end_time': 1622628000,'settle_delay': 300,'reward_delay': 600,'pull_interval': 600},'reward_data': (
                                    (5, 12002711), (20, 12002712), (100, 12002713), (200, 12002714), (1000, 12002715), (10000000, 12002716)),
                      'battle_types': frozenset([42]),'props': (sconst.KILL_HUMAN, sconst.KILL_MECHA)},
   'act_20220720_1': {'time_data': {'end_time': 1659560400,'settle_delay': 300,'reward_delay': 600,'pull_interval': 300},'reward_data': (
                                    (5, 12301490), (20, 12301491), (100, 12301492), (200, 12301493), (1000, 12301494), (10000000, 12301495)),
                      'battle_types': frozenset([4, 6]),'props': (sconst.KILL_HUMAN, sconst.KILL_MECHA),'report_cond': lambda avatar: avatar.rushing_rank_type == 2
                      },
   'act_20210720_2': {'time_data': {'end_time': 1659560400,'settle_delay': 300,'reward_delay': 600,'pull_interval': 300},'reward_data': (
                                    (5, 12301496), (20, 12301497), (100, 12301498), (200, 12301499), (1000, 12301500), (10000000, 12301501)),
                      'battle_types': frozenset([42]),'props': (sconst.KILL_HUMAN, sconst.KILL_MECHA),'report_cond': lambda avatar: avatar.rushing_rank_type == 2
                      },
   'act_20220929_1': {'time_data': {'end_time': 1665608400,'settle_delay': 300,'reward_delay': 600,'pull_interval': 300},'reward_data': (
                                    (5, 12110445), (20, 12110446), (100, 12110447), (200, 12110448), (1000, 12110449), (10000000, 12110450)),
                      'battle_types': frozenset([4, 6]),'props': (sconst.KILL_HUMAN, sconst.KILL_MECHA),'report_cond': lambda avatar: avatar.rushing_rank_type == 2
                      },
   'act_20220929_2': {'time_data': {'end_time': 1665608400,'settle_delay': 300,'reward_delay': 600,'pull_interval': 300},'reward_data': (
                                    (5, 12110451), (20, 12110452), (100, 12110453), (200, 12110454), (1000, 12110455), (10000000, 12110456)),
                      'battle_types': frozenset([42]),'props': (sconst.KILL_HUMAN, sconst.KILL_MECHA),'report_cond': lambda avatar: avatar.rushing_rank_type == 2
                      },
   'act_20221215_1': {'time_data': {'end_time': 1672261200,'settle_delay': 300,'reward_delay': 600,'pull_interval': 300},'reward_data': (
                                    (10, 12301873), (100, 12301874), (200, 12301875), (1000, 12301876)),
                      'battle_types': frozenset([4, 6]),'props': (sconst.KILL_HUMAN, sconst.KILL_MECHA),'report_cond': lambda avatar: avatar.rushing_rank_type == 2,
                      'rank_title': (10, 633885, 1678914000)
                      },
   'act_20221215_2': {'time_data': {'end_time': 1672261200,'settle_delay': 300,'reward_delay': 600,'pull_interval': 300},'reward_data': (
                                    (10, 12301877), (100, 12301878), (200, 12301879), (1000, 12301880)),
                      'battle_types': frozenset([42]),'props': (sconst.KILL_HUMAN, sconst.KILL_MECHA),'report_cond': lambda avatar: avatar.rushing_rank_type == 2,
                      'rank_title': (10, 633886, 1678914000)
                      },
   'act_20230302_1': {'time_data': {'end_time': 1678914000,'settle_delay': 300,'reward_delay': 600,'pull_interval': 300},'reward_data': (
                                    (10, 12301873), (100, 12301874), (200, 12301875), (1000, 12301876)),
                      'battle_types': frozenset([4, 6]),'props': (sconst.KILL_HUMAN, sconst.KILL_MECHA),'report_cond': lambda avatar: avatar.rushing_rank_type == 2,
                      'rank_title': (10, 633885, 1683752400)
                      },
   'act_20230302_2': {'time_data': {'end_time': 1678914000,'settle_delay': 300,'reward_delay': 600,'pull_interval': 300},'reward_data': (
                                    (10, 12301877), (100, 12301878), (200, 12301879), (1000, 12301880)),
                      'battle_types': frozenset([42]),'props': (sconst.KILL_HUMAN, sconst.KILL_MECHA),'report_cond': lambda avatar: avatar.rushing_rank_type == 2,
                      'rank_title': (10, 633886, 1683752400)
                      },
   'act_20230517_1': {'time_data': {'end_time': 1685566800,'settle_delay': 300,'reward_delay': 600,'pull_interval': 300},'reward_data': (
                                    (10, 12301873), (100, 12301874), (200, 12301875), (1000, 12301876)),
                      'battle_types': frozenset([4, 6]),'props': (sconst.KILL_HUMAN, sconst.KILL_MECHA),'report_cond': lambda avatar: avatar.rushing_rank_type == 2,
                      'rank_title': (10, 633885, 1689800400)
                      },
   'act_20230517_2': {'time_data': {'end_time': 1685566800,'settle_delay': 300,'reward_delay': 600,'pull_interval': 300},'reward_data': (
                                    (10, 12301877), (100, 12301878), (200, 12301879), (1000, 12301880)),
                      'battle_types': frozenset([42]),'props': (sconst.KILL_HUMAN, sconst.KILL_MECHA),'report_cond': lambda avatar: avatar.rushing_rank_type == 2,
                      'rank_title': (10, 633886, 1689800400)
                      },
   'act_20230720_1': {'time_data': {'end_time': 1691010000,'settle_delay': 300,'reward_delay': 600,'pull_interval': 300},'reward_data': (
                                    (10, 12301873), (100, 12301874), (200, 12301875), (1000, 12301876)),
                      'battle_types': frozenset([4, 6]),'props': (sconst.KILL_HUMAN, sconst.KILL_MECHA),'report_cond': lambda avatar: avatar.rushing_rank_type == 2,
                      'rank_title': (10, 633885, 1695848400)
                      },
   'act_20230720_2': {'time_data': {'end_time': 1691010000,'settle_delay': 300,'reward_delay': 600,'pull_interval': 300},'reward_data': (
                                    (10, 12301877), (100, 12301878), (200, 12301879), (1000, 12301880)),
                      'battle_types': frozenset([42]),'props': (sconst.KILL_HUMAN, sconst.KILL_MECHA),'report_cond': lambda avatar: avatar.rushing_rank_type == 2,
                      'rank_title': (10, 633886, 1695848400)
                      },
   'act_20230928_1': {'time_data': {'end_time': 1697058000,'settle_delay': 300,'reward_delay': 600,'pull_interval': 300},'reward_data': (
                                    (10, 12301873), (100, 12301874), (200, 12301875), (1000, 12301876)),
                      'battle_types': frozenset([4, 6]),'props': (sconst.KILL_HUMAN, sconst.KILL_MECHA),'report_cond': lambda avatar: avatar.rushing_rank_type == 2,
                      'rank_title': (10, 633885, 1703106000)
                      },
   'act_20230928_2': {'time_data': {'end_time': 1697058000,'settle_delay': 300,'reward_delay': 600,'pull_interval': 300},'reward_data': (
                                    (10, 12301877), (100, 12301878), (200, 12301879), (1000, 12301880)),
                      'battle_types': frozenset([42]),'props': (sconst.KILL_HUMAN, sconst.KILL_MECHA),'report_cond': lambda avatar: avatar.rushing_rank_type == 2,
                      'rank_title': (10, 633886, 1703106000)
                      },
   'act_20231221_1': {'time_data': {'end_time': 1704315600,'settle_delay': 300,'reward_delay': 600,'pull_interval': 300},'reward_data': (
                                    (10, 12301873), (100, 12301874), (200, 12301875), (1000, 12301876)),
                      'battle_types': frozenset([4, 6]),'props': (sconst.KILL_HUMAN, sconst.KILL_MECHA),'report_cond': lambda avatar: avatar.rushing_rank_type == 2,
                      'rank_title': (10, 633885, 1711573200)
                      },
   'act_20231221_2': {'time_data': {'end_time': 1704315600,'settle_delay': 300,'reward_delay': 600,'pull_interval': 300},'reward_data': (
                                    (10, 12301877), (100, 12301878), (200, 12301879), (1000, 12301880)),
                      'battle_types': frozenset([42]),'props': (sconst.KILL_HUMAN, sconst.KILL_MECHA),'report_cond': lambda avatar: avatar.rushing_rank_type == 2,
                      'rank_title': (10, 633886, 1711573200)
                      },
   'act_20240328_1': {'time_data': {'end_time': 1712782800,'settle_delay': 300,'reward_delay': 600,'pull_interval': 300},'reward_data': (
                                    (10, 12301873), (100, 12301874), (200, 12301875), (1000, 12301876)),
                      'battle_types': frozenset([4, 6]),'props': (sconst.KILL_HUMAN, sconst.KILL_MECHA),'report_cond': lambda avatar: avatar.rushing_rank_type == 2,
                      'rank_title': (10, 633885, 1719435600)
                      },
   'act_20240328_2': {'time_data': {'end_time': 1712782800,'settle_delay': 300,'reward_delay': 600,'pull_interval': 300},'reward_data': (
                                    (10, 12301877), (100, 12301878), (200, 12301879), (1000, 12301880)),
                      'battle_types': frozenset([42]),'props': (sconst.KILL_HUMAN, sconst.KILL_MECHA),'report_cond': lambda avatar: avatar.rushing_rank_type == 2,
                      'rank_title': (10, 633886, 1719435600)
                      },
   'act_20240613_1': {'time_data': {'end_time': 1712782800,'settle_delay': 300,'reward_delay': 600,'pull_interval': 300},'reward_data': (
                                    (10, 12301873), (100, 12301874), (200, 12301875), (1000, 12301876)),
                      'battle_types': frozenset([4, 6]),'props': (sconst.KILL_HUMAN, sconst.KILL_MECHA),'report_cond': lambda avatar: avatar.rushing_rank_type == 2,
                      'rank_title': (10, 633885, 1719435600)
                      },
   'act_20240613_2': {'time_data': {'end_time': 1712782800,'settle_delay': 300,'reward_delay': 600,'pull_interval': 300},'reward_data': (
                                    (10, 12301877), (100, 12301878), (200, 12301879), (1000, 12301880)),
                      'battle_types': frozenset([42]),'props': (sconst.KILL_HUMAN, sconst.KILL_MECHA),'report_cond': lambda avatar: avatar.rushing_rank_type == 2,
                      'rank_title': (10, 633886, 1719435600)
                      }
   }
RANK_TYPE_TO_BATTLE_TYPES = {}
BATTLE_TYPE_TO_RANK_TYPES = {}
ACTIVITY_RANK_LIST = []
now = time()
for rank_type, rank_data in data.items():
    end_time = rank_data['time_data']['end_time']
    if now > end_time + ONE_WEEK_SECONDS * 2:
        continue
    act_prop_type = 'prop_%s' % rank_type
    RANK_TYPE_TO_BATTLE_TYPES[rank_type] = (rank_data['battle_types'], act_prop_type)
    rank_center = '%sRankCenter' % rank_type
    rank_stub = '%sRankStub' % rank_type
    rank_name = '%sRank' % rank_type
    ACTIVITY_RANK_LIST.append((rank_type, rank_center, rank_stub, rank_name))
    if now <= end_time:
        for battle_type in rank_data['battle_types']:
            prop_rank_types = BATTLE_TYPE_TO_RANK_TYPES.setdefault(battle_type, [])
            prop_rank_types.append((act_prop_type, rank_data['props']))

def get_battle_types_by_rank_type(rank_type):
    global RANK_TYPE_TO_BATTLE_TYPES
    return RANK_TYPE_TO_BATTLE_TYPES.get(rank_type, ((), ()))


def get_rank_type_by_battle_types(battle_type):
    global BATTLE_TYPE_TO_RANK_TYPES
    return BATTLE_TYPE_TO_RANK_TYPES.get(battle_type, [])


def get_time_data(rank_type):
    return data.get(rank_type, {}).get('time_data', {})


def get_expire_rank_reward_type():
    now = time()
    rank_types = []
    for rank_type, rank_data in data.items():
        if 'reward_data' not in rank_data:
            continue
        if 'time_data' not in rank_data:
            continue
        if now >= rank_data['time_data']['end_time']:
            rank_types.append(rank_type)

    return rank_types


def has_rank_reward(rank_type):
    return rank_type in data and 'reward_data' in data[rank_type]


def get_rank_reward_list(rank_type):
    if not has_rank_reward(rank_type):
        return []
    return data[rank_type]['reward_data']


def get_rank_reward_timestamp(rank_type, delay=0):
    try:
        time_data = data[rank_type]['time_data']
        return time_data['end_time'] + time_data['reward_delay'] + delay
    except:
        return 0


def get_rank_participate_end_timestamp(rank_type):
    try:
        time_data = data[rank_type]['time_data']
        return time_data['end_time']
    except:
        return 0


def get_rank_reward_id(rank_type, rank):
    if rank <= 0:
        return
    else:
        reward_data = data.get(rank_type, {}).get('reward_data', None)
        if not reward_data:
            return
        for _rank, reward_id in reward_data:
            if rank <= _rank:
                return reward_id

        return


def get_rank_title_reward_data(rank_type, avt_rank):
    if avt_rank <= 0:
        return
    else:
        rank_title_data = data.get(rank_type, {}).get('rank_title', None)
        if not rank_title_data:
            return
        rank, match_adcode, expire_time = rank_title_data
        if avt_rank > rank:
            return
        title_data = {str(match_adcode): (avt_rank, expire_time)}
        return title_data


def get_report_cond(rank_type):
    return data.get(rank_type, {}).get('report_cond', None)