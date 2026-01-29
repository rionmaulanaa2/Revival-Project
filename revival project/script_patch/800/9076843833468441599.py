# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComTriggerMineDriver.py
from __future__ import absolute_import
from .ComIgniteGrenadeDriver import ComIgniteGrenadeDriver

class ComTriggerMineDriver(ComIgniteGrenadeDriver):

    def __init__(self):
        super(ComTriggerMineDriver, self).__init__()
        self.scale_tag = False

    def upload_proto(self, pos, entity_id):
        self.send_event('E_CALL_SYNC_METHOD', 'trigger_grenade_explode', ((pos.x, pos.y, pos.z),), True)