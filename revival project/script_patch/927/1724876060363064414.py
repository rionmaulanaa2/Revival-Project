# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gutils/rocker_widget_utils.py
from __future__ import absolute_import
import time
import world
from common.utils.cocos_utils import ccp
from .rocker_utils import set_rocker_center_pos

class RockerWidget(object):

    def __init__(self, rocker_span_node, rocker_respond_layer, rocker_center_node):
        self.rocker_respond_layer = rocker_respond_layer
        self.rocker_span_node = rocker_span_node
        self.enable_drag = True
        self.rocker_center_node = rocker_center_node
        self.tick_cb = None
        self.init_parameters()
        self.init_rocker()
        return

    def destroy(self):

        @self.rocker_respond_layer.callback()
        def OnBegin(layer, touch):
            return False

        @self.rocker_respond_layer.callback()
        def OnDrag(layer, touch):
            pass

        @self.rocker_respond_layer.callback()
        def OnCancel(layer, touch):
            pass

        @self.rocker_respond_layer.callback()
        def OnEnd(layer, touch):
            pass

        self.rocker_respond_layer = None
        self.rocker_span_node = None
        self.rocker_center_node = None
        self._begin_callback = None
        self._drag_callback = None
        self._end_callback = None
        self.tick_cb = None
        self.btn_pushing = False
        return

    def check_can_operate(self):
        return True

    def init_parameters(self):
        self.touch_begin_pos = None
        self._begin_callback = None
        self._drag_callback = None
        self._end_callback = None
        self.is_rocker_enable = False
        self.btn_pushing = False
        self._tick_last_time = 0
        return

    def init_rocker(self):
        self.rocker_respond_layer.SetNoEventAfterMove(False)
        self.update_spawn_radius()
        self.rocker_center = self.rocker_span_node.ConvertToWorldSpacePercentage(50, 50)
        self.stop_btn()
        self.btn_pushing = False

        @self.rocker_respond_layer.callback()
        def OnBegin(layer, touch):
            if self.btn_pushing:
                return False
            else:
                self.btn_pushing = True
                world_pt = touch.getLocation()
                if self._begin_callback and callable(self._begin_callback):
                    ret = self._begin_callback(layer, touch)
                    if ret and self.rocker_respond_layer:
                        self.rocker_start(world_pt)
                        return True
                    return False
                return True

        @self.rocker_respond_layer.callback()
        def OnDrag(layer, touch):
            if self.enable_drag:
                touch_info = self.get_touch_info(touch)
                self.finger_move(touch_info)
                if self._drag_callback and callable(self._drag_callback):
                    self._drag_callback(layer, touch)

        @self.rocker_respond_layer.callback()
        def OnCancel(layer, touch):
            self.btn_pushing = False
            touch_info = self.get_touch_info(touch)
            self.rocker_center_node.setPosition(self.old_rocker_center_pos)
            self.finger_up(touch_info)
            if self._end_callback and callable(self._end_callback):
                self._end_callback(layer, touch)

        @self.rocker_respond_layer.callback()
        def OnEnd(layer, touch):
            self.btn_pushing = False
            self.rocker_center_node.setPosition(self.old_rocker_center_pos)
            if self._end_callback and callable(self._end_callback):
                self._end_callback(layer, touch)

        @self.rocker_respond_layer.callback()
        def OnDisableCancel(btn):
            self.btn_pushing = False
            self.rocker_center_node.setPosition(self.old_rocker_center_pos)

    def get_touch_info(self, touch):
        touch_info = {'pos': touch.getLocation(),
           'id': touch.getId(),
           'vec': touch.getDelta()
           }
        return touch_info

    def get_rocker_scale(self):
        return 1.5

    def rocker_start(self, pos):
        span_center = self.rocker_span_node.ConvertToWorldSpacePercentage(50, 50)
        npos = self.rocker_center_node.getParent().convertToNodeSpace(span_center)
        if not global_data.is_key_mocking_ui_event:
            self.rocker_center_node.setPosition(npos)
        self.touch_begin_pos = pos
        self.is_rocker_enable = True

    def stop_btn(self):
        self.rocker_center_node.SetPosition('50%', '50%')
        self.old_rocker_center_pos = self.rocker_center_node.getPosition()

    def finger_move(self, move_info):
        if not self.is_rocker_enable:
            return
        pt = move_info.get('pos')
        set_rocker_center_pos(pt, self.rocker_center, self.rocker_center_node, self.spawn_radius)

    def finger_up(self, touch_info):
        pass

    def stop_rocker(self):
        pass

    def update_spawn_radius(self):
        sz = self.rocker_span_node.getContentSize()
        scale = self.rocker_span_node.GetNodeToWorldScale()
        local_radius = 0.9 * (sz.width / 2.0) * scale.x
        self.spawn_radius = local_radius

    def set_begin_callback(self, func):
        self._begin_callback = func

    def set_drag_callback(self, func):
        self._drag_callback = func

    def set_end_callback(self, func):
        self._end_callback = func

    def get_spawn_radius(self):
        return self.spawn_radius

    def enable_rocker_tick(self, cb):
        self.tick_cb = cb
        self._tick_last_time = 0
        if cb:
            self.register_tick_timer()
        else:
            self.unregister_tick_timer()

    def register_tick_timer(self):
        import cc
        tag = 221206
        self.rocker_respond_layer.stopActionByTag(tag)
        _action = self.rocker_respond_layer.runAction(cc.RepeatForever.create(cc.Sequence.create([
         cc.DelayTime.create(0.01),
         cc.CallFunc.create(self.rocker_tick)])))
        _action.setTag(tag)

    def unregister_tick_timer(self):
        self.rocker_respond_layer.stopActionByTag(221206)

    def rocker_tick(self):
        if not self.is_rocker_enable:
            return
        if not self._tick_last_time:
            self._tick_last_time = time.time()
        else:
            cur_time = time.time()
            dt = cur_time - self._tick_last_time
            if self.tick_cb:
                self.tick_cb(dt)