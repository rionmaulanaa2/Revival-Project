# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gutils/move_utils.py
from __future__ import absolute_import
from logic.gcommon.behavior.StateBase import clamp
from logic.gcommon.common_const import character_anim_const
import logic.gcommon.common_const.animation_const as animation_const
import logic.gcommon.cdata.status_config as status_config
from logic.gcommon.common_const import water_const
from logic.gcommon.cdata import speed_physic_arg, jump_physic_config
from logic.gcommon.const import NEOX_UNIT_SCALE
from logic.gutils.character_ctrl_utils import AirWalkDirectionSetter
import math3d
import world
import math
UNIT_Y = math3d.vector(0, 1, 0)
NORMAL_MOVE = 0
FLIGHT_FLOAT = 1
SKATE_MOVE = 2

def empty_func(self, *args):
    pass


def init_flight_float(self):
    self.air_walk_direction_setter = AirWalkDirectionSetter(self)


def enter_normal_move(self):
    cur_speed = self.sd.ref_cur_speed
    self.sub_state = self.STATE_MOVE if cur_speed > 1 or not self.move_start_anim else self.STATE_START


def enter_flight_float(self):
    cur_speed = self.sd.ref_cur_speed
    cur_walk_speed = self.slow_down or self.walk_speed if 1 else self.slow_down_speed
    max_speed = self.ev_g_get_speed_scale() * cur_walk_speed
    rocker_dir = self.sd.ref_rocker_dir
    acc = rocker_dir and not rocker_dir.is_zero
    if cur_speed < max_speed:
        if acc:
            self.sub_state = self.STATE_START
        else:
            self.sub_state = self.STATE_STOP
    else:
        self.sub_state = self.STATE_MOVE
    self.on_ground_clock = 0
    self.leave_ground_clock = 0
    self.leaving_ground = False
    self.HORIZONTAL_FORWARD_INTERPOLATE_DURATION = 0.5
    self.air_walk_direction_setter.reset()
    self.send_event('E_FORBID_ROTATION', True)
    self.send_event('E_ENABLE_INJECT_BRAKE_MOVE', False)


def normal_move_logic(self, dt):
    rocker_dir = self.sd.ref_rocker_dir
    if self.last_rocker_dir != rocker_dir:
        self.last_rocker_dir = rocker_dir
        if self.last_rocker_dir is not None:
            self.send_event('E_ACTION_MOVE')
    cur_speed = self.sd.ref_cur_speed
    max_speed = self.ev_g_get_speed_scale()
    if cur_speed is None or max_speed is None:
        return
    else:
        cur_walk_speed = self.slow_down or self.walk_speed if 1 else self.slow_down_speed
        max_speed *= cur_walk_speed
        acc = rocker_dir and not rocker_dir.is_zero
        cur_speed += dt * (self.move_acc if acc else self.brake_acc)
        cur_speed = clamp(cur_speed, 0, max_speed)
        self.sd.ref_cur_speed = cur_speed
        self.send_event('E_MOVE', rocker_dir)
        if not acc and self.sub_state == self.STATE_MOVE and self.move_start_anim:
            self.sub_state = self.STATE_STOP
        if acc and not self.last_is_acc and self.move_stop_anim:
            self.sub_state = self.STATE_START
        self.last_is_acc = acc
        if (cur_speed == max_speed or self.force_dynamic_speed_rate) and cur_walk_speed != 0:
            self.send_event('E_ANIM_RATE', character_anim_const.LOW_BODY, cur_speed / cur_walk_speed * self.dynamic_speed_rate)
        return


