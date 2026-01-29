# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/clan/ClanTaskList.py
from __future__ import absolute_import
from .ClanPageBase import ClanPageBase
from .ClanTaskBase import ClanTaskBase

class ClanTaskList(ClanTaskBase, ClanPageBase):

    def __init__(self, dlg):
        parent = global_data.ui_mgr.get_ui('ClanMainUI')
        ClanTaskBase.__init__(self, parent, None, None, dlg=dlg)
        ClanPageBase.__init__(self, dlg)
        self.init_widget()
        return

    def on_finalize_panel(self):
        ClanTaskBase.destroy(self)

    def init_widget(self):
        ClanTaskBase.init_widget(self, False)