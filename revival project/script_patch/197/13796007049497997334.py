# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/material_test.py
from __future__ import absolute_import
from common.framework import Singleton
import world
import math3d
import game3d
from common.utils import timer
_HASH_roughness_input = game3d.calc_string_hash('roughness_input')
_HASH_metallic_input = game3d.calc_string_hash('metallic_input')
_HASH_color_tint = game3d.calc_string_hash('color_tint')

class CMaterialTest(Singleton):
    ALIAS_NAME = 'material_test_mgr'

    def init(self):
        self.test_timer = None
        self.test_models = []
        self.test_info = (2, 1, 1, 100, 20)
        self.xyz_index = (0, 0, 0)
        return

    def on_finalize(self):
        self.clear_time()
        self.clear_models()

    def clear_time(self):
        self.test_timer and global_data.game_mgr.get_logic_timer().unregister(self.test_timer)
        self.test_timer = None
        return

    def clear_models(self):
        scn = world.get_active_scene()
        if not scn:
            return
        for model in self.test_models:
            if not model or not model.valid:
                continue
            scn.remove_object(model)
            model.clear_events()
            model.destroy()

        self.test_models = []

    def scene_mat_vlm(self, mat):
        mat.set_technique(1, 'shader/lightmap93.nfx::TShader')
        mat.set_macro('ENV_TEX', 'TRUE')
        mat.set_macro('FULLY_ROUGH', 'TRUE')
        mat.set_macro('MIX_MAP_ENABLE', 'FALSE')
        mat.set_macro('LIGHT_MAP_ENABLE', 'FALSE')
        mat.set_macro('NONMETAL', 'TRUE')
        mat.set_macro('USE_VLM', 'TRUE')

    def mecha_mat_pbr(self, mat):
        mat.set_technique(1, 'shader/vbr_toon_mecha_nx2_mobile.nfx::TShader')
        mat.set_macro('NODIFFUSE', 'TRUE')
        mat.set_var(_HASH_color_tint, 'color_tint', (1.0, 0.3875, 0.144, 0.0))
        mat.set_macro('ENV_TEX', 'TRUE')
        mat.set_macro('FULLY_ROUGH', 'FALSE')
        mat.set_macro('MIX_MAP_ENABLE', 'FALSE')
        mat.set_macro('USE_VLM', 'TRUE')
        mat.set_macro('XNORMAL_MAP_ENABLE', 'FALSE')
        mat.set_macro('ALIGN_UE_EFFECT', 'TRUE')
        mat.set_var(_HASH_roughness_input, 'roughness_input', 0.3)
        mat.set_var(_HASH_metallic_input, 'metallic_input', 1.0)

    def scene_mat_pbr(self, mat):
        mat.set_technique(1, 'shader/lightmap93.nfx::TShader')
        mat.set_macro('NODIFFUSE', 'TRUE')
        mat.set_var(_HASH_color_tint, 'color_tint', (1.0, 0.3875, 0.144, 0.0))
        mat.set_macro('ENV_TEX', 'TRUE')
        mat.set_macro('FULLY_ROUGH', 'FALSE')
        mat.set_macro('MIX_MAP_ENABLE', 'FALSE')
        mat.set_macro('USE_VLM', 'TRUE')
        mat.set_macro('NONMETAL', 'FALSE')
        mat.set_macro('ALIGN_UE_EFFECT', 'TRUE')
        mat.set_var(_HASH_roughness_input, 'roughness_input', 0.3)
        mat.set_var(_HASH_metallic_input, 'metallic_input', 1.0)

    def vlm_test(self):
        scn = world.get_active_scene()
        if not scn:
            return
        self.clear_time()
        self.clear_models()
        original_pos = global_data.player.logic.ev_g_position()
        scn.set_macros({'VLM_TEST': '1'})
        self.xyz_index = (0, 0, 0)

        def create_sphere(original_pos=original_pos):
            i_num, j_num, k_num, dis, size = self.test_info
            i, j, k = self.xyz_index
            if k >= k_num:
                j += 1
                k = 0
            if j >= j_num:
                i += 1
                j = 0
            if i >= i_num:
                self.clear_time()
                return
            x = i * dis
            y = j * dis
            z = k * dis
            pos = math3d.vector(original_pos.x + x, original_pos.y + size + y, original_pos.z + z)
            mod = world.model('model_new/test/bone_sphere.gim', scn)
            mat = mod.all_materials
            self.scene_mat_vlm(mat)
            mat.rebuild_tech()
            self.test_models.append(mod)
            mod.position = pos
            mod.scale = math3d.vector(size, size, size)
            k += 1
            self.xyz_index = (i, j, k)

        self.test_timer = global_data.game_mgr.get_logic_timer().register(func=create_sphere, mode=timer.CLOCK, interval=0.1)

    def contrast_pbr(self):
        scn = world.get_active_scene()
        if not scn:
            return
        self.clear_time()
        self.clear_models()
        original_pos = global_data.player.logic.ev_g_position()
        scn.set_macros({'IS_IN_BATTLE': '1'})
        self.xyz_index = (0, 0, 0)
        self.test_info = (3, 1, 1, 100, 80)

        def create_sphere(original_pos=original_pos):
            i_num, j_num, k_num, dis, size = self.test_info
            i, j, k = self.xyz_index
            if k >= k_num:
                j += 1
                k = 0
            if j >= j_num:
                i += 1
                j = 0
            if i >= i_num:
                self.clear_time()
                return
            x = i * dis
            y = j * dis
            z = k * dis
            pos = math3d.vector(original_pos.x + x, original_pos.y + size + y, original_pos.z + z)
            mod = world.model('model_new/test/bone_sphere.gim', scn)
            mat = mod.all_materials
            if k == 1:
                self.scene_mat_pbr(mat)
            elif k == 0:
                self.mecha_mat_pbr(mat)
            mat.set_var(_HASH_roughness_input, 'roughness_input', 0.3 * i)
            mat.set_var(_HASH_metallic_input, 'metallic_input', 0.0)
            mat.rebuild_tech()
            self.test_models.append(mod)
            mod.position = pos
            mod.scale = math3d.vector(size, size, size)
            k += 1
            self.xyz_index = (i, j, k)

        self.test_timer = global_data.game_mgr.get_logic_timer().register(func=create_sphere, mode=timer.CLOCK, interval=0.1)