# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/parts/camera/camera_controller/model_decal_cam_ctrl.py
from __future__ import absolute_import
from .camctrl_base import CameraCtrl
import math
import math3d
import world
from logic.gcommon.const import NEOX_UNIT_SCALE
UNIT_Y = math3d.vector(0, 1, 0)
MIN_RADIUS = 2.5 * NEOX_UNIT_SCALE
MAX_RADIUS = 5.5 * NEOX_UNIT_SCALE
OFFSET_ANGLE = 0
MAX_PHI = 1.7
MIN_PHI = 0.1

def get_transform_by_sphere_param(r, theta, phi, center_pos, offset_angle=0):
    x = r * math.sin(phi) * math.sin(theta) + center_pos.x
    y = r * math.cos(phi) + center_pos.y
    z = -(r * math.sin(phi) * math.cos(theta) + center_pos.z)
    cur_pos = math3d.vector(x, y, z)
    forward = center_pos - cur_pos
    forward.normalize()
    y = UNIT_Y if phi > 0 else -UNIT_Y
    right = forward.cross(y)
    if right.is_zero:
        return (None, None)
    else:
        right.normalize()
        up = right.cross(forward)
        if up.is_zero:
            return (None, None)
        up.normalize()
        if offset_angle != 0:
            offset_phi = math.radians(offset_angle)
            sin_coe = math.sin(offset_phi / 2)
            cos_coe = math.cos(offset_phi / 2)
            offset_rot = math3d.rotation(up.x * sin_coe, up.y * sin_coe, up.z * sin_coe, cos_coe)
            forward = offset_rot.rotate_vector(forward)
        rotation_matrix = math3d.matrix.make_orient(forward, up)
        return (
         cur_pos, rotation_matrix)


class ModelDecalCamCtrl(CameraCtrl):

    def init(self):
        self.events_binded = False
        self._is_active = False
        self.process_event(True)
        self.init_paramter()
        self.default_pos = math3d.vector(0, 0, 0)

    def init_paramter(self):
        self.center_pos = math3d.vector(0, 0, 0)
        self.offset_angle = 0
        self.radius = 5.5 * NEOX_UNIT_SCALE
        self.theta = math.pi
        self.phi = math.pi / 2
        self.enable_scl_tag = True

    def is_active(self):
        return self._is_active

    def process_event(self, flag):
        emgr = global_data.emgr
        e_conf = {'get_decal_camera_param': self.on_get_decal_camera_param,
           'set_decal_camera_param': self.on_set_decal_camera_param,
           'enable_decal_camera_scl': self.enable_scl
           }
        if flag == self.events_binded:
            return
        self.events_binded = flag
        if flag:
            emgr.bind_events(e_conf)
        else:
            emgr.unbind_events(e_conf)

    def enable_scl(self, tag):
        self.enable_scl_tag = tag

    def on_set_decal_camera_param(self, radius, theta, phi):
        self.radius = radius
        global_data.emgr.camera_decal_scl_event.emit(self.radius)
        self.theta = theta
        self.phi = phi

    def on_get_decal_camera_param(self):
        return (
         self.radius, self.theta, self.phi)

    def on_pause(self, flag):
        self.process_event(not flag)

    def on_set_center_pos(self, pos):
        self.center_pos = pos

    def on_mouse_wheel(self, delta):
        if not self.enable_scl_tag:
            return
        sig = 1 if delta < 0 else -1
        delta_radius = 0.2 * NEOX_UNIT_SCALE * sig
        self.radius += delta_radius
        self.radius = MAX_RADIUS if self.radius > MAX_RADIUS else self.radius
        self.radius = MIN_RADIUS if self.radius < MIN_RADIUS else self.radius
        global_data.emgr.camera_decal_scl_event.emit(self.radius)

    def on_touch_slide(self, dx, dy):
        self.theta -= dx
        self.phi += dy
        self.theta = self.clamp_val(self.theta)
        self.phi = self.clamp_val(self.phi)
        self.phi = MAX_PHI if self.phi > MAX_PHI else self.phi
        self.phi = MIN_PHI if self.phi < MIN_PHI else self.phi

    def clamp_val(self, val):
        if val > math.pi:
            val = val - 2 * math.pi
        if val < -math.pi:
            val = val + 2 * math.pi
        return val

    def on_update(self, dt, yaw, pitch):
        pos, rotation = get_transform_by_sphere_param(self.radius, self.theta, self.phi, self.center_pos, self.offset_angle)
        if pos and rotation:
            scene = global_data.game_mgr.scene
            camera = scene.active_camera
            camera.position = pos
            camera.rotation_matrix = rotation
            light = scene.get_light('dir_light')
            light.world_rotation_matrix = camera.world_rotation_matrix

    def reset_cam_state(self):
        self.init_paramter()
        global_data.emgr.camera_decal_scl_event.emit(self.radius)
        self.center_pos = self.default_pos
        self.on_update(None, None, None)
        return