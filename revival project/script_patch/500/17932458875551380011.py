# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/skill/client/SkillPVEIceShooter.py
from __future__ import absolute_import
import world
import math3d
import collision
import random
from math import pi, sin, cos
from .SkillBase import SkillBase
from common.cfg import confmgr
from logic.gcommon.const import NEOX_UNIT_SCALE
from logic.gcommon.common_const.collision_const import GROUP_DYNAMIC_SHOOTUNIT, GROUP_CHARACTER_INCLUDE, WATER_GROUP, WATER_MASK
from logic.gcommon.common_const.idx_const import ExploderID

class SkillPVEIceShooter(SkillBase):

    def __init__(self, skill_id, unit_obj, data):
        super(SkillPVEIceShooter, self).__init__(skill_id, unit_obj, data)
        ext_info = confmgr.get('skill_conf', str(self._skill_id), 'ext_info', default={})
        self.valid_target_dist = ext_info.get('valid_target_dist', 60) * NEOX_UNIT_SCALE
        self._fire_socket = ext_info.get('fire_socket', 'part_point1')

    def remote_do_skill(self, skill_data):
        model = self._unit_obj.ev_g_model()
        if not model or not model.valid:
            return
        else:
            socket = self._fire_socket
            fire_socket_follow_wp_pos = skill_data.get('fire_socket_follow_wp_pos', None)
            if fire_socket_follow_wp_pos:
                follow_status_inf = self._unit_obj.ev_g_gun_status_inf(fire_socket_follow_wp_pos)
                if follow_status_inf:
                    wp_socket = follow_status_inf.get_fired_socket_name()
                    if wp_socket:
                        socket = wp_socket
            if socket and model.has_socket(socket):
                position = model.get_socket_matrix(socket, world.SPACE_TYPE_WORLD).translation
            else:
                position = model.position
            if skill_data.get('random_target', False):
                fire_dir = self.get_random_target(position)
                if not fire_dir:
                    fire_dir = random.random() * 2 * pi
                    fire_dir = math3d.vector(cos(fire_dir), 0, sin(fire_dir))
            else:
                fire_dir = self.get_cam_dir() - position
            if not fire_dir.is_zero:
                fire_dir.normalize()
            throw_item = {'uniq_key': ExploderID.gen(global_data.battle_idx),
               'position': (
                          position.x, position.y, position.z),
               'm_position': (
                            position.x, position.y, position.z),
               'dir': (
                     fire_dir.x, fire_dir.y, fire_dir.z),
               'up': (0, 1, 0),
               'use_rot_mat': 1
               }
            self._unit_obj.send_event('E_CALL_SYNC_METHOD', 'do_skill', [self._skill_id, (throw_item, 0)], True)
            return

    def get_cam_dir(self):
        group = GROUP_CHARACTER_INCLUDE & ~WATER_GROUP
        mask = GROUP_CHARACTER_INCLUDE & ~WATER_MASK
        scn = world.get_active_scene()
        camera = scn.active_camera
        ori_forward = camera.rotation_matrix.forward
        start_pos = camera.position + ori_forward * 3 * NEOX_UNIT_SCALE
        end_pos = start_pos + ori_forward * 1000 * NEOX_UNIT_SCALE
        result = scn.scene_col.hit_by_ray(start_pos, end_pos, 0, group, mask, collision.INCLUDE_FILTER, False)
        if result[0]:
            end_pos = result[1]
        return end_pos

    def get_random_target(self, position):
        scn = global_data.game_mgr.scene
        if not scn:
            return
        else:
            check_obj = collision.col_object(collision.SPHERE, math3d.vector(self.valid_target_dist, self.valid_target_dist, self.valid_target_dist))
            check_obj.position = position
            result = scn.scene_col.static_test(check_obj, 65535, GROUP_DYNAMIC_SHOOTUNIT, collision.INCLUDE_FILTER)
            if not result:
                return
            nearby_units = []
            fire_dirs = []
            for cobj in result:
                cid = cobj.cid
                unit_obj = global_data.emgr.scene_find_unit_event.emit(cid)[0]
                if not unit_obj or unit_obj in nearby_units or not unit_obj.sd.ref_is_pve_monster or unit_obj.ev_g_death():
                    continue
                nearby_units.append(unit_obj)
                unit_model = unit_obj.ev_g_model()
                if unit_model and unit_model.valid:
                    mat = None
                    if unit_model.has_socket('fx_buff'):
                        mat = unit_model.get_socket_matrix('fx_buff', world.SPACE_TYPE_WORLD)
                    if mat:
                        unit_pos = mat.translation
                    else:
                        unit_pos = unit_obj.ev_g_model_position() + math3d.vector(0, 0.5 * NEOX_UNIT_SCALE, 0)
                    fdir = unit_pos - position
                    if fdir.length_sqr < self.valid_target_dist * self.valid_target_dist:
                        fire_dirs.append(fdir)

            if not fire_dirs:
                return
            return fire_dirs[random.randrange(len(fire_dirs))]