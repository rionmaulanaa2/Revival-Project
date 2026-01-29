# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/common_const/water_const.py
from __future__ import absolute_import
from logic.gcommon.const import NEOX_UNIT_SCALE
from logic.gcommon.common_const.battle_const import BATTLE_SCENE_NORMAL, BATTLE_SCENE_KONGDAO
WATER_NONE = 1
WATER_SHALLOW_LEVEL = 2
WATER_SHWLLOW_LEVEL2 = 3
WATER_MID_LEVEL = 4
WATER_DEEP_LEVEL = 5
H_WATER_CRASH_NONE = 1.5
H_WATER_MECHA_DIVING = 4.0 * NEOX_UNIT_SCALE
H_WATER_MECHATRANS_DIVING = 3.0 * NEOX_UNIT_SCALE
WATER_HEIGHT = {BATTLE_SCENE_NORMAL: (0, 0.15, 0.7, 1.5),
   BATTLE_SCENE_KONGDAO: (0, 0.15, 0.7, 1.3)
   }