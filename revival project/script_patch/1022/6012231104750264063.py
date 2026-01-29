# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/behavior/Logic8031.py
from __future__ import absolute_import
import math
from six.moves import range
from mobile.common.EntityManager import EntityManager
from .MoveLogic import Walk
from .Logic8011 import ActionDrivenWeaponFire
from .ShootLogic import Reload
from .StateBase import StateBase
from logic.gcommon.cdata.mecha_status_config import *
from logic.gcommon.common_const.character_anim_const import *
from logic.gutils.character_ctrl_utils import ray_check_on_ground, AirWalkDirectionSetter
from logic.gutils.client_unit_tag_utils import register_unit_tag
from logic.gutils.slash_utils import SlashChecker
from logic.gcommon.const import NEOX_UNIT_SCALE
from logic.gcommon.common_const.mecha_const import BEACON_8031_Y_OFFSET
from common.utils.timer import CLOCK
from logic.gcommon import editor
from logic.gcommon.common_const import buff_const
import collision
import math3d

class Walk8031(Walk):

    def enter(self, leave_states):
        super(Walk8031, self).enter(leave_states)
        self.start_custom_sound('loop')
        if MC_RUN not in leave_states:
            self.start_custom_sound('start')

    def exit(self, enter_states):
        super(Walk8031, self).exit(enter_states)
        self.end_custom_sound('start')
        self.end_custom_sound('loop')
        if MC_RUN not in enter_states:
            self.end_custom_sound('end')
            self.start_custom_sound('end')


class ActionDrivenWeaponFire8031(ActionDrivenWeaponFire):

    def trigger_fire(self):
        self.last_fire_time = global_data.game_time
        self.ev_g_try_weapon_attack_begin(self.weapon_pos)
        self.ev_g_try_weapon_attack_end(self.weapon_pos)


class Reload8031(Reload):

    def read_data_from_custom_param(self):
        super(Reload8031, self).read_data_from_custom_param()
        self.use_up_body_bone = self.custom_param.get('use_up_body_bone', False)
        self.reload_anim = self.custom_param.get('reload_anim', 'j_reload')
        self.anim_dir = self.custom_param.get('anim_dir', 1)

    def init_from_dict(self, unit_obj, bdict, sid, state_info):
        super(Reload8031, self).init_from_dict(unit_obj, bdict, sid, state_info)
        self.up_body_set = False

    def enter(self, leave_states):
        super(Reload8031, self).enter(leave_states)
        if self.use_up_body_bone:
            self.send_event('E_UPBODY_BONE', FULL_BODY_BONE)
        self.up_body_set = self.use_up_body_bone
        self.send_event('E_POST_ACTION', self.reload_anim, UP_BODY, self.anim_dir)

    def exit(self, enter_states):
        super(Reload8031, self).exit(enter_states)
        if self.up_body_set:
            global_data.game_mgr.register_logic_timer(lambda : self.sd.ref_up_body_anim is None and self.send_event('E_UPBODY_BONE', DEFAULT_UP_BODY_BONE), interval=0.2, times=1, mode=CLOCK)

    def on_reloaded(self, weapon_pos, cur_bullet_cnt):
        self.reloaded = True
        continue_fire, fire_weapon_pos = self.ev_g_continue_fire()
        if continue_fire and fire_weapon_pos == weapon_pos:
            self.continue_fire = True


@editor.state_exporter({('dash_action_param_list', 'param'): {'zh_name': '\xe5\x86\xb2\xe5\x88\xba\xe5\x8f\x82\xe6\x95\xb0','post_setter': lambda self: self._register_dash_states_callbacks,
                                         'structure': lambda self: self._get_dash_param_structure()},
   ('slash_action_param_list', 'param'): {'zh_name': '\xe6\x8c\xa5\xe7\xa0\x8d\xe5\x8f\x82\xe6\x95\xb0','post_setter': lambda self: self._register_slash_states_callbacks,
                                          'structure': lambda self: self._get_slash_param_structure()},
   ('hit_range', 'param'): {'zh_name': '\xe6\x8c\xa5\xe7\xa0\x8d\xe5\x88\xa4\xe5\xae\x9a\xe8\x8c\x83\xe5\x9b\xb4',
                            'param_type': 'list','structure': [{'zh_name': '\xe6\x8c\xa5\xe7\xa0\x8d\xe5\xae\xbd\xe5\xba\xa6','type': 'float'}, {'zh_name': '\xe6\x8c\xa5\xe7\xa0\x8d\xe9\xab\x98\xe5\xba\xa6','type': 'float'}, {'zh_name': '\xe6\x8c\xa5\xe7\xa0\x8d\xe9\x95\xbf\xe5\xba\xa6\xef\xbc\x88\xe7\xba\xb5\xe6\xb7\xb1\xef\xbc\x89','type': 'float'}],'post_setter': lambda self: self.refresh_hit_range()
                            }
   })
