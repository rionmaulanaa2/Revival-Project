# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/behavior/MeleeLogic.py
from __future__ import absolute_import
from __future__ import print_function
from six.moves import range
import math
import math3d
from .StateBase import StateBase, clamp
from logic.gcommon.cdata.mecha_status_config import *
from logic.gcommon.common_const.character_anim_const import *
from logic.gcommon.const import NEOX_UNIT_SCALE
from logic.gcommon.common_utils import status_utils
import logic.gcommon.common_const.robot_animation_const as robot_animation_const
from logic.gcommon.common_const import collision_const
from logic.gcommon.common_const.collision_const import GROUP_CHARACTER_INCLUDE
CUT_TIME_SCALE = 1.3
START_CUT_ATTACK_EVENT = 'MC_CUT_ATTACK_hit_start'
END_CUT_ATTACK_EVENT = 'MC_CUT_BACK1_hit_end'
END_CUT_BACK1_EVENT = 'MC_CUT_BACK2_combo'

def rotate_target(self, is_rotate_camera=True):
    self_position = self.ev_g_position()
    if not self_position:
        return
    else:
        target_position = self.ev_g_attack_target_position()
        if not target_position:
            return
        walk_direction = target_position - self_position
        if walk_direction.is_zero:
            return
        walk_direction.y = 0
        self.send_event('E_FORWARD', walk_direction)
        if self.ev_g_is_avatar() and is_rotate_camera:
            if hasattr(global_data, 'melee_lock_camera') and global_data.melee_lock_camera:
                model = self.ev_g_model()
                if model:
                    global_data.emgr.set_camera_yaw_pitch_with_slerp_event.emit(model.rotation_matrix.forward.yaw, None, True, 0.3)
                    global_data.emgr.enable_camera_yaw.emit(False)
        return


def is_block_collision(self):
    track_start_position = self.ev_g_position()
    track_target_position = self.ev_g_attack_target_position()
    if not track_target_position or not track_start_position:
        return
    move_dir = track_target_position - track_start_position
    if not move_dir.is_zero:
        move_dir.normalize()
    height = self.ev_g_height()
    chect_begin = track_start_position
    chect_begin.y = chect_begin.y + height / 2.0
    length = 3 * NEOX_UNIT_SCALE
    length = max(length, 0)
    check_end = chect_begin + move_dir * length
    check_dist = check_end - chect_begin
    group = collision_const.TERRAIN_GROUP | collision_const.WOOD_GROUP | collision_const.STONE_GROUP
    mask = group
    is_hit = self.ev_g_hit_by_scene_collision(chect_begin, check_end)
    return is_hit


