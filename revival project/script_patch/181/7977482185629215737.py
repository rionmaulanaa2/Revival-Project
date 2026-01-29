# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/ctypes/WpFist.py
from __future__ import absolute_import
from .Weapon import Weapon
from logic.gcommon.const import ATK_FIST

class WpFist(Weapon):

    def __init__(self, iItemnum):
        super(WpFist, self).__init__(iItemnum)
        self.iAtkMode = ATK_FIST
        self.id = 1

    def get_config(self, *args):
        if self._conf:
            return self._conf
        _conf = {}
        self._conf = _conf
        return self._conf