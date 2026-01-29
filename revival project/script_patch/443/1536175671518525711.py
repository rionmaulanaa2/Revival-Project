# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/lobby/EntryWidget/LobbyEntryWidgetBase.py
from __future__ import absolute_import
import six
from logic.gutils import activity_utils

class LobbyEntryWidgetBase(object):
    GLOBAL_EVENT = {}

    @classmethod
    def check_shown(cls, widget_type):
        if widget_type:
            player = global_data.player
            if not player:
                return False
            act_list = activity_utils.get_ordered_activity_list(widget_type)
            if act_list:
                return True
            return False
        return False

    def __init__(self, parent, panel, widget_id, widget_type):
        super(LobbyEntryWidgetBase, self).__init__()
        self.widget_id = widget_id
        self.widget_type = widget_type
        self.parent = parent
        self.panel = panel
        self._init_widget()

    def destroy(self):
        self._process_event(False)
        self.on_finalize_widget()

    def _init_widget(self):
        self.on_init_widget()
        self.refresh_red_point()
        self._process_event(True)

    def _process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {}
        for event, func_names in six.iteritems(self.GLOBAL_EVENT):
            if isinstance(func_names, str):
                func_names = (
                 func_names,)
            for func_name in func_names:
                func = getattr(self, func_name)
                if func and callable(func):
                    func_list = econf.setdefault(event, [])
                    func_list.append(func)

        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def on_init_widget(self):
        pass

    def on_finalize_widget(self):
        pass

    def refresh_red_point(self):
        pass

    def get_activity_list(self):
        return activity_utils.get_ordered_activity_list(self.widget_type)