# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/pve/ComPveStory.py
from __future__ import absolute_import
from common.cfg import confmgr
from logic.gcommon.component.UnitCom import UnitCom
from common.cfg import confmgr
from logic.gcommon.common_const import pve_const

class ComPveStory(UnitCom):
    BIND_EVENT = {'REQUEST_STOP_PVE_DIALOG': 'on_request_stop_pve_dialog',
       'G_IS_READING_DIALOG': '_is_reading_dialog'
       }

    def __init__(self):
        super(ComPveStory, self).__init__()
        self.reading_dialog = {}

    def _is_reading_dialog(self):
        return bool(self.reading_dialog)

    def init_from_dict(self, unit_obj, bdict):
        super(ComPveStory, self).init_from_dict(unit_obj, bdict)
        self.reading_dialog = bdict.get('reading_dialog', {})

    def on_init_complete(self):
        if self.reading_dialog:
            global_data.emgr.pve_start_read_dialog_event.emit(global_data.player.logic, self.reading_dialog)

    def on_request_stop_pve_dialog(self):
        self.reading_dialog = {}
        self.send_event('E_CALL_SYNC_METHOD', 'request_stop_pve_dialog', ())