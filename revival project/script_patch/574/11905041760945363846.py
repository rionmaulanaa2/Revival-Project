# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/battlemembers/impPosMarker.py
from __future__ import absolute_import
from mobile.common.rpcdecorator import rpc_method, CLIENT_STUB
from mobile.common.RpcMethodArgs import Str, Dict, Int
from common.utils.timer import CLOCK
from mobile.common.EntityManager import EntityManager
from math import ceil

class impPosMarker(object):
    DUR = 0.1
    MAX = 20

    def _init_posmarker_from_dict(self, bdict):
        self.clear_all_marker()
        self.pos_dict = {}
        self.timer_dict = {}

    def _init_posmarker_completed(self, bdict):
        pass

    def _tick_posmarker(self, delta):
        pass

    def _destroy_posmarker(self, clear_cache):
        self.clear_all_marker()

    def clear_all_marker--- This code section failed: ---

  31       0  LOAD_GLOBAL           0  'hasattr'
           3  LOAD_GLOBAL           1  'timer_dict'
           6  CALL_FUNCTION_2       2 
           9  POP_JUMP_IF_FALSE    82  'to 82'

  32      12  SETUP_LOOP           46  'to 61'
          15  LOAD_FAST             0  'self'
          18  LOAD_ATTR             1  'timer_dict'
          21  GET_ITER         
          22  FOR_ITER             35  'to 60'
          25  STORE_FAST            1  'eid'

  33      28  LOAD_FAST             0  'self'
          31  LOAD_ATTR             1  'timer_dict'
          34  LOAD_FAST             1  'eid'
          37  BINARY_SUBSCR    
          38  STORE_FAST            2  'timer_id'

  34      41  LOAD_GLOBAL           2  'global_data'
          44  LOAD_ATTR             3  'game_mgr'
          47  LOAD_ATTR             4  'unregister_logic_timer'
          50  LOAD_FAST             2  'timer_id'
          53  CALL_FUNCTION_1       1 
          56  POP_TOP          
          57  JUMP_BACK            22  'to 22'
          60  POP_BLOCK        
        61_0  COME_FROM                '12'

  35      61  BUILD_MAP_0           0 
          64  LOAD_FAST             0  'self'
          67  STORE_ATTR            1  'timer_dict'

  36      70  BUILD_MAP_0           0 
          73  LOAD_FAST             0  'self'
          76  STORE_ATTR            5  'pos_dict'
          79  JUMP_FORWARD          0  'to 82'
        82_0  COME_FROM                '79'

Parse error at or near `CALL_FUNCTION_2' instruction at offset 6

    def get_bias_aim_pos(self, eid, bias):
        if eid in self.pos_dict:
            idx = int(ceil(bias / self.DUR))
            if idx > len(self.pos_dict[eid]):
                return None
            return self.pos_dict[eid][-idx]
        else:
            self.reset_timer(eid)
            self.pos_dict[eid] = []
            self.timer_dict[eid] = global_data.game_mgr.register_logic_timer(self.tick_timer, self.DUR, (eid,), -1, CLOCK, False)
            return None
            return None

    def reset_timer(self, eid):
        timer_id = self.timer_dict.get(eid, None)
        if timer_id:
            global_data.game_mgr.unregister_logic_timer(timer_id)
            self.timer_dict.pop(eid)
            self.pos_dict.pop(eid)
        return

    def tick_timer(self, eid):
        if len(self.pos_dict[eid]) > self.MAX:
            self.pos_dict[eid].pop(0)
        target = EntityManager.getentity(eid)
        if target and target.logic:
            target_pos = target.logic.ev_g_position()
            self.pos_dict[eid].append(target_pos)
        else:
            self.pos_dict[eid].append(None)
        return