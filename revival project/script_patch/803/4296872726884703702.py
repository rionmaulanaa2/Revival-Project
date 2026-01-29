# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/parts/PartMarkManager.py
from __future__ import absolute_import
import six
from . import ScenePart
from common.cfg import confmgr
import math3d
import world
import collision
from logic.gcommon import time_utility
from logic.gcommon.common_const.collision_const import GROUP_CHARACTER_EXCLUDE, BUILDING_GROUP, GROUP_CAMERA_INCLUDE, GROUP_SHOOTUNIT

class PartMarkManager(ScenePart.ScenePart):
    INIT_EVENT = {'scene_add_mark': 'add_common_mark',
       'scene_del_mark': 'del_common_mark'
       }

    def __init__(self, scene, name):
        super(PartMarkManager, self).__init__(scene, name)
        self.scene_mark = {}
        self.scene_mark_ext = {}
        self.scene_mark_col = {}

    def add_common_mark(self, mark_id, mark_no, point, is_deep, state, create_timestamp, deep_timestamp):
        if mark_id in self.scene_mark:
            return
        else:
            pass_time = time_utility.get_time() - create_timestamp
            scene_res_info = confmgr.get('mark_data', str(mark_no))
            scene_res_path = scene_res_info.get('scene_res', None)
            scene_res_ext_list = eval(scene_res_info.get('scene_res_ext', '[]'))
            if scene_res_path:
                pos = math3d.vector(*point)

                def create_cb(sfx):
                    if scene_res_ext_list:
                        self.ajust_surface(sfx, pos)

                sid = global_data.sfx_mgr.create_sfx_in_scene(scene_res_path, pos, on_create_func=create_cb)
                self.scene_mark[mark_id] = sid
                if scene_res_ext_list:
                    self.scene_mark_ext[mark_id] = []

                    def create_res_ext_cb(sfx):
                        sfx_pass_tim = pass_time
                        if sfx_pass_tim > sfx.life_span:
                            sfx_pass_tim = sfx.life_span
                        sfx.set_curtime_directly(sfx_pass_tim)

                    for scene_res_ext in scene_res_ext_list:
                        ext_sid = global_data.sfx_mgr.create_sfx_in_scene(scene_res_ext, pos, on_create_func=create_res_ext_cb)
                        self.scene_mark_ext[mark_id].append(ext_sid)

                col = collision.col_object(collision.SPHERE, math3d.vector(10, 10, 10), 0, 0, 0, True)
                col.mask = GROUP_CHARACTER_EXCLUDE ^ GROUP_CAMERA_INCLUDE ^ GROUP_SHOOTUNIT
                col.group = BUILDING_GROUP ^ GROUP_SHOOTUNIT
                col.car_undrivable = True
                pos = math3d.vector(pos)
                col.position = pos
                scn = world.get_active_scene()
                scn.scene_col.add_object(col)
                self.scene_mark_col[mark_id] = col
            return

    def del_common_mark(self, mark_id):
        if mark_id in self.scene_mark:
            global_data.sfx_mgr.remove_sfx_by_id(self.scene_mark[mark_id])
            del self.scene_mark[mark_id]
        if mark_id in self.scene_mark_ext:
            scene_ext_list = self.scene_mark_ext[mark_id]
            for ext_id in scene_ext_list:
                global_data.sfx_mgr.remove_sfx_by_id(ext_id)

            del self.scene_mark_ext[mark_id]
        if mark_id in self.scene_mark_col:
            scn = world.get_active_scene()
            scn.scene_col.remove_object(self.scene_mark_col[mark_id])
            self.scene_mark_col[mark_id] = None
            del self.scene_mark_col[mark_id]
        return

    def on_exit(self):
        for _, sid in six.iteritems(self.scene_mark):
            global_data.sfx_mgr.remove_sfx_by_id(sid)

        self.scene_mark = {}
        for _, sid_list in six.iteritems(self.scene_mark_ext):
            for sid in sid_list:
                global_data.sfx_mgr.remove_sfx_by_id(sid)

        self.scene_mark_ext = {}

    def ajust_surface(self, sfx, pos):
        from logic.gcommon.common_const.collision_const import GROUP_CHARACTER_INCLUDE
        start_pos, end_pos = math3d.vector(pos), math3d.vector(pos)
        start_pos.y += 20
        end_pos.y -= 20
        group = GROUP_CHARACTER_INCLUDE
        scene = world.get_active_scene()
        hit = scene.scene_col.hit_by_ray(start_pos, end_pos, 0, group, group, collision.INCLUDE_FILTER)
        if hit[0]:
            normal = hit[2]
            right = sfx.rotation_matrix.forward.cross(normal)
            forward = normal.cross(right)
            sfx.rotation_matrix = math3d.matrix.make_orient(forward, normal)