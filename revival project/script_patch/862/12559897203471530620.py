# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/behavior/Logic8032.py
import math3d
import world
import math
import collision
import time
from .StateBase import StateBase
from logic.gcommon.behavior.JumpLogic import OnGround, Fall, SuperJumpUp
from logic.gcommon.behavior.ShootLogic import AccumulateShootPure, WeaponFire
from logic.gcommon.behavior.MoveLogic import Run
from logic.gcommon.common_const.mecha_const import MECHA_8032_NORMAL, MECHA_8032_SPRINT, MECHA_8032_STOP_SPRINT, MECHA_8032_ENTER_SPRINT
from logic.gcommon.const import NEOX_UNIT_SCALE
from logic.gutils.angle_utils import get_angle_difference, CIRCLE_ANGLE
from math import radians, sqrt, fabs, pi
from logic.gcommon.cdata.mecha_status_config import *
from logic.gcommon.common_const.character_anim_const import *
from logic.gcommon import editor
from logic.gutils.character_ctrl_utils import AirWalkDirectionSetter
from logic.comsys.control_ui.ShotChecker import ShotChecker
from logic.vscene.parts import PartCtrl
from logic.gcommon.common_const.attr_const import MECHA_MAX_BODY_TURN_SPEED_FACTOR
from logic.gcommon.behavior.ShootLogic import Reload
from common.cfg import confmgr
from logic.gcommon.common_const.web_const import MECHA_MEMORY_LEVEL_7
from logic.client.const.camera_const import FREE_CAMERA_LIST
from logic.gutils.client_unit_tag_utils import register_unit_tag
UP_VECTOR = math3d.vector(0, 1, 0)
MECHA_MONSTER_VALUE = register_unit_tag(('LMecha', 'LMechaRobot', 'LMonster'))

class OnGround8032(OnGround):

    def init_from_dict(self, unit_obj, bdict, sid, info):
        super(OnGround8032, self).init_from_dict(unit_obj, bdict, sid, info)

    def read_data_from_custom_param(self):
        super(OnGround8032, self).read_data_from_custom_param()
        self.jump_anim = self.custom_param.get('jump_anim')

    def enter(self, leave_states):
        super(OnGround8032, self).enter(leave_states)
        if self.sd.ref_cur_state != MECHA_8032_SPRINT:
            self.send_event('E_POST_ACTION', self.jump_anim, LOW_BODY, 1, loop=False)

    def check_transitions(self):
        if self.sd.ref_cur_state == MECHA_8032_SPRINT:
            self.disable_self()
        else:
            return super(OnGround8032, self).check_transitions()


class SprintOnGround(OnGround8032):
    BIND_EVENT = {}

    def init_from_dict(self, unit_obj, bdict, sid, state_info):
        super(SprintOnGround, self).init_from_dict(unit_obj, bdict, sid, state_info)


class SprintFall(Fall):
    BIND_EVENT = {}

    def init_from_dict(self, unit_obj, bdict, sid, state_info):
        super(SprintFall, self).init_from_dict(unit_obj, bdict, sid, state_info)


class SprintSuperJumpUp(SuperJumpUp):
    BIND_EVENT = {}

    def init_from_dict(self, unit_obj, bdict, sid, state_info):
        super(SprintSuperJumpUp, self).init_from_dict(unit_obj, bdict, sid, state_info)


class Run8032(Run):

    def init_from_dict(self, unit_obj, bdict, sid, info):
        super(Run8032, self).init_from_dict(unit_obj, bdict, sid, info)

    def enter(self, leave_states):
        super(Run8032, self).enter(leave_states)
        self.send_event('E_UPDATE_RUNSTATE', True)

    def update(self, dt):
        super(Run8032, self).update(dt)

    def exit(self, enter_states):
        super(Run8032, self).exit(enter_states)
        if self.sd.ref_cur_state != MECHA_8032_SPRINT:
            self.send_event('E_UPDATE_RUNSTATE', False)


class Reload8032(Reload):

    def on_reloading_bullet(self, time, times, weapon_pos):
        if self.sd.ref_reload_shoot:
            return
        if weapon_pos != self.weapon_pos:
            return
        self.reload_time = time
        if not self.ignore_anim:
            self.active_self()

    def on_reloading_bullet(self, time, times, weapon_pos):
        if self.sd.ref_reload_shoot:
            return
        if weapon_pos != self.weapon_pos:
            return
        self.reload_time = time
        if not self.ignore_anim:
            self.active_self()


@editor.state_exporter({('start_anim_time', 'param'): {'zh_name': '\xe8\xb5\xb7\xe8\xb7\xb3\xe5\x8a\xa8\xe4\xbd\x9c\xe6\x97\xb6\xe9\x97\xb4','post_setter': lambda self: self.register_callback()
                                  },
   ('start_anim_rate', 'param'): {'zh_name': '\xe8\xb5\xb7\xe8\xb7\xb3\xe5\x8a\xa8\xe4\xbd\x9c\xe9\x80\x9f\xe5\xba\xa6','post_setter': lambda self: self.register_callback()
                                  },
   ('jump_loop_rate', 'param'): {'zh_name': '\xe4\xb8\x8a\xe5\x8d\x87\xe5\x8a\xa8\xe4\xbd\x9c\xe6\x92\xad\xe6\x94\xbe\xe9\x80\x9f\xe5\xba\xa6','post_setter': lambda self: self.register_callback()
                                 },
   ('start_fall_time', 'param'): {'zh_name': '\xe5\xbc\x80\xe5\xa7\x8b\xe4\xb8\x8b\xe8\x90\xbd\xe6\x97\xb6\xe9\x97\xb4','post_setter': lambda self: self.register_callback()
                                  },
   ('start_fall_rate', 'param'): {'zh_name': '\xe5\xbc\x80\xe5\xa7\x8b\xe4\xb8\x8b\xe8\x90\xbd\xe5\x8a\xa8\xe4\xbd\x9c\xe6\x92\xad\xe6\x94\xbe\xe9\x80\x9f\xe5\xba\xa6','post_setter': lambda self: self.register_callback()
                                  },
   ('fall_anim_rate', 'param'): {'zh_name': '\xe4\xb8\x8b\xe8\x90\xbd\xe5\x8a\xa8\xe4\xbd\x9c\xe9\x80\x9f\xe5\xba\xa6'},('on_ground_time', 'param'): {'zh_name': '\xe8\x90\xbd\xe5\x9c\xb0\xe5\x8a\xa8\xe4\xbd\x9c\xe6\x97\xb6\xe9\x97\xb4','post_setter': lambda self: self.register_callback()
                                 },
   ('on_ground_rate', 'param'): {'zh_name': '\xe8\x90\xbd\xe5\x9c\xb0\xe5\x8a\xa8\xe4\xbd\x9c\xe9\x80\x9f\xe5\xba\xa6','post_setter': lambda self: self.register_callback()
                                 },
   ('vertical_speed', 'param'): {'zh_name': '\xe8\xb5\xb7\xe8\xb7\xb3\xe7\xba\xb5\xe5\x90\x91\xe9\x80\x9f\xe5\xba\xa6'},('horizontal_speed', 'param'): {'zh_name': '\xe8\xb5\xb7\xe8\xb7\xb3\xe6\xa8\xaa\xe5\x90\x91\xe9\x80\x9f\xe5\xba\xa6'},('jump_gravity', 'param'): {'zh_name': '\xe8\xb7\xb3\xe8\xb7\x83\xe6\x97\xb6\xe9\x87\x8d\xe5\x8a\x9b'},('can_interrupt_time', 'param'): {'zh_name': '\xe8\x90\xbd\xe5\x9c\xb0\xe5\x90\x8e\xe6\x91\x87\xe5\x8f\xaf\xe6\x89\x93\xe6\x96\xad\xe6\x97\xb6\xe9\x97\xb4','post_setter': lambda self: self.register_callback()
                                     },
   ('force_enter_sprint_protect_time', 'param'): {'zh_name': '\xe5\xbc\xba\xe5\x88\xb6\xe8\xbf\x9b\xe5\x86\xb2\xe9\x94\x8b\xe5\x90\x8e\xe8\xbf\x9e\xe7\x82\xb9\xe4\xbf\x9d\xe6\x8a\xa4'}})
