# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/client/const/player_battle_info_const.py
from __future__ import absolute_import
import six
_reload_all = True
RANK_MODE_SINGLE = '4'
RANK_MODE_DOUBLE = '5'
RANK_MODE_SQUAD = '6'
RANK_MODE_KOTH = '7'
CUSTOM_MODE_SINGLE = '11'
CUSTOM_MODE_DOUBLE = '12'
CUSTOM_MODE_SQUAD = '13'
CUSTOM_MODE_KOTH = '31'
CUSTOM_MODE_DEATH = '41'
RANK_MODE_DEATH = '42'
ALL_MODES = [
 RANK_MODE_SINGLE, RANK_MODE_DOUBLE, RANK_MODE_SQUAD, RANK_MODE_KOTH,
 CUSTOM_MODE_SINGLE, CUSTOM_MODE_DOUBLE, CUSTOM_MODE_SQUAD, CUSTOM_MODE_KOTH]
PLAY_TYPE_CHICKEN_MODES = set([])
PLAY_TYPE_DEATH_MODES = set([])

def get_chicken_modes():
    if PLAY_TYPE_CHICKEN_MODES:
        return PLAY_TYPE_CHICKEN_MODES
    else:
        from common.cfg import confmgr
        from logic.gcommon.common_const.battle_const import PLAY_TYPE_CHICKEN
        battle_conf = confmgr.get('battle_config')
        for k, v in six.iteritems(battle_conf):
            if v['play_type'] == PLAY_TYPE_CHICKEN:
                PLAY_TYPE_CHICKEN_MODES.add(int(k))

        return PLAY_TYPE_CHICKEN_MODES


def get_death_modes():
    if PLAY_TYPE_DEATH_MODES:
        return PLAY_TYPE_DEATH_MODES
    else:
        from common.cfg import confmgr
        from logic.gcommon.common_const.battle_const import PLAY_TYPE_DEATH
        battle_conf = confmgr.get('battle_config')
        for k, v in six.iteritems(battle_conf):
            if v['play_type'] == PLAY_TYPE_DEATH:
                PLAY_TYPE_DEATH_MODES.add(int(k))

        return PLAY_TYPE_DEATH_MODES