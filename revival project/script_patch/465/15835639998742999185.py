# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/Rank/RankData.py
from __future__ import absolute_import
from common.framework import Singleton

class RankData(Singleton):
    ALIAS_NAME = 'score_battle_rank_data'

    def init(self):
        self.init_parameters()

    def init_parameters(self):
        self.elimination_data = None
        self.brief_rank_data = None
        self.in_waring = False
        return

    def set_brief_rank_data(self, elimination_data, rank_data):
        self.elimination_data = elimination_data
        self.brief_rank_data = rank_data
        warning_rank = 0
        if elimination_data:
            warning_rank, _ = elimination_data
        for data in rank_data:
            rank, group_id, point = data
            if global_data.player and global_data.player.logic and global_data.player.logic.ev_g_group_id() == group_id:
                if warning_rank and rank > warning_rank:
                    self.in_warning = True
                else:
                    self.in_warning = False

    def im_in_waring_rank(self):
        return self.in_warning