# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/lobby/ExtNpk/ExtTipsWidget.py
from __future__ import absolute_import
from common.uisys.BaseUIWidget import BaseUIWidget
from logic.comsys.archive.archive_manager import ArchiveManager

class ExtTipsWidget(BaseUIWidget):

    def __init__(self, parent_ui, panel, panel_name, text_id=611491):
        super(ExtTipsWidget, self).__init__(parent_ui, panel)
        self._archive_data = ArchiveManager().get_archive_data('setting')
        need_show = self._archive_data.get_field(panel_name, True)
        self._archive_data.set_field(panel_name, False)
        self.panel.lab_tips.SetString(text_id)
        self.panel.lab_tips.setVisible(need_show)

        @self.panel.nd_touch.unique_callback()
        def OnClick(*args):
            vis = self.panel.lab_tips.isVisible()
            self.panel.lab_tips.setVisible(not vis)

    def destroy(self):
        self._archive_data = None
        super(ExtTipsWidget, self).destroy()
        return