class TetrapodDash(StateBase):
    BIND_EVENT = {'E_FORCE_ENTER_SPRINT': 'on_force_enter_sprint'
       }
    JUMP_START = 0
    JUMP_LOOP = 1
    JUMP_START_FALL = 2
    JUMP_FALL = 3
    JUMP_GROUND = 4

    def init_from_dict(self, unit_obj, bdict, sid, info):
        super(TetrapodDash, self).init_from_dict(unit_obj, bdict, sid, info)
        self.read_data_from_custom_param()
        self.register_callback()
        self.range_inc = 0.0
        self.can_interrupt = False
        self.force_enter_sprint = False
        self.force_enter_sprint_time = 0
        self.enable_param_changed_by_buff()

    def register_callback(self):
        self.reset_sub_states_callback()
        self.register_substate_callback(self.JUMP_START, 0, self.on_jump_start)
        self.register_substate_callback(self.JUMP_START, self.start_anim_time / self.start_anim_rate, lambda : self.send_event('E_ANIM_RATE', LOW_BODY, 1.5))
        self.register_substate_callback(self.JUMP_START, self.start_anim_time / self.start_anim_rate, self.on_jump_end)
        self.register_substate_callback(self.JUMP_LOOP, 0, self.on_jump_loop)
        self.register_substate_callback(self.JUMP_START_FALL, 0, self.on_jump_start_fall)
        self.register_substate_callback(self.JUMP_START_FALL, self.start_fall_time / self.start_fall_rate, self.on_jump_start_fall_end)
        self.register_substate_callback(self.JUMP_FALL, 0, self.on_fall_loop)
        self.register_substate_callback(self.JUMP_GROUND, self.can_interrupt_time, self.on_interrupt)
        self.register_substate_callback(self.JUMP_GROUND, self.on_ground_time / self.on_ground_rate, self.on_ground_end)

    def enter(self, leave_states):
        super(TetrapodDash, self).enter(leave_states)
        self.can_interrupt = False
        self.sub_state = self.JUMP_START
        self.send_event('E_CLEAR_SPEED')
        self.send_event('E_DO_SKILL', self.skill_id)
        self.regist_event('E_FALL', self.on_fall)
        self.regist_event('E_ON_TOUCH_GROUND', self.on_dash_ground)
        self.send_event('E_ENABLE_CAMERA_ROTATE_SYNC_TO_MODEL', False)

    def exit(self, enter_states):
        super(TetrapodDash, self).exit(enter_states)
        self.force_enter_sprint = False
        self.unregist_event('E_FALL', self.on_fall)
        self.unregist_event('E_ON_TOUCH_GROUND', self.on_dash_ground)
        self.send_event('E_RESET_GRAVITY')
        self.send_event('E_END_SPRINT')
        self.send_event('E_END_SKILL', self.skill_id)
        self.send_event('E_BEGIN_RECOVER_MP', self.skill_id)
        self.send_event('E_ENBALE_8032_STATE_SFX', 'dash', False)
        self.sd.ref_logic_trans.yaw_target = world.get_active_scene().active_camera.rotation_matrix.yaw
        self.sd.ref_common_motor.set_yaw_time(0.2)
        self.send_event('E_ENABLE_CAMERA_ROTATE_SYNC_TO_MODEL', True)
        self.send_event('E_ENBALE_8032_STATE_SFX', 'stomp_end', False)
        self.sound_custom_end()

    def action_btn_down(self):
        if not self.check_can_active():
            return False
        if not self.check_can_cast_skill():
            return False
        if self.force_enter_sprint and time.time() - self.force_enter_sprint_time < self.force_enter_sprint_protect_time:
            return False
        if MC_SPRINT not in self.ev_g_cur_state():
            return False
        self.active_self()
        super(TetrapodDash, self).action_btn_down()
        return True

    def on_force_enter_sprint(self):
        self.force_enter_sprint = True
        self.force_enter_sprint_time = time.time()
        self.send_event('E_BEGIN_RECOVER_MP', self.skill_id)

    def read_data_from_custom_param(self):
        self.stomp_skill_id = self.custom_param.get('stomp_skill_id', 803255)
        self.skill_id = self.custom_param.get('skill_id', 803256)
        self.start_anim = self.custom_param.get('start_anim', 'stomp_01')
        self.start_anim_time = self.custom_param.get('start_anim_time', 0.9)
        self.start_anim_rate = self.custom_param.get('start_anim_rate', 1.0)
        self.jump_loop_anim = self.custom_param.get('jump_loop_anim', 'stomp_02')
        self.jump_loop_rate = self.custom_param.get('jump_loop_rate', 1.0)
        self.start_fall_anim = self.custom_param.get('start_fall_anim', 'stomp_03')
        self.start_fall_time = self.custom_param.get('start_fall_time', 0.2)
        self.start_fall_rate = self.custom_param.get('start_fall_rate', 1.0)
        self.fall_anim = self.custom_param.get('fall_anim', 'stomp_04')
        self.fall_anim_rate = self.custom_param.get('fall_anim_rate', 1.0)
        self.on_ground_anim = self.custom_param.get('on_ground_anim', 'stomp_05')
        self.on_ground_time = self.custom_param.get('on_ground_time', 1.0)
        self.on_ground_rate = self.custom_param.get('on_ground_rate', 1.0)
        self.can_interrupt_time = self.custom_param.get('can_interrupt_time', 1.0)
        self.vertical_speed = self.custom_param.get('vertical_speed', 180.0)
        self.horizontal_speed = self.custom_param.get('horizontal_speed', 20.0)
        self.jump_gravity = self.custom_param.get('jump_gravity', 400.0)
        self.force_enter_sprint_protect_time = self.custom_param.get('force_enter_sprint_protect_time', 0.5)

    def on_jump_start(self):
        self.send_event('E_GRAVITY', self.jump_gravity * NEOX_UNIT_SCALE)
        self.send_event('E_DO_SKILL', self.skill_id)
        self.send_event('E_ANIM_RATE', LOW_BODY, self.start_anim_rate)
        self.send_event('E_POST_ACTION', self.start_anim, LOW_BODY, 1)

    def on_jump_end(self):
        self.sub_state = self.JUMP_LOOP
        self.send_event('E_ANIM_RATE', LOW_BODY, 1.0)
        self.send_event('E_JUMP', self.vertical_speed * NEOX_UNIT_SCALE)
        scn = world.get_active_scene()
        camera = scn.active_camera
        if not camera:
            return
        foward = camera.rotation_matrix.forward
        foward.y = 0.0
        foward.normalize()
        self.send_event('E_SET_WALK_DIRECTION', foward * self.horizontal_speed * (1.0 + self.range_inc) * NEOX_UNIT_SCALE)
        self.send_event('E_ENBALE_8032_STATE_SFX', 'dash', True)

    def on_jump_loop(self):
        self.send_event('E_ANIM_RATE', LOW_BODY, self.jump_loop_rate)
        self.send_event('E_POST_ACTION', self.jump_loop_anim, LOW_BODY, 1)

    def on_jump_start_fall(self):
        self.send_event('E_ANIM_RATE', LOW_BODY, self.start_fall_rate)
        self.send_event('E_POST_ACTION', self.start_fall_anim, LOW_BODY, 1, blend_time=0.5)

    def on_jump_start_fall_end(self):
        self.sub_state = self.JUMP_FALL
        self.send_event('E_ANIM_RATE', LOW_BODY, 1.0)

    def on_fall(self, *args):
        if self.sub_state == self.JUMP_GROUND or self.sub_state == self.JUMP_START_FALL or self.sub_state == self.JUMP_FALL:
            return
        self.sub_state = self.JUMP_START_FALL

    def on_fall_loop(self):
        self.send_event('E_ANIM_RATE', LOW_BODY, self.fall_anim_rate)
        self.send_event('E_POST_ACTION', self.fall_anim, LOW_BODY, 1, loop=True)

    def on_dash_ground(self, *args):
        self.sound_custom_start()
        if self.sub_state != self.JUMP_FALL:
            self.unregist_event('E_FALL', self.on_fall)
        self.sub_state = self.JUMP_GROUND
        self.send_event('E_CLEAR_SPEED')
        self.send_event('E_ANIM_RATE', LOW_BODY, self.on_ground_rate)
        self.send_event('E_POST_ACTION', self.on_ground_anim, LOW_BODY, 1, blend_time=0.0)
        self.send_event('E_DO_SKILL', self.stomp_skill_id, MECHA_8032_NORMAL, ())
        self.send_event('E_PLAY_STOMP_ON_GROUND_SFX')
        self.send_event('E_ENBALE_8032_STATE_SFX', 'dash', False)
        self.send_event('E_ENBALE_8032_STATE_SFX', 'stomp_end', True)

    def on_interrupt(self):
        self.can_interrupt = True
        self.send_event('E_ADD_WHITE_STATE', {MC_MOVE}, self.sid)

    def on_ground_end(self):
        self.send_event('E_ADD_WHITE_STATE', {MC_STAND}, self.sid)
        self.disable_self()

    def check_transitions(self):
        if self.can_interrupt and self.sd.ref_rocker_dir != 0:
            return MC_MOVE

    def destroy(self):
        self.unregist_event('E_FALL', self.on_fall)
        self.unregist_event('E_ON_TOUCH_GROUND', self.on_dash_ground)
        super(TetrapodDash, self).destroy()


@editor.state_exporter({('max_dash_time', 'param'): {'zh_name': '\xe6\x9c\x80\xe5\xa4\xa7\xe5\x86\xb2\xe5\x88\xba\xe6\x97\xb6\xe9\x97\xb4(max_dash_time)','post_setter': lambda self: self.register_callback()
                                },
   ('sprint_speed', 'param'): {'zh_name': '\xe6\x9c\x80\xe5\xa4\xa7\xe5\x86\xb2\xe5\x88\xba\xe9\x80\x9f\xe5\xba\xa6(sprint_speed)'},('camera_sense', 'param'): {'zh_name': '\xe5\x86\xb2\xe5\x88\xba\xe6\x97\xb6\xe9\x95\x9c\xe5\xa4\xb4\xe7\x81\xb5\xe6\x95\x8f\xe5\xba\xa6(camera_sense)'},('hit_anim_rate', 'param'): {'zh_name': '\xe5\x91\xbd\xe4\xb8\xad\xe5\x8a\xa8\xe7\x94\xbb\xe6\x92\xad\xe6\x94\xbe\xe9\x80\x9f\xe5\xba\xa6(hit_anim_rate)','post_setter': lambda self: self.register_callback()
                                },
   ('hit_miss_anim_rate', 'param'): {'zh_name': 'miss\xe5\x8a\xa8\xe4\xbd\x9c\xe9\x80\x9f\xe7\x8e\x87(hit_miss_anim_rate)','post_setter': lambda self: self.register_callback()
                                     },
   ('hit_miss_anim_time', 'param'): {'zh_name': 'miss\xe5\x8a\xa8\xe4\xbd\x9c\xe6\x97\xb6\xe9\x97\xb4(hit_miss_anim_time)','post_setter': lambda self: self.register_callback()
                                     },
   ('hit_keep_anim_rate', 'param'): {'zh_name': '\xe5\x91\xbd\xe4\xb8\xad\xe6\x8b\x96\xe8\xa1\x8c\xe5\x8a\xa8\xe4\xbd\x9c\xe6\x92\xad\xe6\x94\xbe\xe9\x80\x9f\xe7\x8e\x87(hit_keep_anim_rate)','post_setter': lambda self: self.register_callback()
                                     },
   ('hit_start_anim_rate', 'param'): {'zh_name': '\xe5\x91\xbd\xe4\xb8\xad\xe6\x8a\xac\xe6\x89\x8b\xe5\x8a\xa8\xe4\xbd\x9c\xe9\x80\x9f\xe7\x8e\x87(hit_start_anim_rate)','post_setter': lambda self: self.register_callback()
                                      },
   ('hit_start_anim_time', 'param'): {'zh_name': '\xe5\x91\xbd\xe4\xb8\xad\xe6\x8a\xac\xe6\x89\x8b\xe6\x97\xb6\xe9\x97\xb4(hit_start_anim_time)','post_setter': lambda self: self.register_callback()
                                      },
   ('hit_end_anim_rate', 'param'): {'zh_name': '\xe7\xa9\xbf\xe5\x88\xba\xe9\x98\xb6\xe6\xae\xb5\xe5\x8a\xa8\xe7\x94\xbb\xe6\x92\xad\xe6\x94\xbe\xe9\x80\x9f\xe5\xba\xa6(hit_end_anim_rate)','post_setter': lambda self: self.register_callback()
                                    },
   ('hit_end_anim_time', 'param'): {'zh_name': '\xe7\xa9\xbf\xe5\x88\xba\xe9\x98\xb6\xe6\xae\xb5\xe9\x98\xb6\xe6\xae\xb5\xe6\x97\xb6\xe9\x97\xb4(hit_end_anim_time)','post_setter': lambda self: self.register_callback()
                                    },
   ('can_cancel_dash_time', 'param'): {'zh_name': '\xe5\x8f\xaf\xe5\x8f\x96\xe6\xb6\x88\xe5\x86\xb2\xe5\x88\xba\xe9\xa3\x9e\xe8\xa1\x8c\xe7\x9a\x84\xe6\x97\xb6\xe9\x97\xb4(can_cancel_dash_time)','post_setter': lambda self: self.register_callback()
                                       },
   ('can_break_hit_miss_time', 'param'): {'zh_name': 'miss\xe9\x98\xb6\xe6\xae\xb5\xe5\x8f\xaf\xe6\x89\x93\xe6\x96\xad\xe6\x97\xb6\xe9\x97\xb4(can_break_hit_miss_time)','post_setter': lambda self: self.register_callback()
                                          },
   ('can_break_hit_end_time', 'param'): {'zh_name': '\xe7\xa9\xbf\xe5\x88\xba\xe9\x98\xb6\xe6\xae\xb5\xe5\x8f\xaf\xe6\x89\x93\xe6\x96\xad\xe6\x97\xb6\xe9\x97\xb4(can_break_hit_end_time)','post_setter': lambda self: self.register_callback()
                                         },
   ('force_enter_protect_time', 'param'): {'zh_name': '\xe5\xbc\xba\xe5\x88\xb6\xe8\xbf\x9b\xe5\x85\xa5\xe5\x86\xb2\xe9\x94\x8b\xe7\x8a\xb6\xe6\x80\x81\xe4\xb8\x8b\xe8\xbf\x9e\xe6\x8c\x89\xe4\xbf\x9d\xe6\x8a\xa4\xe6\x97\xb6\xe9\x97\xb4(force_enter_protect_time)'},('step_height', 'param'): {'zh_name': '\xe5\x86\xb2\xe5\x88\xba\xe4\xb8\x8b\xe6\x8a\xac\xe8\x84\x9a\xe9\xab\x98\xe5\xba\xa6(step_height)'}})
