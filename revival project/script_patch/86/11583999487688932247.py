# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/survival/SurvivalBattleData.py
from __future__ import absolute_import
from common.framework import Singleton
from logic.client.const import game_mode_const
from common.utils import timer
from logic.comsys.battle.Death.DeathBattleUtils import pnpoly
from logic.comsys.archive import archive_key_const
from common.cfg import confmgr
from logic.gcommon.common_const.collision_const import GROUP_SHOOTUNIT
from logic.gcommon.const import NEOX_UNIT_SCALE
from logic.gcommon.common_const import collision_const
import math3d
import collision

class SurvivalBattleData(Singleton):
    ALIAS_NAME = 'survival_battle_data'
    ZERO_VECTOR = math3d.vector(0, 0, 0)

    def init(self):
        pass