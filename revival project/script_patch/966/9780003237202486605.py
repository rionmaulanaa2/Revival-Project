# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/com_bunker/ComBunkerSideways.py
from __future__ import absolute_import
import time
from math import pi
import math3d
import world
import logic.gcommon.common_const.animation_const as animation_const
from logic.client.const.camera_const import POSTURE_RIGHT_SIDEWAYS, POSTURE_LEFT_SIDEWAYS, POSTURE_UP_SIDEWAYS
from logic.gcommon.cdata import status_config as st_const
from logic.gcommon.common_const.collision_const import GROUP_CAMERA_INCLUDE
from logic.gcommon.const import NEOX_UNIT_SCALE
from logic.gcommon.common_utils.local_text import get_text_by_id
SW_RIGHT = POSTURE_RIGHT_SIDEWAYS
SW_LEFT = POSTURE_LEFT_SIDEWAYS
SW_UP = POSTURE_UP_SIDEWAYS
HOZ_VECTOR = math3d.vector(1, 0, 1)
FORWARD_DIR = math3d.vector(0, 0, 1)
from logic.gcommon.component.client.ComObjCollision import ComObjCollision
from .BunkerCheckHelper import FrameChecker, DirectionChecker

class ComBunkerSideways(ComObjCollision):
    BIND_EVENT = {'E_DEATH': 'on_death',
       'E_MODEL_LOADED': 'on_model_load_complete',
       'G_CHECK_BUNKER_FRONT': 'check_is_bunker_front_helper',
       'S_LEAVE_BUNKER': '_set_leave_bunker',
       'E_DELTA_YAW': '_on_yaw',
       'E_ACTION_MOVE': '_on_action_move',
       'E_ACTION_MOVE_STOP': '_action_move_stop',
       'E_STAND': 'on_posture_stand',
       'E_SQUAT': 'on_posture_squat'
       }

    def __init__(self):
        super(ComBunkerSideways, self).__init__()
        self.is_in_bunker_area = False
        self.is_in_sideways_status = False
        self.enter_bunker_area_time = 0
        self._cur_sideways_timer_id = None
        self._bunker_front_checker = FrameChecker()
        self._bunker_front_width_checker_res = []
        self._direction_checker = None
        self._direction_checker = DirectionChecker()
        self._free_dir_checker = FrameChecker()
        self._free_dir_check_res = []
        self._move_preference = SW_RIGHT
        self._is_move_stop = True
        self._move_stop_timer = None
        self._sideways_move_check_timer = None
        self.init_parameters()
        self._is_need_recheck = True
        self._coll_check_height = self.stand_check_height
        return

    def init_parameters(self):
        from common.cfg import confmgr
        conf = confmgr.get('sideways_conf')
        self.bunker_trigger_dist = conf.get('BUNKER_TRIGGER_DIST', 1.0) * NEOX_UNIT_SCALE
        self.empty_dir_checker_camera_dist = conf.get('EMPTY_DIR_CHECKER_CAMERA_DIST', 1.0) * NEOX_UNIT_SCALE
        self.empty_dir_checker_camera_ray_len = conf.get('EMPTY_DIR_CHECKER_CAMERA_RAY_LEN', 1.0) * NEOX_UNIT_SCALE
        self.sideways_trigger_time = 0.5
        self.stand_check_height = conf.get('STAND_CHECK_HEIGHT', 1.6) * NEOX_UNIT_SCALE
        self.squat_check_height = conf.get('SQUAT_CHECK_HEIGHT', 1) * NEOX_UNIT_SCALE
        self.BUNKER_MIN_WIDTH = conf.get('BUNKER_MIN_WIDTH', 0.6) * NEOX_UNIT_SCALE
        self.width_check_ray_length = conf.get('WIDTH_CHECKER_RAY_LENGTH', 2) * NEOX_UNIT_SCALE
        self.bunker_up_check_angle = conf.get('BUNKER_UP_SIDEWAYS_ANGLE', 0.25)
        import math
        self.valid_normal_pitch_tilted_arc = math.radians(10)

    def init_from_dict(self, unit_obj, bdict):
        super(ComBunkerSideways, self).init_from_dict(unit_obj, bdict)
        from logic.client.const.camera_const import POSTURE_STAND
        cur_posture = self.ev_g_posture()
        if cur_posture == POSTURE_STAND:
            self._coll_check_height = self.stand_check_height
        else:
            self._coll_check_height = self.squat_check_height

    def on_init_complete(self):
        self.need_update = True

    def destroy(self):
        if self._col_obj:
            model = self._model()
            if model and model.valid:
                model.unbind_col_obj(self._col_obj)
        super(ComBunkerSideways, self).destroy()
        if self._move_stop_timer:
            global_data.game_mgr.unregister_logic_timer(self._move_stop_timer)
            self._move_stop_timer = None
        if self._sideways_move_check_timer:
            global_data.game_mgr.unregister_logic_timer(self._sideways_move_check_timer)
            self._sideways_move_check_timer = None
        self._direction_checker = None
        if self._free_dir_checker:
            self._free_dir_checker.destroy()
            self._free_dir_checker = None
        if self._bunker_front_checker:
            self._bunker_front_checker.destroy()
            self._bunker_front_checker = None
        self.need_update = False
        return

    def tick(self, delta):
        if not global_data.is_allow_sideways:
            return
        if not self._bunker_front_checker.is_empty():
            self._bunker_front_checker.update()
        elif not self._free_dir_checker.is_empty():
            self._free_dir_checker.update()
        elif self._is_move_stop and self._is_need_recheck:
            if self.ev_g_is_in_bunker_shot_move() or self.ev_g_sideways_action():
                return
            self.check_is_bunker_at_front()
            self.set_need_recheck(False)
        else:
            self.set_need_recheck(False)
            self.need_update = False
            return

    def update_cur_check_height(self):
        model = self.ev_g_model()
        if not (model and model.valid):
            return
        start_matrix = model.get_bone_matrix(animation_const.BONE_HEAD_NAME, world.SPACE_TYPE_WORLD)
        height = start_matrix.translation.y - model.world_position.y
        self._coll_check_height = height

    def check_is_bunker_at_front(self):
        if not self.check_can_enter_sideways_actions():
            if self.is_in_bunker_area or self.is_in_sideways_status:
                self.on_leave_bunker_area()
            return
        if not self._bunker_front_checker.is_empty():
            self._bunker_front_checker.update()
            return
        model = self.unit_obj.ev_g_model()
        if not (model and model.valid):
            return
        part_cam = self.scene.get_com('PartCamera')
        if not part_cam:
            return
        if part_cam.is_in_cam_slerp():
            return
        result, start_position = self.check_is_bunker_front_helper()
        self.check_is_at_bunker_result(start_position, result)

    def check_is_bunker_front_helper(self):
        import collision
        if not self._col_obj:
            return ((False, None, None, None, None, None, None), None)
        else:
            scene = self.scene
            cam = scene.active_camera
            rotate_mat = math3d.matrix.make_rotation_y(cam.world_transformation.yaw)
            for_dir = FORWARD_DIR * rotate_mat
            self._col_obj.rotation_matrix = rotate_mat
            start_position = self.get_bunker_check_start_pos()
            end_position = for_dir * self.bunker_trigger_dist + start_position
            result = scene.scene_col.sweep_test(self._col_obj, start_position, end_position, GROUP_CAMERA_INCLUDE, GROUP_CAMERA_INCLUDE, 0, collision.INCLUDE_FILTER)
            return (
             result, start_position)

    def check_valid_normal_pitch_range(self, coll_normal):
        pitch = coll_normal.pitch
        if -self.valid_normal_pitch_tilted_arc < pitch < self.valid_normal_pitch_tilted_arc:
            return True
        else:
            return False

    def check_is_at_bunker_result(self, check_start_pos, result):
        if result[0]:
            coll_point = result[1]
            coll_normal = result[2]
            if not self.check_valid_normal_pitch_range(coll_normal):
                self.on_leave_bunker_area()
                return

            def cb(width_pass):
                if width_pass:
                    self._bunker_front_checker.clear()
                    self.on_enter_bunker_area()
                else:
                    self.on_leave_bunker_area()

            check_list = self._check_bunker_width_helper(check_start_pos, pi + coll_normal.yaw, lambda res: cb(res))
            for func in check_list:
                self._bunker_front_checker.add(func)

        else:
            self.on_leave_bunker_area()

    def check_bunker_empty_direction(self, check_callback):
        self.show_tips(get_text_by_id(2204))
        cam = self.scene.active_camera
        self._free_dir_checker.clear()
        self._free_dir_check_res = []
        start_pos = self.get_bunker_check_start_pos()
        camera_start_length = self.empty_dir_checker_camera_dist
        hor_forward = cam.world_rotation_matrix.forward * HOZ_VECTOR
        if hor_forward.is_zero:
            return
        hor_forward.normalize()
        start_pos -= hor_forward * camera_start_length

        def check_func(dir, yaw, pitch):
            max_angle = max(abs(yaw), abs(pitch))
            real_check_length = self.empty_dir_checker_camera_ray_len / math.cos(max_angle)
            coll_res = self._direction_checker.check_cam_dir_ex(start_pos, real_check_length, yaw, pitch, is_world_rotate=False, show_debug_line=True)
            if not coll_res[0]:
                self._free_dir_check_res.append(dir)

        import math
        angle = math.atan2(self.BUNKER_MIN_WIDTH, camera_start_length)
        self._free_dir_checker.add(lambda : check_func(SW_RIGHT, angle, 0))
        self._free_dir_checker.add(lambda : check_func(SW_LEFT, -angle, 0))
        if self._squat_check():
            self._free_dir_checker.add(lambda : check_func(SW_UP, 0, self.bunker_up_check_angle))
        self._free_dir_checker.add(check_callback)

    def get_bunker_empty_check_dir_angle(self, check_dir):
        if check_dir != SW_UP:
            dist_length = self.bunker_trigger_dist
            import math
            angle = math.atan2(self.BUNKER_MIN_WIDTH, dist_length)
            return (
             angle, 0)
        else:
            return (
             0, self.bunker_up_check_angle)

    def check_empty_bunker_direction_result(self):
        dir_to_event = {SW_RIGHT: 'E_TRY_RIGHT_SIDEWAYS',
           SW_LEFT: 'E_TRY_LEFT_SIDEWAYS',
           SW_UP: 'E_TRY_UP_SIDEWAYS'
           }
        action_to_camera_event = {SW_RIGHT: 'E_TO_RIGHT_SIDEWAYS_CAMERA',
           SW_LEFT: 'E_TO_LEFT_SIDEWAYS_CAMERA',
           SW_UP: 'E_TO_UP_SIDEWAYS_CAMERA'
           }
        if self._free_dir_check_res:
            cur_dir = SW_RIGHT
            if self._move_preference in self._free_dir_check_res:
                cur_dir = self._move_preference
                event_name = dir_to_event.get(self._move_preference, 'E_TRY_RIGHT_SIDEWAYS')
            else:
                farest_dir = self._free_dir_check_res[0]
                cur_dir = self._move_preference = farest_dir
                event_name = dir_to_event.get(farest_dir, 'E_TRY_RIGHT_SIDEWAYS')
            self.unit_obj.send_event(event_name)
            camera_event_name = action_to_camera_event.get(cur_dir)
            self.unit_obj.send_event(camera_event_name)
            self.send_event('E_SHOW_SIDEWAYS_DIR', self._free_dir_check_res)
        else:
            self.unit_obj.send_event('E_TRY_RIGHT_SIDEWAYS')
            self.send_event('E_LEAVE_SIDEWAYS_CAMERA')

    def _check_bunker_width_helper(self, start_position, yaw, callback):
        check_func_list = []
        self._bunker_front_width_checker_res = []

        def check_helper--- This code section failed: ---

 346       0  LOAD_GLOBAL           0  'math3d'
           3  LOAD_ATTR             1  'vector'
           6  LOAD_ATTR             1  'vector'
           9  LOAD_CONST            1  ''
          12  CALL_FUNCTION_3       3 
          15  LOAD_GLOBAL           0  'math3d'
          18  LOAD_ATTR             2  'matrix'
          21  LOAD_ATTR             3  'make_rotation_y'
          24  LOAD_FAST             1  'yaw'
          27  CALL_FUNCTION_1       1 
          30  BINARY_MULTIPLY  
          31  STORE_FAST            3  'world_offset'

 347      34  LOAD_FAST             2  'start_pos'
          37  LOAD_FAST             3  'world_offset'
          40  INPLACE_ADD      
          41  STORE_FAST            2  'start_pos'

 348      44  LOAD_DEREF            0  'self'
          47  LOAD_ATTR             4  '_direction_checker'
          50  LOAD_ATTR             5  'check_cam_dir_ex'
          53  LOAD_FAST             2  'start_pos'
          56  LOAD_DEREF            0  'self'
          59  LOAD_ATTR             6  'width_check_ray_length'
          62  LOAD_FAST             1  'yaw'
          65  LOAD_CONST            1  ''
          68  LOAD_CONST            2  'show_debug_line'
          71  LOAD_GLOBAL           7  'True'
          74  CALL_FUNCTION_260   260 
          77  STORE_FAST            4  'coll_res'

 349      80  LOAD_FAST             4  'coll_res'
          83  LOAD_CONST            1  ''
          86  BINARY_SUBSCR    
          87  POP_JUMP_IF_FALSE   109  'to 109'

 350      90  LOAD_DEREF            0  'self'
          93  LOAD_ATTR             8  '_bunker_front_width_checker_res'
          96  LOAD_ATTR             9  'append'
          99  LOAD_FAST             0  'x_offset'
         102  CALL_FUNCTION_1       1 
         105  POP_TOP          
         106  JUMP_FORWARD          0  'to 109'
       109_0  COME_FROM                '106'

