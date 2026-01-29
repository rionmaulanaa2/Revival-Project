# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/cdata/season_data.py
_reload_all = True
if G_IS_NA_PROJECT:
    from .na_season_data import *
else:
    data = {1: {'start_time': '2021/1/20 00:00','start_timestamp': 1611072000,
           'pass_balance_timestamp': 1617206400
           },
       2: {'start_time': '2021/3/17 12:00',
           'start_timestamp': 1615953600,
           'pass_balance_timestamp': 1623340800
           },
       3: {'start_time': '2021/5/26 12:00',
           'start_timestamp': 1622001600,
           'pass_balance_timestamp': 1629907200
           },
       4: {'start_time': '2021/8/11 12:00',
           'start_timestamp': 1628654400,
           'pass_balance_timestamp': 1636560000
           },
       5: {'start_time': '2021/10/27 12:00',
           'start_timestamp': 1635307200,
           'pass_balance_timestamp': 1642608000
           },
       6: {'start_time': '2022/1/5 12:00',
           'start_timestamp': 1641355200,
           'pass_balance_timestamp': 1649865600
           },
       7: {'start_time': '2022/3/30 12:00',
           'start_timestamp': 1648612800,
           'pass_balance_timestamp': 1657123200
           },
       8: {'start_time': '2022/6/22 12:00',
           'start_timestamp': 1655870400,
           'pass_balance_timestamp': 1664380800,
           'rank_start_timestamp': 1657728000,
           'rank_end_timestamp': 1658937600,
           'rank_reward_start_timestamp': 1658955600,
           'rank_reward_end_timestamp': 1659456000
           },
       9: {'start_time': '2022/9/14 12:00',
           'start_timestamp': 1663128000,
           'pass_balance_timestamp': 1671638400
           },
       10: {'start_time': '2022/12/7 12:00',
            'start_timestamp': 1670385600,
            'pass_balance_timestamp': 1678896000
            },
       11: {'start_time': '2023/3/1 12:00',
            'start_timestamp': 1677643200,
            'pass_balance_timestamp': 1684944000
            },
       12: {'start_time': '2023/5/10 12:00',
            'start_timestamp': 1683691200,
            'pass_balance_timestamp': 1690992000
            },
       13: {'start_time': '2023/7/19 12:00',
            'start_timestamp': 1689739200,
            'pass_balance_timestamp': 1697040000
            },
       14: {'start_time': '2023/9/26 12:00',
            'start_timestamp': 1695700800,
            'pass_balance_timestamp': 1704297600
            },
       15: {'start_time': '2023/12/20 12:00',
            'start_timestamp': 1703044800,
            'pass_balance_timestamp': 1712160000
            },
       16: {'start_time': '2024/3/27 12:00',
            'start_timestamp': 1711512000,
            'pass_balance_timestamp': 1720627200
            },
       17: {'start_time': '2024/6/26 12:00',
            'start_timestamp': 1719374400,
            'pass_balance_timestamp': 1727280000
            },
       18: {'start_time': '2024/9/11 12:00',
            'start_timestamp': 1726027200,
            'pass_balance_timestamp': 1734537600
            },
       19: {'start_time': '2024/12/5 21:00',
            'start_timestamp': 1733403600,
            'pass_balance_timestamp': 1741795200
            },
       20: {'start_time': '2025/2/26 12:00',
            'start_timestamp': 1740542400,
            'pass_balance_timestamp': 1749052800
            },
       21: {'start_time': '2025/5/21 12:00',
            'start_timestamp': 1747800000,
            'pass_balance_timestamp': 1756310400
            },
       22: {'start_time': '2025/8/13 12:00',
            'start_timestamp': 1755057600,
            'pass_balance_timestamp': 1763568000
            },
       23: {'start_time': '2025/11/05 12:00',
            'start_timestamp': 1762315200,
            'pass_balance_timestamp': 1770825600
            },
       24: {'start_time': '2026/1/28 12:00',
            'start_timestamp': 1769572800,
            'pass_balance_timestamp': 1778083200
            },
       25: {'start_time': '2026/4/22 12:00',
            'start_timestamp': 1776830400,
            'pass_balance_timestamp': 1785340800
            },
       26: {'start_time': '2026/7/15 12:00',
            'start_timestamp': 1784088000,
            'pass_balance_timestamp': 1791475200
            },
       27: {'start_time': '2026/10/7 12:00',
            'start_timestamp': 1791345600,
            'pass_balance_timestamp': 1799856000
            },
       28: {'start_time': '2026/12/30 12:00',
            'start_timestamp': 1798603200,
            'pass_balance_timestamp': 1807113600
            },
       29: {'start_time': '2027/3/24 12:00',
            'start_timestamp': 1805860800,
            'pass_balance_timestamp': 1814371200
            }
       }