class TetrapodSprintDash(StateBase):
    BIND_EVENT = {'E_ON_POST_JOIN_MECHA': 'on_post_join_mecha',
       'E_ON_LEAVE_MECHA_START': 'on_leave_mecha_start',
       'E_FORCE_ENTER_SPRINT': 'on_force_enter_sprint',
       'E_ENHANCE_8032_SPRINT_DASH': 'on_dash_time_change'
       }
    DASH_NONE = 0
    DASH_FLY = 1
    DASH_HIT_START = 2
    DASH_MISS = 5

    def init_from_dict(self, unit_obj, bdict, sid, info):
        super(TetrapodSprintDash, self).init_from_dict(unit_obj, bdict, sid, info)
        self.read_data_from_custom_param()
        self.init_parameters()
        self.air_walk_direction_setter = AirWalkDirectionSetter(self)
        self.enable_param_changed_by_buff()
        self.register_callback()
        self.notify_outer_parameters()

    def init_parameters(self):
        self.sub_state = self.DASH_NONE
        self.dash_end = False
        self.hit_keep_target = None
        self.event_registered = False
        self.sprint_dash_stop = True
        self.continual_on_ground = True
        self.is_hit_mecha_robot = False
        self.is_force_enter_sprint = False
        self.force_enter_sprint_time = 0
        self.can_cancel_dash = False
        self.time_inc = 0.0
        self.cur_speed = 0.0
        self.dash_on_ground = False
        self.btn_down = False
        PartCtrl.enable_clamp_cam_rotation(False)
        return

    def read_data_from_custom_param(self):
        self.skill_id = self.custom_param.get('skill_id', 803253)
        self.hit_skill = self.custom_param.get('hit_skill', 803257)
        self.dash_anim = self.custom_param.get('dash_anim', 'charge_dash_stab')
        self.max_dash_time = self.custom_param.get('max_dash_time', 5.0)
        self.sprint_speed = self.custom_param.get('sprint_speed', 20.0) * NEOX_UNIT_SCALE
        self.camera_sense = self.custom_param.get('camera_sense', 10.0)
        self.hit_start_anim = self.custom_param.get('hit_start_anim', 'charge_dash_hit_01')
        self.hit_start_anim_rate = self.custom_param.get('hit_start_anim_rate', 1.0)
        self.hit_start_anim_time = self.custom_param.get('hit_start_anim_time', 1.0)
        self.hit_end_anim = self.custom_param.get('hit_end_anim', 'charge_dash_hit_fin')
        self.hit_end_anim_rate = self.custom_param.get('hit_end_anim_rate', 1.0)
        self.hit_end_anim_time = self.custom_param.get('hit_end_anim_time', 1.0)
        self.hit_end_skill_time = self.custom_param.get('hit_end_skill_time', 0.3)
        self.hit_miss_anim = self.custom_param.get('hit_miss_anim', 'charge_dash_miss')
        self.hit_miss_anim_rate = self.custom_param.get('hit_miss_anim_rate', 1.0)
        self.hit_miss_anim_time = self.custom_param.get('hit_miss_anim_time', 1.2)
        self.force_enter_protect_time = self.custom_param.get('force_enter_protect_time', 0.5)
        self.can_cancel_dash_time = self.custom_param.get('can_cancel_dash_time', 1.5)
        self.can_break_hit_miss_time = self.custom_param.get('can_break_hit_miss_time', 0.3)
        self.can_break_hit_end_time = self.custom_param.get('can_break_hit_end_time', 0.3)
        self.step_height = self.custom_param.get('step_height', 1.0) * NEOX_UNIT_SCALE

    def notify_outer_parameters(self):
        self.send_event('E_CREATE_CONTACT_COLLISION', self.sid, {'shape': collision.BOX,
           'size': [
                  39, 52, 52],
           'offset_vec': [
                        0, 50, 40]
           })

    def register_callback(self):
        self.reset_sub_states_callback()
        self.register_substate_callback(self.DASH_FLY, 0, self.on_dash_fly)
        self.register_substate_callback(self.DASH_FLY, self.can_cancel_dash_time, self.on_dash_can_cancel)
        self.register_substate_callback(self.DASH_FLY, self.max_dash_time + self.max_dash_time * self.time_inc, self.on_dash_fly_end)
        self.register_substate_callback(self.DASH_HIT_START, 0, self.on_dash_hit_start)
        self.register_substate_callback(self.DASH_HIT_START, self.hit_start_anim_time / self.hit_start_anim_rate, self.on_dash_hit_start_end)
        self.register_substate_callback(self.DASH_MISS, 0, self.on_dash_miss)
        self.register_substate_callback(self.DASH_MISS, self.can_break_hit_miss_time, self.on_dash_miss_break_post)
        self.register_substate_callback(self.DASH_MISS, self.hit_miss_anim_time, self.on_dash_hit_miss_end)

    def on_dash_can_cancel(self):
        self.can_cancel_dash = True
        self.send_event('E_SET_ACTION_SELECTED', 'action1', True)
        self.send_event('E_SET_ACTION_SELECTED', 'action2', True)
        self.send_event('E_SET_ACTION_SELECTED', 'action3', True)
        self.send_event('E_UPDATE_SPRINT_DASH_UI', True)

    def on_dash_fly(self):
        self.sprint_dash_stop = False
        PartCtrl.enable_clamp_cam_rotation(True, 0.01 * self.camera_sense * (1.0 + self.ev_g_add_attr(MECHA_MAX_BODY_TURN_SPEED_FACTOR)))
        self.air_walk_direction_setter.reset()
        self.send_event('E_POST_ACTION', self.dash_anim, LOW_BODY, 1, loop=True)
        self.send_event('E_DISABLE_ROCKER_ANIM_DIR', True)
        self.send_event('E_TRY_CANCEL_RUN_LOCK')
        self.send_event('E_FORBID_ROTATION', True)
        self.send_event('E_ENABLE_CHECK_CONTACT_TARGET', self.sid, True, self.on_contact_targets)
        self.send_event('E_ENBALE_8032_STATE_SFX', 'sprint_dash', True)
        self.sound_custom_start()

    def on_dash_fly_end(self):
        if self.dash_on_ground:
            self.sub_state = self.DASH_MISS
            return
        self.dash_end = True
        self.sprint_dash_stop = True
        self.send_event('E_ADD_WHITE_STATE', {MC_JUMP_2, MC_STAND}, self.sid)
        self.disable_self()

    def on_dash_miss(self):
        self.start_custom_sound('miss_state')
        self.send_event('E_UPDATE_SPRINT_DASH_UI', False)
        self.send_event('E_ENABLE_CHECK_CONTACT_TARGET', self.sid, False)
        self.send_event('E_RESET_GRAVITY')
        self.send_event('E_ANIM_RATE', LOW_BODY, self.hit_miss_anim_rate)
        self.send_event('E_POST_ACTION', self.hit_miss_anim, LOW_BODY, 1, loop=False)
        self.send_event('E_ENBALE_8032_STATE_SFX', 'sprint_dash', False)

    def on_dash_miss_break_post(self):
        self.send_event('E_ADD_WHITE_STATE', {MC_MOVE, MC_SECOND_WEAPON_ATTACK}, self.sid)

    def on_dash_hit_miss_end(self):
        self.dash_end = True
        self.send_event('E_ADD_WHITE_STATE', {MC_JUMP_2, MC_STAND}, self.sid)
        self.disable_self()

    def on_dash_hit_start(self):
        self.sprint_dash_stop = True
        self.start_custom_sound('hit_state')
        self.send_event('E_ENABLE_CAMERA_ROTATE_SYNC_TO_MODEL', False)
        self.send_event('E_ANIM_RATE', LOW_BODY, self.hit_start_anim_rate)
        self.send_event('E_POST_ACTION', self.hit_start_anim, LOW_BODY, 1, loop=False)

    def on_dash_hit_start_end(self):
        self.sub_state = self.DASH_MISS
        self.send_event('E_ANIM_RATE', LOW_BODY, 1.0)

    def on_dash_hit_end(self):
        self.send_event('E_POST_ACTION', self.hit_end_anim, LOW_BODY, 1, loop=False)

    def on_dash_hit_break_post(self):
        self.send_event('E_ADD_WHITE_STATE', {MC_MOVE, MC_SECOND_WEAPON_ATTACK}, self.sid)

    def on_dash_hit_skill(self):
        self.send_event('E_END_SKILL', self.hit_skill, True, self.hit_keep_target)

    def on_dash_hit_end_finish(self):
        self.dash_end = True
        self.send_event('E_ADD_WHITE_STATE', {MC_JUMP_2, MC_STAND}, self.sid)
        self.disable_self()

    def refresh_param_changed(self):
        self.on_dash_time_change()

    def on_dash_time_change(self):
        self.reset_sub_state_callback(self.DASH_FLY)
        self.register_substate_callback(self.DASH_FLY, 0, self.on_dash_fly)
        self.register_substate_callback(self.DASH_FLY, self.can_cancel_dash_time, self.on_dash_can_cancel)
        self.register_substate_callback(self.DASH_FLY, self.max_dash_time + self.max_dash_time * self.time_inc, self.on_dash_fly_end)

    def on_contact_targets(self, targets):
        if not targets:
            return
        for target in targets:
            if not target.MASK & MECHA_MONSTER_VALUE:
                continue
            if self.sub_state == self.DASH_HIT_START:
                return
            self.sub_state = self.DASH_HIT_START
            self.send_event('E_DO_SKILL', self.hit_skill, True, target.id)
            self.send_event('E_ENABLE_CHECK_CONTACT_TARGET', self.sid, False)
            self.hit_keep_target = target.id
            return

    def recover_mecha_character(self):
        physic_conf = confmgr.get('mecha_conf', 'PhysicConfig', 'Content')
        mecha_id = self.sd.ref_mecha_id or 8001
        physic_conf = physic_conf[str(mecha_id)]
        width = physic_conf['character_size'][0] * NEOX_UNIT_SCALE / 2
        height = physic_conf['character_size'][1] * NEOX_UNIT_SCALE
        self.send_event('E_RESET_CHAR_SIZE', width, height, 0.0)

    def enter(self, leave_states):
        super(TetrapodSprintDash, self).enter(leave_states)
        if self.ev_g_on_ground():
            self.dash_on_ground = True
        else:
            self.dash_on_ground = False
        self.sub_state = self.DASH_FLY
        self.keep_hit_target = None
        self.cur_speed = self.sprint_speed
        self.send_event('E_DO_SKILL', self.skill_id)
        self.send_event('E_STEP_HEIGHT', self.step_height)
        return

    def exit(self, enter_states):
        super(TetrapodSprintDash, self).exit(enter_states)
        self.sub_state = self.DASH_NONE
        self.end_custom_sound('miss_state')
        self.end_custom_sound('hit_state')
        self.send_event('E_CLEAR_SPEED')
        self.send_event('E_RESET_GRAVITY')
        self.send_event('E_FORBID_ROTATION', False)
        self.send_event('E_END_SKILL', self.skill_id)
        self.send_event('E_BEGIN_RECOVER_MP', self.skill_id)
        self.send_event('E_RESET_ROTATION')
        self.send_event('E_ANIM_RATE', LOW_BODY, 1)
        self.send_event('E_ACTION_MOVE_STOP')
        self.send_event('E_END_SPRINT')
        self.send_event('E_ENABLE_CHECK_CONTACT_TARGET', self.sid, False)
        self.send_event('E_DISABLE_ROCKER_ANIM_DIR', False)
        self.send_event('E_SET_ACTION_SELECTED', 'action1', False)
        self.send_event('E_SET_ACTION_SELECTED', 'action2', False)
        self.send_event('E_SET_ACTION_SELECTED', 'action3', False)
        self.send_event('E_ENBALE_8032_STATE_SFX', 'sprint_dash', False)
        self.send_event('E_UPDATE_SPRINT_DASH_UI', False)
        self.sd.ref_logic_trans.yaw_target = world.get_active_scene().active_camera.rotation_matrix.yaw
        self.sd.ref_common_motor.set_yaw_time(0.2)
        self.send_event('E_ENABLE_CAMERA_ROTATE_SYNC_TO_MODEL', True)
        global_data.emgr.enable_camera_yaw.emit(True)
        self.hit_keep_target = None
        PartCtrl.enable_clamp_cam_rotation(False)
        self.keep_hit_target = None
        self.is_force_enter_sprint = False
        self.is_hit_mecha_robot = False
        self.sprint_dash_stop = True
        self.can_cancel_dash = False
        self.dash_end = False
        self.btn_down = False
        self.sound_custom_end()
        self.end_custom_sound('hit_state')
        self.send_event('E_RESET_STEP_HEIGHT')
        return

    def on_post_join_mecha(self):
        if self.ev_g_is_avatar() and not self.event_registered:
            self.regist_event('E_ROTATE', self.on_cam_rotate)
            self.event_registered = True

    def on_leave_mecha_start(self):
        if self.ev_g_is_avatar() and self.event_registered:
            self.unregist_event('E_ROTATE', self.on_cam_rotate)
            self.event_registered = False

    def on_force_enter_sprint(self):
        self.is_force_enter_sprint = True
        self.force_enter_sprint_time = time.time()

    def action_btn_down(self):
        if self.is_active and self.can_cancel_dash == True and self.sub_state == self.DASH_FLY and self.btn_down:
            self.on_dash_fly_end()
            return False
        if self.sub_state != self.DASH_NONE:
            return False
        if not self.check_can_active():
            return False
        if not self.ev_g_can_cast_skill(self.skill_id):
            return False
        if self.is_force_enter_sprint and time.time() - self.force_enter_sprint_time < self.force_enter_protect_time:
            return False
        if MC_SPRINT not in self.ev_g_cur_state():
            return False
        if not self.is_active:
            self.active_self()
        super(TetrapodSprintDash, self).action_btn_down()
        return True

    def action_btn_up(self):
        if self.is_active:
            self.btn_down = True
        super(TetrapodSprintDash, self).action_btn_up()

    def check_transitions(self):
        if self.dash_end:
            if self.dash_on_ground:
                if self.sd.ref_rocker_dir:
                    return MC_MOVE
                else:
                    return MC_STAND

            else:
                return MC_JUMP_2

    def update_flight_direction(self, dt):
        if self.sprint_dash_stop:
            self.send_event('E_CLEAR_SPEED')
            return
        scn = world.get_active_scene()
        if scn:
            part_cam = scn.get_com('PartCamera')
            if part_cam and part_cam.get_cur_camera_state_type() in FREE_CAMERA_LIST:
                return
        forward = scn.active_camera.rotation_matrix.forward
        forward.y = 0
        forward.normalize()
        self.send_event('E_FORWARD', forward, True)
        if self.sub_state == self.DASH_MISS:
            self.cur_speed -= self.sprint_speed * dt
            if self.cur_speed < 0.0:
                self.cur_speed = 0.0
        if self.dash_on_ground:
            self.send_event('E_SET_WALK_DIRECTION', forward * self.cur_speed)
        else:
            self.air_walk_direction_setter.execute(forward * self.cur_speed)

    def update(self, dt):
        super(TetrapodSprintDash, self).update(dt)
        self.update_flight_direction(dt)

    def on_cam_rotate(self, *args):
        if self.sub_state in (self.DASH_HIT_START,):
            return
        if self.is_active:
            scn = world.get_active_scene()
            if scn:
                part_cam = scn.get_com('PartCamera')
                if part_cam and part_cam.get_cur_camera_state_type() in FREE_CAMERA_LIST:
                    return
            forward = scn.active_camera.rotation_matrix.forward
            forward.y = 0
            forward.normalize()
            if self.dash_on_ground:
                self.send_event('E_SET_WALK_DIRECTION', forward * self.cur_speed)
            else:
                self.air_walk_direction_setter.execute(forward * self.cur_speed)
            self.send_event('E_FORWARD', forward, True)

    def destroy(self):
        if self.event_registered:
            self.unregist_event('E_ROTATE', self.on_cam_rotate)
            self.event_registered = False
        if self.air_walk_direction_setter:
            self.air_walk_direction_setter.destroy()
            self.air_walk_direction_setter = None
        PartCtrl.enable_clamp_cam_rotation(False)
        super(TetrapodSprintDash, self).destroy()
        return


