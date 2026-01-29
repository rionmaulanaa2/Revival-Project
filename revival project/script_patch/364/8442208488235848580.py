# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/map/map_widget/MapAirlineWidget.py
from __future__ import absolute_import
import six
from logic.comsys.map.map_widget import MapScaleInterface
import cc
import weakref
from logic.gutils.map_utils import get_map_uv
import math3d
AIRLINE_WIDTH = 2.5
AIRLINE_COLOR = cc.Color4F(1.0, 1.0, 1.0, 0.8)
DEFTAULT_SEG_LENGTH = 1000
from logic.gcommon.const import AIRLINE_AIRSHIP

class MapAirlineWidget(MapScaleInterface.MapScaleInterface):

    def __init__(self, panel, layer):
        super(MapAirlineWidget, self).__init__(panel.map_nd, panel)
        self.airlines = {}
        self.layer = layer
        self.init_airline_controller()
        self.init_widget()
        self.init_event()

    def init_airline_controller(self):
        map_mgr = self.map_panel.scene.get_sub_sys('PartMap', 'SysMapAirlineMgr')
        self.airline_mgr = weakref.ref(map_mgr)

    def on_map_scale(self, scale):
        self.refresh_airline()

    def refresh_airline(self, *args):
        self.clear()
        airline_mgr = self.airline_mgr()
        airline_map = airline_mgr.airline_map
        for k, v in six.iteritems(airline_map):
            self.generate_direct_line_seg(k, v[0], v[1])

    def generate_direct_line_seg(self, entity_id, start_pos, end_pos):
        direction = end_pos - start_pos
        direction_length = direction.length
        direction.normalize()
        seg_length = DEFTAULT_SEG_LENGTH / self.map_panel.cur_map_scale
        cnt_pos = start_pos
        cnt_length = 0
        world_segs = []
        while cnt_length < direction_length:
            world_segs.append([cnt_pos, cnt_pos + direction * (0.5 * seg_length)])
            cnt_pos = cnt_pos + direction * seg_length
            cnt_length += seg_length

        world_segs = self.make_airline_match_border(world_segs)
        content_size = self.parent_nd.GetContentSize()
        for v in world_segs:
            uv_start = get_map_uv(v[0])
            uv_end = get_map_uv(v[1])
            v[0] = cc.Vec2(content_size[0] * uv_start[0], content_size[1] * uv_start[1])
            v[1] = cc.Vec2(content_size[0] * uv_end[0], content_size[1] * uv_end[1])

        self.draw_airline(world_segs)

    def make_airline_match_border(self, segs):
        first_seg = segs[0]
        first_direction = first_seg[0] - first_seg[1]
        before_segs = self.generate_border_segs(first_seg[0], first_direction)
        end_seg = segs[-1]
        end_direction = end_seg[1] - end_seg[0]
        after_segs = self.generate_border_segs(end_seg[1], end_direction)
        before_segs.extend(segs)
        first_seg.extend(after_segs)
        return before_segs

    def generate_border_segs(self, start_pos, direction):
        next_start_pos = start_pos + direction
        cnt_u, cnt_v = get_map_uv(next_start_pos)
        ret_segs = []
        while 1.0 > cnt_u > 0:
            if 1.0 > cnt_v > 0:
                next_end_pos = next_start_pos + direction
                ret_segs.append([next_start_pos, next_end_pos])
                next_start_pos = next_end_pos + direction
                cnt_u, cnt_v = get_map_uv(next_start_pos)

        return ret_segs

    def draw_airline(self, segs):
        line_width = AIRLINE_WIDTH / self.map_panel.cur_map_scale
        for v in segs:
            self._draw_node.drawSegment(v[0], v[1], line_width, AIRLINE_COLOR)

    def init_event(self):
        global_data.emgr.scene_airline_changed_event += self.refresh_airline

    def destroy(self):
        self.clear()
        self.layer = None
        self._draw_node = None
        super(MapAirlineWidget, self).destroy()
        return

    def init_widget(self):
        self._draw_node = cc.DrawNode.create()
        self.layer.addChild(self._draw_node, 10, -1)

    def clear(self):
        self._draw_node.clear()