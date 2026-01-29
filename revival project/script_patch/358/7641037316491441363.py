# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/MontageImp/Gizmo.py
from __future__ import absolute_import
import math3d
import game
import render
import world

class Gizmo(object):
    GIZMO_MOVE = 0
    GIZMO_ROTATE = 1
    GIZMO_SCALE = 2

    def __init__(self, scn=None, t=0):
        super(Gizmo, self).__init__()
        self.gizmo_type = t
        self.scn = scn
        self.object = None
        self.start_matrix = None
        self.scale = 3.4
        if self.scn:
            self.scn.gizmo_init()
        self.drag_listeners = []
        return

    def update(self, *args):
        if not (self.scn and self.scn.valid):
            return
        else:
            self.scn.gizmo_update(self.gizmo_type, 768)
            self.snap_test(game.mouse_x, game.mouse_y)
            if self.is_dragging():
                self.do_dragging(game.mouse_x, game.mouse_y)
                for cb in self.drag_listeners:
                    cb(self.object)

            if self.object:
                if self.object.valid:
                    if hasattr(self.object, 'visible') and not self.object.visible and self.is_visible():
                        self.set_visible(False)
                    if self.is_visible():
                        self.set_position(self.object.position.x, self.object.position.y, self.object.position.z)
                else:
                    self.object = None
                    self.set_visible(False)
            return

    def add_gizmo_dragging_listener(self, cb):
        self.drag_listeners.append(cb)

    def snap_test(self, x, y):
        return self.scn.gizmo_snap_test(self.gizmo_type, x, y)

    def set_visible(self, b):
        if self.object and self.object.valid:
            if b:
                self.set_position(self.object.position.x, self.object.position.y, self.object.position.z)
            if hasattr(self.object, 'show_ext_technique'):
                self.object.show_ext_technique(render.EXT_TECH_OUTLINE, b)
        r = self.scn.gizmo_set_visible(self.gizmo_type, b)
        self.update()
        return r

    def start_dragging(self, x, y):
        if self.object and self.object.valid:
            self.start_matrix = self.object.transformation
        return self.scn.gizmo_start_dragging(self.gizmo_type, x, y)

    def do_dragging(self, x, y):
        from MontageSDK.Lib import MontPathManager
        if self.object is MontPathManager.managers['CameraActor'].virtual_node and MontPathManager.managers['CameraActor'].transformProxy.isValid() and MontPathManager.managers['CameraActor'].transformProxy.getProperty('locked', default=False):
            return
        delta_matrix = self.scn.gizmo_do_dragging(self.gizmo_type, x, y)
        if self.object and self.object.valid and self.start_matrix:
            final = math3d.matrix(self.start_matrix)
            old_pos = math3d.vector(final.translation)
            old_rot = final.rotation
            old_scale = math3d.vector(final.scale)
            new_pos = old_pos + delta_matrix.translation
            new_scale = math3d.vector(old_scale.x * delta_matrix.scale.x, old_scale.y * delta_matrix.scale.y, old_scale.z * delta_matrix.scale.z)
            new_rot = old_rot * delta_matrix.rotation
            m = math3d.matrix()
            m.do_scale(new_scale)
            m.do_rotation(new_rot)
            m.do_translate(new_pos)
            if hasattr(world, 'particlesystem') and isinstance(self.object, world.particlesystem):
                self.object.world_position = new_pos
                self.object.scale = new_scale
                self.object.world_rotation_matrix = new_rot
                self.object.restart()
                import MontageSDK
                track = MontageSDK.Interface.getMovieGroupByName(str(self.object))
                activateTrack = track.getTrackByName('Activate')
                if track.isActivate and activateTrack:
                    self.object.set_curtime_directly(track.getTrackByName('Activate').pauseTime)
            else:
                self.object.transformation = m
        return delta_matrix

    def end_dragging(self):
        self.start_matrix = None
        return self.scn.gizmo_end_dragging(self.gizmo_type)

    def is_visible(self):
        return self.scn.gizmo_is_visible(self.gizmo_type)

    def is_dragging(self):
        return self.scn.gizmo_is_dragging(self.gizmo_type)

    def bind_object(self, gameobject):
        if self.object and self.object.valid:
            if hasattr(self.object, 'show_ext_technique'):
                self.object.show_ext_technique(render.EXT_TECH_OUTLINE, False)
        self.object = gameobject
        if gameobject:
            self.set_position(gameobject.position.x, gameobject.position.y, gameobject.position.z)
            if hasattr(self.object, 'show_ext_technique'):
                self.object.show_ext_technique(render.EXT_TECH_OUTLINE, self.is_visible())
        else:
            self.set_position(0, 0, 0)

    def set_position(self, x, y, z):
        return self.scn.gizmo_set_position(self.gizmo_type, x, y, z)

    def switch_gizmo(self, t):
        if t != self.gizmo_type:
            is_visible = self.is_visible()
            self.end_dragging()
            self.set_visible(False)
            self.gizmo_type = t
            self.set_visible(is_visible)
            if self.object:
                self.set_position(self.object.position.x, self.object.position.y, self.object.position.z)

    def set_scale(self, scale):
        self.scale = scale
        self.scn.gizmo_set_scale(scale)

    def get_scale(self):
        return self.scale

    def get_type(self):
        return self.gizmo_type