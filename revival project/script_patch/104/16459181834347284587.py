# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/parts/camera/CameraStates.py
from __future__ import absolute_import
from __future__ import print_function
import six_ex
import six
from six.moves import range
import cython_flag
import math
import math3d
import world
from logic.gutils.CameraHelper import normalize_angle
import common.utils.str_utils as str_utils
from logic.gcommon.const import NEOX_UNIT_SCALE, ATTACHEMNT_AIM_POS
from data.camera_state_const import *
from logic.client.const.camera_const import get_camera_z_range, DISABLE_POSTURE, ENABLE_POSTURE, INHERIT_POSTURE
from logic.gutils.CameraHelper import cal_vertical_fov
from logic.gcommon.common_utils.parachute_utils import STAGE_FREE_DROP, STAGE_PARACHUTE_DROP, STAGE_PLANE
from logic.gutils.CameraHelper import get_mecha_camera_type
from common.cfg import confmgr
_UP_VECTOR = math3d.vector(0, 1, 0)
_FORWARD_VECTOR = math3d.vector(0, 0, 1)
_RIGHT_VECTOR = math3d.vector(1, 0, 0)
_YZ_VECTOR = math3d.vector(0, 1, 1)
_DEFAULT_ROLE_ID = '11'
_RADIANS_FACTOR = 3.141592653589793 / 180.0001
_FIX_COMS = (
 'ClipCameraCom',)

