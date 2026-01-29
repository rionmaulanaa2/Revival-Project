# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComStatusSeatClient.py
from __future__ import absolute_import
from logic.gcommon.component.client.ComStatusMechaClient import ComStatusMechaClient
from ...cdata import mecha_status_config
from logic.gcommon.common_utils import status_utils
import time
import traceback

class ComStatusSeatClient(ComStatusMechaClient):

    def __init__(self):
        super(ComStatusSeatClient, self).__init__()

    def init_from_dict(self, unit_obj, bdict):
        super(ComStatusSeatClient, self).init_from_dict(unit_obj, bdict)
        self.seat_name = bdict.get('seat_name', '')
        _, seat_index = self.seat_name.split('_')
        self.seat_index = int(seat_index)

    def on_init_complete(self):
        npc_id = '{}_{}'.format(self.sd.ref_mecha_id, self.seat_index)
        self.send_event('E_SWITCH_BEHAVIOR', npc_id)