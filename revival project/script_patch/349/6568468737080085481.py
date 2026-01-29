# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/pve/PVEMechaRadarWidget.py
from __future__ import absolute_import
from six.moves import range
from common.utils.cocos_utils import neox_pos_to_cocos, ccp
from data.camera_state_const import FREE_MODEL
from logic.gcommon.common_const.ui_operation_const import PVE_MECHA_RADAR, PVE_MECHA_RADAR_NONE, PVE_MECHA_RADAR_2D, PVE_MECHA_RADAR_3D
import math3d
import six_ex
import world
import cc
MAX_ITEM_COUNT = 5

class PVEMechaRadarWidget(object):
    _2D_TEMPLATE = 'battle/sound_main'
    _3D_TEMPLATE = 'battle/sound_3d_main'

    def __init__(self, panel):
        self._panel = panel
        self.init_params()
        self.init_widget()
        self.init_camera()
        self.init_event()

    def init_params(self):
        self._2d_widget = None
        self._3d_widget = None
        self._2d_panel_items_dict = {}
        self._3d_panel_items_dict = {}
        self._setting = PVE_MECHA_RADAR_NONE
        self._scene = None
        self._player = None
        self._last_camera_pos = None
        self._camera = None
        self._cam_manager = None
        return

    def init_widget(self):
        self._init_2d_widget()
        self._init_3d_widget()
        self._scene = world.get_active_scene()
        self._player = None
        if self._scene:
            self.player_change(self._scene.get_player())
        return

    def _init_2d_widget(self):
        self._2d_widget = global_data.uisystem.load_template_create(self._2D_TEMPLATE, self._panel)
        self._2d_widget.itemtemp.setVisible(False)
        scale = 0.9
        self._2d_widget.setScaleX(scale)
        self._2d_widget.setScaleY(scale)
        item_conf = global_data.uisystem.load_template('battle/sound_item')
        for index in range(MAX_ITEM_COUNT):
            item = global_data.uisystem.create_item(item_conf, parent=self._2d_widget)
            item.setAnchorPoint(ccp(0.5, 0))
            sector_index = index + 2
            self._2d_panel_items_dict[sector_index] = item
            angle = 270 - 45 * (sector_index - 2)
            item.setRotation(angle)
            item.SetEnableCascadeOpacityRecursion(True)
            item.setVisible(False)
            item.img_sound.SetDisplayFrameByPath('', 'gui/ui_res_2/battle/sound/icon_machine.png')

    def _init_3d_widget(self):
        self._3d_widget = global_data.uisystem.load_template_create(self._3D_TEMPLATE, self._panel)
        self._3d_widget.itemtemp.setVisible(False)
        scale = 0.9
        self._3d_widget.nd_perspective.setScaleX(scale)
        self._3d_widget.nd_perspective.setScaleY(scale)
        item_conf = global_data.uisystem.load_template('battle/i_sound_3d')
        for index in range(MAX_ITEM_COUNT):
            item = global_data.uisystem.create_item(item_conf, parent=self._3d_widget.nd_perspective)
            item.setAnchorPoint(ccp(0.5, 0.5))
            sector_index = index + 2
            self._3d_panel_items_dict[sector_index] = item
            angle = 270 - 45 * (sector_index - 2)
            item.setRotation(angle)
            item.SetEnableCascadeOpacityRecursion(True)
            item.setVisible(False)
            item.img_mech.setVisible(True)

    def init_event(self):
        global_data.emgr.scene_camera_switch_player_setted_event += self.on_player_setted
        global_data.emgr.camera_switch_to_state_event += self.on_camera_state

    def init_camera(self):
        self._camera = global_data.game_mgr.scene.active_camera
        com_camera = global_data.game_mgr.scene.get_com('PartCamera')
        if com_camera:
            self._cam_manager = com_camera.cam_manager

    def on_player_setted(self):
        lplayer = global_data.cam_lplayer
        if lplayer:
            self.player_change(lplayer)

    def player_change(self, lplayer):
        self._player = lplayer
        if not self._player:
            for item in six_ex.values(self._2d_panel_items_dict):
                item.setVisible(False)

            for item in six_ex.values(self._3d_panel_items_dict):
                item.setVisible(False)

    def refresh_visible(self, has_monster_sector_set=[]):
        if self._setting == PVE_MECHA_RADAR_NONE:
            return
        if self._setting == PVE_MECHA_RADAR_2D:
            for sector, item in six_ex.items(self._2d_panel_items_dict):
                if sector in has_monster_sector_set:
                    item.setVisible(True)
                else:
                    item.setVisible(False)

        elif self._setting == PVE_MECHA_RADAR_3D:
            for sector, item in six_ex.items(self._3d_panel_items_dict):
                if sector in has_monster_sector_set:
                    item.setVisible(True)
                else:
                    item.setVisible(False)

    def reset_center_positon(self):
        if not self._3d_widget:
            return
        if not self._cam_manager or not self._camera:
            self.init_camera()
        camera_posture_info = {}
        if self._cam_manager:
            camera_posture_info = self._cam_manager.get_state_enter_setting()
        pos = camera_posture_info.get('pos')
        if not pos:
            return
        if self._last_camera_pos and abs(pos[0] - self._last_camera_pos[0]) <= 20 and abs(pos[1] - self._last_camera_pos[1]) <= 20:
            if abs(pos[2] - self._last_camera_pos[2]) <= 20:
                return
        world_pos = math3d.vector(-pos[0], -pos[1], -pos[2]) * self._camera.world_transformation
        pos_in_screen = self._camera.world_to_screen(world_pos)
        x, y = neox_pos_to_cocos(pos_in_screen[0], pos_in_screen[1])
        lpos = self._3d_widget.convertToNodeSpace(cc.Vec2(x, y))
        if lpos.x > 0:
            self._3d_widget.nd_perspective.SetPosition(lpos.x, '180')
        self._last_camera_pos = pos

    def on_camera_state(self, new_cam_type, old_cam_type, is_finish_switch):
        if self._setting != PVE_MECHA_RADAR_3D:
            return
        if not self._3d_widget:
            return
        if is_finish_switch:
            return
        if new_cam_type == old_cam_type:
            return
        self.reset_center_positon()

    def set_setting(self, setting):
        self._setting = setting
        if self._setting == PVE_MECHA_RADAR_NONE:
            for sector, item in six_ex.items(self._2d_panel_items_dict):
                item.setVisible(False)

            for sector, item in six_ex.items(self._3d_panel_items_dict):
                item.setVisible(False)

        elif self._setting == PVE_MECHA_RADAR_2D:
            for sector, item in six_ex.items(self._3d_panel_items_dict):
                item.setVisible(False)

        elif self._setting == PVE_MECHA_RADAR_3D:
            for sector, item in six_ex.items(self._2d_panel_items_dict):
                item.setVisible(False)

    def clear(self):
        for item in six_ex.values(self._2d_panel_items_dict):
            item.Destroy()

        for item in six_ex.values(self._3d_panel_items_dict):
            item.Destroy()

        self._2d_widget and self._2d_widget.Destroy()
        self._2d_widget = None
        self._3d_widget and self._3d_widget.Destroy()
        self._3d_widget = None
        return

    def destroy(self):
        self.init_params()
        self.clear()
        global_data.emgr.scene_camera_switch_player_setted_event -= self.on_player_setted
        global_data.emgr.camera_switch_to_state_event -= self.on_camera_state