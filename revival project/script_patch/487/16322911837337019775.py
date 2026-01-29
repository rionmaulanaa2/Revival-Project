# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/units/LHPBreakable.py
from __future__ import absolute_import
from logic.gcommon.component.Unit import Unit
from logic.gcommon.component.com_factory import component
from common.cfg import confmgr
import weakref
import math3d
import world
import time

@component(share=[
 'ComHealthSync'], client=[
 'ComClientSynchronizer',
 'ComHpBreakable'])
class LHPBreakable(Unit):
    TIME_LIMIT = 2

    def init_from_dict(self, bdict):
        super(LHPBreakable, self).init_from_dict(bdict)
        self.send_event('E_INIT_HP_MODEL', bdict.get('trans_info', None))
        return