class ReaperSlash(StateBase):
    BIND_EVENT = {'E_EXIT_FOCUS_CAMERA': ('reset_rotation', 99),
       'E_SKILL_BUTTON_BOUNDED': 'on_skill_button_bounded'
       }
    STATE_DASH_1 = 0
    STATE_DASH_2 = 1
    STATE_SLASH_1 = 2
    STATE_SLASH_2 = 3
    THROUGH_TARGET_TAG_VALUE = register_unit_tag(('LLightShield', 'LAttachable', 'LExplosiveRobot'))

    def read_data_from_custom_param(self):
        self.skill_id = self.custom_param.get('skill_id', None)
        self.sub_skill_id = self.custom_param.get('sub_skill_id', None)
        self.action_count = 2
        self.dash_action_param_list = self.custom_param.get('dash_action_param_list', [])
        self.slash_action_param_list = self.custom_param.get('slash_action_param_list', [])
        self.hit_range = self.custom_param.get('hit_range', [5, 5, 5])
        self.hit_bone_name = self.custom_param.get('hit_bone_name', ())
        return

    def _get_dash_param_structure(self):
        param_structure = []
        for i in range(self.action_count):
            sub_structure = dict()
            sub_structure['anim_name'] = {'zh_name': '\xe5\x8a\xa8\xe4\xbd\x9c\xe5\x90\x8d\xe7\xa7\xb0'}
            sub_structure['blend_time'] = {'zh_name': '\xe5\x8a\xa8\xe4\xbd\x9c\xe8\xbf\x87\xe6\xb8\xa1\xe6\x97\xb6\xe9\x95\xbf'}
            sub_structure['dash_speed'] = {'zh_name': '\xe5\x86\xb2\xe5\x88\xba\xe9\x80\x9f\xe5\xba\xa6'}
            sub_structure['max_dash_duration'] = {'zh_name': '\xe6\x9c\x80\xe5\xa4\xa7\xe5\x86\xb2\xe5\x88\xba\xe6\x97\xb6\xe9\x97\xb4'}
            sub_structure['combo_time'] = {'zh_name': '\xe5\x8f\xaf\xe6\x89\x8b\xe5\x8a\xa8\xe8\xa7\xa6\xe5\x8f\x91\xe6\x8c\xa5\xe7\xa0\x8d\xe7\x9a\x84\xe6\x9c\x80\xe5\xb0\x8f\xe6\x97\xb6\xe9\x97\xb4\xe9\x97\xb4\xe9\x9a\x94'}
            sub_structure['keep_time'] = {'zh_name': '\xe7\x8a\xb6\xe6\x80\x81\xe5\xad\x98\xe7\x95\x99\xe6\x97\xb6\xe9\x97\xb4'}
            param_structure.append({'zh_name': '\xe7\xac\xac%d\xe6\xae\xb5\xe5\x86\xb2\xe5\x88\xba\xe5\x8f\x82\xe6\x95\xb0' % (i + 1),'type': 'dict','kwargs': {'structure': sub_structure}})

        return param_structure

    def _register_dash_state_callback(self, state_index):
        self.reset_sub_state_callback(state_index)
        param = self.dash_action_param_list[state_index]
        self.register_substate_callback(state_index, 0, self.on_begin_dash)
        self.register_substate_callback(state_index, param['max_dash_duration'], self.on_end_dash)

    def _register_dash_states_callbacks(self):
        for i in range(self.action_count):
            self._register_dash_state_callback(i)

    def _get_slash_param_structure(self):
        param_structure = []
        for i in range(self.action_count):
            sub_structure = dict()
            sub_structure['anim_name'] = {'zh_name': '\xe5\x8a\xa8\xe4\xbd\x9c\xe5\x90\x8d\xe7\xa7\xb0'}
            sub_structure['anim_duration'] = {'zh_name': '\xe5\x8a\xa8\xe4\xbd\x9c\xe6\x88\xaa\xe5\x8f\x96\xe6\x92\xad\xe6\x94\xbe\xe6\x97\xb6\xe9\x95\xbf'}
            sub_structure['anim_rate'] = {'zh_name': '\xe5\x8a\xa8\xe4\xbd\x9c\xe6\x92\xad\xe6\x94\xbe\xe9\x80\x9f\xe7\x8e\x87'}
            sub_structure['blend_time'] = {'zh_name': '\xe5\x8a\xa8\xe4\xbd\x9c\xe8\xbf\x87\xe6\xb8\xa1\xe6\x97\xb6\xe9\x95\xbf'}
            sub_structure['move_speed'] = {'zh_name': '\xe7\xa7\xbb\xe5\x8a\xa8\xe9\x80\x9f\xe5\xba\xa6(\xe7\xb1\xb3)'}
            sub_structure['end_move_time'] = {'zh_name': '\xe5\x81\x9c\xe6\xad\xa2\xe7\xa7\xbb\xe5\x8a\xa8\xe6\x97\xb6\xe9\x97\xb4'}
            sub_structure['begin_attack_time'] = {'zh_name': '\xe5\xbc\x80\xe5\xa7\x8b\xe6\x94\xbb\xe5\x87\xbb\xe6\x97\xb6\xe9\x97\xb4'}
            sub_structure['begin_damage_time'] = {'zh_name': '\xe5\xbc\x80\xe5\xa7\x8b\xe7\xbb\x93\xe7\xae\x97\xe4\xbc\xa4\xe5\xae\xb3\xe6\x97\xb6\xe9\x97\xb4'}
            sub_structure['end_attack_time'] = {'zh_name': '\xe7\xbb\x93\xe6\x9d\x9f\xe6\x94\xbb\xe5\x87\xbb\xe6\x97\xb6\xe9\x97\xb4'}
            sub_structure['combo_time'] = {'zh_name': '\xe8\xbf\x9e\xe5\x87\xbb\xe6\x97\xb6\xe9\x97\xb4'}
            sub_structure['break_time'] = {'zh_name': '\xe5\x8f\xaf\xe6\x89\x93\xe6\x96\xad\xe6\x97\xb6\xe9\x97\xb4'}
            param_structure.append({'zh_name': '\xe7\xac\xac%d\xe6\xae\xb5\xe6\x8c\xa5\xe7\xa0\x8d\xe5\x8f\x82\xe6\x95\xb0' % (i + 1),'type': 'dict','kwargs': {'structure': sub_structure}})

        return param_structure

    def _register_slash_state_callback(self, state_index):
        self.reset_sub_state_callback(state_index)
        param = self.slash_action_param_list[state_index - self.action_count]
        anim_rate = param['anim_rate']
        self.register_substate_callback(state_index, 0, self.on_begin_slash)
        self.register_substate_callback(state_index, param['end_move_time'] / anim_rate, self.on_end_slash_move)
        self.register_substate_callback(state_index, param['begin_attack_time'] / anim_rate, self.on_begin_attack)
        self.register_substate_callback(state_index, param['begin_damage_time'] / anim_rate, self.on_begin_damage)
        self.register_substate_callback(state_index, param['end_attack_time'] / anim_rate, self.on_end_attack)
        self.register_substate_callback(state_index, param['break_time'] / anim_rate, self.on_enable_break)
        self.register_substate_callback(state_index, param['anim_duration'], self.on_end_slash)

    def _register_slash_states_callbacks(self):
        for i in range(self.action_count, self.action_count + self.action_count):
            self._register_slash_state_callback(i)

    def refresh_hit_range(self):
        if self.slash_checker:
            hit_range = [ value * NEOX_UNIT_SCALE for value in self.hit_range ]
            hit_range[2] += self.hit_depth_add_value * NEOX_UNIT_SCALE
            self.slash_checker.refresh_hit_range(*hit_range)
        self.notify_outer_parameters()

    def init_from_dict(self, unit_obj, bdict, sid, info):
        super(ReaperSlash, self).init_from_dict(unit_obj, bdict, sid, info)
        self.new_custom_param = self.custom_param
        self.read_data_from_custom_param()
        self._register_dash_states_callbacks()
        self._register_slash_states_callbacks()
        self.air_walk_direction_setter = AirWalkDirectionSetter(self)
        self.hit_depth_add_value = 0
        self.slash_checker = SlashChecker(self, self.skill_id, [ value * NEOX_UNIT_SCALE for value in self.hit_range ], self.hit_bone_name)
        self.processing_rotation = False
        self.event_registered = False
        self.cam_yaw = 0
        self.yaw_forbidden = False
        self.last_dash_time = 0
        self.last_dash_state = self.STATE_DASH_1
        self.move_speed = 0
        self.moving = False
        self.breakable = False
        self.btn_down = False
        self.can_slash_in_advance = False
        self.face_to_cursed_target = False
        self.rogue_acc_ratio = 0.0
        self.enable_param_changed_by_buff()

    def notify_outer_parameters(self):
        col_size = [ value * NEOX_UNIT_SCALE / 4 for value in self.hit_range ]
        self.send_event('E_CREATE_CONTACT_COLLISION', self.sid, {'shape': collision.BOX,
           'size': col_size,
           'offset_vec': [
                        0, col_size[1], col_size[2]],
           'check_front_only': True
           })

    def on_init_complete(self):
        super(ReaperSlash, self).on_init_complete()
        self.notify_outer_parameters()

    def destroy(self):
        super(ReaperSlash, self).destroy()
        if self.air_walk_direction_setter:
            self.air_walk_direction_setter.destroy()
            self.air_walk_direction_setter = None
        if self.slash_checker:
            self.slash_checker.destroy()
            self.slash_checker = None
        if self.yaw_forbidden:
            global_data.emgr.enable_camera_yaw.emit(True)
            self.yaw_forbidden = False
        return

    def refresh_param_changed(self):
        self.refresh_hit_range()

    def check_can_cast_skill(self):
        if not self.skill_id or not self.sub_skill_id:
            return True
        return self.ev_g_can_cast_skill(self.skill_id) and self.ev_g_can_cast_skill(self.sub_skill_id)

    def action_btn_down(self):
        self.btn_down = True
        if self.is_active:
            if self.sub_state < self.action_count:
                if self.can_slash_in_advance and self.sub_sid_timer >= self.dash_action_param_list[self.sub_state]['combo_time']:
                    self.on_end_dash()
            elif self.check_can_cast_skill() and self.sub_sid_timer >= self.slash_action_param_list[self.sub_state - self.action_count]['combo_time']:
                self.sub_state = (self.sub_state % self.action_count + 1) % self.action_count
                self.send_event('E_CLEAR_WHITE_STATE', self.sid)
                self.check_enter_state_camera()
        else:
            if not self.check_can_active():
                return False
            if not self.check_can_cast_skill():
                return False
            self.active_self()
        super(ReaperSlash, self).action_btn_down()
        return True

    def action_btn_up(self):
        super(ReaperSlash, self).action_btn_up()
        self.btn_down = False
        self.can_slash_in_advance = True

    def enter(self, leave_states):
        super(ReaperSlash, self).enter(leave_states)
        keep_time = self.dash_action_param_list[self.last_dash_state]['keep_time']
        if global_data.game_time - self.last_dash_time <= keep_time:
            self.sub_state = (self.last_dash_state + 1) % self.action_count
        else:
            self.sub_state = self.STATE_DASH_1

    def reset_rotation(self):
        yaw = self.sd.ref_effective_camera_rot.get_forward().yaw
        self.sd.ref_logic_trans.yaw_target = yaw
        self.sd.ref_common_motor.set_yaw_time(0.2)
        self.send_event('E_ENABLE_CAMERA_ROTATE_SYNC_TO_MODEL', True)

    def on_begin_dash(self):
        if self.btn_down:
            self.can_slash_in_advance = False
        else:
            self.can_slash_in_advance = True
        self.end_custom_sound('dash')
        self.start_custom_sound('dash')
        self.send_event('E_GRAVITY', 0)
        self.send_event('E_CLEAR_SPEED')
        self.send_event('E_VERTICAL_SPEED', 0)
        self.reset_rotation()
        self.air_walk_direction_setter.reset()
        self.breakable = False
        param = self.dash_action_param_list[self.sub_state]
        self.send_event('E_ANIM_RATE', LOW_BODY, 1.0)
        self.send_event('E_POST_ACTION', param['anim_name'], LOW_BODY, 1, blend_time=param['blend_time'])
        self.move_speed = param['dash_speed'] * NEOX_UNIT_SCALE
        self.moving = True
        self.send_event('E_DO_SKILL', self.skill_id)
        self.send_event('E_DO_SKILL', self.sub_skill_id)
        self.send_event('E_ENABLE_CHECK_CONTACT_TARGET', self.sid, True, self.on_contact_targets)
        self.send_event('E_PLAY_DASH_EFFECT', True)
        self.last_dash_state = self.sub_state
        self.last_dash_time = global_data.game_time
        effect = global_data.emgr.show_screen_effect.emit('MeleeRushEffect', {})
        if effect:
            effect = effect[0]
            effect and effect.show()
        self.init_rogue_param()

    def on_end_dash(self):
        self.sub_state += self.action_count
        self.moving = False
        self.send_event('E_ENABLE_CHECK_CONTACT_TARGET', self.sid, False)
        self.send_event('E_PLAY_DASH_EFFECT', False)

    def on_begin_slash(self):
        if self.sub_state & 1:
            sound_key = 'slash_r'
        else:
            sound_key = 'slash_l'
        self.end_custom_sound(sound_key)
        self.start_custom_sound(sound_key)
        param = self.slash_action_param_list[self.sub_state - self.action_count]
        self.send_event('E_ANIM_RATE', LOW_BODY, param['anim_rate'])
        self.send_event('E_POST_ACTION', param['anim_name'], LOW_BODY, 1, blend_time=param['blend_time'])
        self.move_speed = param['move_speed'] * NEOX_UNIT_SCALE
        self.moving = True
        self.yaw_forbidden = True

    def on_end_slash_move(self):
        self.moving = False
        self.send_event('E_CLEAR_SPEED')
        self.send_event('E_VERTICAL_SPEED', 0)

    def on_begin_attack(self):
        self.slash_checker.begin_check()
        self.send_event('E_ENABLE_CAMERA_ROTATE_SYNC_TO_MODEL', False)
        self.send_event('E_SHOW_SLASH_HIT_SCREEN_SFX')

    def on_begin_damage(self):
        self.slash_checker.set_damage_settlement_on(True)

    def on_end_attack(self):
        self.slash_checker.end_check()
        self.check_exit_state_camera()

    def on_enable_break(self):
        self.send_event('E_ADD_WHITE_STATE', {MC_JUMP_2, MC_MOVE, MC_SHOOT, MC_DASH}, self.sid)
        if self.ev_g_on_ground() or ray_check_on_ground(self):
            self.send_event('E_RESET_GRAVITY')
        self.breakable = True

    def on_end_slash(self):
        self.send_event('E_ADD_WHITE_STATE', {MC_STAND}, self.sid)

    def update(self, dt):
        super(ReaperSlash, self).update(dt)
        if self.moving and not self.slash_checker.moving_stopped:
            forward = self.sd.ref_effective_camera_rot.get_forward()
            ex_move_speed = self.move_speed * (1.0 + self.rogue_acc_ratio)
            walk_direction = forward * ex_move_speed
            self.air_walk_direction_setter.execute(walk_direction)

    def check_transitions(self):
        if self.breakable:
            if self.ev_g_on_ground() or ray_check_on_ground(self):
                if self.sd.ref_rocker_dir and not self.sd.ref_rocker_dir.is_zero:
                    return MC_MOVE
                return MC_STAND
            else:
                return MC_JUMP_2

    def _check_custom_param_refreshed(self):
        if self.new_custom_param is not self.custom_param:
            self.custom_param = self.new_custom_param
            self.read_data_from_custom_param()
            self._register_dash_states_callbacks()
            self._register_slash_states_callbacks()
            self.refresh_hit_range()

    def exit(self, enter_states):
        super(ReaperSlash, self).exit(enter_states)
        self.reset_rotation()
        self.send_event('E_ENABLE_CAMERA_ROTATE_SYNC_TO_MODEL', True)
        self.send_event('E_RESET_GRAVITY')
        if self.yaw_forbidden:
            global_data.emgr.enable_camera_yaw.emit(True)
            self.yaw_forbidden = False
        if self.sub_state < self.action_count:
            self.send_event('E_ENABLE_CHECK_CONTACT_TARGET', self.sid, False)
        else:
            self.slash_checker.end_check()
        self.send_event('E_PLAY_DASH_EFFECT', False)
        self._check_custom_param_refreshed()
        global_data.emgr.destroy_screen_effect.emit('MeleeRushEffect')

    def refresh_action_param(self, action_param, custom_param):
        super(ReaperSlash, self).refresh_action_param(action_param, custom_param)
        self.new_custom_param = custom_param
        if not self.is_active:
            self._check_custom_param_refreshed()

    def on_contact_targets(self, target_list):
        if target_list:
            for target in target_list:
                if target.MASK & self.THROUGH_TARGET_TAG_VALUE == 0:
                    self.on_end_dash()
                    break

    def check_face_to_any_cursed_target(self, max_dist, max_angle):
        forward = self.sd.ref_effective_camera_rot.get_forward()
        my_pos = self.ev_g_position()
        all_mecha_entities = EntityManager.get_entities_by_type('Mecha')
        for mecha_eid in all_mecha_entities:
            mecha = all_mecha_entities[mecha_eid]
            if not mecha or not mecha.logic:
                continue
            if not mecha.logic.ev_g_has_buff_by_id(buff_const.BUFF_ID_8031_CURSE):
                continue
            target_pos = mecha.logic.ev_g_position()
            pos_vec = target_pos - my_pos
            if pos_vec.is_zero:
                continue
            if pos_vec.length > max_dist:
                continue
            pos_vec.normalize()
            cos_v = pos_vec.dot(forward)
            if abs(cos_v) < 1.0 and math.radians(max_angle * 0.5) >= math.acos(cos_v):
                return True

        return False

    def init_rogue_param(self):
        if self.ev_g_has_buff_by_id(buff_const.BUFF_ID_8031_ROGUE):
            buff_data = self.ev_g_get_buff(buff_const.BUFF_GLOBAL_KEY, buff_const.BUFF_ID_8031_ROGUE)
            for buff_idx in buff_data:
                one_buff_data = buff_data[buff_idx]
                self.rogue_acc_ratio = one_buff_data.get('acc_rate', 0.0)
                max_dist = one_buff_data.get('max_dist', 0.0)
                max_angle = one_buff_data.get('max_angle', 0.0)
                break

            self.face_to_cursed_target = self.check_face_to_any_cursed_target(max_dist * NEOX_UNIT_SCALE, max_angle)
            if not self.face_to_cursed_target:
                self.rogue_acc_ratio = 0.0
        else:
            self.rogue_acc_ratio = 0.0
            self.face_to_cursed_target = False

    def on_skill_button_bounded(self, skill_id):
        if self.skill_id != skill_id:
            return
        self.send_event('E_ADD_ACTION_SUB_SKILL_ID', self.bind_action_id, self.sub_skill_id)


