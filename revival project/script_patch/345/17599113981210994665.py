# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/underwater/ScreenWater.py
from __future__ import absolute_import
import math
import world
import math3d

class ScreenWater(object):

    def __init__(self, model_path):
        import game3d
        self._obj = None
        self._shader_params = [
         [
          game3d.calc_string_hash('u_hfov'), 'u_hfov', math.radians(45.0 / 2.0)],
         [
          game3d.calc_string_hash('u_near_dist'), 'u_near_dist', 1.0],
         [
          game3d.calc_string_hash('WaterHeight'), 'WaterHeight', 40.0],
         [
          game3d.calc_string_hash('u_water_color'), 'u_water_color', (0.1961, 0.2745, 0.4157, 0)]]
        self._shader_dirty = True
        self._obj_task = None
        self._cam_ref = None
        self._active = False
        self._valid = True
        self._model_path = model_path
        return

    def _load_obj(self):
        self._obj_task = world.create_model_async(self._model_path, self._on_loaded)

    def _on_loaded(self, model, *args):
        self._obj = model
        self._obj.scale *= 10
        self._obj_task = None
        self._apply_param()
        self._obj.visible = self._active
        if self._valid and self._cam_ref and self._cam_ref():
            self._obj.set_parent(self._cam_ref())
            self._obj.scale *= 1000.0
        else:
            self._obj.destroy()
            self._obj = None
        return

    def bind(self, cam):
        if self._obj:
            self._obj.set_parent(cam)
            self._obj.scale *= 1000.0
            self._obj.render_level = 7
        else:
            import weakref
            self._cam_ref = weakref.ref(cam)

    def set_param(self, fov, near_range, water_height):
        if not isinstance(fov, float):
            return
        else:
            hfov = math.radians(fov / 2.0)
            if hfov != self._shader_params[0][2] or near_range != self._shader_params[1][2] or self._shader_params[2][2] != water_height:
                self._shader_params[0][2] = hfov
                self._shader_params[1][2] = near_range
                self._shader_params[2][2] = float(water_height) if water_height is not None else 40.0
                self._shader_dirty = True
                self._apply_param()
            return

    def _apply_param(self):
        if self._shader_dirty and self._obj:
            for hash_name, name, value in self._shader_params:
                self._obj.all_materials.set_var(hash_name, name, value)

            self._shader_dirty = False

    def active(self, value):
        if self._active != value:
            self._active = value
            if self._obj:
                self._obj.visible = value
        if self._active and self._obj == self._obj_task == None:
            self._load_obj()
        return

    def is_active(self):
        return self._active

    def destroy(self):
        if self._obj:
            self._obj.destroy()
            self._obj = None
        if self._obj_task and self._obj_task.valid:
            self._obj_task.cancel()
            self._obj_task = None
        self._valid = False
        return