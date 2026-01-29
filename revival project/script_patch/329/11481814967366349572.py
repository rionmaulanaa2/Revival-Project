# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/parts/PoisonCircleManager.py
from __future__ import absolute_import
import math3d
import world
import render
import game3d
import math
import common.utils.timer as timer
import logic.gcommon.const as const
from logic.gcommon import time_utility
import logic.gcommon.common_const.scene_const as scene_const
from logic.gcommon.common_const import poison_circle_const
from logic.gcommon.common_utils import battle_utils
from . import PoisonDamageViewMgr
import common.utilities
from common.cfg import confmgr
CIRCLE_SCALE = 1.0
_HASH_visible_distance = game3d.calc_string_hash('visible_distance')
_HASH_player_pos = game3d.calc_string_hash('player_pos')
_HASH_poison_radius = game3d.calc_string_hash('poison_radius')
_HASH_poison_scale = game3d.calc_string_hash('poison_scale')
CIRCLE_MAX_VISIBLE_DISTANCE = 400 * const.NEOX_UNIT_SCALE
CIRCLE_HIDE_DISTANCE = CIRCLE_MAX_VISIBLE_DISTANCE + 20 * const.NEOX_UNIT_SCALE

class PoisonCircleManager(object):

    def __init__(self):
        self._poison_damage_view = PoisonDamageViewMgr.PoisonDamageViewMgr(self)
        self._circle = None
        self._original_pos = None
        self._original_r = None
        self._target_pos = None
        self._target_r = None
        self._cur_time = 0.0
        self._last_time = 0.0
        self._start_time = 0.0
        self._cur_circle_r = 0.0
        self._cur_circle_pos = None
        self._poison_to_player_vector = None
        self._poison_close_radius = 0.0
        self._circle_timer = None
        self.level = 0
        self.state = None
        self.delay_exec_id = None
        self._scene = world.get_active_scene()
        self.register_event()
        self.reduce_type = poison_circle_const.POISON_REDUCE_SHRINK
        return

    def get_cnt_circle_info(self):
        return {'level': self.level,
           'harm_center': self._cur_circle_pos,
           'harm_radius': self._cur_circle_r,
           'safe_center': self._target_pos,
           'safe_radius': self._target_r,
           'start_time': self._start_time,
           'last_time': self._last_time,
           'state': self.state,
           'is_inside': self.is_inside(),
           'original_radius': self._original_r,
           'original_center': self._original_pos,
           'reduce_type': self.reduce_type
           }

    def register_event(self, bind=True):
        econf = {'scene_refresh_poison_circle_event': self.start_circle_callback,
           'scene_reduce_poison_circle_event': self.update_circle_callback,
           'scene_clear_poison_circle_event': self.clear_poision_circle_callback
           }
        if bind:
            global_data.emgr.bind_events(econf)
            battle_utils.register_local_player_pos_callback(self, self.refresh_circle)
        else:
            global_data.emgr.unbind_events(econf)
            battle_utils.unregister_local_player_pos_callback(self)

    def start_circle_callback(self, state, refresh_time, last_time, level, posion_point, safe_point, reduce_type):
        self.level = level
        self.state = state
        self._start_time = refresh_time
        self._last_time = last_time
        self.reduce_type = reduce_type
        start_pos = math3d.vector(posion_point[0], -30.0, posion_point[1])
        target_pos = math3d.vector(safe_point[0], -30.0, safe_point[1])
        target_r = safe_point[2]
        self.start_circle(start_pos, posion_point[2], target_pos, target_r)
        global_data.emgr.scene_poison_updated_event.emit()

    def is_in_poison(self):
        if not global_data.cam_lplayer or not global_data.cam_lplayer.is_valid():
            return
        else:
            pos = global_data.cam_lplayer.ev_g_position()
            if pos is None:
                return
            if not self._cur_circle_pos or not self._cur_circle_r:
                return
            return (pos.x - self._cur_circle_pos.x) ** 2 + (pos.z - self._cur_circle_pos.z) ** 2 < self._cur_circle_r ** 2

    def update_circle_callback(self, state, refresh_time, last_time, reduce_type):
        self.state = state
        self.reduce_type = reduce_type
        self.update_circle(refresh_time, last_time)
        global_data.emgr.scene_poison_updated_event.emit()

    def clear_poision_circle_callback(self):
        self.clear_poison()

    def start_circle(self, start_pos, start_r, target_pos, target_r):
        if not self._circle:
            screen_posion_model_path = confmgr.get('script_gim_ref')['screen_effect_poison']
            self._circle = world.model(screen_posion_model_path, self._scene)
            self._circle.all_materials.set_var(_HASH_visible_distance, 'visible_distance', CIRCLE_MAX_VISIBLE_DISTANCE)
            self._circle.all_materials.set_var(_HASH_poison_scale, 'poison_scale', CIRCLE_SCALE)
            self._poison_close_radius = self._circle.bounding_box.x / 3.1415926
            self._cur_circle_pos = start_pos + math3d.vector(0, -40 * const.NEOX_UNIT_SCALE, 0)
            self._cur_circle_r = start_r
            self._poison_damage_view.start_check()
        self._original_pos = start_pos + math3d.vector(0, -40 * const.NEOX_UNIT_SCALE, 0)
        self._original_r = start_r
        self._target_pos = target_pos + math3d.vector(0, -40 * const.NEOX_UNIT_SCALE, 0)
        self._target_r = target_r
        if self._circle_timer:
            global_data.game_mgr.unregister_logic_timer(self._circle_timer)
            self._circle_timer = None
        player_pos = self.get_player_pos()
        self.refresh_circle(player_pos)
        return

    def update_circle(self, start_time, last_time):
        if not self._circle:
            return
        else:
            self._start_time = start_time
            self._cur_time = time_utility.time() - self._start_time
            self._last_time = last_time
            if self._circle_timer:
                global_data.game_mgr.unregister_logic_timer(self._circle_timer)
                self._circle_timer = None
            self._circle_timer = global_data.game_mgr.register_logic_timer(self._circle_timer_callback, interval=1, times=-1, mode=timer.LOGIC)
            return

    def clear_poison(self):
        self.state = poison_circle_const.POISON_CIRCLE_STATE_OVER
        self._cur_circle_pos = math3d.vector(0, -30.0, 0)
        self._cur_circle_r = const.NEOX_UNIT_SCALE * 3000
        self._target_pos = math3d.vector(0, -30.0, 0)
        self._target_r = const.NEOX_UNIT_SCALE * 3000
        self.reduce_type = poison_circle_const.POISON_REDUCE_SHRINK
        if self._circle_timer:
            global_data.game_mgr.unregister_logic_timer(self._circle_timer)
            self._circle_timer = None
        if self._circle and self._circle.valid:
            self._circle.destroy()
            self._circle = None
        self.register_event(False)
        if self._poison_damage_view:
            if global_data.cam_lplayer:
                global_data.cam_lplayer.send_event('E_GUIDE_POISON', False)
                global_data.cam_lplayer.send_event('E_IN_POISON', False)
        self._poison_damage_view and self._poison_damage_view.destroy()
        self._poison_damage_view = None
        global_data.emgr.scene_poison_updated_event.emit()
        return

    def _circle_timer_callback(self):
        if not self._circle:
            return
        else:
            self._cur_time = time_utility.time() - self._start_time
            if self._cur_time >= self._last_time:
                global_data.game_mgr.unregister_logic_timer(self._circle_timer)
                self._circle_timer = None
                self._cur_time = self._last_time
            if self.state >= poison_circle_const.POISON_CIRCLE_STATE_REDUCE:
                rate = self._cur_time / self._last_time if self._last_time != 0 else 1
                if rate < 0.0:
                    rate = 0.0
                elif rate > 1.0:
                    rate = 1.0
                self._cur_circle_pos = self._original_pos + (self._target_pos - self._original_pos) * rate
                self._cur_circle_r = self._original_r + (self._target_r - self._original_r) * rate
            else:
                self._cur_circle_r = self._original_r
                self._cur_circle_pos = self._original_pos
            player_pos = self.get_player_pos()
            self.refresh_circle(player_pos)
            if self._scene.valid:
                self._scene.set_poison_info(self._cur_circle_pos.x, self._cur_circle_pos.y, self._cur_circle_pos.z, self._cur_circle_r)
            return

    def refresh_circle(self, player_pos):
        if self._circle and self._circle.valid:
            circle_vect = player_pos - self._cur_circle_pos
            circle_vect.y = 0.0
            if abs(circle_vect.length - self._cur_circle_r) > CIRCLE_HIDE_DISTANCE:
                self._circle.visible = False
                self._poison_to_player_vector = None
                return
            self._circle.visible = True
            if not self._poison_to_player_vector or self._cur_circle_r > self._poison_close_radius:
                circle_radian = common.utilities.vector_radian(circle_vect) + math.pi
                self._circle.rotation_matrix = math3d.matrix.make_rotation_y(circle_radian)
                if not circle_vect.is_zero:
                    circle_vect.normalize()
                else:
                    circle_vect = math3d.vector(0, 0, 1)
                self._poison_to_player_vector = circle_vect
            else:
                circle_vect = self._poison_to_player_vector
            circle_pos = self._cur_circle_pos + circle_vect * self._cur_circle_r
            self._circle.position = circle_pos
            self._circle.all_materials.set_var(_HASH_player_pos, 'player_pos', (player_pos.x, player_pos.y, player_pos.z))
            self._circle.all_materials.set_var(_HASH_poison_radius, 'poison_radius', self._cur_circle_r)
            if self._cur_circle_r < self._poison_close_radius:
                scale = self._cur_circle_r / self._poison_close_radius
                self._circle.all_materials.set_var(_HASH_poison_scale, 'poison_scale', scale)
            else:
                self._circle.all_materials.set_var(_HASH_poison_scale, 'poison_scale', 1.0)
        return

    def get_player_pos(self):
        cam_lplayer = global_data.cam_lplayer
        if cam_lplayer:
            control_target = cam_lplayer.ev_g_control_target()
            if control_target and control_target.logic:
                pos = control_target.logic.ev_g_model_position()
            else:
                pos = cam_lplayer.ev_g_model_position()
            if pos:
                return pos
        elif global_data.is_in_judge_camera:
            if global_data.game_mgr.scene:
                return global_data.game_mgr.scene.active_camera.world_position
        return global_data.sound_mgr.get_listener_pos()

    def destroy(self):
        if self.delay_exec_id:
            game3d.cancel_delay_exec(self.delay_exec_id)
            self.delay_exec_id = None
        if self._circle_timer:
            global_data.game_mgr.unregister_logic_timer(self._circle_timer)
            self._circle_timer = None
        if self._circle and self._circle.valid:
            self._circle.destroy()
            self._circle = None
        self.register_event(False)
        self._poison_damage_view and self._poison_damage_view.destroy()
        self._poison_damage_view = None
        return

    def is_inside(self):
        return self._poison_damage_view and self._poison_damage_view._is_inside