# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/parts/battleprepare/PveBattlePrepare.py
from __future__ import absolute_import
from .BattlePrepare import BattlePrepareBase

class PveEditBattlePrepare(BattlePrepareBase):

    def __init__(self, parent):
        super(PveEditBattlePrepare, self).__init__(parent)
        self.init_mgr()

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {}
        econf.update(self.get_event_conf())
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def init_mgr(self):
        pass

    def on_exit(self):
        super(PveEditBattlePrepare, self).on_exit()


class PveBattlePrepare(BattlePrepareBase):

    def __init__(self, parent):
        super(PveBattlePrepare, self).__init__(parent)
        self.init_mgr()

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {}
        econf.update(self.get_event_conf())
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def init_mgr(self):
        pass

    def on_exit(self):
        super(PveBattlePrepare, self).on_exit()