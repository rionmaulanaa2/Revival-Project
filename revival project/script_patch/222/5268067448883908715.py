# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComMechaFootIK.py
from __future__ import absolute_import
from __future__ import print_function
from logic.gcommon.component.UnitCom import UnitCom
import logic.gcommon.common_const.collision_const as collision_const
import logic.gcommon.common_utils.bcast_utils as bcast
from common.utils.timer import CLOCK
from common.cfg import confmgr
import collision
import math3d
import world
SUPPORT_MECHA_FOOT_IK = hasattr(world, 'BIND_TYPE_BONE_GROUND')
TURN_ANIM_NAMES = ('turnleft_90', 'turnright_90')

class ComMechaFootIK(UnitCom):
    BIND_EVENT = {'E_ANIMATOR_LOADED': ('on_load_animator_complete', 99),
       'E_SET_SKIP_RAY_CHECK_CID': 'on_set_skip_ray_check_cid',
       'E_ENABLE_MECHA_FOOT_IK': 'enable_foot_ik',
       'E_ENABLE_MECHA_FOOT_IK_BY_MAP': 'enable_foot_ik_by_map',
       'E_ON_POST_JOIN_MECHA': 'on_post_join_mecha',
       'E_MECHA_LOD_LOADED': 'on_mecha_lod_loaded',
       'E_SET_FOOT_IK_PARAM': 'set_ik_parameters',
       'E_RESET_FOOT_IK_PARAM': 'reset_ik_parameters'
       }

    def init_from_dict(self, unit_obj, bdict):
        super(ComMechaFootIK, self).init_from_dict(unit_obj, bdict)
        self.is_avatar = False
        self.ik_mgr = None
        self.ik_solver_list = []
        self.ik_parameters_list = []
        self.ik_solver_count = 0
        self.setting_info_list = []
        self.logic_enabled_map = bdict.get('ik_solver_enable_dict', {})
        self.waiting_sync_enabled_map = {}
        self.skip_cid = -1
        self.skip_update_frame = 0
        self.quality_event_registered = False
        self.cur_lod_level = 0
        self.cur_quality = 0
        self.ik_param_data_for_reset = {}
        self.anim_event_registered = False
        self.is_playing_turn_anim = False
        self.delay_reset_timer = None
        self.ik_key_to_index_list_map = {}
        return

    def _register_quality_event(self, flag):
        if self.quality_event_registered ^ flag:
            if flag:
                global_data.emgr.display_quality_change += self.on_quality_changed
            else:
                global_data.emgr.display_quality_change -= self.on_quality_changed
            self.quality_event_registered = flag

    def _register_anim_event(self, flag):
        if self.anim_event_registered ^ flag:
            if flag:
                self.regist_event('E_POST_ACTION', self.on_play_anim)
            else:
                self.unregist_event('E_POST_ACTION', self.on_play_anim)
            self.anim_event_registered = flag

    def _unregister_reset_timer(self):
        if self.delay_reset_timer:
            global_data.game_mgr.unregister_logic_timer(self.delay_reset_timer)
            self.delay_reset_timer = None
        return

    def destroy(self):
        self.ik_mgr = None
        del self.ik_solver_list[:]
        self.logic_enabled_map = {}
        self._register_quality_event(False)
        self._register_anim_event(False)
        self._unregister_reset_timer()
        super(ComMechaFootIK, self).destroy()
        return

    def _refresh_ik_parameters(self, index):
        ik_solver = self.ik_solver_list[index]
        ik_parameters = self.ik_parameters_list[index]
        ik_solver.set_solver_parameters(ik_parameters['ignore_target_rotation'], True, True, ik_parameters['ik_intrp_speed'], ik_parameters['max_bend_angle'])
        ik_solver.set_provider_parameters(world.BIND_TYPE_BONE_GROUND, (
         self.skip_cid, self.skip_update_frame,
         ik_parameters['ray_check_y_up_offset'], ik_parameters['ray_check_y_down_offset'],
         ik_parameters['ik_y_offset_intrp_speed'], ik_parameters['ik_pitch_intrp_speed'],
         ik_parameters['upward_use_ik_pitch_threshold'], ik_parameters['downward_use_ik_pitch_threshold'],
         ik_parameters['min_use_ik_pitch_threshold'], ik_parameters['horizontal_foot_pitch'],
         ik_parameters['toe_parent_yaw_offset'], ik_parameters['opposite_pitch_dir'],
         ik_parameters['max_up_foot_angle'], ik_parameters['max_down_foot_angle'],
         ik_parameters['foot_bone_height_index'], collision_const.GROUP_CHARACTER_INCLUDE))

    def is_visible_in_this_frame_changed(self, visible):
        if self.ik_mgr:
            self.ik_mgr.enabled = visible

    def on_load_animator_complete(self, *args):
        return
        if not global_data.feature_mgr.is_support_mecha_foot_ik():
            return
        else:
            self.is_avatar = self.ev_g_is_avatar()
            self.cur_lod_level = self.ev_g_lod_level()
            self.skip_update_frame = max(self.cur_lod_level - 1, 0)
            if global_data.game_mgr.gds:
                self.cur_quality = global_data.game_mgr.gds.get_actual_quality()
            if global_data.editor_mecha_foot_ik_parameters:
                conf = global_data.editor_mecha_foot_ik_parameters
            else:
                conf = confmgr.get('mecha_foot_ik_conf', 'MechaFootIKConfig', 'Content')
            skin_id = str(self.ev_g_mecha_fashion_id())
            if skin_id and skin_id in conf:
                first_valid_key = skin_id
            elif str(self.sd.ref_mecha_id) in conf:
                first_valid_key = str(self.sd.ref_mecha_id)
            else:
                first_valid_key = None
            if first_valid_key is None:
                return
            valid_key_list = [
             first_valid_key]
            index = 1
            while True:
                new_key = '{}_{}'.format(first_valid_key, index)
                if new_key in conf:
                    valid_key_list.append(new_key)
                    index += 1
                else:
                    break

            index = 0
            model = self.ev_g_model()
            ik_mgr = model.get_ik_mgr()
            del self.ik_solver_list[:]
            del self.ik_parameters_list[:]
            for valid_key in valid_key_list:
                ik_conf = conf[valid_key]
                bone_names = ik_conf['foot_bone_names']
                setting_info = (bool(ik_conf['self_ik_enabled']), ik_conf['lod_level'], ik_conf['quality'])
                default_enabled, intrp_duration = self.logic_enabled_map.get(None, (bool(ik_conf['default_enabled']), 0.2))
                with_joint = ik_conf['with_joint']
                for i, (foot_bone_name, toe_bone_name) in enumerate(bone_names):
                    if with_joint:
                        ik_solver = ik_mgr.create_two_bone_ik_with_joint(str(i), foot_bone_name, 0)
                    else:
                        ik_solver = ik_mgr.create_two_bone_ik(str(i), foot_bone_name, 0)
                    ik_solver.set_target(model, world.BIND_TYPE_BONE_GROUND, (foot_bone_name, toe_bone_name))
                    self.ik_solver_list.append(ik_solver)
                    self.ik_parameters_list.append({'ik_intrp_speed': ik_conf['ik_intrp_speed'],
                       'max_bend_angle': ik_conf['max_bend_angle'],
                       'ray_check_y_up_offset': ik_conf['ray_check_y_up_offset'],
                       'ray_check_y_down_offset': ik_conf['ray_check_y_down_offset'],
                       'upward_use_ik_pitch_threshold': ik_conf['upward_use_ik_pitch_threshold'],
                       'downward_use_ik_pitch_threshold': ik_conf['downward_use_ik_pitch_threshold'],
                       'min_use_ik_pitch_threshold': ik_conf['min_use_ik_pitch_threshold'],
                       'horizontal_foot_pitch': ik_conf['horizontal_foot_pitch'],
                       'toe_parent_yaw_offset': ik_conf['toe_parent_yaw_offset'],
                       'opposite_pitch_dir': ik_conf['opposite_pitch_dir'],
                       'max_up_foot_angle': ik_conf['max_up_foot_angle'],
                       'max_down_foot_angle': ik_conf['max_down_foot_angle'],
                       'ignore_target_rotation': not bool(ik_conf['ik_foot_pitch_enabled']),
                       'ik_y_offset_intrp_speed': ik_conf['ik_y_offset_intrp_speed'],
                       'ik_pitch_intrp_speed': ik_conf['ik_pitch_intrp_speed'],
                       'foot_bone_height_index': ik_conf['foot_bone_height_index']
                       })
                    self._refresh_ik_parameters(-1)
                    self.setting_info_list.append(setting_info)
                    if index not in self.logic_enabled_map:
                        self.logic_enabled_map[index] = (
                         default_enabled, intrp_duration)
                    index += 1
                    ik_solver.enabled = False

            self.ik_solver_count = index
            self.ik_mgr = ik_mgr
            self.send_event('E_ADD_VISIBLE_IN_THIS_FRAME_CHANGED_CALLBACK', self.is_visible_in_this_frame_changed)
            for turn_anim_name in TURN_ANIM_NAMES:
                if model.has_anim(turn_anim_name):
                    self._register_anim_event(True)
                    self.on_play_anim(self.sd.ref_low_body_anim)
                    break

            return

    def on_set_skip_ray_check_cid(self, cid):
        self.skip_cid = cid
        for ik_solver in self.ik_solver_list:
            ik_solver.set_provider_parameters(world.BIND_TYPE_BONE_GROUND, (self.skip_cid,))

    def _refresh_ik_solver_enabled(self, index):
        if index is None:
            return
        else:
            ik_solver = self.ik_solver_list[index]
            self_ik_enabled, lod_level, quality = self.setting_info_list[index]
            if self.sd.ref_driver_id:
                if self.is_avatar:
                    enabled = self_ik_enabled
                else:
                    enabled = True
            else:
                enabled = False
            logic_enabled, intrp_duration = self.logic_enabled_map[index]
            enabled = enabled and logic_enabled and self.cur_lod_level <= lod_level and self.cur_quality >= quality
            if intrp_duration <= 0:
                if ik_solver.enabled ^ enabled:
                    ik_solver.enabled = enabled
            else:
                if not ik_solver.enabled:
                    ik_solver.enabled = True
                target_weight = 1.0 if enabled else 0.0
                smooth_speed = 1.0 / intrp_duration
                ik_solver.target_weight = target_weight
                ik_solver.smooth_weight_speed = smooth_speed
            return

    def enable_foot_ik(self, enable, intrp_duration=0.2, index=None, need_sync=True):
        return
        new_data = (
         enable, intrp_duration)
        self.logic_enabled_map[index] = new_data
        if index is None:
            for _index in self.logic_enabled_map:
                self.logic_enabled_map[_index] = new_data

        if self.ik_solver_count:
            if index is None:
                for _index in range(self.ik_solver_count):
                    self._refresh_ik_solver_enabled(_index)

            else:
                self._refresh_ik_solver_enabled(index)
        need_sync and self.send_event('E_CALL_SYNC_METHOD', 'update_ik_solver_enable_dict', ({index: new_data},), True)
        return

    def enable_foot_ik_by_map(self, enable_info_map, need_sync=True):
        return
        self.logic_enabled_map.update(enable_info_map)
        if None in enable_info_map:
            enable_info = enable_info_map[None]
            for index in range(self.ik_solver_count):
                self.logic_enabled_map[index] = enable_info
                self._refresh_ik_solver_enabled(index)

        elif self.ik_solver_count:
            for index in enable_info_map:
                self._refresh_ik_solver_enabled(index)

        need_sync and self.send_event('E_CALL_SYNC_METHOD', 'update_ik_solver_enable_dict', (enable_info_map,), True)
        return

    def _refresh_all_ik_solver_enabled(self):
        for index in range(self.ik_solver_count):
            self._refresh_ik_solver_enabled(index)

    def on_post_join_mecha(self, *args):
        self.is_avatar = self.ev_g_is_avatar()
        self._register_quality_event(True)
        self._refresh_all_ik_solver_enabled()

    def _update_ik_skip_update_frame(self):
        self.skip_update_frame = max(self.cur_lod_level - 1, 0)
        for ik_solver in self.ik_solver_list:
            ik_solver.set_provider_parameters(world.BIND_TYPE_BONE_GROUND, (self.skip_cid, self.skip_update_frame))

    def on_mecha_lod_loaded(self, *args):
        self.cur_lod_level = self.ev_g_lod_level()
        self._update_ik_skip_update_frame()
        self._refresh_all_ik_solver_enabled()

    def on_quality_changed(self, quality):
        self.cur_quality = quality
        self._refresh_all_ik_solver_enabled()

    def _set_ik_parameters(self, param_map, index):
        if index not in self.ik_param_data_for_reset:
            self.ik_param_data_for_reset[index] = {}
        ik_parameters = self.ik_parameters_list[index]
        for param_name, param_value in param_map.items():
            if param_name not in self.ik_param_data_for_reset[index]:
                self.ik_param_data_for_reset[index][param_name] = ik_parameters[param_name]
            ik_parameters[param_name] = param_value

        self._refresh_ik_parameters(index)

    def set_ik_parameters(self, param_map, index=None):
        if index is None:
            for index in range(self.ik_solver_count):
                self._set_ik_parameters(param_map, index)

        else:
            self._set_ik_parameters(param_map, index)
        return

    def _reset_ik_parameters(self, param_names, index):
        if index not in self.ik_param_data_for_reset:
            return
        ik_parameters = self.ik_parameters_list[index]
        if param_names:
            data_for_reset = self.ik_param_data_for_reset[index]
            for param_name in param_names:
                if param_name in data_for_reset:
                    ik_parameters[param_name] = data_for_reset.pop(param_name)

            if not data_for_reset:
                self.ik_param_data_for_reset.pop(index)
        else:
            data_for_reset = self.ik_param_data_for_reset.pop(index)
            for param_name, param_value in data_for_reset.items():
                ik_parameters[param_name] = param_value

        self._refresh_ik_parameters(index)

    def reset_ik_parameters(self, param_names, index=None):
        if index is None:
            for index in range(self.ik_solver_count):
                self._reset_ik_parameters(param_names, index)

        else:
            self._reset_ik_parameters(param_names, index)
        return

    def on_play_anim(self, anim_name, *args, **kwargs):
        playing_turn_anim = anim_name in TURN_ANIM_NAMES
        if self.is_playing_turn_anim ^ playing_turn_anim:
            self._unregister_reset_timer()
            if playing_turn_anim:
                self.set_ik_parameters({'ik_pitch_intrp_speed': 80})
            else:
                self.delay_reset_timer = global_data.game_mgr.register_logic_timer(lambda : self.reset_ik_parameters(['ik_pitch_intrp_speed']), interval=0.2, times=1, mode=CLOCK)
            self.is_playing_turn_anim = playing_turn_anim

    def apply_editor_ik_parameters(self, ik_key):
        if ik_key in self.ik_key_to_index_list_map:
            index_list = self.ik_key_to_index_list_map[ik_key]
            for index in index_list:
                cur_effective_parameters = global_data.editor_mecha_foot_ik_parameters[ik_key]
                for param_name, param_value in cur_effective_parameters.items():
                    if param_name == 'ik_foot_pitch_enabled':
                        param_name = 'ignore_target_rotation'
                        param_value = not bool(param_value)
                    if index in self.ik_param_data_for_reset and param_name in self.ik_param_data_for_reset[index]:
                        self.ik_param_data_for_reset[index][param_name] = param_value
                    else:
                        self.ik_parameters_list[index][param_name] = param_value

                self._refresh_ik_parameters(index)