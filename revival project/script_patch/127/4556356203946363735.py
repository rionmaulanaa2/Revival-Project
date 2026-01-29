# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/Granbelm/GranbelmSurvivalBattleMgr.py
from __future__ import absolute_import
from common.framework import Singleton
from logic.gcommon.common_const import collision_const
import math3d
import collision
import world
from logic.gutils import granbelm_utils, granhack_utils
from logic.gcommon.common_const.battle_const import GRANBELM_MAX_RUNE_COUNT
from logic.client.const.game_mode_const import GAME_MODE_GRANBELM_SURVIVAL, GAME_MODE_GRANHACK_SURVIVAL
from logic.gutils.screen_effect_utils import create_screen_effect_directly

class GranbelmSurvivalBattleMgr(Singleton):
    ALIAS_NAME = 'gran_sur_battle_mgr'

    def init(self):
        self.init_parameters()

    def init_parameters(self):
        self.is_sub_mode = global_data.game_mode.is_mode_type(GAME_MODE_GRANHACK_SURVIVAL)
        self.tele_tag = False
        self.below_col = None
        self.region_model = None
        self.region_level = None
        self.region_wpos = None
        self.region_r = None
        return

    def on_finalize(self):
        self.remove_region_model()
        self.destroy_below_col()
        self.init_parameters()

    def set_tele_tag(self, tag):
        self.tele_tag = tag

    def get_tele_tag(self):
        return self.tele_tag

    def set_region_param(self, pos, radius, level):
        if pos and radius and level:
            self.region_level = level
            self.region_wpos = pos
            self.region_r = radius
            self.create_region_model(pos, radius, level)
        else:
            self.region_level = None
            self.region_wpos = None
            self.region_r = None
            self.remove_region_model()
        return

    def get_region_param(self):
        if self.region_wpos and self.region_r and self.region_level:
            return [self.region_wpos, self.region_r, self.region_level]
        else:
            return None

    def create_tele_screen_sfx(self, portal_type):
        if self.is_sub_mode:
            sfx_path = granhack_utils.get_tele_screen_sfx_path(portal_type)
        else:
            sfx_path = granbelm_utils.get_tele_screen_sfx_path(portal_type)
        create_screen_effect_directly(sfx_path)

    def create_tele_sfx(self, portal_type, tele_role, tele_stage, tele_pos):
        if self.is_sub_mode:
            sfx_path = granhack_utils.get_tele_sfx_path(portal_type, tele_role, tele_stage)
        else:
            sfx_path = granbelm_utils.get_tele_sfx_path(portal_type, tele_role, tele_stage)
        sfx_pos = math3d.vector(tele_pos[0], tele_pos[1], tele_pos[2])
        global_data.sfx_mgr.create_sfx_in_scene(sfx_path, sfx_pos)

    def create_region_model(self, region_pos, region_r, region_level):
        if self.is_sub_mode:
            path = granhack_utils.get_region_model_path(region_level)
        else:
            path = granbelm_utils.get_region_model_path(region_level)
        pos = math3d.vector(region_pos[0], region_pos[1], region_pos[2])

        def on_create_callback(model):
            scale_x = region_r / model.bounding_box.x
            scale_y = model.scale.y
            scale_z = region_r / model.bounding_box.z
            model.scale = math3d.vector(scale_x, scale_y, scale_z)
            model.set_rendergroup_and_priority(world.RENDER_GROUP_TRANSPARENT, 100)
            self.region_model = model

        global_data.model_mgr.create_model_in_scene(path, pos, on_create_func=on_create_callback)

    def remove_region_model(self):
        if self.region_model:
            global_data.model_mgr.remove_model(self.region_model)
            self.region_model = None
        return

    def create_below_col(self, pos):
        size = math3d.vector(200, 2, 200)
        col = collision.col_object(collision.BOX, size)
        col.mask = collision_const.GROUP_CHARACTER_INCLUDE
        col.group = collision_const.TERRAIN_GROUP
        scene = global_data.game_mgr.get_cur_scene()
        scene.scene_col.add_object(col)
        col.position = math3d.vector(pos[0], pos[1] - 5, pos[2])
        self.below_col = col

    def destroy_below_col(self):
        if self.below_col:
            scene = global_data.game_mgr.get_cur_scene()
            scene.scene_col.remove_object(self.below_col)
            self.below_col = None
        return