class CameraState(object):
    OBSERVE = False
    TYPE = None
    COMS = []

    def __init__(self, cam_ctrl, **kwargs):
        self._init_attr(cam_ctrl, **kwargs)
        self._init_coms()
        self._init_parameters()

    def _init_attr(self, cam_ctrl, **kwargs):
        self.cam_ctrl = cam_ctrl
        self.max_pitch_radian = 80 * _RADIANS_FACTOR
        self.min_pitch_radian = -70 * _RADIANS_FACTOR
        self.yaw_range = None
        self.max_yaw_radian = None
        self.min_yaw_radian = None
        self._cam_state_data = {}
        return

    def cache(self):
        self._cache_coms()
        self._cam_state_data.clear()
        self.cam_ctrl = None
        return

    def reuse(self, cam_ctrl, **kwargs):
        self._init_attr(cam_ctrl, **kwargs)
        self._reuse_coms()

    def _cache_coms(self):
        for com in six.itervalues(self._coms):
            com.cache()

    def _reuse_coms(self):
        for com in six.itervalues(self._coms):
            com.reuse(self)

    def _init_coms(self, dynamic_coms=()):
        self._coms = {}
        camera_component = global_data.camera_state_pool.create_camera_component
        for com_name in self.COMS:
            self._coms[com_name] = camera_component(self, com_name)

        for com_name in _FIX_COMS:
            if com_name not in self._coms:
                self._coms[com_name] = camera_component(self, com_name)

        if dynamic_coms:
            for com_name in dynamic_coms:
                if com_name not in self._coms:
                    self._coms[com_name] = camera_component(self, com_name)

    def _enter_coms(self):
        for com in six.itervalues(self._coms):
            com.enter()

    def _destroy_coms(self):
        destroy_camera_component = global_data.camera_state_pool.destroy_camera_component
        for com in six.itervalues(self._coms):
            destroy_camera_component(com)

        self._coms = {}

    def _com_iter(self, func_name, *args, **kwargs):
        for com in six.itervalues(self._coms):
            func = getattr(com, func_name)
            if func:
                func(*args, **kwargs)

    def _init_parameters(self):
        conf = self.get_enter_transfer_setting()
        self._posture_setting = conf.get('bSupportPosture', DISABLE_POSTURE)
        self._is_enable_posture = self._posture_setting == ENABLE_POSTURE

    def enter(self, **kwargs):
        self._enter_coms()
        self.on_enter(**kwargs)

    def before_enter(self):
        self.on_before_enter()

    def on_before_enter(self):
        pass

    def on_enter(self, **kwargs):
        pass

    def on_update(self, dt):
        pass

    def on_destroy(self):
        pass

    def destroy(self):
        self._destroy_coms()
        self.on_destroy()
        self.cam_ctrl = None
        return

    def get_real_max_pitch_radian(self):
        return self.max_pitch_radian

    def get_real_min_pitch_radian(self):
        return self.min_pitch_radian

    def get_real_max_yaw_radian(self):
        return self.max_yaw_radian

    def get_real_min_yaw_radian(self):
        return self.min_yaw_radian

    def set_yaw_range(self, yaw_range):
        self.yaw_range = yaw_range

    def get_yaw_range(self):
        return self.yaw_range

    def refresh_real_yaw_range(self):
        if self.yaw_range:
            self.min_yaw_radian = self._yaw - self.yaw_range
            self.max_yaw_radian = self._yaw + self.yaw_range

    @property
    def cur_player_posture(self):
        return self.cam_ctrl.cur_player_posture

    @property
    def cur_role_id(self):
        return self.cam_ctrl._model_role_id

    @property
    def focus_point(self):
        return self.cam_ctrl.focus_point

    @focus_point.setter
    def focus_point(self, value):
        self.cam_ctrl.focus_point = value

    @property
    def default_pos(self):
        return self.cam_ctrl.default_pos

    @default_pos.setter
    def default_pos(self, value):
        self.cam_ctrl.default_pos = value

    @property
    def _pitch(self):
        return self.cam_ctrl._pitch

    @_pitch.setter
    def _pitch(self, val):
        self.cam_ctrl._pitch = val

    @property
    def _yaw(self):
        return self.cam_ctrl._yaw

    @property
    def _roll(self):
        return self.cam_ctrl._roll

    @_yaw.setter
    def _yaw(self, val):
        self.cam_ctrl._yaw = val

    @property
    def cur_fov(self):
        return self.cam_ctrl._cur_fov

    @property
    def cur_target_pos(self):
        return self.cam_ctrl.cur_target_pos

    @property
    def player(self):
        if global_data.cam_lplayer:
            player = global_data.cam_lplayer.ev_g_control_target()
            if player and player.logic:
                return player.logic

    def get_cur_target_model(self):
        if self.player:
            return self.player.ev_g_model()

    def is_valid(self):
        return self.cam_ctrl is not None

    def yaw(self, delta):
        _new_yaw = self._yaw
        if self.max_yaw_radian is not None and self.min_yaw_radian is not None:
            max_yaw_radian = self.max_yaw_radian
            min_yaw_radian = self.min_yaw_radian
            if not min_yaw_radian <= _new_yaw + delta <= max_yaw_radian:
                return
            _yaw = min(max(_new_yaw + delta, min_yaw_radian), max_yaw_radian)
            delta = _yaw - _new_yaw
            _new_yaw = _yaw
        else:
            _new_yaw += delta
        if self.cam_ctrl:
            if not self.cur_target_pos or not self.focus_point:
                return
            rotate_center = self.cur_target_pos + self.focus_point
            self.cam_ctrl.cam.rotate_axis_in_world(rotate_center, _UP_VECTOR, delta)
        self._yaw = _new_yaw
        return

    def pitch(self, delta):
        if self.get_real_camera_type() == FREE_DROP_MODE:
            return
        max_pitch_radian = self.get_real_max_pitch_radian()
        min_pitch_radian = self.get_real_min_pitch_radian()
        _new_pitch = self._pitch
        if not min_pitch_radian <= _new_pitch + delta <= max_pitch_radian:
            if abs(_new_pitch + delta) > abs(_new_pitch):
                return
            _new_pitch += delta
        else:
            _pitch = min(max(_new_pitch + delta, min_pitch_radian), max_pitch_radian)
            delta = _pitch - _new_pitch
            _new_pitch = _pitch
        if self.cam_ctrl:
            if not self.cur_target_pos or not self.focus_point:
                return
            rotate_center = self.cur_target_pos + self.focus_point
            right = self.cam_ctrl.cam.world_transformation.right
            if right.length < 0.0001:
                right = _RIGHT_VECTOR
            self.cam_ctrl.cam.rotate_axis_in_world(rotate_center, right, delta)
        self._pitch = _new_pitch

    def get_state_enter_setting(self, posture=None):
        player_posture = self.cur_player_posture if posture is None else posture
        conf = confmgr.get('camera_config', self.TYPE, default={}).get(player_posture, {})
        return self.check_state_enter_setting(conf)

    def check_state_enter_setting(self, conf, role_id=None):
        role_id = str(self.cur_role_id) if role_id is None else role_id
        pos_conf = conf.get('pos')
        copy_conf = dict(conf)
        if type(pos_conf) == dict:
            pos = pos_conf.get(role_id, None)
            copy_conf['pos'] = pos if pos else pos_conf.get(_DEFAULT_ROLE_ID, [7, 17, -30])
        focus_conf = conf.get('focus')
        if type(focus_conf) == dict:
            focus = focus_conf.get(role_id, None)
            copy_conf['focus'] = focus if focus else focus_conf.get(_DEFAULT_ROLE_ID, [0, 24, 0])
        return copy_conf

    def get_enter_transfer_setting(self, from_type=None):
        conf = confmgr.get('camera_transfer', self.TYPE, default={})
        conf = dict(conf)
        if from_type:
            add_conf = confmgr.get('c_camera_inter_transer_conf', str(self.TYPE), default={}).get(str(from_type), {})
            conf.update(add_conf)
        return conf

    def dump_camera_setting(self):
        trans = math3d.matrix.make_rotation_z(self._roll) * (math3d.matrix.make_rotation_x(self._pitch) * math3d.matrix.make_rotation_y(self._yaw))
        return {'trans': trans,
           'type': self.TYPE,
           'enable_posture': self.is_enable_player_posture()
           }

    def set_fov(self, fov):
        raise NotImplementedError()

    def set_pos(self, pos):
        raise NotImplementedError()

    def on_switch_camera_state(self, old_camera_state):
        if self._posture_setting == INHERIT_POSTURE:
            self._is_enable_posture = old_camera_state._is_enable_posture

    def rotate_by_center(self, pos, center, rotation_mat):
        new_pos = (pos - center) * rotation_mat
        return new_pos + center

    def get_leave_slerp_mid_action(self):
        return []

    def get_need_collision_recover(self):
        return True

    def is_enable_player_posture(self):
        return self._is_enable_posture

    def is_support_posture(self, posture):
        if self.get_state_enter_setting(posture):
            return True
        else:
            return False

    def on_before_switch_cam_player(self):
        pass

    def target_pos_changed(self, wpos):
        self._com_iter('on_target_pos_changed', wpos)

    def on_get_enter_parameters(self):
        self._com_iter('on_get_enter_parameters')

    def get_real_camera_type(self):
        return self.TYPE

    def is_free_camera(self):
        return self._posture_setting == INHERIT_POSTURE

    @staticmethod
    def on_recover_check(cls, lplayer):
        return False

    def set_cam_state_data(self, key, val):
        self._cam_state_data[key] = val

    def get_cam_state_data(self, key, default=None):
        return self._cam_state_data.get(key, default)


