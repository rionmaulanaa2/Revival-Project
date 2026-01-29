# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/parts/PartReflectEffect.py
from __future__ import absolute_import
from __future__ import print_function
import six_ex
from six.moves import range
from . import ScenePart
import math3d
from common.uisys.render_target import RenderTargetHolder
import game3d
import render
import math
import world
from logic.gcommon.const import NEOX_UNIT_SCALE
import weakref
import common.utils.timer as timer
from logic.gcommon.common_const import scene_const
from common.cfg import confmgr
from logic.gutils import lobby_model_display_utils
REAL_SUN_DIST = 40000
_HASH_RT_OR_COLOR = game3d.calc_string_hash('u_change_color')
_HASH_outline_alpha = game3d.calc_string_hash('outline_alpha')
REFLECT_RT_CONF = {'scn_bg_color': 0,
   'cam_fov': 60.0,
   'rt_width': 1757.0,
   'rt_height': 1024.0,
   'cam_euler': math3d.vector(0 / 180 * math.pi, 0 / 180 * math.pi, 0 / 180 * math.pi),
   'cam_pos': math3d.vector(0, 300, 0)
   }

class PartReflectEffect(ScenePart.ScenePart):
    MIRROR_MODEL_NAME = 'shangcheng_jingzi_01'
    INIT_EVENT = {'get_reflect_rt_event': 'get_reflect_rt',
       'check_cur_scene_mirror_model_event': 'check_cur_scene_mirror_model',
       'scene_camera_change_event': 'scene_camera_change',
       'change_scene_event': 'on_change_scene',
       'add_model_to_mirror': 'on_add_model_to_mirror',
       'mirror_model_play_animation': 'on_mirror_model_play_animation',
       'mirror_model_change_pos_rotation': 'on_mirror_model_change_pos_rotation',
       'lobby_set_models_visible_event': 'set_models_visible',
       'debug_reflect_effect_scene': 'debug_reflect_effect_scene'
       }

    def __init__(self, scene, name):
        super(PartReflectEffect, self).__init__(scene, name)
        self._mirror_plane = None
        self._mirror_target = None
        self._ref_model = {}
        self._update_camera_timer_id = None
        self._scene_type = None
        self._is_bind = False
        self._support_multi_mirror = False
        return

    def is_enable_mirrors(self):
        return not global_data.is_32bit or G_IS_NA_PROJECT

    def check_cur_scene_mirror_model(self, scene_info=None):
        if not self.is_enable_mirrors():
            return
        else:
            if scene_info is None:
                new_scene = global_data.game_mgr.get_cur_scene()
                scene_type = global_data.game_mgr.get_cur_scene_type()
            else:
                new_scene, scene_type = scene_info
            is_reflect = lobby_model_display_utils.is_scene_surpport_reflect(scene_type)
            if not is_reflect:
                new_scene = None
            if new_scene:
                self.on_change_scene(new_scene, scene_type)
                global_data.emgr.check_add_model_to_mirror.emit()
            else:
                self.on_change_scene()
            return

    def on_change_scene(self, new_scene=None, scene_type=None):
        if not self.is_enable_mirrors():
            return
        else:
            self.clear()
            if global_data.is_ue_model:
                if new_scene:
                    model = new_scene.get_model(self.MIRROR_MODEL_NAME)
                    if model:
                        model.all_materials.set_technique(1, 'shader/common_mirror.nfx::TShader')
                return
            is_reflect = lobby_model_display_utils.is_scene_surpport_reflect(scene_type)
            if new_scene:
                mirror_plane = new_scene.get_model(self.MIRROR_MODEL_NAME)
                if mirror_plane:
                    mirror_plane.visible = is_reflect
            if not is_reflect:
                new_scene = None
            if new_scene:
                self._update_camera_timer_id = global_data.game_mgr.register_logic_timer(self.scene_camera_change, 1.0 / 33.0, times=-1, mode=timer.CLOCK)
            if not new_scene:
                return
            self._scene_type = scene_type
            scene_conf = confmgr.get('scenes', scene_type)
            self._support_multi_mirror = scene_conf.get('support_multi_mirror', False)
            self._mirror_plane = new_scene.get_model(self.MIRROR_MODEL_NAME)
            if global_data.is_ue_model:
                if self._mirror_plane:
                    self._mirror_plane.all_materials.set_technique(1, 'shader/common_color.nfx::TShader')
            self.init_render_target()
            self.set_render_target_to_model(self._mirror_plane, 'TexReflection', 0)
            return

    def on_enter(self):
        super(PartReflectEffect, self).on_enter()

    def on_mirror_model_play_animation(self, ref_model, *args):
        if not self.is_enable_mirrors():
            return
        mirror_model = self.get_mirror_model(ref_model)
        if mirror_model and mirror_model.valid:
            mirror_model.play_animation(*args)

    def on_add_model_to_mirror(self, model, path=None, remove_socket_list=None):
        if not self.is_enable_mirrors():
            return
        else:
            if not self._mirror_target:
                return
            if not self._support_multi_mirror:
                for ref_model, mirror_model in six_ex.items(self._ref_model):
                    if mirror_model and mirror_model.valid:
                        self._mirror_target.del_model(mirror_model)

                self._ref_model = {}
            if not model:
                return
            if 'model_new/mecha' in path:
                path = path.replace('h.gim', 'l3.gim')
            if global_data.ex_scene_mgr_agent.check_settle_scene_active():
                log_error("{}'s mirror model path is {}".format(str(model), path))
            if model in self._ref_model:
                o_m_model = self._ref_model[model]
                o_m_model and o_m_model.valid and self._mirror_target.del_model(o_m_model)
                self._ref_model.pop(model)
            mirror_model = world.model(path, None)
            if remove_socket_list:
                global_data.model_mgr.remove_model_socket(mirror_model, remove_socket_list)
            self._ref_model[model] = mirror_model
            world_position = model.world_position
            mirror_model.world_position = world_position
            self._mirror_target.add_model(mirror_model, pos=world_position, rotation_matrix=mirror_model.world_rotation_matrix, scale=model.scale)
            mirror_model.all_materials.enable_write_alpha = True
            return

    def set_models_visible(self, visible, index=-1):
        if not self.is_enable_mirrors():
            return
        if index != -1:
            part_md = global_data.game_mgr.scene.get_com('PartModelDisplay')
            if not part_md:
                return
            model_list = part_md.get_cur_model_list()
            if index >= len(model_list):
                return
            model = model_list[index].get_model()
            mirror_model = self._ref_model.get(model)
            if mirror_model and mirror_model.valid:
                mirror_model.visible = visible
        else:
            for mirror_model in six_ex.values(self._ref_model):
                if mirror_model and mirror_model.valid:
                    mirror_model.visible = visible

    def init_render_target(self):
        if not self.is_enable_mirrors():
            return
        else:
            if not self._mirror_plane:
                return
            if self._mirror_target:
                self._mirror_target.stop_render_target()
            bounding_box = self._mirror_plane.bounding_box
            active_camera = world.get_active_scene().active_camera
            REFLECT_RT_CONF['cam_fov'] = active_camera.fov
            all_light = [
             'dir_light']
            self._mirror_target = RenderTargetHolder(None, None, REFLECT_RT_CONF, True, all_light)
            self._mirror_target.start_render_target()
            return

    def debug_reflect_effect_scene(self):
        if not self.is_enable_mirrors():
            return
        print('test--debug_reflect_effect_scene--step0--_mirror_target =', self._mirror_target)
        if not self._mirror_target:
            return
        all_visible_models = self._mirror_target.scn.get_all_visible_models()
        print('test--debug_reflect_effect_scene--step1--len(all_visible_models) =', len(all_visible_models))
        for index in range(len(all_visible_models)):
            one_visible_model = all_visible_models[index]
            print('test--debug_reflect_effect_scene--step2--one_visible_model.name =', one_visible_model.name, '--one_visible_model.filename =', one_visible_model.filename)

        all_models = self._mirror_target.scn.get_models()
        print('test--debug_reflect_effect_scene--step3--len(all_models) =', len(all_models))
        for index in range(len(all_models)):
            one_model = all_models[index]
            print('test--debug_reflect_effect_scene--step4--one_model.name =', one_model.name, '--one_model.filename =', one_model.filename)

    def on_mirror_model_change_pos_rotation(self, ref_model, *args):
        if not self.is_enable_mirrors():
            return
        if not ref_model or not ref_model.valid:
            return
        mirror_model = self.get_mirror_model(ref_model)
        if mirror_model:
            mirror_model.position = ref_model.world_position
            mirror_model.rotation_matrix = ref_model.world_rotation_matrix

    def get_mirror_model(self, ref_model):
        mirror_model = self._ref_model.get(ref_model, None)
        if mirror_model and mirror_model.valid:
            return mirror_model
        else:
            return

    def scene_camera_change(self, *args):
        if not self.is_enable_mirrors():
            return
        if not self._ref_model:
            return
        if not self._mirror_plane or not self._mirror_plane.valid:
            return
        active_camera = world.get_active_scene().active_camera
        if not active_camera:
            return
        if not self._ref_model:
            return
        for ref_model, mirror_model in six_ex.items(self._ref_model):
            if mirror_model and mirror_model.valid and ref_model and ref_model.valid:
                mirror_model.position = ref_model.world_position
                mirror_model.rotation_matrix = ref_model.world_rotation_matrix

        plane_normal = math3d.vector(0, 1, 0)
        reflect_matrix = math3d.matrix.make_reflection(plane_normal, self._mirror_plane.world_position)
        self._mirror_target.camera.transformation = active_camera.transformation * reflect_matrix
        self._mirror_target.camera.aspect = active_camera.aspect
        self._mirror_target.camera.fov = active_camera.fov
        self._mirror_target.camera.z_range = active_camera.z_range
        self._mirror_target.camera.projection_matrix = active_camera.projection_matrix
        self._mirror_target.camera.look_at = active_camera.look_at
        self._mirror_target.camera.scale *= math3d.vector(-1, 1, 1)

    def get_reflect_rt(self):
        return self._mirror_target

    def set_render_target_to_model(self, model, tex_name, tex_index=1):
        if not self.is_enable_mirrors():
            return
        if not model or not model.valid:
            return
        if not self._mirror_target:
            log_error('[PartReflectEffect] mirror_target is None!!!')
            return
        hash_tex = game3d.calc_string_hash(tex_name)
        material = model.get_sub_material(tex_index)
        model.all_materials.set_texture(hash_tex, tex_name, self._mirror_target.tex)

    def clear(self):
        if not self.is_enable_mirrors():
            return
        else:
            for ref_model, mirror_model in six_ex.items(self._ref_model):
                if mirror_model and mirror_model.valid:
                    self._mirror_target.del_model(mirror_model)

            if self._mirror_target:
                self._mirror_target.stop_render_target()
                self._mirror_target.destroy()
            self._mirror_plane = None
            self._mirror_target = None
            self._ref_model = {}
            self._scene_type = None
            if self._update_camera_timer_id:
                global_data.game_mgr.unregister_logic_timer(self._update_camera_timer_id)
                self._update_camera_timer_id = None
            return

    def on_exit(self):
        super(PartReflectEffect, self).on_exit()
        self.clear()