def skate_move_logic(self, dt):
    rocker_dir = self.sd.ref_rocker_dir
    if self.last_rocker_dir != rocker_dir:
        self.last_rocker_dir = rocker_dir
        if self.last_rocker_dir is not None:
            self.send_event('E_ACTION_MOVE')
    cur_speed = self.sd.ref_cur_speed
    cur_walk_speed = self.slow_down or self.walk_speed if 1 else self.slow_down_speed
    max_speed = cur_walk_speed
    if cur_speed is None or max_speed is None:
        return
    else:
        acc = rocker_dir and not rocker_dir.is_zero
        brake_acc = self.brake_acc
        if not acc:
            if cur_speed <= 0 and self.sub_state == self.STATE_MOVE:
                self.sub_state = self.STATE_STOP
            if self.is_skate_braking:
                brake_acc = self.skate_brake_acc
        dt_speed = dt * (self.move_acc if acc else brake_acc)
        cur_speed += dt_speed
        cur_speed = clamp(cur_speed, 0, max_speed + 1)
        self.sd.ref_cur_speed = cur_speed
        self.send_event('E_MOVE', rocker_dir)
        if acc and not self.last_is_acc:
            self.sub_state = self.STATE_START
        self.last_is_acc = acc
        if self.sub_state == self.STATE_MOVE and not self.is_skate_braking:
            time_scale = 1
            if cur_walk_speed > 0:
                time_scale = cur_speed / cur_walk_speed * self.dynamic_speed_rate
            self.send_event('E_ANIM_RATE', character_anim_const.LOW_BODY, time_scale)
        return


def flight_float_logic(self, dt):
    rocker_dir = self.sd.ref_rocker_dir
    if self.last_rocker_dir != rocker_dir:
        self.last_rocker_dir = rocker_dir
        if self.last_rocker_dir is not None:
            self.send_event('E_ACTION_MOVE')
    cur_speed = self.sd.ref_cur_speed
    cur_walk_speed = self.walk_speed
    max_speed = self.ev_g_get_speed_scale() * cur_walk_speed
    if cur_speed is None or max_speed is None:
        return
    else:
        acc = rocker_dir and not rocker_dir.is_zero
        cur_speed += dt * (self.move_acc if acc else self.brake_acc)
        cur_speed = clamp(cur_speed, 0, max_speed + 1)
        self.sd.ref_cur_speed = cur_speed
        camera = world.get_active_scene().active_camera
        if not camera:
            return
        if self.in_free_camera_mode and self.last_camera_matrix:
            cam_matrix = self.last_camera_matrix
        else:
            cam_matrix = camera.rotation_matrix
        if not rocker_dir or rocker_dir.is_zero:
            walk_direction = self.ev_g_get_walk_direction()
            if not walk_direction.is_zero:
                walk_direction.normalize()
        else:
            self.send_event('E_CHANGE_ANIM_MOVE_DIR', rocker_dir.x, rocker_dir.z)
            rot = math3d.matrix_to_rotation(cam_matrix)
            walk_direction = rot.rotate_vector(rocker_dir)
            if rocker_dir.z < 0:
                walk_direction.y = 0
                walk_direction.normalize()
            if self.ev_g_position().y >= self.max_height and walk_direction.y > 0:
                walk_direction.y = 0
                walk_direction.normalize()
            on_ground = self.ev_g_on_ground()
            if on_ground:
                if walk_direction.y > 0:
                    self.on_ground_clock = 0
            walk_direction = walk_direction * cur_speed + self.ev_g_inject_brake_walk_direction()
            self.air_walk_direction_setter.execute(walk_direction)
            self.sd.ref_cur_speed = cur_speed
            if cur_speed < max_speed:
                if acc:
                    self.sub_state = self.STATE_START
                else:
                    self.sub_state = self.STATE_STOP
            else:
                self.sub_state = self.STATE_MOVE
            cam_forward = math3d.vector(cam_matrix.forward)
            v = math3d.vector(0, 0, 0)
            if on_ground:
                self.on_ground_clock += dt
                if self.on_ground_clock > self.HORIZONTAL_FORWARD_INTERPOLATE_DURATION:
                    self.on_ground_clock = self.HORIZONTAL_FORWARD_INTERPOLATE_DURATION
                cam_forward.y = 0
                cam_forward.normalize()
                v.intrp(self.ev_g_forward(), cam_forward, self.on_ground_clock / self.HORIZONTAL_FORWARD_INTERPOLATE_DURATION)
                self.send_event('E_FORWARD', v, True)
                self.leaving_ground = True
                return
        if not self.leaving_ground:
            self.leave_ground_clock = 0
        self.on_ground_clock = 0
        if self.sub_state == self.STATE_START:
            v.intrp(self.ev_g_forward(), cam_forward, cur_speed / max_speed)
        elif self.sub_state == self.STATE_MOVE:
            if self.leaving_ground:
                self.leave_ground_clock += dt
                if self.leave_ground_clock >= self.HORIZONTAL_FORWARD_INTERPOLATE_DURATION:
                    self.leaving_ground = False
                    self.leave_ground_clock = self.HORIZONTAL_FORWARD_INTERPOLATE_DURATION
                v.intrp(self.ev_g_forward(), cam_forward, self.leave_ground_clock / self.HORIZONTAL_FORWARD_INTERPOLATE_DURATION)
            else:
                v = cam_forward
                self.send_event('E_ANIM_RATE', character_anim_const.LOW_BODY, cur_speed / cur_walk_speed * self.dynamic_speed_rate)
        else:
            cam_forward.y = 0
            cam_forward.normalize()
            v.intrp(self.ev_g_forward(), cam_forward, 1 - cur_speed / max_speed)
        self.send_event('E_FORWARD', v, True)
        return


