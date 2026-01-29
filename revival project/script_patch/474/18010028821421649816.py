# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/ctypes/HighlightMoment.py
from __future__ import absolute_import
from functools import cmp_to_key
_reload_all = True
from logic.gcommon.common_const import battle_const as bconst

class HighlightMoment(object):

    def __init__(self):
        self.start = 0
        self.end = 0
        self.kill_cnt = 0
        self.is_lore = False
        self.is_ai = False
        self.kill_info = []
        self.dead_types = set([])

    def init_from_dict(self, bdict):
        self.start = bdict.get('start', 0)
        self.end = bdict.get('end', 0)
        self.kill_cnt = bdict.get('kill_cnt', 0)
        self.is_lore = bdict.get('is_lore', False)
        self.is_ai = bdict.get('is_ai', False)
        self.kill_info = bdict.get('kill_info', [])
        for info in self.kill_info:
            self.dead_types.add(info[0])

    def get_client_dict(self):
        return {'start': self.start,
           'end': self.end,
           'kill_cnt': self.kill_cnt,
           'is_lore': self.is_lore,
           'is_ai': self.is_ai,
           'kill_info': self.kill_info
           }

    def add_kill_info(self, dead_type, kill_time, is_lore, is_ai):
        self.kill_cnt += 1
        self.kill_info.append([dead_type, kill_time, is_lore, is_ai])
        self.dead_types.add(dead_type)
        self.is_lore = self.is_lore or is_lore
        self.is_ai = self.is_ai and is_ai

    def set_lore(self):
        self.is_lore = True
        self.kill_info[-1][2] = True

    def remove_last_kill(self, cnt):
        remove_kill_st = self.kill_info[-cnt][1]
        self.kill_info = self.kill_info[:-cnt]
        self.kill_cnt -= cnt
        self.end = min(self.kill_info[-1][1] + 2, remove_kill_st)
        self.is_lore = False
        self.is_ai = False
        self.dead_types = set([])
        for dead_type, kill_time, is_lore, is_ai in self.kill_info:
            self.dead_types.add(dead_type)
            self.is_lore = self.is_lore or is_lore
            self.is_ai = self.is_ai and is_ai

    @classmethod
    def cmp_highlight_by_priority(cls, h1, h2):
        if h1.is_lore:
            return -1
        if h2.is_lore:
            return 1
        if h1.kill_cnt > h2.kill_cnt:
            return -1
        if h1.kill_cnt < h2.kill_cnt:
            return 1
        if h1.is_ai != h2.is_ai:
            if h1.is_ai:
                return 1
            if h2.is_ai:
                return -1
        for dead_type in bconst.SORT_KILL_TYPES:
            if dead_type in h1.dead_types:
                return -1
            if dead_type in h2.dead_types:
                return 1

        return 0

    @classmethod
    def cmp_highlight_by_time(cls, h1, h2):
        if h1.start < h2.start:
            return -1
        if h1.start > h2.start:
            return 1
        return 0


CUT_TIME_INTV_MAP = {6: (1, 1.5),
   5: (1.2, 2),
   4: (1.5, 2),
   3: (2, 2),
   2: (4, 2),
   1: (10, 2)
   }

def cut_highmoments_to_max_kill(total_kill, highlight_moments, extra_lore=False):
    if total_kill > bconst.HIGHLIGHT_MAX_KILL:
        last_highlight = highlight_moments[-1]
        last_highlight.remove_last_kill(total_kill - bconst.HIGHLIGHT_MAX_KILL)
    highlight_moments.sort(key=cmp_to_key(HighlightMoment.cmp_highlight_by_time))
    if extra_lore:
        if highlight_moments[-1].is_lore:
            highlight_moments[-1].end += 3.5
    return highlight_moments