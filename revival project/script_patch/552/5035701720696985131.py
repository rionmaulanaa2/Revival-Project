# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivitySimpleJump.py
from __future__ import absolute_import
from logic.comsys.activity.ActivityTemplate import ActivityBase
from common.cfg import confmgr
from logic.gutils import activity_utils
from logic.gutils import task_utils

class ActivitySimpleJump(ActivityBase):

    def __init__(self, dlg, activity_type):
        super(ActivitySimpleJump, self).__init__(dlg, activity_type)
        self.init_parameters()
        self.init_event()

    def on_finalize_panel(self):
        self.process_event(False)

    def init_parameters(self):
        pass

    def init_event(self):
        self.process_event(True)

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {}
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def refresh_panel(self):
        self.on_init_panel()

    def on_init_panel(self):
        self.panel.PlayAnimation('appear')
        data = confmgr.get('c_activity_config', self._activity_type, 'cUiData')
        btn_nd_name = data.get('btn_widget', '0')
        btn = getattr(self.panel, btn_nd_name, None)
        btn and btn.BindMethod('OnClick', lambda *args: self.btn_jump())
        return

    def btn_jump(self):
        from logic.gutils import jump_to_ui_utils
        from common.platform import is_win32
        data = confmgr.get('c_activity_config', self._activity_type, 'cUiData')
        func_name = data.get('func', 0)
        if is_win32():
            args = data.get('pc_args', []) if 1 else None
            args = args or data.get('args', [])
        if func_name:
            func = getattr(jump_to_ui_utils, func_name)
            func and func(*args)
        return