# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/common/input/touch.py
from __future__ import absolute_import
from __future__ import print_function
import six
import game
TOUCH_EVENT_BEGAN = 0
TOUCH_EVENT_MOVED = 1
TOUCH_EVENT_ENDED = 2
TOUCH_EVENT_CANCELLED = 3
TOUCH_EVENT_DOUBLE_TAP = 7
TAP_THRESHOLD = 0.0

class TouchData(object):

    def __init__(self, event_type, touches, time):
        super(TouchData, self).__init__()
        self.event_type = event_type
        self.touches = touches
        self.time = time


class TouchManager(object):

    def __init__(self):
        global TAP_THRESHOLD
        from common.cfg import confmgr
        import cc
        self._event_listener = {}
        self._wheel_events = {}
        self._mouse_listener = None
        self._touch_listener = None
        self.cur_mouse_pos = cc.Vec2(0, 0)
        TAP_THRESHOLD = confmgr.get('setting', 'tap_threshold', defalut=TAP_THRESHOLD)

        def on_touches_began(touch, event):
            touches = (
             touch,)
            for cbs in six.itervalues(self._event_listener):
                cbs[0](touches, event)

            gds = global_data.game_mgr.gds
            if gds:
                gds.set_save_energy_mode(False)
            return True

        def on_touches_moved(touch, event):
            touches = (
             touch,)
            for cbs in six.itervalues(self._event_listener):
                cbs[1](touches, event)

            return True

        def on_touches_ended(touch, event):
            touches = (
             touch,)
            for cbs in six.itervalues(self._event_listener):
                cbs[2](touches, event)

            return True

        def on_touches_cancelled(touch, event):
            touches = (
             touch,)
            self._touch_dirty = True
            for cbs in six.itervalues(self._event_listener):
                cbs[3](touches, event)

            return True

        def on_mouse_wheel(msg, delta, key_state):
            self._touch_dirty = True
            for sid, cb in six.iteritems(self._wheel_events):
                cb(msg, delta, key_state)

        def on_mouse_move(event):
            wpos = event.getLocation()
            self.cur_mouse_pos = wpos

        from cocosui import cc
        if not self._touch_listener:
            et = cc.EventListenerTouchOneByOne.create()
            et.setOnTouchBeganCallback(on_touches_began)
            et.setOnTouchMovedCallback(on_touches_moved)
            et.setOnTouchEndedCallback(on_touches_ended)
            et.setOnTouchCancelledCallback(on_touches_cancelled)
            cc.Director.getInstance().getEventDispatcher().addEventListenerWithFixedPriority(et, 999999)
            self._touch_listener = et
        if not self._mouse_listener:
            self._mouse_listener = cc.EventListenerMouse.create()
            self._mouse_listener.setOnMouseMoveCallback(on_mouse_move)
            cc.Director.getInstance().getEventDispatcher().addEventListenerWithFixedPriority(self._mouse_listener, 99999)
        game.on_mouse_wheel = on_mouse_wheel
        return

    def register(self, sid, callbacks):
        global_data.game_mgr.post_exec(self._do_register, sid, callbacks)

    def _do_register(self, sid, callbacks):
        self._event_listener[sid] = callbacks

    def unregister(self, sid):
        global_data.game_mgr.post_exec(self._do_unregister, sid)

    def _do_unregister(self, sid):
        if sid in self._event_listener:
            self._event_listener.pop(sid)
        else:
            print('[WARNING] unregister touch event, cannot find key:', sid)

    def register_wheel(self, sid, callback):
        self._wheel_events[sid] = callback

    def unregister_wheel(self, sid):
        if sid in self._wheel_events:
            del self._wheel_events[sid]
        else:
            print('[WARNING] unregister wheel event, cannot find key:', sid)

    def unregister_all(self):
        self._event_listener = {}
        self._wheel_events = {}

    def disable_touch_event(self):
        if self._touch_listener:
            self._touch_listener.setEnabled(False)

    def enable_touch_event(self):
        if self._touch_listener:
            self._touch_listener.setEnabled(True)