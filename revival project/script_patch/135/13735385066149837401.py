# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/lobby/EntryWidget/OldLobbyEntryWidgetBase.py
from __future__ import absolute_import
from common.uisys.BaseUIWidget import BaseUIWidget
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gutils.lobby_click_interval_utils import global_unique_click
from logic.gutils import activity_utils

class OldLobbyEntryWidgetBase(BaseUIWidget):

    def __init__(self, parent_ui, panel, ui_config, event_conf):
        super(OldLobbyEntryWidgetBase, self).__init__(parent_ui, panel)
        self.ui_config = ui_config
        self.event_conf = event_conf
        self.init_widget()

    def destroy(self):
        self.process_event(False)
        super(OldLobbyEntryWidgetBase, self).destroy()

    def set_event_conf(self, conf):
        self.event_conf = conf

    def init_event(self):
        super(OldLobbyEntryWidgetBase, self).init_event()

    def process_event(self, is_bind):
        emgr = global_data.emgr
        if not self.event_conf:
            return
        if is_bind:
            emgr.bind_events(self.event_conf)
        else:
            emgr.unbind_events(self.event_conf)

    def init_widget(self):
        self._refresh_widget()
        self.process_event(True)
        self.refresh_red_point()

    def _get_entry_btn(self):
        entry_button_name = self.ui_config.get('entry_button_name')
        entry_btn = getattr(self.panel, entry_button_name) if entry_button_name else None
        return entry_btn

    def _refresh_widget(self):
        entry_btn = self._get_entry_btn()
        if not entry_btn:
            return
        if not self.is_activity_open():
            entry_btn.setVisible(False)
            return
        animation_name = self.ui_config.get('animation_name')
        if animation_name:
            self.panel.PlayAnimation(animation_name)
        for animation_name in self.ui_config.get('animation_names', []):
            self.panel.PlayAnimation(animation_name)

        entry_btn.setVisible(True)

        @global_unique_click(entry_btn)
        def OnClick(b, t):
            self.on_entry_btn_click(b, t)

    def on_refresh_activity(self):
        self._refresh_widget()

    def get_activity_list(self):
        return []

    def is_activity_open(self):
        if self.get_activity_list():
            return True
        return False

    def need_show_red_point(self):
        activity_list = self.get_activity_list()
        count = activity_utils.get_activity_red_point_count_by_activity_list(activity_list)
        if count > 0:
            return True
        return False

    def refresh_red_point(self, *args, **kargs):
        need_red_point = self.need_show_red_point()
        entry_btn = self._get_entry_btn()
        if entry_btn and entry_btn.isVisible() and entry_btn.red_point:
            entry_btn.red_point.setVisible(need_red_point)

    def on_entry_btn_click(self, btn, touch):
        ui_name = self.ui_config.get('ui_name')
        ui_path = self.ui_config.get('ui_path')
        if ui_name and ui_path and self.is_activity_open():
            global_data.ui_mgr.show_ui(ui_name, ui_path)
            self.refresh_red_point()
        else:
            global_data.game_mgr.show_tip(get_text_by_id(607177))
            btn.setVisible(False)

    def is_entry_visible(self):
        entry_btn = self._get_entry_btn()
        if entry_btn:
            return entry_btn.isVisible()
        return False