class FirstPersonCamera(CameraState):
    TYPE = FIRST_PERSON_MODEL
    COMS = []

    def is_enable_player_posture(self):
        return True

    @staticmethod
    def on_recover_check(cls, lplayer):
        return False


class ThirdPersonCamera(CameraState):
    TYPE = THIRD_PERSON_MODEL
    COMS = ['RoomOffsetCameraCom', 'SkateOffsetCameraCom', 'RunCam', 'ShotCam']

    def on_before_enter(self):
        normal_z_range = get_camera_z_range('NORMAL')
        self.cam_ctrl.cam.z_range = (normal_z_range[0], normal_z_range[1] * global_data.view_range_fix)

    @staticmethod
    def on_recover_check(cls, lplayer):
        return False


class HidingCamera(ThirdPersonCamera):
    TYPE = HIDING_MODE


class FreeCamera(CameraState):
    TYPE = FREE_MODEL
    COMS = []

    def _init_attr(self, cam_ctrl, **kwargs):
        super(FreeCamera, self)._init_attr(cam_ctrl, **kwargs)
        self.last_cam_state_type = None
        return

    def cache(self):
        self._destroy_coms()
        self.on_destroy()
        self.last_cam_state_type = None
        super(FreeCamera, self).cache()
        return

    def get_state_enter_setting(self, posture=None):
        player_posture = self.cur_player_posture if posture is None else posture
        conf = confmgr.get('camera_config', self.last_cam_state_type, default={}).get(player_posture, {})
        return self.check_state_enter_setting(conf)

    def on_switch_camera_state(self, old_camera_state):
        super(FreeCamera, self).on_switch_camera_state(old_camera_state)
        self.last_cam_state_type = old_camera_state.get_real_camera_type()
        self._destroy_coms()
        self._init_coms(old_camera_state.COMS)

    def get_need_collision_recover(self):
        if self.last_cam_state_type == VEHICLE_MODE:
            return False
        else:
            return True

    def is_enable_player_posture(self):
        return self._is_enable_posture

    def get_real_camera_type(self):
        return self.last_cam_state_type

    @staticmethod
    def on_recover_check(cls, lplayer):
        if lplayer:
            return lplayer.ev_g_free_camera_state()
        return False

    def dump_camera_setting(self):
        base_info = super(FreeCamera, self).dump_camera_setting()
        base_info.update({'real_type': self.get_real_camera_type()})
        return base_info


