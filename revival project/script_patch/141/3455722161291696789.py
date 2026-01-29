# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComMechaCockpit.py
from __future__ import absolute_import
from __future__ import print_function
import six
from ..UnitCom import UnitCom
import math3d
import math
from common.cfg import confmgr
from common.utils.cocos_utils import getScreenSize
COCKPIT_COM_DIC = {'pm_1_01': {'pos_type': 'LEFT_TOP','render_level': 6},'pm_1_02': {'pos_type': 'LEFT_TOP','render_level': 5},'pm_1_03': {'pos_type': 'LEFT_TOP','render_level': 0},'pm_2': {'pos_type': 'CENTER_TOP','render_level': 7},'pm_3_01': {'pos_type': 'RIGHT_TOP','render_level': 6},'pm_3_02': {'pos_type': 'RIGHT_TOP','render_level': 5},'pm_3_03': {'pos_type': 'RIGHT_TOP','render_level': 0},'pm_4': {'pos_type': 'RIGHT_CENTER','render_level': 0},'pm_5_01': {'pos_type': 'RIGHT_BUTTOM','render_level': 6},'pm_5_02': {'pos_type': 'RIGHT_BUTTOM','render_level': 5},'pm_5_03': {'pos_type': 'RIGHT_BUTTOM','render_level': 0},'pm_6': {'pos_type': 'CENTER_BUTTOM','render_level': 7},'pm_7_01': {'pos_type': 'LEFT_BUTTOM','render_level': 6},'pm_7_02': {'pos_type': 'LEFT_BUTTOM','render_level': 5},'pm_7_03': {'pos_type': 'LEFT_BUTTOM','render_level': 0},'pm_8': {'pos_type': 'LEFT_CENTER','render_level': 0}}

