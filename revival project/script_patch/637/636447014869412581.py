# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/behavior/Logic8012.py
from __future__ import absolute_import
import math3d
import world
import time
from math import sin, cos, radians, pi
from .StateBase import StateBase
from .ShootLogic import WeaponFire
from logic.gcommon.cdata.mecha_status_config import *
from logic.gcommon.common_const.character_anim_const import *
from logic.gcommon.const import NEOX_UNIT_SCALE
import logic.gcommon.common_utils.bcast_utils as bcast
from logic.gutils import mecha_utils
from logic.gutils.client_unit_tag_utils import register_unit_tag, preregistered_tags
from common.utils.timer import RELEASE
import logic.gcommon.const as g_const
from logic.gcommon import editor
from logic.gcommon.common_const import ui_operation_const as uoc
from common.cfg import confmgr
from logic.gcommon.component.client.com_mecha_appearance.ComBallDriver import BALL_RADIUS
from logic.gutils.collision_test_utils import CollisionTester
from logic.gutils.sound_utils import play_hit_sound_2d
import collision
from logic.gcommon.common_const.collision_const import GROUP_CAMERA_COLL, GROUP_DYNAMIC_SHOOTUNIT, GROUP_STATIC_SHOOTUNIT
MECHA_VEHICLE_MONSTER_TAG_VALUE = register_unit_tag(('LMecha', 'LMechaRobot', 'LMechaTrans', 'LMotorcycle', 'LMonster'))

def __editor_dash8012_setter(self, v):
    self.init_move_speed = v * NEOX_UNIT_SCALE
    self.refresh_move_speed()