@editor.state_exporter({('dash_duration', 'param'): {'zh_name': '\xe5\x86\xb2\xe5\x88\xba\xe6\x97\xb6\xe9\x95\xbf'},('dash_speed', 'meter'): {'zh_name': '\xe5\x86\xb2\xe5\x88\xba\xe9\x80\x9f\xe5\xba\xa6'}})
class Dash8031(StateBase):
    BIND_EVENT = {'E_END_REAPER_SHAPE_SKILL': 'end_skill'
       }

    def read_data_from_custom_param(self):
        self.skill_id = self.custom_param.get('skill_id', None)
        self.dash_duration = self.custom_param.get('dash_duration', 0.5)
        self.dash_speed = self.custom_param.get('dash_speed', 100) * NEOX_UNIT_SCALE
        return

    def init_from_dict(self, unit_obj, bdict, sid, info):
        super(Dash8031, self).init_from_dict(unit_obj, bdict, sid, info)
        self.read_data_from_custom_param()
        self.need_exit = False
        self.need_reset_gravity = False

    def end_skill(self, teleport_back=True):
        self.send_event('E_END_SKILL', self.skill_id, teleport_back)
        self.send_event('E_BEGIN_RECOVER_MP', self.skill_id)

    def action_btn_down(self):
        if self.sd.ref_is_reaper_shape:
            self.end_skill()
        elif not self.is_active:
            if not self.check_can_active():
                return
            if not self.check_can_cast_skill():
                return
            self.active_self()
        super(Dash8031, self).action_btn_down()
        return True

    @staticmethod
    def _get_dash_anim_name(rocker_dir):
        if abs(rocker_dir.z) > abs(rocker_dir.x):
            if rocker_dir.z >= 0:
                return 'dash_f'
            return 'dash_b'
        if rocker_dir.x < 0:
            return 'dash_l'
        return 'dash_r'

    def enter(self, leave_states):
        super(Dash8031, self).enter(leave_states)
        pos = self.ev_g_position()
        self.send_event('E_DO_SKILL', self.skill_id, pos.x, pos.y + BEACON_8031_Y_OFFSET, pos.z)
        rocker_dir = self.sd.ref_rocker_dir
        if rocker_dir and not rocker_dir.is_zero:
            anim_name = self._get_dash_anim_name(rocker_dir)
            rot = self.ev_g_rotation()
            move_dir = rot.rotate_vector(rocker_dir)
        else:
            anim_name = 'dash_f'
            move_dir = self.ev_g_forward()
        self.send_event('E_POST_ACTION', anim_name, LOW_BODY, 1, loop=True)
        self.need_reset_gravity = not self.ev_g_on_ground()
        if self.need_reset_gravity:
            self.send_event('E_GRAVITY', 0)
            self.send_event('E_VERTICAL_SPEED', 0)
        self.send_event('E_SET_WALK_DIRECTION', move_dir * self.dash_speed)
        self.send_event('E_PLAY_DASH_EFFECT', True, (move_dir.x, move_dir.y, move_dir.z))
        self.sd.ref_cur_speed = self.dash_speed
        self.need_exit = False

    def update(self, dt):
        super(Dash8031, self).update(dt)
        if self.elapsed_time - dt < self.dash_duration <= self.elapsed_time:
            self.send_event('E_ADD_WHITE_STATE', {MC_STAND, MC_MOVE, MC_JUMP_2}, self.sid)
            self.need_exit = True

    def check_transitions(self):
        if self.need_exit:
            if self.ev_g_on_ground():
                if self.sd.ref_rocker_dir and not self.sd.ref_rocker_dir.is_zero:
                    return MC_MOVE
                return MC_STAND
            return MC_JUMP_2

    def exit(self, enter_states):
        super(Dash8031, self).exit(enter_states)
        if self.need_reset_gravity:
            self.send_event('E_RESET_GRAVITY')
        if not self.ev_g_on_ground():
            self.send_event('E_CLEAR_SPEED')
        if self.sd.ref_is_reaper_shape:
            self.send_event('E_ACTIVE_STATE', MC_TRANSFORM)
        self.send_event('E_PLAY_DASH_EFFECT', False)