class AimCamera(CameraState):
    TYPE = AIM_MODE

    def __init__(self, cam_ctrl, **kwargs):
        super(AimCamera, self).__init__(cam_ctrl, **kwargs)
        self.process_event(True)

    def _init_attr(self, cam_ctrl, **kwargs):
        super(AimCamera, self)._init_attr(cam_ctrl, **kwargs)
        magnification = kwargs.get('magnification', 1.0)
        if isinstance(magnification, (list, tuple)):
            self.magnification_range = magnification
            self.magnification = self.magnification_range[0]
        else:
            self.magnification_range = None
            self.magnification = magnification
        self.item_id = kwargs.get('item_id', 0)
        self.aim_adjust_ui_class_name = None
        if self.item_id:
            last_aim_magnification = global_data.cam_lplayer.ev_g_scope_times(self.item_id)
            if last_aim_magnification:
                self.magnification = last_aim_magnification
        self.trans_time = kwargs.get('transfer_time', 0.2)
        self.need_hide_model = kwargs.get('need_hide_model', True)
        self.ALL_MAGNIFICATION_CONFIG = {float(one_magnification):value for one_magnification, value in six.iteritems(confmgr.get('camera_misc_arg')) if str_utils.is_number(one_magnification)}
        self.ALL_MAGNIFICATION_KEYS = six_ex.keys(self.ALL_MAGNIFICATION_CONFIG)
        return

    def cache(self):
        super(AimCamera, self).cache()
        self.on_destroy()

    def reuse(self, cam_ctrl, **kwargs):
        super(AimCamera, self).reuse(cam_ctrl, **kwargs)
        self.process_event(True)

    def on_destroy(self):
        self.process_event(False)
        if global_data.ui_mgr.get_ui('AimLensUI'):
            global_data.ui_mgr.close_ui('AimLensUI')
        if self.aim_adjust_ui_class_name is not None:
            if global_data.ui_mgr.get_ui(self.aim_adjust_ui_class_name):
                global_data.ui_mgr.close_ui(self.aim_adjust_ui_class_name)
        return

    @property
    def player(self):
        if global_data.cam_lplayer:
            player = global_data.cam_lplayer.ev_g_control_target()
            if player and player.logic.__class__.__name__ == 'LMotorcycle':
                return global_data.cam_lplayer
            if player and player.logic:
                return player.logic

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'switch_aim_magnification_event': self.switch_aim_magnification,
           'update_aim_scope_times_event': self._on_update_aim_scope_times,
           'get_magnification_fov_event': self.get_magnification_fov
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def _on_update_aim_scope_times(self, aim_scope_id, times):
        if self.item_id != aim_scope_id:
            return
        if self.magnification_range:
            if times > self.magnification_range[1]:
                times = self.magnification_range[1]
            if times < self.magnification_range[0]:
                times = self.magnification_range[0]
        self.magnification = times

    def get_camera_misc_arg_config(self, magnification):
        new_conf = None
        if magnification in self.ALL_MAGNIFICATION_KEYS:
            new_conf = self.ALL_MAGNIFICATION_CONFIG.get(magnification, {'dist': 0})
        elif magnification <= self.ALL_MAGNIFICATION_KEYS[0]:
            new_conf = self.ALL_MAGNIFICATION_CONFIG.get(self.ALL_MAGNIFICATION_KEYS[0], {'dist': 0})
        elif magnification >= self.ALL_MAGNIFICATION_KEYS[-1]:
            new_conf = self.ALL_MAGNIFICATION_CONFIG.get(self.ALL_MAGNIFICATION_KEYS[-1], {'dist': 0})
        else:
            larger_index = 0
            for index in range(1, len(self.ALL_MAGNIFICATION_KEYS)):
                if self.ALL_MAGNIFICATION_KEYS[index] > magnification:
                    larger_index = index
                    break

            low_magnification = self.ALL_MAGNIFICATION_KEYS[larger_index - 1]
            large_magnification = self.ALL_MAGNIFICATION_KEYS[larger_index]
            low_conf = self.ALL_MAGNIFICATION_CONFIG.get(low_magnification, {'dist': 0})
            large_conf = self.ALL_MAGNIFICATION_CONFIG.get(large_magnification, {'dist': 0})
            low_dist = low_conf.get('dist', 0)
            large_dist = large_conf.get('dist', 0)
            dist = low_dist + (magnification - low_magnification) / (large_magnification - low_magnification) * (large_dist - low_dist)
            new_conf = {'dist': dist}
        viewer_dir_offset = new_conf.get('dist', 0)
        return new_conf

    def switch_aim_magnification(self, magnification):
        if self.magnification_range:
            if magnification < self.magnification_range[0] or magnification > self.magnification_range[1]:
                print(('test--switch_aim_magnification--magnification =', magnification, '--magnification_range =', self.magnification_range, '--magnification out of range'))
                import traceback
                traceback.print_stack()
                return
        self.magnification = magnification
        if self.item_id:
            if global_data.cam_lplayer:
                global_data.cam_lplayer.send_event('E_CHANGE_SCOPE_TIMES', self.item_id, magnification)

    def on_before_enter(self):
        player_model = self.player.sd.ref_aim_model
        has_aim_model = True
        if not player_model:
            player_model = self.get_cur_target_model()
            has_aim_model = False
        if player_model:
            matrix = player_model.get_socket_matrix('camera', world.SPACE_TYPE_WORLD)
            if matrix:
                y = matrix.translation.y
            else:
                y = player_model.world_position.y
            cam = self.cam_ctrl.cam
            if has_aim_model and matrix:
                trans = player_model.world_transformation
                cam.world_position = math3d.vector(matrix.translation)
                player_model.world_transformation = trans
                owner_model = self.player.get_value('G_MODEL')
                t_matrix = owner_model.get_socket_matrix('gun_position', world.SPACE_TYPE_WORLD)
                if t_matrix:
                    rel_yaw, rel_pitch, y_offset, xz_offset, forward_offset = self.player.get_value('G_AIM_MODEL_ARGS')
                    player_model.world_rotation_matrix = math3d.matrix(cam.world_rotation_matrix)
                    axis = cam.world_position - player_model.world_position
                    if not axis.is_zero:
                        axis.normalize()
                    else:
                        axis = cam.world_rotation_matrix.up
                    player_model.world_rotation_matrix *= math3d.matrix.make_rotation(axis, rel_pitch)
                    cur_up = axis.cross(player_model.world_rotation_matrix.forward)
                    if cur_up.y < 0:
                        cur_up = -cur_up
                    cur_up.normalize()
                    player_model.world_rotation_matrix *= math3d.matrix.make_rotation(cur_up, rel_yaw)
                    player_model.world_position += axis * xz_offset
                    player_model.world_position += cur_up * y_offset
                    vec = player_model.world_rotation_matrix.forward
                    player_model.world_position += vec * forward_offset
                    mat = player_model.world_matrix
                    player_model.remove_from_parent()
                    player_model.set_parent(cam)
                    player_model.world_matrix = mat
        attr = global_data.cam_lplayer.ev_g_attachment_attr(ATTACHEMNT_AIM_POS)
        if self.need_hide_model:
            if self.player:
                self.player.send_event('E_HIDE_MODEL')

    def pitch(self, delta):
        max_pitch_radian = self.get_real_max_pitch_radian()
        min_pitch_radian = self.get_real_min_pitch_radian()
        _pitch = min(max(self._pitch + delta, min_pitch_radian), max_pitch_radian)
        delta = _pitch - self._pitch
        if self.cam_ctrl:
            if not self.cur_target_pos or not self.focus_point:
                return
            right = self.cam_ctrl.cam.world_transformation.right
            if right.length < 0.0001:
                right = _RIGHT_VECTOR
            rotate_center = self.cur_target_pos + self.focus_point
            self.cam_ctrl.cam.rotate_axis_in_world(rotate_center, right, delta)
        self._pitch = _pitch

    def get_magnification_fov(self, magnification=None):
        if not magnification:
            if self.magnification_range:
                magnification = self.magnification_range[0]
            else:
                magnification = self.magnification
        posture = None
        conf = super(AimCamera, self).get_state_enter_setting(posture)
        fov = self.cal_magnify_fov(magnification, conf['fov'])
        fov = cal_vertical_fov(fov)
        return fov

    def cal_magnify_fov(self, magnification, cur_fov):
        import math
        cur_size = math.tan(cur_fov * _RADIANS_FACTOR / 2)
        new_fov = 180 / math.pi * math.atan(cur_size / magnification) * 2
        return new_fov

    def cal_magnify_viewer_dir_offset(self, magnification):
        new_conf = self.get_camera_misc_arg_config(magnification)
        return new_conf.get('dist', 0)

    def get_aim_local_pos(self):
        player_model = self.get_cur_target_model()
        if player_model and player_model.valid:
            idx = player_model.get_socket_index('eye')
            if idx != -1:
                matrix = player_model.get_socket_matrix('eye', world.SPACE_TYPE_WORLD)
                if matrix:
                    diff_vec = matrix.translation - player_model.world_position
                    return math3d.vector(0, diff_vec.y, 0)
            idx = player_model.get_socket_index('part_point0')
            if idx != -1:
                matrix = player_model.get_socket_matrix('part_point0', world.SPACE_TYPE_WORLD)
                if matrix:
                    diff_vec = matrix.translation - player_model.world_position
                    return math3d.vector(0, diff_vec.y, 0)
        return self.cur_target_pos + math3d.vector(0, 18, 0)

    def get_state_enter_setting(self, posture=None):
        conf = super(AimCamera, self).get_state_enter_setting(posture)
        diff_vec = self.get_aim_local_pos()
        conf['pos'] = (diff_vec.x, diff_vec.y, diff_vec.z)
        conf['focus'] = (diff_vec.x, diff_vec.y, diff_vec.z)
        new_fov = self.cal_magnify_fov(self.magnification, conf['fov'])
        new_conf = self.get_camera_misc_arg_config(self.magnification)
        viewer_dir_offset = new_conf.get('dist', 0)
        conf['fov'] = new_fov
        conf['viewer_dir_offset'] = viewer_dir_offset * NEOX_UNIT_SCALE
        conf['magnification_triplet'] = self._get_magnification_triplet()
        conf['aim_scope_id'] = self.item_id
        if self.player:
            from logic.gcommon.const import ATTACHEMNT_AIM_POS
            attr = self.player.ev_g_attachment_attr(ATTACHEMNT_AIM_POS)
            if attr and 'cModel' in attr:
                conf['cModel'] = attr['cModel']
            cur_weapon = self.player.share_data.ref_wp_bar_cur_weapon
            if cur_weapon is not None:
                fashion = cur_weapon.get_fashion()
                from logic.gcommon.item.item_const import FASHION_POS_SUIT
                fashion_id = fashion.get(FASHION_POS_SUIT, None)
                if fashion_id is not None:
                    from logic.gutils import dress_utils
                    tmp_right_res, tmp_left_res = dress_utils.get_weapon_skin_res(fashion_id)
                    conf['cModel'] = tmp_right_res.replace('h.gim', 'aim/h.gim')
        return conf

    def on_switch_camera_state(self, old_camera_state):
        old_camera_state.need_hide_model = self.need_hide_model

    def get_enter_transfer_setting(self, from_type=None):
        conf = super(AimCamera, self).get_enter_transfer_setting(from_type)
        conf['fTransferInTime'] = self.trans_time
        aim_look_at_pos = self.player.ev_g_aim_look_at_pos()
        if aim_look_at_pos:
            conf['look_at_pos'] = aim_look_at_pos
        return conf

    def _get_magnification_triplet(self):
        if self.magnification_range:
            return (self.magnification, self.magnification_range[0], self.magnification_range[1])
        else:
            return (
             self.magnification, self.magnification, self.magnification)

    def on_enter(self):
        if self.item_id:
            from logic.gcommon.common_const.weapon_const import LENS_M82
            magnification_triplet = self._get_magnification_triplet()
            if magnification_triplet[1] != magnification_triplet[2]:
                if self.item_id == LENS_M82:
                    from logic.comsys.battle.AimScopeAdjust.AimScopeM82AdjustUI import AimScopeM82AdjustUI
                    AimScopeM82AdjustUI(None, magnification_triplet=magnification_triplet, aim_scope_id=self.item_id)
                    self.aim_adjust_ui_class_name = 'AimScopeM82AdjustUI'
        return

    def rotate_by_center(self, pos, center, rotation_mat):
        new_pos = (pos - center) * math3d.matrix.make_rotation_y(rotation_mat.yaw)
        return new_pos + center

    def dump_camera_setting(self):
        base_info = super(AimCamera, self).dump_camera_setting()
        base_info.update({'magnification': self.magnification})
        base_info.update({'transfer_time': self.trans_time})
        return base_info

    def get_leave_slerp_mid_action(self):
        player = self.player

        def show_model_action(player):
            self._check_model_recover(player)

        return [
         [
          0.95, lambda p=player: show_model_action(p)]]

    def _check_model_recover(self, player):
        if player and player.is_valid():
            if self.need_hide_model:
                if not player.ev_g_is_cam_target():
                    player.send_event('E_SHOW_MODEL')
                    return
                try:
                    scn = world.get_active_scene()
                    partcamera = scn.get_com('PartCamera')
                    cam_state = partcamera.cam_manager.cam_state
                except:
                    cam_state = None

                if cam_state and cam_state.TYPE != AIM_MODE:
                    player.send_event('E_SHOW_MODEL')
                elif not player.sd.ref_in_aim:
                    player.send_event('E_SHOW_MODEL')
        return

    def on_before_switch_cam_player(self):
        player = self.player
        self._check_model_recover(player)

    @staticmethod
    def on_recover_check(cls, lplayer):
        if lplayer:
            return lplayer.sd.ref_in_aim
        return False


