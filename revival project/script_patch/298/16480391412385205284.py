# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/units/LPvePortal.py
from __future__ import absolute_import
from logic.gcommon.component.Unit import Unit
from logic.gcommon.component.com_factory import component

@component(share=(), client=('ComClientSynchronizer', 'com_portal.ComSimplePortalCore',
                             'com_portal.ComSimplePortalCollision', 'com_portal.ComSimplePortalAppearance'))
class LPvePortal(Unit):

    def init_from_dict(self, bdict):
        super(LPvePortal, self).init_from_dict(bdict)