# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/parts/camera/CameraTargetManager.py
from __future__ import absolute_import
from __future__ import print_function
from data.camera_state_const import *
from logic.client.const.camera_const import POSTURE_STAND, POSTURE_SQUAT, POSTURE_KNOCK_DOWN, POSTURE_SWIM, VALID_CAMERA_POSTURE
VIEWER_UPDATE_FRAME = 10
from logic.client.const.camera_const import FREE_CAMERA_LIST
from logic.gcommon.common_utils.parachute_utils import STAGE_FREE_DROP, STAGE_PARACHUTE_DROP, STAGE_PLANE, STAGE_FLY_CARRIER, STAGE_NONE, STAGE_LAUNCH_PREPARE
import math3d
from logic.gutils.CameraHelper import is_posture_inherit_camera_type, is_support_transfer_to_free_mode
from logic.gcommon.cdata import status_config
from logic.gcommon.component.client.com_camera import camera_target_com_utils
from logic.vscene.parts.camera.ObserveFreeCameraSwitchChecker import ObserveFreeCameraSwitchChecker
from logic.vscene.parts.gamemode.GMDecorator import execute_by_mode
from logic.client.const import game_mode_const
from logic.gutils.client_unit_tag_utils import preregistered_tags

class CameraTargetManager(object):

    def __init__(self, camera_manager):
        self.player = None
        self.follow_target_id = None
        self.follow_target = None
        self.cam_manager = camera_manager
        self.init_parameters()
        return

    @property
    def cam_state(self):
        return self.cam_manager.cam_state

    @property
    def is_in_observe(self):
        return self._is_in_observe

    @is_in_observe.setter
    def is_in_observe(self, val):
        self._is_in_observe = val
        self.cam_manager.is_in_observe = val

    def get_cur_camera_state_type(self):
        return self.cam_state.TYPE

    def get_cur_camera_magnification_triplet(self):
        return self.cam_manager.get_cur_camera_magnification_triplet()

    def get_cur_camera_aim_scope_id(self):
        return self.cam_manager.get_cur_camera_aim_scope_id()

    def refresh_yaw_pitch(self):
        self.cam_manager.check_refresh_yaw_and_pitch()

    def on_enter(self):
        self.process_bind_events(True)
        player = global_data.game_mgr.scene.get_player()
        if player:
            self.on_player_setted(player)

    def init_parameters(self):
        self.cur_camera_state_type = None
        self.init_camera_state = THIRD_PERSON_MODEL
        self.init_camera_kwargs = {}
        self._is_in_observe = False
        self.is_in_observe_free = False
        self.need_recover_observe_status = False
        self._cur_cam_effect_model = None
        return

    def destroy(self):
        self.process_bind_events(False)
        self.on_player_setted(None)
        self.cam_manager = None
        self.init_camera_state = None
        self.init_camera_kwargs = {}
        return

    def process_bind_events(self, is_bind):
        emgr = global_data.emgr
        events = {'scene_player_setted_event': self.on_avatar_setted,
           'scene_observed_player_setted_for_cam': self.on_observe_target_setted,
           'switch_target_to_camera_state_event': self.switch_target_to_camera_state,
           'replace_last_camera_state_event': self._on_replace_last_camera_state,
           'switch_to_last_camera_state_event': self.switch_to_last_camera_state,
           'switch_to_aim_camera_event': self.switch_to_aim_camera,
           'target_dead_event': self.on_target_dead,
           'target_defeated_event': self.on_target_dead,
           'camera_enter_free_observe_event': self.enter_free_observe_camera,
           'camera_leave_free_observe_event': self.leave_free_observe_camera,
           'on_observer_parachute_stage_changed': self.on_observer_parachute_stage_changed,
           'on_speed_up': self.on_speed_up_changed,
           'switch_to_right_aim_camera_event': self.switch_to_right_aim,
           'exit_right_aim_camera_event': self.exit_right_aim,
           'switch_to_airship_camera': self.on_switch_airship_camera,
           'switch_to_mecha_camera': self.on_switch_to_mecha_camera,
           'switch_observe_camera_state_event': self.observe_switch_cam_state,
           'net_reconnect_before_destroy_event': self.on_net_reconnect,
           'on_sync_cam_state_event': self.on_sync_cam_state,
           'g_get_in_observe_free': self.get_in_observe_free,
           'recover_observe_camera_event': self.recover_target_observe_camera,
           'refresh_camera_follow_target_position': self.on_refresh_camera_follow_target_position
           }
        if is_bind:
            emgr.bind_events(events)
        else:
            emgr.unbind_events(events)

    def on_net_reconnect(self, *args):
        if self.cam_state.TYPE == AIM_MODE:
            global_data.emgr.switch_to_last_camera_state_event.emit()

    def get_ctrl_target(self):
        from mobile.common.EntityManager import EntityManager
        entity = EntityManager.getentity(self.follow_target_id)
        return entity

    def handle_target_model_load(self, model):
        ctrl_target = self.get_ctrl_target()
        if not (ctrl_target and ctrl_target.logic):
            return
        else:
            self.on_become_cam_target(ctrl_target.logic)
            if self.follow_target_id != ctrl_target.id:
                return
            _plogic = ctrl_target.logic
            _plogic_pos = _plogic.ev_g_position()
            _plogic_specified_pos = _plogic.ev_g_camera_follow_position()
            self.bind_shadowtex_obj(model)
            self.set_model_cam_effect_enable(model)
            self.bind_follow_target(_plogic)
            if self.init_camera_state is not None:
                if self.get_follow_target_model() is not None:
                    battle = global_data.battle
                    if battle:
                        is_in_island = battle.is_in_island() if 1 else False
                        if not _plogic.ev_g_is_parachute_prepare() or is_in_island:
                            self.init_target_pos(_plogic_specified_pos or model.world_position, True)
                            if 'force_trans_time' in self.init_camera_kwargs:
                                del self.init_camera_kwargs['force_trans_time']
                            self.switch_cam_state(self.init_camera_state, force_trans_time=0, **self.init_camera_kwargs)
                            self.init_camera_state = None
                            self.init_camera_kwargs = {}
                            global_data.emgr.camera_inited_event.emit()
                        else:
                            self.init_camera_state = None
                            self.init_camera_kwargs = {}
                else:
                    self.init_target_pos(_plogic_specified_pos, False)
                _plogic.unregist_event('E_MODEL_LOADED', self.handle_target_model_load)
                if self.need_recover_observe_status and self.is_in_observe and self.player:
                    self.need_recover_observe_status = False
                    self.recover_cur_target_status(self.player, True)
            _plogic.send_event('E_ON_CAM_LCTARGET_SET')
            if self.player:
                self.player.send_event('E_ON_CAM_LPLAYER_SET')
            global_data.emgr.scene_camera_target_model_loaded_event.emit()
            return

    def on_avatar_setted(self, player):
        if player:
            if player.ev_g_is_in_spectate():
                return
        self.on_player_setted(player)

    def on_observe_target_setted(self, target, new_cam_lplayer=None, is_observe=True):
        if target is None:
            self.is_in_observe = False
            self.need_recover_observe_status = False
            if new_cam_lplayer:
                target = new_cam_lplayer
        else:
            self.is_in_observe = is_observe
            self.need_recover_observe_status = is_observe
        self.on_player_setted(target)
        global_data.emgr.scene_cam_observe_player_setted.emit()
        return

    def recover_cur_target_status(self, target, remain_observe_free=False):
        from .ObserveCameraRecover import ObserveCameraRecover
        ObserveCameraRecover().recover_camera_status(target)

    def recover_target_observe_camera(self, remain_observe_free=False):
        if global_data.cam_lplayer:
            self.recover_cur_target_status(global_data.cam_lplayer)
        else:
            log_error('recover_target_observe_camera failed! global_data.cam_lplayer is None')

    def on_player_setted(self, player):
        cnt_lplayer = global_data.cam_lplayer
        old_lplayer = cnt_lplayer
        is_switching_player = False
        if old_lplayer != player:
            is_switching_player = True
        self.cam_manager.on_before_switch_cam_player()
        self.unbind_cur_player_event()
        self.unbind_cur_follow_target()
        self.unbind_shadowtex_obj()
        self.set_model_cam_effect_enable(None)
        self._world_offset = math3d.vector(0, 0, 0)
        octrl_target = self.get_ctrl_target()
        if octrl_target and octrl_target.logic:
            octrl_target.logic.unregist_event('E_MODEL_LOADED', self.handle_target_model_load)
            self.on_leave_cam_target(octrl_target.logic)
        global_data.cam_lctarget = None
        self.player = player
        if cnt_lplayer and is_switching_player:
            self.on_del_player_coms(cnt_lplayer)
        if is_switching_player:
            role_id = player.ev_g_role_id() if player else None
            self.cam_manager.on_switch_cam_lplayer(role_id)
        global_data.cam_lplayer = player
        if player and is_switching_player:
            self.on_add_player_coms(player)
            global_data.emgr.scene_camera_switch_player_setted_event.emit()
        global_data.emgr.scene_camera_player_setted_event.emit()
        if player is None:
            return
        else:
            ctrl_target = player.ev_g_control_target()
            if not ctrl_target:
                self.output_debug_info(player, ctrl_target)
                return
            if ctrl_target and not ctrl_target.logic:
                self.output_debug_info(player, ctrl_target)
                return
            l_target = ctrl_target.logic
            global_data.cam_lctarget = l_target
            global_data.emgr.scene_camera_target_setted_event.emit()
            self.follow_target_id = ctrl_target.id
            pos = l_target.ev_g_position()
            if pos:
                self.init_target_pos(None, is_switching_player)
                POS_CHANGE_THRES = 300
                if (global_data.game_mgr.scene.active_camera.position - pos).length > POS_CHANGE_THRES:
                    global_data.game_mgr.scene.active_camera.position = pos
                global_data.game_mgr.scene.do_set_viewer_position(pos)
            self.bind_player_event(player)
            model = l_target.ev_g_model()
            if model is None:
                l_target.unregist_event('E_MODEL_LOADED', self.handle_target_model_load)
                l_target.regist_event('E_MODEL_LOADED', self.handle_target_model_load)
            else:
                self.handle_target_model_load(model)
            return

    def on_refresh_camera_follow_target_position(self, pos):
        ctrl_target = self.get_ctrl_target()
        if not (ctrl_target and ctrl_target.logic):
            return False
        if not ctrl_target.logic.ev_g_model():
            return False
        ctrl_target_position = ctrl_target.logic.ev_g_position()
        if not ctrl_target_position:
            return False
        self.cam_manager.on_target_pos_changed(ctrl_target_position)
        return (
         True, (pos - ctrl_target_position).length)

    def bind_follow_target(self, target):
        if G_POS_CHANGE_MGR:
            target.regist_pos_change(self.cam_manager.on_target_pos_changed)
        else:
            target.send_event('E_REGISTER_A2G_EVENT', 'E_POSITION', 'camera_target_pos_changed_event')
        self.follow_target = target

    def bind_player_event(self, target):
        target.regist_event('E_STAND', self.on_change_posture_stand)
        target.regist_event('E_SQUAT', self.on_change_posture_squat)
        target.regist_event('E_AGONY', self.on_change_posture_knock_down, 10)
        target.regist_event('E_SWIM', self.on_change_posture_swim)
        target.regist_event('E_BOARD_SKATE', self.board_skate)
        target.regist_event('E_SUCCESS_AIM', self.on_open_aim_camera)
        target.regist_event('E_QUIT_AIM', self.on_close_aim_camera)
        target.regist_event('E_ON_CONTROL_TARGET_CHANGE', self.on_switch_control_target)
        target.regist_event('E_TO_THIRD_PERSON_CAMERA', self.switch_to_third_camera)
        target.regist_event('E_TO_VEHICLE_CAMERA', self.update_vehicle_camera)
        target.regist_event('E_TO_PASSENGER_VEHICLE_CAMERA', self.update_passenger_vehicle_camera)
        target.regist_event('E_FREE_CAMERA_STATE', self.set_free_camera_state)
        target.regist_event('E_TO_DRONE_CAMERA', self.on_switch_drone_camera)
        target.regist_event('E_TO_HIDING_CAMERA', self.on_switch_hiding_camera)
        if not target.ev_g_is_avatar():
            target.regist_event('E_ENTER_STATE', self.enter_states)

    def enter_states(self, new_state):
        state_event = {status_config.ST_STAND: self.on_change_posture_stand,
           status_config.ST_CROUCH: self.on_change_posture_squat,
           status_config.ST_SWIM: self.on_change_posture_swim
           }
        func = state_event.get(new_state, None)
        if func:
            func()
        return

    def unbind_cur_follow_target(self):
        if self.follow_target and self.follow_target.is_valid():
            if self.follow_target.send_event:
                if G_POS_CHANGE_MGR:
                    self.follow_target.unregist_pos_change(self.cam_manager.on_target_pos_changed)
                else:
                    self.follow_target.send_event('E_UNREGISTER_A2G_EVENT', 'E_POSITION', 'camera_target_pos_changed_event')
            self.follow_target = None
        return

    def unbind_cur_player_event(self):
        if self.player:
            if self.player.unregist_event:
                func = self.player.unregist_event
                func('E_STAND', self.on_change_posture_stand)
                func('E_SQUAT', self.on_change_posture_squat)
                func('E_AGONY', self.on_change_posture_knock_down)
                func('E_SWIM', self.on_change_posture_swim)
                func('E_BOARD_SKATE', self.board_skate)
                func('E_SUCCESS_AIM', self.on_open_aim_camera)
                func('E_QUIT_AIM', self.on_close_aim_camera)
                func('E_ON_CONTROL_TARGET_CHANGE', self.on_switch_control_target)
                func('E_TO_THIRD_PERSON_CAMERA', self.switch_to_third_camera)
                func('E_TO_VEHICLE_CAMERA', self.update_vehicle_camera)
                func('E_TO_PASSENGER_VEHICLE_CAMERA', self.update_passenger_vehicle_camera)
                func('E_FREE_CAMERA_STATE', self.set_free_camera_state)
                func('E_TO_DRONE_CAMERA', self.on_switch_drone_camera)
                func('E_TO_HIDING_CAMERA', self.on_switch_hiding_camera)
                if not self.player.ev_g_is_avatar():
                    func('E_ENTER_STATE', self.enter_states)

    def bind_shadowtex_obj(self, model):
        global_data.game_mgr.scene.set_shadowtex_obj(model)

    def unbind_shadowtex_obj(self):
        if global_data.game_mgr.scene and global_data.game_mgr.scene.valid:
            global_data.game_mgr.scene.set_shadowtex_obj(None)
        return

    def init_target_pos(self, pos, need_immediately):
        m = self.get_follow_target_model()
        if m is None:
            print('no target ???????')
            return
        else:
            world_pos = pos or m.world_position
            if self.cam_manager:
                self.cam_manager.init_target_pos(world_pos, need_immediately)
            return

    def get_follow_target_model(self):
        if self.follow_target:
            m = self.follow_target.ev_g_model()
            return m
        else:
            return None

    def on_change_posture_stand(self):
        self.on_switch_player_posture(POSTURE_STAND)

    def board_skate(self):
        self.on_switch_player_posture(POSTURE_STAND)

    def on_change_posture_squat(self):
        self.on_switch_player_posture(POSTURE_SQUAT)

    @execute_by_mode(False, game_mode_const.No_KnockDown)
    def on_change_posture_knock_down(self):
        self.on_switch_player_posture(POSTURE_KNOCK_DOWN)

    def on_change_posture_swim(self):
        self.on_switch_player_posture(POSTURE_SWIM)

    def on_open_aim_camera(self):
        import logic.gcommon.const as const
        if self.player:
            target = self.player
            lens_attachment = target.ev_g_attachment_attr(const.ATTACHEMNT_AIM_POS)
            if not lens_attachment:
                return
            len_attr_data = lens_attachment.get('cAttr', {})
            aim_magnitude = len_attr_data.get('iLensMagnitude', 2)
            aim_item_id = lens_attachment.get('iType', 0)
            fAimTime = len_attr_data.get('fAimTime', 0.4)
            global_data.emgr.switch_to_aim_camera_event.emit(aim_magnitude, fAimTime, item_id=aim_item_id)

    def on_close_aim_camera(self):
        if self.cam_state.TYPE == AIM_MODE:
            global_data.emgr.switch_to_last_camera_state_event.emit()
        elif self.init_camera_state == AIM_MODE:
            self.recover_cur_target_status(self.player)

    def on_switch_control_target(self, target_id, pos, *args):
        self.on_refresh_camera()

    def on_refresh_camera(self):
        if not self.player:
            return
        self.on_player_setted(self.player)

    def switch_to_third_camera(self):
        self.switch_cam_state(THIRD_PERSON_MODEL)

    def on_switch_drone_camera(self):
        self.switch_cam_state(DRONE_MODE)
        global_data.sound_mgr.play_sound('Play_drone', None, ('drone_option', 'drone_monitor_open'))
        return

    def on_switch_airship_camera(self):
        self.switch_cam_state(AIRSHIP_MODE)

    def on_switch_hiding_camera(self):
        self.switch_cam_state(HIDING_MODE)

    def on_switch_to_mecha_camera(self, mode, **kwargs):
        self.switch_cam_state(mode, **kwargs)

    def switch_cam_state(self, new_cam_type, **kwargs):
        if not self.is_in_observe:
            self.normal_switch_cam_state(new_cam_type, **kwargs)
        else:
            self.observe_switch_cam_state(new_cam_type, **kwargs)

    def normal_switch_cam_state(self, new_cam_type, **kwargs):
        if self.player is None or self.follow_target is None or self.get_follow_target_model() is None or not self.player.is_valid():
            self.init_camera_state = new_cam_type
            self.init_camera_kwargs = kwargs
            return
        else:
            if not self.cam_manager.cur_target_pos:
                self.init_target_pos(None, True)
            if self.cam_state:
                self.last_camera_state_setting = self.cam_state.dump_camera_setting()
            posture = self.get_target_posture(self.player)
            global_data.emgr.set_cur_camera_posture_event.emit(posture)
            global_data.emgr.switch_camera_state_event.emit(new_cam_type, **kwargs)
            if not self.is_in_observe:
                if self.player:
                    self.player.send_event('E_CAM_STATE', new_cam_type)
            return

    def update_vehicle_camera(self, lvehicle):
        if self.cam_state.TYPE == VEHICLE_MODE:
            return
        from logic.gcommon.common_const import mecha_const
        if lvehicle.ev_g_pattern() == mecha_const.MECHA_TYPE_VEHICLE:
            self.switch_cam_state(VEHICLE_MODE)
        else:
            self.switch_cam_state(MECHA_MODE_TWO)
        if self.is_in_observe:
            if lvehicle:
                lvehicle.send_event('E_VEHICLE_COLLISION_SET', True)

    def update_passenger_vehicle_camera(self, lvehicle):
        self.switch_cam_state(PASSENGER_VEHICLE_MODE)
        if self.is_in_observe:
            if lvehicle:
                lvehicle.send_event('E_VEHICLE_COLLISION_SET', True)

    def on_switch_player_posture(self, new_posture):
        self.cam_manager.on_switch_player_posture(new_posture)

    def get_target_posture(self, target):
        if not self.cam_state.is_enable_player_posture():
            return POSTURE_STAND
        else:
            if target and target.is_valid():
                if target.ev_g_agony():
                    return POSTURE_KNOCK_DOWN
                else:
                    cur_posture = target.ev_g_posture()
                    if cur_posture is not None and cur_posture in VALID_CAMERA_POSTURE:
                        return cur_posture
                    return POSTURE_STAND

            return POSTURE_STAND

    def refresh_yaw_range(self):
        self.cam_manager.refresh_yaw_range()

    def set_yaw(self, yaw):
        global_data.emgr.camera_set_yaw_event.emit(yaw)

    def set_pitch(self, pitch):
        global_data.emgr.camera_set_pitch_event.emit(pitch)

    def set_yaw_and_pitch(self, yaw, pitch):
        self.cam_manager.set_yaw_and_pitch(yaw, pitch)

    def switch_to_right_aim(self):
        self.switch_cam_state(RIGHT_AIM_MODE)

    def exit_right_aim(self):
        if self.follow_target.__class__.__name__ == 'LMotorcycle':
            self.switch_cam_state(MOTORCYCLE_SEAT_3_MODE)
        else:
            self.switch_cam_state(THIRD_PERSON_MODEL)

    def on_observer_parachute_stage_changed(self, stage):
        if stage in (STAGE_PLANE, STAGE_NONE, STAGE_LAUNCH_PREPARE):
            global_data.emgr.camera_enable_follow_event.emit(False)
            return
        global_data.emgr.scene_enable_camera_ctrl_viewpos.emit(stage != STAGE_FREE_DROP)
        global_data.emgr.camera_enable_follow_event.emit(True)

    def on_speed_up_changed(self, enable):
        if enable and self.get_cur_camera_state_type() == THIRD_PERSON_MODEL:
            self.switch_cam_state(THIRD_PERSON_SPEED_UP_MODE)
        if not enable and self.get_cur_camera_state_type() == THIRD_PERSON_SPEED_UP_MODE:
            self.switch_cam_state(THIRD_PERSON_MODEL)

    @execute_by_mode(False, game_mode_const.No_Dead)
    def on_target_dead(self, *args):
        from logic.gcommon.common_utils import battle_utils
        if battle_utils.is_battle_signal_open() and self.player and self.player.ev_g_signal() <= 0 and self.player.ev_g_killer() is None:
            return
        else:
            if self.cam_state.TYPE != DEAD_MODEL:
                self.switch_cam_state(DEAD_MODEL)
            return

    def _on_replace_last_camera_state(self, camera_state, **kwargs):
        if not self.last_camera_state_setting:
            return
        else:
            if camera_state is not None:
                cam_state_obj = self.cam_manager.new_cam_state(camera_state, **kwargs)
                if cam_state_obj:
                    self.last_camera_state_setting = cam_state_obj.dump_camera_setting()
                    self.cam_manager.del_cam_state(cam_state_obj)
            return

    def switch_to_last_camera_state(self):
        if self.last_camera_state_setting:
            last_type = self.last_camera_state_setting.get('real_type', None) or self.last_camera_state_setting.get('type', None)
            if last_type is not None:
                if is_support_transfer_to_free_mode(last_type):
                    global_data.player.logic and global_data.player.logic.ev_g_cancel_state(status_config.ST_AIM)
                    self.switch_cam_state(last_type)
        return

    def switch_to_aim_camera(self, aim_magnitude, trans_time, need_hide_model=True, item_id=0):
        if self.cam_state.TYPE == AIM_MODE and not self.is_in_observe:
            return
        self.switch_cam_state(AIM_MODE, magnification=aim_magnitude, transfer_time=trans_time, need_hide_model=need_hide_model, item_id=item_id)

    def enter_free_observe_camera(self):
        real_ty = self.cam_state.get_real_camera_type()
        target_state = ObserveFreeCameraSwitchChecker.get_target_camera_state(self.player, self.follow_target, real_ty)
        self.is_in_observe_free = True
        self.switch_cam_state(OBSERVE_FREE_MODE, cam_type=target_state)

    def leave_free_observe_camera(self):
        self.is_in_observe_free = False
        self.recover_cur_target_status(self.player, remain_observe_free=False)

    def observe_switch_cam_state(self, new_cam_type, **kwargs):
        if self.cam_state.TYPE == OBSERVE_FREE_MODE and self.is_in_observe_free:
            if new_cam_type == AIM_MODE:
                return
            is_can_switch = ObserveFreeCameraSwitchChecker.check_can_switch(self.player, self.follow_target, new_cam_type)
            if is_can_switch and self.cam_state.get_real_camera_type() != new_cam_type:
                if not is_posture_inherit_camera_type(new_cam_type):
                    self.normal_switch_cam_state(OBSERVE_FREE_MODE, cam_type=new_cam_type)
        else:
            self.normal_switch_cam_state(new_cam_type, **kwargs)

    def get_in_observe_free(self):
        return self.is_in_observe and self.is_in_observe_free

    def set_free_camera_state(self, state):
        if self.is_in_observe_free:
            return
        if state:
            from logic.gcommon.common_utils.local_text import get_text_by_id
            if not is_support_transfer_to_free_mode(self.get_cur_camera_state_type()):
                global_data.emgr.battle_show_message_event.emit(get_text_by_id(18072))
            else:
                self.switch_cam_state(FREE_MODEL)
        elif self.get_cur_camera_state_type() in FREE_CAMERA_LIST:
            global_data.emgr.switch_to_last_camera_state_event.emit()

    def on_become_cam_target(self, target):
        lst_complete = []
        enable_event_list = self.get_cam_target_conf(target)
        for cname, path in enable_event_list:
            com = target.get_com(cname)
            if com is None:
                com = target.add_com(cname, path)
                com.init_from_dict(target, {})
                lst_complete.append(com)

        for com in lst_complete:
            com.on_init_complete()

        for com in lst_complete:
            com.on_post_init_complete({})

        return

    def on_leave_cam_target(self, target):
        enable_event_list = self.get_cam_target_conf(target)
        for cname, path in enable_event_list:
            com = target.get_com(cname)
            if com is not None:
                target.del_com(cname)

        return

    def get_cam_target_conf(self, target):
        if not target:
            return []
        ret_com_list = []
        if target.MASK & preregistered_tags.HUMAN_TAG_VALUE:
            conf_name = 'HUMAN_TARGET_COMS'
            ret_com_list.extend(camera_target_com_utils.cam_target_coms.get(conf_name, []))
        else:
            ret_com_list.extend(camera_target_com_utils.cam_target_coms.get('NON_HUMAN_TARGET_COMS', []))
            if target.share_data.ref_mecha_id:
                conf_name = 'MECHA_TARGET_COMS'
                ret_com_list.extend(camera_target_com_utils.cam_target_coms.get(conf_name, []))
        ret_com_list.append(('ComDataCamTarget', 'client'))
        return ret_com_list

    def on_add_player_coms(self, target):
        from logic.units.LAvatar import LAvatar
        from logic.units.LPuppet import LPuppet
        if isinstance(target, LAvatar):
            com = target.add_com('ComPlayerGlobalSender', 'client.com_global_sync')
        elif isinstance(target, LPuppet):
            com = target.add_com('ComObserverGlobalSender', 'client.com_global_sync')
        else:
            raise NotImplementedError('Not Support target become camera target!:%s' % str(type(target)))
        if com:
            com.init_from_dict(target, {})
        lst_complete = []
        enable_event_list = camera_target_com_utils.cam_target_coms.get('PLAYER_COMS', [])
        for cname, path in enable_event_list:
            com = target.get_com(cname)
            if com is None:
                com = target.add_com(cname, path)
                com.init_from_dict(target, {})
                lst_complete.append(com)

        for com in lst_complete:
            com.on_init_complete()

        for com in lst_complete:
            com.on_post_init_complete({})

        return

    def on_del_player_coms(self, target):
        from logic.units.LAvatar import LAvatar
        from logic.units.LPuppet import LPuppet
        if isinstance(target, LAvatar):
            target.del_com('ComPlayerGlobalSender')
        elif isinstance(target, LPuppet):
            target.del_com('ComObserverGlobalSender')
        else:
            raise NotImplementedError()
        enable_event_list = camera_target_com_utils.cam_target_coms.get('PLAYER_COMS', [])
        for cname, path in enable_event_list:
            com = target.get_com(cname)
            if com is not None:
                target.del_com(cname)

        return

    def switch_target_to_camera_state(self, camera_state, **kwargs):
        if camera_state != self.get_cur_camera_state_type() or camera_state == AIM_MODE:
            self.switch_cam_state(camera_state, **kwargs)

    def output_debug_info(self, player, control_target):
        import traceback
        traceback.print_stack()
        log_error('player = ', player)
        log_error('control target = ', control_target)

    def set_model_cam_effect_enable(self, model):
        import weakref
        if self._cur_cam_effect_model and self._cur_cam_effect_model() == model:
            return
        else:
            if self._cur_cam_effect_model is not None:
                old_model = self._cur_cam_effect_model()
                if old_model and old_model.valid:
                    old_model.set_cam_effect_enable(False)
                self._cur_cam_effect_model = None
            if model and hasattr(model, 'set_cam_effect_enable'):
                self._cur_cam_effect_model = weakref.ref(model)
                model.set_cam_effect_enable(True)
            return

    def on_sync_cam_state(self, cam_state):
        old_cam_state = self.get_cur_camera_state_type()
        if cam_state == FREE_MODEL:
            self.set_free_camera_state(True)
        elif old_cam_state == FREE_MODEL:
            self.set_free_camera_state(False)
        if old_cam_state != cam_state:
            self.switch_cam_state(cam_state)
            self.check_sync_cam_state_rot(old_cam_state, self.cam_state.TYPE)

    def check_sync_cam_state_rot(self, old_cam_state, new_cam_state):
        from .ObserveCameraStates import check_sync_cam_state_rot_helper
        res = check_sync_cam_state_rot_helper(self.player, old_cam_state, new_cam_state)
        if res:
            f_yaw, f_pitch = res
            global_data.emgr.set_camera_yaw_pitch_with_slerp_event.emit(f_yaw, f_pitch, True)