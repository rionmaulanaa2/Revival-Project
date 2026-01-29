# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/parts/camera/CamAimModelRT.py
from __future__ import absolute_import
import world
import game3d
import math3d
import math
from common.uisys.render_target import RenderTargetHolder
import render
import time
import common.utils.timer as timer
from common.cfg import confmgr
from logic.manager_agents.manager_decorators import sync_exec
REFLECT_TEX_HASH = game3d.calc_string_hash('TexReflection')
CAM_RT_CONF = {'scn_bg_color': 4278190080L,
   'cam_fov': 60.0,
   'rt_width': 1344.0,
   'rt_height': 750.0,
   'cam_euler': math3d.vector(0 / 180 * math.pi, 0 / 180 * math.pi, 0 / 180 * math.pi),
   'cam_pos': math3d.vector(0, 300, 0)
   }

class CamAimModelRT(object):

    def __init__(self, fov):
        self.refresh_rt_conf()
        self.aim_rt = RenderTargetHolder(None, None, CAM_RT_CONF, True)
        self.aim_rt.camera.z_range = (1, 20000)
        if global_data.is_ue_model:
            self.load_env_new_sync()
        else:
            self.aim_rt.scn.load_env('scene/scene_env_confs/bw.xml')
        self.rt_model = world.model(confmgr.get('script_gim_ref')['screen_effect_water_gun'], None)
        self.rt_model.get_sub_material(0).set_texture(REFLECT_TEX_HASH, 'TexReflection', self.aim_rt.tex)
        self.rt_model.set_rendergroup_and_priority(world.RENDER_GROUP_TRANSPARENT, world.SUB_RENDER_PRIORITY_MAX_OFS)
        self.rt_timer = None
        self.fov = fov
        global_data.aim_rt = self.aim_rt
        self.update_transformation_every_frame = False
        self.last_update_rotation_timestamp = 0.0
        return

    @sync_exec
    def load_env_new_sync(self):
        if self.aim_rt and self.aim_rt.scn:
            self.aim_rt.scn.load_env_new('scene/scene_env_confs/aim_nx2_mobile.xml')
            self.aim_rt.apply_conf('aim')

    def refresh_rt_conf(self):
        import game3d
        import render
        redirect_scale = render.get_redirect_scale()
        win_size = game3d.get_window_size()[:2]
        CAM_RT_CONF['rt_width'] = win_size[0]
        CAM_RT_CONF['rt_height'] = win_size[1]

    def set_render_model(self, model, is_follow_cam=False):
        if self.aim_rt and model and model.valid:
            active_cam = global_data.game_mgr.scene.active_camera
            rt_model = self.rt_model
            if not rt_model or not rt_model.valid or not active_cam:
                return
            self.on_update()
            self.update_transformation()
            old_world_mat = model.world_transformation
            model.remove_from_parent()
            if is_follow_cam and self.aim_rt.camera.valid:
                model.set_parent(self.aim_rt.camera)
            else:
                self.aim_rt.scn.add_object(model)
            model.world_transformation = old_world_mat
            rt_model.remove_from_parent()
            rt_model.set_parent(active_cam)
            rt_model.position = math3d.vector(0, 0, 30)
            self.start()

    def start(self):
        self.stop()
        render.enable_dynamic_culling(False)
        if self.aim_rt:
            self.aim_rt.start_render_target()
        cam = global_data.game_mgr.scene.active_camera
        if self.rt_model and cam:
            self.rt_model.set_parent(cam)
            self.rt_model.position = math3d.vector(0, 0, 30)
        else:
            log_error('invalid active camera')
        tm = global_data.game_mgr.get_post_logic_timer()
        if self.rt_timer:
            tm.unregister(self.rt_timer)
        self.rt_timer = tm.register(None, self.on_update, interval=1, times=-1, mode=timer.LOGIC)
        return

    def refresh_update_transformation_flag(self, flag):
        self.update_transformation_every_frame = flag

    def on_update(self, flag=False):
        if self.aim_rt:
            scn = global_data.game_mgr.scene
            if not scn or not scn.valid:
                return
            cam = scn.active_camera
            if not cam or not cam.valid:
                return
            if not self.fov:
                self.fov = cam.fov
            rt_cam = self.aim_rt.camera
            rt_cam.aspect = cam.aspect
            rt_cam.fov = self.fov
            rt_cam.look_at = cam.look_at
            if self.update_transformation_every_frame:
                rt_cam.transformation = cam.transformation
            else:
                cur_timestamp = time.time()
                if cur_timestamp - self.last_update_rotation_timestamp > 0.06:
                    self.last_update_rotation_timestamp = cur_timestamp
                    rt_cam.rotation_matrix = cam.rotation_matrix

    def update_transformation(self):
        scn = global_data.game_mgr.scene
        if not scn or not scn.valid:
            return
        cam = scn.active_camera
        if not cam or not cam.valid:
            return
        rt_cam = self.aim_rt.camera
        rt_cam.transformation = cam.transformation

    def stop(self):
        if self.aim_rt:
            self.aim_rt.stop_render_target()
        if self.rt_timer:
            global_data.game_mgr.get_post_logic_timer().unregister(self.rt_timer)
            self.rt_timer = None
        if self.rt_model:
            self.rt_model.remove_from_parent()
        render.enable_dynamic_culling(global_data.feature_mgr.is_support_dyculling())
        return

    def update_cam_param(self, cur_cam):
        if self.aim_rt:
            rt_cam = self.aim_rt.camera
            rt_cam.aspect = cur_cam.aspect
            rt_cam.fov = cur_cam.fov
            rt_cam.look_at = cur_cam.look_at
            rt_cam.projection_matrix = cur_cam.projection_matrix
            rt_cam.transformation = cur_cam.transformation

    def destroy(self):
        self.stop()
        if self.rt_model and self.rt_model.valid:
            self.rt_model.destroy()
            self.rt_model = None
        if self.aim_rt:
            self.aim_rt.stop_render_target()
            self.aim_rt.destroy()
            self.aim_rt = None
        render.enable_dynamic_culling(global_data.feature_mgr.is_support_dyculling())
        return