def exit_flight_float(self, *args):
    self.send_event('E_FORBID_ROTATION', False)
    self.send_event('E_ENABLE_INJECT_BRAKE_MOVE', True)


def destroy_flight_float(self, *args):
    if self.air_walk_direction_setter:
        self.air_walk_direction_setter.destroy()
        self.air_walk_direction_setter = None
    return


init_func = {NORMAL_MOVE: empty_func,
   FLIGHT_FLOAT: init_flight_float,
   SKATE_MOVE: empty_func
   }
enter_func = {NORMAL_MOVE: enter_normal_move,
   FLIGHT_FLOAT: enter_flight_float,
   SKATE_MOVE: enter_normal_move
   }
move_func = {NORMAL_MOVE: normal_move_logic,
   FLIGHT_FLOAT: flight_float_logic,
   SKATE_MOVE: skate_move_logic
   }
exit_func = {NORMAL_MOVE: empty_func,
   FLIGHT_FLOAT: exit_flight_float,
   SKATE_MOVE: empty_func
   }
destroy_func = {NORMAL_MOVE: empty_func,
   FLIGHT_FLOAT: destroy_flight_float,
   SKATE_MOVE: empty_func
   }
SKATE_ROCK_FAST_SPEED_MAX_YAW = math.radians(30)
SKATE_ROCK_MEDIUM_SPEED_MAX_YAW = math.radians(150)

def skip_when_can_not_move(fail_ret=None):

    def decorator_gen(func):

        def wrapped(*args, **kwargs):
            if not can_move():
                return fail_ret
            return func(*args, **kwargs)

        return wrapped

    return decorator_gen


def can_move():
    if global_data.game_mode:
        from logic.client.const import game_mode_const
        if global_data.game_mode.is_mode_type(game_mode_const.GAME_MODE_WHAT):
            if global_data.improvise_battle_data and not global_data.improvise_battle_data.is_operable():
                return False
            if global_data.armrace_battle_data and not global_data.armrace_battle_data.is_operable():
                return False
    if global_data.battle and hasattr(global_data.battle, 'can_move'):
        return global_data.battle.can_move()
    return True


def can_roll():
    if global_data.game_mode:
        from logic.client.const import game_mode_const
        if global_data.game_mode.is_mode_type(game_mode_const.GAME_MODE_WHAT):
            if global_data.improvise_battle_data and not global_data.improvise_battle_data.is_operable():
                return False
            if global_data.armrace_battle_data and not global_data.armrace_battle_data.is_operable():
                return False
    if global_data.battle and hasattr(global_data.battle, 'can_roll'):
        return global_data.battle.can_roll()
    return True


