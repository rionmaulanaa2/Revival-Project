# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/map/map_widget/MapParachuteCoverWidget.py
from __future__ import absolute_import
from logic.comsys.map.map_widget import MapScaleInterface
from common import utilities
import math
import math3d

class MapParachuteCoverWidget(MapScaleInterface.MapScaleInterface):

    def __init__(self, map_panel, parent_nd):
        super(MapParachuteCoverWidget, self).__init__(parent_nd, map_panel)
        self._nd = global_data.uisystem.load_template_create('battle_before/ccb_temp_cover')
        self.parent_nd.AddChild('', self._nd, Z=3)
        self._nd.setVisible(False)
        self._nd.setScale(10)
        self.update()
        self.update_timer_id = global_data.game_mgr.register_logic_timer(self.update, 1)

    def on_login_reconnect(self):
        global_data.game_mgr.unregister_logic_timer(self.update_timer_id)
        self.update_timer_id = global_data.game_mgr.register_logic_timer(self.update, 1)

    def on_map_scale(self, map_scale):
        self._nd.setScale(10)

    def destroy(self):
        self._nd = None
        global_data.game_mgr.unregister_logic_timer(self.update_timer_id)
        super(MapParachuteCoverWidget, self).destroy()
        return

    def update(self):
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
        airline_start_pos = plane.ev_g_airline_start_pos()
        self.set_world_position(airline_start_pos)
        airline_direction = plane.ev_g_plane_direction()
        default_direction = math3d.vector(1, 0, 0)
        radian2 = utilities.vect2d_radian(default_direction, airline_direction)
        degree2 = math.degrees(radian2)
        self._nd.setRotation(-degree2)
        self._nd.setVisible(True)