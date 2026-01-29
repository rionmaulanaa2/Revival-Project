# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComJumpTrack.py
from __future__ import absolute_import
from ..UnitCom import UnitCom
import math3d
import world
import render
from math import sqrt
from logic.manager_agents.manager_decorators import sync_exec
TRACK_COUNT = 35
MIN_DIST_BOUNDARY, MAX_DIST_BOUNDARY, MIN_SCALE, MAX_SCALE = (500.0, 800.0, 1.0, 2.0)

class ComJumpTrack(UnitCom):
    BIND_EVENT = {'E_SHOW_JUMP_TRACK': 'show_track',
       'E_HIDE_JUMP_TRACK': 'hide_track'
       }

    def __init__(self):
        super(ComJumpTrack, self).__init__()
        self.triangle_strip = None
        self.end_sfx = None
        self.end_sfx_id = 0
        self._speed = 0
        self._gravity = 0
        self._start_pos = None
        self._last_refresh_time = 0
        self._gravity_track = None
        self.is_init = False
        self._end_pos = None
        return

    def show_track(self, end_sfx_path, start_pos, speed, gravity, end_pos):
        if type(start_pos) in [tuple, list]:
            start_pos = math3d.vector(start_pos[0], start_pos[1], start_pos[2])
        if type(speed) in [tuple, list]:
            speed = math3d.vector(speed[0], speed[1], speed[2])
        if type(end_pos) in [tuple, list]:
            end_pos = math3d.vector(end_pos[0], end_pos[1], end_pos[2])
        self.set_initial_info(start_pos, speed, gravity, end_pos)
        if not self.is_init:
            self.set_track_sfx(end_sfx_path)
            self.is_init = True
        else:
            self.set_track_visibility(True)
            self.update_track()
        if self.end_sfx_id == 0:
            self.end_sfx_id = global_data.sfx_mgr.create_sfx_in_scene(end_sfx_path, on_create_func=self.end_sfx_callback)

    def update_track(self):
        if not self.triangle_strip.visible:
            self.triangle_strip.visible = True
        self._refresh_strip()

    def hide_track(self):
        self.set_track_visibility(False)
        if self.end_sfx_id:
            global_data.sfx_mgr.remove_sfx_by_id(self.end_sfx_id)
            self.end_sfx = None
            self.end_sfx_id = 0
        return

    def set_track_visibility(self, visible):
        if self.triangle_strip:
            self.triangle_strip.visible = visible
        if self.end_sfx:
            self.end_sfx.visible = visible

    def set_track_sfx(self, end_sfx_path):
        speed = self._speed
        g = self._gravity
        vy, vz, direction = self.get_strip_speed()
        start_pos = self._start_pos
        self._gravity_track = world.gravity_track(TRACK_COUNT)
        self._gravity_track.set_track_gravity(self._gravity)
        self.triangle_strip = self._gravity_track.get_primitives()
        if not self.triangle_strip:
            return
        self._refresh_strip()
        tech = render.technique(render.TECH_TYPE_EFFECT, 'shader/throw_line.fx', 'TShader')
        self.triangle_strip.set_technique(tech)
        tex = render.texture('shader/texture/zhishixian_01_bu.tga')
        self.triangle_strip.set_texture(0, tex)
        self._set_strip_top_most()
        direction.y = 0
        if direction.is_zero:
            self.triangle_strip.position = start_pos
        else:
            self.triangle_strip.set_placement(start_pos, direction, math3d.vector(0, 1, 0))
        if not self._start_pos:
            self.set_track_visibility(False)

    @sync_exec
    def _set_strip_top_most(self):
        if self.triangle_strip and self.triangle_strip.valid:
            self.triangle_strip.top_most = True

    def set_initial_info(self, start_pos, speed, gravity, end_pos):
        self._start_pos = start_pos
        self._speed = speed
        if self._gravity_track and self._gravity != gravity:
            self._gravity = gravity
            self._gravity_track.set_track_gravity(self._gravity)
        self._end_pos = end_pos

    def _refresh_strip(self, start_pos=None):
        if not self.triangle_strip or not self.triangle_strip.valid:
            return
        if start_pos:
            self._start_pos = start_pos
        pos = self._start_pos
        if not pos:
            return
        speed_info = self.get_strip_speed()
        g = self._gravity
        if not speed_info:
            return
        speed = self._speed
        vy, vz, direction = speed_info
        if self.end_sfx:
            self.end_sfx.visible = True
            self.end_sfx.position = self._end_pos
            dist = (world.get_active_scene().active_camera.position - self._end_pos).length
            if dist < MIN_DIST_BOUNDARY:
                scale = MIN_SCALE
            elif dist > MAX_DIST_BOUNDARY:
                scale = MAX_SCALE
            else:
                scale = MIN_SCALE + (dist - MIN_DIST_BOUNDARY) / (MAX_DIST_BOUNDARY - MIN_DIST_BOUNDARY) * (MAX_SCALE - MIN_SCALE)
            self.end_sfx.scale = math3d.vector(scale, scale, scale)
        offset = self._end_pos - pos
        if abs(direction.x + direction.z) > 0.0001:
            time = (offset.x + offset.z) / ((direction.x + direction.z) * speed.length)
        else:
            time = 2 * g / vy
        self._gravity_track.set_track_info(math3d.vector(0, vy, vz), time)
        direction.y = 0
        if direction.is_zero:
            self.triangle_strip.position = pos
        else:
            self.triangle_strip.set_placement(pos, direction, math3d.vector(0, 1, 0))

    def get_strip_speed(self):
        speed = self._speed
        direction = math3d.vector(speed)
        if direction.is_zero:
            return (None, None, None)
        else:
            direction.normalize()
            vy = speed.y
            vz = sqrt(speed.x * speed.x + speed.z * speed.z)
            return (
             vy, vz, direction)

    def end_sfx_callback(self, sfx, *args):
        if not self._end_pos:
            global_data.sfx_mgr.remove_sfx(sfx)
            return
        sfx.position = self._end_pos or math3d.vector(0, 0, 0)
        self.end_sfx = sfx

    def destroy_sfx(self):
        if not self.triangle_strip:
            return
        else:
            self._gravity_track = None
            self.triangle_strip = None
            self._end_pos = None
            global_data.sfx_mgr.remove_sfx_by_id(self.end_sfx_id)
            self.end_sfx_id = 0
            self.end_sfx = None
            return

    def destroy(self):
        self.destroy_sfx()
        super(ComJumpTrack, self).destroy()