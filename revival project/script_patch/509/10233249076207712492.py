# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComMechaTransWheelchair.py
from __future__ import absolute_import
import six_ex
import six
from ..UnitCom import UnitCom
import common.utils.timer as timer
import math3d
import world
from logic.gcommon.common_const.scene_const import *
from logic.gcommon.item.item_use_var_name_data import *
from logic.gutils.client_unit_tag_utils import preregistered_tags
from logic.gcommon.const import NEOX_UNIT_SCALE
from logic.gcommon.common_const import mecha_const
from logic.gcommon.item.item_const import FASHION_POS_SUIT
import weakref
import math
import math3d
WHEEL_INDEX_0 = 0
WHEEL_INDEX_1 = 1
WHEEL_INDEX_2 = 2
WHEEL_INDEX_3 = 3
MOVE_DIR_FRONT = 1
MOVE_DIR_BACK = -1

class ComMechaTransWheelchair(UnitCom):
    BIND_EVENT = {'E_MODEL_LOADED': 'on_model_loaded',
       'E_VEHICLE_ENGINE_SPEED_CHANGE': 'on_engine_rotation_speed',
       'E_SPEED_CHANGED': 'on_speed_change',
       'E_CHANGE_PATTERN': 'change_pattern'
       }

    def __init__(self):
        super(ComMechaTransWheelchair, self).__init__()
        self._model_ref = None
        self._last_pos = math3d.vector(0, 0, 0)
        self._wheels_angle = {}
        self._scene = world.get_active_scene()
        self._mecha_id = 0
        self._is_mecha_trans = False
        self.update_wheel_timer_id = None
        return

    def on_model_loaded(self, model):
        self._model_ref = weakref.ref(model)
        self._last_pos = self.ev_g_model_position()

    def destroy(self):
        self._model_ref = None
        self.clear_refresh_timer()
        super(ComMechaTransWheelchair, self).destroy()
        return

    def init_from_dict(self, unit_obj, bdict):
        super(ComMechaTransWheelchair, self).init_from_dict(unit_obj, bdict)
        self.skin_id = bdict.get('mecha_fashion', {}).get(FASHION_POS_SUIT)

    def on_init_complete(self):
        self._mecha_id = self.sd.ref_mecha_id

    def is_self_control(self):
        if global_data.cam_lctarget and self.unit_obj == global_data.cam_lctarget:
            return True
        return False

    def change_pattern(self, pattern):
        pass

    def on_speed_change(self, speed):
        _cur_speed = speed[0]
        _max_speed = speed[1]

    def on_engine_rotation_speed(self, sp_info):
        self._wheels_angle = sp_info.get('wheels_agl', {})
        self.on_update_wheel_rotation()

    def on_update_wheel_rotation(self):
        is_self = self.is_self_control()
        if is_self:
            self.update_wheel_rotation()
        else:
            self.update_wheel_rotation_by_step()

    def update_wheel_rotation(self):
        radian_l = self._wheels_angle.get(WHEEL_INDEX_0)
        radian_r = self._wheels_angle.get(WHEEL_INDEX_1)
        if radian_l is None or radian_r is None:
            return
        else:
            radian_l = round(radian_l % (2 * math.pi), 2)
            radian_r = round(radian_r % (2 * math.pi), 2)
            self.on_turn_wheel(radian_l, radian_r)
            return

    def on_turn_wheel(self, radian_l, radian_r):
        LEFT_WHEEL_SOCKET = 'lunzi_l'
        self.roate_sub_wheel(LEFT_WHEEL_SOCKET, radian_l)
        RIGHT_WHEEL_SOCKET = 'lunzi_r'
        self.roate_sub_wheel(RIGHT_WHEEL_SOCKET, radian_r)

    def roate_sub_wheel(self, wheel_model_name, radian):
        model = self.ev_g_model()
        if model and model.valid:
            socket_model = model.get_socket_obj(wheel_model_name, 0)
            if socket_model and socket_model.valid:
                socket_model.rotation_matrix = math3d.matrix.make_rotation_x(radian)

    def update_wheel_rotation_by_step(self):
        if not self.update_wheel_timer_id:
            self.update_wheel_timer_id = global_data.game_mgr.register_logic_timer(self.check_step_turn, interval=1, times=-1, mode=timer.LOGIC)

    def check_step_turn(self):
        delta_raian = self.cal_wheel_step_radian()
        if delta_raian is None:
            self.clear_refresh_timer()
            return
        else:
            self.on_update_step_turn(delta_raian)
            return

    def on_update_step_turn(self, step_raian):
        LEFT_WHEEL_SOCKET = 'lunzi_l'
        self.roate_one_wheel_by_step(LEFT_WHEEL_SOCKET, step_raian)
        RIGHT_WHEEL_SOCKET = 'lunzi_r'
        self.roate_one_wheel_by_step(RIGHT_WHEEL_SOCKET, step_raian)

    def cal_wheel_step_radian(self):
        model = self.ev_g_model()
        if not model or not model.valid:
            return
        socket_model = model.get_socket_obj('lunzi_l', 0)
        if not socket_model:
            return
        _wheel_radius = socket_model.bounding_radius
        cur_pos = self.ev_g_model_position()
        move_dir = cur_pos - self._last_pos
        self._last_pos = cur_pos
        if move_dir.is_zero:
            return
        model_forward = model.world_rotation_matrix.forward
        model_forward and model_forward.normalize()
        dot = move_dir.dot(model_forward)
        move_dir_flag = MOVE_DIR_FRONT if dot > 0 else MOVE_DIR_BACK
        delta_radian = move_dir.length / _wheel_radius
        return move_dir_flag * delta_radian

    def clear_refresh_timer(self):
        if self.update_wheel_timer_id:
            global_data.game_mgr.unregister_logic_timer(self.update_wheel_timer_id)
            self.update_wheel_timer_id = None
        return

    def roate_one_wheel_by_step(self, wheel_model_name, delta_radian):
        model = self.ev_g_model()
        if model and model.valid:
            socket_model = model.get_socket_obj(wheel_model_name, 0)
            if socket_model and socket_model.valid:
                model_matrix = socket_model.world_rotation_matrix
                right = math3d.matrix.make_rotation_x(model_matrix.pitch or 0).right
                rot = math3d.rotation(0, 0, 0, 1)
                rot.set_axis_angle(right, delta_radian)
                cur_rot = math3d.matrix_to_rotation(socket_model.rotation_matrix)
                cur_rot = rot * cur_rot
                socket_model.rotation_matrix = math3d.rotation_to_matrix(cur_rot)