class AccumulateShoot8032(AccumulateShootPure):
    BIND_EVENT = AccumulateShootPure.BIND_EVENT.copy()
    BREAK_POST_STATES = {
     MC_SHOOT, MC_RELOAD, MC_MOVE, MC_FORCE_SPRINT, MC_DASH, MC_RELOAD_SHOOT}

    def init_from_dict(self, unit_obj, bdict, sid, info):
        super(AccumulateShoot8032, self).init_from_dict(unit_obj, bdict, sid, info)

    def enter(self, leave_states):
        super(AccumulateShoot8032, self).enter(leave_states)
        self.send_event('E_SHOW_ACC_WP_TRACK')
        if self.sd.ref_cur_state != MECHA_8032_SPRINT:
            self.send_event('E_REPLACE_ACTION_TRIGGER_ANIM', MC_STAND, self.loop_anim_name, loop=True)

    def on_begin_loop(self):
        super(AccumulateShoot8032, self).on_begin_loop()
        self.send_event('E_PLAY_CAMERA_TRK', '1055_CHARGE')
        self.sound_custom_start()

    def _fire(self):
        super(AccumulateShoot8032, self)._fire()
        self.sound_custom_end()
        self.send_event('E_STOP_ACC_WP_TRACK')
        self.send_event('E_CANCEL_CAMERA_TRK', '1055_CHARGE')
        if self.sd.ref_cur_state != MECHA_8032_SPRINT:
            self.send_event('E_REPLACE_ACTION_TRIGGER_ANIM', MC_STAND, 'vice_fire_end', loop=False)

    def cancel_shoot(self):
        super(AccumulateShoot8032, self).cancel_shoot()
        self.send_event('E_CANCEL_CAMERA_TRK', '1055_CHARGE')

    def exit(self, enter_states):
        super(AccumulateShoot8032, self).exit(enter_states)
        if self.sd.ref_cur_state != MECHA_8032_SPRINT:
            self.send_event('E_REPLACE_ACTION_TRIGGER_ANIM', MC_STAND, None)
        self.send_event('E_STOP_ACC_WP_TRACK')
        self.send_event('E_CANCEL_CAMERA_TRK', '1055_CHARGE')
        return


class TetrapodShoot(WeaponFire):
    BIND_EVENT = WeaponFire.BIND_EVENT.copy()
    BIND_EVENT.update({'E_ENABLE_THROUGH_SHIELD': 'enable_through_shield'
       })

    def init_from_dict(self, unit_obj, bdict, sid, info):
        super(TetrapodShoot, self).init_from_dict(unit_obj, bdict, sid, info)
        self.enhance_weapon_pos = self.custom_param.get('enhance_weapon_pos', 4)
        self.normal_weapon_pos = self.custom_param.get('normal_weapon_pos', 1)

    def action_btn_down(self, ignore_reload=False):
        if self.sd.ref_cur_state == MECHA_8032_SPRINT:
            self.disable_self()
            return False
        return super(TetrapodShoot, self).action_btn_down(ignore_reload)

    def enable_through_shield(self, state, *args):
        self.try_weapon_attack_end()
        if state:
            self.weapon_pos = self.enhance_weapon_pos
            self.send_event('E_ENBALE_8032_STATE_SFX', 'stomp_buff', True)
        else:
            self.weapon_pos = self.normal_weapon_pos
            self.send_event('E_ENBALE_8032_STATE_SFX', 'stomp_buff', False)
        self.send_event('E_SWITCH_BIND_WEAPON', 0, self.weapon_pos)

    def enter(self, leave_states):
        super(TetrapodShoot, self).enter(leave_states)
        if self.sd.ref_cur_state == MECHA_8032_SPRINT:
            self.disable_self()
            return
        self.send_event('E_UPDATE_RUNSTATE', False)

    def on_fire(self, f_cdtime, weapon_pos, fired_socket_index=None):
        if self.weapon_pos != weapon_pos:
            return
        if self.sd.ref_cur_state == MECHA_8032_SPRINT:
            self.action_btn_up()
            self.disable_self()
            return
        super(TetrapodShoot, self).on_fire(f_cdtime, weapon_pos, fired_socket_index)

    def continue_fire(self):
        if self.sd.ref_cur_state == MECHA_8032_SPRINT:
            return (False, self.weapon_pos)
        return super(TetrapodShoot, self).continue_fire()


@editor.state_exporter({('max_loop_time', 'param'): {'zh_name': 'loop\xe6\x9c\x80\xe5\xa4\xa7\xe6\x97\xb6\xe9\x95\xbf','post_setter': lambda self: self.register_callbacks()
                                }
   })
class TetrapodSprintShoot(AccumulateShootPure):
    PART = LOW_BODY

    def init_from_dict(self, unit_obj, bdict, sid, state_info):
        super(TetrapodSprintShoot, self).init_from_dict(unit_obj, bdict, sid, state_info)
        self.enable_param_changed_by_buff()
        self.is_enhanced = False

    def register_callbacks(self):
        super(TetrapodSprintShoot, self).register_callbacks()
        self.register_substate_callback(self.STATE_LOOP, self.max_loop_time, self.on_end_loop)

    def on_end_loop(self):
        self.btn_down = False
        self.sub_state = self.STATE_POST

    def action_btn_down(self):
        super(AccumulateShootPure, self).action_btn_down()
        if not self.is_active:
            self.btn_down = not self.sd.ref_reload_shoot or self.sd.ref_cur_state == MECHA_8032_SPRINT
        if not self.sd.ref_is_robot and ShotChecker().check_camera_can_shot():
            return False
        if not self.check_can_active():
            return False
        if not self.check_can_cast_skill():
            return False
        if not self.ev_g_check_can_weapon_attack(self.weapon_pos):
            return False
        if self.sd.ref_cur_state == MECHA_8032_SPRINT:
            self.active_self()
        return True

    def on_begin_loop(self):
        super(TetrapodSprintShoot, self).on_begin_loop()
        self.send_event('E_PLAY_CAMERA_TRK', '1055_CHARGE')

    def enter(self, leave_states):
        super(AccumulateShootPure, self).enter(leave_states)
        self.acc_skill_ended = False
        self.send_event('E_ACC_SKILL_BEGIN', self.weapon_pos)
        if self.use_up_body_bone and self.PART == UP_BODY:
            self.send_event('E_UPBODY_BONE', FULL_BODY_BONE)
        if self.btn_down:
            if self.pre_anim_name:
                self.sub_state = self.STATE_PRE
            else:
                self.sub_state = self.STATE_LOOP
        elif self.force_pre and self.pre_anim_name:
            self.sub_state = self.STATE_PRE
        else:
            self.sub_state = self.STATE_POST

    def read_data_from_custom_param(self):
        self.max_loop_time = self.custom_param.get('max_loop_time', 3.0)
        self.enhanced_weapon_pos = self.custom_param.get('enhanced_weapon_pos', 4)
        self.reload_weapon_pos = self.custom_param.get('reload_weapon_pos', 1)
        super(TetrapodSprintShoot, self).read_data_from_custom_param()

    def _fire(self):
        self.ev_g_try_weapon_attack_begin(self.enhanced_weapon_pos if self.is_enhanced else self.weapon_pos)
        self.ev_g_try_weapon_attack_end(self.enhanced_weapon_pos if self.is_enhanced else self.weapon_pos)
        self.send_event('E_CANCEL_CAMERA_TRK', '1055_CHARGE')

    def exit(self, enter_states):
        super(TetrapodSprintShoot, self).exit(enter_states)
        self.sub_state = None
        self.send_event('E_ANIM_RATE', LOW_BODY, 1.0)
        self.send_event('E_END_SPRINT')
        return


@editor.state_exporter({('shoot_time', 'param'): {'zh_name': '\xe5\xb0\x84\xe5\x87\xbb\xe6\x97\xb6\xe9\x97\xb4','post_setter': lambda self: self.register_callbacks()
                             },
   ('shoot_anim_time', 'param'): {'zh_name': '\xe5\xb0\x84\xe5\x87\xbb\xe5\x8a\xa8\xe7\x94\xbb\xe6\x97\xb6\xe9\x97\xb4','post_setter': lambda self: self.register_callbacks()
                                  },
   ('shoot_anim_rate', 'param'): {'zh_name': '\xe5\xb0\x84\xe5\x87\xbb\xe5\x8a\xa8\xe7\x94\xbb\xe9\x80\x9f\xe7\x8e\x87','post_setter': lambda self: self.register_callbacks()
                                  }
   })
