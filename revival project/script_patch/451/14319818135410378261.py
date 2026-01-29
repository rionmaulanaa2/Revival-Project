# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/com_mecha_effect/ComMechaEffect8033.py
from __future__ import absolute_import
from .ComGenericMechaEffect import ComGenericMechaEffect
from logic.gcommon.common_const.mecha_const import MECHA_PATTERN_NORMAL, MECHA_PATTERN_VEHICLE
from logic.gcommon.const import PART_WEAPON_POS_MAIN6
import logic.gcommon.common_utils.bcast_utils as bcast
from logic.gcommon.common_const import collision_const
from logic.gcommon.common_const.skill_const import SKILL_8033_SCAN
import collision
import world
import math3d
import weakref
END_STRIP_SFX = 'effect/fx/weapon/other/touzhi_biaoshi.sfx'
HUMAN_SCALE = 1.0
CAR_SCALE = 1.875
GUN_COL_SIZE = math3d.vector(64, 20, 12)
GUN_COL_OFFSET = (15, 0, -5)
GUN_BONE_NAME = 'gj_paoguan_root'
CAR_SHIELD_COL_INFO = (
 60, math3d.vector(-10, 0, 0))
CAR_SHOOT_COL_INFO = ([8, 7, 5.5], math3d.vector(-10, 0, 0))
CAR_VICE_WEAPON_ENERGY_FULL_STATE_ID = 'energy_full'
CAR_VICE_WEAPON_ENERGY_FULL_EFFECT_ID = '10'

