# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComAtkTrackAppearance.py
from __future__ import absolute_import
import world
import collision
from ..UnitCom import UnitCom
from common.cfg import confmgr
from common.framework import Functor
from logic.gcommon.const import NEOX_UNIT_SCALE
from logic.gcommon.cdata.status_config import ST_SHOOT
from logic.gcommon.common_const.collision_const import GROUP_CHARACTER_INCLUDE, GROUP_CHARACTER_EXCLUDE, WATER_GROUP, WATER_MASK
MAX_AIM_DISTANCE = 1000 * NEOX_UNIT_SCALE
TRACK_GROUP = GROUP_CHARACTER_INCLUDE & ~WATER_GROUP
TRACK_MASK = GROUP_CHARACTER_INCLUDE & ~WATER_MASK

class ComAtkTrackAppearance(UnitCom):
    BIND_EVENT = {'E_SUCCESS_RIGHT_AIM': 'on_right_aim',
       'E_FINISH_QUIT_RIGHT_AIM': 'on_quit_right_aim'
       }

    def __init__(self):
        super(ComAtkTrackAppearance, self).__init__()
        self._timer = 0
        self.hook_model = None
        self._hook_model_id = None
        self._cur_weapon_model = None
        self.throw_track_visible = False
        self.is_bind_socket = True
        return

    def destroy(self):
        self.unregister_timer()
        self.clear_model()
        super(ComAtkTrackAppearance, self).destroy()

    def init_from_dict(self, unit_obj, bdict):
        super(ComAtkTrackAppearance, self).init_from_dict(unit_obj, bdict)

    def register_timer(self):
        from common.utils.timer import CLOCK
        self.unregister_timer()
        self._timer = global_data.game_mgr.get_logic_timer().register(func=self.timer_update, interval=0.033, mode=CLOCK)

    def unregister_timer(self):
        if self._timer > 0:
            global_data.game_mgr.get_logic_timer().unregister(self._timer)
        self._timer = 0

    def on_right_aim(self):
        if global_data.player and self.unit_obj != global_data.player.logic:
            return
        obj_weapon = self.sd.ref_wp_bar_cur_weapon
        if not obj_weapon:
            return
        self.register_timer()
        self.create_model()
        self.throw_track_visible = True

    def on_quit_right_aim(self):
        if global_data.player and self.unit_obj != global_data.player.logic:
            return
        self.unregister_timer()
        self.need_update = False
        self.throw_track_visible = False
        if self.hook_model:
            self.hook_model.visible = False

    def create_model(self):
        weapon_model = self.ev_g_get_weapon_model()
        self._cur_weapon_model = weapon_model

        def create_cb(model, *args):
            self.hook_model = model
            self.hook_model.visible = self.throw_track_visible

        path = 'effect/fx/weapon/qingjiqiang/lmg_hongwaixian.sfx'
        if not self._hook_model_id:
            self._hook_model_id = global_data.sfx_mgr.create_sfx_on_model(path, self._cur_weapon_model, 'fx_hongwaixian', type=world.BIND_TYPE_ALL, on_create_func=create_cb)
        if self.hook_model:
            self.hook_model.visible = True

    def clear_model(self):
        if self._hook_model_id is not None:
            global_data.model_mgr.remove_model_by_id(self._hook_model_id)
        self.hook_model = None
        self._hook_model_id = None
        return

    def timer_update(self):
        if not self.ev_g_status_check_pass(ST_SHOOT):
            if self.throw_track_visible:
                self.throw_track_visible = False
                if self.hook_model:
                    self.hook_model.visible = False
        elif not self.throw_track_visible:
            self.throw_track_visible = True
            if self.hook_model:
                self.hook_model.visible = True
        if self.hook_model and self.throw_track_visible:
            scn = self.scene
            weapon_model = self._cur_weapon_model
            if self.is_bind_socket:
                mat = weapon_model.get_socket_matrix('fx_hongwaixian', world.SPACE_TYPE_WORLD)
                camera_pos = mat.translation
                forward = mat.forward
            else:
                mat = weapon_model.get_socket_matrix('fx_hongwaixian', world.SPACE_TYPE_WORLD)
                camera = scn.active_camera
                camera_pos, forward, up_dir = self._on_get_camera_param()
            new_end_pos = camera_pos + forward * MAX_AIM_DISTANCE
            fire_pos = mat.translation
            result = scn.scene_col.hit_by_ray(camera_pos, new_end_pos, 0, TRACK_GROUP, TRACK_MASK, collision.INCLUDE_FILTER, False)
            m_mat = self.hook_model.world_rotation_matrix
            if result[0]:
                pos, normal = result[1], result[2]
                self.hook_model.end_pos = pos
                dir_vec = pos - fire_pos
                dir_vec.normalize()
                self.hook_model.world_rotation_matrix = m_mat.make_rotation_x(dir_vec.pitch) * m_mat.make_rotation_y(dir_vec.yaw)
            else:
                self.hook_model.end_pos = new_end_pos
                dir_vec = new_end_pos - fire_pos
                dir_vec.normalize()
                self.hook_model.world_rotation_matrix = m_mat.make_rotation_x(dir_vec.pitch) * m_mat.make_rotation_y(dir_vec.yaw)

    def _on_get_camera_param(self):
        if self.unit_obj == global_data.cam_lctarget:
            scn = self.scene
            partcamera = scn.get_com('PartCamera')
            if partcamera:
                camera = partcamera.cam if 1 else None
                return camera or (None, None, None)
            matrix = self._get_cam_trans()
            camera_pos = camera.world_position
            camera_direction = matrix.forward
            return (
             camera_pos, camera_direction, matrix.up)
        else:
            return (None, None, None)

    def _get_cam_trans(self):
        from logic.client.const import camera_const
        scn = self.scene
        partcamera = scn.get_com('PartCamera')
        camera = partcamera.cam
        cameradata = partcamera.cam_manager.last_camera_state_setting
        matrix = None
        if cameradata:
            cameradata['type']
            if partcamera.get_cur_camera_state_type() == camera_const.FREE_MODEL:
                matrix = cameradata['trans']
                self._last_cam_trans = matrix
            elif partcamera.is_out_cam_state_slerp(camera_const.FREE_MODEL):
                matrix = self._last_cam_trans
        if matrix is None:
            matrix = camera.world_rotation_matrix
        return matrix