def get_skate_move_speed_key(self):
    if not self.ev_g_get_state(status_config.ST_SKATE):
        return
    spd_key = ''
    if self.ev_g_is_in_any_state((status_config.ST_SKATE_MOVE, status_config.ST_SKATE_BRAKE)):
        spd_key = 'skate_run_lr'
        if self.ev_g_get_state(status_config.ST_AIM):
            spd_key = 'skate_move_aim'
        elif self.ev_g_get_state(status_config.ST_SHOOT) or self.ev_g_action_is_shoot():
            spd_key = 'skate_move_fire'
        else:
            is_reload = self.ev_g_is_in_any_state((status_config.ST_RELOAD, status_config.ST_RELOAD_LOOP))
            walk_direction = self.sd.ref_rocker_dir
            if not walk_direction:
                walk_direction = self.ev_g_get_walk_direction()
            yaw = abs(walk_direction.yaw)
            if yaw <= SKATE_ROCK_FAST_SPEED_MAX_YAW:
                spd_key = is_reload and 'skate_move_reload_f' or 'skate_run_f'
            elif yaw <= SKATE_ROCK_MEDIUM_SPEED_MAX_YAW:
                spd_key = is_reload and 'skate_move_reload_lr' or 'skate_run_lr'
            else:
                spd_key = is_reload and 'skate_move_reload_b' or 'skate_run_b'
    return spd_key


