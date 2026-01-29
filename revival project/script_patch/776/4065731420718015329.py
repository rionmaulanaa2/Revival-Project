# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComParabolaTrackAppearance.py
from __future__ import absolute_import
from six.moves import range
import world
import math3d
from math import radians, sin
from ..UnitCom import UnitCom
from logic.manager_agents.manager_decorators import sync_exec
TRACK_COUNT = 35

class ComParabolaTrackAppearance(UnitCom):
    BIND_EVENT = {'E_SHOW_PARABOLA_TRACK': 'show_track',
       'E_UPDATE_PARABOLA_TRACK': 'update_track',
       'E_SET_PARA_LINE_VISIBLE': 'set_para_line_visible',
       'E_HIDE_PARABOLA_TRACK': 'hide_track',
       'G_TRACK_LINE_VISIBLE': 'is_track_line_visible',
       'E_DEATH': ('on_die', 10)
       }

    def __init__(self):
        super(ComParabolaTrackAppearance, self).__init__()
        self.triangle_strip = None
        self.end_sfx = None
        self.initial_speed = 0
        self.gravity = 0
        self._extraUpAngle = 0
        self._col = None
        self._start_pos = None
        self._last_refresh_time = 0
        self.is_init = False
        self.col = None
        self.end_pos = None
        self.direction = None
        self.para_line_visible = True
        self.update_callback = None
        self._mass = 1.0
        self._linear_damping = 0.0
        return

    def is_track_line_visible(self):
        return self.para_line_visible

    def show_track(self, end_sfx_path, start_pos, speed, gravity, extraUpAngle, callback=None, para_line_visible=True, direction=None, mass=1.0, linear_damping=0.0):
        self.direction = direction
        self.para_line_visible = para_line_visible
        self.update_callback = callback
        self.set_initial_info(start_pos, speed, gravity, extraUpAngle, mass, linear_damping)
        self.set_track_sfx(end_sfx_path)
        self.update_track(start_pos, self.direction)

    def update_track(self, start_pos, direction=None):
        if not self.triangle_strip:
            return
        if not self.triangle_strip.visible:
            self.triangle_strip.visible = True and self.para_line_visible
        self._start_pos = start_pos
        self.direction = direction
        self._refresh_strip()

    def on_die(self, *args):
        self.destroy_sfx()

    def hide_track(self, hide=True):
        self.para_line_visible = False
        self.set_track_visibility(not hide)
        if hide and self.end_sfx:
            global_data.sfx_mgr.remove_sfx(self.end_sfx)
            self.end_sfx = None
        return

    def set_para_line_visible(self, visible):
        self.para_line_visible = visible
        self.set_track_visibility(visible)

    def set_track_visibility(self, visible):
        if self.triangle_strip:
            self.triangle_strip.visible = visible and self.para_line_visible
        if self.end_sfx:
            self.end_sfx.visible = visible

    def set_track_sfx(self, end_sfx_path):
        if not end_sfx_path:
            self.show_throw_line()
            self.end_sfx = None
            return
        else:
            global_data.sfx_mgr.create_sfx_in_scene(end_sfx_path, on_create_func=self.end_sfx_callback)
            return

    def show_throw_line(self):
        import world
        import math3d
        import render
        speed = self.initial_speed
        g = self.gravity
        vy, vz, direction = self.get_strip_speed()
        start_pos = self._start_pos
        if not start_pos:
            start_pos = math3d.vector(0, -100, 0)
        end_point, normal = self.get_contact_end(start_pos, direction * speed, g)
        self.end_pos = end_point
        if not normal:
            self.end_pos.y = -100
        self._gravity_track = world.gravity_track(TRACK_COUNT)
        self._gravity_track.set_width(2)
        self._gravity_track.set_track_gravity(self.gravity)
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
        if not self.para_line_visible:
            self.triangle_strip.visible = False

    @sync_exec
    def _set_strip_top_most(self):
        if self.triangle_strip and self.triangle_strip.valid:
            self.triangle_strip.top_most = True

    def set_initial_info(self, start_pos, speed, gravity, extraUpAngle, mass, linear_damping):
        self._start_pos = start_pos
        self.initial_speed = speed
        self._extraUpAngle = extraUpAngle
        self.gravity = gravity
        self._mass = mass
        self._linear_damping = linear_damping

    def _refresh_strip(self, start_pos=None):
        if not self.triangle_strip or not self.triangle_strip.valid:
            return
        if start_pos:
            self._start_pos = start_pos
        pos = self._start_pos
        if not pos:
            return
        speed_info = self.get_strip_speed()
        g = self.gravity
        if not speed_info:
            return
        speed = self.initial_speed
        vy, vz, direction = speed_info
        end_point, normal = self.get_contact_end(pos, direction * speed, g)
        self.end_pos = end_point
        if normal:
            if self.end_sfx:
                self.end_sfx.visible = True and self.para_line_visible
                self.end_sfx.position = end_point
            if self.update_callback:
                self.update_callback(True, self._start_pos, end_point)
        elif self.end_sfx:
            self.end_sfx.visible = False
            if self.update_callback:
                self.update_callback(False, self._start_pos, end_point)
        else:
            self.end_pos.y = -100
            if self.update_callback:
                self.update_callback(False, self._start_pos, end_point)
        offset = end_point - pos
        if abs(direction.x + direction.z) > 0.0001:
            time = (offset.x + offset.z) / ((direction.x + direction.z) * speed)
        else:
            time = 3.5
        self._gravity_track.set_track_info(math3d.vector(0, vy, vz), time)
        direction.y = 0
        if direction.is_zero:
            self.triangle_strip.position = pos
        else:
            self.triangle_strip.set_placement(pos, direction, math3d.vector(0, 1, 0))

    def get_strip_speed(self):
        direction = self.cal_direction(self._extraUpAngle)
        if not direction:
            return (None, None, None)
        else:
            speed = self.initial_speed
            vy = direction.y
            if abs(vy) < 1:
                from math import sqrt
                vz = sqrt(1 - vy * vy) * speed
            else:
                vz = 0
            vy *= speed
            return (
             vy, vz, direction)

    def get_contact_end(self, pos, speed, gy):
        import world
        fpos = pos
        tpos = pos
        col = self.get_col()
        scene_col = world.get_active_scene().scene_col
        from logic.gcommon.common_const.collision_const import GROUP_CHARACTER_INCLUDE
        import collision
        speed = math3d.vector(speed)
        damping_factor = self._linear_damping * self._linear_damping / self._mass
        for i in range(1, 16):
            t = 0.25
            a_damping = speed * damping_factor
            speed -= a_damping * t
            speed.y += gy * t
            tpos = fpos + speed * t
            info = scene_col.sweep_test(col, fpos, tpos, GROUP_CHARACTER_INCLUDE, GROUP_CHARACTER_INCLUDE, 0, collision.INCLUDE_FILTER)
            if info[0]:
                return (info[1], info[2])
            fpos = tpos

        return (
         tpos, None)

    def get_col(self):
        if self.col is not None:
            return self.col
        else:
            import math3d
            import collision
            import world
            size = math3d.vector(0.1, 0.1, 0.1)
            self.col = collision.col_object(collision.SPHERE, size, -1, -1)
            world.get_active_scene().scene_col.add_object(self.col)
            return self.col

    def end_sfx_callback(self, sfx, *args):
        self.show_throw_line()
        if not self.end_pos:
            global_data.sfx_mgr.remove_sfx(sfx)
            return
        if self.end_pos.y > -1:
            sfx.position = self.end_pos
        else:
            sfx.visible = False
        if self.end_sfx:
            global_data.sfx_mgr.remove_sfx(self.end_sfx)
        self.end_sfx = sfx
        self.end_sfx.visible = self.para_line_visible

    def cal_direction(self, up_angle):
        camera = world.get_active_scene().active_camera
        rotation_matrix = camera.world_rotation_matrix
        direction = rotation_matrix.forward
        right = rotation_matrix.right
        if self.direction:
            direction = self.direction
            up = math3d.vector(0, 1, 0)
            right = direction.cross(up) * -1
        if up_angle <= 0:
            return direction
        if direction.y > sin(radians(90 - up_angle)):
            direction = math3d.vector(0, 1, 0)
        else:
            mat = math3d.matrix.make_rotation(right, -radians(up_angle))
            direction = direction * mat
        return direction

    def destroy_sfx(self):
        if not self.triangle_strip:
            return
        else:
            self._gravity_track = None
            self.triangle_strip = None
            self.end_pos = None
            if self.end_sfx:
                global_data.sfx_mgr.remove_sfx(self.end_sfx)
                self.end_sfx = None
            return

    def destroy(self):
        if self.col:
            self.scene.scene_col.remove_object(self.col)
            self.col = None
        self.destroy_sfx()
        super(ComParabolaTrackAppearance, self).destroy()
        return

    def set_weapon(self, obj_weapon):
        pass