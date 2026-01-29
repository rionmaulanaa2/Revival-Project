# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/map/map_widget/MapRouteWidget.py
from __future__ import absolute_import
from six.moves import range
from logic.comsys.map.map_widget import MapScaleInterface
from mobile.common.EntityManager import EntityManager
from common.utils.cocos_utils import ccc4fFromHex
import cc

class MapRouteWidget(MapScaleInterface.MapScaleInterface):
    MIN_DRAW_LENGTH = 10
    MAX_POINT = 200
    DRAWING_COLOR = ccc4fFromHex(3894305791L)
    DISPLAY_COLOR = ccc4fFromHex(4118544639L)

    def __init__(self, panel, draw_layer, touch_callback):
        super(MapRouteWidget, self).__init__(draw_layer, panel)
        self.layer = draw_layer
        self.touch_poses = []
        self.points = []
        self.draw_end_callback = touch_callback
        self.line_width = MapScaleInterface.LINE_WIDTH
        self._valid_touch_id = None
        self.cam_lplayer_id = None
        self.showing_route_tid = 0
        self.init_widget()
        self.timer_id = global_data.game_mgr.register_logic_timer(self.on_update, 30)
        self.on_update()
        return

    def init_widget(self):
        self._draw_node = cc.DrawNode.create()
        self.layer.addChild(self._draw_node, 10, -1)
        if self.draw_end_callback:
            self.init_touch_event()
        else:
            self.set_enable_draw(False)

    def init_touch_event(self):
        self.layer.BindMethod('OnBegin', self.on_layer_touch_begin)
        self.layer.BindMethod('OnDrag', self.on_layer_touch_move)
        self.layer.BindMethod('OnEnd', self.on_layer_touch_end)
        self.set_enable_draw(False)

    def on_update(self):
        if self._valid_touch_id is not None:
            return
        else:
            lplayer = global_data.cam_lplayer
            if not lplayer:
                if self.points:
                    self.clear()
                return
            groupmates = lplayer.ev_g_groupmate() or {}
            recent_route_info = ([], 0)
            cam_lplayer_id = self.cam_lplayer_id
            for mate_id in groupmates:
                mate = EntityManager.getentity(mate_id)
                if not mate or not mate.logic:
                    continue
                mate = mate.logic
                mate_route = mate.ev_g_drawn_map_route()
                if mate_route is None:
                    continue
                if mate_route[1] > recent_route_info[1]:
                    recent_route_info = mate_route
                    cam_lplayer_id = mate.id

            self.cam_lplayer_id = cam_lplayer_id
            if recent_route_info[1] == 0:
                self.draw_line([])
                self.showing_route_tid = 0
            else:
                if recent_route_info[1] <= self.showing_route_tid:
                    return
                pts = [ cc.Vec2(p[0], p[1]) for p in recent_route_info[0] ]
                self.draw_line(pts)
                self.showing_route_tid = recent_route_info[1]
            return

    def on_layer_touch_begin(self, ui_obj, touch):
        if self._valid_touch_id is not None:
            return False
        else:
            self._valid_touch_id = touch.getId()
            self.clear()
            self.touch_poses.append(self._touch_point_to_map_pos(touch.getLocation()))
            return True

    def on_layer_touch_move(self, ui_obj, touch):
        if self._valid_touch_id is None:
            return
        else:
            point = touch.getLocation()
            last_point = self.touch_poses[-1]
            map_pos = self._touch_point_to_map_pos(point)
            diff_vec = cc.Vec2(map_pos)
            diff_vec.subtract(last_point)
            if diff_vec.getLength() > self.MIN_DRAW_LENGTH and len(self.touch_poses) < self.MAX_POINT:
                self.touch_poses.append(map_pos)
                self.draw_segment(last_point, map_pos, self.line_width)
            return

    def on_layer_touch_end(self, ui_obj, touch):
        if self._valid_touch_id is None:
            return
        else:
            self._valid_touch_id = None
            if self.draw_end_callback and callable(self.draw_end_callback):
                self.draw_end_callback(self.touch_poses)
                self.touch_poses = []
                self.on_update()
            return

    def set_enable_draw(self, enable):
        self.layer.SetEnableTouch(enable)
        if enable:
            self.layer.SetNoEventAfterMove(False)
        self.map_panel.sv_map.setTouchEnabled(not enable)

    def _touch_point_to_map_pos(self, touch_wpos):
        return self.layer.convertToNodeSpace(touch_wpos)

    def clear(self):
        self._draw_node.clear()
        self.touch_poses = []
        self.points = []
        self.showing_route_tid = 0
        self.cam_lplayer_id = None
        return

    def draw_segment(self, start, end, line_width):
        self._draw_node.drawSegment(start, end, line_width, cc.Color4F(1, 0.5, 0, 1))

    def draw_line(self, verts, color=cc.Color4F(1, 0, 0, 1)):
        self.clear()
        self.points = list(verts)
        for idx in range(0, len(verts) - 1):
            self._draw_node.drawSegment(verts[idx], verts[idx + 1], self.line_width, color)

    def on_map_scale(self, map_scale):
        self.line_width = MapScaleInterface.LINE_WIDTH * 1.0 / map_scale
        self._valid_touch_id = None
        self.draw_line(self.points)
        return

    def destroy(self):
        global_data.game_mgr.unregister_logic_timer(self.timer_id)
        super(MapRouteWidget, self).destroy()
        self.draw_end_callback = None
        self._valid_touch_id = None
        self.touch_poses = None
        self.points = None
        return