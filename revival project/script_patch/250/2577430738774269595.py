# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/com_mecha_effect/ComMechaEffect8020.py
from __future__ import absolute_import
from .ComGenericMechaEffect import ComGenericMechaEffect
from logic.gcommon.const import NEOX_UNIT_SCALE
import weakref
import math3d
import world
RUSH_HIT_BONE_NAME = ('biped_bone78', 'biped_bone98', 'arm_l_bone_01', 'arm_r_bone_02')
RUSH_HIT_UNIT_EFFECT_ID = '99'
RUSH_HIT_SCENE_EFFECT_ID = '100'
UNIT_Y = math3d.vector(0, 1, 0)
CAR_MODE_ANIM_NAMES = {
 'trans_1', 'trans_move', 'trans_jump01', 'trans_jump02', 'trans_jump03',
 'dash_trans', 'dash_pre', 'dash_f', 'dash_end'}

class ComMechaEffect8020(ComGenericMechaEffect):
    BIND_EVENT = ComGenericMechaEffect.BIND_EVENT.copy()
    BIND_EVENT.update({'E_SHOW_RUSH_HIT_EFFECT': 'on_show_rush_hit_effect'
       })

    def init_from_dict(self, unit_obj, bdict):
        super(ComMechaEffect8020, self).init_from_dict(unit_obj, bdict)

    def on_post_init_complete(self, bdict):
        super(ComMechaEffect8020, self).on_post_init_complete(bdict)
        self.need_handle_anim = self.ev_g_mecha_fashion_id() in (201802052, 201802053,
                                                                 201802054)
        self.is_car_mode = False

    def destroy(self):
        super(ComMechaEffect8020, self).destroy()
        self.model_ref = None
        return

    def on_model_loaded(self, model):
        super(ComMechaEffect8020, self).on_model_loaded(model)
        self.model_ref = weakref.ref(model)

    def on_trigger_anim_effect(self, anim_name, *args, **kwargs):
        super(ComMechaEffect8020, self).on_trigger_anim_effect(anim_name, *args, **kwargs)
        if self.need_handle_anim and anim_name:
            is_car_mode = anim_name in CAR_MODE_ANIM_NAMES
            if self.is_car_mode ^ is_car_mode:
                self.is_car_mode = is_car_mode
                self.sd.ref_socket_res_agent.set_sfx_res_visible(not is_car_mode, 'human_only')
                self.sd.ref_socket_res_agent.set_model_res_visible(not is_car_mode, 'human_only')
                self.sd.ref_socket_res_agent.set_model_res_visible(is_car_mode, 'car_only')

    @staticmethod
    def _get_consider_pos_list(model):
        forward = model.rotation_matrix.forward
        bone_middle_pos = math3d.vector(0, 0, 0)
        all_consider_pos = []
        for bone_name in RUSH_HIT_BONE_NAME:
            bone_mat = model.get_bone_matrix(bone_name, world.SPACE_TYPE_WORLD)
            if not bone_mat:
                continue
            bone_pos = bone_mat.translation
            bone_pos += forward * 0.5 * NEOX_UNIT_SCALE
            all_consider_pos.append(bone_pos)
            bone_middle_pos += bone_pos

        bone_middle_pos *= 1.0 / len(all_consider_pos)
        all_consider_pos.append(bone_middle_pos)
        return all_consider_pos

    def _on_rush_hit_unit(self, model, target_unit):
        target_model = target_unit.ev_g_model()
        if not target_model:
            return
        else:
            end = target_model.position + math3d.vector(0, target_model.bounding_box.y, 0)
            all_consider_pos = self._get_consider_pos_list(model)
            min_dist = None
            start = None
            for consider_pos in all_consider_pos:
                if min_dist is None:
                    start = consider_pos
                    min_dist = (start - end).length
                else:
                    cur_dist = (consider_pos - end).length
                    if cur_dist < min_dist:
                        min_dist = cur_dist
                        start = consider_pos

            direct = end - start
            direct.normalize()
            mat = math3d.matrix.make_orient(direct, UNIT_Y)
            rot = math3d.matrix_to_rotation(mat)
            direct *= NEOX_UNIT_SCALE * 50
            if target_unit.sd.ref_model_hit_by_ray_func:
                res = target_unit.sd.ref_model_hit_by_ray_func(start, direct)
            else:
                res = target_model.hit_by_ray2(start, direct)
            if res and res[0]:
                hit_pos = start + direct * res[1]
                hit_pos = (hit_pos.x, hit_pos.y, hit_pos.z)
            else:
                hit_pos = (
                 start.x, start.y, start.z)
            self.on_trigger_disposable_effect(RUSH_HIT_UNIT_EFFECT_ID, hit_pos, (rot.x, rot.y, rot.z, rot.w), duration=0, need_sync=True)
            return

    def _on_rush_hit_scene(self, model):
        all_consider_pos = self._get_consider_pos_list(model)
        hit_pos = all_consider_pos[-1]
        rot = math3d.matrix_to_rotation(model.rotation_matrix)
        self.on_trigger_disposable_effect(RUSH_HIT_SCENE_EFFECT_ID, (hit_pos.x, hit_pos.y, hit_pos.z), (rot.x, rot.y, rot.z, rot.w), duration=0, need_sync=True)

    def on_show_rush_hit_effect(self, target_unit_list):
        if not self.model_ref:
            return
        model = self.model_ref()
        if not model:
            return
        if target_unit_list:
            for target_unit in target_unit_list:
                self._on_rush_hit_unit(model, target_unit)

        else:
            self._on_rush_hit_scene(model)