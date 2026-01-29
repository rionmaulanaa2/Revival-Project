# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/map/map_widget/MapMarkDirection.py
from __future__ import absolute_import
from six.moves import range
from logic.comsys.map.map_widget import MapScaleInterface
import cc
from common.utils.ui_utils import get_vec2_distance_square
import math
DEFTAULT_SEG_LENGTH = 20.0
MAX_VEC_COUNT = 40
LINE_WIDTH = 1.5
DISPLAY_LENGTH = 25
EPSILON_LENGTH = 0.01

class MapMarkDirection(MapScaleInterface.MapScaleInterface):

    def __init__(self, ctrl_widget, direction_color):
        map_panel = ctrl_widget.map_panel
        super(MapMarkDirection, self).__init__(map_panel.map_nd, map_panel)
        self.layer = map_panel.map_nd.draw_layer
        self.seg_caches = [ [ cc.Vec2(0, 0) for i in range(0, MAX_VEC_COUNT) ] for j in range(0, 2) ]
        self.seg_caches_len = MAX_VEC_COUNT
        self.init_widget()
        self.color = direction_color
        self.start_pos = None
        self.end_pos = None
        self.direction_hidden = False
        return

    def init_widget(self):
        self._draw_node = cc.DrawNode.create()
        self.layer.addChild(self._draw_node, 10, -1)

    def destroy(self):
        self._draw_node.clear()
        self._draw_node.removeFromParent()
        self.layer = None
        self.seg_caches = None
        super(MapMarkDirection, self).destroy()
        return

    def update_direction_pos(self, player, start_pos, end_pos):
        if self.end_pos and start_pos and end_pos:
            distance_sq_end_pos = get_vec2_distance_square(end_pos, self.end_pos)
            distance_sq_start_pos = get_vec2_distance_square(start_pos, self.start_pos)
            if distance_sq_end_pos < 4.0 and distance_sq_start_pos < 4.0:
                return
        self.start_pos = start_pos
        self.direction_hidden = player.ev_g_mark_reached()
        self.end_pos = end_pos
        self.refresh_direction_line(player)

    def clear(self):
        self._draw_node.clear()

    def refresh_direction_line(self, player=None, force=False):
        self.clear()
        if self.direction_hidden or not (self.start_pos and self.end_pos):
            return
        distance_sqr = get_vec2_distance_square(self.start_pos, self.end_pos)
        if player and distance_sqr < DISPLAY_LENGTH ** 2:
            self.direction_hidden = True
            player.send_event('E_SET_MARK_REACHED', True)
            return
        self.generate_direct_line_seg(self.start_pos, self.end_pos, math.sqrt(distance_sqr))

    def on_map_scale(self, scale):
        self.refresh_direction_line(None, True)
        return

    def generate_direct_line_seg(self, start_pos, end_pos, distance):
        seg_length = DEFTAULT_SEG_LENGTH / self.map_panel.cur_map_scale
        start_x, start_y = start_pos.x, start_pos.y
        end_x, end_y = end_pos.x, end_pos.y
        delta_x, delta_y = (end_x - start_x) / distance * seg_length, (end_y - start_y) / distance * seg_length
        half_delta_x, half_delta_y = delta_x * 0.5, delta_y * 0.5
        cnt_distance = 0
        cnt_index = 0
        while cnt_distance < distance:
            if cnt_index >= self.seg_caches_len:
                self.seg_caches[0].append(cc.Vec2(0, 0))
                self.seg_caches[1].append(cc.Vec2(0, 0))
                self.seg_caches_len += 1
            cnt_start_pos = self.seg_caches[0][cnt_index]
            cnt_start_pos.x, cnt_start_pos.y = start_x, start_y
            cnt_end_pos = self.seg_caches[1][cnt_index]
            if distance - cnt_distance < seg_length:
                cnt_end_pos.x = end_x
                cnt_end_pos.y = end_y
                cnt_index += 1
                break
            start_x += delta_x
            start_y += delta_y
            cnt_end_pos.x, cnt_end_pos.y = start_x, start_y
            cnt_distance += seg_length * 1.5
            start_x += half_delta_x
            start_y += half_delta_y
            cnt_index += 1

        self.draw_line(cnt_index)

    def draw_line(self, seg_count):
        line_width = LINE_WIDTH * 1.0 / self.map_panel.cur_map_scale
        start_poses = self.seg_caches[0]
        end_poses = self.seg_caches[1]
        for v in range(0, seg_count):
            self._draw_node.drawSegment(start_poses[v], end_poses[v], line_width, self.color)