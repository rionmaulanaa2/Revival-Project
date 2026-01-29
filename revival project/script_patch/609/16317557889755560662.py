# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/behavior/BoardMechaLogic.py
from __future__ import absolute_import
from __future__ import print_function
import math3d
import world
from .StateBase import StateBase
from logic.gcommon.common_const.character_anim_const import *
from logic.gcommon.component.client.com_character_ctrl.ComAnimMgr import DEFAULT_ANIM_NAME
from logic.gcommon.const import NEOX_UNIT_SCALE
from common.utils import timer
import logic.gcommon.common_const.animation_const as animation_const
import logic.gcommon.cdata.status_config as status_config
from mobile.common.EntityManager import EntityManager
from common.cfg import confmgr
from logic.gutils.CameraHelper import track_build
import logic.gcommon.common_utils.bcast_utils as bcast
from logic.gutils.CameraHelper import get_mecha_camera_type
from logic.gcommon.common_const import mecha_const
from data import camera_state_const
from logic.gutils import character_action_utils
import math
from logic.gutils import mecha_utils
pi2 = math.pi * 2
MODEL_SHADER_CTRL_SET_ENABLE = hasattr(world.model, 'set_inherit_parent_shaderctrl')

class MechaBoard(StateBase):
    BIND_EVENT = {'E_ON_ACTION_ENTER_MECHA': '_on_enter_mecha',
       'E_CLEAR_JOIN_MECHA_ACTION': '_clear_join_mecha_action',
       'E_TEST_MECHA_STATE': 'test_adjust_to_mecha_camera',
       'E_DEATH': '_cancel_enter_mecha',
       'E_AGONY': '_cancel_enter_mecha',
       'E_ANIMATOR_LOADED': 'on_load_animator_complete'
       }

    def init_from_dict(self, unit_obj, bdict, sid, state_info):
        super(MechaBoard, self).init_from_dict(unit_obj, bdict, sid, state_info)
        self._clear_timer = None
        self._force_interrupt_enter = False
        self._enter_mecha_id = 0
        self._anim_time = 0
        return

    def on_load_animator_complete(self, *args):
        animator = self.ev_g_animator()
        if not animator:
            return
        self.send_event('E_REGISTER_ANIM_KEY_EVENT', 'mount_8001', 'hide', self._end_enter_mecha)
        self.send_event('E_REGISTER_ANIM_KEY_EVENT', 'mount_8002', 'hide', self._end_enter_mecha)

    def enter(self, leave_states):
        self.send_event('E_SWITCH_STATUS', animation_const.STATE_ENTER_MECHA)
        super(MechaBoard, self).enter(leave_states)

    def exit(self, enter_states):
        elapsed_time = self.elapsed_time
        super(MechaBoard, self).exit(enter_states)
        self._clear_join_mecha_action()
        if self._enter_mecha_id:
            self._end_enter_mecha()
        if elapsed_time >= self._anim_time:
            entity = EntityManager.getentity(self._enter_mecha_id)
            if entity and entity.logic:
                self._enter_mecha_id = 0

    def update(self, dt):
        super(MechaBoard, self).update(dt)
        if self._anim_time > 0 and self.elapsed_time >= self._anim_time:
            self.disable_self()
            self._try_join_mecha()

    def _end_enter_mecha(self, *args):
        self._try_join_mecha()
        entity = EntityManager.getentity(self._enter_mecha_id)
        if entity and entity.logic:
            unregist_func = entity.logic.unregist_event
            unregist_func('E_DEATH', self._cancel_enter_mecha)
            self._enter_mecha_id = 0
        self.unregist_event('E_DEATH', self._cancel_enter_mecha)
        self.unregist_event('E_AGONY', self._cancel_enter_mecha)

    def test_adjust_to_mecha_camera(self):
        mecha_camera_state = 20
        from logic.gutils.CameraHelper import get_camera_state_def_mat
        scn = global_data.game_mgr.scene
        cam = scn.active_camera
        from logic.client.const.camera_const import POSTURE_STAND, THIRD_PERSON_MODEL
        end_mat_org = get_camera_state_def_mat(mecha_camera_state, POSTURE_STAND, self.ev_g_role_id())
        start_mat_org = get_camera_state_def_mat(THIRD_PERSON_MODEL, POSTURE_STAND, self.ev_g_role_id())
        self.adjust_to_mecha_camera(mecha_camera_state, '1', start_mat_org, end_mat_org, 5)

    def _clear_join_mecha_action(self):
        if self._clear_timer:
            global_data.game_mgr.unregister_logic_timer(self._clear_timer)
            self._clear_timer = 0

    def _on_enter_mecha(self, mecha_id, *args):
        self._enter_mecha_id = mecha_id
        if not self.ev_g_is_avatar() and not self.sd.ref_is_agent:
            return
        self.active_self()
        self._force_interrupt_enter = False
        self._anim_time = 0
        self.send_event('E_SET_EMPTY_HAND', False)
        entity = EntityManager.getentity(self._enter_mecha_id)
        if not entity or not entity.logic:
            return
        model = entity.logic.ev_g_model()
        if not model:
            return
        target_pos = model.position - model.rotation_matrix.forward * 2 * NEOX_UNIT_SCALE
        from_pos = self.ev_g_position() or target_pos
        dist = target_pos - from_pos
        if dist.is_zero:
            self._action_enter_mecha()
        elif entity.is_share():
            if G_POS_CHANGE_MGR:
                self.notify_pos_change(target_pos, True)
            else:
                self.send_event('E_POSITION', target_pos)
            f_yaw = model.rotation_matrix.forward.yaw
            if self.ev_g_is_cam_target():
                global_data.emgr.set_camera_yaw_pitch_with_slerp_event.emit(f_yaw, 0, False)
            self._action_enter_mecha()
        else:
            self.mount_dist = dist.length
            self.cur_pos = self.ev_g_position()
            speed = dist
            speed.normalize()
            speed = speed * 100

            def lerp_cb(dt):
                if not self.unit_obj or not self.unit_obj.is_valid():
                    return timer.RELEASE
                self.cur_pos += speed * dt
                if G_POS_CHANGE_MGR:
                    self.notify_pos_change(self.cur_pos)
                else:
                    self.send_event('E_POSITION', self.cur_pos)
                self.mount_dist -= 100 * dt
                if self.mount_dist <= 0:
                    self._action_enter_mecha()
                    return timer.RELEASE

            global_data.game_mgr.register_logic_timer(lerp_cb, interval=1, times=-1, mode=timer.LOGIC, timedelta=True)

    def _action_enter_mecha(self):
        if not self or not self.is_valid():
            return
        if self.ev_g_death() or self.ev_g_agony():
            return
        mecha_entity_id = self._enter_mecha_id
        entity = EntityManager.getentity(mecha_entity_id)
        if entity and entity.logic:
            entity.logic.send_event('E_RESUME_MOUNT')
            mecha_type_id = entity.logic.share_data.ref_mecha_id
            clip_name = 'mount_{}'.format(mecha_type_id)
            model = self.ev_g_model()
            mecha_model = entity.logic.ev_g_model()
            if model and mecha_model:
                if self.ev_g_is_cam_target():
                    self.play_mount_trk(mecha_entity_id)
                clip_name = clip_name if model.has_anim(clip_name) else 'mount_8002'
                model.remove_from_parent()
                model.position = math3d.vector(0, 0, 0)
                model.rotation_matrix = math3d.matrix()
                mecha_model.bind('mount', model, world.BIND_TYPE_ALL)
                if MODEL_SHADER_CTRL_SET_ENABLE:
                    model.set_inherit_parent_shaderctrl(False)
                self._anim_time = self.custom_param.get(clip_name, 1)
                self.elapsed_time = 0
                self.send_event('E_POST_ACTION', clip_name, LOW_BODY, 1, timeScale=1)
                if self._clear_timer:
                    global_data.game_mgr.unregister_logic_timer(self._clear_timer)

                def cb(*args):
                    if model and model.valid:
                        model.position = math3d.vector(0, 0, 0)
                        model.rotation_matrix = math3d.matrix()

                self._clear_timer = global_data.game_mgr.register_logic_timer(cb, interval=1, times=-1, mode=timer.LOGIC)
        if self._anim_time <= 0:
            print(('test--_action_enter_mecha--_anim_time =', self._anim_time))
            import traceback
            traceback.print_stack()

    def _cancel_enter_mecha(self, *args):
        if not self.is_active:
            return
        self._force_interrupt_enter = True
        self.ev_g_cancel_state(self.sid)
        self.send_event('E_SWITCH_TO_MECHA_STATE', self._enter_mecha_id)
        if not self.ev_g_death() and not self.ev_g_agony():
            self.send_event('E_ACTIVE_STATE', status_config.ST_STAND)
            if not self.ev_g_is_avatar():
                return
            global_data.emgr.switch_to_mecha_camera.emit(camera_state_const.THIRD_PERSON_MODEL)
            self.send_event('E_ROTATE_MODEL_TO_CAMERA_DIR', False)
            model = self.ev_g_model()
            if model:
                move_dir = model.rotation_matrix.forward
                self.sd.ref_cur_speed = 5 * NEOX_UNIT_SCALE
                self.send_event('E_MOVE', -move_dir)
                self.send_event('E_VERTICAL_SPEED', 10 * NEOX_UNIT_SCALE)
                self.send_event('E_FALL')
                self.send_event('E_RESET_GRAVITY')

    def play_mount_trk(self, mecha_entity_id):

        def end_callback():
            global_data.emgr.camera_cancel_added_trk_event.emit('Mount_State_Offset', None)
            global_data.emgr.camera_cancel_added_trk_event.emit('Mount_Step_back2', None)
            global_data.emgr.camera_additional_transformation_event.emit(math3d.matrix(), 0, False, False)
            mecha_entity = EntityManager.getentity(mecha_entity_id)
            if mecha_entity and mecha_entity.logic:
                mecha_id = mecha_entity.logic.share_data.ref_mecha_id
                mecha_fashion_id = mecha_entity.logic.ev_g_mecha_fashion_id()
                camera_type = get_mecha_camera_type(mecha_id, mecha_fashion_id)
                if not self.ev_g_in_mecha('Mecha'):
                    global_data.emgr.camera_additional_transformation_event.emit(math3d.matrix(), 0, False, True)
                    return
                self.send_event('E_MECHA_CAMERA', camera_type)
            return

        from logic.gutils.CameraHelper import get_camera_state_def_mat
        mecha_entity = EntityManager.getentity(mecha_entity_id)
        if mecha_entity and mecha_entity.logic:
            avatar_pos = self.ev_g_position()
            mecha_pos = mecha_entity.logic.ev_g_position()
            if not avatar_pos or not mecha_pos:
                return
            mecha_id = mecha_entity.logic.share_data.ref_mecha_id
            mecha_fashion_id = mecha_entity.logic.ev_g_mecha_fashion_id()
            mecha_camera_state = get_mecha_camera_type(mecha_id, mecha_fashion_id)
            from logic.client.const.camera_const import POSTURE_STAND, THIRD_PERSON_MODEL
            end_mat_org = get_camera_state_def_mat(mecha_camera_state, POSTURE_STAND, self.ev_g_role_id())
            start_mat_org = get_camera_state_def_mat(THIRD_PERSON_MODEL, POSTURE_STAND, self.ev_g_role_id())
            start_mat = math3d.matrix(start_mat_org)
            end_mat = math3d.matrix(end_mat_org)
            start_mat.inverse()
            end_mat *= start_mat
            custom_data = None
            mount_time = mecha_entity.logic.ev_g_mount_time() or 1.0
            slerp_start_time = mecha_entity.logic.ev_g_mount_slerp_start_time()
            pre_mount_trk_info = mecha_entity.logic.ev_g_pre_mount_trk_info() or {}
            pre_mount_trk_dist = math3d.vector(*pre_mount_trk_info.get('dis', [0, 0, 0]))
            pre_mount_trk_time = pre_mount_trk_info.get('trk_time', 0)
            sfx_item_no = mecha_utils.get_select_sfx(self, mecha_id, self.ev_g_select_sfx())
            callCameraOffset = confmgr.get('display_enter_effect', 'Content', str(sfx_item_no), 'callCameraOffset', default=None)
            if callCameraOffset:
                pre_mount_trk_dist = pre_mount_trk_dist + math3d.vector(*callCameraOffset)
                if not pre_mount_trk_time:
                    pre_mount_trk_time = 0.1
            pos_diff = mecha_pos - avatar_pos
            yaw = self.ev_g_yaw() or 0
            rot_mat = math3d.matrix.make_rotation_y(-yaw)
            pos_diff *= rot_mat
            end_mat.translation += pos_diff
            if pre_mount_trk_time:
                end_mat.translation -= pre_mount_trk_dist
            if end_mat and mount_time and slerp_start_time:
                duration = mount_time - slerp_start_time - 0.066 - pre_mount_trk_time
                add_trk_data = {'trk_start_time': slerp_start_time,'end_mat': end_mat,'duration': duration if duration > 0 else 0,
                   'trk_real_end_time': mount_time
                   }
                custom_data = {'end_add_trk': add_trk_data}

            def real_mount_trk_callback():
                if self and self.is_valid():
                    self.send_event('E_CANCEL_CAMERA_STATE_TRK', 'C_MECHA_MOUNT', mecha_id, False)
                    if self._anim_time > 0:
                        if self.elapsed_time < self._anim_time:
                            self.send_event('E_PLAY_CAMERA_STATE_TRK', 'C_MECHA_BOARD', end_callback, mecha_id, custom_data)
                        else:
                            end_callback()
                    else:
                        self.send_event('E_PLAY_CAMERA_STATE_TRK', 'C_MECHA_BOARD', end_callback, mecha_id, custom_data)

            self.adjust_to_mecha_camera(mecha_camera_state, mecha_entity.logic, start_mat_org, end_mat_org, mount_time)
            if pre_mount_trk_time:
                self.play_pre_mount_trk(pre_mount_trk_dist, pre_mount_trk_time, mount_time, real_mount_trk_callback)
            else:
                real_mount_trk_callback()
        return

    def adjust_to_mecha_camera(self, mecha_camera_state, mecha_entity_logic, start_mat, end_mat, total_duration):
        if not mecha_entity_logic:
            return
        else:
            scn = global_data.game_mgr.scene
            cam = scn.active_camera
            global_data.emgr.set_camera_yaw_pitch_with_slerp_event.emit(None, 0, False)
            global_data.emgr.switch_observe_camera_state_event.emit(mecha_camera_state, force_trans_time=0.0)
            end_mat.inverse()
            start_mat *= end_mat
            total_duration = round(total_duration * 1000.0 / 33.33333333) * 33.333333333 * 2
            track = track_build([(0, math3d.matrix()), (33.33, start_mat), (total_duration, start_mat)], total_duration)
            global_data.emgr.camera_play_added_trk_event.emit('Mount_State_Offset', None, {'trk_instance': track,'disable_unrecover_smooth': True,
               'not_additive': False,
               'trk_type': 190724
               }, True)
            return

    def play_pre_mount_trk(self, distance, duration, total_duration, callback):
        duration = round(duration * 1000.0 / 33.33333333) * 33.333333333
        total_duration = round(total_duration * 1000.0 / 33.33333333) * 33.333333333 * 2
        end_trans = math3d.matrix()
        end_trans.translation = distance

        def callback2--- This code section failed: ---

 360       0  LOAD_DEREF            0  'callback'
           3  CALL_FUNCTION_0       0 
           6  POP_TOP          

 362       7  LOAD_GLOBAL           0  'track_build'
          10  LOAD_CONST            1  ''
          13  LOAD_GLOBAL           1  'math3d'
          16  LOAD_ATTR             2  'matrix'
          19  CALL_FUNCTION_0       0 
          22  BUILD_TUPLE_2         2 
          25  LOAD_CONST            2  33.333
          28  LOAD_DEREF            1  'end_trans'
          31  BUILD_TUPLE_2         2 
          34  LOAD_DEREF            2  'total_duration'
          37  LOAD_DEREF            1  'end_trans'
          40  BUILD_TUPLE_2         2 
          43  BUILD_LIST_3          3 

 363      46  LOAD_DEREF            2  'total_duration'
          49  CALL_FUNCTION_2       2 
          52  STORE_FAST            0  'track2'

 365      55  LOAD_GLOBAL           3  'global_data'
          58  LOAD_ATTR             4  'emgr'
          61  LOAD_ATTR             5  'camera_play_added_trk_event'
          64  LOAD_ATTR             6  'emit'
          67  LOAD_CONST            3  'Mount_Step_back2'
          70  LOAD_CONST            0  ''

 366      73  BUILD_MAP_4           4 
          76  BUILD_MAP_4           4 
          79  STORE_MAP        
          80  LOAD_GLOBAL           8  'True'
          83  LOAD_CONST            5  'disable_unrecover_smooth'
          86  STORE_MAP        

 367      87  LOAD_GLOBAL           9  'False'
          90  LOAD_CONST            6  'not_additive'
          93  STORE_MAP        

 368      94  LOAD_CONST            7  190726
          97  LOAD_CONST            8  'trk_type'
         100  STORE_MAP        

 369     101  LOAD_GLOBAL           8  'True'
         104  CALL_FUNCTION_4       4 
         107  POP_TOP          
         108  LOAD_CONST            0  ''
         111  RETURN_VALUE     

