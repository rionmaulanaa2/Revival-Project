# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/avatarmembers/impTown.py
from __future__ import absolute_import
from mobile.common.EntityManager import EntityManager

class impTown(object):

    def _init_town_from_dict(self, bdict):
        self._town_id = None
        return

    def get_town(self):
        if not self._town_id:
            return None
        else:
            battle = EntityManager.getentity(self._town_id)
            return battle

    def quit_town(self):
        self._town_id = None
        return

    def enter_town(self, town_id):
        self._town_id = town_id