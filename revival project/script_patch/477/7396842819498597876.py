# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/ctypes/SpectateData.py
from __future__ import absolute_import
import json
import six
from msgpack.bson_msgpack import msgpackext
from msgpack.bson_msgpack import ext_hook
try:
    from msgpack import packb, unpackb
except ImportError:
    from msgpack.embed import packb, unpackb

from logic.gcommon import time_utility as tutil
from logic.gcommon.common_const import spectate_const as sp_const
from logic.gcommon.common_const import battle_const
ENCODE = --- This code section failed: ---

  18       0  LOAD_GLOBAL           0  'packb'
           3  LOAD_GLOBAL           1  'True'
           6  LOAD_GLOBAL           1  'True'
           9  LOAD_CONST            2  'default'
          12  LOAD_GLOBAL           2  'msgpackext'
          15  CALL_FUNCTION_513   513 
          18  RETURN_VALUE_LAMBDA
          -1  LAMBDA_MARKER    

Parse error at or near `CALL_FUNCTION_513' instruction at offset 15
if six.PY3:
    DECODE = --- This code section failed: ---

  20       0  LOAD_GLOBAL           0  'unpackb'
           3  LOAD_GLOBAL           1  'ext_hook'
           6  LOAD_CONST            2  'utf-8'
           9  LOAD_CONST            3  'ext_hook'
          12  LOAD_GLOBAL           1  'ext_hook'
          15  CALL_FUNCTION_513   513 
          18  RETURN_VALUE_LAMBDA
          -1  LAMBDA_MARKER    

Parse error at or near `CALL_FUNCTION_513' instruction at offset 15
else:
    DECODE = --- This code section failed: ---

  22       0  LOAD_GLOBAL           0  'unpackb'
           3  LOAD_GLOBAL           1  'ext_hook'
           6  LOAD_GLOBAL           1  'ext_hook'
           9  CALL_FUNCTION_257   257 
          12  RETURN_VALUE_LAMBDA
          -1  LAMBDA_MARKER    