def get_human_speed--- This code section failed: ---

 356       0  LOAD_CONST            1  ''
           3  STORE_FAST            1  'value'

 357       6  LOAD_CONST            0  ''
           9  STORE_FAST            2  'spd_key'

 358      12  LOAD_CONST            2  1
          15  STORE_FAST            3  'speed_scale_by_land_type'

 359      18  LOAD_CONST            2  1
          21  STORE_FAST            4  'speed_scale_by_rocker_type'

 360      24  LOAD_FAST             0  'self'
          27  LOAD_ATTR             1  'ev_g_is_jump'
          30  CALL_FUNCTION_0       0 
          33  POP_JUMP_IF_TRUE    105  'to 105'

 361      36  LOAD_FAST             0  'self'
          39  LOAD_ATTR             2  'sd'
          42  LOAD_ATTR             3  'ref_water_status'
          45  STORE_FAST            5  'water_status'

 362      48  LOAD_FAST             5  'water_status'
          51  LOAD_GLOBAL           4  'water_const'
          54  LOAD_ATTR             5  'WATER_SHWLLOW_LEVEL2'
          57  COMPARE_OP            2  '=='
          60  POP_JUMP_IF_FALSE    75  'to 75'

 363      63  LOAD_GLOBAL           6  'speed_physic_arg'
          66  LOAD_ATTR             7  'qian_ceng_speed_scale'
          69  STORE_FAST            3  'speed_scale_by_land_type'
          72  JUMP_ABSOLUTE       105  'to 105'

 364      75  LOAD_FAST             5  'water_status'
          78  LOAD_GLOBAL           4  'water_const'
          81  LOAD_ATTR             8  'WATER_MID_LEVEL'
          84  COMPARE_OP            2  '=='
          87  POP_JUMP_IF_FALSE   105  'to 105'

 365      90  LOAD_GLOBAL           6  'speed_physic_arg'
          93  LOAD_ATTR             9  'zhong_ceng_speed_scale'
          96  STORE_FAST            3  'speed_scale_by_land_type'
          99  JUMP_ABSOLUTE       105  'to 105'
         102  JUMP_FORWARD          0  'to 105'
       105_0  COME_FROM                '102'

 368     105  LOAD_FAST             0  'self'
         108  LOAD_ATTR            10  'ev_g_get_state'
         111  LOAD_GLOBAL          11  'status_config'
         114  LOAD_ATTR            12  'ST_DOWN'
         117  CALL_FUNCTION_1       1 
         120  POP_JUMP_IF_FALSE   132  'to 132'

 369     123  LOAD_CONST            3  'down_walk'
         126  STORE_FAST            2  'spd_key'
         129  JUMP_FORWARD        447  'to 579'

 370     132  LOAD_FAST             0  'self'
         135  LOAD_ATTR            10  'ev_g_get_state'
         138  LOAD_GLOBAL          11  'status_config'
         141  LOAD_ATTR            13  'ST_SKATE'
         144  CALL_FUNCTION_1       1 
         147  POP_JUMP_IF_FALSE   207  'to 207'

 371     150  LOAD_GLOBAL          14  'get_skate_move_speed_key'
         153  LOAD_FAST             0  'self'
         156  CALL_FUNCTION_1       1 
         159  STORE_FAST            2  'spd_key'

 372     162  LOAD_FAST             2  'spd_key'
         165  POP_JUMP_IF_TRUE    177  'to 177'

 373     168  LOAD_CONST            1  ''
         171  STORE_FAST            1  'value'
         174  JUMP_FORWARD          0  'to 177'
       177_0  COME_FROM                '174'

 374     177  LOAD_FAST             0  'self'
         180  LOAD_ATTR             2  'sd'
         183  LOAD_ATTR            15  'ref_rocker_run_state'
         186  POP_JUMP_IF_FALSE   195  'to 195'
         189  LOAD_CONST            4  1.0
         192  JUMP_FORWARD          6  'to 201'
         195  LOAD_GLOBAL           6  'speed_physic_arg'
         198  LOAD_ATTR            16  'skate_slow_rate'
       201_0  COME_FROM                '192'
         201  STORE_FAST            4  'speed_scale_by_rocker_type'
         204  JUMP_FORWARD        372  'to 579'

 375     207  LOAD_FAST             0  'self'
         210  LOAD_ATTR            10  'ev_g_get_state'
         213  LOAD_GLOBAL          11  'status_config'
         216  LOAD_ATTR            17  'ST_MOVE'
         219  CALL_FUNCTION_1       1 
         222  POP_JUMP_IF_FALSE   274  'to 274'

 376     225  LOAD_FAST             0  'self'
         228  LOAD_ATTR            18  'ev_g_action_is_shoot'
         231  CALL_FUNCTION_0       0 
         234  POP_JUMP_IF_FALSE   265  'to 265'
         237  LOAD_FAST             0  'self'
         240  LOAD_ATTR            10  'ev_g_get_state'
         243  LOAD_GLOBAL          11  'status_config'
         246  LOAD_ATTR            19  'ST_SHOOT'
         249  CALL_FUNCTION_1       1 
         252  UNARY_NOT        
       253_0  COME_FROM                '234'
         253  POP_JUMP_IF_FALSE   265  'to 265'

 378     256  LOAD_CONST            5  'have_gun_shoot'
         259  STORE_FAST            2  'spd_key'
         262  JUMP_ABSOLUTE       579  'to 579'

 381     265  LOAD_CONST            6  'have_gun_walk'
         268  STORE_FAST            2  'spd_key'
         271  JUMP_FORWARD        305  'to 579'

 382     274  LOAD_FAST             0  'self'
         277  LOAD_ATTR            10  'ev_g_get_state'
         280  LOAD_GLOBAL          11  'status_config'
         283  LOAD_ATTR            20  'ST_RUN'
         286  CALL_FUNCTION_1       1 
         289  POP_JUMP_IF_FALSE   337  'to 337'

 383     292  LOAD_FAST             0  'self'
         295  LOAD_ATTR            21  'ev_g_move_stage'
         298  CALL_FUNCTION_0       0 
         301  STORE_FAST            6  'move_stage'

 384     304  LOAD_FAST             6  'move_stage'
         307  LOAD_GLOBAL          22  'animation_const'
         310  LOAD_ATTR            23  'RUN_FIRST_STAGE'
         313  COMPARE_OP            2  '=='
         316  POP_JUMP_IF_FALSE   328  'to 328'

 385     319  LOAD_CONST            6  'have_gun_walk'
         322  STORE_FAST            2  'spd_key'
         325  JUMP_ABSOLUTE       579  'to 579'

 387     328  LOAD_CONST            7  'have_gun_run'
         331  STORE_FAST            2  'spd_key'
         334  JUMP_FORWARD        242  'to 579'

 388     337  LOAD_FAST             0  'self'
         340  LOAD_ATTR            10  'ev_g_get_state'
         343  LOAD_GLOBAL          11  'status_config'
         346  LOAD_ATTR            24  'ST_CROUCH_MOVE'
         349  CALL_FUNCTION_1       1 
         352  POP_JUMP_IF_FALSE   404  'to 404'

 389     355  LOAD_FAST             0  'self'
         358  LOAD_ATTR            18  'ev_g_action_is_shoot'
         361  CALL_FUNCTION_0       0 
         364  POP_JUMP_IF_FALSE   395  'to 395'
         367  LOAD_FAST             0  'self'
         370  LOAD_ATTR            10  'ev_g_get_state'
         373  LOAD_GLOBAL          11  'status_config'
         376  LOAD_ATTR            19  'ST_SHOOT'
         379  CALL_FUNCTION_1       1 
         382  UNARY_NOT        
       383_0  COME_FROM                '364'
         383  POP_JUMP_IF_FALSE   395  'to 395'

 391     386  LOAD_CONST            8  'squat_shoot'
         389  STORE_FAST            2  'spd_key'
         392  JUMP_ABSOLUTE       579  'to 579'

 394     395  LOAD_CONST            9  'squat_walk'
         398  STORE_FAST            2  'spd_key'
         401  JUMP_FORWARD        175  'to 579'

 395     404  LOAD_FAST             0  'self'
         407  LOAD_ATTR            10  'ev_g_get_state'
         410  LOAD_GLOBAL          11  'status_config'
         413  LOAD_ATTR            25  'ST_CROUCH_RUN'
         416  CALL_FUNCTION_1       1 
         419  POP_JUMP_IF_FALSE   431  'to 431'

 396     422  LOAD_CONST           10  'squat_run'
         425  STORE_FAST            2  'spd_key'
         428  JUMP_FORWARD        148  'to 579'

 397     431  LOAD_FAST             0  'self'
         434  LOAD_ATTR             1  'ev_g_is_jump'
         437  CALL_FUNCTION_0       0 
         440  POP_JUMP_IF_FALSE   540  'to 540'

 399     443  LOAD_FAST             0  'self'
         446  LOAD_ATTR            26  'ev_g_is_multiple_jump'
         449  CALL_FUNCTION_0       0 
         452  POP_JUMP_IF_FALSE   471  'to 471'

 402     455  LOAD_GLOBAL          27  'jump_physic_config'
         458  LOAD_ATTR            28  'double_jump_speed_horizontal'
         461  LOAD_GLOBAL          29  'NEOX_UNIT_SCALE'
         464  BINARY_MULTIPLY  
         465  STORE_FAST            1  'value'
         468  JUMP_ABSOLUTE       579  'to 579'

 405     471  LOAD_FAST             0  'self'
         474  LOAD_ATTR            30  'ev_g_move_state_before_jump'
         477  CALL_FUNCTION_0       0 
         480  STORE_FAST            7  'move_state_before_jump'

 406     483  LOAD_FAST             7  'move_state_before_jump'
         486  LOAD_GLOBAL          11  'status_config'
         489  LOAD_ATTR            17  'ST_MOVE'
         492  COMPARE_OP            2  '=='
         495  POP_JUMP_IF_FALSE   507  'to 507'

 407     498  LOAD_CONST           11  'walk_then_jump'
         501  STORE_FAST            2  'spd_key'
         504  JUMP_ABSOLUTE       579  'to 579'

 408     507  LOAD_FAST             7  'move_state_before_jump'
         510  LOAD_GLOBAL          11  'status_config'
         513  LOAD_ATTR            20  'ST_RUN'
         516  COMPARE_OP            2  '=='
         519  POP_JUMP_IF_FALSE   531  'to 531'

 409     522  LOAD_CONST           12  'run_then_jump'
         525  STORE_FAST            2  'spd_key'
         528  JUMP_ABSOLUTE       579  'to 579'

 411     531  LOAD_CONST           13  'stand_then_jump'
         534  STORE_FAST            2  'spd_key'
         537  JUMP_FORWARD         39  'to 579'

 412     540  LOAD_FAST             0  'self'
         543  LOAD_ATTR            10  'ev_g_get_state'
         546  LOAD_GLOBAL          11  'status_config'
         549  LOAD_ATTR            31  'ST_SWIM'
         552  CALL_FUNCTION_1       1 
         555  POP_JUMP_IF_FALSE   567  'to 567'

 413     558  LOAD_CONST           14  'swim_run'
         561  STORE_FAST            2  'spd_key'
         564  JUMP_FORWARD         12  'to 579'

 416     567  LOAD_CONST           15  1.5
         570  STORE_FAST            1  'value'

 417     573  LOAD_CONST           16  'empty_hand_walk'
         576  STORE_FAST            2  'spd_key'
       579_0  COME_FROM                '564'
       579_1  COME_FROM                '537'
       579_2  COME_FROM                '428'
       579_3  COME_FROM                '401'
       579_4  COME_FROM                '334'
       579_5  COME_FROM                '271'
       579_6  COME_FROM                '204'
       579_7  COME_FROM                '129'

 419     579  LOAD_FAST             2  'spd_key'
         582  POP_JUMP_IF_FALSE   669  'to 669'

 420     585  LOAD_GLOBAL          32  'getattr'
         588  LOAD_FAST             0  'self'
         591  LOAD_FAST             2  'spd_key'
         594  LOAD_CONST            1  ''
         597  CALL_FUNCTION_3       3 
         600  STORE_FAST            1  'value'

 421     603  LOAD_FAST             0  'self'
         606  LOAD_ATTR            33  'ev_g_filter_spd'
         609  LOAD_FAST             2  'spd_key'
         612  LOAD_FAST             1  'value'
         615  CALL_FUNCTION_2       2 
         618  STORE_FAST            8  'ret'

 422     621  LOAD_FAST             8  'ret'
         624  LOAD_CONST            0  ''
         627  COMPARE_OP            9  'is-not'
         630  POP_JUMP_IF_FALSE   642  'to 642'

 423     633  LOAD_FAST             8  'ret'
         636  STORE_FAST            1  'value'
         639  JUMP_ABSOLUTE       669  'to 669'

 428     642  LOAD_FAST             1  'value'
         645  POP_JUMP_IF_TRUE    669  'to 669'

 429     648  LOAD_GLOBAL          32  'getattr'
         651  LOAD_GLOBAL           6  'speed_physic_arg'
         654  LOAD_FAST             2  'spd_key'
         657  CALL_FUNCTION_2       2 
         660  STORE_FAST            1  'value'
         663  JUMP_ABSOLUTE       669  'to 669'
         666  JUMP_FORWARD          0  'to 669'
       669_0  COME_FROM                '666'

 431     669  LOAD_FAST             0  'self'
         672  LOAD_ATTR            34  'ev_g_get_speed_scale'
         675  CALL_FUNCTION_0       0 
         678  STORE_FAST            9  'speed_scale'

 432     681  LOAD_FAST             1  'value'
         684  LOAD_FAST             3  'speed_scale_by_land_type'
         687  BINARY_MULTIPLY  
         688  LOAD_GLOBAL          32  'getattr'
         691  LOAD_GLOBAL          17  'ST_MOVE'
         694  LOAD_CONST            2  1
         697  CALL_FUNCTION_3       3 
         700  BINARY_MULTIPLY  
         701  LOAD_FAST             9  'speed_scale'
         704  BINARY_MULTIPLY  
         705  LOAD_FAST             4  'speed_scale_by_rocker_type'
         708  BINARY_MULTIPLY  
         709  STORE_FAST           10  'speed'

 433     712  LOAD_FAST            10  'speed'
         715  RETURN_VALUE     

Parse error at or near `BINARY_MULTIPLY' instruction at offset 700