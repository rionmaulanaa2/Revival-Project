# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComRatRobotAppearance.py
from __future__ import absolute_import
from .ComExplosiveRobotAppearance import ComExplosiveRobotAppearance

class ComRatRobotAppearance(ComExplosiveRobotAppearance):

    def init_from_dict(self, unit_obj, bdict):
        super(ComRatRobotAppearance, self).init_from_dict(unit_obj, bdict)
        self.itype = bdict.get('npc_id', self.itype)