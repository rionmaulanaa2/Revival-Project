# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/manager_agents/TouchManagerAgent.py
from __future__ import absolute_import
from logic.manager_agents import ManagerAgentBase
from common.input import touch

class TouchManagerAgent(ManagerAgentBase.ManagerAgentBase):
    ALIAS_NAME = 'touch_mgr_agent'

    def init(self, *args):
        super(TouchManagerAgent, self).init()
        self.touch = touch.TouchManager()

    def get_cursor_pos(self):
        return self.touch.cur_mouse_pos

    def register_touch_event(self, sid, callbacks):
        self.touch.register(sid, callbacks)

    def unregister_touch_event(self, sid):
        self.touch.unregister(sid)

    def unregister_touch_event_all(self):
        self.touch.unregister_all()

    def register_wheel_event(self, sid, callback):
        self.touch.register_wheel(sid, callback)

    def unregister_wheel_event(self, sid):
        self.touch.unregister_wheel(sid)

    def disable_touch_event(self):
        self.touch.disable_touch_event()

    def enable_touch_event(self):
        self.touch.enable_touch_event()