class DeadCamera(CameraState):
    TYPE = DEAD_MODEL
    COMS = []

    @staticmethod
    def on_recover_check(cls, lplayer):
        return False


class PreviewCamera(FreeCamera):
    TYPE = PREVIEW_MODEL

    def get_state_enter_setting(self, posture=None):
        return CameraState.get_state_enter_setting(self, posture)

    @staticmethod
    def on_recover_check(cls, lplayer):
        return False


class DroneCamera(CameraState):
    TYPE = DRONE_MODE
    COMS = []

    @staticmethod
    def on_recover_check(cls, lplayer):
        if lplayer:
            return lplayer.ev_g_in_drone()
        return False


class AirshipCamera(CameraState):
    TYPE = AIRSHIP_MODE
    COMS = []

    @staticmethod
    def on_recover_check(cls, lplayer):
        if lplayer:
            control_target = lplayer.ev_g_control_target()
            if control_target:
                return control_target.__class__.__name__ == 'Airship'
        return False


class PlaneCamera(CameraState):
    TYPE = PLANE_MODE
    COMS = []

    def on_before_enter(self):
        self.cam_ctrl.cam.z_range = get_camera_z_range('PARACHUTE')

    @staticmethod
    def on_recover_check(cls, lplayer):
        if lplayer:
            para_stage = lplayer.share_data.ref_parachute_stage
            return para_stage == STAGE_PLANE
        return False