Parse error at or near `STORE_MAP' instruction at offset 79

        track = track_build([(0, math3d.matrix()), (duration, end_trans)], duration)
        global_data.emgr.camera_play_added_trk_event.emit('Mount_Step_back', callback2, {'trk_instance': track,'disable_unrecover_smooth': True,'not_additive': False,
           'trk_type': 190725
           }, True)

    def _try_join_mecha(self):
        self._clear_join_mecha_action()
        if self._enter_mecha_id == 0:
            return
        from mobile.common.EntityManager import EntityManager
        mecha = EntityManager.getentity(self._enter_mecha_id)
        if mecha and mecha.logic and not mecha.logic.ev_g_death():
            psg_info = mecha.logic.ev_g_passenger_info()
            if not psg_info:
                return
            if not self._force_interrupt_enter:
                self.send_event('E_ON_JOIN_MECHA', self._enter_mecha_id)
        model = self.ev_g_model()
        if model:
            scene = global_data.game_mgr.scene
            model.remove_from_parent()
            if MODEL_SHADER_CTRL_SET_ENABLE:
                model.set_inherit_parent_shaderctrl(True)
            if scene:
                scene.add_object(model)


class MechaDriver(StateBase):
    BIND_EVENT = {'E_SEAT_ON_MECHA': 'seat_on_mecha',
       'E_VEHICLE_TURN': 'on_turn_vehicle',
       'E_ON_ACTION_ON_VEHICLE': 'on_enter_vehicle',
       'E_ENTER_STATE': 'enter_states',
       'E_LEAVE_STATE': 'leave_states',
       'E_ROTATE_TO_VEHICLE': 'rotate_to_vehicle',
       'E_ON_LEAVE_VEHICLE': ('_on_leave_vehicle', 99),
       'E_ON_ACTION_LEAVE_VEHICLE': '_on_leave_vehicle',
       'E_ON_LEAVE_MECHA': ('_on_leave_mecha', -10),
       'E_FORCE_MECHA_DRIVER': 'force_mecha_driver',
       'G_MECHA_DRIVER_IDLE_ANIM': 'get_idle_anim',
       'G_SEAT_INDEX': 'get_seat_index',
       'E_VEHICLE_STOP': 'on_vehicle_stop',
       'E_VEHICLE_BEGIN_MOVE': 'on_vehicle_begin_move'
       }

    def init_from_dict(self, unit_obj, bdict, sid, state_info):
        super(MechaDriver, self).init_from_dict(unit_obj, bdict, sid, state_info)
        self.inside_idle_anim = self.custom_param.get('inside_idle', DEFAULT_ANIM_NAME)
        anim_param = self.custom_param.get('single', {})
        self.idle_anim = anim_param.get('idle', DEFAULT_ANIM_NAME)
        self.turn_left_anim = anim_param.get('turn_left', DEFAULT_ANIM_NAME)
        self.turn_right_anim = anim_param.get('turn_right', DEFAULT_ANIM_NAME)
        self.show_inside = False
        self.seat_index = 0
        self.is_motorcycle = False
        self.motorcycle_anim_param = None
        return

    def init_anim_param(self, control_target, seat_index):
        self.seat_index = seat_index
        if not control_target or control_target.logic.__class__.__name__ != 'LMotorcycle':
            self.is_motorcycle = False
            skin_id = str(control_target.logic.ev_g_mecha_fashion_id())
            anim_param = self.custom_param.get(skin_id, self.custom_param['single'])
            self.idle_anim = anim_param.get('idle', DEFAULT_ANIM_NAME)
            self.turn_left_anim = anim_param.get('turn_left', DEFAULT_ANIM_NAME)
            self.turn_right_anim = anim_param.get('turn_right', DEFAULT_ANIM_NAME)
        else:
            self.is_motorcycle = True
            if 'motorcycle' in self.custom_param:
                anim_param = self.custom_param.get('motorcycle', {})
                self.motorcycle_anim_param = anim_param
            else:
                self.motorcycle_anim_param = self.custom_param

    def enter_states(self, new_state):
        if new_state == self.sid:
            self.sd.ref_logic_trans.yaw_target = 0
            self.sd.ref_rotatedata.deactivate_ecs()

    def leave_states(self, leave_state, new_state=None):
        is_auto_cancel = leave_state == self.sid and new_state != self.sid
        if leave_state == self.sid:
            self.sd.ref_rotatedata.activate_ecs()
        if is_auto_cancel:
            self.send_event('E_FORBID_ROTATION', False)
            self.send_event('E_ROTATE_MODEL_TO_CAMERA_DIR', force_use_camera_yaw=True)
            self.send_event('E_CAM_PITCH', global_data.cam_data.pitch)
            self.send_event('E_ACTION_SYNC_HEAD_PITCH', global_data.cam_data.pitch)
        if not self.is_active:
            return
        if is_auto_cancel:
            self.send_event('E_REMOVE_TRIGGER_STATE', self.sid)

    def _on_leave_vehicle(self, *arg):
        self.send_event('E_CTRL_STAND', ignore_col=True)

    def _on_leave_mecha(self):
        if self.ev_g_is_cam_target():
            ctrl_target = self.ev_g_control_target()
            if ctrl_target and ctrl_target.logic:
                ctrl_target.logic.send_event('E_CANCEL_CAMERA_STATE_TRK', 'C_MECHA_BOARD', self.ev_g_get_bind_mecha_type(), True)
            global_data.emgr.camera_cancel_added_trk_event.emit('Mount_State_Offset', None)
            global_data.emgr.camera_cancel_added_trk_event.emit('Mount_Step_back2', None)
            global_data.emgr.camera_additional_transformation_event.emit(math3d.matrix(), 0, False, False)
        return

    def get_seat_index(self):
        return self.seat_index

    def get_idle_anim(self):
        if self.is_motorcycle:
            return self.motorcycle_anim_param['idle']
        else:
            if self.show_inside:
                return self.inside_idle_anim
            return self.idle_anim

    def on_vehicle_begin_move(self):
        if not self.ev_g_get_state(self.sid):
            return
        if self.seat_index != 0:
            return
        move_anim_param = self.motorcycle_anim_param['move']
        anim_name, anim_part, dir_type, kwargs = move_anim_param
        part = LOW_BODY if anim_part == 'lower' else UP_BODY
        self.send_event('E_POST_ACTION', anim_name, part, dir_type, **kwargs)

    def on_vehicle_stop(self):
        if not self.ev_g_get_state(self.sid):
            return
        idle_anim = self.get_idle_anim()
        self.send_event('E_POST_ACTION', idle_anim, LOW_BODY, 1, loop=True)

    def rotate_to_vehicle(self, *args):
        if not self.ev_g_get_state(self.sid):
            return
        else:
            self.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', [bcast.E_ROTATE_TO_VEHICLE, ()], True)
            model = self.ev_g_model()
            mecha_model = None
            control_target = self.ev_g_control_target()
            if control_target and control_target.logic:
                mecha_model = control_target.logic.ev_g_model()
            if model and mecha_model:
                model.position = math3d.vector(0, 0, 0)
                if self.ev_g_is_avatar() or not self.ev_g_get_state(status_config.ST_VEHICLE_PASSENGER):
                    self.sd.ref_logic_trans.yaw_target = 0
                model.world_rotation_matrix = mecha_model.world_rotation_matrix
            return

    def force_mecha_driver(self, *args):
        if not self.ev_g_get_state(self.sid):
            return
        if not self.ev_g_is_avatar():
            self.rotate_to_vehicle()
        else:
            self.enter(set())

    def enter(self, leave_states):
        self.rotate_to_vehicle()
        self.send_event('E_ROCK_STOP')
        self.send_event('E_MOVE_STOP')
        self.send_event('E_SWITCH_STATUS', animation_const.STATE_DRIVE)
        self.send_event('S_ATTR_SET', 'human_state', animation_const.STATE_DRIVE)
        self.send_event('E_ROTATE_BODY_BY_X', 0)
        self.send_event('E_ROTATE_BODY_BY_Y', 0)
        super(MechaDriver, self).enter(leave_states)
        self.change_idle_anim()
        self.on_change_behavior()

    def change_idle_anim(self):
        idle_anim = self.get_idle_anim()
        self.send_event('E_POST_ACTION', idle_anim, LOW_BODY, 1, loop=True)

    def on_change_behavior(self):
        self.send_event('E_DISABLE_BEHAVIOR')
        control_target = self.ev_g_control_target()
        if control_target and control_target.logic.__class__.__name__ == 'LMechaTrans':
            pattern = control_target.logic.ev_g_pattern()
            camera_state = camera_state_const.MECHA_MODE_TWO if pattern == mecha_const.MECHA_PATTERN_NORMAL else camera_state_const.VEHICLE_MODE
            self.send_event('E_MECHA_CAMERA', camera_state)

    def exit(self, enter_states):
        super(MechaDriver, self).exit(enter_states)
        self.send_event('E_ROTATE_MODEL_TO_CAMERA_DIR')

    def seat_on_mecha(self, show, mecha_eid=None):
        self.show_inside = show
        if self.is_active:
            self.enter(set())
        else:
            self.active_self()
        if show:
            mecha = EntityManager.getentity(mecha_eid)
            if not mecha or not mecha.logic:
                return
            driver_model, mecha_model = self.ev_g_model(), mecha.logic.ev_g_model()
            if driver_model and mecha_model:
                driver_model.remove_from_parent()
                driver_model.position = math3d.vector(0, 0, 0)
                driver_model.rotation_matrix = math3d.matrix()
                if MODEL_SHADER_CTRL_SET_ENABLE:
                    driver_model.set_inherit_parent_shaderctrl(False)
                mecha_model.bind('seat', driver_model, world.BIND_TYPE_ALL)
            self.send_event('E_SHOW_MODEL')
        else:
            self.send_event('E_HIDE_MODEL')

    def on_turn_vehicle(self, diff_yaw):
        if not self.ev_g_get_state(self.sid):
            return
        if self.is_motorcycle:
            return
        convert_diff_yaw = diff_yaw
        if abs(diff_yaw) < 0.2:
            convert_diff_yaw = 0
        loop = False
        if convert_diff_yaw > 0:
            move_action = animation_const.MOVE_STATE_TURN_LEFT
            clip_name = self.turn_left_anim
        elif convert_diff_yaw < 0:
            move_action = animation_const.MOVE_STATE_TURN_RIGHT
            clip_name = self.turn_right_anim
        else:
            move_action = animation_const.MOVE_STATE_STAND
            clip_name = self.idle_anim
            loop = True
        old_move_action = self.ev_g_move_state()
        if old_move_action == move_action:
            return
        self.send_event('E_MOVE_STATE', move_action)
        self.send_event('E_POST_ACTION', clip_name, LOW_BODY, 1, loop=loop)

    def real_enter_vehicle(self, control_target):
        seat_index = control_target.logic.ev_g_passenger_seat_index(self.unit_obj.id)
        self.init_anim_param(control_target, seat_index)
        self.change_idle_anim()
        self.send_event('E_MOVE_STATE', animation_const.MOVE_STATE_STAND)
        self.on_change_seat()

    def on_enter_vehicle(self, control_target):
        if not control_target or not control_target.logic:
            return
        if control_target.logic.sd.ref_driver_id != self.unit_obj.id:
            return
        self.real_enter_vehicle(control_target)

    def on_change_seat(self, *args):
        self.send_event('E_CLEAR_UP_BODY_ANIM')
        weapon_pos = self.sd.ref_wp_bar_cur_pos
        if weapon_pos and weapon_pos > 0:
            self.send_event('E_SET_EMPTY_HAND', False)


class VehiclePassenger(MechaDriver):
    SEAT_INDEX = 2
    FRONT = 1
    BACK = 2
    BIND_EVENT = MechaDriver.BIND_EVENT.copy()
    BIND_EVENT.update({'E_EXIT_WEAPON_ACTION': 'exit_weapon_action',
       'E_CHANGE_SHOOT_STATE': 'on_change_shoot_state',
       'E_TURN_ON_SEAT': 'turn_on_seat',
       'G_PASSENGER_REF_MODEL': 'get_ref_model'
       })

    def init_from_dict(self, unit_obj, bdict, sid, state_info):
        super(VehiclePassenger, self).init_from_dict(unit_obj, bdict, sid, state_info)
        self.turn_dir = self.FRONT
        self.rotate_yaw = 0
        self.ref_model = None
        self.last_twist_yaw_angle = 0
        return

    def enter_states(self, new_state):
        if new_state == self.sid:
            self.sd.ref_rotatedata.activate_ecs()

    def destroy(self):
        super(VehiclePassenger, self).destroy()
        if self.ref_model and self.ref_model.valid:
            self.ref_model.destroy()
        self.ref_model = None
        return

    def seat_on_mecha(self, show, mecha_eid=None):
        pass

    def get_yaw_angle_range(self):
        left_max_yaw_angle, right_max_yaw_angle = (-1, 1)
        return (
         left_max_yaw_angle, right_max_yaw_angle)

    def cal_twist_angle(self, camera_yaw, vehicle_trans_yaw):
        if self.turn_dir == self.BACK:
            camera_yaw = camera_yaw + math.pi
        camera_yaw = math.fmod(camera_yaw, pi2)
        offset_rad = camera_yaw - vehicle_trans_yaw
        if offset_rad > math.pi:
            offset_rad -= 2 * math.pi
            camera_yaw -= 2 * math.pi
        elif offset_rad < -math.pi:
            offset_rad += 2 * math.pi
            camera_yaw += 2 * math.pi
        twist_angle = offset_rad * 180 / math.pi
        if global_data.debug_motorcycle:
            print(('test--cal_twist_angle--twist_angle =', twist_angle, '--turn_dir =', self.turn_dir, '--FRONT =', self.FRONT, '----camera_yaw =', camera_yaw, '--offset_rad =', offset_rad, '--ev_g_trans_yaw =', self.ev_g_trans_yaw(), '--unit_obj =', self.unit_obj))
        return twist_angle

    def turn_on_seat(self, camera_yaw, vehicle_trans_yaw, init_dt_yaw):
        if global_data.debug_motorcycle:
            print(('test--turn_on_seat--step1--camera_yaw =', camera_yaw, '--vehicle_trans_yaw =', vehicle_trans_yaw, '--init_dt_yaw =', init_dt_yaw, '--unit_obj =', self.unit_obj))
        model = self.ev_g_model()
        if not model:
            return
        control_target = self.ev_g_control_target()
        if not control_target or not control_target.logic:
            return
        vehicle_model = control_target.logic.ev_g_model()
        if not vehicle_model:
            return
        if init_dt_yaw == 0:
            return
        twist_yaw_angle = self.cal_twist_angle(camera_yaw, vehicle_trans_yaw)
        left_max_yaw_angle, right_max_yaw_angle = self.get_yaw_angle_range()
        max_angle = 180
        THRESHOLD_ANGLE = 2
        if global_data._test_motorcycle_anim:
            return
        model_rotation_matrix = model.world_rotation_matrix
        if not self.ref_model or not self.ref_model.valid:
            self.create_ref_model()
        init_human_forward_dir = self.ref_model.world_rotation_matrix.forward
        if self.turn_dir == self.BACK:
            init_human_forward_dir = -init_human_forward_dir
        cur_human_forward_dir = model_rotation_matrix.forward
        cur_twist_yaw = math.radians(self.ev_g_twist_yaw() or 0)
        dot_value = cur_human_forward_dir.dot(init_human_forward_dir)
        dot_value = max(dot_value, -1)
        dot_value = min(dot_value, 1)
        init_now_accum_diff_yaw = math.acos(dot_value)
        now_accum_diff_angle = math.degrees(abs(init_now_accum_diff_yaw) + abs(cur_twist_yaw))
        if global_data.debug_motorcycle:
            print(('test--turn_on_seat--step2--now_accum_diff_angle =', now_accum_diff_angle, '--twist_yaw_angle =', twist_yaw_angle, '--last_twist_yaw_angle =', self.last_twist_yaw_angle, '--init_dt_yaw =', init_dt_yaw, '--turn_dir =', self.turn_dir, '--FRONT =', self.FRONT, '--ref_model.forward =', init_human_forward_dir, '--left_max_yaw_angle =', left_max_yaw_angle, '--right_max_yaw_angle =', right_max_yaw_angle))
        if self.turn_dir == self.FRONT:
            if abs(now_accum_diff_angle) >= 120 and self.last_twist_yaw_angle * twist_yaw_angle < 0 or abs(twist_yaw_angle) >= max_angle:
                self.turn_dir = self.BACK
                self.send_event('E_TWIST_YAW', 0)
                human_forward_dir = -init_human_forward_dir
                self.send_event('E_FORWARD', human_forward_dir)
                self.rotate_yaw = 0
                model_rotation_matrix = model.world_rotation_matrix
                if global_data.debug_motorcycle:
                    print(('test--turn_on_seat--step3--TO_BACK--cur_twist_yaw =', cur_twist_yaw, '--model_rotation_matrix.yaw =', model_rotation_matrix.yaw, '--human_forward_dir =', human_forward_dir, '--init_human_forward_dir =', init_human_forward_dir))
                return
            if twist_yaw_angle < left_max_yaw_angle or twist_yaw_angle > right_max_yaw_angle:
                max_yaw_angle = left_max_yaw_angle
                if twist_yaw_angle > right_max_yaw_angle:
                    max_yaw_angle = right_max_yaw_angle
                max_diff_angle = max_angle - abs(max_yaw_angle)
                dst = 100
                src = 0
                cur_diff_angle = abs(twist_yaw_angle) - abs(max_yaw_angle)
                blend_scale = cur_diff_angle / max_diff_angle * (dst - src)
                self.send_event('E_CHANGE_ANIM_BLEND_SCALE', blend_scale)
                self.send_event('E_TWIST_YAW', max_yaw_angle)
                twist_root_angle = twist_yaw_angle - max_yaw_angle
                diff_yaw = math.radians(twist_root_angle)
                dt_yaw = diff_yaw - self.rotate_yaw
                self.rotate_yaw = diff_yaw
                if global_data.debug_motorcycle:
                    print(('test--turn_on_seat--step4--blend_scale =', blend_scale, '--dt_angle =', math.degrees(dt_yaw), '--dt_yaw =', dt_yaw, '***********************'))
                self.sd.ref_logic_trans.yaw_target = self.rotate_yaw
            else:
                self.rotate_yaw = 0
                self.send_event('E_TWIST_YAW', twist_yaw_angle)
            self.last_twist_yaw_angle = twist_yaw_angle
        else:
            adjust_twist_yaw_angle = twist_yaw_angle
            if abs(now_accum_diff_angle) >= 120 and self.last_twist_yaw_angle * adjust_twist_yaw_angle < 0 or abs(adjust_twist_yaw_angle) >= max_angle:
                self.turn_dir = self.FRONT
                cur_twist_yaw = math.radians(self.ev_g_twist_yaw() or 0)
                self.send_event('E_TWIST_YAW', 0)
                human_forward_dir = -init_human_forward_dir
                self.send_event('E_FORWARD', human_forward_dir)
                self.rotate_yaw = 0
                if global_data.debug_motorcycle:
                    print(('test--turn_on_seat--step6--TO_FRONT--cur_twist_yaw =', cur_twist_yaw, '--model_rotation_matrix.yaw =', model_rotation_matrix.yaw, '--human_forward_dir =', human_forward_dir, '--init_human_forward_dir =', init_human_forward_dir))
                return
            if adjust_twist_yaw_angle < left_max_yaw_angle or adjust_twist_yaw_angle > right_max_yaw_angle:
                max_yaw_angle = left_max_yaw_angle
                if adjust_twist_yaw_angle > right_max_yaw_angle:
                    max_yaw_angle = right_max_yaw_angle
                max_diff_angle = max_angle - abs(max_yaw_angle)
                dst = 0
                src = 100
                cur_diff_angle = abs(adjust_twist_yaw_angle) - abs(max_yaw_angle)
                blend_scale = src + cur_diff_angle / max_diff_angle * (dst - src)
                self.send_event('E_CHANGE_ANIM_BLEND_SCALE', blend_scale)
                self.send_event('E_TWIST_YAW', max_yaw_angle)
                twist_root_angle = adjust_twist_yaw_angle - max_yaw_angle
                diff_yaw = math.radians(twist_root_angle)
                last_rotate_yaw = self.rotate_yaw
                dt_yaw = diff_yaw - self.rotate_yaw
                self.rotate_yaw = diff_yaw
                if global_data.debug_motorcycle:
                    print(('test--turn_on_seat--step8--blend_scale =', blend_scale, '--math.degrees(diff_yaw) =', math.degrees(dt_yaw), '--dt_yaw =', dt_yaw, '--diff_yaw =', diff_yaw, '--last_rotate_yaw =', last_rotate_yaw, '***********************'))
                self.sd.ref_logic_trans.yaw_target = self.rotate_yaw + math.pi
            else:
                self.rotate_yaw = 0
                self.send_event('E_TWIST_YAW', adjust_twist_yaw_angle)
            self.last_twist_yaw_angle = adjust_twist_yaw_angle

    def _on_leave_vehicle(self, *arg):
        super(VehiclePassenger, self)._on_leave_vehicle()
        self.send_event('E_CLEAR_UP_BODY_ANIM')
        self.send_event('E_DISABLE_STATE', (status_config.ST_RIGHT_AIM, status_config.ST_AIM, status_config.ST_WEAPON_ACCUMULATE))

    def on_vehicle_stop(self):
        pass

    def on_change_behavior(self):
        self.send_event('E_ENABLE_BEHAVIOR')

    def get_ref_model(self):
        return self.ref_model

    def create_ref_model(self):
        control_target = self.ev_g_control_target()
        if not control_target or not control_target.logic:
            return
        vehicle_model = control_target.logic.ev_g_model()
        if not vehicle_model:
            return
        self.ref_model = world.model('character/12/2000/empty.gim', world.get_active_scene())
        self.ref_model.remove_from_parent()
        seat_name = 'renwu_03_1'
        vehicle_model.bind(seat_name, self.ref_model, world.BIND_TYPE_ALL)
        self.ref_model.position = math3d.vector(0, 1.5 * NEOX_UNIT_SCALE, 0)
        self.ref_model.world_rotation_matrix = vehicle_model.world_rotation_matrix
        self.ref_model.visible = False
        self.ref_model.active_collision = False
        self.ref_model.play_animation('duoren_03_idle_f')

    def on_enter_vehicle(self, control_target):
        if not control_target or not control_target.logic:
            return
        vehicle_model = control_target.logic.ev_g_model()
        if not vehicle_model:
            return
        seat_index = control_target.logic.ev_g_passenger_seat_index(self.unit_obj.id)
        if seat_index != self.SEAT_INDEX:
            return
        self.real_enter_vehicle(control_target)
        self.turn_dir = self.FRONT
        self.rotate_yaw = 0
        self.last_twist_yaw_angle = 0
        global_data._test_motorcycle_anim = 0
        if not self.ref_model or not self.ref_model.valid:
            self.create_ref_model()
        if self.ref_model and self.ref_model.valid:
            self.ref_model.visible = False

    def enter(self, leave_states):
        super(VehiclePassenger, self).enter(leave_states)
        self.send_event('E_CHANGE_ANIM_BLEND_SCALE', 0)
        self.send_event('E_DISABLE_YAW_WITH_CAMREA', True)
        self.send_event('E_ENABLE_ROTATE', True)
        control_target = self.ev_g_control_target()
        if control_target and control_target.logic:
            seat_logic = control_target.logic.sd.ref_avatar_seat_logic
            if seat_logic:
                seat_logic.send_event('E_ACTION_SET_YAW', global_data.cam_data.yaw)
                self.send_event('E_ACTION_SET_YAW', global_data.cam_data.yaw)
        self.sd.ref_rotatedata.activate_ecs()
        self.sd.ref_logic_trans.yaw_target = self.rotate_yaw if self.turn_dir == self.FRONT else self.rotate_yaw + math.pi

    def exit(self, enter_states):
        super(VehiclePassenger, self).exit(enter_states)
        self.send_event('E_DISABLE_YAW_WITH_CAMREA', False)
        self.send_event('E_TRANS_YAW', self.ev_g_yaw() or 0)
        self.send_event('E_TWIST_YAW', 0)

    def update(self, dt):
        last_time = self.elapsed_time
        super(VehiclePassenger, self).update(dt)
        pass_time = self.elapsed_time - last_time
        keep_shoot_time = self.ev_g_keep_shoot_time()
        if keep_shoot_time > 0:
            keep_shoot_time -= pass_time
            self.send_event('E_KEEP_SHOOT_TIME', keep_shoot_time)
            if keep_shoot_time <= 0:
                self.send_event('E_ACTION_IS_SHOOT', 0)

    def change_idle_anim(self):
        clip_name, part, blend_dir, kwargs = self.motorcycle_anim_param['idle']
        self.send_event('E_POST_ACTION', clip_name, (LOW_BODY if part == 'lower' else UP_BODY), blend_dir, **kwargs)

    def on_change_seat(self, *args):
        clip_name, _, _ = character_action_utils.get_idle_clip(self, self.sid)
        self.send_event('E_POST_ACTION', clip_name, UP_BODY, 1, loop=True)
        weapon_pos = self.sd.ref_wp_bar_cur_pos
        if weapon_pos <= 0:
            self.send_event('E_SWITCH_LAST_GUN', switch_status=False)

    def on_change_shoot_state(self, *args):
        if self.ev_g_get_state(self.sid):
            self.exit_weapon_action()

    def exit_weapon_action(self, *args):
        if self.ev_g_get_state(self.sid):
            clip_name, _, _ = character_action_utils.get_idle_clip(self, status_config.ST_VEHICLE_PASSENGER)
            self.send_event('E_POST_ACTION', clip_name, UP_BODY, 1, loop=True)
            self.send_event('E_UPBODY_BONE', DEFAULT_UP_BODY_BONE)
        else:
            self.send_event('E_CLEAR_UP_BODY_ANIM')
            if not self.ev_g_is_in_any_state(character_action_utils.CROUCH_STATE):
                self.send_event('E_CLEAR_UP_BODY_ANIM', part=LOWER_UP_BODY)


class VehicleGunner(MechaDriver):
    SEAT_INDEX = 1

    def seat_on_mecha(self, show, mecha_eid=None):
        pass

    def on_enter_vehicle(self, control_target):
        if not control_target or not control_target.logic:
            return
        seat_index = control_target.logic.ev_g_passenger_seat_index(self.unit_obj.id)
        if seat_index != self.SEAT_INDEX:
            return
        self.real_enter_vehicle(control_target)

    def enter(self, leave_states):
        super(VehicleGunner, self).enter(leave_states)
        self.send_event('E_CLEAR_UP_BODY_ANIM')

    def on_change_seat(self, *args):
        if not self.ev_g_get_state(self.sid):
            return
        weapon_pos = self.sd.ref_wp_bar_cur_pos
        if weapon_pos > 0:
            self.send_event('E_SET_EMPTY_HAND', switch_status=False)
        self.send_event('E_CLEAR_UP_BODY_ANIM')


class ControllingSpecialWeapon(StateBase):

    def enter(self, leave_states):
        super(ControllingSpecialWeapon, self).enter(leave_states)
        self.send_event('E_POST_ACTION', 'duoren_02_idle', LOW_BODY, 1, loop=True)