from six.moves import range
SETTLE_DAN_PRIORITY = 1
SETTLE_STAT_PRIORITY = 2
import math
from logic.gcommon import time_utility as tutil
DATE_FORMAT = '%Y/%m/%d %H:%M'

def get_total_season():
    return len(data)


def get_start_time(season):
    return data.get(season, {}).get('start_time', None)


def get_end_time--- This code section failed: ---

 211       0  LOAD_GLOBAL           0  'data'
           3  LOAD_ATTR             1  'get'
           6  LOAD_ATTR             1  'get'
           9  BINARY_ADD       
          10  BUILD_MAP_0           0 
          13  CALL_FUNCTION_2       2 
          16  LOAD_ATTR             1  'get'
          19  LOAD_CONST            2  'start_time'
          22  LOAD_CONST            0  ''
          25  CALL_FUNCTION_2       2 
          28  RETURN_VALUE     

Parse error at or near `BINARY_ADD' instruction at offset 9


def get_balance_time(season):
    return data.get(season, {}).get('pass_balance_timestamp', 0)


def get_start_timestamp(season):
    return data.get(season, {}).get('start_timestamp', 0)


def get_end_timestamp--- This code section failed: ---

 221       0  LOAD_GLOBAL           0  'data'
           3  LOAD_ATTR             1  'get'
           6  LOAD_ATTR             1  'get'
           9  BINARY_ADD       
          10  BUILD_MAP_0           0 
          13  CALL_FUNCTION_2       2 
          16  LOAD_ATTR             1  'get'
          19  LOAD_CONST            2  'start_timestamp'
          22  LOAD_CONST            3  ''
          25  CALL_FUNCTION_2       2 
          28  RETURN_VALUE     
          -1  RETURN_LAST      

Parse error at or near `BINARY_ADD' instruction at offset 9


def get_battle_season(cur_season=1):
    now = tutil.time()
    max_season = get_total_season()
    for season in range(cur_season, max_season + 1):
        start_timestamp = get_start_timestamp(season)
        if not start_timestamp or now < start_timestamp:
            return season
        end_timestamp = get_end_timestamp(season)
        if not end_timestamp:
            return season
        if start_timestamp <= now < end_timestamp:
            return season

    return 1


def get_season_week(season):
    if season:
        start_timestamp = get_start_timestamp(season)
        if not start_timestamp:
            log_error('No data of season %s', season)
            return 0
        now = tutil.time()
        if now < start_timestamp:
            week_no = 1
        else:
            week_no = int(math.ceil(float(now - start_timestamp) / tutil.ONE_WEEK_SECONDS))
        return week_no
    else:
        return 0


CUR_SEASON = 1

def get_cur_battle_season():
    global CUR_SEASON
    CUR_SEASON = get_battle_season(CUR_SEASON)
    return CUR_SEASON


def get_season_day_no(season, game_time):
    season_start_ts = get_start_timestamp(season)
    day_start_ts = tutil.get_day_start_timestamp(season_start_ts)
    game_day_no = tutil.get_rela_day_no(game_time, base_time=day_start_ts)
    return game_day_no