class FreeDropCamera(CameraState):
    TYPE = FREE_DROP_MODE
    COMS = ['ParachuteAssistCam']

    def on_before_enter(self):
        self.cam_ctrl.cam.z_range = get_camera_z_range('PARACHUTE')

    @staticmethod
    def on_recover_check(cls, lplayer):
        if lplayer:
            para_stage = lplayer.share_data.ref_parachute_stage
            return para_stage == STAGE_FREE_DROP
        return False


class ParachuteCamera(FreeCamera):
    TYPE = PARACHUTE_MODE

    def get_state_enter_setting(self, posture=None):
        return CameraState.get_state_enter_setting(self, posture)

    def get_real_camera_type(self):
        return self.TYPE

    @staticmethod
    def on_recover_check(cls, lplayer):
        if lplayer:
            para_stage = lplayer.share_data.ref_parachute_stage
            return para_stage == STAGE_PARACHUTE_DROP
        return False


class VehicleCamera(CameraState):
    TYPE = VEHICLE_MODE
    COMS = []

    def get_need_collision_recover(self):
        return False

    @staticmethod
    def on_recover_check(cls, lplayer):
        from logic.gcommon.common_const import mecha_const
        if lplayer:
            control_target = lplayer.ev_g_control_target()
            if control_target and control_target.logic and control_target.logic.ev_g_is_mechatran():
                return mecha_const.MECHA_TYPE_VEHICLE == control_target.logic.ev_g_pattern()
        return False


