# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/parts/PartEffectManager.py
from __future__ import absolute_import
import six
import random
import math
from . import ScenePart
import math3d
import game3d
import world
import render
from logic.comsys.effect import screen_effect
from common.framework import Functor
from logic.gcommon.const import NEOX_UNIT_SCALE
from data.constant_break_data import data as constant_break_list
from common.utils.sfxmgr import CREATE_SRC_NORMAL, CREATE_SRC_OTHER_HIT
_HASH_TextureTransform0 = game3d.calc_string_hash('TextureTransform0')
_HASH_Diffuse = game3d.calc_string_hash('Diffuse')
_HASH_u_use_local_uv = game3d.calc_string_hash('u_use_local_uv')
_HASH_u_decal_grid_size = game3d.calc_string_hash('u_decal_grid_size')
_HASH_u_depth_bias = game3d.calc_string_hash('u_depth_bias')
_HASH_DecalTexDiffuse = game3d.calc_string_hash('Tex2')
_HASH_u_fade_time = game3d.calc_string_hash('u_fade_time')
ValidEffectNames = {'DarkCornerEffect': screen_effect.DarkCornerEffect,
   'GrayEffect': screen_effect.GrayEffect,
   'GaussanBlurEffect': screen_effect.GaussanBlurEffect,
   'ParachuteSlow': screen_effect.ParachuteSlow,
   'ParachuteFast': screen_effect.ParachuteFast,
   'MechaChongCiEffect': screen_effect.MechaChongCiEffect,
   'HumanRushEffect': screen_effect.HumanRushEffect,
   'MeleeRushEffect': screen_effect.MeleeRushEffect,
   'ScreenWhite': screen_effect.ScreenWhite,
   'ScreenMapStart': screen_effect.ScreenMapStart,
   'ScreenMapEnd': screen_effect.ScreenMapEnd,
   'SpeedLine': screen_effect.ScreenSpeedLine,
   'ScreenNBombPlaced': screen_effect.ScreenNBombPlaced
   }
SfxSuffixDistortion = '_distortion.sfx'
SFX_TASK_INVALID = -2

class PartEffectManager(ScenePart.ScenePart):
    INIT_EVENT = {'show_screen_effect': 'show_effect',
       'hide_screen_effect': 'hide_effect',
       'destroy_screen_effect': 'remove_effect',
       'model_hitted_effect_event': 'add_model_hitted_effect'
       }

    def __init__(self, scene, name):
        super(PartEffectManager, self).__init__(scene, name)
        self._effects_map = {}
        self.is_valid = True

    def _cancel_pp_timer--- This code section failed: ---

  64       0  LOAD_GLOBAL           0  'global_data'
           3  LOAD_ATTR             1  'game_mgr'
           6  LOAD_ATTR             2  'get_render_timer'
           9  CALL_FUNCTION_0       0 
          12  STORE_FAST            1  'tm'

  65      15  LOAD_GLOBAL           3  'hasattr'
          18  LOAD_GLOBAL           1  'game_mgr'
          21  CALL_FUNCTION_2       2 
          24  POP_JUMP_IF_FALSE    51  'to 51'

  66      27  LOAD_FAST             1  'tm'
          30  LOAD_ATTR             4  'unregister'
          33  LOAD_FAST             0  'self'
          36  LOAD_ATTR             5  'pp_timer_id'
          39  CALL_FUNCTION_1       1 
          42  POP_JUMP_IF_FALSE    51  'to 51'

  67      45  JUMP_ABSOLUTE        51  'to 51'
          48  JUMP_FORWARD          0  'to 51'
        51_0  COME_FROM                '48'

Parse error at or near `CALL_FUNCTION_2' instruction at offset 21

    def add_model_hitted_effect(self, model, start_pos, end_pos, sfx_path='effect/fx/weapon/bullet/jinshu.sfx'):
        import random
        if not (model and model.valid):
            return
        hit_vect = end_pos - start_pos
        if hit_vect.is_zero:
            hit_vect = math3d.vector(0, 0, 1)
        else:
            hit_vect.normalize()
        check_pos = end_pos - hit_vect * 10
        check_dir = hit_vect * 30
        result = model.hit_by_ray(check_pos, check_dir)
        if result[0]:
            pos = check_pos + check_dir * result[1]
            normal = model.get_triangle_normal(result[2], result[3])
            offset = 0.005 + 0.4 * random.random()
            pos = pos + normal * offset
            from logic.gcommon.common_const import weapon_const

            def create_cb(sfx):
                global_data.sfx_mgr.set_rotation_by_normal(sfx, normal)

            global_data.sfx_mgr.create_sfx_for_model(sfx_path, model, pos, duration=weapon_const.BULLET_HOLE_LIFE_TIME, on_create_func=create_cb, int_check_type=CREATE_SRC_OTHER_HIT)

    def on_enter(self):
        pass

    def on_exit(self):
        self.is_valid = False
        for eff_name, eff_inst in six.iteritems(self._effects_map):
            if eff_inst:
                eff_inst.destroy()

        self._effects_map.clear()
        self._cancel_pp_timer()

    def show_effect(self, effect_name, info_dict):
        if global_data.ex_scene_mgr_agent.check_settle_scene_active():
            return None
        else:
            if effect_name in self._effects_map and self._effects_map[effect_name]:
                self._effects_map[effect_name].show_with_parameters(info_dict)
            else:
                effect = self.create_effect(effect_name, info_dict)
                self._effects_map[effect_name] = effect
            return self._effects_map[effect_name]

    def set_effect_var(self, effect_name, var_name, var_val):
        if effect_name in self._effects_map:
            self._effects_map[effect_name].set_effect_parameter(var_name, var_val)

    def hide_effect(self, effect_name):
        if effect_name in self._effects_map:
            self._effects_map[effect_name].hide()

    def remove_effect(self, effect_name):
        if effect_name in self._effects_map:
            if self._effects_map[effect_name]:
                self._effects_map[effect_name].destroy()
            del self._effects_map[effect_name]

    def create_effect(self, effect_name, info_dict):
        effect_class = ValidEffectNames.get(effect_name, None)
        if effect_class:
            return effect_class(info_dict)
        else:
            log_error('Unexist effect: %s' % effect_name)
            return
            return