Parse error at or near `CALL_FUNCTION_3' instruction at offset 12

        def width_helper():
            if not self._bunker_front_width_checker_res:
                callback(False)
                return
            max_w = max(self._bunker_front_width_checker_res)
            min_w = min(self._bunker_front_width_checker_res)
            if callback:
                if max_w - min_w >= self.BUNKER_MIN_WIDTH:
                    callback(True)
                else:
                    callback(False)

        check_func_list.append(lambda : check_helper(self.BUNKER_MIN_WIDTH))
        check_func_list.append(lambda : check_helper(self.BUNKER_MIN_WIDTH / 2.0))
        check_func_list.append(lambda : check_helper(0))
        check_func_list.append(lambda : check_helper(-self.BUNKER_MIN_WIDTH / 2.0))
        check_func_list.append(lambda : check_helper(-self.BUNKER_MIN_WIDTH))
        check_func_list.append(lambda : width_helper())
        return check_func_list

    def on_enter_bunker_area(self):
        cur_time = time.time()
        if not self.is_in_bunker_area:
            self.show_tips(get_text_by_id(2205))
        if not self.is_in_bunker_area:
            self.enter_bunker_area_time = cur_time
        elif not self.is_in_sideways_status:
            self.enter_sideways_action()
        else:
            self.check_sideways_camera()
        self.is_in_bunker_area = True

    def on_leave_bunker_area(self):
        if self.is_in_bunker_area:
            self.show_tips(get_text_by_id(2206))
        self._bunker_front_checker.clear()
        self._bunker_front_checker_res = False
        self.is_in_bunker_area = False
        if self.is_in_sideways_status:
            self.leave_sideways_action()

    def enter_sideways_action(self):
        self.show_tips(get_text_by_id(2207))
        model = self.unit_obj.ev_g_model()
        if not (model and model.valid):
            return
        self.is_in_sideways_status = True
        self.check_bunker_empty_direction(self.check_empty_bunker_direction_result)

    def leave_sideways_action(self):
        if self.is_in_sideways_status:
            self.unit_obj.send_event('E_LEAVE_SIDEWAYS')
        self.is_in_sideways_status = False
        self._free_dir_checker.clear()
        self._free_dir_check_res = []
        self.send_event('E_SHOW_SIDEWAYS_DIR', None)
        return

    def check_sideways_camera(self):
        if not self.is_in_sideways_status:
            return
        else:
            if self._move_preference is not None:
                self.check_preference_dir(self._move_preference)
            return

    def on_death(self, *arg):
        self.need_update = False

    def _on_action_move(self, move_dir):
        if not move_dir:
            return
        else:
            if abs(move_dir.z) > abs(move_dir.x):
                self._move_preference = SW_UP
            elif move_dir.x >= 0.1:
                self._move_preference = SW_RIGHT
            else:
                self._move_preference = SW_LEFT
            self._is_move_stop = False
            if self._move_stop_timer:
                global_data.game_mgr.unregister_logic_timer(self._move_stop_timer)
                self._move_stop_timer = None

            def action_move_check_callback():
                self._sideways_move_check_timer = None
                if self.is_in_bunker_area:
                    self.recheck_dir_when_sideways(move_dir)
                return

            from common.utils.timer import CLOCK
            if not self._sideways_move_check_timer and self.is_in_bunker_area:
                self._sideways_move_check_timer = global_data.game_mgr.register_logic_timer(action_move_check_callback, interval=0.3, times=1, mode=CLOCK)
            return

    def recheck_dir_when_sideways(self, move_dir):
        if move_dir.z < 0 and self.is_in_bunker_area and not self.ev_g_sideways_action():
            result, start_position = self.check_is_bunker_front_helper()
            if not result[0]:
                self.on_leave_bunker_area()
            return
        self.check_preference_dir(self._move_preference)

    def check_preference_dir(self, preference):
        if self.is_in_sideways_status and self._free_dir_checker.is_empty():
            if self.ev_g_in_bunker_camera() and preference == self.ev_g_last_bunker_camera_offset_dir():
                return
            self.enter_sideways_action()

    def _squat_check(self):
        if self.ev_g_is_in_any_state((st_const.ST_CROUCH,)):
            return True
        else:
            return False

    def get_collision_info(self):
        import math3d
        import collision
        self._mask = 0
        self._group = 0
        width, height = self.BUNKER_MIN_WIDTH, 1
        bounding_box = math3d.vector(1, width, 1)
        mask = self._mask
        group = self._group
        mass = 0
        return {'collision_type': collision.BOX,'bounding_box': bounding_box,'mask': mask,'group': group,'mass': mass}

    def _create_col_obj(self):
        super(ComBunkerSideways, self)._create_col_obj()
        if self._col_obj:
            model = self._model()
            if model:
                model.bind_col_obj(self._col_obj, animation_const.BONE_HEAD_NAME)

    def on_camera_state_check(self):
        from data.camera_state_const import THIRD_PERSON_MODEL
        return self.get_cur_camera_state() == THIRD_PERSON_MODEL

    def on_player_state_check(self):
        from logic.gcommon import const
        if self.ev_g_is_in_any_state((st_const.ST_CROUCH, st_const.ST_STAND)) and self.ev_g_status_check_pass(st_const.ST_SHOOT) and self.ev_g_status_check_pass(st_const.ST_MOVE) and self.sd.ref_wp_bar_cur_pos in const.MAIN_WEAPON_LIST:
            return True
        return False

    def check_can_enter_sideways_actions(self):
        return self.on_camera_state_check() and self.on_player_state_check()

    def get_cur_camera_state(self):
        part_cam = self.scene.get_com('PartCamera')
        return part_cam.get_cur_camera_state_type()

    def get_bunker_check_start_pos(self):
        if self.ev_g_sideways_action():
            model_sideways_offset = self.ev_g_player_sideways_offset()
        else:
            model_sideways_offset = None
        pos = self.ev_g_model_position()
        pos = math3d.vector(pos)
        if model_sideways_offset is not None:
            pos = pos - model_sideways_offset
        pos.y += self._coll_check_height
        return pos

    def _action_move_stop(self, *args):
        from common.utils.timer import CLOCK

        def set_move_stop():
            self._is_move_stop = True
            self.set_need_recheck(True)
            self.reset_checker()

        if self._sideways_move_check_timer:
            global_data.game_mgr.unregister_logic_timer(self._sideways_move_check_timer)
            self._sideways_move_check_timer = None
        if self._move_stop_timer:
            global_data.game_mgr.unregister_logic_timer(self._move_stop_timer)
            self._move_stop_timer = None
        self._move_stop_timer = global_data.game_mgr.register_logic_timer(set_move_stop, interval=0.3, times=1, mode=CLOCK)
        return

    def on_posture_stand(self):
        self.set_need_recheck(True)
        self._coll_check_height = self.stand_check_height
        self.reset_checker()

    def on_posture_squat(self):
        self.set_need_recheck(True)
        self._coll_check_height = self.squat_check_height
        self.reset_checker()

    def _set_leave_bunker(self):
        self.on_leave_bunker_area()

    def set_need_recheck(self, is_need):
        self._is_need_recheck = is_need
        if is_need:
            if self.ev_g_status_check_pass(st_const.ST_SHOOT):
                self.need_update = True

    def _on_yaw(self, *args):
        self.set_need_recheck(True)
        self.reset_checker()

    def reset_checker(self):
        self._free_dir_checker.clear()
        self._bunker_front_checker.clear()

    def show_tips(self, str):
        if hasattr(global_data, 'show_sideways_check_line') and global_data.show_sideways_check_line:
            global_data.game_mgr.show_tip(str)