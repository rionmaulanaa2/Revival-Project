# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/parts/PoisonFixedRectManager.py
from __future__ import absolute_import
from . import PoisonDamageViewMgr

class PoisonFixedRectManager(object):

    def __init__(self):
        self._poison_damage_view = PoisonDamageViewMgr.PoisonDamageViewMgr(self)
        self.start_poison()

    def get_cnt_circle_info(self):
        return {}

    def is_in_poison(self):
        if not global_data.cam_lplayer or not global_data.cam_lplayer.is_valid():
            return
        else:
            pos = global_data.cam_lplayer.ev_g_position()
            if pos is None:
                return
            battle = global_data.battle
            if not battle:
                return
            born_data = global_data.game_mode.get_born_data()
            range_data = born_data[str(battle.area_id)].get('safe_range')
            min_x = min(range_data[0][0], range_data[1][0])
            max_x = max(range_data[0][0], range_data[1][0])
            min_z = min(range_data[0][1], range_data[1][1])
            max_z = max(range_data[0][1], range_data[1][1])
            return min_x <= pos.x <= max_x and min_z <= pos.z <= max_z

    def start_poison(self):
        self._poison_damage_view.start_check()

    def destroy(self):
        self._poison_damage_view and self._poison_damage_view.destroy()
        self._poison_damage_view = None
        return