class TetrapodReloadShoot(StateBase):
    BIND_EVENT = {'E_RELOADING': 'on_reload'
       }
    STATE_NONE = 0
    STATE_SHOOT = 1

    def init_from_dict(self, unit_obj, bdict, sid, info):
        super(TetrapodReloadShoot, self).init_from_dict(unit_obj, bdict, sid, info)
        self.is_enhanced = False
        self.is_end_shoot = False
        self.reload_time = 0.0
        self.start_reload_time = 0.0
        self.shoot_anim = self.custom_param.get('shoot_anim', 'reload_module')
        self.shoot_time = self.custom_param.get('shoot_time', 0.6)
        self.normal_weapon_pos = self.custom_param.get('weapon_pos', 3)
        self.shoot_anim_time = self.custom_param.get('shoot_anim_time', 0.5)
        self.shoot_anim_rate = self.custom_param.get('shoot_anim_rate', 1.0)
        self.reload_weapon_pos = self.custom_param.get('reload_weapon_pos', (1, 4))
        self.register_callbacks()
        self.enable_param_changed_by_buff()

    def register_callbacks(self):
        self.reset_sub_states_callback()
        self.register_substate_callback(self.STATE_SHOOT, 0, self.on_shoot_start)
        self.register_substate_callback(self.STATE_SHOOT, self.shoot_time, self._fire)
        self.register_substate_callback(self.STATE_SHOOT, self.shoot_anim_time / self.shoot_anim_rate, self.on_shoot_end)

    def action_btn_down(self):
        super(TetrapodReloadShoot, self).action_btn_down()
        if not self.sd.ref_is_robot and ShotChecker().check_camera_can_shot():
            return False
        if not self.check_can_active():
            return False
        if not self.ev_g_check_can_weapon_attack(self.normal_weapon_pos):
            return False
        if self.is_active:
            return False
        if self.reload_time and self.start_reload_time:
            if time.time() - self.start_reload_time < self.reload_time:
                return False
        self.send_event('E_TRY_RELOAD', self.reload_weapon_pos[0])
        return True

    def on_reload(self, reload_time, times, weapon_pos):
        if weapon_pos not in self.reload_weapon_pos:
            return
        if not self.sd.ref_reload_shoot:
            return
        if self.is_active:
            return False
        self.reload_time = reload_time
        self.start_reload_time = time.time()
        self.active_self()

    def _fire(self):
        self.ev_g_try_weapon_attack_begin(self.normal_weapon_pos)
        self.ev_g_try_weapon_attack_end(self.normal_weapon_pos)

    def on_shoot_start(self):
        self.send_event('E_POST_ACTION', self.shoot_anim, UP_BODY, 1, loop=False)
        self.send_event('E_ANIM_RATE', UP_BODY, self.shoot_anim_rate)

    def on_shoot_end(self):
        self.send_event('E_ANIM_RATE', UP_BODY, 1.0)
        self.is_end_shoot = True

    def enter(self, leave_states):
        super(TetrapodReloadShoot, self).enter(leave_states)
        self.sub_state = self.STATE_SHOOT
        self.is_end_shoot = False

    def exit(self, enter_states):
        super(TetrapodReloadShoot, self).exit(enter_states)
        self.sub_state = self.STATE_NONE
        self.send_event('E_CLEAR_UP_BODY_ANIM')

    def check_transitions(self):
        if self.is_end_shoot:
            self.disable_self()


@editor.state_exporter({('sprint_start_time', 'param'): {'zh_name': '\xe5\x90\xaf\xe5\x8a\xa8\xe5\x8a\xa8\xe4\xbd\x9c\xe6\x97\xb6\xe9\x97\xb4','post_setter': lambda self: self.register_sub_event()
                                    },
   ('sprint_start_rate', 'param'): {'zh_name': '\xe5\x90\xaf\xe5\x8a\xa8\xe5\x8a\xa8\xe4\xbd\x9c\xe9\x80\x9f\xe7\x8e\x87','post_setter': lambda self: self.register_sub_event()
                                    },
   ('sprint_stop_anim_rate', 'param'): {'zh_name': '\xe5\x88\xb9\xe8\xbd\xa6\xe5\x8a\xa8\xe4\xbd\x9c\xe9\x80\x9f\xe7\x8e\x87','post_setter': lambda self: self.register_sub_event()
                                        },
   ('sprint_stop_anim_time', 'param'): {'zh_name': '\xe5\x88\xb9\xe8\xbd\xa6\xe5\x8a\xa8\xe4\xbd\x9c\xe6\x97\xb6\xe9\x97\xb4','post_setter': lambda self: self.register_sub_event()
                                        },
   ('sprint_stop_break_time', 'param'): {'zh_name': '\xe5\x88\xb9\xe8\xbd\xa6\xe5\x8f\xaf\xe6\x89\x93\xe6\x96\xad\xe6\x97\xb6\xe9\x97\xb4(sprint_stop_break_time)','post_setter': lambda self: self.register_sub_event()
                                         },
   ('sprint_max_speed_increase', 'param'): {'zh_name': '\xe5\xbc\xba\xe5\x88\xb6\xe8\xbf\x9b\xe5\x85\xa5\xe5\x86\xb2\xe9\x94\x8b\xe9\x80\x9f\xe5\xba\xa6\xe6\x8f\x90\xe5\x8d\x87'},('sprint_dec_max_time', 'param'): {'zh_name': '\xe5\xbc\xba\xe5\x88\xb6\xe8\xbf\x9b\xe5\x85\xa5\xe5\x86\xb2\xe9\x94\x8b\xe5\x87\x8f\xe9\x80\x9f\xe5\x88\xb0\xe5\xb8\xb8\xe9\xa9\xbb\xe9\x80\x9f\xe5\xba\xa6\xe7\x9a\x84\xe6\x97\xb6\xe9\x97\xb4'},('max_speed', 'meter'): {'zh_name': '\xe9\xbb\x98\xe8\xae\xa4\xe6\x9c\x80\xe5\xa4\xa7\xe9\x80\x9f\xe5\xba\xa6'},('acc_speed', 'meter'): {'zh_name': '\xe9\xbb\x98\xe8\xae\xa4\xe5\x8a\xa0\xe9\x80\x9f\xe5\xba\xa6'},('step_height', 'meter'): {'zh_name': '\xe5\x86\xb2\xe9\x94\x8b\xe4\xb8\x8b\xe6\x8a\xac\xe8\x84\x9a\xe9\xab\x98\xe5\xba\xa6(step_height)'},('min_turning_angle_boundary', 'angle'): {'zh_name': '\xe8\xbd\xac\xe5\x90\x91\xe8\xa1\x8c\xe9\xa9\xb6\xe9\x80\x9f\xe5\xba\xa6\xe6\x9c\x80\xe5\xb0\x8f\xe8\xa7\x92\xe5\xba\xa6\xe9\x98\x88\xe5\x80\xbc\xef\xbc\x88\xe8\xa7\x92\xe5\xba\xa6\xef\xbc\x89','post_setter': lambda self: self._update_turning_speed_data()
                                             },
   ('max_turning_acc_speed', 'meter'): {'zh_name': '\xe8\xbd\xac\xe5\x90\x91\xe6\x9c\x80\xe5\xa4\xa7\xe8\xa1\x8c\xe9\xa9\xb6\xe5\x8a\xa0\xe9\x80\x9f\xe5\xba\xa6','post_setter': lambda self: self._update_turning_speed_data()
                                        },
   ('max_turning_max_speed', 'meter'): {'zh_name': '\xe8\xbd\xac\xe5\x90\x91\xe6\x9c\x80\xe5\xa4\xa7\xe8\xa1\x8c\xe9\xa9\xb6\xe9\x80\x9f\xe5\xba\xa6','post_setter': lambda self: self._update_turning_speed_data()
                                        },
   ('min_turning_dec_speed', 'meter'): {'zh_name': '\xe8\xbd\xac\xe5\x90\x91\xe6\x9c\x80\xe5\xb0\x8f\xe8\xa1\x8c\xe9\xa9\xb6\xe5\x87\x8f\xe9\x80\x9f\xe5\xba\xa6','post_setter': lambda self: self._update_turning_speed_data()
                                        },
   ('max_turning_angle_boundary', 'angle'): {'zh_name': '\xe8\xbd\xac\xe5\x90\x91\xe8\xa1\x8c\xe9\xa9\xb6\xe9\x80\x9f\xe5\xba\xa6\xe6\x9c\x80\xe5\xa4\xa7\xe8\xa7\x92\xe5\xba\xa6\xe9\x98\x88\xe5\x80\xbc\xef\xbc\x88\xe8\xa7\x92\xe5\xba\xa6\xef\xbc\x89','post_setter': lambda self: self._update_turning_speed_data()
                                             },
   ('min_turning_acc_speed', 'meter'): {'zh_name': '\xe8\xbd\xac\xe5\x90\x91\xe6\x9c\x80\xe5\xb0\x8f\xe8\xa1\x8c\xe9\xa9\xb6\xe5\x8a\xa0\xe9\x80\x9f\xe5\xba\xa6','post_setter': lambda self: self._update_turning_speed_data()
                                        },
   ('min_turning_max_speed', 'meter'): {'zh_name': '\xe8\xbd\xac\xe5\x90\x91\xe6\x9c\x80\xe5\xb0\x8f\xe8\xa1\x8c\xe9\xa9\xb6\xe9\x80\x9f\xe5\xba\xa6','post_setter': lambda self: self._update_turning_speed_data()
                                        },
   ('max_turning_dec_speed', 'meter'): {'zh_name': '\xe8\xbd\xac\xe5\x90\x91\xe6\x9c\x80\xe5\xa4\xa7\xe8\xa1\x8c\xe9\xa9\xb6\xe5\x87\x8f\xe9\x80\x9f\xe5\xba\xa6','post_setter': lambda self: self._update_turning_speed_data()
                                        },
   ('air_acc_speed', 'meter'): {'zh_name': '\xe7\xa9\xba\xe4\xb8\xad\xe5\x8a\xa0\xe9\x80\x9f\xe5\xba\xa6'},('air_max_speed', 'meter'): {'zh_name': '\xe7\xa9\xba\xe4\xb8\xad\xe6\x9c\x80\xe5\xa4\xa7\xe9\x80\x9f\xe5\xba\xa6'},('air_dec_speed', 'meter'): {'zh_name': '\xe7\xa9\xba\xe4\xb8\xad\xe5\x87\x8f\xe9\x80\x9f\xe5\xba\xa6'},('max_anim_move_dir_angle', 'angle'): {'zh_name': '\xe5\x8a\xa8\xe4\xbd\x9c\xe6\x9c\x80\xe5\xa4\xa7\xe5\x80\xbe\xe6\x96\x9c\xe5\xaf\xb9\xe5\xba\x94\xe8\xa7\x92\xe5\xba\xa6'},('min_angle_boundary', 'angle'): {'zh_name': '\xe6\x9c\x80\xe5\xb0\x8f\xe8\xa7\x92\xe5\xba\xa6\xe9\x98\x88\xe5\x80\xbc\xef\xbc\x88\xe8\xa7\x92\xe5\xba\xa6\xef\xbc\x89','post_setter': lambda self: self._update_turn_speed_data()
                                     },
   ('min_turn_speed', 'angle'): {'zh_name': '\xe6\x9c\x80\xe5\xb0\x8f\xe8\xbd\xac\xe5\x90\x91\xe9\x80\x9f\xe5\xba\xa6\xef\xbc\x88\xe8\xa7\x92\xe5\xba\xa6\xef\xbc\x89','post_setter': lambda self: self._update_turn_speed_data()
                                 },
   ('mid_angle_boundary', 'angle'): {'zh_name': '\xe4\xb8\xad\xe9\x97\xb4\xe8\xa7\x92 \xe5\xba\xa6\xe9\x98\x88\xe5\x80\xbc\xef\xbc\x88\xe8\xa7\x92\xe5\xba\xa6\xef\xbc\x89','post_setter': lambda self: self._update_turn_speed_data()
                                     },
   ('mid_turn_speed', 'angle'): {'zh_name': '\xe4\xb8\xad\xe9\x97\xb4\xe8\xbd\xac\xe5\x90\x91\xe9\x80\x9f\xe5\xba\xa6\xef\xbc\x88\xe8\xa7\x92\xe5\xba\xa6\xef\xbc\x89','post_setter': lambda self: self._update_turn_speed_data()
                                 },
   ('max_angle_boundary', 'angle'): {'zh_name': '\xe6\x9c\x80\xe5\xa4\xa7\xe8\xa7\x92\xe5\xba\xa6\xe9\x98\x88\xe5\x80\xbc\xef\xbc\x88\xe8\xa7\x92\xe5\xba\xa6\xef\xbc\x89','post_setter': lambda self: self._update_turn_speed_data()
                                     },
   ('max_turn_speed', 'angle'): {'zh_name': '\xe6\x9c\x80\xe5\xa4\xa7\xe8\xbd\xac\xe5\x90\x91\xe9\x80\x9f\xe5\xba\xa6\xef\xbc\x88\xe8\xa7\x92\xe5\xba\xa6\xef\xbc\x89','post_setter': lambda self: self._update_turn_speed_data()
                                 },
   ('min_offset_boundary', 'angle'): {'zh_name': '\xe6\x9c\x80\xe5\xb0\x8f\xe5\x81\x8f\xe7\xa7\xbb\xe8\xa7\x92\xe5\xba\xa6\xe9\x98\x88\xe5\x80\xbc\xef\xbc\x88\xe8\xa7\x92\xe5\xba\xa6\xef\xbc\x89','post_setter': lambda self: self._update_offset_angle_data()
                                      },
   ('min_offset_angle', 'angle'): {'zh_name': '\xe6\x9c\x80\xe5\xb0\x8f\xe5\x81\x8f\xe7\xa7\xbb\xe8\xa7\x92\xe5\xba\xa6\xef\xbc\x88\xe8\xa7\x92\xe5\xba\xa6\xef\xbc\x89','post_setter': lambda self: self._update_offset_angle_data()
                                   },
   ('max_offset_boundary', 'angle'): {'zh_name': '\xe6\x9c\x80\xe5\xa4\xa7\xe5\x81\x8f\xe7\xa7\xbb\xe8\xa7\x92\xe5\xba\xa6\xe9\x98\x88\xe5\x80\xbc\xef\xbc\x88\xe8\xa7\x92\xe5\xba\xa6\xef\xbc\x89','post_setter': lambda self: self._update_offset_angle_data()
                                      },
   ('max_offset_angle', 'angle'): {'zh_name': '\xe6\x9c\x80\xe5\xa4\xa7\xe5\x81\x8f\xe7\xa7\xbb\xe8\xa7\x92\xe5\xba\xa6\xef\xbc\x88\xe8\xa7\x92\xe5\xba\xa6\xef\xbc\x89','post_setter': lambda self: self._update_offset_angle_data()
                                   }
   })
