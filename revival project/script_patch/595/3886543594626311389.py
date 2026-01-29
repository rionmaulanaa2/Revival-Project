# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/map/map_widget/MapParachuteRangeWidget.py
from __future__ import absolute_import
from __future__ import print_function
from logic.comsys.map.map_widget import MapScaleInterface
from logic.gutils import map_utils
import math3d
from common import utilities
import math

class MapParachuteRangeWidget(MapScaleInterface.MapScaleInterface):

    def __init__(self, map_panel, parent_nd):
        super(MapParachuteRangeWidget, self).__init__(parent_nd, map_panel)
        self._nd = global_data.uisystem.load_template_create('battle_before/ccb_temp_range')
        self.parent_nd.AddChild('', self._nd, Z=2)
        map_dist = map_utils.get_map_dist()
        self.prev_mark_info = None
        self.init_radius = self._nd.nd_can_jump.GetContentSize()[1] / 2
        print('init radius is', self.init_radius)
        self.init_map_radius = self.init_radius * 1.0 / self.parent_nd.GetContentSize()[1] * map_dist
        print('init map radius is', self.init_map_radius, self.parent_nd.GetContentSize(), map_dist)
        print('cur map scale is', map_panel.cur_map_scale)
        self.init_event()
        self.update()
        self.update_timer_id = global_data.game_mgr.register_logic_timer(self.update, 1)
        return

    def init_event(self):
        self.map_panel.btn_launch.SetEnable(False)
        self.map_panel.btn_launch.BindMethod('OnClick', self.on_click_launch)
        global_data.emgr.net_login_reconnect_event += self.on_login_reconnect
        global_data.emgr.net_reconnect_event += self.on_login_reconnect

    def on_login_reconnect(self):
        global_data.game_mgr.unregister_logic_timer(self.update_timer_id)
        self.update_timer_id = global_data.game_mgr.register_logic_timer(self.update, 1)

    def on_click_launch(self, *args):
        if not self.prev_mark_info:
            return
        self.on_update()
        if not self.map_panel.btn_launch.IsEnable():
            return
        global_data.emgr.player_try_switch_parachute_stage.emit()

    def on_map_scale(self, map_scale):
        pass

    def destroy(self):
        self._nd = None
        global_data.game_mgr.unregister_logic_timer(self.update_timer_id)
        super(MapParachuteRangeWidget, self).destroy()
        return

    def update(self):
        if not (self._nd and self._nd.isValid()):
            return
        self._nd.setVisible(bool(self.on_update()))

    def on_update(self):
        battle = global_data.battle
        if not battle:
            return False
        player = global_data.cam_lplayer
        if not player:
            return False
        plane = battle.get_entity(battle.plane_id)
        if not (plane and plane.logic):
            return False
        plane = plane.logic
        pos = plane.ev_g_position()
        if not pos:
            return False
        airline_start_pos = plane.ev_g_airline_start_pos()
        self.set_world_position(airline_start_pos)
        airline_direction = plane.ev_g_plane_direction()
        default_direction = math3d.vector(1, 0, 0)
        radian2 = utilities.vect2d_radian(default_direction, airline_direction)
        degree2 = math.degrees(radian2)
        self._nd.setRotation(-degree2)
        self._nd.setVisible(True)
        cnt_radius = plane.ev_g_cnt_plane_radius()
        self._nd.setScale(cnt_radius * 1.0 / self.init_map_radius)
        mark_info = player.ev_g_warning_drawn_map_mark()
        if mark_info:
            self.prev_mark_info = mark_info
        else:
            mark_info = self.prev_mark_info
        can_launch = False
        if mark_info and battle.plane_started:
            mark_pos = mark_info['v3d_map_pos']
            can_launch = plane.ev_g_can_jump_to(mark_pos)
        self.map_panel.btn_launch.SetEnable(can_launch)
        return True