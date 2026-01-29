# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/pve/PVESurviveWidget.py
from __future__ import absolute_import
from logic.gcommon.common_utils.local_text import get_text_by_id

class PVESurviveWidget(object):
    TEMPLATE = 'pve/i_pve_defend_countdown'

    def __init__(self, panel):
        self.panel = panel
        self.init_params()
        self.init_widget()
        self.process_events(True)

    def init_params(self):
        self.widget = None
        return

    def process_events(self, is_bind):
        econf = {}
        global_data.emgr.bind_events(econf) if is_bind else global_data.emgr.unbind_events(econf)

    def clear(self):
        if self.widget:
            self.widget.setVisible(False)
            self.widget.Destroy()
        self.widget = None
        return

    def destroy(self):
        self.clear()
        self.init_params()
        self.process_events(False)
        self.panel = None
        return

    def init_widget(self):
        self.widget = global_data.uisystem.load_template_create(self.TEMPLATE, self.panel)
        self.widget.nd_hp.nd_prog.prog.SetPercent(100.0)

    def set_visible(self, vis):
        if not self.widget:
            return
        self.widget.nd_name.setVisible(vis)
        self.widget.nd_hp.setVisible(vis)

    def set_prog(self, s_prog, s_lab):
        if self.widget:
            self.widget.nd_hp.nd_prog.prog.SetPercent(s_prog)
            self.widget.nd_hp.lab_prog.SetString(get_text_by_id(633922).format(s_lab))