class TetrapodSprint(StateBase):
    BIND_EVENT = {'E_FORCE_ENTER_SPRINT': 'on_force_enter_sprint',
       'E_ON_FROZEN': 'on_frozen',
       'E_IMMOBILIZED': 'on_immobilize',
       'E_JUMP': 'on_jump_up',
       'E_ON_BEAT_BACK': 'on_beat_back'
       }
    STATE_START = 4
    STATE_SPRINT = 0
    STATE_STOP = 1
    STATE_GROUND = 2
    STATE_NONE = 3
    BREAK_STATE = {MC_MOVE, MC_SHOOT, MC_SECOND_WEAPON_ATTACK}

    def init_from_dict(self, unit_obj, bdict, sid, info):
        super(TetrapodSprint, self).init_from_dict(unit_obj, bdict, sid, info)
        self.read_data_from_custom_param()
        self.init_parameters()
        self.register_sub_event()

    def register_sub_event(self):
        self.reset_sub_states_callback()
        self.register_substate_callback(self.STATE_START, 0, self.on_start)
        self.register_substate_callback(self.STATE_START, self.sprint_start_time / self.sprint_start_rate, self.on_start_end)
        self.register_substate_callback(self.STATE_STOP, 0, self.on_sprint_stop)
        self.register_substate_callback(self.STATE_STOP, self.sprint_stop_break_time, self.on_sprint_stop_break)
        self.register_substate_callback(self.STATE_STOP, self.sprint_stop_anim_time / self.sprint_stop_anim_rate, self.on_end_sprint_stop)
        self.register_substate_callback(self.STATE_GROUND, 0, self.on_ground_start)
        self.register_substate_callback(self.STATE_GROUND, 0.2, self.on_ground_end)

    def init_parameters(self):
        self.event_registered = False
        self.stop_mask = 0
        self.stopped = False
        self.cam_yaw = 0
        self.last_update_target_direction_time_stamp = 0
        self.last_turn_dir = -1
        self.cur_turn_speed = 0.0
        self.turning_with_offset = False
        self.offset_angle = 0.0
        self.offset_angle_symbol = 1
        self.clearing_offset = False
        self.speed_up_factor = 0.0
        self.cur_speed = 0.0
        self.playing_sound = False
        self.sound_rtpc_value = 0.0
        self.tick_rotate_cam_yaw = 0.0
        self.cam_rotate_dir = 1
        self.extra_turn_speed = 1.0
        self.force_enter_sprint = False
        self.sprint_dec_time = 0.0
        self._dash_dis = 0
        self._old_pos = 0.0
        self._is_drag_rocker_enter = False
        self._is_jump = False

    def read_data_from_custom_param(self):
        self.skill_id = self.custom_param.get('skill_id', 0)
        self.sprint_anim = self.custom_param.get('sprint_anim', 'charge')
        self.move_anim = self.custom_param.get('move_anim', 'move')
        self.acc_speed = self.custom_param.get('acc_speed', 40) * NEOX_UNIT_SCALE
        self.max_speed = self.custom_param.get('max_speed', 20) * NEOX_UNIT_SCALE
        self.min_turning_angle_boundary = radians(self.custom_param.get('min_turning_angle_boundary', 10))
        self.max_turning_acc_speed = self.custom_param.get('max_turning_acc_speed', 80) * NEOX_UNIT_SCALE
        self.max_turning_max_speed = self.custom_param.get('max_turning_max_speed', 18) * NEOX_UNIT_SCALE
        self.min_turning_dec_speed = self.custom_param.get('dec_turning_dec_speed', 20) * NEOX_UNIT_SCALE
        self.max_turning_angle_boundary = radians(self.custom_param.get('max_turning_angle_boundary', 80))
        self.min_turning_acc_speed = self.custom_param.get('min_turning_acc_speed', 20) * NEOX_UNIT_SCALE
        self.min_turning_max_speed = self.custom_param.get('min_turning_max_speed', 10) * NEOX_UNIT_SCALE
        self.max_turning_dec_speed = self.custom_param.get('max_turning_dec_speed', 50) * NEOX_UNIT_SCALE
        self._update_turning_speed_data()
        self.air_acc_speed = self.custom_param.get('air_acc_speed', 25) * NEOX_UNIT_SCALE
        self.air_max_speed = self.custom_param.get('air_max_speed', 12) * NEOX_UNIT_SCALE
        self.air_dec_speed = self.custom_param.get('air_dec_speed', 30) * NEOX_UNIT_SCALE
        self.max_anim_move_dir_angle = radians(self.custom_param.get('max_anim_move_dir_angle', 120))
        self.min_angle_boundary = radians(self.custom_param.get('min_angle_boundary', 2))
        self.min_turn_speed = radians(self.custom_param.get('min_turn_speed', 5))
        self.mid_angle_boundary = radians(self.custom_param.get('mid_angle_boundary', 5))
        self.mid_turn_speed = radians(self.custom_param.get('mid_turn_speed', 15))
        self.max_angle_boundary = radians(self.custom_param.get('max_angle_boundary', 70))
        self.max_turn_speed = radians(self.custom_param.get('max_turn_speed', 60))
        self._update_turn_speed_data()
        self.min_offset_boundary = radians(self.custom_param.get('min_offset_boundary', 70))
        self.min_offset_angle = radians(self.custom_param.get('min_offset_angle', 1))
        self.max_offset_boundary = radians(self.custom_param.get('max_offset_boundary', 120))
        self.max_offset_angle = radians(self.custom_param.get('max_offset_angle', 3))
        self._update_offset_angle_data()
        self.cam_rotate_speed = self.custom_param.get('cam_rotate_speed', 10.0)
        self.turn_speed_add = self.custom_param.get('turn_speed_add', 100.0)
        self.sprint_stop_anim = self.custom_param.get('sprint_stop_anim', 'charge_stop')
        self.sprint_stop_anim_rate = self.custom_param.get('sprint_stop_anim_rate', 1.0)
        self.sprint_stop_anim_time = self.custom_param.get('sprint_stop_anim_time', 0.5)
        self.sprint_stop_break_time = self.custom_param.get('sprint_stop_break_time', 0.1)
        self.sprint_max_speed_increase = self.custom_param.get('sprint_sprint_max_speed_increase', 10.0) * NEOX_UNIT_SCALE
        self.sprint_dec_max_time = self.custom_param.get('sprint_dec_max_time', 2.0)
        self.sprint_start_anim = self.custom_param.get('sprint_start_anim', 'charge_start')
        self.sprint_start_time = self.custom_param.get('sprint_start_time', 0.2)
        self.sprint_start_rate = self.custom_param.get('sprint_start_rate', 1.0)
        self.step_height = self.custom_param.get('step_height', 1.0) * NEOX_UNIT_SCALE

    def on_force_enter_sprint(self):
        self.force_enter_sprint = True

    def _update_turning_speed_data(self):
        boundary_distance = self.max_turning_angle_boundary - self.min_turning_angle_boundary
        self.turning_acc_speed_rate = (self.max_turning_acc_speed - self.min_turning_acc_speed) / boundary_distance
        self.turning_max_speed_rate = (self.max_turning_max_speed - self.min_turning_max_speed) / boundary_distance
        self.turning_dec_speed_rate = (self.max_turning_dec_speed - self.min_turning_dec_speed) / boundary_distance

    def _update_turn_speed_data(self):
        self.angle_boundary_data = (
         self.min_angle_boundary, self.mid_angle_boundary, self.max_angle_boundary)
        self.turn_speed_data = (self.min_turn_speed, self.mid_turn_speed, self.max_turn_speed)
        self.angle_speed_rate_data = (
         0.0,
         (self.mid_turn_speed - self.min_turn_speed) / (self.mid_angle_boundary - self.min_angle_boundary),
         (self.max_turn_speed - self.mid_turn_speed) / (self.max_angle_boundary - self.mid_angle_boundary))

    def _update_offset_angle_data(self):
        self.mid_offset_angle_rate = (self.max_offset_angle - self.min_offset_angle) / (self.max_offset_boundary - self.min_offset_boundary)

    def enable_drive(self, enable):
        self.send_event('E_DISABLE_ROCKER_ANIM_DIR', enable)
        global_data.emgr.set_move_rocker_opacity_and_swallow_touch.emit(0 if enable else 255, not enable)
        self.send_event('E_ENABLE_CAMERA_ROTATE_SYNC_TO_MODEL', not enable)
        self.send_event('E_ENABLE_TWIST_PITCH', not enable, need_sync=True)
        self._register_rotate_event(enable)
        if enable:
            self.cam_yaw = self.sd.ref_logic_trans.yaw_target

    def _get_turn_speed(self, angle):
        for i, boundary_angle in enumerate(self.angle_boundary_data):
            if angle <= boundary_angle:
                if i > 0:
                    return self.turn_speed_data[i - 1] + self.angle_speed_rate_data[i] * (angle - self.angle_boundary_data[i - 1])
                return self.turn_speed_data[i]
        else:
            return self.turn_speed_data[-1]

    def _register_rotate_event(self, enable):
        if self.event_registered == enable:
            return
        if enable:
            self.regist_event('E_ROTATE', self.on_rotate)
        else:
            self.unregist_event('E_ROTATE', self.on_rotate)
        self.event_registered = enable

    def _update_rotation(self):
        cur_yaw_target = self.cam_yaw + self.offset_angle * self.offset_angle_symbol
        cur_yaw_target %= CIRCLE_ANGLE
        cur_yaw = self.sd.ref_rotatedata.yaw_head
        angle, symbol = get_angle_difference(cur_yaw, cur_yaw_target)
        if angle == 0:
            self.send_event('E_CHANGE_ANIM_MOVE_DIR', 0, 1)
        else:
            ratio = angle / self.max_anim_move_dir_angle
            if ratio > 1.0:
                ratio = 1.0
            x = ratio
            self.send_event('E_CHANGE_ANIM_MOVE_DIR', x * symbol, 0.1)
        if angle == 0:
            if self.turning_with_offset:
                self.turning_with_offset = False
                self.offset_angle = 0.0
                self.offset_angle_symbol = 0
                angle = fabs(cur_yaw - self.cam_yaw)
                self.clearing_offset = True
            elif self.clearing_offset:
                self.clearing_offset = False
        turn_speed = self.min_turn_speed if self.clearing_offset else self._get_turn_speed(angle) * self.extra_turn_speed
        cur_yaw_target = self.cam_yaw + self.offset_angle * self.offset_angle_symbol
        if self.sd.ref_logic_trans.yaw_target != cur_yaw_target or turn_speed != self.cur_turn_speed:
            self.sd.ref_logic_trans.yaw_target = cur_yaw_target
            self.sd.ref_common_motor.set_yaw_time(angle / turn_speed)
            self.cur_turn_speed = turn_speed

    def _get_offset_angle(self, angle):
        if angle <= self.min_offset_boundary:
            return self.min_offset_angle
        if angle <= self.max_offset_boundary:
            return self.min_offset_angle + self.mid_offset_angle_rate * (angle - self.min_offset_boundary)
        return self.max_offset_angle

    def _update_offset_angle(self):
        if self.clearing_offset:
            self.clearing_offset = False
        cur_yaw = self.sd.ref_rotatedata.yaw_head
        angle, symbol = get_angle_difference(cur_yaw, self.cam_yaw)
        if symbol:
            if angle >= self.min_offset_boundary:
                self.turning_with_offset = True
                self.offset_angle = self._get_offset_angle(angle)
                self.offset_angle_symbol = symbol
            else:
                self.turning_with_offset = False
                self.offset_angle = 0.0
                self.offset_angle_symbol = 0
        else:
            self.turning_with_offset = False
            self.offset_angle = 0.0
            self.offset_angle_symbol = 0

    def _update_cur_speed(self, dt, angle_difference):
        cur_speed = self.cur_speed
        if self.sd.ref_on_ground:
            if angle_difference > 0:
                if angle_difference < self.min_turning_angle_boundary:
                    acc_speed, max_speed, dec_speed = self.max_turning_acc_speed, self.max_turning_max_speed, self.min_turning_dec_speed
                elif angle_difference < self.max_turning_angle_boundary:
                    acc_speed = self.max_turning_acc_speed - angle_difference * self.turning_acc_speed_rate
                    max_speed = self.max_turning_max_speed - angle_difference * self.turning_max_speed_rate
                    dec_speed = self.min_turning_dec_speed + angle_difference * self.turning_dec_speed_rate
                else:
                    acc_speed, max_speed, dec_speed = self.min_turning_acc_speed, self.min_turning_max_speed, self.max_turning_dec_speed
            else:
                acc_speed, max_speed, dec_speed = self.acc_speed, self.max_speed, 130.0
        else:
            acc_speed, max_speed, dec_speed = self.air_acc_speed, self.air_max_speed, self.air_dec_speed
        if self.force_enter_sprint:
            max_speed += self.sprint_max_speed_increase * (self.sprint_dec_max_time - self.sprint_dec_time)
        max_speed *= 1.0 + self.speed_up_factor
        if cur_speed > max_speed:
            cur_speed -= dec_speed * dt
            if cur_speed < max_speed:
                cur_speed = max_speed
        elif cur_speed < max_speed:
            cur_speed += acc_speed * dt
            if cur_speed > max_speed:
                cur_speed = max_speed
        self.cur_speed = cur_speed

    def on_rotate(self, delta_yaw):
        self.cam_yaw += delta_yaw
        self.cam_yaw %= CIRCLE_ANGLE
        if self.stop_mask:
            return
        self._update_offset_angle()
        self._update_rotation()

    def on_beat_back(self, state):
        if state:
            self.send_event('E_END_SPRINT')

    def enter(self, leave_states):
        super(TetrapodSprint, self).enter(leave_states)
        if self.sd.ref_rocker_dir:
            if self.sd.ref_rocker_dir.z < 0.0:
                self._is_drag_rocker_enter = True
        self._is_jump = False
        self.sub_state = self.STATE_START
        self.cur_speed = self.sd.ref_cur_speed
        self.cur_turn_speed = 0.0
        self.turning_with_offset = False
        self.offset_angle = 0.0
        self.offset_angle_symbol = 1
        self.clearing_offset = False
        self.enable_drive(True)
        self.send_event('E_CHANGE_ANIM_MOVE_DIR', 0, 1)
        self.regist_event('E_ON_TOUCH_GROUND', self.on_ground)
        self.on_rotate(0)
        self._start_cal_dash_dist()
        self.send_event('E_UPDATE_SPRINT_UI', True, self.cancel_sprint)
        self.send_event('E_STEP_HEIGHT', self.step_height)
        if self.force_enter_sprint:
            self.send_event('E_ENBALE_8032_STATE_SFX', 'force_sprint', True)
        else:
            self.sound_custom_start()
            self.send_event('E_ENBALE_8032_STATE_SFX', 'sprint', True)
        self.send_event('E_ENBALE_8032_STATE_SFX', 'run_state_loop', True)
        global_data.emgr.disable_free_sight_btn.emit(True)

    def cancel_sprint(self):
        self.sub_state = self.STATE_STOP

    def on_start(self):
        self.send_event('E_POST_ACTION', self.sprint_start_anim, LOW_BODY, 1, loop=False)

    def on_start_end(self):
        self.sub_state = self.STATE_SPRINT
        self.send_event('E_POST_ACTION', self.sprint_anim, LOW_BODY, 6, loop=True)
        self.sound_custom_end()

    def on_sprint_stop(self):
        self.send_event('E_ADD_BLACK_STATE', {MC_SPRINT_DASH, MC_DASH})
        self.send_event('E_POST_ACTION', self.sprint_stop_anim, LOW_BODY, 1)
        self.send_event('E_ANIM_RATE', LOW_BODY, self.sprint_stop_anim_rate)
        self.send_event('E_END_SPRINT')
        self.start_custom_sound('stop_state')

    def on_sprint_stop_break(self):
        self.send_event('E_ADD_WHITE_STATE', self.BREAK_STATE, self.sid)

    def on_ground(self, *args):
        if self.sub_state == self.STATE_STOP:
            return
        self._is_jump = False
        self.sub_state = self.STATE_GROUND
        self.send_event('E_POST_ACTION', self.sprint_anim, LOW_BODY, 6, loop=True)

    def on_ground_start(self):
        self.send_event('E_POST_ACTION', 'charge_jump_03', LOW_BODY, 1, loop=False)

    def on_ground_end(self):
        self.sub_state = self.STATE_SPRINT
        if self._is_jump:
            return
        self.send_event('E_POST_ACTION', self.sprint_anim, LOW_BODY, 6, loop=True)

    def on_jump_up(self, *args):
        if not self.is_active:
            return
        self._is_jump = True

    def on_frozen(self, state, *args):
        if state and self.is_active:
            self.send_event('E_END_SPRINT')
            self.disable_self()

    def on_immobilize(self, state, *args):
        if state and self.is_active:
            self.send_event('E_END_SPRINT')
            self.disable_self()

    def on_end_sprint_stop(self):
        self.send_event('E_ANIM_RATE', LOW_BODY, 1.0)
        self.send_event('E_ADD_WHITE_STATE', {MC_STAND}, self.sid)
        self.disable_self()

    def _start_cal_dash_dist(self):
        self._dash_dis = 0
        self._old_pos = self.ev_g_position()
        self.regist_pos_change(self._on_pos_changed, 0.1)

    def _finish_cal_dash_dist(self):
        self.unregist_pos_change(self._on_pos_changed)
        if self._dash_dis > 0:
            self.send_event('E_CALL_SYNC_METHOD', 'record_mecha_memory', ('8032', MECHA_MEMORY_LEVEL_7, self._dash_dis / NEOX_UNIT_SCALE), False, True)

    def _on_pos_changed(self, pos):
        dist = int((pos - self._old_pos).length) if self._old_pos else 0
        self._old_pos = pos
        if dist > 0:
            self._dash_dis += dist

    def update(self, dt):
        super(TetrapodSprint, self).update(dt)
        if self._is_drag_rocker_enter:
            if not self.sd.ref_rocker_dir or self.sd.ref_rocker_dir and self.sd.ref_rocker_dir.z > -0.0:
                self._is_drag_rocker_enter = False
        if self.is_active and self.sd.ref_rocker_dir and self.sd.ref_rocker_dir.z < -0.5 and self.sub_state != self.STATE_STOP and not self._is_drag_rocker_enter:
            if not self.sd.ref_drag_state:
                self.sub_state = self.STATE_STOP
        if self.force_enter_sprint:
            if self.sprint_dec_time < self.sprint_dec_max_time:
                self.sprint_dec_time += dt
        if self.cam_rotate_dir > 0 and self.tick_rotate_cam_yaw > 0:
            part_ctrl = global_data.game_mgr.scene.get_com('PartCtrl')
            delta = dt * self.cam_rotate_speed * self.cam_rotate_dir
            part_ctrl.rotate_camera(delta, 0, force=True)
            self.tick_rotate_cam_yaw -= delta
            self.extra_turn_speed = self.turn_speed_add
        elif self.cam_rotate_dir < 0 and self.tick_rotate_cam_yaw > 0:
            part_ctrl = global_data.game_mgr.scene.get_com('PartCtrl')
            delta = dt * self.cam_rotate_speed * self.cam_rotate_dir
            part_ctrl.rotate_camera(delta, 0, force=True)
            self.tick_rotate_cam_yaw += delta
            self.extra_turn_speed = self.turn_speed_add
        else:
            self.extra_turn_speed = 1.0
        cur_yaw = self.sd.ref_rotatedata.yaw_head
        self._update_rotation()
        self._update_cur_speed(dt, get_angle_difference(cur_yaw, self.cam_yaw)[0])
        self.sd.ref_cur_speed = self.cur_speed * self.ev_g_get_speed_scale()
        rot = math3d.rotation(0, 0, 0, 1)
        rot.set_axis_angle(UP_VECTOR, cur_yaw)
        self.send_event('E_SET_WALK_DIRECTION', rot.get_forward() * self.sd.ref_cur_speed)
        self.send_event('E_ACTION_MOVE')

    def exit(self, enter_states):
        super(TetrapodSprint, self).exit(enter_states)
        self._is_drag_rocker_enter = False
        self.sprint_dec_time = 0.0
        self.sub_state = self.STATE_NONE
        self.tick_rotate_cam_yaw = 0
        self.sd.ref_logic_trans.yaw_target = self.cam_yaw
        self.sd.ref_common_motor.set_yaw_time(0.2)
        if self.force_enter_sprint:
            self.send_event('E_ENBALE_8032_STATE_SFX', 'force_sprint', False)
        else:
            self.send_event('E_ENBALE_8032_STATE_SFX', 'sprint', False)
        self.force_enter_sprint = False
        self.enable_drive(False)
        self.send_event('E_CHANGE_ANIM_MOVE_DIR', 0, 0)
        self.send_event('E_ACTION_MOVE_STOP')
        self.send_event('E_CLEAR_SPEED')
        self.unregist_event('E_ON_TOUCH_GROUND', self.on_ground)
        self.send_event('E_CLEAR_BLACK_STATE')
        self.send_event('E_UPDATE_SPRINT_UI', False)
        self._finish_cal_dash_dist()
        self.send_event('E_ENBALE_8032_STATE_SFX', 'run_state_loop', False)
        global_data.emgr.disable_free_sight_btn.emit(False)
        self.end_custom_sound('stop_state')
        self.send_event('E_RESET_STEP_HEIGHT')

    def reset_enable_twist_pitch(self, *args):
        self.send_event('E_ENABLE_TWIST_PITCH', True, need_sync=True)

    def destroy(self):
        self._register_rotate_event(False)


