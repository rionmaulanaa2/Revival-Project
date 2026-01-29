# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/parts/PartAdaptiveNearClip.py
from __future__ import absolute_import
from six.moves import range
from . import ScenePart
import math3d
import math
import collision
from logic.client.const.camera_const import ADAPTIVE_Z_DIST
from logic.gcommon.common_const.collision_const import WATER_GROUP
import logic.gcommon.cdata.status_config as status_config

class PartAdaptiveNearClip(ScenePart.ScenePart):
    INIT_EVENT = {'camera_on_start_nearclip': 'start',
       'camera_on_stop_nearclip': 'stop'
       }
    ENTER_EVENT = {'net_login_reconnect_event': '_on_net_reconnect'
       }

    def __init__(self, scene, name):
        import device_compatibility
        super(PartAdaptiveNearClip, self).__init__(scene, name)
        self._timer1 = None
        self._near_save = 1
        self._valid = False
        self.min_distance = 1
        self.max_distance = 20
        self.min_water_distance = 3
        self.character_offset_z = 3
        self.water_excluded_group_mask = 65535 & ~WATER_GROUP
        if device_compatibility.IS_DX:
            self._near_dis_rate = 0.35
            self.min_aim_distance = 7
        else:
            self._near_dis_rate = 0.75
            self.min_aim_distance = 10
        self._sweep_cols = []
        self._static_cols = []
        self._static_scale = ()
        self._cur_static_id = 0
        self._static_id_max = 0
        self._cur_static_start = 0
        self._last_static_test = True
        self._sweep_test_start = 0
        return

    def on_enter(self):
        self._valid = True
        self.start(*ADAPTIVE_Z_DIST)

    def _on_net_reconnect(self, *args):
        self.start(*ADAPTIVE_Z_DIST)

    def stop(self):
        if self._timer1 is not None:
            global_data.game_mgr.get_post_logic_timer().unregister(self._timer1)
            self._timer1 = None
        if self._valid:
            self.scene().active_camera.z_range = (
             self._near_save, self.scene().active_camera.z_range[1])
        self._sweep_cols = []
        self._static_cols = []
        self._static_scale = ()
        self._cur_static_id = 0
        self._static_id_max = 0
        self._cur_static_start = 0
        self._last_static_test = True
        self._sweep_test_start = 0
        return

    def start(self, min_distance=ADAPTIVE_Z_DIST[0], max_distance=ADAPTIVE_Z_DIST[1]):
        if not self._valid:
            return
        self.stop()
        cam = self.scene().active_camera
        near = cam.z_range[0]
        self._near_save = near
        self.max_distance = max_distance
        self.min_distance = min_distance
        self._timer1 = global_data.game_mgr.get_post_logic_timer().register(func=self._tick, interval=1)
        unit_height = math.tan(math.radians(cam.fov / 2)) * 2.0
        unit_width = cam.aspect * unit_height
        half_h = unit_height / 2
        half_w = unit_width / 2
        step = max_distance / 6.0
        self._sweep_cols = []
        static_scale = (1.0, 0.667, 0.5)
        for scale in static_scale:
            d = max_distance * scale
            col = collision.col_object(collision.BOX, math3d.vector(half_w * d, half_h * d, d / 2))
            self._static_cols.append(col)

        self._static_scale = static_scale
        self._static_id_max = len(static_scale) - 1
        total_dist = 0
        for i in range(1, 4):
            dist = step * i
            total_dist = dist + total_dist
            col = collision.col_object(collision.BOX, math3d.vector(half_w * total_dist, half_h * total_dist, 1))
            self._sweep_cols.append((col, dist))

    def _tick(self):
        if not self._valid:
            return
        scn = self.scene()
        cam = scn.active_camera
        forward = cam.transformation.forward
        rot_mat = cam.rotation_matrix
        cam_pos = cam.position
        scene_col = scn.scene_col
        start_pos = cam_pos
        now = global_data.game_time
        if self._cur_static_id and now - self._cur_static_start > 10:
            self._cur_static_id -= 1
            self._cur_static_start = now
        col_obj = self._static_cols[self._cur_static_id]
        last_near = self.max_distance * self._static_scale[self._cur_static_id]
        col_obj.rotation_matrix = rot_mat
        col_obj.position = cam_pos + forward * last_near * 0.5
        if scene_col.static_test(col_obj, self.water_excluded_group_mask, self.water_excluded_group_mask, collision.INCLUDE_FILTER):
            if self._last_static_test:
                self._last_static_test = False
                self._sweep_test_start = now
            last_near = 0
            for test_col, dist in self._sweep_cols:
                test_col.rotation_matrix = rot_mat
                end_pos = start_pos + forward * dist
                ret = scene_col.sweep_test(test_col, start_pos, end_pos, self.water_excluded_group_mask, self.water_excluded_group_mask, 0, collision.INCLUDE_FILTER)
                if ret[0]:
                    last_near = max(self.min_distance, ret[3] * dist + last_near)
                    break
                else:
                    last_near = dist + last_near
                start_pos = end_pos

            if now - self._sweep_test_start > 1:
                if self._cur_static_id < self._static_id_max:
                    self._cur_static_id += 1
                self._cur_static_start = now
        else:
            self._last_static_test = True
        last_near = max(self.min_distance, last_near * self._near_dis_rate)
        if global_data.mecha and global_data.mecha.logic:
            is_aim = global_data.mecha.logic.sd.ref_in_open_aim
            if is_aim:
                last_near = max(self.min_aim_distance, last_near)
        elif global_data.player and global_data.player.logic:
            is_aim = global_data.player.logic.sd.ref_in_aim
            if is_aim:
                is_fire_blocked = global_data.player.logic.ev_g_fire_blocked()
                if not is_fire_blocked:
                    last_near = max(self.min_aim_distance, last_near)
            elif last_near > self.character_offset_z + 0.1:
                last_near -= self.character_offset_z
        if global_data.cam_lctarget and global_data.cam_lctarget.ev_g_is_diving():
            last_near = min(self.min_water_distance, last_near)
        elif global_data.cam_lplayer and global_data.cam_lplayer.ev_g_is_in_any_state((status_config.ST_SWIM,)):
            last_near = min(self.min_water_distance, last_near)
        cam.z_range = (max(global_data.min_adaptive_near, last_near), cam.z_range[1])

    def on_exit(self):
        self.stop()
        self._valid = False
        super(PartAdaptiveNearClip, self).on_exit()