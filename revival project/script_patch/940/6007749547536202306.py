# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/com_human_appearance/ComSprayMaker.py
from __future__ import absolute_import
from __future__ import print_function
from logic.gcommon.component.UnitCom import UnitCom
from logic.gcommon.const import NEOX_UNIT_SCALE
from logic.gcommon.common_const import collision_const
from time import time
import math3d
import collision
import math

class ComSprayMaker(UnitCom):
    BIND_EVENT = {'E_SPRAY': 'try_spray'
       }

    def __init__(self):
        super(ComSprayMaker, self).__init__()

    def init_from_dict(self, unit_obj, bdict):
        super(ComSprayMaker, self).init_from_dict(unit_obj, bdict)
        self.forward_check_distance = 20 * NEOX_UNIT_SCALE
        self.last_spray_time = 0
        self.spray_interval = 3
        self.spray_id_list = []
        self.min_vertical_sin = math.sin(math.pi / 3)

    def try_spray(self, idx):
        cnt_time = time()
        print('make spray by item_no', idx)
        if cnt_time - self.last_spray_time <= self.spray_interval:
            return
        if not self.scene and global_data.battle:
            return
        right = self.ev_g_model_right()
        if not right:
            return
        if not global_data.cam_world_transform:
            return
        cam_pos = global_data.cam_world_transform.translation
        cam_forward = global_data.cam_world_transform.forward
        check_end = cam_forward * (self.forward_check_distance * 2) + cam_pos
        self.send_event('E_SUCCESS_INTERACTION')
        result = self.scene.scene_col.hit_by_ray(cam_pos, check_end, 0, collision_const.GROUP_STATIC_SHOOTUNIT, 65535, collision.INCLUDE_FILTER, False)
        if result[0]:
            spray_normal = result[2]
            spray_position = result[1]
            spray_forward = right.cross(spray_normal)
            print('spray normal is', spray_normal)
            if abs(spray_normal.y) < self.min_vertical_sin:
                spray_forward = math3d.vector(0, 1, 0)
            spray_forward = spray_normal.cross(spray_forward)
            spray_rotation = math3d.matrix.make_orient(spray_forward, -spray_normal)
            spray_euler = math3d.matrix_to_euler(spray_rotation)
            self._do_spray(idx, spray_position, spray_euler, {})
            from mobile.common.IdManager import IdManager
            spray_dict = {'position': (
                          spray_position.x, spray_position.y, spray_position.z),
               'rotation_euler': (
                                spray_euler.x, spray_euler.y, spray_euler.z),
               'spray_idx': idx
               }
            print('original spray dict', spray_dict)
        else:
            return
        self.last_spray_time = cnt_time

    def _do_spray(self, spray_id, v3d_pos, v3d_elr_rot, ex_data):
        lst_pos = (
         v3d_pos.x, v3d_pos.y, v3d_pos.z)
        lst_elr_rot = (v3d_elr_rot.x, v3d_elr_rot.y, v3d_elr_rot.z)
        self.send_event('E_CALL_SYNC_METHOD', 'add_spray', (spray_id, lst_pos, lst_elr_rot, ex_data), True)