class ComMechaCockpit(UnitCom):
    BIND_EVENT = {'E_SHOW_MECHA_UI': '_show_mecha_ui',
       'E_CLOSE_MECHA_UI': '_close_mecha_ui'
       }

    def __init__(self):
        super(ComMechaCockpit, self).__init__()
        self._cockpit_model_list = {}
        self.screen_size = getScreenSize()
        self._is_play_trk = False
        self._is_reseting_cockpit = False
        self._last_rotate_yaw = 0
        self._last_rotate_pitch = 0
        self._last_rotate_roll = 0
        self._total_rotate_yaw = 0
        self._total_rotate_pitch = 0
        self._total_rotate_roll = 0
        self._cockpit_depth = 100
        self._cockpit_ready_state = False
        self._show_state = False
        self.fov_update = False
        self.cur_mecha_orignal_fov = 0

    def init_from_dict(self, unit_obj, bdict):
        super(ComMechaCockpit, self).init_from_dict(unit_obj, bdict)

    def _show_mecha_ui(self):
        if not global_data.can_show_cockpit_decor:
            return
        self.need_update = True
        self._show_state = True
        self._cockpit_loaded_num = 0
        self.cur_camera_zrange = self.scene.active_camera.z_range[0]
        for key, value in six.iteritems(COCKPIT_COM_DIC):
            res_path = 'effect/mesh/scenes/pm/{0}.gim'.format(key)
            params = {'key': key}
            params.update(value)
            self.ev_g_load_model(res_path, self._cockpit_model_load_callback, params)

        self._cockpit_ready_state = True
        global_data.emgr.camera_play_added_trk_start += self._on_play_trk_start
        global_data.emgr.camera_switch_to_state_event += self._on_camera_state_change
        global_data.emgr.camera_trans_change += self._on_camera_trans_change
        global_data.emgr.camera_all_trk_play_end += self._on_all_trk_play_end

    def _close_mecha_ui(self):
        self._show_state = False
        self.need_update = False
        self._is_play_trk = False
        self._is_reseting_cockpit = False
        self._last_rotate_yaw = 0
        self._last_rotate_pitch = 0
        self._last_rotate_roll = 0
        self._total_rotate_yaw = 0
        self._total_rotate_pitch = 0
        self._total_rotate_roll = 0
        self.cur_mecha_orignal_fov = 0
        global_data.emgr.camera_play_added_trk_start -= self._on_play_trk_start
        global_data.emgr.camera_switch_to_state_event -= self._on_camera_state_change
        global_data.emgr.camera_trans_change -= self._on_camera_trans_change
        global_data.emgr.camera_all_trk_play_end -= self._on_all_trk_play_end
        for _model in six.itervalues(self._cockpit_model_list):
            try:
                _model.remove_from_parent()
                _model.destroy()
            except:
                print('model has been remove form sceen %s' % self.__class__.__name__)

        self._cockpit_model_list = {}
        self._cockpit_loaded_num = 0

    def _get_cockpit_model_pos(self, key):
        screen_x = 0
        screen_y = 0
        pos_type = COCKPIT_COM_DIC[key]['pos_type']
        if pos_type == 'LEFT_TOP':
            screen_x = 0
            screen_y = 0
        elif pos_type == 'LEFT_BUTTOM':
            screen_x = 0
            screen_y = self.screen_size.height
        elif pos_type == 'CENTER_TOP':
            screen_x = self.screen_size.width / 2
            screen_y = 15
        elif pos_type == 'CENTER_BUTTOM':
            screen_x = self.screen_size.width / 2
            screen_y = self.screen_size.height - 5
        elif pos_type == 'RIGHT_TOP':
            screen_x = self.screen_size.width
            screen_y = 0
        elif pos_type == 'RIGHT_BUTTOM':
            screen_x = self.screen_size.width
            screen_y = self.screen_size.height
        elif pos_type == 'LEFT_CENTER':
            screen_x = 0
            screen_y = self.screen_size.height / 2
        elif pos_type == 'RIGHT_CENTER':
            screen_x = self.screen_size.width
            screen_y = self.screen_size.height / 2
        world_pt, dir = self.scene.active_camera.screen_to_world(screen_x, screen_y)
        camera_pt = self.scene.active_camera.world_to_camera(world_pt)
        return camera_pt * self.cal_pos_rate()

    def _get_cockpit_world_axis(self):
        left_top_model = self._cockpit_model_list['pm_1_01']
        start_pos = math3d.vector(0, 0, left_top_model.position.z)
        start_world_pos = self.scene.active_camera.camera_to_world(start_pos)
        end_pos = math3d.vector(1, 0, left_top_model.position.z)
        end_world_pos = self.scene.active_camera.camera_to_world(end_pos)
        x_axis = end_world_pos - start_world_pos
        end_pos = math3d.vector(0, 1, left_top_model.position.z)
        end_world_pos = self.scene.active_camera.camera_to_world(end_pos)
        y_axis = end_world_pos - start_world_pos
        end_pos = math3d.vector(0, 0, 0)
        end_world_pos = self.scene.active_camera.camera_to_world(end_pos)
        z_axis = end_world_pos - start_world_pos
        return (
         start_world_pos, x_axis, y_axis, z_axis)

    def cal_pos_rate(self):
        return (self.scene.active_camera.z_range[0] + self._cockpit_depth) / self.scene.active_camera.z_range[0]

    def cal_scale_rate(self):
        return (self.scene.active_camera.z_range[0] + self._cockpit_depth) / (1 + self._cockpit_depth)

    def _cockpit_model_load_callback(self, cockpit_model, *args):
        if not self._show_state:
            return
        self._cockpit_loaded_num += 1
        key = args[0]['key']
        pos_type = args[0]['pos_type']
        render_level = args[0]['render_level']
        self._cockpit_model_list[key] = cockpit_model
        cockpit_model.enable_post_process(False, True)
        cockpit_model.set_parent(self.scene.active_camera)
        cockpit_model.render_level = render_level
        cockpit_model.position = self._get_cockpit_model_pos(key)
        rate = self.cal_scale_rate()
        cockpit_model.scale = math3d.vector(rate, rate, rate)

    def _is_all_model_loaded(self):
        return self._cockpit_loaded_num == len(COCKPIT_COM_DIC)

    def _reset_cokpit_model_pos(self):
        rate = self.cal_scale_rate()
        for key, _model in six.iteritems(self._cockpit_model_list):
            _model.position = self._get_cockpit_model_pos(key)
            _model.scale = math3d.vector(rate, rate, rate)

    def _on_play_trk_start(self, trk_tag):
        trk_conf = confmgr.get('camera_trk_sfx_conf', 'TrkConfig').get('Content').get(str(trk_tag), None)
        if not trk_conf:
            log_error("Can't find cam trk %s" % trk_tag)
            return
        else:
            self._is_play_trk = True
            self._is_reseting_cockpit = False
            self._last_cam_pos = self.scene.active_camera.world_position
            self._delay_cur_time = 0
            self._delay_follow_time = trk_conf.get('delay_follow_time', 0.5)
            self._translate_swing = trk_conf.get('translate_swing', 0.01)
            self._rotate_swing = trk_conf.get('rotate_swing', 1)
            return

    def _on_all_trk_play_end(self):
        if not self._is_play_trk:
            return
        self._is_play_trk = False
        self._is_reseting_cockpit = True
        self._reset_time = 0.5
        self._reset_cur_time = 0
        self._per_fix_offset_caluated = False
        self._per_fix_offset = {}

    def _follow_cockpit_pos(self, delta):
        if not self._is_all_model_loaded():
            return
        self._delay_cur_time += delta
        if self._delay_cur_time < self._delay_follow_time:
            cur_cam_pos = self.scene.active_camera.world_position
            offset_y = cur_cam_pos.y - self._last_cam_pos.y
            self._last_cam_pos = cur_cam_pos
            offset_y = offset_y * self._translate_swing
            left_top_model = self._cockpit_model_list['pm_1_01']
            original_pos = self._get_cockpit_model_pos('pm_1_01')
            max_offset_y = 20
            if abs(left_top_model.position.y - offset_y - original_pos.y) > max_offset_y:
                if offset_y > 0:
                    offset_y = max_offset_y - (original_pos.y - left_top_model.position.y)
                else:
                    offset_y = left_top_model.position.y - original_pos.y - max_offset_y
            new_pos_offset = math3d.vector(0, offset_y, 0)
            for key, _model in six.iteritems(self._cockpit_model_list):
                _model.position -= new_pos_offset

    def _reset_cockpit_pos_gradually(self, delta):
        if not self._is_all_model_loaded():
            return
        if self._total_rotate_roll != 0 or self._total_rotate_yaw != 0 or self._total_rotate_pitch != 0:
            start_pos, x_axis, y_axis, z_axis = self._get_cockpit_world_axis()
            for key, _model in six.iteritems(self._cockpit_model_list):
                mat = _model.rotation_matrix
                mat.set_identity()
                _model.rotation_matrix = mat

        self._total_rotate_yaw = 0
        self._total_rotate_roll = 0
        self._total_rotate_pitch = 0
        if not self._per_fix_offset_caluated:
            self._per_fix_offset_caluated = True
            for key, _model in six.iteritems(self._cockpit_model_list):
                original_pos = self._get_cockpit_model_pos(key)
                dis_pos = _model.position - original_pos
                self._per_fix_offset[key] = -dis_pos * (1 / self._reset_time)

        self._reset_cur_time += delta
        if self._reset_cur_time > self._reset_time:
            self._is_reseting_cockpit = False
            self._reset_cokpit_model_pos()
            return
        for key, _model in six.iteritems(self._cockpit_model_list):
            new_pos_offset = self._per_fix_offset[key] * delta
            _model.position += new_pos_offset

    def _on_camera_state_change(self, new_cam_type, old_cam_type, is_finish_switch):
        if is_finish_switch:
            self._cockpit_ready_state = False
            self.cur_mecha_orignal_fov = global_data.game_mgr.scene.active_camera.fov
            global_data.emgr.camera_switch_to_state_event -= self._on_camera_state_change

    def _on_camera_trans_change(self, trans):
        if self.fov_update:
            return
        if not self._is_play_trk or not self._is_all_model_loaded():
            return
        delta_rotate_yaw = trans.rotation.yaw - self._last_rotate_yaw
        delta_rotate_pitch = trans.rotation.pitch - self._last_rotate_pitch
        delta_rotate_roll = trans.rotation.roll - self._last_rotate_roll
        self._last_rotate_yaw = trans.rotation.yaw
        self._last_rotate_pitch = trans.rotation.pitch
        self._last_rotate_roll = trans.rotation.roll
        start_pos, x_axis, y_axis, z_axis = self._get_cockpit_world_axis()
        if abs(self._total_rotate_pitch + delta_rotate_pitch) < 0.08:
            self._total_rotate_pitch += delta_rotate_pitch
            for key, _model in six.iteritems(self._cockpit_model_list):
                _model.rotate_axis_in_world(start_pos, x_axis, delta_rotate_pitch)

        if abs(self._total_rotate_yaw + delta_rotate_yaw) < 1:
            self._total_rotate_yaw += delta_rotate_yaw
            for key, _model in six.iteritems(self._cockpit_model_list):
                _model.rotate_axis_in_world(start_pos, y_axis, delta_rotate_yaw)

        if abs(self._total_rotate_roll + delta_rotate_roll) < 1:
            self._total_rotate_roll += delta_rotate_roll
            for key, _model in six.iteritems(self._cockpit_model_list):
                _model.rotate_axis_in_world(start_pos, z_axis, delta_rotate_roll)

    def tick(self, delta):
        if self._cockpit_ready_state:
            self._reset_cokpit_model_pos()
        elif not self._update_cokpit_model_pos_by_fov():
            if not self._update_camera_range():
                if self._is_play_trk:
                    self._follow_cockpit_pos(delta)
                elif self._is_reseting_cockpit:
                    self._reset_cockpit_pos_gradually(delta)

    def _update_camera_range(self):
        if not self._is_all_model_loaded():
            return False
        if self.cur_camera_zrange == self.scene.active_camera.z_range[0]:
            return False
        self.cur_camera_zrange = self.scene.active_camera.z_range[0]
        self._reset_cokpit_model_pos()
        return True

    def _update_cokpit_model_pos_by_fov(self):
        if not self._is_all_model_loaded() or self.cur_mecha_orignal_fov == 0:
            return False
        delta_fov = self.cur_mecha_orignal_fov - global_data.game_mgr.scene.active_camera.fov
        if delta_fov == 0 and not self.fov_update:
            return False
        if delta_fov == 0:
            self.fov_update = False
        else:
            self.fov_update = True
        left_top_model = self._cockpit_model_list['pm_1_01']
        direction_pos = math3d.vector(0, 0, left_top_model.position.z)
        offset_scale = delta_fov / 300
        for key, _model in six.iteritems(self._cockpit_model_list):
            original_pos = self._get_cockpit_model_pos(key)
            cur_dirction = direction_pos - original_pos
            new_pos = original_pos + cur_dirction * offset_scale
            _model.position = new_pos

        return True

    def destroy(self):
        self._close_mecha_ui()
        super(ComMechaCockpit, self).destroy()