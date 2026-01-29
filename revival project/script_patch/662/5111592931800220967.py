# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/parts/PartUnderWater.py
from __future__ import absolute_import
from . import ScenePart
from logic.comsys.underwater.ScreenWater import ScreenWater
from logic.gcommon.common_const import water_const, scene_const
from common.cfg import confmgr
import game3d
DEFAULT_WATER_HEIGHT = 40

class PartUnderWater(ScenePart.ScenePart):

    def __init__(self, scene, name):
        super(PartUnderWater, self).__init__(scene, name)
        screen_water_model_path = confmgr.get('script_gim_ref')['screen_effect_water']
        self.water = ScreenWater(screen_water_model_path)
        self._timer = None
        self._timer2 = None
        self._water_mtl_set = set((scene_const.MTL_WATER, scene_const.MTL_DEEP_WATER))
        self._tmp_window_size = game3d.get_window_size()
        return

    def on_enter(self):
        scn = self.scene()
        self.water.bind(scn.active_camera)
        self._timer = global_data.game_mgr.get_logic_timer().register(func=self.on_update, interval=1)
        self._timer2 = global_data.game_mgr.get_logic_timer().register(func=self.on_update_per_frame, interval=1)

    def on_update(self):
        scn = self.scene()
        cam = scn.active_camera
        pos = cam.world_position
        material_index = scn.get_scene_info_2d(pos.x, pos.z)
        is_active = material_index in self._water_mtl_set
        self._tmp_window_size = game3d.get_window_size()
        if is_active and global_data.cam_lplayer:
            ct = global_data.cam_lplayer.ev_g_control_target()
            if ct and ct.logic:
                h = self._tmp_window_size[1]
                cam_low_point = cam.screen_to_world(0, h)[0].y
                water_height = ct.logic.ev_g_water_height()
                if water_height is not None:
                    is_active = cam_low_point < water_height
                else:
                    is_active = False
        elif global_data.is_judge_ob:
            is_active = False
        self.water.active(is_active)
        return

    def on_update_per_frame(self):
        if self.water.is_active():
            if global_data.cam_lplayer:
                target_player = global_data.cam_lplayer.ev_g_control_target()
                target_player = target_player.logic if target_player else None
                if target_player:
                    cam = self.scene().active_camera
                    height = target_player.ev_g_water_height()
                    self.water.set_param(cam.fov, cam.z_range[0], height)
            elif global_data.is_judge_ob:
                pass
        return

    def on_exit(self):
        if self._timer is not None:
            global_data.game_mgr.get_logic_timer().unregister(self._timer)
            self._timer = None
        if self._timer2 is not None:
            global_data.game_mgr.get_logic_timer().unregister(self._timer2)
            self._timer2 = None
        self.water.destroy()
        return