class CutTrack(StateBase):
    NOT_MOVE_DIST_SQR = (0.1 * NEOX_UNIT_SCALE) ** 2
    AUTO_STOP_WHEN_NOT_MOVE_TIMES = 5

    def init_from_dict(self, unit_obj, bdict, sid, state_info):
        super(CutTrack, self).init_from_dict(unit_obj, bdict, sid, state_info)
        self._track_speed = self.custom_param.get('track_speed', 35) * NEOX_UNIT_SCALE
        self._max_track_time = self.custom_param.get('max_track_time', 2)
        max_track_angle_speed = self.custom_param.get('max_track_angle_speed', 15)
        self._max_track_radian_speed = math.radians(max_track_angle_speed)
        self._last_rush_position = None
        self._not_same_pos_times = 0
        self._rush_cut_leave_time = self._max_track_time
        self._cut_rush_speed = 0
        self._last_rush_cut_move_dir = None
        return

    def action_btn_down(self):
        super(CutTrack, self).action_btn_down()
        return True

    def enter(self, leave_states):
        super(CutTrack, self).enter(leave_states)
        self_position = self.ev_g_foot_position()
        if not self_position:
            return
        target_position = self.ev_g_attack_target_position()
        if not target_position:
            return
        walk_direction = target_position - self_position
        walk_direction.y = 0
        if walk_direction.is_zero:
            return
        self.send_event('E_UPBODY_BONE', FULL_BODY_BONE)
        self.send_event('E_GRAVITY', 0)
        walk_direction.normalize()
        speed = self._track_speed
        walk_direction = walk_direction * speed
        self._rush_cut_leave_time = self._max_track_time
        move_dir = walk_direction
        self._last_rush_position = self_position
        self._not_same_pos_times = 0
        diff_position = target_position - self_position
        if diff_position.y > NEOX_UNIT_SCALE:
            upper_self_position = math3d.vector(self_position)
            upper_self_position.y += NEOX_UNIT_SCALE
            self.send_event('E_FOOT_POSITION', upper_self_position)
        if move_dir.y == 0:
            if not self.ev_g_is_jump():
                self.send_event('E_VERTICAL_SPEED', move_dir.y)
        else:
            self.send_event('E_VERTICAL_SPEED', move_dir.y)
        move_dir.y = 0
        self._cut_rush_speed = move_dir.length
        self.send_event('E_SET_WALK_DIRECTION', move_dir)
        move_dir.normalize()
        self._last_rush_cut_move_dir = move_dir

    def exit(self, enter_states):
        super(CutTrack, self).exit(enter_states)
        self.send_event('E_UPBODY_BONE', DEFAULT_UP_BODY_BONE)
        self.send_event('E_CLEAR_UP_BODY_ANIM')
        self.send_event('E_RESET_GRAVITY')
        global_data.emgr.enable_camera_yaw.emit(True)
        self.cur_stage = 0
        self._next_stage = 0
        model = self.ev_g_model()
        if model:
            sfx = model.get_anim_trigger_socket_obj(robot_animation_const.MELEE_CUT_RUSH_CLIP, 'fx_chongci', 4)
            if sfx:
                sfx.shutdown()

    def calcute_new_cut_rush_dir(self):
        base = self._last_rush_cut_move_dir
        track_start_position = self.ev_g_position()
        track_target_position = self.ev_g_attack_target_position()
        if not track_start_position or not track_target_position:
            return math3d.vector(0, 0, 0)
        another = track_target_position - track_start_position
        another.y = 0
        another.normalize()
        max_radians = self._max_track_radian_speed
        max_degrees = math.degrees(max_radians)
        dot_value = base.dot(another)
        dot_value = max(dot_value, 0)
        dot_value = min(dot_value, 1)
        actual_radians = math.acos(dot_value)
        if abs(actual_radians) <= max_radians:
            return another
        actual_degrees = math.degrees(actual_radians)
        if actual_degrees < 0:
            max_degrees *= -1
        product_dir = base.cross(another)
        max_radian = math.radians(max_degrees)
        product_dir.normalize()
        rot = math3d.matrix.make_rotation(product_dir, max_radian)
        final_dir = rot.mulvec3x3(base)
        final_dir.normalize()
        return final_dir

    def cut_rush_meet_target(self):
        self.disable_self()
        print('test--cut_rush_meet_target--step1')
        self.send_event('E_ACTIVE_STATE', MC_CUT_RUSH)
        self.send_event('E_DIRECT_TO_HIT_START')
        self.send_event('E_CLEAR_SPEED')
        self.send_event('E_EXIT_CAM_CLIP', 'CHASING_HIT')

    def update--- This code section failed: ---

 228       0  LOAD_GLOBAL           0  'super'
           3  LOAD_GLOBAL           1  'CutTrack'
           6  LOAD_FAST             0  'self'
           9  CALL_FUNCTION_2       2 
          12  LOAD_ATTR             2  'update'
          15  LOAD_FAST             1  'dt'
          18  CALL_FUNCTION_1       1 
          21  POP_TOP          

 230      22  LOAD_FAST             0  'self'
          25  DUP_TOP          
          26  LOAD_ATTR             3  '_rush_cut_leave_time'
          29  LOAD_FAST             1  'dt'
          32  INPLACE_SUBTRACT 
          33  ROT_TWO          
          34  STORE_ATTR            3  '_rush_cut_leave_time'

 231      37  LOAD_FAST             0  'self'
          40  LOAD_ATTR             3  '_rush_cut_leave_time'
          43  LOAD_CONST            1  ''
          46  COMPARE_OP            1  '<='
          49  POP_JUMP_IF_FALSE    66  'to 66'

 233      52  LOAD_FAST             0  'self'
          55  LOAD_ATTR             4  'cut_rush_meet_target'
          58  CALL_FUNCTION_0       0 
          61  POP_TOP          

 234      62  LOAD_CONST            0  ''
          65  RETURN_END_IF    
        66_0  COME_FROM                '49'

 236      66  LOAD_FAST             0  'self'
          69  LOAD_ATTR             5  'ev_g_position'
          72  CALL_FUNCTION_0       0 
          75  STORE_FAST            2  'cur_position'

 239      78  LOAD_FAST             0  'self'
          81  LOAD_ATTR             6  '_last_rush_position'
          84  POP_JUMP_IF_FALSE   148  'to 148'

 240      87  LOAD_FAST             2  'cur_position'
          90  LOAD_FAST             0  'self'
          93  LOAD_ATTR             6  '_last_rush_position'
          96  BINARY_SUBTRACT  
          97  STORE_FAST            3  'frame_diff_dist'

 243     100  LOAD_FAST             3  'frame_diff_dist'
         103  LOAD_ATTR             7  'length_sqr'
         106  LOAD_FAST             0  'self'
         109  LOAD_ATTR             8  'NOT_MOVE_DIST_SQR'
         112  COMPARE_OP            1  '<='
         115  POP_JUMP_IF_FALSE   136  'to 136'

 244     118  LOAD_FAST             0  'self'
         121  DUP_TOP          
         122  LOAD_ATTR             9  '_not_same_pos_times'
         125  LOAD_CONST            2  1
         128  INPLACE_ADD      
         129  ROT_TWO          
         130  STORE_ATTR            9  '_not_same_pos_times'
         133  JUMP_ABSOLUTE       148  'to 148'

 246     136  LOAD_CONST            1  ''
         139  LOAD_FAST             0  'self'
         142  STORE_ATTR            9  '_not_same_pos_times'
         145  JUMP_FORWARD          0  'to 148'
       148_0  COME_FROM                '145'

 248     148  LOAD_FAST             0  'self'
         151  LOAD_ATTR             9  '_not_same_pos_times'
         154  LOAD_FAST             0  'self'
         157  LOAD_ATTR            10  'AUTO_STOP_WHEN_NOT_MOVE_TIMES'
         160  COMPARE_OP            5  '>='
         163  POP_JUMP_IF_FALSE   180  'to 180'

 250     166  LOAD_FAST             0  'self'
         169  LOAD_ATTR             4  'cut_rush_meet_target'
         172  CALL_FUNCTION_0       0 
         175  POP_TOP          

 251     176  LOAD_CONST            0  ''
         179  RETURN_END_IF    
       180_0  COME_FROM                '163'

 253     180  LOAD_FAST             0  'self'
         183  LOAD_ATTR             5  'ev_g_position'
         186  CALL_FUNCTION_0       0 
         189  STORE_FAST            4  'track_start_position'

 254     192  LOAD_FAST             0  'self'
         195  LOAD_ATTR            11  'ev_g_attack_target_position'
         198  CALL_FUNCTION_0       0 
         201  STORE_FAST            5  'track_target_position'

 255     204  LOAD_FAST             4  'track_start_position'
         207  UNARY_NOT        
         208  POP_JUMP_IF_TRUE    218  'to 218'
         211  LOAD_FAST             5  'track_target_position'
         214  UNARY_NOT        
       215_0  COME_FROM                '208'
         215  POP_JUMP_IF_FALSE   232  'to 232'

 256     218  LOAD_FAST             0  'self'
         221  LOAD_ATTR             4  'cut_rush_meet_target'
         224  CALL_FUNCTION_0       0 
         227  POP_TOP          

 257     228  LOAD_CONST            0  ''
         231  RETURN_END_IF    
       232_0  COME_FROM                '215'

 259     232  LOAD_FAST             5  'track_target_position'
         235  LOAD_FAST             4  'track_start_position'
         238  BINARY_SUBTRACT  
         239  STORE_FAST            6  'dist_dir'

 260     242  LOAD_CONST            1  ''
         245  LOAD_FAST             6  'dist_dir'
         248  STORE_ATTR           12  'y'

 261     251  LOAD_FAST             6  'dist_dir'
         254  LOAD_ATTR            13  'length'
         257  STORE_FAST            7  'dist'

 263     260  LOAD_FAST             0  'self'
         263  LOAD_ATTR            14  'ev_g_cut_track_gap_dist'
         266  CALL_FUNCTION_0       0 
         269  STORE_FAST            8  'cut_track_gap_dist'

 266     272  LOAD_FAST             7  'dist'
         275  LOAD_FAST             8  'cut_track_gap_dist'
         278  COMPARE_OP            1  '<='
         281  POP_JUMP_IF_FALSE   298  'to 298'

 267     284  LOAD_FAST             0  'self'
         287  LOAD_ATTR             4  'cut_rush_meet_target'
         290  CALL_FUNCTION_0       0 
         293  POP_TOP          

 269     294  LOAD_CONST            0  ''
         297  RETURN_END_IF    
       298_0  COME_FROM                '281'

 271     298  LOAD_GLOBAL          15  'math3d'
         301  LOAD_ATTR            16  'vector'
         304  LOAD_FAST             6  'dist_dir'
         307  CALL_FUNCTION_1       1 
         310  STORE_FAST            9  'move_dir'

 272     313  LOAD_FAST             9  'move_dir'
         316  LOAD_ATTR            17  'is_zero'
         319  POP_JUMP_IF_TRUE    335  'to 335'

 273     322  LOAD_FAST             9  'move_dir'
         325  LOAD_ATTR            18  'normalize'
         328  CALL_FUNCTION_0       0 
         331  POP_TOP          
         332  JUMP_FORWARD          0  'to 335'
       335_0  COME_FROM                '332'

 275     335  LOAD_FAST             0  'self'
         338  LOAD_ATTR            19  'calcute_new_cut_rush_dir'
         341  CALL_FUNCTION_0       0 
         344  STORE_FAST           10  'rush_cut_move_dir'

 276     347  LOAD_FAST            10  'rush_cut_move_dir'
         350  LOAD_FAST             0  'self'
         353  LOAD_ATTR            20  '_cut_rush_speed'
         356  BINARY_MULTIPLY  
         357  STORE_FAST           11  'speed_dir'

 278     360  LOAD_FAST             7  'dist'
         363  LOAD_FAST             8  'cut_track_gap_dist'
         366  BINARY_SUBTRACT  
         367  STORE_FAST           12  'need_move_dist'

 279     370  LOAD_FAST             4  'track_start_position'
         373  LOAD_FAST             9  'move_dir'
         376  LOAD_FAST            12  'need_move_dist'
         379  BINARY_MULTIPLY  
         380  BINARY_ADD       
         381  STORE_FAST           13  'reach_target_pos'

 281     384  LOAD_FAST             0  'self'
         387  LOAD_ATTR            21  'send_event'
         390  LOAD_CONST            3  'E_SET_WALK_DIRECTION'
         393  LOAD_FAST            11  'speed_dir'
         396  LOAD_FAST             0  'self'
         399  LOAD_ATTR            22  'cut_rush_reach_target_callback'
         402  LOAD_FAST            13  'reach_target_pos'
         405  CALL_FUNCTION_4       4 
         408  POP_TOP          

 282     409  LOAD_GLOBAL          23  'rotate_target'
         412  LOAD_GLOBAL           4  'cut_rush_meet_target'
         415  LOAD_GLOBAL          24  'False'
         418  CALL_FUNCTION_257   257 
         421  POP_TOP          

 283     422  LOAD_FAST            10  'rush_cut_move_dir'
         425  LOAD_FAST             0  'self'
         428  STORE_ATTR           25  '_last_rush_cut_move_dir'

 284     431  LOAD_FAST             2  'cur_position'
         434  LOAD_FAST             0  'self'
         437  STORE_ATTR            6  '_last_rush_position'

 286     440  LOAD_GLOBAL          26  'is_block_collision'
         443  LOAD_FAST             0  'self'
         446  CALL_FUNCTION_1       1 
         449  POP_JUMP_IF_FALSE   466  'to 466'

 288     452  LOAD_FAST             0  'self'
         455  LOAD_ATTR             4  'cut_rush_meet_target'
         458  CALL_FUNCTION_0       0 
         461  POP_TOP          

 289     462  LOAD_CONST            0  ''
         465  RETURN_END_IF    
       466_0  COME_FROM                '449'

