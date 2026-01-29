# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/widget/ActivityWidgetBase.py
from __future__ import absolute_import
import six

class ActivityWidgetBase(object):
    GLOBAL_EVENT = {}

    def __init__(self, panel, activity_id, extra_conf=None):
        self.panel = panel
        self.activity_id = activity_id
        self.extra_conf = extra_conf or {}
        self.on_init_panel()
        self.process_global_event(True)

    def on_init_panel(self):
        pass

    def on_finalize_panel(self):
        self.process_global_event(False)
        self.panel = None
        return

    def process_global_event(self, is_bind):
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
            global_data.emgr.bind_events(econf)
        else:
            global_data.emgr.unbind_events(econf)