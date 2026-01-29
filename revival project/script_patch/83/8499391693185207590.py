# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/parts/PartMirror.py
from __future__ import absolute_import
import six
from . import ScenePart
import math3d
import game3d
import render
import math
import world
import weakref
import common.utils.timer as timer
from common.cfg import confmgr
from logic.gutils import lobby_model_display_utils
from common.uisys.render_target import RenderTargetHolderLobbyMirr
from logic.gcommon.const import NEOX_UNIT_SCALE
from logic.gcommon.common_const import scene_const
REFLECT_RT_CONF = {'scn_bg_color': 0,
   'cam_fov': 60.0,
   'rt_width': 1757.0,
   'rt_height': 1024.0,
   'cam_euler': math3d.vector(0 / 180 * math.pi, 0 / 180 * math.pi, 0 / 180 * math.pi),
   'cam_pos': math3d.vector(0, 300, 0)
   }
MIRROR_CENTER_OFFSET = math3d.vector(24, 6, 0)

class PartMirror(ScenePart.ScenePart):
    MIRROR_MODEL_NAME = 'lobby_mirror'
    INIT_EVENT = {'get_parent_model_of_mirror_model': 'get_parent_model_of_mirror_model'
       }

    def __init__(self, scene, name):
        super(PartMirror, self).__init__(scene, name)
        self._mirror_plane = None
        self._mirror_target = None
        self._dynamic_model = {}
        self._dynamic_model_reverse = {}
        self._ref_model = {}
        self._ref_sfx = {}
        self._tick_timer = None
        self._last_in_area = False
        self.reflect_matrix = None
        self._in_area_timer = 0
        self.stop_area_timer = False
        return

    def is_enable_mirrors(self):
        return not global_data.is_32bit or G_IS_NA_PROJECT

    def replace_scene_models(self, lobby_scene_type):
        if self._mirror_target:
            self._mirror_target.replace_scene_models(lobby_scene_type)

    def on_enter(self):
        super(PartMirror, self).on_enter()
        if not self.is_enable_mirrors():
            return
        self.init_render_target()
        self.start_tick()

    def on_exit(self):
        super(PartMirror, self).on_exit()
        self.clear()

    def on_pause(self, flag):
        if not self.is_enable_mirrors():
            return
        if self._tick_timer:
            global_data.game_mgr.get_post_logic_timer().set_pause(self._tick_timer, flag)
        if self._mirror_target:
            if flag:
                self._mirror_target.stop_render_target()
            else:
                self._mirror_target.start_render_target()

    def clear(self):
        self.stop_tick()
        for mirror_model in self._ref_model:
            if mirror_model and mirror_model.valid:
                self._mirror_target.del_model(mirror_model)

        for mirror_sfx in self._ref_sfx:
            if mirror_sfx and mirror_sfx.valid:
                self._mirror_target.del_sfx(mirror_sfx)

        if self._mirror_target:
            self._mirror_target.stop_render_target()
            self._mirror_target.destroy()
        self._mirror_plane = None
        self._mirror_target = None
        self._dynamic_model = {}
        self._dynamic_model_reverse = {}
        self._ref_model = {}
        self._ref_sfx = {}
        return

    def init_render_target(self):
        if not self.is_enable_mirrors():
            return
        else:
            self._mirror_plane = world.get_active_scene().get_model(self.MIRROR_MODEL_NAME)
            if not self._mirror_plane:
                return
            self._mirror_plane.all_materials.set_technique(1, 'shader/common_mirror.nfx::TShader')
            active_camera = world.get_active_scene().active_camera
            REFLECT_RT_CONF['cam_fov'] = active_camera.fov
            all_light = []
            self._mirror_target = RenderTargetHolderLobbyMirr(None, None, REFLECT_RT_CONF, True, all_light, scene_type='LobbyMirror')
            self._mirror_target.start_render_target()
            hash_tex = game3d.calc_string_hash('TexReflection')
            self._mirror_plane.all_materials.set_texture(hash_tex, 'TexReflection', self._mirror_target.tex)
            plane_normal = -self._mirror_plane.rotation_matrix.forward
            self.reflect_matrix = math3d.matrix.make_reflection(plane_normal, self._mirror_plane.world_position + plane_normal * NEOX_UNIT_SCALE * 0)
            return

    def start_tick(self):
        if not self.is_enable_mirrors():
            return
        self.stop_tick()

        def start():
            if self.scene() and self.scene().valid:
                self._tick_timer = global_data.game_mgr.get_post_logic_timer().register(func=self.on_update, timedelta=True)

        global_data.game_mgr.delay_exec(0.3, start)

    def stop_tick(self):
        if not self.is_enable_mirrors():
            return
        else:
            if self._tick_timer:
                global_data.game_mgr.get_post_logic_timer().unregister(self._tick_timer)
                self._tick_timer = None
            return

    def load_static_models(self):
        pass

    def add_model_to_mirror(self, model, mirror_model=None, is_dynamic=False):
        if not self.is_enable_mirrors():
            return
        else:
            if not self._mirror_target:
                return
            if not model or not model.valid:
                return
            if model in self._ref_model:
                return
            if not mirror_model:
                mirror_model = world.model(model.filename, None)
            self._ref_model[model] = mirror_model
            if is_dynamic:
                self._dynamic_model[model] = mirror_model
                self._dynamic_model_reverse[mirror_model] = model
                mirror_model.all_materials.set_macro('RIM_LIGHT_ENABLE', 'TRUE')
                mirror_model.all_materials.rebuild_tech()
            self._mirror_target.add_model(mirror_model, pos=model.world_position, rotation_matrix=model.world_rotation_matrix, scale=model.scale)
            mirror_model.all_materials.enable_write_alpha = True
            if 'mumu' in global_data.deviceinfo.get_device_model_name():
                mirror_model.all_materials.set_macro('ENV_TEX', 'FALSE')
                mirror_model.all_materials.rebuild_tech()
            return

    def remove_model_from_mirror(self, model):
        if not self.is_enable_mirrors():
            return
        if model in self._dynamic_model:
            mirror_model = self._dynamic_model[model]
            del self._dynamic_model[model]
            del self._dynamic_model_reverse[mirror_model]
        if model in self._ref_model:
            del self._ref_model[model]

    def set_model_visible_from_mirror(self, model, visible):
        if not self.is_enable_mirrors():
            return
        if not self._mirror_target:
            return
        if not model or not model.valid:
            return
        if model in self._ref_model:
            self._ref_model[model].visible = visible

    def add_sfx_from_mirror(self, sfx):
        if not self.is_enable_mirrors():
            return
        else:
            if not self._mirror_target:
                return
            if not sfx or not sfx.valid:
                return
            if sfx in self._ref_sfx:
                return
            mirror_sfx = world.sfx(sfx.filename, scene=None)
            self._ref_sfx[sfx] = mirror_sfx
            self._mirror_target.add_sfx(mirror_sfx, pos=sfx.world_position, rotation_matrix=sfx.rotation_matrix, scale=sfx.scale)
            return

    def remove_sfx_from_mirror(self, sfx):
        if not self.is_enable_mirrors():
            return
        if sfx in self._ref_sfx:
            self._ref_sfx[sfx].destroy()
            del self._ref_sfx[sfx]

    def on_update(self, dt):
        if not self.is_enable_mirrors():
            return
        if not self._mirror_plane or not self._mirror_plane.valid:
            return
        if not self._dynamic_model:
            return
        active_camera = world.get_active_scene().active_camera
        if not active_camera:
            return
        for ref_model, mirror_model in six.iteritems(self._dynamic_model):
            if mirror_model and mirror_model.valid and ref_model and ref_model.valid:
                mirror_model.position = ref_model.world_position
                mirror_model.rotation_matrix = ref_model.world_rotation_matrix

        self._mirror_target.camera.transformation = active_camera.transformation * self.reflect_matrix
        self._mirror_target.camera.aspect = active_camera.aspect
        self._mirror_target.camera.fov = active_camera.fov
        self._mirror_target.camera.z_range = active_camera.z_range
        self._mirror_target.camera.projection_matrix = active_camera.projection_matrix
        self._mirror_target.camera.look_at = active_camera.look_at
        self._mirror_target.camera.scale *= math3d.vector(-1, 1, 1)
        in_area = self.check_in_mirror_area()
        if in_area and not self.stop_area_timer:
            self._in_area_timer += dt
        else:
            self._in_area_timer = 0
        ui = global_data.ui_mgr.get_ui('LobbyUI')
        if self._in_area_timer > 2 and ui and ui.isVisible():
            from logic.comsys.share.LobbySceneOnlyUI import LobbySceneOnlyUI
            LobbySceneOnlyUI()
        elif not in_area and self._last_in_area:
            global_data.ui_mgr.close_ui('LobbySceneOnlyUI')
        elif in_area and not self._last_in_area:
            self.stop_area_timer = False
        self._last_in_area = in_area

    def get_reflect_rt(self):
        return self._mirror_target

    def check_in_mirror_area(self):
        if not self.is_enable_mirrors():
            return False
        player = global_data.lobby_player
        if not player or not self._mirror_plane:
            return False
        pos = player.ev_g_position()
        if not pos:
            return False
        dist = pos - self._mirror_plane.world_position - MIRROR_CENTER_OFFSET
        mirror_forward = self._mirror_plane.rotation_matrix.forward
        cam_forward = player.ev_g_model().rotation_matrix.forward
        dot = mirror_forward.dot(cam_forward)
        return dist.length < 19 and dot < 0.1

    def update_mirror_env(self, env_path, env_conf):
        if not self.is_enable_mirrors():
            return
        if not self._mirror_target:
            return
        self._mirror_target.set_new_env(env_path, env_conf)

    def get_parent_model_of_mirror_model(self, mirror_model):
        return self._dynamic_model_reverse.get(mirror_model)