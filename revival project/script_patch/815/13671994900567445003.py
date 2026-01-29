# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/map/map_widget/MapStartAirlineWidget.py
from __future__ import absolute_import
from logic.comsys.map.map_widget import MapScaleInterface
import cc
from logic.entities.Battle import Battle
import math3d

class MapStartAirlineWidget(MapScaleInterface.MapScaleInterface):

    def __init__(self, panel):
        super(MapStartAirlineWidget, self).__init__(panel.map_nd, panel)
        self.dir_widget = self.map_panel.map_nd.sv_safe_dir4
        self.dir_widget.setTouchEnabled(False)
        self.start_map_pos = None
        self.end_map_pos = None
        self.content_height = self.dir_widget.getContentSize().height
        self.init_event()
        self.init_status()
        return

    def init_status(self):
        if global_data.battle:
            status = global_data.battle.battle_status
            self.on_battle_status_changed(status)

    def init_event(self):
        global_data.emgr.net_login_reconnect_event += self.on_reconnect
        global_data.emgr.on_battle_status_changed += self.on_battle_status_changed

    def on_reconnect(self):
        if global_data.battle:
            status = global_data.battle.battle_status
            if status in [Battle.BATTLE_STATUS_PREPARE, Battle.BATTLE_STATUS_PARACHUTE]:
                self.on_battle_status_changed(Battle.BATTLE_STATUS_PREPARE)
            else:
                self.hide_direction()

    def on_battle_status_changed(self, status):
        if status in [Battle.BATTLE_STATUS_PREPARE, Battle.BATTLE_STATUS_PARACHUTE]:
            if global_data.battle:
                flight_dict = global_data.battle.flight_dict
                if flight_dict and 'start_pos' in flight_dict:
                    st_pos = math3d.vector(*flight_dict['start_pos'])
                    ed_pos = math3d.vector(*flight_dict['end_pos'])
                    self.show_direction_by_world_pos(st_pos, ed_pos)
        else:
            self.hide_direction()

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

    def show_direction_by_world_pos(self, start, end):
        start_map_position = self.trans_world_position(start)
        round_map_position = self.trans_world_position(end)
        self.show_direction(start_map_position, round_map_position)

    def destroy(self):
        self.hide_direction()
        self.dir_widget = None
        super(MapStartAirlineWidget, self).destroy()
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