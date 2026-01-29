# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/mecha_display/mecha_memory/MechaMemoryStatMgr.py
from __future__ import absolute_import
from common.cfg import confmgr
import cc
from common.framework import Singleton
from common.cfg import confmgr

class MechaMemoryStatMgr(Singleton):
    ALIAS_NAME = 'mecha_memory_stat_mgr'

    def init(self):
        self.data = {}
        self.requesting_data = set()

    def on_finalize(self):
        self.data = {}
        self.requesting_data = set()

    def get_mecha_memory_data(self, uid, season):
        season = str(season)
        uid_season_data = self.data.get(self.get_season_key(uid, season), {})
        if uid_season_data:
            return uid_season_data
        else:
            return None
            return None

    def get_or_request_mecha_memory_data(self, uid, season):
        season_data = self.get_mecha_memory_data(uid, season)
        if season_data is None:
            key = self.get_season_key(uid, season)
            if key not in self.requesting_data:
                from logic.gutils.memory_utils import show_memory_data
                show_memory_data(season, uid)
                self.requesting_data.add(key)
            return
        else:
            return season_data
            return

    def received_mecha_memory_data(self, _id, data):
        if _id in self.requesting_data:
            self.requesting_data.remove(_id)
            self.data[_id] = data

    def invalidate_mecha_memory_cur_and_all_season_data(self):
        if not global_data.player:
            return
        from logic.gcommon.common_const.web_const import MECHA_MEMORY_ALL_SEASON_MODE
        cur_seasons = [global_data.player.get_battle_season(), MECHA_MEMORY_ALL_SEASON_MODE]
        for cur_season in cur_seasons:
            key = self.get_season_key(global_data.player.uid, cur_season)
            if key in self.data:
                del self.data[key]
            if key in self.requesting_data:
                self.requesting_data.remove(key)

    def get_season_key(self, uid, season):
        from logic.gutils.memory_utils import get_season_key
        return get_season_key(uid, season)