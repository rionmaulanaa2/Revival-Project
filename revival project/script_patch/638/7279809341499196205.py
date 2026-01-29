# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComIsland.py
from __future__ import absolute_import
from logic.gcommon.component.UnitCom import UnitCom
from logic.gcommon.common_const.battle_const import MARK_DANGER, MARK_GOTO, MARK_NORMAL, MARK_RES, MARK_TYPE_TO_CLASS, MARK_CLASS_RES, MARK_CLASS_WARNING, MARK_CLASS_CNT, MARK_WAY_MAP, MARK_WAY_QUICK, MARK_WAY_DOUBLE_CLICK
from time import time
import math3d
from logic.gutils.map_utils import get_map_pos_from_world
from logic.gcommon.common_const.battle_const import MARK_CLASS_RES
from logic.gutils import map_utils
from common.utils.timer import CLOCK
from logic.gutils.ui_salog_utils import add_uiclick_add_up_salog

class ComIsland(UnitCom):
    BIND_EVENT = {'G_ISLAND_SET_ID': 'get_island_set_id'
       }

    def init_from_dict(self, unit_obj, bdict):
        super(ComIsland, self).init_from_dict(unit_obj, bdict)
        self._island_set_id = bdict.get('island_set_id', None)
        return

    def get_island_set_id(self):
        return self._island_set_id