Parse error at or near `CALL_FUNCTION_257' instruction at offset 418

    def cut_rush_reach_target_callback(self, *args):
        self.send_event('E_CLEAR_SPEED')
        if not self.ev_g_is_jump():
            self.send_event('E_VERTICAL_SPEED', 0)


class NormalMelee(StateBase):
    BIND_EVENT = {'E_CHARACTER_ATTR': 'change_character_attr',
       'E_ANIMATOR_LOADED': 'on_load_animator_complete',
       'E_ATTACK_TARGET_POSITION': 'set_target_position',
       'G_ATTACK_TARGET_POSITION': 'get_target_position',
       'E_MELEE_HIT_TARGET': 'hit_target',
       'E_LEAVE_STATE': '_leave_states',
       'E_RESUME_HIT_ANIM': '_resume_hit_anim',
       'E_MECHA_ENTER_DIVING': '_on_enter_diving',
       'E_MECHA_LEAVE_DIVING': '_on_leave_diving',
       'G_MELEE_STAGE': 'get_stage',
       'E_MELEE_STAGE': 'set_stage',
       'E_CHECK_MELEE_NEXT_STAGE': 'check_continue_next_stage',
       'E_DIRECT_TO_HIT_START': 'direct_to_hit_start',
       'G_CUT_TRACK_GAP_DIST': 'get_cut_track_gap_dist',
       'E_DECIDE_TRACK_OR_CUT': 'decide_track_or_cut'
       }
    ATTACK_ANIM_TRIGGER = 'fx_attack'
    MAX_STAGE = 3
    DO_NOT_MOVE_MAX_DIST = 0.5 * NEOX_UNIT_SCALE
    ATTACK_STATE = tuple(set([MC_CUT_RUSH]))
    END_TRACK_EVENT = 'tracking'
    BEGIN_COMBO_MOVE_EVENT = 'MC_COMBO_MOVE_ATTACK_combo_move'
    STATE_ATTACK_1 = 1
    STATE_ATTACK_2 = 2
    STATE_ATTACK_3 = 3

    def init_from_dict(self, unit_obj, bdict, sid, state_info):
        super(NormalMelee, self).init_from_dict(unit_obj, bdict, sid, state_info)
        self.cur_stage = 0
        self._next_stage = 0
        self._move_duration = 1
        self._target = None
        self._track_rate = 1
        self._track_target_position = None
        self._track_start_position = None
        self._enable = True
        self._last_stage_hit_target = None
        self._rush_cut_leave_time = 0
        self._cut_human_track_gap_dist = 0
        self._cut_mecha_track_gap_dist = 0
        self._allow_break_self = False
        self._start_from_hit = False
        self.init_paramater()
        self.register_substate()
        return

    def on_load_animator_complete(self, *args):
        self._is_on_gournd(True)

    def change_character_attr(self, name, *arg):
        if name == 'animator_info':
            if self.is_active:
                print('test--NormalMelee.animator_info--cur_stage =', self.cur_stage, '--_next_stage =', self._next_stage, '--sub_state =', self.sub_state, '--sub_sid_timer =', self.sub_sid_timer, '--sub_states_triggers =', self.sub_states_triggers)

    def init_paramater(self):
        self._cut_human_track_gap_dist = self.custom_param.get('cut_human_track_gap_dist', 3.5) * NEOX_UNIT_SCALE
        self._cut_mecha_track_gap_dist = self.custom_param.get('cut_mecha_track_gap_dist', 6) * NEOX_UNIT_SCALE
        self._no_target_cut_move_dist = self.custom_param.get('no_target_cut_move_dist', 2) * NEOX_UNIT_SCALE
        self._mecha_cut_track_max_dist = self.custom_param.get('mecha_cut_track_max_dist', 30) * NEOX_UNIT_SCALE
        self._human_cut_track_max_dist = self.custom_param.get('human_cut_track_max_dist', 30) * NEOX_UNIT_SCALE
        self._min_track_threshold = self.custom_param.get('min_track_threshold', 10) * NEOX_UNIT_SCALE
        self._hit_stop_frames = self.custom_param.get('hit_stop_frames', 3)
        self._clip_list = self.custom_param.get('clip_list', robot_animation_const.MELEE_CLIPS)
        self._anim_duration_list = self.custom_param.get('anim_duration_list', [ 1 for _ in range(len(self._clip_list)) ])

    def register_substate(self):
        for stage in range(1, self.MAX_STAGE + 1):
            key = 'stage_%d' % stage
            stage_config = self.custom_param.get(key, None)
            if not stage_config:
                continue
            start_time = stage_config[self.END_TRACK_EVENT]
            start_time /= CUT_TIME_SCALE
            self.register_substate_callback(stage, start_time, self.end_tracking)
            start_time = stage_config[START_CUT_ATTACK_EVENT]
            start_time /= CUT_TIME_SCALE
            self.register_substate_callback(stage, start_time, self.start_cut_attack)
            start_time = stage_config[END_CUT_ATTACK_EVENT]
            start_time /= CUT_TIME_SCALE
            self.register_substate_callback(stage, start_time, self.end_cut_attack)
            start_time = stage_config[self.BEGIN_COMBO_MOVE_EVENT]
            start_time /= CUT_TIME_SCALE
            self.register_substate_callback(stage, start_time, self.being_combo_move)
            start_time = stage_config[END_CUT_BACK1_EVENT]
            start_time /= CUT_TIME_SCALE
            self.register_substate_callback(stage, start_time, self.end_cut_back1)
            start_time = self._anim_duration_list[stage - 1]
            start_time /= CUT_TIME_SCALE
            self.register_substate_callback(stage, start_time, self.exit_attack)

        stage = self.MAX_STAGE + 1
        start_time = self._anim_duration_list[stage - 1]
        start_time /= CUT_TIME_SCALE
        self.register_substate_callback(stage, start_time, self.exit_attack)
        return

    def action_btn_down(self):
        super(NormalMelee, self).action_btn_down()
        if not self._enable:
            return True
        if self.ev_g_get_state(MC_THUMP_RUSH):
            return True
        if self.is_active:
            if not self._allow_break_self:
                if self._next_stage == self.cur_stage:
                    self._next_stage += 1
                    if self._next_stage > self.MAX_STAGE + 1:
                        self._next_stage = 1
                return True
        if self.ev_g_get_state(MC_DASH):
            self.send_event('E_DISABLE_STATE', MC_DASH)
            self.send_event('E_ACTIVE_STATE', MC_THUMP_RUSH)
            return True
        dist = self.get_attack_dist()
        if dist > self._min_track_threshold and not is_block_collision(self):
            self.disable_self()
            self.send_event('E_ACTIVE_STATE', MC_CUT_TRACK)
        elif self.is_active:
            self.start_melee()
        else:
            self.active_self()
        return True

    def decide_track_or_cut(self):
        self.cur_stage = 0
        self._next_stage = 0
        dist = self.get_attack_dist()
        if dist > self._min_track_threshold and not is_block_collision(self):
            self.send_event('E_ACTIVE_STATE', MC_CUT_TRACK)
        else:
            self.active_self()

    def start_melee(self):
        self.cur_stage += 1
        self._next_stage = self.cur_stage
        self.begin_attack()
        self.send_event('E_UPDATE_STATUS_TIME', MC_CUT_RUSH)
        if self.cur_stage > self.MAX_STAGE + 1:
            self.send_event('E_DUMP_STATE')
        delay_time = self._anim_duration_list[self.cur_stage - 1]

    def enter(self, leave_states):
        self.send_event('E_UPBODY_BONE', FULL_BODY_BONE)
        super(NormalMelee, self).enter(leave_states)
        if leave_states and MC_SWORD_ENERGY in leave_states:
            cur_stage = self.cur_stage
            if cur_stage >= self.MAX_STAGE:
                self.cur_stage = 0
        self.start_melee()

    def exit(self, enter_states):
        super(NormalMelee, self).exit(enter_states)
        self.send_event('E_UPBODY_BONE', DEFAULT_UP_BODY_BONE)
        self.send_event('E_CLEAR_UP_BODY_ANIM')
        if MC_SWORD_ENERGY not in enter_states:
            self.cur_stage = 0
        self._last_stage_hit_target = None
        global_data.emgr.enable_camera_yaw.emit(True)
        self.end_hit_target()
        self._next_stage = 0
        if self.ev_g_is_jump():
            self.immediate_stop_melee()
        else:
            self.reach_target_callback()
        return

    def exit_attack(self, *args):
        if self.cur_stage > self.MAX_STAGE:
            self.check_continue_next_stage()
        elif self._next_stage == self.cur_stage:
            self.disable_self()
            self.send_event('E_ACTIVE_STATE', MC_STAND)
        else:
            self.check_continue_next_stage()

    @property
    def cur_stage(self):
        return self.ev_g_attack_stage()

    @cur_stage.setter
    def cur_stage(self, value):
        self.sub_state = value
        self.send_event('E_ATTACK_STAGE', value, auto_clear_stage=False)

    def end_tracking(self, *args):
        if self._move_duration > 0 and self.ev_g_on_ground():
            self.send_event('E_CLEAR_SPEED')
        self.reach_target_callback()

    def start_cut_attack(self, *args):
        self.send_event('E_START_MELEE_HIT', self.cur_stage)

    def end_cut_attack(self, *args):
        self.send_event('E_END_MELEE_HIT')
        if self.ev_g_is_jump():
            self.immediate_stop_melee()
        if not self.ev_g_is_avatar():
            return
        if hasattr(global_data, 'melee_lock_camera') and global_data.melee_lock_camera:
            global_data.emgr.enable_camera_yaw.emit(True)
            self.send_event('E_RESET_ROTATION')

    def being_combo_move(self, *args):
        white_states = self.custom_param.get('MC_COMBO_MOVE_ATTACK', None)
        if white_states:
            self.send_event('E_ADD_WHITE_STATE', status_utils.convert_status(set(white_states)), MC_CUT_RUSH)
        return

    def on_auto_claer_stage(self):
        self._next_stage = 0

    def end_cut_back1(self, *args):
        self._allow_break_self = True
        self.send_event('E_BEGIN_ATTACK_STAGE', self.on_auto_claer_stage)
        if self._next_stage == self.cur_stage:
            white_states = self.custom_param.get('MC_CUT_BACK2', None)
            if white_states:
                self.send_event('E_ADD_WHITE_STATE', status_utils.convert_status(set(white_states)), MC_CUT_RUSH)
            if self.ev_g_is_jump():
                self.immediate_stop_melee()
            rocker_dir = self.sd.ref_rocker_dir
            if rocker_dir and not rocker_dir.is_zero:
                self.disable_self()
                self.send_event('E_ACTIVE_STATE', MC_MOVE)
        else:
            self.check_continue_next_stage()
        return

    def immediate_stop_melee(self, duration=0.1):
        pass

    def check_continue_next_stage(self):
        old_stage = self.cur_stage
        if self._next_stage != self.cur_stage:
            self.cur_stage = self._next_stage
            if self.cur_stage > self.MAX_STAGE + 1:
                self.send_event('E_DUMP_STATE')
                self.send_event('E_CHARACTER_ATTR', 'animator_info', True)
            self.begin_attack(from_check=True)
        elif self._next_stage > self.MAX_STAGE:
            self.cur_stage = 1
            self._next_stage = self.cur_stage
            self.begin_attack(from_check=True)

    def set_target_position(self, position, track_rate=1, target=None):
        self._track_rate = track_rate
        self._target = target

    def get_target_position(self):
        if not self._target:
            return
        return self._target.ev_g_position()

    def _resume_hit_anim(self):
        self.end_hit_target()

    def end_hit_target_action(self):
        model = self.ev_g_model()
        if not model:
            return
        clip_name = self.get_attack_clip_name()
        sfx = model.get_anim_trigger_socket_obj(clip_name, self.ATTACK_ANIM_TRIGGER, 0)
        if sfx:
            sfx.frame_rate = 1

    def end_hit_target(self, *args):
        self.end_hit_target_action()
        self.send_event('E_RESUME_FREEZE')

    def hit_target(self, target):
        self._last_stage_hit_target = True
        if not target:
            return
        model = self.ev_g_model()
        if not model:
            return
        clip_name = self.get_attack_clip_name()
        sfx = model.get_anim_trigger_socket_obj(clip_name, self.ATTACK_ANIM_TRIGGER, 0)
        if sfx:
            sfx.frame_rate = 0
        delay_time = self._hit_stop_frames / 30.0
        import common.utils.timer as timer
        global_data.game_mgr.register_logic_timer(self.end_hit_target, delay_time, times=1, mode=timer.CLOCK, timedelta=True)

    def get_stage(self):
        return self.cur_stage

    def set_stage(self, stage):
        if stage >= self.MAX_STAGE or stage < 0:
            stage = 0
        self.cur_stage = stage

    def get_attack_dist(self):
        track_target_position = self.ev_g_attack_target_position()
        if not track_target_position:
            return 0
        track_start_position = self.ev_g_position()
        if not track_start_position:
            return 0
        dist_dir = track_target_position - track_start_position
        return dist_dir.length

    def get_cut_track_gap_dist(self):
        if self._target.ev_g_in_mecha():
            return self._cut_mecha_track_gap_dist
        else:
            return self._cut_human_track_gap_dist

    def begin_attack(self, *args, **kwargs):
        self._allow_break_self = False
        if self.cur_stage > self.MAX_STAGE:
            self.decide_attack()
            return
        self._track_start_position = self.ev_g_position()
        self._track_target_position = self.ev_g_attack_target_position()
        forward_dir = self.ev_g_model_forward()
        if not forward_dir or forward_dir.is_zero:
            print('[error] test--forward_dir.is_zero')
            return
        from_check = kwargs.get('from_check', False)
        forward_dir.normalize()
        dist = 0
        if not self._track_target_position:
            self.decide_attack(from_sync=from_check)
            if self.ev_g_is_jump():
                self._move_duration = 0
                return
            dist = self._no_target_cut_move_dist
            self._track_target_position = self._track_start_position + forward_dir * dist
            rotate_target(self)
        else:
            dist_dir = self._track_target_position - self._track_start_position
            cut_track_max_dist = 0
            if self._target.ev_g_in_mecha():
                cut_track_max_dist = self._mecha_cut_track_max_dist
            else:
                cut_track_max_dist = self._human_cut_track_max_dist
            cut_track_gap_dist = self.get_cut_track_gap_dist()
            cut_track_max_dist = cut_track_max_dist * self._track_rate - cut_track_gap_dist
            dist = dist_dir.length
            dist_dir.normalize()
            self.decide_attack()
            rotate_target(self)
            if dist <= cut_track_gap_dist:
                return
        if dist > cut_track_max_dist:
            self._track_target_position = self._track_start_position + dist_dir * cut_track_max_dist
        elif dist > cut_track_gap_dist:
            need_move_dist = dist - cut_track_gap_dist
            self._track_target_position = self._track_start_position + dist_dir * need_move_dist
        self.move_to_target()

    def move_to_target(self, *args):
        self_position = self._track_start_position
        if not self_position:
            return
        target_position = self._track_target_position
        if not target_position:
            return
        walk_direction = target_position - self_position
        if walk_direction.is_zero:
            return
        if walk_direction.length <= self.DO_NOT_MOVE_MAX_DIST:
            return
        move_dir = math3d.vector(0, 0, 0)
        if self._move_duration <= 0:
            print('test-[error]--_move_duration =', self._move_duration)
            self._move_duration = 1
        scale = 1.0 / self._move_duration
        speed = walk_direction * scale
        move_dir = speed
        if move_dir.y == 0:
            if not self.ev_g_is_jump():
                self.send_event('E_VERTICAL_SPEED', move_dir.y)
        else:
            self.send_event('E_VERTICAL_SPEED', move_dir.y)
        move_dir.y = 0
        self.send_event('E_SET_WALK_DIRECTION', move_dir)

    def get_attack_clip_name(self):
        anim_idx = self.cur_stage - 1
        if anim_idx >= len(self._clip_list) or anim_idx < 0:
            print('[error]test--get_attack_clip_name--cur_stage =', self.cur_stage, '--len(_clip_list) =', len(self._clip_list))
            anim_idx = 0
        clip_name = self._clip_list[anim_idx]
        return clip_name

    def get_track_duration(self):
        key = 'stage_%d' % self.cur_stage
        stage_config = self.custom_param.get(key, None)
        if not stage_config:
            return 0.1
        else:
            return stage_config.get('tracking', 0.1)

    def decide_attack(self, from_sync=False):
        driver = self.sd.ref_driver_id
        if not from_sync and not self.ev_g_is_avatar():
            return
        else:
            clip_name = self.get_attack_clip_name()
            blend_time = 0
            if self.cur_stage == self.MAX_STAGE + 1:
                blend_time = 0.2
            if self._last_stage_hit_target:
                self._last_stage_hit_target = None
            if self.cur_stage <= self.MAX_STAGE:
                self._move_duration = self.get_track_duration()
            dest_phase = 0
            if self._start_from_hit:
                self._start_from_hit = False
                model = self.ev_g_model()
                if model:
                    start_time = model.get_anim_event_time(clip_name, 'hit_start')
                    end_time = model.get_anim_event_time(clip_name, 'end')
                    dest_phase = start_time / end_time
            self.send_event('E_POST_ACTION', clip_name, UP_BODY, 1, blend_time=blend_time, timeScale=CUT_TIME_SCALE * self.timer_rate, phase=dest_phase)
            self.send_event('E_ANIM_PHASE', UP_BODY, dest_phase)
            return

    def direct_to_hit_start(self):
        self._start_from_hit = True

    def reach_target_callback(self, *args):
        if not self.ev_g_is_jump():
            self.send_event('E_VERTICAL_SPEED', 0)

    def _is_on_gournd(self, on_ground):
        model = self.ev_g_model()
        if not model:
            return
        for index in range(1, 4):
            model.set_socket_bound_obj_active('fx_attack_0{}'.format(index), 4, on_ground, False)

    def _on_enter_diving(self):
        self._enable = False

    def _on_leave_diving(self):
        self._enable = True


class HeavyMelee(StateBase):
    SUB_STATE_ID = 1
    ACC_STOP_EVENT = 'acc_stop'
    BIND_EVENT = {'E_CHARACTER_ATTR': 'change_character_attr',
       'E_START_DASH_MELEE': 'start_melee',
       'G_IS_HEAVY_MELEE': 'is_heavy_melee',
       'G_CAN_BREAK_HEAVY_MELEE': 'can_break_heavy_melee',
       'E_MECHA_ENTER_DIVING': '_on_enter_diving',
       'E_MECHA_LEAVE_DIVING': '_on_leave_diving'
       }

    def init_from_dict(self, unit_obj, bdict, sid, state_info):
        super(HeavyMelee, self).init_from_dict(unit_obj, bdict, sid, state_info)
        self._have_next_stage = None
        self._thump_dash_speed = 0
        self._brake_acc_val = 0
        self._max_rush_time = 1
        self._rush_time = 0
        self._allow_break_self = False
        self._enable = True
        self._is_finish = True
        self.init_paramater()
        self.register_substate()
        return

    def change_character_attr(self, name, *arg):
        if name == 'animator_info':
            if self.is_active:
                print('test--HeavyMelee.animator_info--_rush_time =', self._rush_time, '--_allow_break_self =', self._allow_break_self, '--sub_state =', self.sub_state, '--sub_sid_timer =', self.sub_sid_timer, '--sub_states_triggers =', self.sub_states_triggers)

    def action_btn_down(self):
        super(HeavyMelee, self).action_btn_down()
        if not self._enable or self._is_finish:
            return True
        if self.is_active:
            if not self._allow_break_self:
                self._have_next_stage = True
                return True
        self.begin_next_melee()
        return True

    def begin_next_melee(self):
        self.disable_self()
        self.send_event('E_DECIDE_TRACK_OR_CUT')
        self._is_finish = True
        self._have_next_stage = None
        return

    def init_paramater(self):
        self._thump_dash_speed = self.custom_param.get('thump_dash_speed', 15) * NEOX_UNIT_SCALE
        start_brake_time = self.custom_param.get('acc_stop', 0.168)
        brake_end_time = self.custom_param.get('stop', 0.622)
        self._max_rush_time = brake_end_time - start_brake_time
        self._brake_acc_val = -self._thump_dash_speed / self._max_rush_time

    def register_substate(self):
        event_config = self.custom_param.get('event', {})
        start_time = event_config.get(self.ACC_STOP_EVENT, 0.1)
        self.register_substate_callback(self.SUB_STATE_ID, start_time, self.on_start_stop)
        start_time = event_config.get(START_CUT_ATTACK_EVENT, 0.1)
        self.register_substate_callback(self.SUB_STATE_ID, start_time, self.start_cut_attack)
        start_time = event_config.get(END_CUT_ATTACK_EVENT, 0.2)
        self.register_substate_callback(self.SUB_STATE_ID, start_time, self.end_cut_attack)
        start_time = event_config.get(END_CUT_BACK1_EVENT, 0.3)
        self.register_substate_callback(self.SUB_STATE_ID, start_time, self.end_cut_back1)
        start_time = self.custom_param.get('anim_duration', 2)
        self.register_substate_callback(self.SUB_STATE_ID, start_time, self.exit_attack)

    def enter(self, leave_states):
        super(HeavyMelee, self).enter(leave_states)
        self._is_finish = False
        action = self.ev_g_get_action_by_status(MC_CUT_RUSH)
        if action:
            self.send_event('E_SWITCH_ACTION', action, MC_THUMP_RUSH)
        self.send_event('E_UPBODY_BONE', FULL_BODY_BONE)
        self.sub_state = self.SUB_STATE_ID
        self._have_next_stage = None
        self.start_melee()
        return

    def exit(self, enter_states):
        super(HeavyMelee, self).exit(enter_states)
        action = self.ev_g_get_action_by_status(MC_THUMP_RUSH)
        if action:
            self.send_event('E_SWITCH_ACTION', action, MC_CUT_RUSH)
        self.send_event('E_UPBODY_BONE', DEFAULT_UP_BODY_BONE)
        self.send_event('E_CLEAR_UP_BODY_ANIM')
        if self.ev_g_on_ground():
            self.send_event('E_CLEAR_SPEED')
        self.sub_state = None
        self._have_next_stage = None
        self._rush_time = 0
        self._is_finish = True
        return

    def exit_attack(self, *args):
        print('test--HeavyMelee.exit_attack')
        self.disable_self()

    def on_start_stop(self, *args):
        self._rush_time = self._max_rush_time
        self._speed = self._thump_dash_speed
        if not self.ev_g_is_jump():
            self.send_event('E_VERTICAL_SPEED', 0)

    def start_melee(self):
        self._allow_break_self = False
        self.begin_attack()
        self.begin_move()

    def begin_attack(self, *args):
        pass

    def begin_move(self):
        walk_direction = self.ev_g_get_walk_direction()
        if walk_direction.is_zero:
            return
        walk_direction.normalize()
        walk_direction = walk_direction * self._thump_dash_speed
        self.send_event('E_SET_WALK_DIRECTION', walk_direction)
        self.send_event('E_CHANGE_CHAR_GROUP', GROUP_CHARACTER_INCLUDE)

    def update(self, dt):
        super(HeavyMelee, self).update(dt)
        if self._rush_time <= 0:
            return
        self._rush_time -= dt
        self._speed = self._speed + dt * self._brake_acc_val
        if self._speed <= 0:
            self._speed = 0
        elif self._speed >= self._thump_dash_speed:
            self._speed = self._thump_dash_speed
        walk_direction = self.ev_g_model_forward()
        walk_direction = walk_direction * self._speed
        self.send_event('E_SET_WALK_DIRECTION', walk_direction)

    def start_cut_attack(self, *args):
        self.send_event('E_START_MELEE_HIT', 1)

    def end_cut_attack(self, *args):
        self.send_event('E_END_MELEE_HIT')
        if self.ev_g_is_jump():
            self.immediate_stop_melee()
        if not self.ev_g_is_avatar():
            return
        if hasattr(global_data, 'melee_lock_camera') and global_data.melee_lock_camera:
            global_data.emgr.enable_camera_yaw.emit(True)
            self.send_event('E_RESET_ROTATION')

    def end_cut_back1(self, *args):
        self._allow_break_self = True
        if self._have_next_stage:
            self.begin_next_melee()
        else:
            if self.ev_g_is_jump():
                self.immediate_stop_melee()
            self.send_event('E_ACTIVE_STATE', MC_STAND)

    def can_break_heavy_melee(self, *args):
        return self._allow_break_self

    def immediate_stop_melee(self, duration=0.1):
        pass

    def is_heavy_melee(self, *args):
        return self.is_active

    def _on_enter_diving(self):
        self._enable = False

    def _on_leave_diving(self):
        self._enable = True