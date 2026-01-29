# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComEnv.py
from __future__ import absolute_import
from ..UnitCom import UnitCom
from logic.gcommon.common_const.scene_const import MTL_HOUSE
import collision
from logic.gcommon.common_const.collision_const import GROUP_STATIC_SHOOTUNIT
import math3d
from logic.gcommon.const import NEOX_UNIT_SCALE
import common.utils.timer as timer
import game3d
import world
from logic.gcommon.common_const import animation_const
from logic.gcommon.component import UnitCom as UnitCom_file
from logic.gcommon.common_const import scene_const
from logic.gcommon.utility import dummy_cb
from common.utils.sfxmgr import CREATE_SRC_SIMPLE
CHECK_HEIGHT_OFFSET = math3d.vector(0, 30 * NEOX_UNIT_SCALE, 0)
CHECK_INTERVAL = 0.5
FADE_IN_LAST_TIMES = 30
SNOW_FOOTSTEP_MAX_DISTANCE_SQR = (20 * NEOX_UNIT_SCALE) ** 2
UNDER_SUN_CHECK_DISTANCE = 1000.0 * NEOX_UNIT_SCALE
_HASH_u_inside_sig = game3d.calc_string_hash('u_inside_sig')
MECHA_FOOTSTEP = [
 'effect/fx/scenes/common/snow/snow_jj_jiaoyin_zuo.sfx', 'effect/fx/scenes/common/snow/snow_jj_jiaoyin_you.sfx']
HUMAN_FOOTSTEP = ['effect/fx/scenes/common/snow/snow_rw_jiaoyin_zuo.sfx', 'effect/fx/scenes/common/snow/snow_rw_jiaoyin_you.sfx']
LEFT_FOOTSTEP = 0
RIGHT_FOOTSTEP = 1
MECH_CHECK_FOOT_STEP_OFFSET = math3d.vector(0.0, 1 * NEOX_UNIT_SCALE, 0.0)
HUMAN_CHECK_FOOT_STEP_OFFSET = math3d.vector(0.0, 0.3 * NEOX_UNIT_SCALE, 0.0)
DELAY_RESET = 2000

