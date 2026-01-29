# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/map/map_widget/MapVehicleMarkWidget.py
from __future__ import absolute_import
from __future__ import print_function
from logic.comsys.map.map_widget import MapScaleInterface
from common.utils.cocos_utils import ccp
from logic.gcommon.const import NEOX_UNIT_SCALE

class MapVehicleMarkWidget(MapScaleInterface.MapScaleInterface):

    def __init__(self, panel, parent_nd):
        super(MapVehicleMarkWidget, self).__init__(parent_nd, panel)
        self._nd = global_data.uisystem.load_template_create('map/ccb_map_mark')
        self.parent_nd.AddChild('', self._nd, Z=2)
        self._nd.setAnchorPoint(ccp(0.5, 0.5))
        self._nd.sp_mark.SetDisplayFrameByPath('', 'gui/ui_res_2/battle/map/icon_map_drive.png')
        self._nd.nd_distance.setVisible(False)
        self.on_update()
        self.timer_id = global_data.game_mgr.register_logic_timer(self.on_update, 50)

    def on_update(self):
        cam_lplayer = global_data.cam_lplayer
        if not self.map_panel.isVisible():
            return
        if not cam_lplayer:
            self._nd.setVisible(False)
            return
        if cam_lplayer.ev_g_death():
            self._nd.setVisible(False)
            return
        vehicle_id = cam_lplayer.ev_g_last_vehicle_id()
        if not vehicle_id:
            self._nd.setVisible(False)
            return
        from mobile.common.EntityManager import EntityManager
        target = EntityManager.getentity(vehicle_id)
        if not (target and target.logic):
            self._nd.setVisible(False)
            return
        print(cam_lplayer.ev_g_control_target(), target)
        if cam_lplayer.ev_g_control_target() is target:
            self._nd.setVisible(False)
            return
        position = target.logic.ev_g_position()
        if not position:
            self._nd.setVisible(False)
            return
        self._nd.setVisible(True)
        self.set_world_position(position)

    def destroy(self):
        global_data.game_mgr.unregister_logic_timer(self.timer_id)
        super(MapVehicleMarkWidget, self).destroy()