Parse error at or near `CALL_FUNCTION_257' instruction at offset 9

class SpectateData(object):

    @staticmethod
    def is_spectate_detail_data_valid(spectate_data, now, extra_info):
        if not spectate_data:
            return False
        else:
            if spectate_data.get('battle_id') is None:
                return False
            if not SpectateData.is_spectate_data_time_valid(spectate_data, now, extra_info):
                return False
            return True

    @staticmethod
    def is_spectate_data_time_valid(spectate_data, now, extra_info):
        if not spectate_data or not now or not extra_info:
            return False
        else:
            delta_time = now - float(spectate_data.get('start_time', 0))
            need_delay = sp_const.SPECTATE_CLIENT_DELAY_TIME
            play_type = extra_info.get('play_type', None)
            if play_type not in battle_const.GLOBAL_SPECTATE_NO_PARACHUTE_DELAY_PLAY_TYPES:
                need_delay += sp_const.GLOBAL_SPECTATE_WAIT_PARACHUTE_MAX_TIME
            if delta_time <= need_delay or delta_time > 1800:
                return False
            return True

    @staticmethod
    def get_battle_cache_data--- This code section failed: ---

  63       0  BUILD_MAP_13         13 

  64       3  LOAD_GLOBAL           0  'tutil'
           6  LOAD_ATTR             1  'get_time'
           9  CALL_FUNCTION_0       0 
          12  LOAD_CONST            1  'start_time'
          15  STORE_MAP        

  65      16  STORE_MAP        
          17  STORE_MAP        
          18  STORE_MAP        
          19  STORE_MAP        

  66      20  LOAD_FAST             1  'stub_bin_mb'
          23  LOAD_CONST            3  'stub_mb'
          26  STORE_MAP        

  67      27  LOAD_GLOBAL           2  'str'
          30  LOAD_FAST             2  'battle'
          33  LOAD_ATTR             3  'id'
          36  CALL_FUNCTION_1       1 
          39  LOAD_CONST            4  'battle_id'
          42  STORE_MAP        

  68      43  LOAD_FAST             2  'battle'
          46  LOAD_ATTR             4  'get_battle_type'
          49  CALL_FUNCTION_0       0 
          52  LOAD_CONST            5  'battle_type'
          55  STORE_MAP        

  69      56  LOAD_FAST             2  'battle'
          59  LOAD_ATTR             5  'get_fighter_num'
          62  CALL_FUNCTION_0       0 
          65  LOAD_CONST            6  'left_player'
          68  STORE_MAP        

  70      69  LOAD_FAST             2  'battle'
          72  LOAD_ATTR             6  'get_battle_people_size'
          75  CALL_FUNCTION_0       0 
          78  LOAD_CONST            7  'total_player'
          81  STORE_MAP        

  71      82  LOAD_FAST             2  'battle'
          85  LOAD_ATTR             7  '_entity_type'
          88  LOAD_CONST            8  'battle_entity_type'
          91  STORE_MAP        

  72      92  LOAD_FAST             2  'battle'
          95  LOAD_ATTR             8  'get_map_id'
          98  CALL_FUNCTION_0       0 
         101  LOAD_CONST            9  'map_id'
         104  STORE_MAP        

  73     105  LOAD_FAST             2  'battle'
         108  LOAD_ATTR             9  'get_map_area_id'
         111  CALL_FUNCTION_0       0 
         114  LOAD_CONST           10  'map_area_id'
         117  STORE_MAP        

  74     118  LOAD_FAST             2  'battle'
         121  LOAD_ATTR            10  'get_battle_environment'
         124  CALL_FUNCTION_0       0 
         127  LOAD_CONST           11  'battle_environment'
         130  STORE_MAP        

  75     131  LOAD_FAST             2  'battle'
         134  LOAD_ATTR            11  'is_competition'
         137  CALL_FUNCTION_0       0 
         140  POP_JUMP_IF_FALSE   155  'to 155'
         143  LOAD_FAST             2  'battle'
         146  LOAD_ATTR            12  'get_room_competition_region'
         149  CALL_FUNCTION_0       0 
         152  JUMP_FORWARD          3  'to 158'
         155  LOAD_CONST            0  ''
       158_0  COME_FROM                '152'
         158  LOAD_CONST           12  'competition_region'
         161  STORE_MAP        

  76     162  LOAD_FAST             2  'battle'
         165  LOAD_ATTR            14  'get_battle_time_uid'
         168  CALL_FUNCTION_0       0 
         171  LOAD_CONST           13  'battle_time_uid'
         174  STORE_MAP        
         175  RETURN_VALUE     

Parse error at or near `STORE_MAP' instruction at offset 16

    @staticmethod
    def encode_dan_info(dan_info):
        survival_dan = dan_info.get('survival_dan', {})
        dan_short = [survival_dan.get('dan', 1), survival_dan.get('lv', 1), survival_dan.get('star', 1)]
        return dan_short

    @staticmethod
    def decode_dan_info(dan_short):
        if not dan_short:
            dan_short = [
             1, 1, 1]
        dan, dan_lv, dan_star = dan_short
        return {'survival_dan': {'dan': dan,'lv': dan_lv,'star': dan_star}}

    @staticmethod
    def get_soul_cache_dict(battle, soul, battle_cache_data, place_holder_uid=None):
        uid = place_holder_uid or soul.get_uid() if 1 else place_holder_uid
        role_id = soul.get_role()
        role_name = soul.get_name()
        role_fashion = soul.logic.ev_g_fashion()
        dan_info = soul.get_dan_info()
        recommend_key = soul.get_recommend_key()
        clan_id = soul.get_cid()
        rank_use_title_dict = soul.get_rank_use_title_dict()
        enable_be_spectated = place_holder_uid or soul.get_enable_be_spectated() if 1 else True
        dan_short = SpectateData.encode_dan_info(dan_info)
        brief_data = ENCODE((
         dan_short,
         battle_cache_data['competition_region'],
         battle_cache_data['battle_type'],
         battle_cache_data['start_time'],
         uid,
         role_name,
         role_fashion,
         enable_be_spectated))
        detail_data = {'uid': uid,
           'role_id': role_id,
           'role_name': role_name,
           'clan_id': clan_id,
           'role_fashion': json.dumps(role_fashion),
           'dan_info': json.dumps(dan_info),
           'rank_use_title_dict': json.dumps(rank_use_title_dict),
           'enable_be_spectated': enable_be_spectated,
           'battle_init_dict': battle.get_client_dict(soul, False),
           'soul_id': str(soul.id),
           'kill': 0,
           'damage': 0,
           'cur_likenum': 0,
           'total_likenum': soul.get_old_likenum(),
           'spectator_cnt': 0,
           'bat_spectator_cnt': soul.get_battle_spectator_num(),
           'match_score': soul.get_match_score()
           }
        detail_data['battle_init_dict']['battle_idx'] = 0
        detail_data['battle_init_dict']['parachute_stage'] = None
        detail_data['battle_init_dict'] = ENCODE(detail_data['battle_init_dict'])
        if recommend_key:
            detail_data['recommend_key'] = recommend_key
        detail_data.update(battle_cache_data)
        return (
         brief_data, detail_data)

    @staticmethod
    def decode_spectate_brief_data(encoded_brief_info):
        if not encoded_brief_info:
            return
        else:
            brief_data = DECODE(encoded_brief_info)
            if not brief_data:
                return
            player_uid, competition_region, short_dan = (None, 0, None)
            enable_be_spectated = None
            brief_data_len = len(brief_data)
            if brief_data_len == 5:
                battle_type, start_time, player_uid, role_name, role_fashion = brief_data
            else:
                if brief_data_len == 6:
                    competition_region, battle_type, start_time, player_uid, role_name, role_fashion = brief_data
                elif brief_data_len == 7:
                    short_dan, competition_region, battle_type, start_time, player_uid, role_name, role_fashion = brief_data
                elif brief_data_len == 8:
                    short_dan, competition_region, battle_type, start_time, player_uid, role_name, role_fashion, enable_be_spectated = brief_data
                dan_info = SpectateData.decode_dan_info(short_dan)
                if not player_uid:
                    return
            item_data = {'uid': int(player_uid),'role_name': role_name,
               'role_fashion': role_fashion,
               'start_time': start_time,
               'battle_type': battle_type,
               'competition_region': competition_region,
               'dan_info': dan_info,
               'enable_be_spectated': enable_be_spectated
               }
            return item_data

    @staticmethod
    def get_battle_init_data_for_ob(battle_data, battle, soul):
        battle_init_dict = battle.get_client_dict(soul, False)
        battle_init_dict['statistics'] = battle.get_statistics_data()
        battle_init_dict['all_player_info'] = battle.get_global_spectate_init_player_info_for_ob()
        battle_init_dict['flight_dict'] = battle.get_flight_client_dict()
        battle_init_dict['battle_idx'] = 0
        if battle_init_dict['flight_dict']:
            battle_init_dict['flight_dict']['start_timestamp'] = battle.get_prepare_timestamp()
        ob_battle_init_data = {'ob_uid_set': list(battle.get_ob_uid_set()),
           'battle_init_dict': ENCODE(battle_init_dict),
           'soul_id': str(soul.id)
           }
        ob_battle_init_data.update(battle_data)
        return ob_battle_init_data

    @staticmethod
    def get_battle_init_data_for_replay(battle, soul):
        battle_init_dict = battle.get_client_dict(soul, False)
        battle_init_dict['battle_idx'] = 0
        battle_init_dict['parachute_stage'] = None
        return {'battle_init_dict': battle_init_dict,
           'battle_entity_type': battle._entity_type,
           'battle_id': str(battle.id),
           'soul_id': str(soul.id)
           }