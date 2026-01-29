# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/map/map_widget/MapPoisonDirectionWidget.py
from __future__ import absolute_import
from logic.comsys.map.map_widget import MapScaleInterface
import cc

class MapPoisonDirectionWidget(MapScaleInterface.MapScaleInterface):

    def __init__(self, panel):
        super(MapPoisonDirectionWidget, self).__init__(panel.map_nd, panel)
        self.dir_widget = self.map_panel.map_nd.sv_safe_dir
        self.dir_widget.setTouchEnabled(False)
        self.start_map_pos = None
        self.end_map_pos = None
        self.content_height = self.dir_widget.getContentSize().height
        self.on_update()
        self.update_timer_id = global_data.game_mgr.register_logic_timer(self.on_update, 5)
        self.init_event()
        return

    def init_event(self):
        global_data.emgr.net_login_reconnect_event += self.on_reconnect

    def on_reconnect(self):
        global_data.game_mgr.unregister_logic_timer(self.update_timer_id)
        self.update_timer_id = global_data.game_mgr.register_logic_timer(self.on_update, 5)

    def show_direction(self, start_map_pos, end_map_pos):
        self.start_map_pos = start_map_pos
        self.end_map_pos = end_map_pos
        self.dir_widget.setVisible(True)
        self.update_direction()

    def hide_direction(self):
        self.start_map_pos = None
        self.end_map_pos = None
        if self.dir_widget:
            self.dir_widget.setVisible(False)
        return

    def on_update(self):
        cam_lplayer = global_data.cam_lplayer
        if not cam_lplayer:
            self.hide_direction()
            return
        if not self.map_panel:
            return
        poison_mgr = self.map_panel.poison_mgr()
        if not poison_mgr:
            return
        cnt_circle_data = poison_mgr.get_cnt_circle_info()
        position = cam_lplayer.ev_g_position() or cam_lplayer.ev_g_model_position()
        if not position:
            return
        if not cnt_circle_data or cnt_circle_data['level'] == 0 or not position:
            self.hide_direction()
            return
        safe_center = cnt_circle_data['safe_center']
        position.y = safe_center.y
        c_p_direction = safe_center - position
        c_p_length = c_p_direction.length
        if c_p_length - cnt_circle_data['safe_radius'] < 0 or c_p_length == 0 or cnt_circle_data['safe_radius'] == 0:
            self.hide_direction()
            return
        start_map_position = self.trans_world_position(position)
        c_p_direction.normalize()
        c_p_direction = c_p_direction * (c_p_length - cnt_circle_data['safe_radius'])
        round_pos = position + c_p_direction
        round_map_position = self.trans_world_position(round_pos)
        self.show_direction(start_map_position, round_map_position)

    def destroy(self):
        self.hide_direction()
        self.dir_widget = None
        global_data.game_mgr.unregister_logic_timer(self.update_timer_id)
        super(MapPoisonDirectionWidget, self).destroy()
        return

    def update_direction(self):
        if not (self.start_map_pos and self.end_map_pos):
            return
        self.update_widget_scale()
        start_map_pos = cc.Vec2(self.start_map_pos)
        diff_vec = cc.Vec2(self.end_map_pos)
        diff_vec.subtract(start_map_pos)
        lens = diff_vec.getLength()
        diff_vec.normalize()
        widget_scale = self.dir_widget.getScale()
        start_omit_length = 10
        diff_vec.scale(start_omit_length)
        start_map_pos.add(diff_vec)
        self.dir_widget.setPosition(start_map_pos)
        angle = diff_vec.getAngle()
        self.dir_widget.setRotation(-angle * 180 / 3.1415)
        actual_lens = (lens - start_omit_length) / widget_scale
        if actual_lens < 20:
            self.hide_direction()
            return
        self.dir_widget.SetContentSize(actual_lens, self.content_height)

    def update_widget_scale(self):
        self.dir_widget.setScale(1.0 / self.map_panel.cur_map_scale)

    def on_map_scale(self, scale):
        self.update_direction()