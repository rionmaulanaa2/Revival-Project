# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComParadropCollision.py
from __future__ import absolute_import
from ..UnitCom import UnitCom
import math3d
from logic.gcommon.common_const.collision_const import GROUP_CHARACTER_INCLUDE, GROUP_SHOOTUNIT
import collision
from .ComCommonShootCollision import ComCommonShootCollision

class ComParadropCollision(ComCommonShootCollision):

    def __init__(self):
        super(ComParadropCollision, self).__init__()

    def init_from_dict(self, unit_obj, bdict):
        super(ComParadropCollision, self).init_from_dict(unit_obj, bdict)

    def _check_shoot_info(self, begin, pdir):
        idx = self.ev_g_shoot_part(begin, pdir)
        if idx is not None:
            pass
        return idx