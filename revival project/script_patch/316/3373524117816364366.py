# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComMoveShadow.py
from __future__ import absolute_import
import six
from ..UnitCom import UnitCom
import math
import math3d
import world
TAN_PI_3 = math.tan(math.pi / 3)
TYPE_DETOUR = 1
TYPE_LOGIC = 2
COLOR_MAP = {TYPE_DETOUR: {'color_s': 16774799,
                 'color_d': 16747520,
                 'color_p': 16774799,
                 'point_h': 4,
                 'point_w': 8
                 },
   TYPE_LOGIC: {'color_s': 1869550,
                'color_d': 139,
                'color_p': 13435085,
                'point_h': 8,
                'point_w': 4
                }
   }

class ComMoveShadow(UnitCom):
    BIND_EVENT = {'E_MOVE_SHADOW_TO': '_move_shadow_to',
       'E_MOVE_SHADOW_PATH': '_show_path'
       }

    def __init__(self):
        super(ComMoveShadow, self).__init__()
        self._oobbjj = None
        self._mp_path_objs = {}
        return

    def _move_shadow_to(self, point):
        self.create_oobbjj()
        if self._oobbjj:
            self._oobbjj.position = math3d.vector(*point)

    def create_oobbjj(self):
        if self._oobbjj:
            return
        scene = self.scene
        if scene:
            self._oobbjj = world.primitives(scene)
            self._oobbjj.create_poly3(get_pos_shadow_poly3())

    def clear(self):
        if self._oobbjj:
            self._oobbjj.remove_from_parent()
            self._oobbjj = None
        self.clear_path()
        return

    def destroy(self):
        self.clear()
        super(ComMoveShadow, self).destroy()

    def _show_path(self, lst_path, i_type):
        self.create_path(lst_path, i_type)

    def create_path(self, lst_path, i_type):
        self.del_path_by_type(i_type)
        scene = self.scene
        if scene:
            holder = []
            self._mp_path_objs[i_type] = holder
            self.do_draw_path(scene, holder, lst_path, i_type)

    def del_path_by_type(self, i_type):
        if i_type in self._mp_path_objs:
            holder = self._mp_path_objs.pop(i_type)
            for obj in holder:
                obj.remove_from_parent()

    def clear_path(self):
        for i_type, holder in six.iteritems(self._mp_path_objs):
            for obj in holder:
                obj.remove_from_parent()

        self._mp_path_objs = {}

    def do_draw_path(self, scene, holder, lst_path, i_type):
        mp_color = COLOR_MAP[i_type]
        color_s = mp_color['color_s']
        color_d = mp_color['color_d']
        color_p = mp_color['color_p']
        w = mp_color['point_w']
        h = mp_color['point_h']
        s_pos = lst_path.pop(0)
        y = s_pos[1]
        s_pos = [s_pos[0], y, s_pos[2]]
        for d_pos in lst_path:
            draw_line(scene, holder, s_pos, d_pos, color_s, color_d, h)
            drop_point(scene, holder, s_pos, color_p, h, w)
            s_pos = d_pos


def get_pos_shadow_poly3(pos=None, h=None, w=None, color=None):
    h = h or 13
    w = w or 13
    x = w / 2.0 * math.tan(math.pi / 6)
    z = w / 2.0
    z2 = w / 2.0 / math.cos(math.pi / 6)
    p0 = math3d.vector(0, 0, 0)
    p1 = math3d.vector(-x, h, z)
    p2 = math3d.vector(-x, h, -z)
    p3 = math3d.vector(z2, h, 0)
    if pos is not None:
        p0 = p0 + pos
        p1 = p1 + pos
        p2 = p2 + pos
        p3 = p3 + pos
    v0 = (p0, color or 13421568)
    v1 = (p1, color or 5622784)
    v2 = (p2, color or 21964)
    v3 = (p3, color or 13369429)
    prim_1 = (
     v0, v1, v2)
    prim_2 = (v0, v2, v3)
    prim_3 = (v0, v3, v1)
    prim_4 = (v3, v2, v1)
    list_poly3 = [
     prim_1, prim_2, prim_3, prim_4]
    return list_poly3


