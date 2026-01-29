# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/chart_ui/EndSettlementChartUIMapTouchLayerWidget.py
from __future__ import absolute_import
from __future__ import print_function
import six_ex
import cc
from common.utils.ui_utils import get_scale
from common.utils.cocos_utils import ccp

class EndSettlementChartUIMapTouchLayerWidget(object):

    def __init__(self, panel):
        super(EndSettlementChartUIMapTouchLayerWidget, self).__init__()
        self.map_panel = panel
        self._cur_touch_IDs = []
        self.touch_poses = {}
        self._touch_center = None
        self._cur_multi_touch = False
        self._touch_start_dist = 0
        self._touch_start_scale = 2
        self.init_scroll_touch_event()
        self.init_mouse_event()
        self.now_scale = 1
        return

    def destroy(self):
        self.map_panel = None
        return

    def __getattr__(self, name):
        print('[warning]touch layer name', name, 'may be map_panel attribute')
        return self.map_panel.__getattr__(name)

    def init_mouse_event(self):
        listener = cc.EventListenerMouse.create()
        listener.setOnMouseScrollCallback(self.on_mouse_scroll)
        cc.Director.getInstance().getEventDispatcher().addEventListenerWithSceneGraphPriority(listener, self.map_panel.panel.touch_layer.get())

    def on_mouse_scroll(self, event):
        dist = event.getScrollY() + event.getScrollX()
        if dist >= 0:
            magn = dist / 240.0 + 1
        else:
            magn = min(-60.0 / dist, 1)
        new_scale = self.calc_map_scale(magn)
        self.map_panel.cur_map_scale = new_scale
        wpos = event.getLocation()
        lpos = self.map_panel.panel.list_map.GetContainer().getParent().convertToNodeSpace(wpos)
        sz = self.map_panel.panel.list_map.GetInnerContentSize()
        zoom_anchor_x = lpos.x / sz.width
        zoom_anchor_y = lpos.y / sz.height
        self.set_map_scale_with_anchor(new_scale, zoom_anchor_x, zoom_anchor_y)

    def on_layer_touch_ended(self, layer, touch):
        tid = touch.getId()
        if tid in self._cur_touch_IDs:
            self._cur_touch_IDs.remove(tid)
            del self.touch_poses[tid]
        if len(self._cur_touch_IDs) <= 1:
            if not self.map_panel.panel.list_map.isTouchEnabled():
                if self.cur_map_draw_mode is None:
                    self.panel.list_map.setTouchEnabled(True)
                    layer.setSwallowTouch(False)
            self._touch_start_dist = 0
            self._touch_center = None
        return

    def on_layer_touch_begin(self, layer, touch):
        if len(self._cur_touch_IDs) >= 2:
            self._cur_multi_touch = True
            return False
        tid = touch.getId()
        touch_wpos = touch.getLocation()
        if tid not in self._cur_touch_IDs:
            self.touch_poses[tid] = touch_wpos
            self._cur_touch_IDs.append(tid)
        if len(self._cur_touch_IDs) >= 2:
            self.map_panel.panel.list_map.setTouchEnabled(False)
            layer.SetSwallowTouch(True)
            pts = six_ex.values(self.touch_poses)
            self._touch_center = ccp((pts[0].x + pts[1].x) / 2.0, (pts[0].y + pts[1].y) / 2.0)
            self._touch_start_dist = ccp(pts[0].x - pts[1].x, pts[0].y - pts[1].y).getLength()
            self._touch_start_scale = self.map_panel.list_map.GetContainer().getScale()
        else:
            layer.SetSwallowTouch(False)
        return True

    def on_layer_touch_drag(self, layer, touch):
        tid = touch.getId()
        touch_wpos = touch.getLocation()
        if tid not in self._cur_touch_IDs:
            return
        if len(self._cur_touch_IDs) >= 2:
            self.touch_poses[tid] = touch_wpos
            pts = six_ex.values(self.touch_poses)
            tmp_vec = cc.Vec2(pts[0])
            tmp_vec.subtract(pts[1])
            cur_dist = tmp_vec.getLength()
            start_dist = max(self._touch_start_dist, 1.0)
            magn = cur_dist / start_dist
            new_scale = magn * self._touch_start_scale
            new_scale = max(min(new_scale, 2), 1)
            sz = self.map_panel.panel.list_map.GetInnerContentSize()
            lpos = self.map_panel.panel.list_map.GetContainer().getParent().convertToNodeSpace(self._touch_center)
            zoom_anchor_x = lpos.x / sz.width
            zoom_anchor_y = lpos.y / sz.height
            self.set_map_scale_with_anchor(new_scale, zoom_anchor_x, zoom_anchor_y)

    def on_layer_touch_end(self, layer, touch):
        tid = touch.getId()
        if tid in self._cur_touch_IDs:
            self._cur_touch_IDs.remove(tid)
            del self.touch_poses[tid]
        if len(self._cur_touch_IDs) <= 1:
            self.map_panel.panel.list_map.setTouchEnabled(True)
            self._touch_start_dist = 0
            self._touch_center = None
        if len(self._cur_touch_IDs) == 0:
            if not self._cur_multi_touch:
                start_location = touch.getStartLocation()
                cnt_location = touch.getLocation()
                start_location.subtract(cnt_location)
                if start_location.getLength() < get_scale('20w'):
                    pass
            self._cur_multi_touch = False
        return

    def init_scroll_touch_event(self):
        touch_layer = self.map_panel.panel.touch_layer
        touch_layer.EnableDoubleClick(False)
        touch_layer.set_sound_enable(False)
        touch_layer.BindMethod('OnBegin', self.on_layer_touch_begin)
        touch_layer.BindMethod('OnDrag', self.on_layer_touch_drag)
        touch_layer.BindMethod('OnEnd', self.on_layer_touch_end)

    def set_map_scale_with_anchor(self, scale, zoom_anchor_x, zoom_anchor_y):
        self.map_panel.list_map.SetContainerScale(scale, zoom_anchor_x, zoom_anchor_y)
        for icon in self.map_panel.icon_container.GetAllItem():
            icon.setScale(1.0 / scale)

        for desc in self.map_panel.desc_container.GetAllItem():
            desc.setScale(1.0 / scale)

        self.now_scale = scale

    def calc_map_scale(self, magnify_value=2.5):
        new_scale = max(min(self.map_panel.list_map.GetContainer().getScale() * magnify_value, 2), 1)
        return new_scale