class ComMechaEffect8033(ComGenericMechaEffect):
    WEAPON_KEYS = [
     'pedestal', 'gun']
    BIND_EVENT = ComGenericMechaEffect.BIND_EVENT.copy()
    BIND_EVENT.update({'E_CREATE_HOLD_EFFECT': 'on_trigger_hold_effect',
       'E_SCAN_ENEMY_8033': 'on_scan_enemy',
       'E_SHOW_GUN_8033': 'on_show_gun',
       'E_SET_MECAH_MODE': 'on_set_mecha_mode',
       'E_SET_GUN_PITCH_AND_YAW_8033': 'on_set_gun_model_pitch_and_yaw',
       'E_GUN_MODEL_ANI_8033': 'on_gun_model_ani',
       'E_ON_SKIN_SUB_MODEL_LOADED': 'on_skin_sub_model_loaded',
       'G_IGNORE_RECOVERY_ANIM': 'is_ignore_recovery_anim',
       'G_MECHA_MODE': 'get_mecha_mode',
       'E_ON_ACTION_ENTER_MECHA': 'on_enter_mecha',
       'E_ENERGY_CHANGE': 'on_energy_change',
       'E_FREE_CAMERA_SWITCH_FINISH': 'on_free_camera_switch_finish',
       'E_SHOW_BUFF_PROGRESS': 'on_show_dash_progress',
       'E_CLOSE_BUFF_PROGRESS': 'on_clsoe_dash_progress'
       })

    def init_from_dict(self, unit_obj, bdict):
        super(ComMechaEffect8033, self).init_from_dict(unit_obj, bdict)
        self.mecha_mode = bdict.get('shape_form', MECHA_PATTERN_NORMAL)
        self.sd.ref_is_car_shape = self.mecha_mode == MECHA_PATTERN_VEHICLE
        self.sd.ref_open_aim_weapon_pos = PART_WEAPON_POS_MAIN6
        self._model_ref = None
        self.cur_model_scale = HUMAN_SCALE
        self.target_model_scale = HUMAN_SCALE
        self.gun_rotation_progress = 0.0
        self.final_pitch = 0
        self.final_yaw = 0
        self.need_update = False
        self.sync_pitch_and_yaw = False
        self.gun_col = None
        self.gun_col_active = False
        self.car_vice_weapon_energy_full = False
        return

    def destroy(self):
        if self.gun_col:
            global_data.emgr.scene_remove_common_shoot_obj.emit(self.gun_col.cid)
            self.gun_col = None
        super(ComMechaEffect8033, self).destroy()
        return

    def is_ignore_recovery_anim(self):
        return self.mecha_mode == MECHA_PATTERN_VEHICLE

    def on_model_loaded(self, model):
        super(ComMechaEffect8033, self).on_model_loaded(model)
        self._model_ref = weakref.ref(model)
        if self.mecha_mode == MECHA_PATTERN_VEHICLE:
            self.cur_model_scale = CAR_SCALE
            self.target_model_scale = HUMAN_SCALE
        else:
            self.cur_model_scale = HUMAN_SCALE
            self.target_model_scale = CAR_SCALE
        model.scale = math3d.vector(self.cur_model_scale, self.cur_model_scale, self.cur_model_scale)
        self.on_set_mecha_mode(self.mecha_mode, True)
        self.on_energy_change(SKILL_8033_SCAN, self.ev_g_energy(SKILL_8033_SCAN))

    def on_skin_sub_model_loaded(self):
        if not self._model_ref:
            return
        model = self._model_ref()
        if not model:
            return
        self.gun_col = collision.col_object(collision.BOX, GUN_COL_SIZE * CAR_SCALE * 0.5, collision_const.GROUP_GRENADE | collision_const.GROUP_DYNAMIC_SHOOTUNIT, collision_const.GROUP_DYNAMIC_SHOOTUNIT, 0, False)
        if self.mecha_mode == MECHA_PATTERN_VEHICLE:
            self.show_gun()
            self.final_pitch = model.world_rotation_matrix.pitch
            self.final_yaw = model.world_rotation_matrix.yaw
            self.gun_rotation_progress = 1.0
            self.sync_pitch_and_yaw = True
            self.update_gun_model_pitch_and_yaw(1.0)
        else:
            self.hide_gun()
        gun_models = self.sd.ref_socket_res_agent.model_res_map.get('gun')
        if gun_models:
            self.sd.ref_aim_model = gun_models[0]

    def tick(self, delta):
        scale_stop = self.update_model_scale(delta)
        pitch_yaw_stop = self.update_gun_model_pitch_and_yaw(delta)
        if scale_stop and pitch_yaw_stop:
            self.need_update = False

    def on_scan_enemy(self):
        sfx_path = 'effect/fx/robot/common/saomiao_001.sfx'
        sfx_path1 = 'effect/fx/robot/common/saomiao_002.sfx'
        player_position = global_data.mecha.logic.ev_g_position()
        size = global_data.really_sfx_window_size
        scale = math3d.vector(size[0] / 1280.0, size[1] / 720.0, 1.0)

        def create_callback(sfx, scale=scale):
            sfx.scale = scale

        global_data.sfx_mgr.create_sfx_in_scene(sfx_path, on_create_func=create_callback)
        global_data.sfx_mgr.create_sfx_in_scene(sfx_path1, player_position)

    def on_show_gun(self, is_show):
        if is_show:
            self.show_gun()
        else:
            self.hide_gun()
        self.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', (bcast.E_SHOW_GUN_8033, (is_show,)), False, True)

    def _activate_gun_col(self, flag):
        if self.gun_col_active ^ flag:
            if flag:
                if self.sd.ref_socket_res_agent.model_res_map.get('gun'):
                    gun_model = self.sd.ref_socket_res_agent.model_res_map.get('gun')[0]
                    gun_model.bind_col_obj(self.gun_col, GUN_BONE_NAME)
                    self.gun_col.bone_matrix = math3d.matrix.make_translation(*GUN_COL_OFFSET)
                    global_data.emgr.scene_add_common_shoot_obj.emit(self.gun_col.cid, self.unit_obj)
                else:
                    return
            elif self.sd.ref_socket_res_agent.model_res_map.get('gun'):
                gun_model = self.sd.ref_socket_res_agent.model_res_map.get('gun')[0]
                gun_model.unbind_col_obj(self.gun_col)
                global_data.emgr.scene_remove_common_shoot_obj.emit(self.gun_col.cid)
            else:
                return
            self.gun_col_active = flag

    def show_gun(self):
        self.sd.ref_socket_res_agent.set_sub_mesh_visible('8033_wuqi', False)
        for key in self.WEAPON_KEYS:
            self.sd.ref_socket_res_agent.set_model_res_visible(True, key)

        self._activate_gun_col(True)

    def hide_gun(self):
        self.sd.ref_socket_res_agent.set_sub_mesh_visible('8033_wuqi', True)
        for key in self.WEAPON_KEYS:
            self.sd.ref_socket_res_agent.set_model_res_visible(False, key)

        self._activate_gun_col(False)

    def on_set_mecha_mode(self, mecha_mode, is_force=False):
        if self.mecha_mode == mecha_mode and not is_force:
            return
        self.mecha_mode = mecha_mode
        self.sd.ref_is_car_shape = self.mecha_mode == MECHA_PATTERN_VEHICLE
        if self.mecha_mode == MECHA_PATTERN_VEHICLE:
            self.send_event('E_REFRESH_STATE_PARAM', '8033_car', include_camera_param=True)
            self.cur_model_scale = HUMAN_SCALE
            self.target_model_scale = CAR_SCALE
            self.sd.ref_skip_model_ray_check = True
            self.send_event('E_CHANGE_MECHA_COLLISION', CAR_SHIELD_COL_INFO, CAR_SHOOT_COL_INFO)
            self.send_event('E_ENABLE_TWIST_PITCH', False)
        else:
            self.send_event('E_RESET_STATE_PARAM', '8033_car', include_camera_param=True)
            self.cur_model_scale = CAR_SCALE
            self.target_model_scale = HUMAN_SCALE
            self.sd.ref_skip_model_ray_check = False
            self.send_event('E_CHANGE_MECHA_COLLISION')
            self.send_event('E_ENABLE_TWIST_PITCH', True)
        self.need_update = True
        self.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', (bcast.E_SET_MECAH_MODE, (mecha_mode,)), False, True)
        self.on_gun_model_ani('juji_idle')

    def get_mecha_mode(self):
        return self.mecha_mode

    def update_model_scale(self, dt):
        if not self._model_ref:
            return True
        model = self._model_ref()
        if not model:
            return True
        if self.cur_model_scale < self.target_model_scale:
            self.cur_model_scale += dt * 2.0
            if self.cur_model_scale >= self.target_model_scale:
                self.cur_model_scale = self.target_model_scale
                model.scale = math3d.vector(self.cur_model_scale, self.cur_model_scale, self.cur_model_scale)
                self.send_event('E_MODEL_SCALE_CHANGED', self.cur_model_scale)
                return True
            model.scale = math3d.vector(self.cur_model_scale, self.cur_model_scale, self.cur_model_scale)
            self.send_event('E_MODEL_SCALE_CHANGED', self.cur_model_scale)
            return False
        if self.cur_model_scale > self.target_model_scale:
            self.cur_model_scale -= dt * 2.0
            if self.cur_model_scale <= self.target_model_scale:
                self.cur_model_scale = self.target_model_scale
                model.scale = math3d.vector(self.cur_model_scale, self.cur_model_scale, self.cur_model_scale)
                self.send_event('E_MODEL_SCALE_CHANGED', self.cur_model_scale)
                return True
            model.scale = math3d.vector(self.cur_model_scale, self.cur_model_scale, self.cur_model_scale)
            self.send_event('E_MODEL_SCALE_CHANGED', self.cur_model_scale)
            return False
        return True

    def on_set_gun_model_pitch_and_yaw(self, pitch, yaw):
        self.final_pitch = pitch
        self.final_yaw = yaw
        self.gun_rotation_progress = 0.0
        self.need_update = True
        self.sync_pitch_and_yaw = True

    def update_gun_model_pitch_and_yaw(self, dt):
        if not self.sync_pitch_and_yaw:
            return True
        if not self._model_ref:
            return True
        model = self._model_ref()
        if not model:
            self.sync_pitch_and_yaw = False
            return True
        gun_models = self.sd.ref_socket_res_agent.model_res_map.get('gun')
        pedestal_models = self.sd.ref_socket_res_agent.model_res_map.get('pedestal')
        self.gun_rotation_progress = min(self.gun_rotation_progress + dt, 1.0)
        if model and gun_models and pedestal_models:
            old_mat = gun_models[0].rotation_matrix
            off_mat = math3d.matrix.make_orient(math3d.vector(0, -1, 0), math3d.vector(-1, 0, 0))
            x_rotate = math3d.matrix.make_rotation_x(self.final_pitch)
            y_rotate = math3d.matrix.make_rotation_y(self.final_yaw)
            new_mat = off_mat * x_rotate * y_rotate
            local_rot = math3d.matrix_to_rotation(old_mat)
            local_rot.slerp(local_rot, math3d.matrix_to_rotation(new_mat), self.gun_rotation_progress)
            gun_models[0].rotation_matrix = math3d.rotation_to_matrix(local_rot)
            old_mat = pedestal_models[0].rotation_matrix
            off_mat = math3d.matrix.make_orient(math3d.vector(0, 0, 1), math3d.vector(-1, 0, 0))
            new_mat = off_mat * y_rotate
            local_rot = math3d.matrix_to_rotation(old_mat)
            local_rot.slerp(local_rot, math3d.matrix_to_rotation(new_mat), self.gun_rotation_progress)
            pedestal_models[0].rotation_matrix = off_mat * y_rotate
        if self.gun_rotation_progress == 1.0:
            self.sync_pitch_and_yaw = False
            return True
        return False

    def on_gun_model_ani(self, anim_name):
        gun_models = self.sd.ref_socket_res_agent.model_res_map.get('gun')
        if gun_models:
            gun_models[0].play_animation(anim_name, 100, world.TRANSIT_TYPE_IMM, 0, world.PLAY_FLAG_NO_LOOP)
        self.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', (bcast.E_GUN_MODEL_ANI_8033, (anim_name,)))

    def on_enter_mecha(self, *args):
        if self.unit_obj.get_owner().is_share():
            self.on_set_mecha_mode(MECHA_PATTERN_NORMAL)
            self.hide_gun()

    def on_energy_change(self, key, percent):
        if key == SKILL_8033_SCAN:
            energy_full = percent >= 1.0
            if self.car_vice_weapon_energy_full ^ energy_full:
                self.on_trigger_state_effect(CAR_VICE_WEAPON_ENERGY_FULL_STATE_ID, CAR_VICE_WEAPON_ENERGY_FULL_EFFECT_ID if energy_full else '', need_sync=True)
                self.car_vice_weapon_energy_full = energy_full

    def on_free_camera_switch_finish(self):
        scn = world.get_active_scene()
        if scn and scn.active_camera:
            dir = scn.active_camera.world_rotation_matrix.forward
            self.sd.ref_logic_trans.yaw_target = dir.yaw
            self.sd.ref_common_motor.set_yaw_time(0.2)

    def on_show_dash_progress(self, buff_id, data, left_time):
        from logic.gcommon.common_const.buff_const import BUFF_ID_8033_CAR_DASH
        if buff_id != BUFF_ID_8033_CAR_DASH:
            return
        self.on_trigger_state_effect('car_dash_screen_effect', '11')
        self.on_trigger_state_effect('car_dash_off_gas_effect', '12', need_sync=True)

    def on_clsoe_dash_progress(self):
        self.on_trigger_state_effect('car_dash_screen_effect', '')
        self.on_trigger_state_effect('car_dash_off_gas_effect', '', need_sync=True)