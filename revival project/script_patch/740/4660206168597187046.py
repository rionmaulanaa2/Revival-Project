# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComPveBoxLogic.py
from __future__ import absolute_import
from ..UnitCom import UnitCom
from logic.gutils import rogue_utils as r_u
from logic.gcommon import time_utility as tutil
from logic.gcommon.cdata import rogue_gift_config

class ComPveBoxLogic(UnitCom):
    BIND_EVENT = {'G_CHECK_ENTER_CONSOLOE_ZONE': '_check_enter_zone',
       'G_POSITION': '_get_pos'
       }

    def _get_pos(self):
        return self._pos

    def _check_enter_zone(self, pos):
        from logic.gcommon.common_const import battle_const
        if self._pos:
            start = self._pos
            radius = (pos - start).length
            if radius < battle_const.TRANSFER_PORTAL_MIN_DISTANCE_CHECK:
                return (True, radius)
        return (
         False, None)