# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/Fire/FireSurvivalBattleMgr.py
from __future__ import absolute_import
import six
import six_ex
from common.framework import Singleton
import math3d
import collision
import world
from logic.gutils import gravity_mode_utils
from common.utils import timer

class FireCircleRegionChecker(object):

    def __init__(self):
        self._timer_id = 0
        self._region_id = None
        return

    def destroy(self):
        self.clear_timer()

    def clear_timer(self):
        if self._timer_id:
            global_data.game_mgr.get_logic_timer().unregister(self._timer_id)
            self._timer_id = None
        return

    def init_timer(self):
        if self._timer_id:
            global_data.game_mgr.get_logic_timer().unregister(self._timer_id)
        self._timer_id = global_data.game_mgr.get_logic_timer().register(func=self.check_in_fire_region, mode=timer.CLOCK, interval=1)

    def check_in_fire_region(self):
        player_pos = self.get_player_pos()
        if player_pos:
            region_id = global_data.fire_sur_battle_mgr.get_region_by_pos(player_pos)
            self._region_id = region_id
            global_data.emgr.notify_inside_fire_region_id.emit(region_id)

    def get_player_region(self):
        return self._region_id

    def get_player_pos(self):
        cam_lplayer = global_data.cam_lplayer
        if cam_lplayer:
            control_target = cam_lplayer.ev_g_control_target()
            if control_target and control_target.logic:
                pos = control_target.logic.ev_g_model_position()
            else:
                pos = cam_lplayer.ev_g_model_position()
            if pos:
                return pos
        elif global_data.is_in_judge_camera:
            if global_data.game_mgr.scene:
                return global_data.game_mgr.scene.active_camera.world_position
        return global_data.sound_mgr.get_listener_pos()


class FireSurvivalBattleMgr(Singleton):
    ALIAS_NAME = 'fire_sur_battle_mgr'

    def init(self):
        self.init_parameters()
        self.fire_checker = FireCircleRegionChecker()

    def init_parameters(self):
        self.fire_region_model_id_dict = {}
        self.fire_region_info_dict = {}

    def on_finalize(self):
        for region_id in list(six_ex.keys(self.fire_region_info_dict)):
            self.set_region_param(region_id, None, None, None)

        if self.fire_checker:
            self.fire_checker.destroy()
            self.fire_checker = None
        self.remove_region_model()
        self.init_parameters()
        return

    def get_region_by_pos(self, t_pos):
        for region_id in six.iterkeys(self.fire_region_info_dict):
            pos, radius, data = self.fire_region_info_dict[region_id]
            if (t_pos.x - pos[0]) * (t_pos.x - pos[0]) + (t_pos.z - pos[2]) * (t_pos.z - pos[2]) <= radius * radius:
                return region_id

        return None

    def get_player_region(self):
        return self.fire_checker.get_player_region()

    def get_all_region_ids(self):
        return six_ex.keys(self.fire_region_info_dict)

    def update_fire_regions(self, region_all_dict):
        region_dict = region_all_dict.get('fire_region', {})
        region_level = region_all_dict.get('region_level')
        to_be_remove_region_id = []
        for cur_region_id in six.iterkeys(self.fire_region_info_dict):
            if cur_region_id not in region_dict:
                to_be_remove_region_id.append(cur_region_id)

        for rid in to_be_remove_region_id:
            self.set_region_param(rid, None, None, None)

        for region_id, region_info in six.iteritems(region_dict):
            if region_id not in self.fire_region_info_dict:
                region_pos = region_info[0]
                region_r = region_info[1]
                self.set_region_param(region_id, region_pos, region_r, {})

        if self.fire_checker:
            if self.fire_region_info_dict:
                self.fire_checker.init_timer()
            else:
                self.fire_checker.clear_timer()
                self.fire_checker.check_in_fire_region()
        return

    def set_region_param(self, region_id, pos, radius, data):
        if pos and radius:
            self.fire_region_info_dict[region_id] = (
             pos, radius, data)
            self.create_region_model(region_id)
            global_data.emgr.init_fire_region.emit(region_id)
        else:
            if region_id in self.fire_region_info_dict:
                del self.fire_region_info_dict[region_id]
            self.remove_region_model(region_id)
            global_data.emgr.remove_fire_region.emit(region_id)

    def get_region_param(self, region_id):
        return self.fire_region_info_dict.get(region_id, [None, None, None])

    def create_region_model(self, region_id):
        if region_id in self.fire_region_model_id_dict:
            return
        region_pos, region_r, region_data = self.get_region_param(region_id)
        path = gravity_mode_utils.get_region_model_path(gravity_mode_utils.OVER_GRAVITY, 1)
        if not path:
            return
        pos = math3d.vector(region_pos[0], region_pos[1], region_pos[2])

        def on_create_callback(model, region_r=region_r):
            scale_x = region_r / (model.bounding_box.x - 27.811500000000002)
            scale_y = model.scale.y
            scale_z = region_r / (model.bounding_box.z - 27.811500000000002)
            model.scale = math3d.vector(scale_x, scale_y, scale_z)
            model.set_rendergroup_and_priority(world.RENDER_GROUP_TRANSPARENT, 100)

        self.remove_region_model(region_id)
        region_model_id = global_data.model_mgr.create_model_in_scene(path, pos, on_create_func=on_create_callback)
        self.fire_region_model_id_dict[region_id] = region_model_id

    def remove_region_model(self, region_id=None):
        if region_id is not None:
            if region_id in self.fire_region_model_id_dict:
                global_data.model_mgr.remove_model_by_id(self.fire_region_model_id_dict[region_id])
                del self.fire_region_model_id_dict[region_id]
        return