class ComEnv(UnitCom):
    BIND_EVENT = {'E_MODEL_LOADED': 'on_target_change',
       'E_CHANGE_WEAPON_MODEL': 'on_weapon_model_change',
       'E_MODEL_LOADED': 'on_model_loaded',
       'G_IS_IN_HOUSE': 'is_in_house'
       }

    def init_from_dict(self, unit_obj, bdict):
        super(ComEnv, self).init_from_dict(unit_obj, bdict)
        self._scene = global_data.game_mgr.scene
        self._last_in_house = False
        self.check_in_house_timer = None
        self.fade_out_timer = None
        self._last_under_sun = True
        self._last_uniform_data = (0.0, 1.0)
        self._part_camera = global_data.game_mgr.scene.get_com('PartCamera')
        self.delay_exec_id = None
        if self.sd.ref_is_mecha:
            self.foot_step_sfx = MECHA_FOOTSTEP
            self.check_foot_step_offset = MECH_CHECK_FOOT_STEP_OFFSET
        else:
            self.foot_step_sfx = HUMAN_FOOTSTEP
            self.check_foot_step_offset = HUMAN_CHECK_FOOT_STEP_OFFSET
        global_data.emgr.scene_camera_target_setted_event += self.on_target_change
        global_data.emgr.net_login_reconnect_event += self.on_login_reconnect
        if global_data.game_mode.is_snow_res():
            self.regist_event('E_FOOTSTEP_SMOKE', self.on_footstep_smoke_snow)
        else:
            self.regist_event('E_FOOTSTEP_SMOKE', self.on_footstep_smoke_normal)
        self.uniform_fade_to = self.uniform_fade_to_mecha if self.sd.ref_is_mecha else self.uniform_fade_to_human
        return

    def on_model_loaded(self, model):
        if global_data.game_mgr.gds.get_actual_quality() == 0:
            return

        def callback():
            if self.unit_obj == global_data.cam_lctarget:
                data = (
                 1.0 if self._last_in_house else 0.0, 1.0 if self._last_under_sun else 0.0)
                self.reset_uniform(data)
            self.delay_exec_id = None
            return

        if self.unit_obj == global_data.cam_lctarget:
            self.delay_exec_id = game3d.delay_exec(DELAY_RESET, callback)

    def on_target_change(self, *args):
        if self.unit_obj == global_data.cam_lctarget:
            if global_data.game_mgr.gds.get_actual_quality() == 0:
                if self.check_in_house_timer:
                    global_data.game_mgr.unregister_logic_timer(self.check_in_house_timer)
                    self.check_in_house_timer = None
            else:
                if not self.check_in_house_timer:
                    self.check_in_house_timer = global_data.game_mgr.register_logic_timer(self.tick, interval=CHECK_INTERVAL, times=-1, mode=timer.CLOCK)
                data = (1.0 if self._last_in_house else 0.0, 1.0 if self._last_under_sun else 0.0)
                self.reset_uniform(data)
        elif self.check_in_house_timer:
            global_data.game_mgr.unregister_logic_timer(self.check_in_house_timer)
            self.check_in_house_timer = None
            self.reset_uniform((0.0, 1.0))
        return

    def reset_uniform(self, data):
        model = self.ev_g_model()
        if model:
            model.all_materials.set_var(_HASH_u_inside_sig, 'u_inside_sig', data)
        if self.sd.ref_is_mecha:
            if self.sd.ref_socket_res_agent:
                for model_res in self.sd.ref_socket_res_agent.model_res_list:
                    model_res.all_materials.set_var(_HASH_u_inside_sig, 'u_inside_sig', data)

        else:
            weapon_model = self.sd.ref_hand_weapon_model
            if weapon_model:
                weapon_model.all_materials.set_var(_HASH_u_inside_sig, 'u_inside_sig', data)
            left_weapon_model = self.sd.ref_left_hand_weapon_model
            if left_weapon_model:
                left_weapon_model.all_materials.set_var(_HASH_u_inside_sig, 'u_inside_sig', data)

    def is_in_house(self):
        return self._last_in_house

    def tick(self):
        if not (self._scene and self._scene.valid):
            return False
        pos = self.ev_g_model_position()
        if not pos:
            return False
        dirty = False
        if not self.sd.ref_is_mecha:
            in_house = self.check_in_house(pos)
            if in_house != self._last_in_house:
                self._last_in_house = in_house
                dirty = True
                self.send_event('E_IN_HOUSE_STATE_CHANGE', in_house)
        under_sun = self.check_under_sun(pos)
        if self._last_under_sun != under_sun:
            self._last_under_sun = under_sun
            dirty = True
        if dirty:
            new_data = (1.0 if self._last_in_house else 0.0, 1.0 if self._last_under_sun else 0.0)
            self.uniform_fade_to(self._last_uniform_data, new_data)
            self._last_uniform_data = new_data

    def uniform_fade_to_human(self, from_value, to_value):
        model = self.ev_g_model()
        weapon_model = self.sd.ref_hand_weapon_model
        left_weapon_model = self.sd.ref_left_hand_weapon_model
        if self.fade_out_timer:
            global_data.game_mgr.unregister_logic_timer(self.fade_out_timer)
        self.count = 0

        def callback():
            self.count += 1
            rate = float(self.count) / FADE_IN_LAST_TIMES
            value_x = from_value[0] + (to_value[0] - from_value[0]) * rate
            value_y = from_value[1] + (to_value[1] - from_value[1]) * rate
            if model and model.valid:
                model.all_materials.set_var(_HASH_u_inside_sig, 'u_inside_sig', (value_x, value_y))
            if weapon_model and weapon_model.valid:
                weapon_model.all_materials.set_var(_HASH_u_inside_sig, 'u_inside_sig', (value_x, value_y))
            if left_weapon_model and left_weapon_model.valid:
                left_weapon_model.all_materials.set_var(_HASH_u_inside_sig, 'u_inside_sig', (value_x, value_y))

        self.fade_out_timer = global_data.game_mgr.register_logic_timer(callback, interval=1, times=FADE_IN_LAST_TIMES, mode=timer.LOGIC)

    def uniform_fade_to_mecha(self, from_value, to_value):
        model = self.ev_g_model()
        if self.fade_out_timer:
            global_data.game_mgr.unregister_logic_timer(self.fade_out_timer)
        self.count = 0

        def callback():
            self.count += 1
            rate = float(self.count) / FADE_IN_LAST_TIMES
            value_x = from_value[0] + (to_value[0] - from_value[0]) * rate
            value_y = from_value[1] + (to_value[1] - from_value[1]) * rate
            if model and model.valid:
                model.all_materials.set_var(_HASH_u_inside_sig, 'u_inside_sig', (value_x, value_y))
            if self.sd.ref_is_mecha:
                if self.sd.ref_socket_res_agent:
                    for model_res in self.sd.ref_socket_res_agent.model_res_list:
                        model_res.all_materials.set_var(_HASH_u_inside_sig, 'u_inside_sig', (value_x, value_y))

        self.fade_out_timer = global_data.game_mgr.register_logic_timer(callback, interval=1, times=FADE_IN_LAST_TIMES, mode=timer.LOGIC)

    def check_in_house(self, pos):
        scene_2d_info_value = self._scene.get_scene_info_2d(pos.x, pos.z)
        if scene_2d_info_value == MTL_HOUSE:
            end_pos = pos + CHECK_HEIGHT_OFFSET
            result = global_data.game_mgr.scene.scene_col.hit_by_ray(pos, end_pos, 0, GROUP_STATIC_SHOOTUNIT, 65535, collision.INCLUDE_FILTER, False)
            if result[0]:
                return True
        return False

    def check_under_sun(self, pos):
        pos_offset = self._part_camera.get_focus_point_y()
        check_pos = pos + math3d.vector(0.0, pos_offset, 0.0)
        if not self._scene.realtime_shadow_light:
            return False
        direction = -self._scene.realtime_shadow_light.direction
        result = self._scene.scene_col.hit_by_ray(check_pos, check_pos + direction * UNDER_SUN_CHECK_DISTANCE, 0, GROUP_STATIC_SHOOTUNIT, 65535, collision.INCLUDE_FILTER)
        return not result[0]

    def on_weapon_model_change(self, *args):
        new_data = (
         1.0 if self._last_in_house else 0.0, 1.0 if self._last_under_sun else 0.0)
        weapon_model = self.sd.ref_hand_weapon_model
        if weapon_model and weapon_model.valid:
            weapon_model.all_materials.set_var(_HASH_u_inside_sig, 'u_inside_sig', new_data)
        left_weapon_model = self.sd.ref_left_hand_weapon_model
        if left_weapon_model and left_weapon_model.valid:
            left_weapon_model.all_materials.set_var(_HASH_u_inside_sig, 'u_inside_sig', new_data)

    def on_login_reconnect(self, *args):
        if self.check_in_house_timer:
            global_data.game_mgr.unregister_logic_timer(self.check_in_house_timer)
            self.check_in_house_timer = global_data.game_mgr.register_logic_timer(self.tick, interval=CHECK_INTERVAL, times=-1, mode=timer.CLOCK)

    def destroy(self):
        self.need_update = False
        if self.check_in_house_timer:
            global_data.game_mgr.unregister_logic_timer(self.check_in_house_timer)
            self.check_in_house_timer = None
        if self.fade_out_timer:
            global_data.game_mgr.unregister_logic_timer(self.fade_out_timer)
            self.fade_out_timer = None
        if self.delay_exec_id:
            game3d.cancel_delay_exec(self.delay_exec_id)
        self.uniform_fade_to = dummy_cb
        super(ComEnv, self).destroy()
        return

    def on_footstep_smoke_normal(self, material_type, pos, length_sqr):
        if not self.sd.ref_finish_load_lod_model and not self.sd.ref_is_mecha:
            return
        footstep_sfx = scene_const.footstep_sfx_dic.get(material_type, '')
        if footstep_sfx:
            global_data.sfx_mgr.create_sfx_in_scene(footstep_sfx, pos, duration=3.0, int_check_type=CREATE_SRC_SIMPLE)

    def on_footstep_smoke_snow(self, material_type, pos, length_sqr):
        if material_type in ('road', 'ice'):
            return
        if not self._last_in_house:
            material_type = 'snow'
        if not self.sd.ref_finish_load_lod_model and not self.sd.ref_is_mecha:
            return
        footstep_sfx = scene_const.footstep_sfx_dic.get(material_type, '')
        if footstep_sfx:
            global_data.sfx_mgr.create_sfx_in_scene(footstep_sfx, pos, duration=3.0, int_check_type=CREATE_SRC_SIMPLE)
        if length_sqr < SNOW_FOOTSTEP_MAX_DISTANCE_SQR and not self._last_in_house:
            self.add_snow_footstep()

    def add_snow_footstep(self, *args):
        model = self.ev_g_model()
        if not model:
            return
        mat_l = model.get_bone_matrix('biped l foot', world.SPACE_TYPE_WORLD)
        mat_r = model.get_bone_matrix('biped r foot', world.SPACE_TYPE_WORLD)
        if mat_l.translation.y < mat_r.translation.y:
            foot_mat = mat_l
            foot_sfx = self.foot_step_sfx[LEFT_FOOTSTEP]
        else:
            foot_mat = mat_r
            foot_sfx = self.foot_step_sfx[RIGHT_FOOTSTEP]
        result = self._scene.scene_col.hit_by_ray(foot_mat.translation + self.check_foot_step_offset, foot_mat.translation - self.check_foot_step_offset, 0, GROUP_STATIC_SHOOTUNIT, 65535, collision.INCLUDE_FILTER, False)
        if result[0]:

            def on_create_func(sfx):
                rotation_mat = math3d.matrix.make_rotation_y(foot_mat.yaw)
                normal_mat = math3d.matrix.make_rotation_between(math3d.vector(0.0, 1.0, 0.0), result[2])
                sfx.rotation_matrix = rotation_mat * normal_mat

            global_data.sfx_mgr.create_sfx_in_scene(foot_sfx, result[1] + math3d.vector(0.0, 0.5, 0.0), on_create_func=on_create_func, int_check_type=CREATE_SRC_SIMPLE)