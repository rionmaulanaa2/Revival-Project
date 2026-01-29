# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/parts/PartMainCamera.py
from __future__ import absolute_import
from . import ScenePart
import math3d
import world
import math
from common.cfg import confmgr

class PartMainCamera(ScenePart.ScenePart):

    def __init__(self, scene, name):
        super(PartMainCamera, self).__init__(scene, name)
        self.ref_model = None
        self.ref_model_task = None
        self.need_update = True
        self.init_ani_name = 'choose_idle'
        return

    def on_enter(self):
        self.load_ref_model()

    def play_ref_model_ani(self, ani_name, loop=False):
        if not self.ref_model:
            self.init_ani_name = ani_name
            return
        self.ref_model.play_animation(ani_name)

    def load_ref_model(self):
        camera_ref_model_path = confmgr.get('script_gim_ref')['lobby_camera_ref_model']
        self.ref_model_task = world.create_model_async(camera_ref_model_path, self.bind_ref_model)

    def bind_ref_model(self, model, *args):
        self.ref_model_task = None
        self.ref_model = model
        scn = self.scene()
        self.camera = scn.create_camera(True)
        self.camera.fov = 60
        scn.add_object(model)
        self.camera.position = math3d.vector(-21, 25, -132)
        self.camera.z_range = (1, 1000)
        self.ref_model.play_animation(self.init_ani_name)
        self.cam_follow_model()
        global_data.emgr.login_scene_prepared_signal.emit()
        self.camera.position = math3d.vector(190, 42, 184)
        self.camera.rotation_matrix = math3d.rotation_to_matrix(math3d.euler_to_rotation(math3d.vector(math.radians(349), math.radians(215), math.radians(7))))
        return

    def on_exit(self):
        if self.ref_model:
            self.ref_model.destroy()
            self.ref_model = None
        elif self.ref_model_task:
            self.ref_model_task.cancel()
            self.ref_model_task = None
        return

    def cam_follow_model(self):
        cam_bone_mat = self.ref_model.get_bone_matrix('bone_camera', world.SPACE_TYPE_WORLD)
        pos = cam_bone_mat.translation
        rot = cam_bone_mat.rotation
        forward = rot.forward
        forward = forward.cross(-rot.right)
        self.camera.set_placement(pos, forward, rot.forward)

    def on_update(self, dt):
        return
        if not self.ref_model:
            return
        self.cam_follow_model()