SPRINT_DASH_ICON = 'gui/ui_res_2/battle/mech_main/icon_mech8032_4.png'
SHOOT_ICON = 'gui/ui_res_2/battle/mech_main/icon_mech8032_1.png'
DASH_ICON = 'gui/ui_res_2/battle/mech_main/icon_mech8032_6.png'
FORCE_SPRINT = 'gui/ui_res_2/battle/mech_main/icon_mech8032_7.png'

@editor.state_exporter({('switch_keep_time', 'param'): {'zh_name': '\xe8\xbf\x9b\xe5\x85\xa5\xe5\x86\xb2\xe9\x94\x8b\xe7\x8a\xb6\xe6\x80\x81\xe9\x9c\x80\xe4\xbf\x9d\xe6\x8c\x81\xe8\xb7\x91\xe6\xad\xa5\xe6\x97\xb6\xe9\x97\xb4(switch_keep_time)','post_setter': lambda self: self.register_callbacks()
                                   },
   ('reduce_speed_first', 'param'): {'zh_name': '\xe7\xac\xac\xe4\xb8\x80\xe9\x98\xb6\xe6\xae\xb5\xe5\x87\x8f\xe8\xbf\x9b\xe5\xba\xa6\xe9\x80\x9f\xe5\xba\xa6(reduce_speed_first)','post_setter': lambda self: self.register_callbacks()
                                     },
   ('reduce_speed_second', 'param'): {'zh_name': '\xe7\xac\xac\xe4\xba\x8c\xe9\x98\xb6\xe6\xae\xb5\xe5\x87\x8f\xe8\xbf\x9b\xe5\xba\xa6\xe9\x80\x9f\xe5\xba\xa6(reduce_speed_second)','post_setter': lambda self: self.register_callbacks()
                                      },
   ('enter_reduce_second_time', 'param'): {'zh_name': '\xe8\xbf\x9b\xe5\x85\xa5\xe7\xac\xac\xe4\xba\x8c\xe5\x87\x8f\xe8\xbf\x9b\xe5\xba\xa6\xe7\x9a\x84\xe6\x97\xb6\xe9\x97\xb4\xe7\x82\xb9(enter_reduce_second_time)','post_setter': lambda self: self.register_callbacks()
                                           }
   })