@editor.state_exporter({('switch_anim_duration', 'param'): {'zh_name': '\xe5\x8f\x98\xe8\xba\xab\xe5\x8a\xa8\xe4\xbd\x9c\xe6\x97\xb6\xe9\x95\xbf'},('switch_anim_rate', 'param'): {'zh_name': '\xe5\x8f\x98\xe8\xba\xab\xe5\x8a\xa8\xe4\xbd\x9c\xe6\x92\xad\xe6\x94\xbe\xe9\x80\x9f\xe7\x8e\x87'}})
class SwitchReaperShape(StateBase):
    BIND_EVENT = {}

    def read_data_from_custom_param(self):
        self.switch_anim = self.custom_param.get('switch_anim', 'people_to_god')
        self.switch_anim_duration = self.custom_param.get('switch_anim_duration', 0.5)
        self.switch_anim_rate = self.custom_param.get('switch_anim_rate', 1.0)

    def init_from_dict(self, unit_obj, bdict, sid, info):
        super(SwitchReaperShape, self).init_from_dict(unit_obj, bdict, sid, info)
        self.read_data_from_custom_param()

    def enter(self, leave_states):
        super(SwitchReaperShape, self).enter(leave_states)
        self.send_event('E_ANIM_RATE', UP_BODY, self.switch_anim_rate)
        self.send_event('E_UPBODY_BONE', FULL_BODY_BONE)
        self.send_event('E_POST_ACTION', self.switch_anim, UP_BODY, 1)

    def update(self, dt):
        super(SwitchReaperShape, self).update(dt)
        if self.elapsed_time >= self.switch_anim_duration:
            self.disable_self()

    def exit(self, enter_states):
        super(SwitchReaperShape, self).exit(enter_states)
        self.send_event('E_ANIM_RATE', UP_BODY, 1.0)
        self.send_event('E_CLEAR_UP_BODY_ANIM')
        global_data.game_mgr.register_logic_timer(lambda : self.sd.ref_up_body_anim is None and self.send_event('E_UPBODY_BONE', DEFAULT_UP_BODY_BONE), interval=0.2, times=1, mode=CLOCK)

    def refresh_action_param(self, action_param, custom_param):
        super(SwitchReaperShape, self).refresh_action_param(action_param, custom_param)
        self.custom_param = custom_param
        self.read_data_from_custom_param()


