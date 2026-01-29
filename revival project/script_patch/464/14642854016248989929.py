# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/lobby_answering_system/LobbyASBaseWidget.py
from __future__ import absolute_import
from logic.gutils.lobby_click_interval_utils import global_unique_click

class LobbyASBaseWidget(object):

    def __init__(self, nd, parent):
        self.nd = nd
        self.parent = parent
        self.process_next_stage = parent.process_next_stage
        self.init_parameters()
        self.init_panel()
        self.process_event(True)
        if self.nd.btn_answer:

            @global_unique_click(self.nd.btn_answer)
            def OnClick(*args):
                self.on_click_btn_next()

    def init_parameters(self):
        pass

    def init_panel(self):
        pass

    def get_event_conf(self):
        return {}

    def process_event(self, flag):
        emgr = global_data.emgr
        econf = self.get_event_conf()
        func = emgr.bind_events if flag else emgr.unbind_events
        func(econf)

    def destroy(self):
        self.nd = None
        self.parent = None
        self.process_next_stage = None
        self.process_event(False)
        return

    def on_click_btn_next(self):
        pass

    def show(self):
        self.nd.setVisible(True)
        self.refresh_data()

    def refresh_data(self):
        pass

    def hide(self):
        self.nd.setVisible(False)