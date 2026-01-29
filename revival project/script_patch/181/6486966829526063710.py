# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/parts/PartBackground.py
from __future__ import absolute_import
from . import ScenePart
import render
import world
import math3d
import game3d
import copy
import time

class PartBackground(ScenePart.ScenePart):
    ENTER_EVENT = {'scene_switch_background': '_switch_background_panel',
       'scene_destroy_background': '_destroy_background_panel',
       'scene_cam_move': '_fix_model_position'
       }

    def __init__(self, scene, name):
        super(PartBackground, self).__init__(scene, name, False)
        self._background_model_info = copy.deepcopy(self.get_scene().scene_conf.get('background_model', {}))

    def on_enter(self):
        self._switch_background_panel()

    def on_exit(self):
        pass

    def _switch_background_panel(self, cls_name=None):
        if not self._background_model_info:
            return
        else:
            info = self._background_model_info
            model = self.get_scene().get_model(info['name'])
            tex_name = info['tex_name']
            if 'hash_name' not in info:
                info['hash_name'] = game3d.calc_string_hash(tex_name)
            hash_name = info['hash_name']
            if cls_name is None:
                cls_name = info['default_bg']
            global_data.scene_background.set_active_background(cls_name)
            tex = global_data.scene_background.get_texture()
            model.all_materials.set_texture(hash_name, tex_name, tex)
            self._fix_model_position()
            return

    def _destroy_background_panel(self, cls_name):
        if not cls_name:
            return
        global_data.scene_background.destroy_background(cls_name)

    def _fix_model_position(self, *args):
        if not self._background_model_info:
            return
        scene = self.get_scene()
        model = scene.get_model(self._background_model_info['name'])
        cam_pos = scene.active_camera.world_position
        model.world_position = math3d.vector(cam_pos.x, cam_pos.y, model.world_position.z)
        self._fix_model_scale()

    def _fix_model_scale(self):
        if not self._background_model_info:
            return
        scene = self.get_scene()
        model = scene.get_model(self._background_model_info['name'])
        bbox = model.bounding_box
        cam = scene.active_camera
        cam_pos = cam.world_position
        lb_pos = math3d.vector(cam_pos.x + bbox.x / 2, cam_pos.y + bbox.y / 2, model.world_position.z)
        screen_pos = cam.world_to_screen(lb_pos)
        if screen_pos[0] < -10000 or screen_pos[1] < -10000:
            return
        center_pos = cam.world_to_screen(math3d.vector(cam_pos.x, cam_pos.y, model.world_position.z))
        if center_pos[0] == screen_pos[0] or center_pos[1] == screen_pos[1]:
            return
        scale = 1.0 / 0.85 / 2
        x_scale = center_pos[0] * scale / (center_pos[0] - screen_pos[0])
        y_scale = center_pos[1] * scale / (center_pos[1] - screen_pos[1])
        model.scale = math3d.vector(x_scale, y_scale, 1)