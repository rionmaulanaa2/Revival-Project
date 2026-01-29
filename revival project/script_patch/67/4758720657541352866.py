# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/battlemembers/impLevelMgr.py
from __future__ import absolute_import
from mobile.common.rpcdecorator import rpc_method, CLIENT_STUB
from mobile.common.RpcMethodArgs import Float, Dict, Int

class impLevelMgr(object):

    def _init_levelmgr_from_dict(self, bdict):
        self._major_level = bdict.get('major_level', 1)
        self._minor_level = bdict.get('minor_level', 0)
        self._difficulty = bdict.get('difficulty', 1)
        self._max_level = bdict.get('max_level', 0)
        self._confirm_enter_next_ids = bdict.get('confirm_enter_next_ids', [])
        self._confirm_enter_ts = bdict.get('confir_enter_ts', 0)

    def _init_levelmgr_completed(self, bdict):
        pass

    def _tick_levelmgr(self, delta):
        pass

    def _destroy_levelmgr(self, clear_cache):
        pass

    def try_enter_next_level(self):
        self._confirm_enter_next_ids.append(global_data.player.id)
        self.call_soul_method('try_enter_next_level', (self._minor_level,))

    @rpc_method(CLIENT_STUB, (Float('confirm_enter_ts'),))
    def on_confirm_enter_next_level(self, confirm_enter_ts):
        self._confirm_enter_ts = confirm_enter_ts
        show_self = global_data.player.id not in self._confirm_enter_next_ids
        global_data.emgr.pve_teleport_ts_event.emit(confirm_enter_ts, show_self)

    @rpc_method(CLIENT_STUB, (Int('confirm_cnt'), Int('alive_cnt')))
    def on_someone_confirm_enter(self, confirm_cnt, alive_cnt):
        global_data.emgr.pve_teammate_confirm_teleport.emit(confirm_cnt, alive_cnt)

    @rpc_method(CLIENT_STUB, (Int('major_level'), Int('minor_level'), Int('difficulty')))
    def on_enter_level(self, major_level, minor_level, difficulty):
        self._major_level = major_level
        self._minor_level = minor_level
        self._difficulty = difficulty
        self._confirm_enter_next_ids = []
        global_data.emgr.pve_enter_level_event.emit(self._major_level, self._minor_level, self._difficulty)

    def get_cur_pve_level--- This code section failed: ---

  50       0  LOAD_GLOBAL           0  'hasattr'
           3  LOAD_GLOBAL           1  '_save_init_bdict'
           6  CALL_FUNCTION_2       2 
           9  POP_JUMP_IF_TRUE     63  'to 63'

  51      12  LOAD_FAST             0  'self'
          15  LOAD_ATTR             1  '_save_init_bdict'
          18  LOAD_ATTR             2  'get'
          21  LOAD_CONST            2  'major_level'
          24  LOAD_CONST            3  ''
          27  CALL_FUNCTION_2       2 
          30  LOAD_FAST             0  'self'
          33  STORE_ATTR            3  '_major_level'

  52      36  LOAD_FAST             0  'self'
          39  LOAD_ATTR             1  '_save_init_bdict'
          42  LOAD_ATTR             2  'get'
          45  LOAD_CONST            4  'minor_level'
          48  LOAD_CONST            3  ''
          51  CALL_FUNCTION_2       2 
          54  LOAD_FAST             0  'self'
          57  STORE_ATTR            4  '_minor_level'
          60  JUMP_FORWARD          0  'to 63'
        63_0  COME_FROM                '60'

  53      63  LOAD_FAST             0  'self'
          66  LOAD_ATTR             3  '_major_level'
          69  POP_JUMP_IF_TRUE     81  'to 81'
          72  LOAD_FAST             0  'self'
          75  LOAD_ATTR             4  '_minor_level'
        78_0  COME_FROM                '69'
          78  POP_JUMP_IF_FALSE    97  'to 97'
          81  LOAD_FAST             0  'self'
          84  LOAD_ATTR             3  '_major_level'
          87  LOAD_FAST             0  'self'
          90  LOAD_ATTR             4  '_minor_level'
          93  BUILD_LIST_2          2 
          96  RETURN_END_IF    
        97_0  COME_FROM                '78'
          97  LOAD_CONST            0  ''
         100  RETURN_VALUE     

Parse error at or near `CALL_FUNCTION_2' instruction at offset 6

    def get_cur_pve_difficulty(self):
        return self._difficulty

    def get_max_level(self):
        return self._max_level