class TetrapodSwitch(StateBase):
    BIND_EVENT = {'E_UPDATE_RUNSTATE': 'on_update_runstate',
       'E_END_SPRINT': 'on_end_sprint',
       'E_ENABLE_RELOAD_SHOOT': 'on_change_reload_form',
       'E_FORCE_ENTER_SPRINT': 'on_force_switch_to_sprint',
       'E_ON_FROZEN': 'on_frozen',
       'E_IMMOBILIZED': 'on_immobilize',
       'E_ON_BEAT_BACK': 'on_beat_back'
       }
    STATE_STOP = 1
    STATE_KEEP_RUN = 2
    STATE_SPRINT = 3
    STATE_END_SPRINT = 4
    STATE_REDUCE = 5

    def init_from_dict(self, unit_obj, bdict, sid, info):
        super(TetrapodSwitch, self).init_from_dict(unit_obj, bdict, sid, info)
        self.switch_keep_time = self.custom_param.get('switch_keep_time', 3.0)
        self.reduce_speed_first = self.custom_param.get('reduce_speed_first', 1.0)
        self.reduce_speed_second = self.custom_param.get('reduce_speed_second', 2.0)
        self.enter_reduce_second_time = self.custom_param.get('enter_reduce_second_time', 1.0)
        self.register_callbacks()
        self.sd.ref_cur_state = MECHA_8032_NORMAL
        self.force_enter_sprint = False
        self.arrive_mid_progress = False
        self.cur_progress = 0.0
        self.cur_reduce_speed = 0.0

    def register_callbacks(self):
        self.reset_sub_states_callback()
        self.register_substate_callback(self.STATE_STOP, 0, self.on_end_runstate)
        self.register_substate_callback(self.STATE_KEEP_RUN, 0, self.on_enter_run)
        self.register_substate_callback(self.STATE_SPRINT, 0, self.on_enter_sprint)
        self.register_substate_callback(self.STATE_END_SPRINT, 0, self.on_end_sprint)
        self.register_substate_callback(self.STATE_REDUCE, 0, self.on_enter_reduce_step_first)
        self.register_substate_callback(self.STATE_REDUCE, self.enter_reduce_second_time, self.on_enter_reduce_step_second)

    def on_init_complete(self):
        super(TetrapodSwitch, self).on_init_complete()

    def on_update_runstate(self, state):
        if not self.is_active:
            self.active_self()
        if self.sd.ref_cur_state == MECHA_8032_SPRINT:
            return
        if self.force_enter_sprint:
            return
        if state:
            self.sub_state = self.STATE_KEEP_RUN
        else:
            self.sub_state = self.STATE_REDUCE

    def on_frozen(self, *args):
        if self.sd.ref_cur_state == MECHA_8032_SPRINT:
            self.on_end_sprint()

    def on_immobilize(self, *args):
        if self.sd.ref_cur_state == MECHA_8032_SPRINT:
            self.on_end_sprint()

    def on_beat_back(self, *args):
        if self.sd.ref_cur_state == MECHA_8032_SPRINT:
            self.on_end_sprint()

    def on_enter_run(self):
        self.send_event('E_UPDATE_RUNSTATE_UI', True, self.cur_progress, self.switch_keep_time, 1.0)

    def on_force_switch_to_sprint(self):
        self.force_enter_sprint = True
        self.active_self()
        self.on_switch_to_sprint()

    def on_switch_to_sprint(self):
        self.sub_state = self.STATE_SPRINT
        self.send_event('E_ENBALE_8032_STATE_SFX', 'run_state_mid', False)

    def on_enter_sprint(self):
        self.sd.ref_cur_state = MECHA_8032_SPRINT
        self.send_event('E_ACTIVE_STATE', MC_SPRINT)
        self.send_event('E_SWITCH_ACTION', 'action5', MC_OTHER_JUMP_1)
        self.send_event('E_SWITCH_ACTION', 'action6', MC_DASH)
        self.send_event('E_REPLACE_STATE_PARAM', MC_JUMP_2, MC_OTHER_JUMP_2)
        self.send_event('E_REPLACE_STATE_PARAM', MC_JUMP_3, MC_OTHER_JUMP_3)
        self.send_event('E_REPLACE_STATE_PARAM', MC_SUPER_JUMP, MC_OTHER_SUPER_JUMP)
        self.send_event('E_SWITCH_ACTION', 'action1', MC_SPRINT_DASH)
        self.send_event('E_SWITCH_ACTION', 'action2', MC_SPRINT_DASH)
        self.send_event('E_SWITCH_ACTION', 'action3', MC_SPRINT_DASH)
        self.send_event('E_SET_ACTION_ICON', 'action1', SPRINT_DASH_ICON)
        self.send_event('E_SET_ACTION_ICON', 'action2', SPRINT_DASH_ICON)
        self.send_event('E_SET_ACTION_ICON', 'action3', SPRINT_DASH_ICON)
        self.send_event('E_SET_ACTION_ICON', 'action6', DASH_ICON)
        self.send_event('E_CALL_SYNC_METHOD', 'update_8032_run_state', (MECHA_8032_ENTER_SPRINT,))

    def on_end_sprint(self):
        self.sd.ref_cur_state = MECHA_8032_NORMAL
        self.send_event('E_SWITCH_ACTION', 'action5', MC_JUMP_1)
        self.send_event('E_REPLACE_STATE_PARAM', MC_JUMP_2, MC_JUMP_2)
        self.send_event('E_REPLACE_STATE_PARAM', MC_JUMP_3, MC_JUMP_3)
        self.send_event('E_REPLACE_STATE_PARAM', MC_SUPER_JUMP, MC_SUPER_JUMP)
        self.send_event('E_SWITCH_ACTION', 'action1', MC_SHOOT)
        self.send_event('E_SWITCH_ACTION', 'action2', MC_SHOOT)
        self.send_event('E_SWITCH_ACTION', 'action3', MC_SHOOT)
        self.send_event('E_SWITCH_ACTION', 'action6', MC_FORCE_SPRINT)
        self.send_event('E_SET_ACTION_ICON', 'action1', SHOOT_ICON)
        self.send_event('E_SET_ACTION_ICON', 'action2', SHOOT_ICON)
        self.send_event('E_SET_ACTION_ICON', 'action3', SHOOT_ICON)
        self.send_event('E_SET_ACTION_ICON', 'action6', FORCE_SPRINT)
        self.send_event('E_CALL_SYNC_METHOD', 'update_8032_run_state', (MECHA_8032_STOP_SPRINT,))
        self.disable_self()

    def on_enter_reduce_step_first(self):
        self.arrive_mid_progress = False
        self.cur_reduce_speed = self.reduce_speed_first
        self.send_event('E_UPDATE_RUNSTATE_UI', False, self.cur_progress, self.switch_keep_time, self.cur_reduce_speed * -1.0)
        self.send_event('E_ENBALE_8032_STATE_SFX', 'run_state_mid', False)

    def on_enter_reduce_step_second(self):
        self.cur_reduce_speed = self.reduce_speed_second
        self.send_event('E_UPDATE_RUNSTATE_UI', False, self.cur_progress, self.switch_keep_time, self.cur_reduce_speed * -1.0)

    def on_end_runstate(self):
        self.send_event('E_ENBALE_8032_STATE_SFX', 'run_state_mid', False)
        self.disable_self()

    def exit(self, enter_states):
        super(TetrapodSwitch, self).exit(enter_states)
        self.cur_progress = 0.0
        self.cur_reduce_speed = 0.0
        self.force_enter_sprint = False
        self.arrive_mid_progress = False
        self.send_event('E_ENBALE_8032_STATE_SFX', 'run_state_mid', False)

    def update(self, dt):
        super(TetrapodSwitch, self).update(dt)
        if self.sub_state == self.STATE_KEEP_RUN:
            self.cur_progress += dt
            if self.cur_progress >= self.switch_keep_time / 2.0 and not self.arrive_mid_progress:
                self.arrive_mid_progress = True
                self.send_event('E_ENBALE_8032_STATE_SFX', 'run_state_mid', True)
            if self.cur_progress >= self.switch_keep_time:
                self.on_switch_to_sprint()
        if self.sub_state == self.STATE_REDUCE:
            self.cur_progress -= self.cur_reduce_speed * dt
            if self.cur_progress <= 0.0 and self.sub_state != self.STATE_STOP:
                self.sub_state = self.STATE_STOP

    def on_change_reload_form(self, state):
        self.sd.ref_reload_shoot = state
        if state:
            self.send_event('E_SWITCH_ACTION', 'action8', MC_RELOAD_SHOOT)
        else:
            self.send_event('E_SWITCH_ACTION', 'action8', MC_RELOAD)


class TetrapodForceSprint(StateBase):
    BIND_EVENT = {'E_END_SPRINT': 'end_force_sprint'
       }

    def init_from_dict(self, unit_obj, bdict, sid, info):
        super(TetrapodForceSprint, self).init_from_dict(unit_obj, bdict, sid, info)
        self.skill_id = self.custom_param.get('skill_id', 803256)
        self.force_enter = False

    def action_btn_down(self):
        if not self.check_can_active():
            return False
        if not self.check_can_cast_skill():
            return False
        self.active_self()
        super(TetrapodForceSprint, self).action_btn_down()
        return True

    def enter(self, leave_states):
        super(TetrapodForceSprint, self).enter(leave_states)
        self.force_enter = True
        self.send_event('E_DO_SKILL', self.skill_id)
        self.send_event('E_FORCE_ENTER_SPRINT')
        self.send_event('E_UPDATE_RUNSTATE_UI', False, 0.0, 0.0, 1.0)
        self.disable_self()

    def end_force_sprint(self):
        self.force_enter = False
        self.send_event('E_BEGIN_RECOVER_MP', self.skill_id)

    def exit(self, enter_states):
        super(TetrapodForceSprint, self).exit(enter_states)
        self.send_event('E_END_SKILL', self.skill_id)
        self.send_event('E_BEGIN_RECOVER_MP', self.skill_id)