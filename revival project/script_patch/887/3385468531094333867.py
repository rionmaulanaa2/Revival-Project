# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/avatarmembers/impCharm.py
from __future__ import absolute_import
from logic.gcommon.cdata import charm_data
from logic.gcommon.item import lobby_item_type as litem_type

class impCharm(object):

    def _init_charm_from_dict(self, bdict):
        self.charm = bdict.get('charm', 0)

    def update_charm(self, item_num, item_type, degree):
        self.charm += item_num * charm_data.get_charm(item_type, degree)

    def get_charm_value(self):
        return self.charm