def draw_line(scene, holder, v1, v2, color, color2, h):
    v1 = [
     v1[0], v1[1] + h, v1[2]]
    v2 = [v2[0], v2[1] + h, v2[2]]
    p1 = math3d.vector(*v1)
    p2 = math3d.vector(*v2)
    df = p2 - p1
    w = 0.4
    if not df.is_zero:
        df.normalize()
    vr = df.cross(math3d.vector(df.z, df.x, df.y))
    vr.normalize()
    p3 = p1 + vr * w * 2
    p4 = p2 + vr * w * 2
    vr2 = df.cross(vr)
    vr2.normalize()
    p5 = p1 + vr * w + vr2 * w * TAN_PI_3
    p6 = p2 + vr * w + vr2 * w * TAN_PI_3
    res_lst = [
     (
      p1, color), (p2, color2), (p5, color), (p6, color2), (p3, color), (p4, color2), (p1, color), (p2, color2),
     (
      p6, color2), (p5, color), (p4, color2), (p3, color), (p2, color2), (p1, color), (p6, color2), (p5, color)]
    obj = world.primitives(scene)
    obj.create_triangle_strip(res_lst)
    holder.append(obj)


def drop_point(scene, holder, pos, color, h, w):
    pos = math3d.vector(*pos)
    x = w / 2.0 * math.tan(math.pi / 6)
    z = w / 2.0
    z2 = w / 2.0 / math.cos(math.pi / 6)
    p0 = math3d.vector(0, h, 0)
    p1 = math3d.vector(-x, 0, z)
    p2 = math3d.vector(-x, 0, -z)
    p3 = math3d.vector(z2, 0, 0)
    p0 = p0 + pos
    p1 = p1 + pos
    p2 = p2 + pos
    p3 = p3 + pos
    v0 = (
     p0, color)
    v1 = (p1, color)
    v2 = (p2, color)
    v3 = (p3, color)
    prim_1 = (
     v0, v1, v2)
    prim_2 = (v0, v2, v3)
    prim_3 = (v0, v3, v1)
    prim_4 = (v3, v2, v1)
    list_poly3 = [
     prim_1, prim_2, prim_3, prim_4]
    obj = world.primitives(scene)
    obj.create_poly3(list_poly3)
    holder.append(obj)


from collision import INCLUDE_FILTER
from logic.gcommon.common_const.collision_const import LAND_GROUP

def get_height(pos, scene):
    tp1 = math3d.vector(pos.x, 4000, pos.z)
    tp2 = math3d.vector(pos.x, -4000, pos.z)
    ret = scene.scene_col.hit_by_ray(tp1, tp2, 0, LAND_GROUP, LAND_GROUP, INCLUDE_FILTER)
    if ret and ret[0]:
        return ret[1].y + 1
    else:
        return None


def draw_grid(scene, holder, length, pos, color=13435085, offset=0):
    length = length / 2 - 1
    pos = math3d.vector(*pos)
    pos.y = get_height(pos, scene)
    pos.y = pos.y + 1
    p0 = math3d.vector(0, 0, length) + pos
    height = get_height(p0, scene)
    if height:
        p0.y = height + offset
    p1 = math3d.vector(length, 0, length) + pos
    height = get_height(p1, scene)
    if height:
        p1.y = height + offset
    p2 = math3d.vector(length, 0, 0) + pos
    height = get_height(p2, scene)
    if height:
        p2.y = height + offset
    p3 = math3d.vector(length, 0, -length) + pos
    height = get_height(p3, scene)
    if height:
        p3.y = height + offset
    p4 = math3d.vector(0, 0, -length) + pos
    height = get_height(p4, scene)
    if height:
        p4.y = height + offset
    p5 = math3d.vector(-length, 0, -length) + pos
    height = get_height(p5, scene)
    if height:
        p5.y = height + offset
    p6 = math3d.vector(-length, 0, 0) + pos
    height = get_height(p6, scene)
    if height:
        p6.y = height + offset
    p7 = math3d.vector(-length, 0, length) + pos
    height = get_height(p7, scene)
    if height:
        p7.y = height + offset
    v = (pos, color)
    v0 = (p0, color)
    v1 = (p1, color)
    v2 = (p2, color)
    v3 = (p3, color)
    v4 = (p4, color)
    v5 = (p5, color)
    v6 = (p6, color)
    v7 = (p7, color)
    g1 = (
     v, v0, v1, v2)
    g2 = (v, v2, v3, v4)
    g3 = (v, v4, v5, v6)
    g4 = (v, v6, v7, v0)
    obj = world.primitives(scene)
    obj.create_poly4([g1, g2, g3, g4])
    holder.append(obj)