# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/avatarmembers/impDan.py
from __future__ import absolute_import
from mobile.common.RpcMethodArgs import Str, Dict, Int, Bool
from mobile.common.rpcdecorator import rpc_method, CLIENT_STUB
from logic.gcommon.cdata import dan_data
from common.cfg import confmgr

class impDan(object):

    def _init_dan_from_dict(self, bdict):
        self.dan_info = bdict.get('dan_info', {})
        self.history_max_dan = bdict.get('history_max_dan', {})
        self.dan_protect_num = bdict.get('dan_protect_num', {})
        self.season_max_dan = bdict.get('season_max_dan', {})
        self.fate_group_time = bdict.get('fate_group_time', 0)
        self.last_season_dan = bdict.get('last_season_dan', 1)
        self.last_battle_dan_info = {}

    def get_dan_info_by_type(self, dan_type):
        return self.dan_info.get(dan_type, {})

    def get_history_max_dan(self):
        return self.history_max_dan

    def get_season_max_dan(self):
        return self.season_max_dan

    def get_last_season_dan(self):
        return self.last_season_dan

    def get_dan_info(self):
        return self.dan_info

    def get_dan(self, dan_type):
        return self.get_dan_info_by_type(dan_type).get('dan', dan_data.BROZE)

    def get_dan_lv(self, dan_type):
        return self.get_dan_info_by_type(dan_type).get('lv', dan_data.get_lv_num(dan_data.BROZE))

    def get_dan_star(self, dan_type):
        return self.get_dan_info_by_type(dan_type).get('star', 0)

    def get_league_point(self, dan_type):
        return self.get_dan_info_by_type(dan_type).get('league_point', 0)

    def get_dan_protect_num(self, dan_type):
        return self.dan_protect_num.get(dan_type, 0)

    @rpc_method(CLIENT_STUB, (Str('dan_type'), Int('dan'), Int('lv'), Int('star'), Int('league_point'), Int('dan_protect_num'), Bool('is_init'), Dict('ext_info')))
    def update_dan_info(self, dan_type, dan, lv, star, league_point, dan_protect_num, is_init, ext_info):
        from logic.gutils import season_utils
        self.dan_info.setdefault(dan_type, {})
        dan_info = self.dan_info[dan_type]
        info = {'dan_type': dan_type,
           'dan': (
                 dan_info.get('dan', 1), dan),
           'lv': (
                dan_info.get('lv', 3), lv),
           'star': (
                  dan_info.get('star', 0), star),
           'league_point': (
                          dan_info.get('league_point', 0), league_point),
           'dan_protect_num': (
                             self.dan_protect_num.get(dan_type, 0), dan_protect_num),
           'ext_info': ext_info
           }
        if ext_info.get('game_id'):
            self.last_battle_dan_info = info
        dan_info['dan'] = dan
        dan_info['lv'] = lv
        dan_info['star'] = star
        dan_info['league_point'] = league_point
        self.dan_protect_num[dan_type] = dan_protect_num
        if dan_data.cmp_dan(dan_info, self.season_max_dan):
            self.season_max_dan = dan_info.copy()
        if ext_info.get('fate_group_point', 0) > 0:
            self.fate_group_time = 1
        season_utils.check_dan_frame_reward(info)

    def show_fight_end_advance(self, info, is_init):
        fight_end_disable = False
        ext_info = info.get('ext_info', {})
        battle_tid = ext_info.get('battle_type')
        if battle_tid:
            fight_end_disable = confmgr.get('battle_config', str(battle_tid), 'bFightEndDisable', default=False)
        if fight_end_disable:
            return

        def callback--- This code section failed: ---

 104       0  LOAD_CONST            1  ''
           3  LOAD_CONST            2  ('FightEndUI',)
           6  IMPORT_NAME           0  'logic.comsys.season.FightEndUI'
           9  IMPORT_FROM           1  'FightEndUI'
          12  STORE_FAST            0  'FightEndUI'
          15  POP_TOP          

 105      16  POP_TOP          
          17  PRINT_ITEM_TO    
          18  PRINT_ITEM_TO    
          19  LOAD_DEREF            0  'info'
          22  LOAD_CONST            4  'show_anim'
          25  LOAD_DEREF            1  'is_init'
          28  UNARY_NOT        
          29  CALL_FUNCTION_512   512 
          32  POP_TOP          

Parse error at or near `POP_TOP' instruction at offset 16

        self.add_advance_callback('FightEndUI', callback)

    def receive_season_dan_reward(self):
        self.call_server_method('receive_season_reward')

    @rpc_method(CLIENT_STUB, ())
    def reset_fate_group_time(self):
        self.fate_group_time = 0

    def get_fate_group_time(self):
        return self.fate_group_time

    def get_last_battle_dan_info(self):
        return self.last_battle_dan_info

    def clear_last_battle_dan_info(self):
        self.last_battle_dan_info = {}