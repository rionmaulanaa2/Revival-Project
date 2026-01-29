# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComBondGift.py
from __future__ import absolute_import
from ..UnitCom import UnitCom
from common.cfg import confmgr

class ComBondGift(UnitCom):
    BIND_EVENT = {}

    def __init__(self):
        super(ComBondGift, self).__init__(need_update=False)

    def init_from_dict(self, unit_obj, bdict):
        super(ComBondGift, self).init_from_dict(unit_obj, bdict)

    def on_post_init_complete(self, bdict):
        pass

    def destroy(self):
        super(ComBondGift, self).destroy()