class FocusCamera(CameraState):
    TYPE = FOCUS_MODE
    COMS = []

    def _init_attr(self, cam_ctrl, **kwargs):
        super(FocusCamera, self)._init_attr(cam_ctrl, **kwargs)
        self._focus_id = kwargs.get('focus_id')
        self._timer_id = None
        self._last_time = 2
        return

    def cache(self):
        super(FocusCamera, self).cache()
        self.on_destroy()

    def on_enter(self, **kwargs):
        from logic.comsys.battle.FocusKillerUI import FocusKillerUI
        FocusKillerUI(None, self._focus_id)
        from common.utils.timer import LOGIC
        tmr = global_data.game_mgr.get_logic_timer()
        self._timer_id = tmr.register(func=self.on_focus_update, times=self._last_time * 30, mode=LOGIC)
        return

    def get_target_yaw_pitch(self):
        from mobile.common.EntityManager import EntityManager
        if self._focus_id:
            ent = EntityManager.getentity(self._focus_id)
            if ent and ent.logic:
                con_target = ent.logic.ev_g_control_target()
                if con_target and con_target.logic:
                    pos = con_target.logic.ev_g_position()
                else:
                    pos = ent.logic.ev_g_position()
                center_pos = self.cur_target_pos + self.focus_point
                if pos:
                    diff_vec = pos - center_pos
                    return (
                     diff_vec.yaw, diff_vec.pitch)
        return (None, None)

    def on_focus_update(self):
        yaw, pitch = self.get_target_yaw_pitch()
        if not yaw or not pitch:
            return
        yaw_diff = yaw - self._yaw
        yaw_diff = normalize_angle(yaw_diff)
        pitch_diff = pitch - self._pitch
        pitch_diff = normalize_angle(pitch_diff)
        rot_speed = math.pi / 60
        yaw_speed = min(abs(yaw_diff), rot_speed)
        pitch_speed = min(abs(pitch_diff), rot_speed)
        if yaw_diff < 0:
            yaw_speed *= -1
        if pitch_diff < 0:
            pitch_speed *= -1
        self.cam_ctrl.yaw(yaw_speed)
        self.cam_ctrl.pitch(pitch_speed)

    def on_destroy(self):
        if self._timer_id is not None:
            global_data.game_mgr.get_logic_timer().unregister(self._timer_id)
            self._timer_id = None
        global_data.ui_mgr.close_ui('FocusKillerUI')
        return

    @staticmethod
    def on_recover_check(cls, lplayer):
        return False


