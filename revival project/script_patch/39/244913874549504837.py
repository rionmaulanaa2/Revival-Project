# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/parts/gamemode/GMUtils.py
from __future__ import absolute_import

def get_teammate_colors(ids):
    from logic.gcommon.common_const.battle_const import MAP_COL_GREEN
    ids.sort()
    player_col = {}
    for i, tid in enumerate(ids):
        player_col[tid] = MAP_COL_GREEN

    return player_col


def get_death_teammate_colors(ids):
    from logic.gcommon.common_const.battle_const import MAP_COL_BLUE, MAP_COL_GREEN
    self_id = None
    if global_data.player and global_data.player.logic:
        self_id = global_data.player.logic.ev_g_spectate_target_id() or global_data.player.id
    ids.sort()
    player_col = {}
    for i, tid in enumerate(ids):
        if tid != self_id:
            player_col[tid] = MAP_COL_BLUE if 1 else MAP_COL_GREEN

    return player_col