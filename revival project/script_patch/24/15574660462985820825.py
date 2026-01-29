# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/accelerometer/AccInput.py
from __future__ import absolute_import
import game3d
import math3d
import world
from common.framework import Singleton
from logic.client.const import camera_const
from logic.gcommon.common_const.ui_operation_const import SST_GYROSCOPE_RD_KEY, SST_GYROSCOPE_2M_KEY, SST_GYROSCOPE_4M_KEY, SST_GYROSCOPE_SCR_KEY, SST_GYROSCOPE_6M_KEY, SST_GYROSCOPE_SCR_MECHA_VAL_KEY, SST_GYROSCOPE_SCR_SCOPE_MECHA_VAL_KEY, SST_GYROSCOPE_SCR_SPECIAL_FORM_MECHA_VAL_KEY
from logic.gcommon.common_const.ui_operation_const import OPEN_CONDITION_NONE, OPEN_CONDITION_AIM_OPEN
from logic.gcommon.common_const.weapon_const import LENS_RED_DOT, LENS_FOUR_MAGNITUDE, LENS_TWO_MAGNITUDE, LENS_MECHA_07, LENS_PULSE, LENS_M82, LENS_M14, LENS_M4
from logic.gcommon.common_const import ui_operation_const as uoc
LENS_AIM_MODE_SETTING_MAP = {LENS_RED_DOT: SST_GYROSCOPE_RD_KEY,
   LENS_TWO_MAGNITUDE: SST_GYROSCOPE_2M_KEY,
   LENS_FOUR_MAGNITUDE: SST_GYROSCOPE_4M_KEY,
   LENS_MECHA_07: SST_GYROSCOPE_4M_KEY,
   LENS_PULSE: SST_GYROSCOPE_RD_KEY,
   LENS_M82: SST_GYROSCOPE_6M_KEY,
   LENS_M4: SST_GYROSCOPE_RD_KEY,
   LENS_M14: SST_GYROSCOPE_2M_KEY
   }

