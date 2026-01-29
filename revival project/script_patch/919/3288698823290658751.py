# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/Counter.py
from __future__ import absolute_import
import six
import six_ex
from six.moves import range
from functools import cmp_to_key
from common.framework import SingletonBase
from collections import defaultdict
COUNT_FRAMES = 30

def default_empty():
    ret = [
     None] * COUNT_FRAMES
    for i in range(COUNT_FRAMES):
        ret[i] = {}

    return ret


class Counter(SingletonBase):

    def init(self):
        super(Counter, self).__init__()
        self._cur_idx = 0
        self.count_lists = defaultdict(default_empty)
        global_data.game_mgr.register_logic_timer(self.next_frame, 1)

    def on_finalize(self):
        pass

    def next_frame(self):
        self._cur_idx += 1
        if self._cur_idx >= COUNT_FRAMES:
            self._cur_idx = 0
        for count_list in six.itervalues(self.count_lists):
            count_list[self._cur_idx].clear()

    def record(self, category, key):
        i = self._cur_idx
        self.count_lists[category][i][key] = self.count_lists[category][i].get(key, 0) + 1

    def count(self, category):
        ret = {}
        for value_dict in self.count_lists[category]:
            for key, value in six.iteritems(value_dict):
                ret[key] = ret.get(key, 0) + value

        return sorted(six_ex.items(ret), reverse=True, key=cmp_to_key(--- This code section failed: ---

  54       0  LOAD_GLOBAL           0  'six_ex'
           3  LOAD_ATTR             1  'compare'
           6  LOAD_ATTR             1  'compare'
           9  BINARY_SUBSCR    
          10  LOAD_FAST             1  'y'
          13  LOAD_CONST            1  1
          16  BINARY_SUBSCR    
          17  CALL_FUNCTION_2       2 
          20  RETURN_VALUE_LAMBDA
          -1  LAMBDA_MARKER    

Parse error at or near `BINARY_SUBSCR' instruction at offset 9
))