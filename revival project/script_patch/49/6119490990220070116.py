# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/Gravity/GravitySurvivalBattleMgr.py
from __future__ import absolute_import
from common.framework import Singleton
import math3d
import collision
import world
from logic.gutils import gravity_mode_utils

class GravitySurvivalBattleMgr(Singleton):
    ALIAS_NAME = 'gravity_sur_battle_mgr'

    def init(self):
        self.init_parameters()

    def init_parameters(self):
        self.less_gravity_region_model_id = []
        self.less_gravity_region_info = []
        self.over_gravity_region_model_id = []
        self.over_gravity_region_info = []
        self.aero_less_gravity_region_model_id = []
        self.aero_less_gravity_region_info = []

    def on_finalize(self):
        self.remove_region_model()
        self.init_parameters()

    def is_gravity_type(self, type):
        return type in (gravity_mode_utils.LESS_GRAVITY, gravity_mode_utils.OVER_GRAVITY, gravity_mode_utils.AERO_LESS_GRAVITY)

    def set_region_param(self, type=None, params=None):
        if not type:
            self.less_gravity_region_info = []
            self.over_gravity_region_info = []
            self.remove_region_model()
            return
        if not self.is_gravity_type(type):
            return
        if type == gravity_mode_utils.LESS_GRAVITY:
            self.less_gravity_region_info = []
            self.remove_region_model(type)
            gravity_region_info = self.less_gravity_region_info
        else:
            if type == gravity_mode_utils.OVER_GRAVITY:
                self.over_gravity_region_info = []
                self.remove_region_model(type)
                gravity_region_info = self.over_gravity_region_info
            elif type == gravity_mode_utils.AERO_LESS_GRAVITY:
                self.aero_less_gravity_region_info = []
                self.remove_region_model(type)
                gravity_region_info = self.aero_less_gravity_region_info
            if not params:
                return
        for info in params:
            pos, radius, level = info
            if pos and radius and level:
                index = len(gravity_region_info)
                gravity_region_info.append((pos, radius, level))
                self.create_region_model(type, index)

    def get_region_param(self, type):
        if not self.is_gravity_type(type):
            return
        if type == gravity_mode_utils.LESS_GRAVITY:
            if self.less_gravity_region_info:
                return self.less_gravity_region_info
        elif type == gravity_mode_utils.OVER_GRAVITY:
            if self.over_gravity_region_info:
                return self.over_gravity_region_info
        elif type == gravity_mode_utils.AERO_LESS_GRAVITY:
            if self.aero_less_gravity_region_info:
                return self.aero_less_gravity_region_info

    def create_region_model(self, type, index):
        if not self.is_gravity_type(type):
            return
        region_pos, region_r, region_level = self.get_region_param(type)[index]
        path = gravity_mode_utils.get_region_model_path(type, region_level)
        if not path:
            return
        pos = math3d.vector(region_pos[0], region_pos[1], region_pos[2])

        def on_create_callback(model, region_r=region_r):
            scale_x = region_r / model.bounding_box.x
            scale_y = model.scale.y
            scale_z = region_r / model.bounding_box.z
            model.scale = math3d.vector(scale_x, scale_y, scale_z)
            model.set_rendergroup_and_priority(world.RENDER_GROUP_TRANSPARENT, 100)

        if type == gravity_mode_utils.LESS_GRAVITY:
            self.less_gravity_region_model_id.append(global_data.model_mgr.create_model_in_scene(path, pos, on_create_func=on_create_callback))
        elif type == gravity_mode_utils.OVER_GRAVITY:
            self.over_gravity_region_model_id.append(global_data.model_mgr.create_model_in_scene(path, pos, on_create_func=on_create_callback))
        elif type == gravity_mode_utils.AERO_LESS_GRAVITY:
            self.aero_less_gravity_region_model_id.append(global_data.model_mgr.create_model_in_scene(path, pos, on_create_func=on_create_callback))

    def remove_region_model(self, type=None):
        if type and not self.is_gravity_type(type):
            return
        if (type and type == gravity_mode_utils.LESS_GRAVITY or not type) and self.less_gravity_region_model_id:
            for model_id in self.less_gravity_region_model_id:
                global_data.model_mgr.remove_model_by_id(model_id)

            self.less_gravity_region_model_id = []
        if (type and type == gravity_mode_utils.OVER_GRAVITY or not type) and self.over_gravity_region_model_id:
            for model_id in self.over_gravity_region_model_id:
                global_data.model_mgr.remove_model_by_id(model_id)

            self.over_gravity_region_model_id = []
        if (type and type == gravity_mode_utils.AERO_LESS_GRAVITY or not type) and self.aero_less_gravity_region_model_id:
            for model_id in self.aero_less_gravity_region_model_id:
                global_data.model_mgr.remove_model_by_id(model_id)

            self.aero_less_gravity_region_model_id = []