class FreeObserveCamera(FreeCamera):
    TYPE = OBSERVE_FREE_MODE

    def _init_attr(self, cam_ctrl, **kwargs):
        super(FreeObserveCamera, self)._init_attr(cam_ctrl, **kwargs)
        self.last_cam_state_type = kwargs.get('cam_type')

    def on_switch_camera_state(self, old_camera_state):
        old_last_cam_state_type = self.last_cam_state_type
        super(FreeObserveCamera, self).on_switch_camera_state(old_camera_state)
        if old_last_cam_state_type:
            self.last_cam_state_type = old_last_cam_state_type

    @staticmethod
    def on_recover_check(cls, lplayer):
        return False


class ThirdPersonSpeedUpCamera(ThirdPersonCamera):
    TYPE = THIRD_PERSON_SPEED_UP_MODE
    COMS = ['RoomOffsetCameraCom', 'SkateOffsetCameraCom']


class PassengerVehicleCamera(VehicleCamera):
    TYPE = PASSENGER_VEHICLE_MODE
    COMS = []


class RightAimCamera(CameraState):
    TYPE = RIGHT_AIM_MODE
    COMS = []

    @staticmethod
    def on_recover_check(cls, lplayer):
        if lplayer and lplayer.ev_g_in_right_aim():
            return True
        return False


class MechaBaseCamera(CameraState):
    TYPE = MECHA_MODE
    COMS = []

    @staticmethod
    def on_recover_check(cls, lplayer):
        if lplayer and lplayer.ev_g_in_mecha():
            control_target = lplayer.ev_g_control_target()
            if control_target and control_target.logic:
                return get_mecha_camera_type(control_target.logic.share_data.ref_mecha_id, control_target.logic.ev_g_mecha_fashion_id()) == cls.TYPE
        return False


class MechaCamera(MechaBaseCamera):
    TYPE = MECHA_MODE
    COMS = ['ShoulderCannonCam']


class MechaTransCamera(MechaBaseCamera):
    TYPE = MECHA_MODE_TWO

    @staticmethod
    def on_recover_check(cls, lplayer):
        from logic.gcommon.common_const import mecha_const
        if lplayer:
            control_target = lplayer.ev_g_control_target()
            if control_target and control_target.logic and control_target.logic.ev_g_is_mechatran():
                return mecha_const.MECHA_TYPE_NORMAL == control_target.logic.ev_g_pattern()
        return False


class DebugModeCamera(FreeCamera):
    TYPE = DEBUG_MODE

    def yaw(self, delta):
        if self.cam_ctrl:
            if self.cam_ctrl.cam.get_parent() not in [None, world.get_active_scene()]:
                return
        _new_yaw = self._yaw
        if self.max_yaw_radian is not None and self.min_yaw_radian is not None:
            max_yaw_radian = self.max_yaw_radian
            min_yaw_radian = self.min_yaw_radian
            if not min_yaw_radian <= self._yaw + delta <= max_yaw_radian:
                return
            _yaw = min(max(self._yaw + delta, min_yaw_radian), max_yaw_radian)
            delta = _yaw - self._yaw
            _new_yaw = _yaw
        else:
            _new_yaw = self._yaw + delta
        if self.cam_ctrl:
            if not self.cur_target_pos or not self.focus_point:
                return
            if not True:
                rotate_center = self.cur_target_pos + self.focus_point
            else:
                rotate_center = self.cam_ctrl.cam.world_position
            self.cam_ctrl.cam.rotate_axis_in_world(rotate_center, _UP_VECTOR, delta)
        self._yaw = _new_yaw
        return

    def pitch(self, delta):
        if self.cam_ctrl:
            if self.cam_ctrl.cam.get_parent() not in [None, world.get_active_scene()]:
                return
        max_pitch_radian = self.get_real_max_pitch_radian()
        min_pitch_radian = self.get_real_min_pitch_radian()
        _new_pitch = self._pitch
        if not min_pitch_radian <= self._pitch + delta <= max_pitch_radian:
            if abs(self._pitch + delta) > abs(self._pitch):
                return
            _new_pitch += delta
        else:
            _pitch = min(max(self._pitch + delta, min_pitch_radian), max_pitch_radian)
            delta = _pitch - self._pitch
            _new_pitch = _pitch
        if self.cam_ctrl:
            if not self.cur_target_pos or not self.focus_point:
                return
            if not True:
                rotate_center = self.cur_target_pos + self.focus_point
            else:
                rotate_center = self.cam_ctrl.cam.world_position
            right = self.cam_ctrl.cam.world_transformation.right
            if right.length < 0.0001:
                right = _RIGHT_VECTOR
            self.cam_ctrl.cam.rotate_axis_in_world(rotate_center, right, delta)
        self._pitch = _new_pitch
        return