@editor.state_exporter({('max_horizontal_dist', 'meter'): {'zh_name': '\xe6\x9c\x80\xe5\xa4\xa7\xe6\xb0\xb4\xe5\xb9\xb3\xe8\xb7\x9d\xe7\xa6\xbb'},('max_vertical_dist', 'meter'): {'zh_name': '\xe6\x9c\x80\xe5\xa4\xa7\xe7\xab\x96\xe7\x9b\xb4\xe8\xb7\x9d\xe7\xa6\xbb'}})
class ReaperShape(StateBase):
    BIND_EVENT = {'E_NOTIFY_REAPER_SHAPE_MAX_DURATION': 'on_notify_reaper_shape_max_duration',
       'E_TRANS_TO_REAPER': 'on_trans_to_reaper',
       'G_STATE_DEFAULT_CAMERA': 'get_state_default_camera',
       'E_DO_RB_POS': ('on_rb_pos_finish', 99)
       }

    def init_from_dict(self, unit_obj, bdict, sid, info):
        super(ReaperShape, self).init_from_dict(unit_obj, bdict, sid, info)
        self.max_horizontal_dist = self.custom_param.get('max_horizontal_dist', 100) * NEOX_UNIT_SCALE
        self.max_vertical_dist = self.custom_param.get('max_vertical_dist', 80) * NEOX_UNIT_SCALE
        self.sd.ref_is_reaper_shape = False
        self.beacon_eid = None
        self.beacon_root_position = None
        self.teleport_sfx_position = None
        self.max_duration = 8
        self.left_time = 0
        self.get_left_time_point = 0
        self.sd.ref_reaper_shape_left_time_percent = 1.0
        return

    def enter(self, leave_states):
        super(ReaperShape, self).enter(leave_states)
        self.sd.ref_is_reaper_shape = True
        self.send_event('E_REFRESH_STATE_PARAM', include_camera_param=True)
        self.send_event('E_SET_ACTION_SELECTED', 'action6', True)
        self.send_event('E_SHOW_REAPER_SHAPE_EFFECT', True)
        self.end_skill_event_sent = False
        self.teleport_sfx_position = None
        cur_time = global_data.game_time
        interval = cur_time - self.get_left_time_point
        if interval > 0:
            self.left_time -= interval
            self.sd.ref_reaper_shape_left_time_percent = self.left_time / self.max_duration
        self.end_custom_sound('loop')
        self.start_custom_sound('loop')
        return

    def _send_end_skill_event(self):
        if self.end_skill_event_sent:
            return
        self.end_skill_event_sent = True
        self.send_event('E_END_REAPER_SHAPE_SKILL', False)

    def update_beacon_root_position(self):
        if self.beacon_eid:
            beacon = global_data.battle.get_entity(self.beacon_eid)
            if beacon and beacon.logic:
                self.beacon_root_position = beacon.logic.sd.ref_root_position
                return True
        self.beacon_root_position = None
        return False

    def update(self, dt):
        super(ReaperShape, self).update(dt)
        self.left_time -= dt
        if self.left_time <= 0:
            self._send_end_skill_event()
            self.left_time = 0
            self.disable_self()
        elif not self.end_skill_event_sent:
            if self.beacon_root_position is None:
                if not self.update_beacon_root_position():
                    return
            cur_pos = self.ev_g_position()
            dist_vec = cur_pos - self.beacon_root_position
            vertical_dist = dist_vec.y
            dist_vec.y = 0
            horizontal_dist = dist_vec.length
            if vertical_dist > self.max_vertical_dist or horizontal_dist > self.max_horizontal_dist:
                self._send_end_skill_event()
        self.sd.ref_reaper_shape_left_time_percent = self.left_time / self.max_duration
        return

    def exit(self, enter_states):
        super(ReaperShape, self).exit(enter_states)
        self.sd.ref_is_reaper_shape = False
        self.beacon_root_position = None
        self.send_event('E_RESET_STATE_PARAM', include_camera_param=True)
        self.send_event('E_SET_ACTION_SELECTED', 'action6', False)
        self.send_event('E_ACTIVE_STATE', MC_TRANSFORM)
        self.send_event('E_SHOW_REAPER_SHAPE_EFFECT', False)
        self.end_custom_sound('loop')
        self.end_custom_sound('end')
        self.start_custom_sound('end')
        return

    def on_notify_reaper_shape_max_duration(self, max_duration):
        self.max_duration = max_duration

    def on_trans_to_reaper(self, left_time, beacon_eid=None):
        self.left_time = left_time
        self.get_left_time_point = global_data.game_time
        self.sd.ref_reaper_shape_left_time_percent = self.left_time / self.max_duration
        self.beacon_eid = beacon_eid
        if left_time > 0:
            self.active_self()
            self.sd.ref_socket_res_agent.set_sfx_res_visible(True, 'reaper')
        else:
            self.disable_self()
            self.teleport_sfx_position = self.ev_g_position()
            self.sd.ref_socket_res_agent.set_sfx_res_visible(False, 'reaper')
            self.send_event('E_END_REAPER_SHAPE_SKILL')

    def get_state_default_camera(self):
        if self.is_active:
            return self.state_camera_conf.get('cam')
        else:
            return None

    def on_rb_pos_finish(self, *args):
        if self.ev_g_is_avatar() and self.teleport_sfx_position:
            pos = self.teleport_sfx_position
            rot = self.ev_g_rotation()
            self.send_event('E_SHOW_TELEPORT_SHADOW_SFX', (pos.x, pos.y, pos.z), (rot.x, rot.y, rot.z, rot.w))
            offset_vector = math3d.vector(0, BEACON_8031_Y_OFFSET, 0)
            guide_start_pos = pos + offset_vector
            guide_end_pos = self.ev_g_position() + offset_vector
            self.send_event('E_SHOW_TELEPORT_GUIDE_SFX', (guide_start_pos.x, guide_start_pos.y, guide_start_pos.z), (
             guide_end_pos.x, guide_end_pos.y, guide_end_pos.z))
            self.teleport_sfx_position = None
            self.send_event('E_VERTICAL_SPEED', 0)
            self.send_event('E_CLEAR_SPEED')
        return