class AccInput(Singleton):
    EPSILON_DELTA_ACC = 0.001

    def init(self):
        self._enable = False
        self.update_freq()
        self.init_data()
        self.init_conf()
        self.init_event()
        self.switch_to_setting_gyr_state()

    def update_freq(self):
        self._freq = 1.0 / game3d.get_frame_rate()

    def init_conf(self):
        from common.cfg import confmgr
        adjust_conf = confmgr.get('slide_adjust_conf')
        self.delta_gyro_epsilon = adjust_conf['DELTA_GYRO_EPSILON']

    def init_data(self):
        self._acc_update_timer = 0
        self._cnt_acc_vector = math3d.vector(0, 0, 0)
        self._acc_sensitivity = 0.1
        self._inited = False
        self._rotation_flag = 1
        self._is_prev_slide = False
        self._horiz_sensitivity = 1.0
        self._vertical_sensitivity = 1.0
        self.state = OPEN_CONDITION_NONE
        self.init_direction_data()

    def init_direction_data(self):
        gyr_state, x_reverse, y_reverse = global_data.player.get_setting(uoc.GYROSCOPE_STATE_KEY)
        self.direction_x = -1 if x_reverse else 1
        self.direction_y = -1 if y_reverse else 1

    def update_sensitivity(self, *args):
        player = global_data.player
        if not (player and player.logic):
            return
        else:
            cam_part = world.get_active_scene().get_com('PartCamera')
            _state = cam_part.get_cur_camera_state_type() if cam_part else camera_const.THIRD_PERSON_MODEL
            if _state == camera_const.AIM_MODE:
                aim_lens_type = player.logic.ev_g_aim_lens_type()
                sense_setting = LENS_AIM_MODE_SETTING_MAP.get(aim_lens_type, SST_GYROSCOPE_SCR_KEY)
            else:
                aim_lens_type = None
                sense_setting = SST_GYROSCOPE_SCR_KEY
            conf = player.get_setting(sense_setting)
            mecha_type_id = self._get_cur_mecha_type_id()
            if isinstance(mecha_type_id, int):
                from logic.gutils import mecha_utils
                from data.mecha_sens_open_scheme import check_scope_sensitivity_opened, check_special_form_sensitivity_opened
                if _state == camera_const.AIM_MODE and check_scope_sensitivity_opened(mecha_type_id):
                    base_val = mecha_utils.get_mecha_sens_setting_val(mecha_type_id, SST_GYROSCOPE_SCR_SCOPE_MECHA_VAL_KEY)
                elif global_data.mecha and global_data.mecha.logic and global_data.mecha.logic.sd.ref_use_mecha_special_form_sensitivity and check_special_form_sensitivity_opened(mecha_type_id):
                    base_val = mecha_utils.get_mecha_sens_setting_val(mecha_type_id, SST_GYROSCOPE_SCR_SPECIAL_FORM_MECHA_VAL_KEY)
                else:
                    base_val = mecha_utils.get_mecha_sens_setting_val(mecha_type_id, SST_GYROSCOPE_SCR_MECHA_VAL_KEY)
            else:
                base_val = conf[0]
            horiz = base_val * conf[1]
            vertical = base_val * conf[3]
            self._horiz_sensitivity = horiz * self._acc_sensitivity
            self._vertical_sensitivity = vertical * self._acc_sensitivity
            self.init_direction_data()
            return

    def _get_cur_mecha_type_id(self):
        if global_data.is_pc_mode:
            return
        else:
            if not global_data.cam_lplayer:
                return
            lp = global_data.cam_lplayer
            if lp.ev_g_in_mecha_only():
                mecha = lp.ev_g_control_target()
                lmecha = mecha.logic if mecha else None
                mecha_type_id = lmecha.share_data.ref_mecha_id if lmecha else None
                return mecha_type_id
            return
            return

    @property
    def enable(self):
        return self._enable

    def enable_acc_input(self, enable):
        last_enable = self._enable
        if global_data.is_pc_mode:
            enable = False
        tm = global_data.game_mgr.get_post_logic_timer()
        if not enable and self._acc_update_timer:
            tm.unregister(self._acc_update_timer)
            self._acc_update_timer = 0
        self._enable = enable
        if not enable or not last_enable:
            self._inited = False
        if enable:
            self._is_prev_slide = False
            if not self._acc_update_timer:
                self._acc_update_timer = tm.register(func=self.acc_update, interval=1)
            self.update_sensitivity()

    def switch_acc_input_open_condition(self, condition):
        if condition == OPEN_CONDITION_NONE:
            self.enable_acc_input(False)
        elif condition == OPEN_CONDITION_AIM_OPEN:
            import world
            scene = world.get_active_scene()
            if not scene:
                self.enable_acc_input(False)
                return
            camera_part = scene.get_com('PartCamera')
            self.enable_acc_input(camera_part and camera_part.get_cur_camera_state_type() == camera_const.AIM_MODE)
        else:
            self.enable_acc_input(True)

    def on_camera_state_switched(self, state, *args):
        self.switch_to_setting_gyr_state()

    def reset_gyroscope(self):
        game3d.activate_gyroscope(False, self._freq)
        game3d.activate_gyroscope(True, self._freq)
        self._cnt_gyro_vector = math3d.vector(0, 0, 0)
        self._inited = True

    def get_gyro_dxdy(self):
        new_gyro_vector = math3d.vector(*game3d.get_gyroscope_rotation())
        new_vector = self._cnt_gyro_vector * 0.5 + new_gyro_vector * 0.5
        dx, dy = new_vector.x - self._cnt_gyro_vector.x, new_vector.y - self._cnt_gyro_vector.y
        self._cnt_gyro_vector = new_vector
        dx = dx if abs(dx) > self.delta_gyro_epsilon else 0
        dy = dy if abs(dy) > self.delta_gyro_epsilon else 0
        return (
         dy, dx)

    def acc_update(self):
        _rotation = game3d.get_rotation()
        if _rotation == 90:
            self._rotation_flag = 1
        else:
            if _rotation == 270:
                self._rotation_flag = -1
            if not self._inited:
                self.reset_gyroscope()
                self._inited = True
                return
            dx, dy = self.get_gyro_dxdy()
            if dx == 0 and dy == 0:
                return
        sense_x = self._horiz_sensitivity * self._rotation_flag
        sense_y = self._horiz_sensitivity * self._rotation_flag
        global_data.emgr.camera_on_acc_input_update.emit(-dy * sense_x * self.direction_x, dx * sense_y * self.direction_y)

    def on_camera_delta_change(self, dx, dy, input_src):
        if input_src == camera_const.CAM_ROT_INPUT_SRC_SLIDE:
            self._is_prev_slide = True

    def on_parachute_end(self, *args):
        self.switch_to_setting_gyr_state()

    def switch_to_setting_gyr_state(self):
        from logic.gcommon.common_const.ui_operation_const import GYROSCOPE_STATE_KEY
        if not global_data.player:
            return
        gyr_open_state, x_reverse, y_reverse = global_data.player.get_setting(GYROSCOPE_STATE_KEY)
        self.switch_acc_input_open_condition(gyr_open_state)

    def on_camera_player_setted(self, *args):
        state_valid = False
        if global_data.player and global_data.player.logic and global_data.cam_lplayer:
            avt_id = global_data.player.logic.id
            cam_id = global_data.cam_lplayer.id
            if avt_id == cam_id:
                state_valid = True
        self.switch_to_setting_gyr_state() if state_valid else self.switch_acc_input_open_condition(OPEN_CONDITION_NONE)

    def on_reconnect(self):
        self.enable_acc_input(self._enable)

    def on_frame_rate_changed(self):
        self.update_freq()
        self.enable_acc_input(self._enable)

    def _on_mecha_sens_val_changed(self, mecha_id, val_key):
        if self._get_cur_mecha_type_id() != mecha_id:
            return
        else:
            if val_key is None or val_key == SST_GYROSCOPE_SCR_MECHA_VAL_KEY or val_key == SST_GYROSCOPE_SCR_SCOPE_MECHA_VAL_KEY or val_key == SST_GYROSCOPE_SCR_SPECIAL_FORM_MECHA_VAL_KEY:
                self.update_sensitivity()
            return

    def _on_ctrl_target_changed(self, *args):
        self.update_sensitivity()

    def init_event(self):
        global_data.emgr.parachute_end_event += self.on_parachute_end
        global_data.emgr.player_update_acc_sensitivity_event += self.update_sensitivity
        global_data.emgr.camera_switch_to_state_event += self.on_camera_state_switched
        global_data.emgr.scene_camera_player_setted_event += self.on_camera_player_setted
        global_data.emgr.net_reconnect_event += self.on_reconnect
        global_data.emgr.net_login_reconnect_event += self.on_reconnect
        global_data.emgr.app_frame_rate_changed_event += self.on_frame_rate_changed
        global_data.emgr.mecha_sens_val_changed += self._on_mecha_sens_val_changed
        global_data.emgr.switch_control_target_event += self._on_ctrl_target_changed
        global_data.emgr.update_mecha_sensitivity_type += self.update_sensitivity