@editor.state_exporter({('skill_id', 'param'): {'zh_name': '\xe6\x8a\x80\xe8\x83\xbdid'},('attack_skill_id', 'param'): {'zh_name': '\xe5\x86\xb2\xe6\x92\x9e\xe6\x8a\x80\xe8\x83\xbdid'},('trans_to_ball_time', 'param'): {'zh_name': '\xe5\x8f\x98\xe7\x90\x83\xe6\x97\xb6\xe9\x97\xb4'},('trans_to_human_fall_time', 'param'): {'zh_name': '\xe5\x8f\x98\xe4\xba\xba\xe6\x8f\x90\xe5\x89\x8d\xe6\x89\x93\xe6\x96\xad\xe6\x97\xb6\xe9\x97\xb4'},('trans_to_human_time', 'param'): {'zh_name': '\xe5\x8f\x98\xe4\xba\xba\xe5\x8a\xa8\xe4\xbd\x9c\xe6\x80\xbb\xe6\x97\xb6\xe9\x95\xbf'},('jump_speed', 'meter'): {'zh_name': '\xe7\x90\x83\xe5\xbd\xa2\xe6\x80\x81\xe8\xb7\xb3\xe8\xb7\x83\xe9\x80\x9f\xe5\xba\xa6','min_val': 20,'max_val': 100},('super_jump_speed', 'meter'): {'zh_name': '\xe7\x90\x83\xe5\xbd\xa2\xe6\x80\x81\xe8\xb6\x85\xe7\xba\xa7\xe8\xb7\xb3\xe9\x80\x9f\xe5\xba\xa6','explain': '\xe7\x90\x83\xe5\xbd\xa2\xe6\x80\x81\xe5\x8f\x97\xe5\x88\xb0\xe5\xbc\xb9\xe8\xb7\xb3\xe5\x8f\xb0\xe4\xbd\x9c\xe7\x94\xa8\xe6\x97\xb6\xe8\xb7\xb3\xe8\xb7\x83\xe5\xa2\x9e\xe5\xbc\xba\xe7\xb3\xbb\xe6\x95\xb0'},('beat_back_v_speed', 'meter'): {'zh_name': '\xe7\x90\x83\xe5\xbd\xa2\xe6\x80\x81\xe8\xa2\xab\xe5\x87\xbb\xe9\x80\x80\xe5\x9e\x82\xe7\x9b\xb4\xe9\x80\x9f\xe5\xba\xa6'},('beat_back_h_speed', 'meter'): {'zh_name': '\xe7\x90\x83\xe5\xbd\xa2\xe6\x80\x81\xe8\xa2\xab\xe5\x87\xbb\xe9\x80\x80\xe6\xb0\xb4\xe5\xb9\xb3\xe9\x80\x9f\xe5\xba\xa6'},('jump_gravity', 'meter'): {'zh_name': '\xe8\xb7\xb3\xe8\xb7\x83\xe6\x97\xb6\xe9\x87\x8d\xe5\x8a\x9b(\xe9\x9c\x80\xe9\x87\x8d\xe6\x96\xb0\xe5\x8f\x98\xe5\xbd\xa2\xe7\x94\x9f\xe6\x95\x88)','min_val': 20,'max_val': 200},('super_jump_gravity', 'meter'): {'zh_name': '\xe7\x90\x83\xe5\xbd\xa2\xe6\x80\x81\xe8\xb6\x85\xe7\xba\xa7\xe8\xb7\xb3\xe9\x87\x8d\xe5\x8a\x9b'},('fall_gravity', 'meter'): {'zh_name': '\xe4\xb8\x8b\xe8\x90\xbd\xe6\x97\xb6\xe9\x87\x8d\xe5\x8a\x9b(\xe9\x9c\x80\xe9\x87\x8d\xe6\x96\xb0\xe5\x8f\x98\xe5\xbd\xa2\xe7\x94\x9f\xe6\x95\x88)','min_val': 20,'max_val': 200},('damage_speed', 'meter'): {'zh_name': '\xe6\x94\xbb\xe5\x87\xbb\xe9\x80\x9f\xe5\xba\xa6','min_val': 0,'max_val': 30,'explain': '\xe7\x90\x83\xe5\xbd\xa2\xe6\x80\x81\xe8\x83\xbd\xe5\xa4\x9f\xe9\x80\xa0\xe6\x88\x90\xe4\xbc\xa4\xe5\xae\xb3\xe7\x9a\x84\xe6\x9c\x80\xe5\xb0\x8f\xe9\x80\x9f\xe5\xba\xa6'},('damage_interval', 'param'): {'zh_name': '\xe6\x94\xbb\xe5\x87\xbb\xe9\x97\xb4\xe9\x9a\x94'},('move_speed', 'param'): {'zh_name': '\xe7\xa7\xbb\xe5\x8a\xa8\xe9\x80\x9f\xe5\xba\xa6','min_val': 0,'max_val': 30,'getter': --- This code section failed: ---

  52       0  LOAD_GLOBAL           0  'getattr'
           3  LOAD_GLOBAL           1  'NEOX_UNIT_SCALE'
           6  CALL_FUNCTION_2       2 
           9  LOAD_GLOBAL           1  'NEOX_UNIT_SCALE'
          12  BINARY_DIVIDE    
          13  RETURN_VALUE_LAMBDA
          -1  LAMBDA_MARKER    

Parse error at or near `CALL_FUNCTION_2' instruction at offset 6
,'setter': lambda self, v: __editor_dash8012_setter(self, v)
                             },
   ('acc_speed', 'meter'): {'zh_name': '\xe7\x90\x83\xe5\xbd\xa2\xe6\x80\x81\xe5\x8a\xa0\xe9\x80\x9f\xe5\xba\xa6','min_val': 0,'max_val': 100},('air_acc_coe', 'param'): {'zh_name': '\xe7\xa9\xba\xe4\xb8\xad\xe7\xa7\xbb\xe5\x8a\xa8\xe9\x80\x9f\xe5\xba\xa6\xe6\xaf\x94\xe4\xbe\x8b'},('rebound_h_speed', 'meter'): {'zh_name': '\xe6\x92\x9e\xe5\x87\xbb\xe5\x9b\x9e\xe5\xbc\xb9\xe6\xb0\xb4\xe5\xb9\xb3\xe9\x80\x9f\xe5\xba\xa6'},('rebound_v_speed', 'meter'): {'zh_name': '\xe6\x92\x9e\xe5\x87\xbb\xe5\x9b\x9e\xe5\xbc\xb9\xe5\x9e\x82\xe7\x9b\xb4\xe9\x80\x9f\xe5\xba\xa6'},('jump_cam_follow_speed', 'param'): {'zh_name': '\xe8\xb7\xb3\xe8\xb7\x83\xe6\x97\xb6\xe7\x9b\xb8\xe6\x9c\xba\xe8\xb7\x9f\xe9\x9a\x8f\xe9\x80\x9f\xe5\xba\xa6','min_val': 0,'max_val': 1},('jump_cam_recover_delay', 'param'): {'zh_name': '\xe8\xb7\xb3\xe8\xb7\x83\xe6\x97\xb6\xe7\x9b\xb8\xe6\x9c\xba\xe8\xb7\x9f\xe9\x9a\x8f\xe8\xbf\x9f\xe6\xbb\x9e'},('jump_cam_recover_time', 'param'): {'zh_name': '\xe8\xb7\xb3\xe8\xb7\x83\xe6\x97\xb6\xe7\x9b\xb8\xe6\x9c\xba\xe6\x81\xa2\xe5\xa4\x8d\xe6\x97\xb6\xe9\x97\xb4'},('super_jump_cam_follow_speed', 'param'): {'zh_name': '\xe5\xbc\xb9\xe8\xb7\xb3\xe5\x8f\xb0\xe8\xb7\xb3\xe8\xb7\x83\xe6\x97\xb6\xe7\x9b\xb8\xe6\x9c\xba\xe8\xb7\x9f\xe9\x9a\x8f\xe9\x80\x9f\xe5\xba\xa6','min_val': 0,'max_val': 1},('super_jump_cam_recover_delay', 'param'): {'zh_name': '\xe5\xbc\xb9\xe8\xb7\xb3\xe5\x8f\xb0\xe8\xb6\x85\xe7\xba\xa7\xe8\xb7\xb3\xe8\xb7\x83\xe6\x97\xb6\xe7\x9b\xb8\xe6\x9c\xba\xe8\xb7\x9f\xe9\x9a\x8f\xe8\xbf\x9f\xe6\xbb\x9e'},('super_jump_cam_recover_time', 'param'): {'zh_name': '\xe5\xbc\xb9\xe8\xb7\xb3\xe5\x8f\xb0\xe8\xb7\xb3\xe8\xb7\x83\xe6\x97\xb6\xe7\x9b\xb8\xe6\x9c\xba\xe6\x81\xa2\xe5\xa4\x8d\xe6\x97\xb6\xe9\x97\xb4'}})
class Dash8012(StateBase):
    SUB_ST_TO_BALL = 1
    SUB_ST_BALL = 2
    SUB_ST_TO_HUMAN = 3
    BIND_EVENT = {'E_SUPER_JUMP': 'super_jump',
       'E_RUSH_HIT_TARGET': 'on_hit_target',
       'E_RUSH_HIT_HUMAN': 'on_hit_human',
       'E_TRANS_TO_BALL': 'on_trans_to_ball',
       'E_TRANS_TO_HUMAN': 'on_trans_to_human',
       'E_BALL_OVERLOAD_START': 'on_overload',
       'E_BALL_OVERLOAD_STOP': 'on_overload_stop',
       'E_BEAT_BACK': 'on_beat_back',
       'E_BALL_IS_DASH': 'on_ball_dash',
       'G_LEAVE_MECHA_IN_BALL': 'on_leave_mecha_in_ball',
       'E_SKILL_FUEL_EXHAUSTED': 'on_fuel_exhausted',
       'G_TRY_EXIT_BALL_STATE': 'try_exit_ball_state',
       'E_SET_SPEED_SCALE': 'on_set_speed_scale'
       }

    def init_from_dict(self, unit_obj, bdict, sid, info):
        super(Dash8012, self).init_from_dict(unit_obj, bdict, sid, info)
        self.skill_id = self.custom_param.get('skill_id')
        self.attack_skill_id = self.custom_param.get('attack_skill_id')
        self.jump_skill_id = self.custom_param.get('jump_skill_id')
        self.trans_to_ball_anim = self.custom_param.get('trans_to_ball_anim', 'dash_f')
        self.ball_anim = self.custom_param.get('ball_anim', 'roll_stand')
        self.trans_back_anim = self.custom_param.get('trans_back_anim', 'trans_back')
        self.trans_to_ball_time = self.custom_param.get('trans_to_ball_time', 0.7)
        self.trans_to_human_fall_time = self.custom_param.get('trans_to_human_fall_time', 0.4)
        self.trans_to_human_brake_time = self.custom_param.get('trans_to_human_brake_time', 0.7)
        self.trans_to_human_time = self.custom_param.get('trans_to_human_time', 2.1)
        self.jump_speed = self.custom_param.get('jump_speed', 200) * NEOX_UNIT_SCALE
        self.super_jump_speed = self.custom_param.get('super_jump_speed', 64) * NEOX_UNIT_SCALE
        self.beat_back_v_speed = self.custom_param.get('beat_back_v_speed', 200) * NEOX_UNIT_SCALE
        self.beat_back_h_speed = self.custom_param.get('beat_back_h_speed', 200) * NEOX_UNIT_SCALE
        self.jump_gravity = self.custom_param.get('jump_gravity', 50) * NEOX_UNIT_SCALE
        self.super_jump_gravity = self.custom_param.get('super_jump_gravity', 40) * NEOX_UNIT_SCALE
        self.fall_gravity = self.custom_param.get('fall_gravity', 100) * NEOX_UNIT_SCALE
        self.damage_speed = self.custom_param.get('damage_speed', 15) * NEOX_UNIT_SCALE
        self.damage_interval = self.custom_param.get('damage_interval', 2)
        self.move_speed = self.custom_param['move_speed'] * NEOX_UNIT_SCALE
        self.init_move_speed = self.move_speed
        self.acc_speed = self.custom_param['acc_speed'] * NEOX_UNIT_SCALE
        self.air_acc_coe = self.custom_param['air_acc_coe']
        self.rebound_h_speed = self.custom_param.get('rebound_h_speed', 30) * NEOX_UNIT_SCALE
        self.rebound_v_speed = self.custom_param.get('rebound_v_speed', 10) * NEOX_UNIT_SCALE
        self.jump_cam_follow_speed = self.custom_param.get('jump_cam_follow_speed', 0.5)
        self.jump_cam_recover_delay = self.custom_param.get('jump_cam_recover_delay', 0.3)
        self.jump_cam_recover_time = self.custom_param.get('jump_cam_recover_time', 0.5)
        self.super_jump_cam_follow_speed = self.custom_param.get('super_jump_cam_follow_speed', 0.5)
        self.super_jump_cam_recover_delay = self.custom_param.get('super_jump_cam_recover_delay', 0.3)
        self.super_jump_cam_recover_time = self.custom_param.get('super_jump_cam_recover_time', 0.5)
        self.sub_state = -1
        self.register_substate_callback(self.SUB_ST_TO_BALL, 0, self.begin_trans_to_ball)
        self.register_substate_callback(self.SUB_ST_TO_BALL, self.trans_to_ball_time, self.trans_to_ball)
        self.register_substate_callback(self.SUB_ST_TO_HUMAN, 0, self.begin_trans_to_human)
        self.register_substate_callback(self.SUB_ST_TO_HUMAN, self.trans_to_human_fall_time, self.trans_to_human_in_air)
        self.register_substate_callback(self.SUB_ST_TO_HUMAN, self.trans_to_human_brake_time, self.trans_to_human_brake)
        self.register_substate_callback(self.SUB_ST_TO_HUMAN, self.trans_to_human_time, self.trans_to_human)
        self.can_brake = False
        self.trans_back_finished = False
        self.last_jump_input = False
        self.last_dash_input = False
        self.first_trans = True
        self.leave_mecha_in_ball = False
        self.is_overloading = False
        self.last_detect_time = 0
        self.hit_targets = {}
        self.move_speed_add_factor = 0.0
        self.sphere_flamethrower_enabled = False
        self.enable_param_changed_by_buff()
        self.ball_is_dash = False
        self.dash_can_damage = False
        self.is_ball_driver = False
        self.left_time = 0
        self.move_timer = 0
        self.need_trans_to_human = False
        self.block_trans_to_human_failed_msg = -1
        self.speed_scale = 1.0
        self.is_pve = global_data.game_mode.is_pve()
        if self.is_pve:
            self.pve_fire_field_skill_id = 801259
            skill_conf = confmgr.get('skill_conf', str(self.pve_fire_field_skill_id), default={})
            skill_ext_info = skill_conf.get('ext_info', {})
            field_id = skill_conf.get('field_id', None)
            field_conf = confmgr.get('field_data', str(field_id), default={})
            self.field_create_inter = field_conf.get('fTime', 4) * skill_ext_info.get('field_create_inter_rate', 1.0)
            self.field_create_dist = field_conf.get('fRange', 10) * skill_ext_info.get('field_create_dist_rate', 1.0) * NEOX_UNIT_SCALE
            self.last_field_info = None
        self.pve_ball_dash_enhance_radius = 0
        self.pve_bump_speed_add_rate = 0
        self.pve_bump_speed_add_max_layer = 0
        self.pve_bump_speed_add_duration = 0
        self.pve_bump_speed_add_layer = 0
        self.pve_bump_speed_add_timer = 0.0
        return

    def on_ball_dash(self, is_dash, dash_can_damage):
        self.ball_is_dash = is_dash
        self.dash_can_damage = dash_can_damage

    def on_set_speed_scale(self, speed_scale):
        self.speed_scale = speed_scale
        self.refresh_move_speed()

    def refresh_param_changed(self):
        self.refresh_move_speed()
        if self.is_active:
            if self.sphere_flamethrower_enabled:
                self.send_event('E_CLEAR_BLACK_STATE')
                self.send_event('E_SET_ACTION_ICON', 'action4', 'gui/ui_res_2/battle/mech_main/icon_mech8012_2_2.png', 'show')
            else:
                self.send_event('E_SET_ACTION_ICON', 'action4', 'gui/ui_res_2/battle/mech_main/icon_mech8012_2.png', 'show')

    def refresh_move_speed(self):
        speed_add_factor = self.speed_scale + self.move_speed_add_factor
        if self.is_pve and self.pve_bump_speed_add_layer > 0 and self.pve_bump_speed_add_rate > 0:
            speed_add_factor += self.pve_bump_speed_add_rate * self.pve_bump_speed_add_layer
        self.move_speed = self.init_move_speed * speed_add_factor
        if self.sd.ref_is_ball_mode:
            self.send_event('E_SET_BALL_MOVE_SPEED', self.move_speed)

    def begin_trans_to_ball(self):
        rocker_dir = self.sd.ref_rocker_dir
        dir_sufix = ''
        forward = self.ev_g_forward()
        right = math3d.vector(0, 1, 0).cross(forward)
        dir_vec = forward
        speed = 0
        if rocker_dir and not rocker_dir.is_zero:
            if abs(rocker_dir.z) < 0.001:
                if rocker_dir.x < 0:
                    dir_sufix = '_l'
                    dir_vec = -right
                elif rocker_dir.x > 0:
                    dir_sufix = '_r'
                    dir_vec = right
                speed = 22 * NEOX_UNIT_SCALE * 0.7
            else:
                if rocker_dir.z > 0:
                    dir_sufix = '_f'
                    flag = 1
                    speed = 22.25 * NEOX_UNIT_SCALE * 0.7
                else:
                    dir_sufix = '_b'
                    flag = -1
                    speed = 18.75 * NEOX_UNIT_SCALE * 0.7
                dir_vec = forward * abs(rocker_dir.z) + right * flag * rocker_dir.x
                dir_vec.normalize()
        dir_vec = -dir_vec if dir_sufix == '_b' else dir_vec
        self.send_event('E_SET_WALK_DIRECTION', dir_vec * speed)
        anim = 'dash' + dir_sufix if dir_sufix != '' else 'transform'
        self.send_event('E_ANIM_RATE', LOW_BODY, 1.0)
        self.send_event('E_POST_ACTION', anim, LOW_BODY, 1, loop=False)
        self.send_event('E_ACTIVE_BALL_DRIVER', self.fall_gravity, self.move_speed, self.acc_speed, self.air_acc_coe, self.damage_speed)

    def trans_to_ball(self):
        self.send_event('E_POST_ACTION', self.ball_anim, LOW_BODY, 1, loop=False, blend_time=0.0)
        if not self.sd.ref_is_ball_mode:
            self.send_event('E_ACTIVE_BALL_DRIVER', self.fall_gravity, self.move_speed, self.acc_speed, self.air_acc_coe, self.damage_speed)
        self.send_event('E_OX_BEGIN_RUSH')
        self.send_event('E_CLEAR_UP_BODY_ANIM')
        self.send_event('E_DISABLE_YAW_WITH_CAMREA', True)
        self.sub_state = self.SUB_ST_BALL
        self.is_ball_driver = True

    def begin_trans_to_human(self):
        self.trans_back_finished = False
        walk_direction = self.ev_g_char_walk_direction()
        if walk_direction.length > self.move_speed:
            move_dir = math3d.vector(walk_direction)
            move_dir.normalize()
            self.sd.ref_cur_speed = self.move_speed
            self.send_event('E_CHARACTER_WALK', move_dir * self.move_speed)
        self.recover_to_character()
        self.send_event('E_POST_ACTION', self.trans_back_anim, LOW_BODY, 1, loop=False)
        self.check_exit_state_camera()

    def trans_to_human_in_air(self):
        white_states = self._get_white_state_set(in_air=True)
        self.send_event('E_CLEAR_WHITE_STATE', self.sid)
        self.send_event('E_ADD_WHITE_STATE', white_states, self.sid)
        if self.ev_g_on_ground():
            self.send_event('E_LOGIC_ON_GROUND', self.ev_g_vertical_speed())
            if self.ev_g_is_in_lift():
                self.send_event('E_IGNORE_GRAVITY', True)
        else:
            self.send_event('E_FALL')

    def trans_to_human_brake(self):
        white_states = self._get_white_state_set(in_air=False)
        self.send_event('E_CLEAR_WHITE_STATE', self.sid)
        self.send_event('E_ADD_WHITE_STATE', white_states, self.sid)
        self.can_brake = True

    def _get_white_state_set(self, in_air=False):
        if self.ev_g_is_in_frozen():
            white_states = {
             MC_FROZEN}
        elif self.ev_g_immobilized():
            white_states = {
             MC_IMMOBILIZE}
        else:
            white_states = {MC_JUMP_2, MC_JUMP_3} if in_air else {MC_STAND, MC_JUMP_1, MC_SECOND_WEAPON_ATTACK, MC_SHOOT, MC_MOVE}
        return white_states

    def trans_to_human(self):
        self.trans_back_finished = True
        self.need_trans_to_human = False

    def on_fuel_exhausted(self, skill_id, *args):
        if str(skill_id) != str(self.skill_id):
            return
        if self.sub_state == self.SUB_ST_BALL:
            self.need_trans_to_human = True
            self.on_trans_to_human()

    def enter(self, leave_states):
        super(Dash8012, self).enter(leave_states)
        self.send_event('E_ENABLE_HELP_ANIM', False)
        if self.ev_g_on_ground():
            self.check_delay_camera_parameter()
        if self.sphere_flamethrower_enabled:
            self.send_event('E_SET_ACTION_ICON', 'action4', 'gui/ui_res_2/battle/mech_main/icon_mech8012_2_2.png', 'show')
            if MC_SECOND_WEAPON_ATTACK in leave_states:
                self.ev_g_need_auto_continue_second_weapon() and self.send_event('E_KEEP_TRYING_SECOND_WEAPON')
        else:
            self.send_event('E_ADD_BLACK_STATE', {MC_SECOND_WEAPON_ATTACK})
        self.hit_targets = {}
        self.send_event('E_SWITCH_ACTION', 'action1', MC_THUMP_RUSH, False)
        self.send_event('E_SWITCH_ACTION', 'action2', MC_THUMP_RUSH, False)
        self.send_event('E_SWITCH_ACTION', 'action3', MC_THUMP_RUSH, False)
        self.send_event('E_SET_ACTION_ICON', 'action1', 'gui/ui_res_2/battle/mech_main/icon_mech8012_3.png', 'show')
        self.send_event('E_SET_ACTION_ICON', 'action2', 'gui/ui_res_2/battle/mech_main/icon_mech8012_3.png', 'show')
        self.send_event('E_SET_ACTION_ICON', 'action3', 'gui/ui_res_2/battle/mech_main/icon_mech8012_3.png', 'show')
        self.send_event('E_SET_ACTION_ICON', 'action6', 'gui/ui_res_2/battle/mech_main/mech_rush_not_roll.png')
        self.send_event('E_SET_ACTION_SELECTED', self.bind_action_id, True)
        self.send_event('E_IGNORE_RELOAD_ANIM', True)
        self.send_event('E_ENABLE_KILL_ACTION', False)
        self.send_event('E_SHOW_LIGHT', False)
        self.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', (bcast.E_SHOW_LIGHT, (False,)))
        self.send_event('E_CLEAR_UP_BODY_ANIM')
        if self.first_trans:
            self.sub_state = self.SUB_ST_TO_BALL
        else:
            self.trans_to_ball()
        self.clear_move_timer()
        self.move_timer = global_data.game_mgr.get_fix_logic_timer().register(func=self.on_move_ball, interval=1, timedelta=True)
        self.block_trans_to_human_failed_msg = -1

    def on_move_ball(self, dt):
        if not self.is_active:
            return
        if self.sub_state == self.SUB_ST_BALL and not self.ball_is_dash:
            rocker_dir = self.sd.ref_rocker_dir
            self.send_event('E_MOVE_BALL', rocker_dir, dt)
            if self.is_pve and self.ev_g_on_ground():
                from logic.gcommon.component.client.com_mecha_appearance.ComBallDriver import BALL_RADIUS
                should_create_field = True
                cur_ts = time.time()
                cur_pos = self.ev_g_position() - math3d.vector(0, BALL_RADIUS, 0)
                if self.last_field_info:
                    create_ts, create_pos = self.last_field_info
                    if cur_ts - create_ts < self.field_create_inter and (cur_pos - create_pos).length < self.field_create_dist:
                        should_create_field = False
                if should_create_field:
                    self.last_field_info = (
                     cur_ts, cur_pos)
                    self.send_event('E_DO_SKILL', self.pve_fire_field_skill_id, {'position': [cur_pos.x, cur_pos.y, cur_pos.z]})

    def update(self, dt):
        super(Dash8012, self).update(dt)
        if self.is_pve and self.pve_bump_speed_add_timer > 0:
            self.pve_bump_speed_add_timer -= dt
            if self.pve_bump_speed_add_timer <= 0:
                self.pve_bump_speed_add_layer = 0
                self.refresh_move_speed()
        if self.sub_state == self.SUB_ST_BALL and not self.ball_is_dash:
            cur_jump_input = self.ev_g_action_status('action5')
            if not self.last_jump_input and cur_jump_input:
                if self.ev_g_can_cast_skill(self.jump_skill_id):
                    self.send_event('E_BALL_JUMP', self.jump_speed, self.jump_gravity, self.jump_cam_follow_speed, self.jump_cam_recover_delay, self.jump_cam_recover_time, self.jump_skill_id)
            self.last_jump_input = cur_jump_input
        if self.is_overloading:
            self.last_detect_time += dt
            if self.last_detect_time > 0.1:
                self.last_detect_time = 0
                self.try_trans_to_human(show_msg=False)
        if self.need_trans_to_human:
            self.try_trans_to_human(show_msg=False)

    def check_transitions(self):
        if self.can_brake:
            if self.ev_g_is_in_frozen():
                return MC_FROZEN
            if self.ev_g_immobilized():
                return MC_IMMOBILIZE
            rocker_dir = self.sd.ref_rocker_dir
            if rocker_dir and not rocker_dir.is_zero:
                return MC_MOVE
        if self.sub_state == self.SUB_ST_TO_HUMAN and self.trans_back_finished:
            return MC_STAND

    def exit(self, enter_states):
        self.send_event('E_CLEAR_BLACK_STATE')
        if self.sphere_flamethrower_enabled and MC_SECOND_WEAPON_ATTACK in self.ev_g_cur_state():
            self.send_event('TRY_STOP_WEAPON_ATTACK')
            self.ev_g_need_auto_continue_second_weapon() and self.send_event('E_KEEP_TRYING_SECOND_WEAPON')
        self.leave_mecha_in_ball = MC_DRIVER_LEAVING in enter_states or MC_DEAD in enter_states
        self.recover_to_character()
        self.clear_move_timer()
        self.ev_g_cancel_state(MC_HELP)
        self.send_event('E_ENABLE_HELP_ANIM', True)
        if MC_DRIVER_LEAVING in enter_states:
            self.send_event('E_DISABLE_DRIVER')
        if MC_IMMOBILIZE in enter_states or MC_DEAD in enter_states:
            self.send_event('E_CLEAR_SPEED')
        self.send_event('E_CLEAR_WHITE_STATE', self.sid)
        self.send_event('E_SET_ACTION_SELECTED', self.bind_action_id, False)
        self.sub_state = -1
        self.is_overloading = False
        self.hit_targets = {}
        super(Dash8012, self).exit(enter_states)

    def action_btn_down(self):
        if self.sub_state in (self.SUB_ST_TO_HUMAN, self.SUB_ST_TO_BALL):
            return False
        else:
            if self.try_trans_to_human():
                return False
            if not self.check_can_active():
                return False
            if not self.check_can_cast_skill():
                return False
            super(Dash8012, self).action_btn_down()
            if self.sub_state != self.SUB_ST_BALL:
                self.send_event('E_DO_SKILL', self.skill_id)
                return True
            return False

    def action_btn_up(self):
        super(Dash8012, self).action_btn_up()
        self.send_event('E_SET_ACTION_SELECTED', self.bind_action_id, self.is_active)

    def recover_to_character(self):
        if not self.is_ball_driver:
            return
        self.is_ball_driver = False
        self.send_event('E_DISABLE_BALL_DRIVER')
        self.send_event('E_RESET_ROTATION', 0)
        self.send_event('E_SWITCH_ACTION', 'action1', MC_SHOOT)
        self.send_event('E_SWITCH_ACTION', 'action2', MC_SHOOT)
        self.send_event('E_SWITCH_ACTION', 'action3', MC_SHOOT)
        self.send_event('E_SET_ACTION_ICON', 'action1', 'gui/ui_res_2/battle/mech_main/icon_mech8012_1.png', 'show')
        self.send_event('E_SET_ACTION_ICON', 'action2', 'gui/ui_res_2/battle/mech_main/icon_mech8012_1.png', 'show')
        self.send_event('E_SET_ACTION_ICON', 'action3', 'gui/ui_res_2/battle/mech_main/icon_mech8012_1.png', 'show')
        if self.sphere_flamethrower_enabled:
            self.send_event('E_SET_ACTION_ICON', 'action4', 'gui/ui_res_2/battle/mech_main/icon_mech8012_2.png', 'show')
        self.send_event('E_SET_ACTION_ICON', 'action6', 'gui/ui_res_2/battle/mech_main/mech_rush_roll.png')
        self.send_event('E_ENABLE_KILL_ACTION', True)
        self.send_event('E_IGNORE_RELOAD_ANIM', False)
        self.send_event('E_BEGIN_RECOVER_MP', self.skill_id)
        self.send_event('E_OX_END_RUSH')
        self.send_event('E_DISABLE_YAW_WITH_CAMREA', False)
        if self.ev_g_is_diving():
            self.send_event('E_SHOW_LIGHT', True)
            self.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', (bcast.E_SHOW_LIGHT, (True,)))
        if self.ev_g_is_avatar():
            self.send_event('E_BALL_DASH_SCREEN_SFX', False)

    def super_jump(self, jump_args=None):
        if self.sub_state != self.SUB_ST_BALL:
            return
        self.send_event('E_BALL_JUMP', self.super_jump_speed, self.super_jump_gravity, self.super_jump_cam_follow_speed, self.super_jump_cam_recover_delay, self.super_jump_cam_recover_time)

    def on_hit_target--- This code section failed: ---

 489       0  LOAD_FAST             1  'target'
           3  UNARY_NOT        
           4  POP_JUMP_IF_TRUE     20  'to 20'
           7  LOAD_FAST             1  'target'
          10  LOAD_ATTR             0  'is_valid'
          13  CALL_FUNCTION_0       0 
          16  UNARY_NOT        
        17_0  COME_FROM                '4'
          17  POP_JUMP_IF_FALSE    24  'to 24'

 490      20  LOAD_CONST            0  ''
          23  RETURN_END_IF    
        24_0  COME_FROM                '17'

 491      24  LOAD_FAST             0  'self'
          27  LOAD_ATTR             1  'sub_state'
          30  LOAD_FAST             0  'self'
          33  LOAD_ATTR             2  'SUB_ST_BALL'
          36  COMPARE_OP            3  '!='
          39  POP_JUMP_IF_FALSE    46  'to 46'

 492      42  LOAD_CONST            0  ''
          45  RETURN_END_IF    
        46_0  COME_FROM                '39'

 493      46  LOAD_FAST             0  'self'
          49  LOAD_ATTR             3  'ev_g_ball_avg_speed'
          52  CALL_FUNCTION_0       0 
          55  STORE_FAST            2  'cur_speed'

 494      58  LOAD_FAST             2  'cur_speed'
          61  LOAD_FAST             0  'self'
          64  LOAD_ATTR             4  'damage_speed'
          67  COMPARE_OP            0  '<'
          70  POP_JUMP_IF_FALSE    87  'to 87'
          73  LOAD_FAST             0  'self'
          76  LOAD_ATTR             5  'dash_can_damage'
          79  UNARY_NOT        
        80_0  COME_FROM                '70'
          80  POP_JUMP_IF_FALSE    87  'to 87'

 495      83  LOAD_CONST            0  ''
          86  RETURN_END_IF    
        87_0  COME_FROM                '80'

 496      87  LOAD_GLOBAL           6  'time'
          90  LOAD_ATTR             6  'time'
          93  CALL_FUNCTION_0       0 
          96  STORE_FAST            3  'now'

 497      99  LOAD_FAST             1  'target'
         102  LOAD_ATTR             7  'id'
         105  LOAD_FAST             0  'self'
         108  LOAD_ATTR             8  'hit_targets'
         111  COMPARE_OP            6  'in'
         114  POP_JUMP_IF_FALSE   150  'to 150'
         117  LOAD_FAST             3  'now'
         120  LOAD_FAST             0  'self'
         123  LOAD_ATTR             8  'hit_targets'
         126  LOAD_FAST             1  'target'
         129  LOAD_ATTR             7  'id'
         132  BINARY_SUBSCR    
         133  BINARY_SUBTRACT  
         134  LOAD_FAST             0  'self'
         137  LOAD_ATTR             9  'damage_interval'
         140  COMPARE_OP            0  '<'
       143_0  COME_FROM                '114'
         143  POP_JUMP_IF_FALSE   150  'to 150'

 498     146  LOAD_CONST            0  ''
         149  RETURN_END_IF    
       150_0  COME_FROM                '143'

 499     150  LOAD_FAST             3  'now'
         153  LOAD_FAST             0  'self'
         156  LOAD_ATTR             8  'hit_targets'
         159  LOAD_FAST             1  'target'
         162  LOAD_ATTR             7  'id'
         165  STORE_SUBSCR     

 500     166  LOAD_GLOBAL          10  'math3d'
         169  LOAD_ATTR            11  'matrix'
         172  LOAD_ATTR            12  'make_rotation_y'
         175  LOAD_FAST             0  'self'
         178  LOAD_ATTR            13  'ev_g_yaw'
         181  CALL_FUNCTION_0       0 
         184  CALL_FUNCTION_1       1 
         187  LOAD_ATTR            14  'forward'
         190  STORE_FAST            4  'forward'

 501     193  LOAD_FAST             0  'self'
         196  LOAD_ATTR            15  'ev_g_position'
         199  CALL_FUNCTION_0       0 
         202  LOAD_FAST             4  'forward'
         205  LOAD_CONST            1  3
         208  BINARY_MULTIPLY  
         209  LOAD_GLOBAL          16  'NEOX_UNIT_SCALE'
         212  BINARY_MULTIPLY  
         213  BINARY_SUBTRACT  
         214  STORE_FAST            5  'pos'

 502     217  LOAD_FAST             0  'self'
         220  LOAD_ATTR            17  'ev_g_acc_duration_percent'
         223  CALL_FUNCTION_0       0 
         226  STORE_FAST            6  'energy'

 503     229  LOAD_FAST             0  'self'
         232  LOAD_ATTR            18  'send_event'
         235  LOAD_CONST            2  'E_DO_SKILL'
         238  LOAD_FAST             0  'self'
         241  LOAD_ATTR            19  'attack_skill_id'
         244  LOAD_FAST             1  'target'
         247  LOAD_ATTR             7  'id'
         250  LOAD_FAST             5  'pos'
         253  LOAD_FAST             2  'cur_speed'
         256  LOAD_GLOBAL          16  'NEOX_UNIT_SCALE'
         259  BINARY_DIVIDE    
         260  LOAD_FAST             6  'energy'
         263  LOAD_FAST             3  'now'
         266  CALL_FUNCTION_7       7 
         269  POP_TOP          

 505     270  LOAD_FAST             0  'self'
         273  LOAD_ATTR            20  'is_pve'
         276  POP_JUMP_IF_FALSE   349  'to 349'
         279  LOAD_FAST             0  'self'
         282  LOAD_ATTR            21  'pve_bump_speed_add_rate'
       285_0  COME_FROM                '276'
         285  POP_JUMP_IF_FALSE   349  'to 349'

 506     288  LOAD_FAST             0  'self'
         291  LOAD_ATTR            22  'pve_bump_speed_add_layer'
         294  LOAD_FAST             0  'self'
         297  LOAD_ATTR            23  'pve_bump_speed_add_max_layer'
         300  COMPARE_OP            0  '<'
         303  POP_JUMP_IF_FALSE   334  'to 334'

 507     306  LOAD_FAST             0  'self'
         309  DUP_TOP          
         310  LOAD_ATTR            22  'pve_bump_speed_add_layer'
         313  LOAD_CONST            3  1
         316  INPLACE_ADD      
         317  ROT_TWO          
         318  STORE_ATTR           22  'pve_bump_speed_add_layer'

 508     321  LOAD_FAST             0  'self'
         324  LOAD_ATTR            24  'refresh_move_speed'
         327  CALL_FUNCTION_0       0 
         330  POP_TOP          
         331  JUMP_FORWARD          0  'to 334'
       334_0  COME_FROM                '331'

 509     334  LOAD_FAST             0  'self'
         337  LOAD_ATTR            25  'pve_bump_speed_add_duration'
         340  LOAD_FAST             0  'self'
         343  STORE_ATTR           26  'pve_bump_speed_add_timer'
         346  JUMP_FORWARD          0  'to 349'
       349_0  COME_FROM                '346'

 511     349  LOAD_FAST             0  'self'
         352  LOAD_ATTR            27  'pve_ball_dash_enhance_radius'
         355  LOAD_CONST            4  ''
         358  COMPARE_OP            4  '>'
         361  POP_JUMP_IF_FALSE   907  'to 907'

 512     364  LOAD_GLOBAL          28  'getattr'
         367  LOAD_GLOBAL           5  'dash_can_damage'
         370  LOAD_CONST            0  ''
         373  CALL_FUNCTION_3       3 
         376  STORE_FAST            7  'check_obj'

 513     379  LOAD_FAST             7  'check_obj'
         382  POP_JUMP_IF_TRUE    444  'to 444'

 514     385  LOAD_FAST             0  'self'
         388  LOAD_ATTR            27  'pve_ball_dash_enhance_radius'
         391  LOAD_GLOBAL          16  'NEOX_UNIT_SCALE'
         394  BINARY_MULTIPLY  
         395  STORE_FAST            8  'radius'

 515     398  LOAD_GLOBAL          30  'collision'
         401  LOAD_ATTR            31  'col_object'
         404  LOAD_GLOBAL          30  'collision'
         407  LOAD_ATTR            32  'SPHERE'
         410  LOAD_GLOBAL          10  'math3d'
         413  LOAD_ATTR            33  'vector'
         416  LOAD_FAST             8  'radius'
         419  LOAD_FAST             8  'radius'
         422  LOAD_FAST             8  'radius'
         425  CALL_FUNCTION_3       3 
         428  CALL_FUNCTION_2       2 
         431  DUP_TOP          
         432  LOAD_FAST             0  'self'
         435  STORE_ATTR           34  'check_obj'
         438  STORE_FAST            7  'check_obj'
         441  JUMP_FORWARD          0  'to 444'
       444_0  COME_FROM                '441'

 516     444  LOAD_FAST             5  'pos'
         447  LOAD_FAST             7  'check_obj'
         450  STORE_ATTR           35  'position'

 517     453  LOAD_GLOBAL          36  'global_data'
         456  LOAD_ATTR            37  'game_mgr'
         459  LOAD_ATTR            38  'scene'
         462  LOAD_ATTR            39  'scene_col'
         465  LOAD_ATTR            40  'static_test'
         468  LOAD_FAST             7  'check_obj'
         471  LOAD_CONST            6  65535
         474  LOAD_GLOBAL          41  'GROUP_DYNAMIC_SHOOTUNIT'
         477  LOAD_GLOBAL          30  'collision'
         480  LOAD_ATTR            42  'INCLUDE_FILTER'
         483  CALL_FUNCTION_4       4 
         486  STORE_FAST            9  'check_ret'

 518     489  SETUP_LOOP          415  'to 907'
         492  LOAD_FAST             9  'check_ret'
         495  GET_ITER         
         496  FOR_ITER            404  'to 903'
         499  STORE_FAST           10  'cobj'

 519     502  LOAD_FAST            10  'cobj'
         505  LOAD_ATTR            43  'cid'
         508  STORE_FAST           11  'cid'

 520     511  LOAD_GLOBAL          36  'global_data'
         514  LOAD_ATTR            44  'emgr'
         517  LOAD_ATTR            45  'scene_find_unit_event'
         520  LOAD_ATTR            46  'emit'
         523  LOAD_FAST            11  'cid'
         526  CALL_FUNCTION_1       1 
         529  LOAD_CONST            4  ''
         532  BINARY_SUBSCR    
         533  STORE_FAST           12  'unit_obj'

 521     536  LOAD_FAST            12  'unit_obj'
         539  UNARY_NOT        
         540  POP_JUMP_IF_TRUE    496  'to 496'
         543  LOAD_FAST            12  'unit_obj'
         546  LOAD_ATTR             7  'id'
         549  LOAD_FAST             0  'self'
         552  LOAD_ATTR             8  'hit_targets'
         555  COMPARE_OP            6  'in'
         558  POP_JUMP_IF_TRUE    496  'to 496'

 522     561  LOAD_FAST            12  'unit_obj'
         564  LOAD_ATTR            47  'is_monster'
         567  CALL_FUNCTION_0       0 
         570  UNARY_NOT        
       571_0  COME_FROM                '558'
       571_1  COME_FROM                '540'
         571  POP_JUMP_IF_FALSE   580  'to 580'

 523     574  CONTINUE            496  'to 496'
         577  JUMP_FORWARD          0  'to 580'
       580_0  COME_FROM                '577'

 524     580  LOAD_FAST            12  'unit_obj'
         583  LOAD_ATTR            48  'ev_g_model'
         586  CALL_FUNCTION_0       0 
         589  STORE_FAST           13  'model'

 525     592  LOAD_FAST            13  'model'
         595  POP_JUMP_IF_TRUE    604  'to 604'

 526     598  CONTINUE            496  'to 496'
         601  JUMP_FORWARD          0  'to 604'
       604_0  COME_FROM                '601'

 527     604  LOAD_GLOBAL          49  'True'
         607  STORE_FAST           14  'enable_unit'

 528     610  LOAD_FAST            13  'model'
         613  LOAD_ATTR            50  'get_socket_matrix'
         616  LOAD_CONST            7  'fx_buff'
         619  LOAD_GLOBAL          51  'world'
         622  LOAD_ATTR            52  'SPACE_TYPE_WORLD'
         625  CALL_FUNCTION_2       2 
         628  STORE_FAST           15  'mat'

 529     631  LOAD_FAST            15  'mat'
         634  POP_JUMP_IF_FALSE   649  'to 649'

 530     637  LOAD_FAST            15  'mat'
         640  LOAD_ATTR            53  'translation'
         643  STORE_FAST           16  'unit_pos'
         646  JUMP_FORWARD         35  'to 684'

 532     649  LOAD_FAST            12  'unit_obj'
         652  LOAD_ATTR            54  'ev_g_model_position'
         655  CALL_FUNCTION_0       0 
         658  LOAD_GLOBAL          10  'math3d'
         661  LOAD_ATTR            33  'vector'
         664  LOAD_CONST            4  ''
         667  LOAD_CONST            8  0.5
         670  LOAD_GLOBAL          16  'NEOX_UNIT_SCALE'
         673  BINARY_MULTIPLY  
         674  LOAD_CONST            4  ''
         677  CALL_FUNCTION_3       3 
         680  BINARY_ADD       
         681  STORE_FAST           16  'unit_pos'
       684_0  COME_FROM                '646'

 533     684  LOAD_GLOBAL          55  'GROUP_STATIC_SHOOTUNIT'
         687  LOAD_GLOBAL          41  'GROUP_DYNAMIC_SHOOTUNIT'
         690  BINARY_OR        
         691  STORE_FAST           17  'group'

 534     694  LOAD_GLOBAL          55  'GROUP_STATIC_SHOOTUNIT'
         697  LOAD_GLOBAL          41  'GROUP_DYNAMIC_SHOOTUNIT'
         700  BINARY_OR        
         701  STORE_FAST           18  'mask'

 535     704  LOAD_GLOBAL          36  'global_data'
         707  LOAD_ATTR            37  'game_mgr'
         710  LOAD_ATTR            38  'scene'
         713  LOAD_ATTR            39  'scene_col'
         716  LOAD_ATTR            56  'hit_by_ray'

 536     719  LOAD_FAST             5  'pos'
         722  LOAD_FAST            16  'unit_pos'
         725  LOAD_CONST            4  ''
         728  LOAD_FAST            17  'group'
         731  LOAD_FAST            18  'mask'
         734  LOAD_GLOBAL          30  'collision'
         737  LOAD_ATTR            42  'INCLUDE_FILTER'
         740  LOAD_GLOBAL          49  'True'
         743  CALL_FUNCTION_7       7 
         746  STORE_FAST           19  'result'

 537     749  LOAD_FAST            19  'result'
         752  LOAD_CONST            4  ''
         755  BINARY_SUBSCR    
         756  POP_JUMP_IF_FALSE   834  'to 834'

 538     759  SETUP_LOOP           72  'to 834'
         762  LOAD_FAST            19  'result'
         765  LOAD_CONST            3  1
         768  BINARY_SUBSCR    
         769  GET_ITER         
         770  FOR_ITER             57  'to 830'
         773  STORE_FAST           10  'cobj'

 539     776  LOAD_FAST            10  'cobj'
         779  LOAD_CONST            9  4
         782  BINARY_SUBSCR    
         783  LOAD_ATTR            43  'cid'
         786  STORE_FAST           20  'cobj_id'

 540     789  LOAD_GLOBAL          36  'global_data'
         792  LOAD_ATTR            44  'emgr'
         795  LOAD_ATTR            45  'scene_find_unit_event'
         798  LOAD_ATTR            46  'emit'
         801  LOAD_FAST            20  'cobj_id'
         804  CALL_FUNCTION_1       1 
         807  LOAD_CONST            4  ''
         810  BINARY_SUBSCR    
         811  POP_JUMP_IF_FALSE   820  'to 820'

 541     814  CONTINUE            770  'to 770'
         817  JUMP_FORWARD          0  'to 820'
       820_0  COME_FROM                '817'

 542     820  LOAD_GLOBAL          57  'False'
         823  STORE_FAST           14  'enable_unit'

 543     826  BREAK_LOOP       
         827  JUMP_BACK           770  'to 770'
         830  POP_BLOCK        
       831_0  COME_FROM                '759'
         831  JUMP_FORWARD          0  'to 834'
       834_0  COME_FROM                '759'

 544     834  LOAD_FAST            14  'enable_unit'
         837  POP_JUMP_IF_FALSE   496  'to 496'

 545     840  LOAD_FAST             3  'now'
         843  LOAD_FAST             0  'self'
         846  LOAD_ATTR             8  'hit_targets'
         849  LOAD_FAST            12  'unit_obj'
         852  LOAD_ATTR             7  'id'
         855  STORE_SUBSCR     

 546     856  LOAD_FAST             0  'self'
         859  LOAD_ATTR            18  'send_event'
         862  LOAD_CONST            2  'E_DO_SKILL'
         865  LOAD_FAST             0  'self'
         868  LOAD_ATTR            19  'attack_skill_id'
         871  LOAD_FAST            12  'unit_obj'
         874  LOAD_ATTR             7  'id'
         877  LOAD_FAST             5  'pos'
         880  LOAD_FAST             2  'cur_speed'
         883  LOAD_GLOBAL          16  'NEOX_UNIT_SCALE'
         886  BINARY_DIVIDE    
         887  LOAD_FAST             6  'energy'
         890  LOAD_FAST             3  'now'
         893  CALL_FUNCTION_7       7 
         896  POP_TOP          
         897  JUMP_BACK           496  'to 496'
         900  JUMP_BACK           496  'to 496'
         903  POP_BLOCK        
       904_0  COME_FROM                '489'
         904  JUMP_FORWARD          0  'to 907'
       907_0  COME_FROM                '489'

 548     907  LOAD_FAST             0  'self'
         910  LOAD_ATTR            18  'send_event'
         913  LOAD_CONST           10  'E_PLAY_CAMERA_TRK'
         916  LOAD_CONST           11  '8012_DASH_MID'
         919  CALL_FUNCTION_2       2 
         922  POP_TOP          

 549     923  LOAD_FAST             0  'self'
         926  LOAD_ATTR            58  'ball_is_dash'
         929  UNARY_NOT        
         930  POP_JUMP_IF_FALSE  1098  'to 1098'
         933  LOAD_FAST             1  'target'
         936  LOAD_ATTR            59  'MASK'
         939  LOAD_GLOBAL          60  'MECHA_VEHICLE_MONSTER_TAG_VALUE'
         942  BINARY_AND       
       943_0  COME_FROM                '930'
         943  POP_JUMP_IF_FALSE  1098  'to 1098'

 550     946  LOAD_FAST             0  'self'
         949  LOAD_ATTR            61  'ev_g_char_walk_direction'
         952  CALL_FUNCTION_0       0 
         955  STORE_FAST           21  'cur_h_v'

 551     958  LOAD_GLOBAL          10  'math3d'
         961  LOAD_ATTR            33  'vector'
         964  LOAD_FAST            21  'cur_h_v'
         967  CALL_FUNCTION_1       1 
         970  STORE_FAST           21  'cur_h_v'

 552     973  LOAD_GLOBAL          10  'math3d'
         976  LOAD_ATTR            33  'vector'
         979  LOAD_FAST            21  'cur_h_v'
         982  CALL_FUNCTION_1       1 
         985  STORE_FAST           22  'move_dir'

 553     988  LOAD_FAST            22  'move_dir'
         991  LOAD_ATTR            62  'is_zero'
         994  POP_JUMP_IF_FALSE  1021  'to 1021'

 554     997  LOAD_GLOBAL          10  'math3d'
        1000  LOAD_ATTR            33  'vector'
        1003  LOAD_CONST            4  ''
        1006  LOAD_CONST            4  ''
        1009  LOAD_CONST            4  ''
        1012  CALL_FUNCTION_3       3 
        1015  STORE_FAST           21  'cur_h_v'
        1018  JUMP_FORWARD         24  'to 1045'

 556    1021  LOAD_FAST            22  'move_dir'
        1024  LOAD_ATTR            63  'normalize'
        1027  CALL_FUNCTION_0       0 
        1030  POP_TOP          

 557    1031  LOAD_FAST            22  'move_dir'
        1034  UNARY_NEGATIVE   
        1035  LOAD_FAST             0  'self'
        1038  LOAD_ATTR            64  'rebound_h_speed'
        1041  BINARY_MULTIPLY  
        1042  STORE_FAST           21  'cur_h_v'
      1045_0  COME_FROM                '1018'

 558    1045  LOAD_FAST             0  'self'
        1048  LOAD_ATTR            64  'rebound_h_speed'
        1051  LOAD_FAST             0  'self'
        1054  LOAD_ATTR            65  'sd'
        1057  STORE_ATTR           66  'ref_cur_speed'

 559    1060  LOAD_FAST             0  'self'
        1063  LOAD_ATTR            18  'send_event'
        1066  LOAD_CONST           12  'E_CHARACTER_WALK'
        1069  LOAD_FAST            21  'cur_h_v'
        1072  CALL_FUNCTION_2       2 
        1075  POP_TOP          

 560    1076  LOAD_FAST             0  'self'
        1079  LOAD_ATTR            18  'send_event'
        1082  LOAD_CONST           13  'E_JUMP'
        1085  LOAD_FAST             0  'self'
        1088  LOAD_ATTR            67  'rebound_v_speed'
        1091  CALL_FUNCTION_2       2 
        1094  POP_TOP          
        1095  JUMP_FORWARD          0  'to 1098'
      1098_0  COME_FROM                '1095'
        1098  LOAD_CONST            0  ''
        1101  RETURN_VALUE     

Parse error at or near `CALL_FUNCTION_3' instruction at offset 373

    def on_hit_human(self, target):
        if self.sub_state != self.SUB_ST_BALL:
            return
        else:
            cur_speed = self.ev_g_ball_avg_speed()
            if cur_speed < self.damage_speed and not self.dash_can_damage:
                return
            now = time.time()
            if target.id in self.hit_targets and now - self.hit_targets[target.id] < self.damage_interval:
                return
            self.hit_targets[target.id] = now
            lst_vel_give, vehicle_speed, t = self.calc_hit_human_vec(target)
            if vehicle_speed.length < 5:
                return
            self.send_event('E_PLAY_CAMERA_TRK', '8012_DASH_WEAK')
            crash_id = target.ev_g_crash_id_get_next()
            if crash_id is not None:
                self.send_event('E_DO_SKILL', self.attack_skill_id, target.id, None, cur_speed / NEOX_UNIT_SCALE, 0, now)
            return

    def calc_hit_human_vec(self, unit_obj):
        human_pos = unit_obj.ev_g_position()
        velocity = self.ev_g_char_walk_direction()
        if velocity is None:
            return (math3d.vector(0, 0, 0), math3d.vector(0, 0, 0), 0)
        else:
            if not human_pos:
                return (math3d.vector(0, 0, 0), math3d.vector(0, 0, 0), 0)
            model = self.ev_g_model()
            human_dir = human_pos - model.world_position
            right = model.world_transformation.right
            forward = model.world_transformation.forward
            flag = 1 if forward.cross(human_dir).y > 0 else -1
            v_speed = velocity.length / NEOX_UNIT_SCALE * 3.6
            factor = 14.4 if v_speed >= 50 else 4.4 + 0.004 * v_speed ** 2
            t = 0.2 + 0.008 * v_speed
            return (
             right * flag * (factor / 3.6 * NEOX_UNIT_SCALE) + velocity, velocity, t)

    def on_overload(self, *args):
        self.is_overloading = True

    def on_overload_stop(self):
        self.is_overloading = False

    def on_trans_to_ball(self, first_trans, left_time, duration):
        self.first_trans = first_trans
        self.left_time = left_time
        self.active_self()
        self.sound_custom_start()

    def on_trans_to_human(self):
        if self.is_active:
            self.sound_custom_end()
            if self.sub_state != self.SUB_ST_BALL:
                return
            if self.ev_g_is_in_any_state(MC_THUMP_RUSH):
                return
            if mecha_utils.check_trans_back_to_mecha(self.sd.ref_mecha_id, self.ev_g_position()):
                self.sub_state = self.SUB_ST_TO_HUMAN
                self.send_event('E_END_SKILL', self.skill_id)
                self.need_trans_to_human = False

    def try_trans_to_human(self, show_msg=True, force=False):
        if self.is_active:
            if self.sub_state != self.SUB_ST_BALL:
                return
            if self.ev_g_is_in_any_state(MC_THUMP_RUSH) and not force:
                if self.ev_g_can_break_ball_dash():
                    self.send_event('E_DISABLE_STATE', MC_THUMP_RUSH)
                else:
                    return
            if not mecha_utils.check_trans_back_to_mecha(self.sd.ref_mecha_id, self.ev_g_position()):
                if show_msg and self.block_trans_to_human_failed_msg != 1:
                    self.send_event('E_SHOW_MESSAGE', get_text_local_content(18145))
                if self.block_trans_to_human_failed_msg == 1:
                    self.block_trans_to_human_failed_msg = 0
                return False
            self.sub_state = self.SUB_ST_TO_HUMAN
            self.send_event('E_END_SKILL', self.skill_id)
            self.need_trans_to_human = False
            return True
        return False

    def destroy(self):
        self.recover_to_character()
        super(Dash8012, self).destroy()

    def on_beat_back(self, from_pos, coe_v, coe_h, *args):
        if self.sub_state != self.SUB_ST_BALL:
            return
        dir_vec = self.ev_g_position() - from_pos
        if dir_vec.is_zero:
            return
        dir_vec.normalize()
        beat_back_h_v = math3d.vector(dir_vec.x * coe_h * self.beat_back_h_speed, 0, dir_vec.z * coe_h * self.beat_back_h_speed)
        self.send_event('E_JUMP', coe_v * self.beat_back_v_speed)
        self.sd.ref_cur_speed = coe_h * self.beat_back_h_speed
        self.send_event('E_CHARACTER_WALK', beat_back_h_v)

    def on_leave_mecha_in_ball(self):
        return self.leave_mecha_in_ball

    def clear_move_timer(self):
        if self.move_timer:
            global_data.game_mgr.get_fix_logic_timer().unregister(self.move_timer)
        self.move_timer = 0

    def try_exit_ball_state(self):
        if not self.is_active:
            return False
        if self.block_trans_to_human_failed_msg < 0:
            self.block_trans_to_human_failed_msg = 1
        self.action_btn_down()
        return True


def __editor_balldash_setter1(self, v):
    self.init_dash_speed = v * NEOX_UNIT_SCALE
    self.dash_speed = self.init_dash_speed * (1 + self.dash_speed_add_factor)


def __editor_balldash_setter2(self, v):
    self.init_pre_time = v
    self.pre_time = self.init_pre_time * (1 + self.pre_time_add_factor)
    self.refresh_param_changed()


@editor.state_exporter({('skill_id', 'param'): {'zh_name': '\xe6\x8a\x80\xe8\x83\xbdid'},('dash_speed', 'param'): {'zh_name': '\xe5\x86\xb2\xe5\x88\xba\xe9\x80\x9f\xe5\xba\xa6','getter': --- This code section failed: ---

 701       0  LOAD_GLOBAL           0  'getattr'
           3  LOAD_GLOBAL           1  'NEOX_UNIT_SCALE'
           6  CALL_FUNCTION_2       2 
           9  LOAD_GLOBAL           1  'NEOX_UNIT_SCALE'
          12  BINARY_DIVIDE    
          13  RETURN_VALUE_LAMBDA
          -1  LAMBDA_MARKER    

Parse error at or near `CALL_FUNCTION_2' instruction at offset 6
,'setter': lambda self, v: __editor_balldash_setter1(self, v)
                             },
   ('pre_time', 'param'): {'zh_name': '\xe5\x86\xb2\xe5\x88\xba\xe5\x89\x8d\xe6\x91\x87\xe6\x97\xb6\xe9\x97\xb4','getter': --- This code section failed: ---

 704       0  LOAD_GLOBAL           0  'getattr'
           3  LOAD_GLOBAL           1  'NEOX_UNIT_SCALE'
           6  CALL_FUNCTION_2       2 
           9  LOAD_GLOBAL           1  'NEOX_UNIT_SCALE'
          12  BINARY_DIVIDE    
          13  RETURN_VALUE_LAMBDA
          -1  LAMBDA_MARKER    

Parse error at or near `CALL_FUNCTION_2' instruction at offset 6
,'setter': lambda self, v: __editor_balldash_setter2(self, v)
                           },
   ('min_pre_duration', 'param'): {'zh_name': '\xe6\x9c\x80\xe5\xb0\x8f\xe5\x86\xb2\xe5\x88\xba\xe5\x89\x8d\xe6\x91\x87'},('dash_time', 'param'): {'zh_name': '\xe5\x86\xb2\xe5\x88\xba\xe6\x8c\x81\xe7\xbb\xad\xe6\x97\xb6\xe9\x97\xb4'},('pre_float_speed', 'meter'): {'zh_name': '\xe5\x89\x8d\xe6\x91\x87\xe6\x97\xb6\xe6\xb5\xae\xe7\xa9\xba\xe9\x80\x9f\xe5\xba\xa6','min_val': 0,'max_val': 5},('pre_slow_acc', 'meter'): {'zh_name': '\xe5\x89\x8d\xe6\x91\x87\xe6\x97\xb6\xe5\x88\xb9\xe8\xbd\xa6\xe5\x8a\xa0\xe9\x80\x9f\xe5\xba\xa6','min_val': 10,'max_val': 300},('post_slow_acc', 'meter'): {'zh_name': '\xe5\x90\x8e\xe6\x91\x87\xe6\x97\xb6\xe5\x88\xb9\xe8\xbd\xa6\xe5\x8a\xa0\xe9\x80\x9f\xe5\xba\xa6','min_val': 10,'max_val': 300},('rebound_h_speed', 'meter'): {'zh_name': '\xe6\x92\x9e\xe5\x87\xbb\xe5\x9b\x9e\xe5\xbc\xb9\xe6\xb0\xb4\xe5\xb9\xb3\xe9\x80\x9f\xe5\xba\xa6'},('rebound_v_speed', 'meter'): {'zh_name': '\xe6\x92\x9e\xe5\x87\xbb\xe5\x9b\x9e\xe5\xbc\xb9\xe5\x9e\x82\xe7\x9b\xb4\xe9\x80\x9f\xe5\xba\xa6'},('camera_follow_speed', 'param'): {'zh_name': '\xe5\x86\xb2\xe5\x88\xba\xe6\x97\xb6\xe7\x9b\xb8\xe6\x9c\xba\xe8\xb7\x9f\xe9\x9a\x8f\xe9\x80\x9f\xe5\xba\xa6','min_val': 0,'max_val': 1},('camera_recover_delay', 'param'): {'zh_name': '\xe5\x86\xb2\xe5\x88\xba\xe6\x97\xb6\xe7\x9b\xb8\xe6\x9c\xba\xe8\xb7\x9f\xe9\x9a\x8f\xe8\xbf\x9f\xe6\xbb\x9e'},('camera_recover_time', 'param'): {'zh_name': '\xe5\x86\xb2\xe5\x88\xba\xe6\x97\xb6\xe7\x9b\xb8\xe6\x9c\xba\xe6\x81\xa2\xe5\xa4\x8d\xe6\x97\xb6\xe9\x97\xb4'},('reflect_cut_angle', 'param'): {'zh_name': '\xe8\xa1\xb0\xe5\x87\x8f\xe5\x88\x86\xe5\x89\xb2\xe8\xa7\x92\xe5\xba\xa6','min_val': 1,'max_val': 89,'explain': '\xe6\x92\x9e\xe5\x87\xbb\xe6\x97\xb6\xef\xbc\x8c\xe6\x92\x9e\xe5\x87\xbb\xe9\x9d\xa2\xe5\x8f\x91\xe7\x8e\xb0\xe7\x9a\x84\xe8\xa7\x92\xe5\xba\xa6\xe5\x88\x86\xe5\x89\xb2\xe5\x80\xbc\xef\xbc\x8c\xe5\xa4\xa7\xe4\xba\x8e\xe8\xaf\xa5\xe5\x80\xbc\xe4\xbd\xbf\xe7\x94\xa8\xe5\xb0\x8f\xe8\xa1\xb0\xe5\x87\x8f\xe7\xb3\xbb\xe6\x95\xb0\xef\xbc\x8c\xe5\xb0\x8f\xe4\xba\x8e\xe8\xaf\xa5\xe5\x80\xbc\xe4\xbd\xbf\xe7\x94\xa8\xe5\xa4\xa7\xe8\xa1\xb0\xe5\x87\x8f\xe7\xb3\xbb\xe6\x95\xb0'},('reflect_rate_small', 'param'): {'zh_name': '\xe5\x8f\x8d\xe5\xbc\xb9\xe5\xb0\x8f\xe8\xa1\xb0\xe5\x87\x8f\xe7\xb3\xbb\xe6\x95\xb0','min_val': 0.0,'max_val': 0.8},('reflect_rate_large', 'param'): {'zh_name': '\xe5\x8f\x8d\xe5\xbc\xb9\xe5\xa4\xa7\xe8\xa1\xb0\xe5\x87\x8f\xe7\xb3\xbb\xe6\x95\xb0','min_val': 0.0,'max_val': 0.8},('min_reflect_rate', 'param'): {'zh_name': '\xe6\x9c\x80\xe5\xb0\x8f\xe9\x80\x9f\xe5\xba\xa6\xe8\xa1\xb0\xe5\x87\x8f\xe7\xb3\xbb\xe6\x95\xb0','min_val': 0.0,'max_val': 0.8}})
class BallDash(StateBase):
    ST_NONE = -1
    ST_PRE = 0
    ST_DASH = 1
    ST_SLOW = 2
    BIND_EVENT = {'E_DISABLE_BALL_DRIVER': 'on_disable_ball_driver',
       'E_RUSH_HIT_TARGET': 'on_hit_target',
       'E_IMMOBILIZED': 'on_immobilized',
       'E_ON_FROZEN': 'on_immobilized',
       'E_CHANGE_DASH_FORWARD': 'on_change_forward',
       'G_CAN_BREAK_BALL_DASH': 'check_in_slow_state',
       'E_FUEL_EXHAUSTED': 'on_fuel_exhausted',
       'G_ACC_DURATION_PERCENT': 'get_acc_duration_percent'
       }

    def init_from_dict(self, unit_obj, bdict, sid, info):
        super(BallDash, self).init_from_dict(unit_obj, bdict, sid, info)
        self.hover_skill_id = self.custom_param['hover_skill_id']
        self.skill_id = self.custom_param['skill_id']
        self.dash_speed = self.custom_param.get('dash_speed', 120) * NEOX_UNIT_SCALE
        self.init_dash_speed = self.dash_speed
        self.pre_time = self.custom_param.get('pre_time', 1.0) * 1.0
        self.min_pre_duration = self.custom_param.get('min_pre_duration', 0.2)
        self.init_pre_time = self.pre_time
        self.dash_time = self.custom_param.get('dash_time', 0.6)
        self.pre_float_speed = self.custom_param.get('pre_float_speed', 1) * NEOX_UNIT_SCALE
        self.pre_slow_acc = self.custom_param.get('pre_slow_acc', 100) * NEOX_UNIT_SCALE
        self.post_slow_acc = self.custom_param.get('post_slow_acc', 200) * NEOX_UNIT_SCALE
        self.rebound_h_speed = self.custom_param.get('rebound_h_speed', 80) * NEOX_UNIT_SCALE
        self.rebound_v_speed = self.custom_param.get('rebound_v_speed', 50) * NEOX_UNIT_SCALE
        self.camera_follow_speed = self.custom_param.get('camera_follow_time', 0.1)
        self.camera_recover_delay = self.custom_param.get('camera_recover_delay', 0.4)
        self.camera_recover_time = self.custom_param.get('camera_recover_time', 0.7)
        self.damage_interval = 1
        self.hit_target_time = 0
        self.ball_driver_active = False
        self.ball_fall_gravity = (0, -50 * NEOX_UNIT_SCALE, 0)
        self.hover_skill_begun = False
        self.acc_duration_percent = 0.0
        self.dash_reflect_info = []
        self.reflect_rate_large = self.custom_param.get('reflect_rate_large', 0.5)
        self.reflect_rate_small = self.custom_param.get('reflect_rate_small', 0.2)
        self.reflect_cut_angle = self.custom_param.get('reflect_cut_angle', 20)
        self.min_reflect_rate = self.custom_param.get('min_reflect_rate', 0.2)
        self.dash_speed_add_factor = 0.0
        self.pre_time_add_factor = 0.0
        self.dash_time_add_factor = 0.0
        self.enable_param_changed_by_buff()
        self.hit_targets = {}
        self.trigger_hit = False
        self.float_speed_added = False
        self.pre_float_speed_rate = 1.0
        self.move_timer = 0
        self.btn_down = False
        self.action_canceled = False
        self.pve_breakthrough_enabled = False
        self.pve_fire_field_skill_id = 801259
        self._register_callbacks()

    def _register_callbacks(self):
        self.reset_sub_states_callback()
        self.register_substate_callback(self.ST_PRE, self.pre_time, self.start_hover)
        self.register_substate_callback(self.ST_DASH, self.dash_time * (1.0 + self.dash_time_add_factor), self.dash_end)

    def destroy(self):
        self.clear_move_timer()
        if self.ev_g_is_avatar():
            self.send_event('E_BALL_DASH_SCREEN_SFX', False)
            self.send_event('E_CANCEL_CAMERA_TRK', '8012_BALL')
            self.send_event('E_CANCEL_CAMERA_TRK', '8012_BALL_DASH')
            global_data.ui_mgr.close_ui('MechaCancelUI')
        super(BallDash, self).destroy()

    def action_btn_down(self):
        self.btn_down = True
        super(BallDash, self).action_btn_down()
        if self.is_active or self.action_canceled:
            return
        if not self.sd.ref_is_ball_mode:
            return
        if not self.check_can_active():
            return
        if not self.check_can_cast_skill():
            return
        self.active_self()
        return True

    def _ensure_end_hover_skill(self):
        if self.hover_skill_begun:
            self.send_event('E_END_SKILL', self.hover_skill_id)
            self.hover_skill_begun = False

    def pre_end(self):
        if self.ev_g_is_avatar():
            global_data.ui_mgr.close_ui('MechaCancelUI')
        self.end_custom_sound('loop')
        self.end_custom_sound('post')
        self.start_custom_sound('post')
        self.send_event('E_DO_SKILL', self.skill_id)
        self.send_event('E_BALL_IS_DASH', True, True)
        self.acc_duration_percent = self.sub_sid_timer / self.pre_time
        if self.acc_duration_percent > 1.0:
            self.acc_duration_percent = 1.0
        self.sub_state = self.ST_DASH
        self._ensure_end_hover_skill()
        if self.ev_g_is_avatar() and self.ev_g_ball_can_damage():
            self.send_event('E_BALL_DASH_SCREEN_SFX', True)
            self.send_event('E_CANCEL_CAMERA_TRK', '8012_BALL_IDLE_DASH_LOOP')
            self.send_event('E_PLAY_CAMERA_TRK', '8012_BALL_DASH')
            self.send_event('E_SET_CAMERA_FOLLOW_SPEED', True, self.camera_follow_speed, self.camera_recover_delay, self.camera_recover_time)
        from logic.gutils.mecha_utils import get_fire_end_posiiton
        end_pos = get_fire_end_posiiton(self.unit_obj)
        self.dash_forward = end_pos - self.ev_g_position()
        self.dash_forward.normalize()
        rot = math3d.matrix_to_rotation(math3d.matrix.make_rotation_y(self.dash_forward.yaw))
        self.send_event('E_SHOW_BALL_DASH_PRE_SFX', False, (rot.x, rot.y, rot.z, rot.w))
        self.send_event('E_SHOW_BALL_DASH_SFX', True, (rot.x, rot.y, rot.z, rot.w))
        self.send_event('E_SHOW_DASH_PRE_PROGRESS', False)

    def action_btn_up(self):
        self.btn_down = False
        if self.is_active and self.sub_state == self.ST_PRE:
            self.pre_end()
        self.action_canceled = False

    def cancel(self):
        if self.is_active and self.sub_state == self.ST_PRE:
            self.sub_state = self.ST_NONE
            self.action_canceled = True

    def enter(self, leave_states):
        super(BallDash, self).enter(leave_states)
        self.dash_reflect_info = []
        self.ball_driver_active = True
        self.hover_skill_begun = False
        self.sub_state = self.ST_PRE
        self.start_custom_sound('loop')
        self.send_event('E_GRAVITY', 0)
        self.send_event('E_BALL_CHECK_DAMAGE', True)
        self.send_event('E_BALL_IS_DASH', True, False)
        self.send_event('E_CANCEL_CAMERA_TRK', '8012_BALL')
        self.send_event('E_PLAY_CAMERA_TRK', '8012_BALL_IDLE_DASH_LOOP')
        self.send_event('E_SHOW_DASH_PRE_PROGRESS', True, self.pre_time)
        rot = math3d.matrix_to_rotation(math3d.matrix.make_rotation_y(self.ev_g_yaw() or 0))
        self.send_event('E_SHOW_BALL_DASH_PRE_SFX', True, (rot.x, rot.y, rot.z, rot.w))
        self.ball_fall_gravity = self.ev_g_ball_fall_gravity()
        self.trigger_hit = False
        self.float_speed_added = False
        self.clear_move_timer()
        self.move_timer = global_data.game_mgr.get_fix_logic_timer().register(func=self.on_move_ball, interval=1, timedelta=True)
        if self.ev_g_is_avatar():
            from logic.comsys.mecha_ui.MechaCancelUI import MechaCancelUI
            MechaCancelUI(None, self.cancel)
        return

    def start_hover(self):
        self.send_event('E_DO_SKILL', self.hover_skill_id)
        self.hover_skill_begun = True

    def dash_end(self):
        self.sub_state = self.ST_SLOW
        self.send_event('E_GRAVITY', self.ball_fall_gravity)
        rot = math3d.matrix_to_rotation(math3d.matrix.make_rotation_y(self.dash_forward.yaw))
        self.send_event('E_SHOW_BALL_DASH_SFX', False, (rot.x, rot.y, rot.z, rot.w))
        self.send_event('E_END_SKILL', self.skill_id)

    def update(self, dt):
        super(BallDash, self).update(dt)
        if self.elapsed_time - dt < self.min_pre_duration <= self.elapsed_time and self.sub_state == self.ST_PRE and not self.btn_down:
            self.pre_end()

    def exit(self, enter_states):
        super(BallDash, self).exit(enter_states)
        self.end_custom_sound('loop')
        if self.ball_driver_active:
            self.send_event('E_TRY_SWITCH_TO_CAMERA_STATE', str(52))
        if self.ev_g_is_avatar():
            self.send_event('E_BALL_DASH_SCREEN_SFX', False)
            self.send_event('E_CANCEL_CAMERA_TRK', '8012_BALL_DASH')
            self.send_event('E_CANCEL_CAMERA_TRK', '8012_BALL_IDLE_DASH_LOOP')
            if self.ev_g_ball_can_damage() and self.ball_driver_active:
                self.send_event('E_PLAY_CAMERA_TRK', '8012_BALL')
            global_data.ui_mgr.close_ui('MechaCancelUI')
        self._ensure_end_hover_skill()
        self.send_event('E_GRAVITY', self.ball_fall_gravity)
        self.send_event('E_BALL_IS_DASH', False, False)
        self.send_event('E_SHOW_BALL_DASH_PRE_SFX', False)
        self.send_event('E_SHOW_BALL_DASH_SFX', False)
        self.send_event('E_SHOW_DASH_PRE_PROGRESS', False)
        self.send_event('E_END_SKILL', self.skill_id)
        self.clear_move_timer()

    def on_disable_ball_driver(self):
        self.ball_driver_active = False
        self.sub_state = self.ST_NONE
        self.send_event('E_RESET_ROTATION', 0)

    def on_change_forward(self, forward, surface_angle):
        if self.sub_state == self.ST_DASH:
            self.dash_forward = forward
            rate = self.reflect_rate_small if abs(surface_angle) > self.reflect_cut_angle else self.reflect_rate_large
            self.dash_reflect_info.append(rate)
        self.trigger_hit = True

    def check_in_slow_state(self):
        return self.sub_state == self.ST_SLOW

    def on_move_ball(self, dt):
        if self.sub_state == self.ST_NONE:
            return
        walk_direction = self.ev_g_char_walk_direction()
        vertical_speed = self.ev_g_vertical_speed()
        if self.sub_state == self.ST_PRE:
            if self.float_speed_added:
                vertical_speed -= self.pre_float_speed * self.pre_float_speed_rate
            move_dir = walk_direction + math3d.vector(0, vertical_speed, 0)
            if not move_dir.is_zero:
                move_dir.normalize()
            dv = -move_dir * self.pre_slow_acc * dt
            dv_ver = dv.y
            dv.y = 0
            dv_hor = dv
            if walk_direction.length < dv_hor.length:
                walk_direction = math3d.vector(0, 0, 0)
            else:
                walk_direction += dv_hor
            self.send_event('E_CHARACTER_WALK', walk_direction)
            if abs(vertical_speed) < abs(dv_ver):
                vertical_speed = 0
            else:
                vertical_speed += dv_ver
            vertical_speed += self.pre_float_speed * self.pre_float_speed_rate
            self.float_speed_added = True
            self.send_event('E_VERTICAL_SPEED', vertical_speed)
            right = math3d.matrix.make_rotation_y(self.ev_g_yaw() or 0).right
            rot = math3d.rotation(0, 0, 0, 1)
            rot.set_axis_angle(right, -dt * 30)
            cur_rot = math3d.matrix_to_rotation(self.sd.ref_cur_rotation_matrix)
            cur_rot = rot * cur_rot
            self.sd.ref_cur_rotation_matrix = math3d.rotation_to_matrix(cur_rot)
        elif self.sub_state == self.ST_DASH:
            dv = self.dash_forward * 500 * NEOX_UNIT_SCALE * dt
            velocity_sum = walk_direction + math3d.vector(0, vertical_speed, 0)
            velocity_sum += dv
            max_speed = self.dash_speed
            for rate in self.dash_reflect_info:
                max_speed = max(max_speed * (1 - rate), self.dash_speed * self.min_reflect_rate)

            if velocity_sum.length_sqr > max_speed ** 2:
                velocity_sum = self.dash_forward * max_speed
            self.send_event('E_VERTICAL_SPEED', velocity_sum.y)
            walk_direction = math3d.vector(velocity_sum.x, 0, velocity_sum.z)
            self.send_event('E_CHARACTER_WALK', walk_direction)
        elif self.sub_state == self.ST_SLOW:
            if self.trigger_hit and global_data.player.get_setting_2(uoc.BOOST_HIT_AUTO_TRIGGER_TRANSFORM_8012):
                self.ev_g_action_down('action6')
            velocity_sum = walk_direction + math3d.vector(0, vertical_speed, 0)
            move_dir = math3d.vector(velocity_sum)
            if not move_dir.is_zero:
                move_dir.normalize()
            if velocity_sum.length_sqr > 25 * NEOX_UNIT_SCALE * (25 * NEOX_UNIT_SCALE):
                dv = -move_dir * self.post_slow_acc * dt
                if velocity_sum.length_sqr < dv.length_sqr:
                    velocity_sum = math3d.vector(0, 0, 0)
                else:
                    velocity_sum += dv
                if velocity_sum.length_sqr <= 25 * NEOX_UNIT_SCALE * (25 * NEOX_UNIT_SCALE):
                    velocity_sum = move_dir * 25 * NEOX_UNIT_SCALE
                    self.sub_state = self.ST_NONE
                self.send_event('E_VERTICAL_SPEED', velocity_sum.y)
                walk_direction = math3d.vector(velocity_sum.x, 0, velocity_sum.z)
                self.send_event('E_CHARACTER_WALK', walk_direction)
            else:
                self.sub_state = self.ST_NONE
            speed = velocity_sum.length / NEOX_UNIT_SCALE
            right = math3d.vector(0, 1, 0).cross(move_dir)
            rot = math3d.rotation(0, 0, 0, 1)
            rot.set_axis_angle(right, dt * speed * 0.5)
            cur_rot = math3d.matrix_to_rotation(self.sd.ref_cur_rotation_matrix)
            cur_rot = rot * cur_rot
            self.sd.ref_cur_rotation_matrix = math3d.rotation_to_matrix(cur_rot)
        self.send_event('E_BALL_SYNC_TRANSFORM')

    def check_transitions(self):
        if self.sub_state == self.ST_NONE:
            self.disable_self()

    def refresh_param_changed(self):
        self.dash_speed = self.init_dash_speed * (1 + self.dash_speed_add_factor)
        self.pre_time = self.init_pre_time * (1 + self.pre_time_add_factor)
        self._register_callbacks()

    def on_hit_target(self, target):
        if not self.is_active or not target or self.sub_state not in (self.ST_DASH, self.ST_SLOW) or target.id in self.hit_targets and time.time() - self.hit_targets[target.id] < self.damage_interval:
            return
        else:
            self.hit_targets[target.id] = time.time()
            if target.MASK & MECHA_VEHICLE_MONSTER_TAG_VALUE == 0:
                return
            self.trigger_hit = True
            scene = world.get_active_scene()
            move_dir = scene.active_camera.rotation_matrix.forward
            move_dir.normalize()
            cur_v = -move_dir * self.rebound_h_speed
            cur_v.y = self.rebound_v_speed
            self.send_event('E_CHARACTER_WALK', cur_v)
            self.sub_state = self.ST_SLOW
            forward = scene.active_camera.rotation_matrix.forward
            point = self.ev_g_position() + forward * BALL_RADIUS
            normal = -forward
            self.send_event('E_SHOW_BALL_DAH_HIT_SFX', (point.x, point.y, point.z), (normal.x, normal.y, normal.z))
            if self.pve_breakthrough_enabled:
                field_pos = None
                if self.ev_g_on_ground():
                    field_pos = self.ev_g_position()
                else:
                    cur_pos = self.ev_g_position()
                    hit_ret = global_data.game_mgr.scene.scene_col.hit_by_ray(cur_pos, cur_pos + math3d.vector(0, -10 * NEOX_UNIT_SCALE, 0), 0, GROUP_CAMERA_COLL, GROUP_CAMERA_COLL, collision.INCLUDE_FILTER, False)
                    if hit_ret[0]:
                        field_pos = hit_ret[1]
                if field_pos:
                    self.send_event('E_DO_SKILL', self.pve_fire_field_skill_id, {'position': [field_pos.x, field_pos.y, field_pos.z]})
            return

    def on_immobilized(self, immobilized, *args):
        if self.is_active and immobilized:
            self.sub_state = self.ST_NONE

    def clear_move_timer(self):
        if self.move_timer:
            global_data.game_mgr.get_fix_logic_timer().unregister(self.move_timer)
        self.move_timer = 0

    def on_fuel_exhausted(self):
        if self.is_active and self.sub_state == self.ST_PRE:
            self.pre_end()

    def get_acc_duration_percent(self):
        if self.is_active:
            return self.acc_duration_percent
        else:
            return None


@editor.state_exporter({('pre_anim_duration', 'param'): {'zh_name': '\xe5\x89\x8d\xe6\x91\x87\xe5\x8a\xa8\xe4\xbd\x9c\xe6\x97\xb6\xe9\x95\xbf','post_setter': lambda self: self._register_callbacks()
                                    },
   ('pre_anim_rate', 'param'): {'zh_name': '\xe5\x89\x8d\xe6\x91\x87\xe5\x8a\xa8\xe4\xbd\x9c\xe6\x92\xad\xe6\x94\xbe\xe9\x80\x9f\xe7\x8e\x87','post_setter': lambda self: self._register_callbacks()
                                },
   ('post_anim_duration', 'param'): {'zh_name': '\xe5\x90\x8e\xe6\x91\x87\xe5\x8a\xa8\xe4\xbd\x9c\xe6\x97\xb6\xe9\x95\xbf','post_setter': lambda self: self._register_callbacks()
                                     },
   ('post_anim_rate', 'param'): {'zh_name': '\xe5\x90\x8e\xe6\x91\x87\xe5\x8a\xa8\xe4\xbd\x9c\xe6\x92\xad\xe6\x94\xbe\xe9\x80\x9f\xe7\x8e\x87','post_setter': lambda self: self._register_callbacks()
                                 },
   ('post_break_time', 'param'): {'zh_name': '\xe5\x90\x8e\xe6\x91\x87\xe5\x8a\xa8\xe4\xbd\x9c\xe5\x8f\xaf\xe6\x89\x93\xe6\x96\xad\xe6\x97\xb6\xe9\x97\xb4\xe7\x82\xb9','post_setter': lambda self: self._register_callbacks()
                                  },
   ('common_cd', 'param'): {'zh_name': '\xe6\x99\xae\xe9\x80\x9aCD\xe9\x95\xbf\xe5\xba\xa6'},('energy_exhausted_cd', 'param'): {'zh_name': '\xe8\x83\xbd\xe9\x87\x8f\xe6\xb6\x88\xe8\x80\x97\xe5\xae\x8c\xe5\x90\x8eCD\xe9\x95\xbf\xe5\xba\xa6'}})
class Flamethrower8012(StateBase):
    BIND_EVENT = {'TRY_STOP_WEAPON_ATTACK': 'end_shoot',
       'E_ENERGY_EXHAUSTED': 'on_energy_exhausted',
       'G_CAN_CONTINUOUSLY_SHOOT': 'check_can_shoot',
       'G_NEED_AUTO_CONTINUE_SECOND_WEAPON': 'get_need_auto_continue',
       'E_KEEP_TRYING_SECOND_WEAPON': 'keep_trying_second_weapon'
       }
    STATE_PRE = 0
    STATE_HOLD = 1
    STATE_POST = 2
    STATE_NONE = -1
    SPHERE_FLAMETHROWER_PARAM_INITIALIZED = False
    SPHERE_FLAMETHROWER_RADIUS = 30 * NEOX_UNIT_SCALE
    SPHERE_FLAMETHROWER_HEIGHT = 10 * NEOX_UNIT_SCALE
    SPHERE_FLAMETHROWER_CD = 0.3
    PLAY_HIT_SOUND_INTERVAL = 0.2

    def read_data_from_custom_param(self):
        self.weapon_pos = self.custom_param.get('weapon_pos', g_const.PART_WEAPON_POS_MAIN2)
        self.skill_id = self.custom_param.get('skill_id', None)
        self.pre_anim = self.custom_param.get('pre_anim', None)
        self.pre_anim_duration = self.custom_param.get('pre_anim_duration', 0.5)
        self.pre_anim_rate = self.custom_param.get('pre_anim_rate', 1.0)
        self.hold_anim = self.custom_param.get('hold_anim', None)
        self.post_anim = self.custom_param.get('post_anim', None)
        self.post_anim_duration = self.custom_param.get('post_anim_duration', 1.5)
        self.post_anim_rate = self.custom_param.get('post_anim_rate', 1.0)
        self.post_break_time = self.custom_param.get('post_break_time', 0.5)
        self.all_anim_set = {self.pre_anim, self.hold_anim, self.post_anim}
        self.common_cd = self.custom_param.get('common_cd', 0.2)
        self.energy_exhausted_cd = self.custom_param.get('energy_exhausted_cd', 0.5)
        self._register_callbacks()
        state_exit_trigger_setting_type = self.custom_param.get('state_exit_trigger_setting_type', None)
        self._exit_trigger_setting_key = self.convert_to_exit_trigger_setting_key(state_exit_trigger_setting_type)
        return

    def _register_callbacks(self):
        self.reset_sub_states_callback()
        self.register_substate_callback(self.STATE_PRE, 0, self.begin_pre_anim)
        self.register_substate_callback(self.STATE_PRE, self.pre_anim_duration / self.pre_anim_rate, self._start_fire)
        self.register_substate_callback(self.STATE_HOLD, 0, self.begin_hold_anim)
        self.register_substate_callback(self.STATE_POST, 0, self.begin_post_anim)
        self.register_substate_callback(self.STATE_POST, self.post_break_time, self.enable_break_post_process)
        self.register_substate_callback(self.STATE_POST, self.post_anim_duration / self.post_anim_rate, self.disable_self)

    def init_from_dict(self, unit_obj, bdict, sid, info):
        super(Flamethrower8012, self).init_from_dict(unit_obj, bdict, sid, info)
        self.is_firing = False
        self.keep_trying_fire = False
        self.last_exit_time = 0.0
        self.last_energy_exhausted_time = 0.0
        self.pressing_action_btn = False
        self.btn_down_timer = None
        self.trying_timer = None
        self.read_data_from_custom_param()
        self.sphere_flamethrower_enabled = False
        self.enable_param_changed_by_buff()
        if not self.SPHERE_FLAMETHROWER_PARAM_INITIALIZED:
            conf = confmgr.get('skill_conf', str(self.skill_id), 'ext_info', default={})
            self.SPHERE_FLAMETHROWER_RADIUS = conf.get('radius', 30) * NEOX_UNIT_SCALE
            self.SPHERE_FLAMETHROWER_HEIGHT = conf.get('height', 10) * NEOX_UNIT_SCALE
            self.SPHERE_FLAMETHROWER_CD = conf.get('cd', 0.3)
            self.SPHERE_FLAMETHROWER_PARAM_INITIALIZED = True
        self.static_tester = None
        self.last_play_hit_human_sound_time = 0.0
        self.last_play_hit_others_sound_time = 0.0
        self.is_pve = global_data.game_mode.is_pve()
        self.start_ball_fire_ts = 0
        self.ball_fire_cnt = 2
        self.ball_fire_angle = 0
        self.ball_fire_range_add_rate = 0.0
        self.ball_fire_rot_speed = 0
        self.ball_fire_rot_add_rate = 0.0
        self.last_hit_ts = None
        self.burn_ground_inter = -1
        self.pve_fire_field_skill_id = 801259
        self.need_do_fire_field_skill = []
        return

    def refresh_param_changed(self):
        if self.sphere_flamethrower_enabled and self.ev_g_is_avatar():
            radius = self.SPHERE_FLAMETHROWER_RADIUS * (1.0 + self.ball_fire_range_add_rate)
            col = collision.col_object(collision.BOX, math3d.vector(radius, self.SPHERE_FLAMETHROWER_HEIGHT / 2 * (1.0 + self.ball_fire_range_add_rate), radius), 0, 0, 1)
            if not self.static_tester:
                self.static_tester = CollisionTester(col, self.unit_obj.id, ignore_groupmates=True)
            else:
                self.static_tester.col = col
        elif self.sd.ref_is_ball_mode:
            self.end_shoot()

    def destroy(self):
        self._release_btn_down_timer()
        self._release_tyring_timer()
        if self.static_tester:
            self.static_tester.destroy()
            self.static_tester = None
        super(Flamethrower8012, self).destroy()
        return

    @classmethod
    def convert_to_exit_trigger_setting_key(cls, state_exit_trigger_setting_type):
        if state_exit_trigger_setting_type == 8012:
            return uoc.CONTINUOUSLY_SHOOT_TRIGGER_PRESS_8012
        else:
            return None
            return None

    def exit_by_setting_when_btn_up(self):
        if self._exit_trigger_setting_key is not None and self.ev_g_is_avatar():
            setting_val = global_data.player.get_setting_2(self._exit_trigger_setting_key)
            if setting_val is not None:
                if setting_val:
                    return True
        return False

    def check_can_shoot(self, need_check_common_cd=False):
        cur_time = time.time()
        if cur_time - self.last_energy_exhausted_time <= self.energy_exhausted_cd:
            return False
        if need_check_common_cd and cur_time - self.last_exit_time <= self.common_cd:
            return False
        return True

    def _release_btn_down_timer(self):
        if self.btn_down_timer:
            global_data.game_mgr.unregister_logic_timer(self.btn_down_timer)
            self.btn_down_timer = None
        return

    def _register_btn_down_timer(self):
        self._release_btn_down_timer()
        self.btn_down_timer = global_data.game_mgr.register_logic_timer(self._simulate_action_btn_down, interval=1, times=-1)

    def _simulate_action_btn_down(self):
        if self.is_active:
            self.btn_down_timer = None
            return RELEASE
        else:
            if self.ev_g_try_exit_ball_state():
                return
            if not self.check_can_active():
                return
            if not self.check_can_cast_skill():
                return
            if not self.is_active:
                if self.check_can_shoot(need_check_common_cd=True):
                    self.active_self()
            return

    def action_btn_down(self):
        if self.sphere_flamethrower_enabled:
            if not self.exit_by_setting_when_btn_up():
                self._release_tyring_timer()
                if not self.pressing_action_btn:
                    if self.is_active:
                        if self.sub_state == self.STATE_HOLD:
                            self.sub_state = self.STATE_POST
                        else:
                            self.disable_self()
                        return
                    if self.trying_timer:
                        self.disable_self()
                        return
                self.pressing_action_btn = True
        elif not self.exit_by_setting_when_btn_up():
            if not self.pressing_action_btn:
                if self.is_active:
                    if self.sub_state == self.STATE_HOLD:
                        self.sub_state = self.STATE_POST
                    else:
                        self.disable_self()
                    return
                if self.ev_g_try_exit_ball_state():
                    if not self.btn_down_timer:
                        self._register_btn_down_timer()
                    return
            else:
                self._release_btn_down_timer()
            self.pressing_action_btn = True
        elif self.ev_g_try_exit_ball_state():
            return False
        if not self.check_can_active():
            return
        if not self.check_can_cast_skill():
            return
        if not self.is_active:
            if self.check_can_shoot(need_check_common_cd=True):
                self.active_self()
        super(Flamethrower8012, self).action_btn_down()
        return True

    def action_btn_up(self):
        if not self.exit_by_setting_when_btn_up():
            self.pressing_action_btn = False
            return
        if self.is_active:
            if self.sub_state == self.STATE_HOLD:
                self.sub_state = self.STATE_POST
            else:
                self.disable_self()
        super(Flamethrower8012, self).action_btn_up()
        return True

    def enter(self, leave_states):
        super(Flamethrower8012, self).enter(leave_states)
        self._release_btn_down_timer()
        self._release_tyring_timer()
        if self.is_pve and self.sd.ref_is_ball_mode:
            skill_conf = confmgr.get('skill_conf', str(self.skill_id), 'ext_info', default={})
            self.ball_fire_angle = cos(radians(skill_conf.get('ball_fire_angle', 30)))
            self.ball_fire_rot_speed = radians(skill_conf.get('ball_fire_rot_speed', 180))
            self.last_hit_ts = [ {} for i in range(int(self.ball_fire_cnt)) ]
            self.start_ball_fire_ts = time.time()
            self.start_ball_fire_yaw = world.get_active_scene().active_camera.rotation_matrix.yaw
        self.sub_state = self.STATE_PRE
        self.send_event('E_SLOW_DOWN', True)
        self.send_event('E_SET_ACTION_SELECTED', self.bind_action_id, True)

    def _check_can_fire(self):
        if not self.sd.ref_is_ball_mode:
            return self.ev_g_try_weapon_attack_begin(self.weapon_pos)
        if self.sphere_flamethrower_enabled:
            return self.check_can_cast_skill()
        return False

    def _start_fire(self):
        if not self._check_can_fire():
            self.keep_trying_fire = True
            return
        self.start_custom_sound('loop')
        self.send_event('E_DO_SKILL', self.skill_id)
        self.is_firing = True
        self.sub_state = self.STATE_HOLD
        self.last_play_hit_human_sound_time = 0.0
        self.last_play_hit_others_sound_time = 0.0
        self.keep_trying_fire = False
        if not self.sd.ref_is_ball_mode:
            return
        if self.is_pve:
            self.send_event('E_SHOW_SPHERE_FLAMETHROWER', self.start_ball_fire_yaw, int(self.ball_fire_cnt), self.ball_fire_rot_speed * (1.0 + self.ball_fire_rot_add_rate))
        else:
            self.send_event('E_SHOW_SPHERE_FLAMETHROWER', world.get_active_scene().active_camera.rotation_matrix.yaw)

    def _end_fire(self):
        if self.is_firing:
            self.end_custom_sound('loop')
            self.end_custom_sound('post')
            self.start_custom_sound('post')
            if not self.sd.ref_is_ball_mode:
                self.ev_g_try_weapon_attack_end(self.weapon_pos, True)
            self.is_firing = False
            self.send_event('E_END_SKILL', self.skill_id)
            self.send_event('E_SHOW_SPHERE_FLAMETHROWER', fire_cnt=0)

    def begin_pre_anim(self):
        if not self.sd.ref_is_ball_mode:
            self.send_event('E_ANIM_RATE', UP_BODY, self.pre_anim_rate)
            self.send_event('E_POST_ACTION', self.pre_anim, UP_BODY, 1)
        self.send_event('E_CONTINUOUSLY_SHOOT', True)

    def begin_hold_anim(self):
        if not self.sd.ref_is_ball_mode:
            self.send_event('E_ANIM_RATE', UP_BODY, 1.0)
            self.send_event('E_POST_ACTION', self.hold_anim, UP_BODY, 1, loop=True)

    def begin_post_anim(self):
        self._end_fire()
        self.send_event('E_SET_ACTION_SELECTED', self.bind_action_id, False)
        if not self.sd.ref_is_ball_mode:
            self.send_event('E_ANIM_RATE', UP_BODY, self.post_anim_rate)
            self.send_event('E_POST_ACTION', self.post_anim, UP_BODY, 1)

    def enable_break_post_process(self):
        self.send_event('E_ADD_WHITE_STATE', {MC_SHOOT, MC_DASH}, self.sid)

    def _play_sphere_flamethrower_hit_sound(self, hit_human, hit_others):
        cur_time = global_data.game_time
        if hit_human and cur_time - self.last_play_hit_human_sound_time >= self.PLAY_HIT_SOUND_INTERVAL:
            play_hit_sound_2d(801203, True, False)
            if self.last_play_hit_human_sound_time == 0.0:
                self.last_play_hit_human_sound_time = cur_time
            else:
                self.last_play_hit_human_sound_time += self.PLAY_HIT_SOUND_INTERVAL
        if hit_others and cur_time - self.last_play_hit_others_sound_time >= self.PLAY_HIT_SOUND_INTERVAL:
            play_hit_sound_2d(801203, False, False)
            if self.last_play_hit_others_sound_time == 0.0:
                self.last_play_hit_others_sound_time = cur_time
            else:
                self.last_play_hit_others_sound_time += self.PLAY_HIT_SOUND_INTERVAL

    def update--- This code section failed: ---

1420       0  LOAD_GLOBAL           0  'super'
           3  LOAD_GLOBAL           1  'Flamethrower8012'
           6  LOAD_FAST             0  'self'
           9  CALL_FUNCTION_2       2 
          12  LOAD_ATTR             2  'update'
          15  LOAD_FAST             1  'dt'
          18  CALL_FUNCTION_1       1 
          21  POP_TOP          

1421      22  LOAD_FAST             0  'self'
          25  LOAD_ATTR             3  'keep_trying_fire'
          28  POP_JUMP_IF_FALSE    44  'to 44'

1422      31  LOAD_FAST             0  'self'
          34  LOAD_ATTR             4  '_start_fire'
          37  CALL_FUNCTION_0       0 
          40  POP_TOP          
          41  JUMP_FORWARD          0  'to 44'
        44_0  COME_FROM                '41'

1423      44  LOAD_FAST             0  'self'
          47  LOAD_ATTR             5  'sd'
          50  LOAD_ATTR             6  'ref_is_ball_mode'
          53  POP_JUMP_IF_TRUE    609  'to 609'

1424      56  LOAD_FAST             0  'self'
          59  LOAD_ATTR             7  'burn_ground_inter'
          62  LOAD_CONST            1  ''
          65  COMPARE_OP            4  '>'
          68  POP_JUMP_IF_FALSE  1365  'to 1365'

1425      71  LOAD_GLOBAL           8  'time'
          74  LOAD_ATTR             8  'time'
          77  CALL_FUNCTION_0       0 
          80  STORE_FAST            2  'cur_time'

1426      83  SETUP_LOOP          111  'to 197'
          86  LOAD_FAST             0  'self'
          89  LOAD_ATTR             9  'need_do_fire_field_skill'
          92  POP_JUMP_IF_FALSE   196  'to 196'

1427      95  LOAD_FAST             0  'self'
          98  LOAD_ATTR             9  'need_do_fire_field_skill'
         101  LOAD_CONST            1  ''
         104  BINARY_SUBSCR    
         105  UNPACK_SEQUENCE_2     2 
         108  STORE_FAST            3  'create_time'
         111  STORE_FAST            4  'create_pos'

1428     114  LOAD_FAST             3  'create_time'
         117  LOAD_FAST             2  'cur_time'
         120  COMPARE_OP            4  '>'
         123  POP_JUMP_IF_FALSE   130  'to 130'

1429     126  BREAK_LOOP       
         127  JUMP_FORWARD          0  'to 130'
       130_0  COME_FROM                '127'

1430     130  LOAD_FAST             0  'self'
         133  LOAD_ATTR             9  'need_do_fire_field_skill'
         136  LOAD_ATTR            10  'pop'
         139  LOAD_CONST            1  ''
         142  CALL_FUNCTION_1       1 
         145  POP_TOP          

1431     146  LOAD_FAST             0  'self'
         149  LOAD_ATTR            11  'send_event'
         152  LOAD_CONST            2  'E_DO_SKILL'
         155  LOAD_FAST             0  'self'
         158  LOAD_ATTR            12  'pve_fire_field_skill_id'
         161  BUILD_MAP_1           1 
         164  LOAD_FAST             4  'create_pos'
         167  LOAD_ATTR            13  'x'
         170  LOAD_FAST             4  'create_pos'
         173  LOAD_ATTR            14  'y'
         176  LOAD_FAST             4  'create_pos'
         179  LOAD_ATTR            15  'z'
         182  BUILD_LIST_3          3 
         185  LOAD_CONST            3  'position'
         188  STORE_MAP        
         189  CALL_FUNCTION_3       3 
         192  POP_TOP          
         193  JUMP_BACK            86  'to 86'
         196  POP_BLOCK        
       197_0  COME_FROM                '83'

1433     197  LOAD_GLOBAL          16  'hasattr'
         200  LOAD_GLOBAL           4  '_start_fire'
         203  CALL_FUNCTION_2       2 
         206  POP_JUMP_IF_TRUE    379  'to 379'

1434     209  LOAD_FAST             0  'self'
         212  LOAD_ATTR            17  'ev_g_gun_status_inf'
         215  LOAD_GLOBAL          18  'g_const'
         218  LOAD_ATTR            19  'PART_WEAPON_POS_MAIN2'
         221  CALL_FUNCTION_1       1 
         224  STORE_FAST            5  'gun_status'

1435     227  LOAD_FAST             5  'gun_status'
         230  POP_JUMP_IF_FALSE   379  'to 379'
         233  LOAD_FAST             5  'gun_status'
         236  LOAD_ATTR            20  '_wp'
       239_0  COME_FROM                '230'
         239  POP_JUMP_IF_FALSE   379  'to 379'

1436     242  LOAD_CONST            1  ''
         245  LOAD_CONST            5  ('ATTR_GRENADE_MAX_DISTANCE_ADD_FACTOR',)
         248  IMPORT_NAME          21  'logic.gcommon.common_const.attr_const'
         251  IMPORT_FROM          22  'ATTR_GRENADE_MAX_DISTANCE_ADD_FACTOR'
         254  STORE_FAST            6  'ATTR_GRENADE_MAX_DISTANCE_ADD_FACTOR'
         257  POP_TOP          

1437     258  LOAD_FAST             5  'gun_status'
         261  LOAD_ATTR            20  '_wp'
         264  LOAD_ATTR            23  'iType'
         267  STORE_FAST            7  'item_id'

1438     270  LOAD_GLOBAL          24  'confmgr'
         273  LOAD_ATTR            25  'get'
         276  LOAD_CONST            6  'grenade_config'
         279  LOAD_GLOBAL          26  'str'
         282  LOAD_FAST             7  'item_id'
         285  CALL_FUNCTION_1       1 
         288  LOAD_CONST            7  'default'
         291  BUILD_MAP_0           0 
         294  CALL_FUNCTION_258   258 
         297  STORE_FAST            8  'grenade_conf'

1439     300  LOAD_FAST             8  'grenade_conf'
         303  LOAD_ATTR            25  'get'
         306  LOAD_CONST            8  'fMaxDistance'
         309  LOAD_CONST            1  ''
         312  CALL_FUNCTION_2       2 
         315  LOAD_FAST             0  'self'
         318  STORE_ATTR           27  'grenade_max_distance'

1440     321  LOAD_FAST             0  'self'
         324  DUP_TOP          
         325  LOAD_ATTR            27  'grenade_max_distance'
         328  LOAD_CONST            9  1.0
         331  LOAD_FAST             0  'self'
         334  LOAD_ATTR            28  'ev_g_add_attr'
         337  LOAD_FAST             6  'ATTR_GRENADE_MAX_DISTANCE_ADD_FACTOR'
         340  LOAD_FAST             7  'item_id'
         343  CALL_FUNCTION_2       2 
         346  BINARY_ADD       
         347  INPLACE_MULTIPLY 
         348  ROT_TWO          
         349  STORE_ATTR           27  'grenade_max_distance'

1441     352  LOAD_FAST             8  'grenade_conf'
         355  LOAD_ATTR            25  'get'
         358  LOAD_CONST           10  'fSpeed'
         361  LOAD_CONST            9  1.0
         364  CALL_FUNCTION_2       2 
         367  LOAD_FAST             0  'self'
         370  STORE_ATTR           29  'grenade_fly_speed'
         373  JUMP_ABSOLUTE       379  'to 379'
         376  JUMP_FORWARD          0  'to 379'
       379_0  COME_FROM                '376'

1442     379  LOAD_FAST             0  'self'
         382  LOAD_ATTR            30  'ev_g_mecha_fire_ray'
         385  LOAD_GLOBAL          18  'g_const'
         388  LOAD_ATTR            19  'PART_WEAPON_POS_MAIN2'
         391  LOAD_CONST           11  -1
         394  LOAD_GLOBAL          31  'True'
         397  LOAD_GLOBAL          31  'True'
         400  CALL_FUNCTION_4       4 
         403  UNPACK_SEQUENCE_3     3 
         406  STORE_FAST            9  'fire_pos'
         409  STORE_FAST           10  'fire_dir'
         412  STORE_FAST           11  '_'

1443     415  LOAD_GLOBAL          32  'global_data'
         418  LOAD_ATTR            33  'game_mgr'
         421  LOAD_ATTR            34  'scene'
         424  LOAD_ATTR            35  'scene_col'
         427  LOAD_ATTR            36  'hit_by_ray'

1444     430  LOAD_FAST             9  'fire_pos'
         433  LOAD_FAST             9  'fire_pos'
         436  LOAD_FAST            10  'fire_dir'
         439  LOAD_FAST             0  'self'
         442  LOAD_ATTR            27  'grenade_max_distance'
         445  BINARY_MULTIPLY  
         446  BINARY_ADD       
         447  LOAD_CONST            1  ''

1445     450  LOAD_GLOBAL          37  'GROUP_CAMERA_COLL'
         453  LOAD_GLOBAL          37  'GROUP_CAMERA_COLL'
         456  LOAD_GLOBAL          38  'collision'
         459  LOAD_ATTR            39  'INCLUDE_FILTER'
         462  LOAD_GLOBAL          40  'False'
         465  CALL_FUNCTION_7       7 
         468  STORE_FAST           12  'hit_ret'

1446     471  LOAD_FAST            12  'hit_ret'
         474  LOAD_CONST            1  ''
         477  BINARY_SUBSCR    
         478  POP_JUMP_IF_FALSE   606  'to 606'
         481  LOAD_FAST            12  'hit_ret'
         484  LOAD_CONST           12  2
         487  BINARY_SUBSCR    
         488  LOAD_ATTR            14  'y'
         491  LOAD_CONST           13  0.6
         494  COMPARE_OP            4  '>'
       497_0  COME_FROM                '478'
         497  POP_JUMP_IF_FALSE   606  'to 606'

1447     500  LOAD_FAST             2  'cur_time'
         503  LOAD_FAST             0  'self'
         506  LOAD_ATTR            27  'grenade_max_distance'
         509  LOAD_FAST            12  'hit_ret'
         512  LOAD_CONST           14  3
         515  BINARY_SUBSCR    
         516  BINARY_MULTIPLY  
         517  LOAD_FAST             0  'self'
         520  LOAD_ATTR            29  'grenade_fly_speed'
         523  BINARY_DIVIDE    
         524  BINARY_ADD       
         525  STORE_FAST            3  'create_time'

1448     528  LOAD_GLOBAL          41  'getattr'
         531  LOAD_GLOBAL          15  'z'
         534  LOAD_CONST            1  ''
         537  CALL_FUNCTION_3       3 
         540  STORE_FAST           13  'last_burn_time'

1449     543  LOAD_FAST             3  'create_time'
         546  LOAD_FAST            13  'last_burn_time'
         549  BINARY_SUBTRACT  
         550  LOAD_FAST             0  'self'
         553  LOAD_ATTR             7  'burn_ground_inter'
         556  COMPARE_OP            5  '>='
         559  POP_JUMP_IF_FALSE   603  'to 603'

1450     562  LOAD_FAST             0  'self'
         565  LOAD_ATTR             9  'need_do_fire_field_skill'
         568  LOAD_ATTR            42  'append'
         571  LOAD_FAST            13  'last_burn_time'
         574  LOAD_FAST            12  'hit_ret'
         577  LOAD_CONST           16  1
         580  BINARY_SUBSCR    
         581  BUILD_LIST_2          2 
         584  CALL_FUNCTION_1       1 
         587  POP_TOP          

1451     588  LOAD_FAST             3  'create_time'
         591  LOAD_FAST             0  'self'
         594  STORE_ATTR           43  'last_burn_time'
         597  JUMP_ABSOLUTE       603  'to 603'
         600  JUMP_ABSOLUTE       606  'to 606'
         603  JUMP_ABSOLUTE      1365  'to 1365'
         606  JUMP_FORWARD        756  'to 1365'

1452     609  LOAD_FAST             0  'self'
         612  LOAD_ATTR            44  'sphere_flamethrower_enabled'
         615  POP_JUMP_IF_FALSE  1365  'to 1365'
         618  LOAD_FAST             0  'self'
         621  LOAD_ATTR            45  'is_firing'
       624_0  COME_FROM                '615'
         624  POP_JUMP_IF_FALSE  1365  'to 1365'

1453     627  LOAD_FAST             0  'self'
         630  LOAD_ATTR            46  'ev_g_position'
         633  CALL_FUNCTION_0       0 
         636  STORE_FAST           14  'cur_pos'

1454     639  LOAD_FAST             0  'self'
         642  LOAD_ATTR            47  'is_pve'
         645  POP_JUMP_IF_FALSE  1184  'to 1184'

1455     648  LOAD_FAST             0  'self'
         651  LOAD_ATTR            48  'static_tester'
         654  LOAD_ATTR            49  'get_hit_obj_eid_list_with_cd_by_static_test_2'
         657  LOAD_FAST            14  'cur_pos'
         660  LOAD_CONST           17  'hit_cd'
         663  LOAD_CONST           18  ''
         666  CALL_FUNCTION_257   257 
         669  UNPACK_SEQUENCE_2     2 
         672  STORE_FAST           11  '_'
         675  STORE_FAST           15  'unit_list'

1456     678  LOAD_GLOBAL           8  'time'
         681  LOAD_ATTR             8  'time'
         684  CALL_FUNCTION_0       0 
         687  STORE_FAST            2  'cur_time'

1457     690  LOAD_FAST             2  'cur_time'
         693  LOAD_FAST             0  'self'
         696  LOAD_ATTR            50  'start_ball_fire_ts'
         699  BINARY_SUBTRACT  
         700  LOAD_FAST             0  'self'
         703  LOAD_ATTR            51  'ball_fire_rot_speed'
         706  BINARY_MULTIPLY  
         707  LOAD_CONST            9  1.0
         710  LOAD_FAST             0  'self'
         713  LOAD_ATTR            52  'ball_fire_rot_add_rate'
         716  BINARY_ADD       
         717  BINARY_MULTIPLY  
         718  STORE_FAST           16  'cur_fire_rot'

1458     721  LOAD_GLOBAL          53  'pi'
         724  LOAD_CONST           19  2.0
         727  BINARY_MULTIPLY  
         728  LOAD_FAST             0  'self'
         731  LOAD_ATTR            54  'ball_fire_cnt'
         734  BINARY_DIVIDE    
         735  STORE_FAST           17  'fire_inter'

1459     738  BUILD_LIST_0          0 
         741  STORE_FAST           18  'fire_vec'

1460     744  SETUP_LOOP           83  'to 830'
         747  LOAD_GLOBAL          55  'range'
         750  LOAD_GLOBAL          56  'int'
         753  LOAD_FAST             0  'self'
         756  LOAD_ATTR            54  'ball_fire_cnt'
         759  CALL_FUNCTION_1       1 
         762  CALL_FUNCTION_1       1 
         765  GET_ITER         
         766  FOR_ITER             60  'to 829'
         769  STORE_FAST           19  'fire_idx'

1461     772  LOAD_FAST            16  'cur_fire_rot'
         775  LOAD_FAST            17  'fire_inter'
         778  LOAD_FAST            19  'fire_idx'
         781  BINARY_MULTIPLY  
         782  BINARY_ADD       
         783  STORE_FAST           20  'rot'

1462     786  LOAD_FAST            18  'fire_vec'
         789  LOAD_ATTR            42  'append'
         792  LOAD_GLOBAL          57  'math3d'
         795  LOAD_ATTR            58  'vector'
         798  LOAD_GLOBAL          59  'sin'
         801  LOAD_FAST            20  'rot'
         804  CALL_FUNCTION_1       1 
         807  LOAD_CONST            1  ''
         810  LOAD_GLOBAL          60  'cos'
         813  LOAD_FAST            20  'rot'
         816  CALL_FUNCTION_1       1 
         819  CALL_FUNCTION_3       3 
         822  CALL_FUNCTION_1       1 
         825  POP_TOP          
         826  JUMP_BACK           766  'to 766'
         829  POP_BLOCK        
       830_0  COME_FROM                '744'

1463     830  BUILD_LIST_0          0 
         833  STORE_FAST           21  'valid_unit_list'

1464     836  BUILD_LIST_0          0 
         839  STORE_FAST           22  'valid_eid_list'

1465     842  LOAD_FAST             0  'self'
         845  LOAD_ATTR            46  'ev_g_position'
         848  CALL_FUNCTION_0       0 
         851  STORE_FAST           23  'ball_pos'

1466     854  SETUP_LOOP          311  'to 1168'
         857  LOAD_FAST            15  'unit_list'
         860  GET_ITER         
         861  FOR_ITER            303  'to 1167'
         864  STORE_FAST           24  'unit'

1467     867  LOAD_FAST            24  'unit'
         870  LOAD_ATTR            46  'ev_g_position'
         873  CALL_FUNCTION_0       0 
         876  LOAD_FAST            23  'ball_pos'
         879  BINARY_SUBTRACT  
         880  STORE_FAST           25  'unit_vec'

1468     883  LOAD_CONST           18  ''
         886  LOAD_FAST            25  'unit_vec'
         889  STORE_ATTR           14  'y'

1469     892  LOAD_FAST            25  'unit_vec'
         895  LOAD_ATTR            61  'is_zero'
         898  POP_JUMP_IF_FALSE   936  'to 936'

1470     901  LOAD_FAST            21  'valid_unit_list'
         904  LOAD_ATTR            42  'append'
         907  LOAD_FAST            24  'unit'
         910  CALL_FUNCTION_1       1 
         913  POP_TOP          

1471     914  LOAD_FAST            22  'valid_eid_list'
         917  LOAD_ATTR            42  'append'
         920  LOAD_FAST            24  'unit'
         923  LOAD_ATTR            62  'id'
         926  CALL_FUNCTION_1       1 
         929  POP_TOP          

1472     930  CONTINUE            861  'to 861'
         933  JUMP_FORWARD          0  'to 936'
       936_0  COME_FROM                '933'

1473     936  LOAD_FAST            25  'unit_vec'
         939  LOAD_ATTR            63  'normalize'
         942  CALL_FUNCTION_0       0 
         945  POP_TOP          

1474     946  LOAD_GLOBAL          40  'False'
         949  STORE_FAST           26  'valid'

1475     952  SETUP_LOOP          171  'to 1126'
         955  LOAD_GLOBAL          55  'range'
         958  LOAD_GLOBAL          56  'int'
         961  LOAD_FAST             0  'self'
         964  LOAD_ATTR            54  'ball_fire_cnt'
         967  CALL_FUNCTION_1       1 
         970  CALL_FUNCTION_1       1 
         973  GET_ITER         
         974  FOR_ITER            148  'to 1125'
         977  STORE_FAST           19  'fire_idx'

1476     980  LOAD_FAST            18  'fire_vec'
         983  LOAD_FAST            19  'fire_idx'
         986  BINARY_SUBSCR    
         987  LOAD_ATTR            64  'cross'
         990  LOAD_FAST            25  'unit_vec'
         993  CALL_FUNCTION_1       1 
         996  STORE_FAST           27  'cross_val'

1477     999  LOAD_FAST            18  'fire_vec'
        1002  LOAD_FAST            19  'fire_idx'
        1005  BINARY_SUBSCR    
        1006  LOAD_ATTR            65  'dot'
        1009  LOAD_FAST            25  'unit_vec'
        1012  CALL_FUNCTION_1       1 
        1015  STORE_FAST           28  'dot_val'

1478    1018  LOAD_FAST            27  'cross_val'
        1021  LOAD_ATTR            14  'y'
        1024  LOAD_CONST            1  ''
        1027  COMPARE_OP            0  '<'
        1030  POP_JUMP_IF_TRUE    974  'to 974'
        1033  LOAD_FAST            28  'dot_val'
        1036  LOAD_FAST             0  'self'
        1039  LOAD_ATTR            66  'ball_fire_angle'
        1042  COMPARE_OP            0  '<'
        1045  POP_JUMP_IF_TRUE    974  'to 974'

1479    1048  LOAD_FAST             2  'cur_time'
        1051  LOAD_FAST             0  'self'
        1054  LOAD_ATTR            67  'last_hit_ts'
        1057  LOAD_FAST            19  'fire_idx'
        1060  BINARY_SUBSCR    
        1061  LOAD_ATTR            25  'get'
        1064  LOAD_FAST            24  'unit'
        1067  LOAD_ATTR            62  'id'
        1070  LOAD_CONST           18  ''
        1073  CALL_FUNCTION_2       2 
        1076  BINARY_SUBTRACT  
        1077  LOAD_FAST             0  'self'
        1080  LOAD_ATTR            68  'SPHERE_FLAMETHROWER_CD'
        1083  COMPARE_OP            0  '<'
      1086_0  COME_FROM                '1045'
      1086_1  COME_FROM                '1030'
        1086  POP_JUMP_IF_FALSE  1095  'to 1095'

1480    1089  CONTINUE            974  'to 974'
        1092  JUMP_FORWARD          0  'to 1095'
      1095_0  COME_FROM                '1092'

1481    1095  LOAD_FAST             2  'cur_time'
        1098  LOAD_FAST             0  'self'
        1101  LOAD_ATTR            67  'last_hit_ts'
        1104  LOAD_FAST            19  'fire_idx'
        1107  BINARY_SUBSCR    
        1108  LOAD_FAST            24  'unit'
        1111  LOAD_ATTR            62  'id'
        1114  STORE_SUBSCR     

1482    1115  LOAD_GLOBAL          31  'True'
        1118  STORE_FAST           26  'valid'

1483    1121  BREAK_LOOP       
        1122  JUMP_BACK           974  'to 974'
        1125  POP_BLOCK        
      1126_0  COME_FROM                '952'

1484    1126  LOAD_FAST            26  'valid'
        1129  POP_JUMP_IF_FALSE   861  'to 861'

1485    1132  LOAD_FAST            21  'valid_unit_list'
        1135  LOAD_ATTR            42  'append'
        1138  LOAD_FAST            24  'unit'
        1141  CALL_FUNCTION_1       1 
        1144  POP_TOP          

1486    1145  LOAD_FAST            22  'valid_eid_list'
        1148  LOAD_ATTR            42  'append'
        1151  LOAD_FAST            24  'unit'
        1154  LOAD_ATTR            62  'id'
        1157  CALL_FUNCTION_1       1 
        1160  POP_TOP          
        1161  JUMP_BACK           861  'to 861'
        1164  JUMP_BACK           861  'to 861'
        1167  POP_BLOCK        
      1168_0  COME_FROM                '854'

1487    1168  LOAD_FAST            22  'valid_eid_list'
        1171  LOAD_FAST            21  'valid_unit_list'
        1174  ROT_TWO          
        1175  STORE_FAST           29  'eid_list'
        1178  STORE_FAST           15  'unit_list'
        1181  JUMP_FORWARD         33  'to 1217'

1489    1184  LOAD_FAST             0  'self'
        1187  LOAD_ATTR            48  'static_tester'
        1190  LOAD_ATTR            49  'get_hit_obj_eid_list_with_cd_by_static_test_2'
        1193  LOAD_FAST            14  'cur_pos'
        1196  LOAD_CONST           17  'hit_cd'
        1199  LOAD_FAST             0  'self'
        1202  LOAD_ATTR            68  'SPHERE_FLAMETHROWER_CD'
        1205  CALL_FUNCTION_257   257 
        1208  UNPACK_SEQUENCE_2     2 
        1211  STORE_FAST           29  'eid_list'
        1214  STORE_FAST           15  'unit_list'
      1217_0  COME_FROM                '1181'

1490    1217  LOAD_FAST            29  'eid_list'
        1220  POP_JUMP_IF_TRUE   1227  'to 1227'

1491    1223  LOAD_CONST            0  ''
        1226  RETURN_END_IF    
      1227_0  COME_FROM                '1220'

1493    1227  LOAD_GLOBAL          40  'False'
        1230  STORE_FAST           30  'hit_human'

1494    1233  LOAD_GLOBAL          40  'False'
        1236  STORE_FAST           31  'hit_others'

1495    1239  SETUP_LOOP           61  'to 1303'
        1242  LOAD_FAST            15  'unit_list'
        1245  GET_ITER         
        1246  FOR_ITER             53  'to 1302'
        1249  STORE_FAST           24  'unit'

1496    1252  LOAD_FAST            24  'unit'
        1255  LOAD_ATTR            69  'MASK'
        1258  LOAD_GLOBAL          70  'preregistered_tags'
        1261  LOAD_ATTR            71  'HUMAN_TAG_VALUE'
        1264  BINARY_AND       
        1265  POP_JUMP_IF_FALSE  1277  'to 1277'

1497    1268  LOAD_GLOBAL          31  'True'
        1271  STORE_FAST           30  'hit_human'
        1274  JUMP_FORWARD          6  'to 1283'

1499    1277  LOAD_GLOBAL          31  'True'
        1280  STORE_FAST           31  'hit_others'
      1283_0  COME_FROM                '1274'

1500    1283  LOAD_FAST            30  'hit_human'
        1286  POP_JUMP_IF_FALSE  1246  'to 1246'
        1289  LOAD_FAST            31  'hit_others'
      1292_0  COME_FROM                '1286'
        1292  POP_JUMP_IF_FALSE  1246  'to 1246'

1501    1295  BREAK_LOOP       
        1296  JUMP_BACK          1246  'to 1246'
        1299  JUMP_BACK          1246  'to 1246'
        1302  POP_BLOCK        
      1303_0  COME_FROM                '1239'

1502    1303  LOAD_FAST             0  'self'
        1306  LOAD_ATTR            72  '_play_sphere_flamethrower_hit_sound'
        1309  LOAD_FAST            30  'hit_human'
        1312  LOAD_FAST            31  'hit_others'
        1315  CALL_FUNCTION_2       2 
        1318  POP_TOP          

1503    1319  LOAD_FAST             0  'self'
        1322  LOAD_ATTR            11  'send_event'
        1325  LOAD_CONST           20  'E_CALL_SYNC_METHOD'
        1328  LOAD_CONST           21  'skill_hit_on_target'
        1331  LOAD_FAST             0  'self'
        1334  LOAD_ATTR            73  'skill_id'
        1337  LOAD_FAST            29  'eid_list'
        1340  LOAD_GLOBAL           8  'time'
        1343  LOAD_ATTR             8  'time'
        1346  CALL_FUNCTION_0       0 
        1349  BUILD_TUPLE_3         3 
        1352  LOAD_GLOBAL          40  'False'
        1355  LOAD_GLOBAL          31  'True'
        1358  CALL_FUNCTION_5       5 
        1361  POP_TOP          
        1362  JUMP_FORWARD          0  'to 1365'
      1365_0  COME_FROM                '1362'
      1365_1  COME_FROM                '606'

Parse error at or near `CALL_FUNCTION_2' instruction at offset 203

    def exit(self, enter_states):
        super(Flamethrower8012, self).exit(enter_states)
        self.send_event('E_SET_ACTION_SELECTED', self.bind_action_id, False)
        self.send_event('E_CONTINUOUSLY_SHOOT', False)
        self._end_fire()
        self.send_event('E_BEGIN_RECOVER_MP', self.skill_id)
        self.keep_trying_fire = False
        self.ev_g_try_weapon_attack_end(self.weapon_pos, True)
        self.sub_state = self.STATE_NONE
        if self.sd.ref_up_body_anim in self.all_anim_set:
            self.send_event('E_ANIM_RATE', UP_BODY, 1.0)
            self.send_event('E_CLEAR_UP_BODY_ANIM')
        self.send_event('E_CLEAR_WHITE_STATE', self.sid)
        self.send_event('E_SLOW_DOWN', False)
        self.last_exit_time = time.time()
        if not self.exit_by_setting_when_btn_up() and MC_BEAT_BACK in enter_states:
            self._register_btn_down_timer()

    def end_shoot(self, *args):
        if self.is_active:
            if self.sub_state == self.STATE_HOLD:
                self.sub_state = self.STATE_POST
            else:
                self.disable_self()
        self._release_tyring_timer()

    def on_energy_exhausted(self, skill_id):
        if not self.is_active:
            return
        if skill_id != self.skill_id:
            return
        self.last_energy_exhausted_time = time.time()
        self.end_shoot()

    def get_need_auto_continue(self):
        return not self.exit_by_setting_when_btn_up()

    def try_start_second_weapon(self):
        if not self.check_can_active():
            return
        if not self.check_can_cast_skill():
            return
        if not self.is_active:
            if self.check_can_shoot(need_check_common_cd=True):
                self.active_self()

    def _release_tyring_timer(self):
        if self.trying_timer:
            global_data.game_mgr.unregister_logic_timer(self.trying_timer)
            self.trying_timer = None
        return

    def keep_trying_second_weapon(self):
        self._release_tyring_timer()
        self.trying_timer = global_data.game_mgr.register_logic_timer(self.try_start_second_weapon, interval=1, times=-1)


class WeaponFire8012(WeaponFire):

    def read_data_from_custom_param(self):
        super(WeaponFire8012, self).read_data_from_custom_param()
        self.enhanced_weapon_id = 801202
        self.enhanced_skill_id = 801251

    def init_from_dict(self, unit_obj, bdict, sid, state_info):
        super(WeaponFire8012, self).init_from_dict(unit_obj, bdict, sid, state_info)
        self.oil_bottle_enabled = False
        self.enable_param_changed_by_buff()
        self.enhanced_weapon_cd = confmgr.get('firearm_config', str(self.enhanced_weapon_id), 'fCDTime', default=0.2)
        self.last_fire_enhanced_weapon_time = 0.0

    def update(self, dt):
        super(WeaponFire8012, self).update(dt)
        if self.oil_bottle_enabled and self.want_to_fire:
            cur_time = global_data.game_time
            if cur_time - self.last_fire_enhanced_weapon_time > self.enhanced_weapon_cd:
                cam = world.get_active_scene().active_camera
                self.send_event('E_DO_SKILL', self.enhanced_skill_id, 0, cam.position, cam.rotation_matrix.forward)
                self.last_fire_enhanced_weapon_time = cur_time