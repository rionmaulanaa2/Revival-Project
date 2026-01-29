# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/role_profile/VoiceWrapWidget.py
from __future__ import absolute_import
from common.uisys.BaseUIWidget import BaseUIWidget
import cc
from copy import copy
from .VoiceWidget import VoiceWidget

class VoiceWrapWidget(BaseUIWidget):

    def __init__(self, parent, panel):
        self.global_events = {}
        super(VoiceWrapWidget, self).__init__(parent, panel)
        self.role_id = 0
        self._ui_role_id = 0
        self.widget = VoiceWidget(self, getattr(self.panel, 'temp_voice'))

    def show_panel(self, flag):
        self.panel.setVisible(flag)

    def on_hide(self):
        global_data.ui_mgr.close_ui('GameRuleDescUI')
        self.widget.on_parent_hide()

    def destroy(self):
        if self.widget:
            self.widget.destroy()
            self.widget = None
        super(VoiceWrapWidget, self).destroy()
        return

    def set_role_id(self, role_id):
        self.role_id = role_id
        self.widget.set_role_id(role_id)
        global_data.ui_mgr.close_ui('GameRuleDescUI')

    def refresh_all_content(self, update_data_only=False):
        self._ui_role_id = self.role_id
        if not update_data_only:
            self.widget.refresh_all_content()

    def on_dress_change(self, new_skin_id):
        self.refresh_all_content()

    def get_preview_skin_id(self):
        return self.parent.get_preview_skin_id()