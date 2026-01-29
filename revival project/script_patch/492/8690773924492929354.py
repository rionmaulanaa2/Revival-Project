# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/behavior/Logic8021.py
from __future__ import absolute_import
from six.moves import range
import math3d
from common.cfg import confmgr
from collision import col_object, BOX, INCLUDE_FILTER, SPHERE
from logic.gcommon.common_const.collision_const import GROUP_DYNAMIC_SHOOTUNIT, GROUP_CAMERA_COLL, BREAK_TRIGGER_TYPE_WEAPON
from logic.gutils.scene_utils import trigger_show_outline
import world
import math
from math3d import vector, matrix
from logic.gcommon import editor
from .StateBase import StateBase
from logic.gcommon.cdata.mecha_status_config import *
from logic.gcommon.common_const.character_anim_const import *
from logic.gcommon.const import NEOX_UNIT_SCALE, SOUND_TYPE_MECHA_FIRE
from logic.gcommon.common_const.attr_const import SEC_WEAPON_RANGE_FACTOR_8021
from logic.gutils import detection_utils
from logic.gutils.client_unit_tag_utils import register_unit_tag
from logic.gutils.slash_utils import SlashChecker
from logic.gcommon.common_utils import status_utils
from logic.gcommon.common_utils.bcast_utils import E_EXECUTE_MECHA_ACTION_SOUND
from math import pi
from logic.gcommon.time_utility import get_server_time
from logic.gutils.mecha_utils import do_hit_phantom
TWO_PI = pi * 2
DEATH_DOOR_MECHA_TAG_VALUE = register_unit_tag(('LDeathDoor', 'LMecha', 'LMechaRobot'))
BLOCK_TAG_VALUE = register_unit_tag(('LHouse', 'LField'))

@editor.state_exporter({('common_param', 'param'): {'zh_name': '\xe6\x99\xae\xe9\x80\x9a\xe5\x8f\x82\xe6\x95\xb0',
                               'param_type': 'dict','structure': {'hit_range': {'zh_name': '\xe5\x8a\x88\xe7\xa0\x8d\xe7\xa2\xb0\xe6\x92\x9e\xe4\xbd\x93\xe5\xae\xbd\xe9\xab\x98\xe9\x95\xbf','type': 'list','structure': [{'zh_name': '\xe6\x8c\xa5\xe7\xa0\x8d\xe5\xae\xbd\xe5\xba\xa6','type': 'float'}, {'zh_name': '\xe6\x8c\xa5\xe7\xa0\x8d\xe9\xab\x98\xe5\xba\xa6','type': 'float'}, {'zh_name': '\xe6\x8c\xa5\xe7\xa0\x8d\xe9\x95\xbf\xe5\xba\xa6\xef\xbc\x88\xe7\xba\xb5\xe6\xb7\xb1\xef\xbc\x89','type': 'float'}]},'slash_anim': {'zh_name': '\xe6\x8c\xa5\xe7\xa0\x8d\xe5\x8a\xa8\xe7\x94\xbb','type': 'list','structure': [{'zh_name': '\xe7\xac\xac\xe4\xb8\x80\xe5\x88\x80\xe5\x8a\xa8\xe7\x94\xbb','type': 'string'}, {'zh_name': '\xe7\xac\xac\xe4\xba\x8c\xe5\x88\x80\xe5\x8a\xa8\xe7\x94\xbb','type': 'string'}]},'combo_time': {'zh_name': '\xe8\xbf\x9e\xe5\x87\xbb\xe6\x97\xb6\xe9\x97\xb4','type': 'float'},'anim_duration': {'zh_name': '\xe6\x8c\xa5\xe7\xa0\x8d\xe5\x8a\xa8\xe7\x94\xbb\xe6\x97\xb6\xe9\x95\xbf','type': 'float'},'anim_rate': {'zh_name': '\xe6\x8c\xa5\xe7\xa0\x8d\xe5\x8a\xa8\xe7\x94\xbb\xe9\x80\x9f\xe7\x8e\x87','type': 'float'},'slash_end_anim': {'zh_name': '\xe7\xac\xac\xe4\xb8\x80\xe5\x88\x80\xe5\x90\x8e\xe6\x91\x87\xe5\x8a\xa8\xe7\x94\xbb','type': 'string'},'slash_end_anim_len': {'zh_name': '\xe7\xac\xac\xe4\xb8\x80\xe5\x88\x80\xe5\x90\x8e\xe6\x91\x87\xe5\x8a\xa8\xe7\x94\xbb\xe6\x97\xb6\xe9\x95\xbf','type': 'float'},'slash_sound': {'zh_name': '\xe9\x9f\xb3\xe6\x95\x88\xe5\x88\x97\xe8\xa1\xa8','type': 'list'},'play_sound_time': {'zh_name': '\xe9\x9f\xb3\xe6\x95\x88\xe6\x92\xad\xe6\x94\xbe\xe6\x97\xb6\xe9\x97\xb4','type': 'float'},'interrupt_time': {'zh_name': '\xe5\x8f\xaf\xe6\x89\x93\xe6\x96\xad\xe6\x97\xb6\xe9\x97\xb4','type': 'float'},'begin_attack_time': {'zh_name': '\xe5\xbc\x80\xe5\xa7\x8b\xe6\x8c\xa5\xe7\xa0\x8d\xe7\xa2\xb0\xe6\x92\x9e\xe6\x97\xb6\xe9\x97\xb4','type': 'float'},'end_attack_time': {'zh_name': '\xe7\xbb\x93\xe6\x9d\x9f\xe6\x8c\xa5\xe7\xa0\x8d\xe7\xa2\xb0\xe6\x92\x9e\xe6\x97\xb6\xe9\x97\xb4','type': 'float'},'begin_damage_time': {'zh_name': '\xe5\xbc\x80\xe5\xa7\x8b\xe7\xbb\x93\xe7\xae\x97\xe4\xbc\xa4\xe5\xae\xb3\xe6\x97\xb6\xe9\x97\xb4','type': 'float'},'end_damage_time': {'zh_name': '\xe7\xbb\x93\xe6\x9d\x9f\xe7\xbb\x93\xe7\xae\x97\xe4\xbc\xa4\xe5\xae\xb3\xe6\x97\xb6\xe9\x97\xb4','type': 'float'},'fire_energy_time': {'zh_name': '\xe5\x8f\x91\xe5\xb0\x84\xe5\x89\x91\xe6\xb0\x94\xe6\x97\xb6\xe9\x97\xb4','type': 'float'},'move_param': {'zh_name': '\xe5\x89\x8d\xe5\x86\xb2\xe5\x8f\x82\xe6\x95\xb0','type': 'dict','structure': {'begin_move_time': {'zh_name': '\xe5\xbc\x80\xe5\xa7\x8b\xe5\x89\x8d\xe5\x86\xb2\xe6\x97\xb6\xe9\x97\xb4','type': 'float'},'begin_brake_time': {'zh_name': '\xe5\xbc\x80\xe5\xa7\x8b\xe5\x87\x8f\xe9\x80\x9f\xe6\x97\xb6\xe9\x97\xb4','type': 'float'},'end_brake_time': {'zh_name': '\xe7\xbb\x93\xe6\x9d\x9f\xe7\xa7\xbb\xe5\x8a\xa8\xe6\x97\xb6\xe9\x97\xb4','type': 'float'},'velocity': {'zh_name': '\xe5\x89\x8d\xe5\x86\xb2\xe5\x88\x9d\xe9\x80\x9f\xe5\xba\xa6','type': 'float'}}},'move_param_air': {'zh_name': '\xe7\xa9\xba\xe4\xb8\xad\xe5\x89\x8d\xe5\x86\xb2\xe5\x8f\x82\xe6\x95\xb0','type': 'dict','structure': {'begin_move_time': {'zh_name': '\xe5\xbc\x80\xe5\xa7\x8b\xe5\x89\x8d\xe5\x86\xb2\xe6\x97\xb6\xe9\x97\xb4','type': 'float'},'begin_brake_time': {'zh_name': '\xe5\xbc\x80\xe5\xa7\x8b\xe5\x87\x8f\xe9\x80\x9f\xe6\x97\xb6\xe9\x97\xb4','type': 'float'},'end_brake_time': {'zh_name': '\xe7\xbb\x93\xe6\x9d\x9f\xe7\xa7\xbb\xe5\x8a\xa8\xe6\x97\xb6\xe9\x97\xb4','type': 'float'},'velocity': {'zh_name': '\xe5\x89\x8d\xe5\x86\xb2\xe5\x88\x9d\xe9\x80\x9f\xe5\xba\xa6','type': 'float'}}},'hit_stop': {'zh_name': '\xe5\x87\xbb\xe4\xb8\xad\xe7\x9b\xae\xe6\xa0\x87\xe6\x97\xb6\xe5\x81\x9c\xe6\xad\xa2\xe5\x89\x8d\xe5\x86\xb2','type': 'bool'}},'setter': lambda self, value, core=False: __editor_param_setter(self, value, core)
                               },
   ('core_param', 'param'): {'zh_name': '\xe6\xa0\xb8\xe5\xbf\x83\xe6\xa8\xa1\xe7\xbb\x84\xe5\x8f\x82\xe6\x95\xb0',
                             'param_type': 'dict','structure': {'hit_range': {'zh_name': '\xe5\x8a\x88\xe7\xa0\x8d\xe7\xa2\xb0\xe6\x92\x9e\xe4\xbd\x93\xe5\xae\xbd\xe9\xab\x98\xe9\x95\xbf','type': 'list','structure': [{'zh_name': '\xe6\x8c\xa5\xe7\xa0\x8d\xe5\xae\xbd\xe5\xba\xa6','type': 'float'}, {'zh_name': '\xe6\x8c\xa5\xe7\xa0\x8d\xe9\xab\x98\xe5\xba\xa6','type': 'float'}, {'zh_name': '\xe6\x8c\xa5\xe7\xa0\x8d\xe9\x95\xbf\xe5\xba\xa6\xef\xbc\x88\xe7\xba\xb5\xe6\xb7\xb1\xef\xbc\x89','type': 'float'}]},'slash_anim': {'zh_name': '\xe6\x8c\xa5\xe7\xa0\x8d\xe5\x8a\xa8\xe7\x94\xbb','type': 'list','structure': [{'zh_name': '\xe7\xac\xac\xe4\xb8\x80\xe5\x88\x80\xe5\x8a\xa8\xe7\x94\xbb','type': 'string'}, {'zh_name': '\xe7\xac\xac\xe4\xba\x8c\xe5\x88\x80\xe5\x8a\xa8\xe7\x94\xbb','type': 'string'}]},'combo_time': {'zh_name': '\xe8\xbf\x9e\xe5\x87\xbb\xe6\x97\xb6\xe9\x97\xb4','type': 'float'},'anim_duration': {'zh_name': '\xe6\x8c\xa5\xe7\xa0\x8d\xe5\x8a\xa8\xe7\x94\xbb\xe6\x97\xb6\xe9\x95\xbf','type': 'float'},'anim_rate': {'zh_name': '\xe6\x8c\xa5\xe7\xa0\x8d\xe5\x8a\xa8\xe7\x94\xbb\xe9\x80\x9f\xe7\x8e\x87','type': 'float'},'slash_end_anim': {'zh_name': '\xe7\xac\xac\xe4\xb8\x80\xe5\x88\x80\xe5\x90\x8e\xe6\x91\x87\xe5\x8a\xa8\xe7\x94\xbb','type': 'string'},'slash_end_anim_len': {'zh_name': '\xe7\xac\xac\xe4\xb8\x80\xe5\x88\x80\xe5\x90\x8e\xe6\x91\x87\xe5\x8a\xa8\xe7\x94\xbb\xe6\x97\xb6\xe9\x95\xbf','type': 'float'},'slash_sound': {'zh_name': '\xe9\x9f\xb3\xe6\x95\x88\xe5\x88\x97\xe8\xa1\xa8','type': 'list'},'play_sound_time': {'zh_name': '\xe9\x9f\xb3\xe6\x95\x88\xe6\x92\xad\xe6\x94\xbe\xe6\x97\xb6\xe9\x97\xb4','type': 'float'},'interrupt_time': {'zh_name': '\xe5\x8f\xaf\xe6\x89\x93\xe6\x96\xad\xe6\x97\xb6\xe9\x97\xb4','type': 'float'},'begin_attack_time': {'zh_name': '\xe5\xbc\x80\xe5\xa7\x8b\xe6\x8c\xa5\xe7\xa0\x8d\xe7\xa2\xb0\xe6\x92\x9e\xe6\x97\xb6\xe9\x97\xb4','type': 'float'},'end_attack_time': {'zh_name': '\xe7\xbb\x93\xe6\x9d\x9f\xe6\x8c\xa5\xe7\xa0\x8d\xe7\xa2\xb0\xe6\x92\x9e\xe6\x97\xb6\xe9\x97\xb4','type': 'float'},'begin_damage_time': {'zh_name': '\xe5\xbc\x80\xe5\xa7\x8b\xe7\xbb\x93\xe7\xae\x97\xe4\xbc\xa4\xe5\xae\xb3\xe6\x97\xb6\xe9\x97\xb4','type': 'float'},'end_damage_time': {'zh_name': '\xe7\xbb\x93\xe6\x9d\x9f\xe7\xbb\x93\xe7\xae\x97\xe4\xbc\xa4\xe5\xae\xb3\xe6\x97\xb6\xe9\x97\xb4','type': 'float'},'fire_energy_time': {'zh_name': '\xe5\x8f\x91\xe5\xb0\x84\xe5\x89\x91\xe6\xb0\x94\xe6\x97\xb6\xe9\x97\xb4','type': 'float'},'move_velocity': {'zh_name': '\xe7\xa7\xbb\xe5\x8a\xa8\xe9\x80\x9f\xe5\xba\xa6','type': 'float'},'move_velocity_air': {'zh_name': '\xe7\xa9\xba\xe4\xb8\xad\xe7\xa7\xbb\xe5\x8a\xa8\xe9\x80\x9f\xe5\xba\xa6','type': 'float'}},'setter': lambda self, value, core=True: __editor_param_setter(self, value, core)
                             },
   ('turn_speed', 'param'): {'zh_name': '\xe5\x90\x8e\xe6\x91\x87\xe8\xbd\xac\xe5\x90\x91\xe9\x80\x9f\xe5\xba\xa6','param_type': 'float'}})
class Slash8021(StateBase):
    SLASH_END = -1
    SLASH_ONE = 0
    SLASH_TWO = 1
    BIND_EVENT = {'E_ON_POST_JOIN_MECHA': 'on_post_join_mecha',
       'E_ENTER_STATE': 'enter_states',
       'E_ENTER_SLASHJUMP_HOLD': 'end_button_down',
       'E_BEGIN_AGENT_AI': 'begin_agent',
       'TRY_STOP_WEAPON_ATTACK': 'disable_self'
       }
    BIND_ATTR_CHANGE = {SEC_WEAPON_RANGE_FACTOR_8021: 'on_sec_weapon_range_factor_8021_change'
       }

    def read_data_from_custom_param(self):
        self.skill_id = self.custom_param.get('skill_id', 802151)
        self.hit_skill_id = self.skill_id
        self.fuel_skill_id = self.custom_param.get('fuel_skill_id', None)
        self.turn_speed = self.custom_param.get('turn_speed', 10.0)
        self.hold_anim = self.custom_param.get('hold_anim', 'dash_02')
        self.hold_move_anim = self.custom_param.get('hold_move_anim', 'dash_move')
        self.common_param = {'hit_range': [
                       8, 5, 4],
           'slash_anim': [
                        'vice_01', 'vice_02'],
           'slash_end_anim': 'vice_01_end',
           'slash_end_anim_len': 1.0,
           'slash_sound': [
                         [
                          'm_8021_weapon1_attack', 'nf'], ['m_8021_weapon1_attack', 'nf']],
           'anim_duration': 0.8,
           'anim_rate': 1.0,
           'play_sound_time': 0.0,
           'interrupt_time': 0.5,
           'begin_attack_time': 0.0,
           'end_attack_time': 0.5,
           'begin_damage_time': 0.0,
           'end_damage_time': 0.5,
           'fire_energy_time': 0.0,
           'move_param': {'begin_move_time': 0.1,
                          'begin_brake_time': 0.1,
                          'end_brake_time': 0.2,
                          'velocity': 10
                          },
           'move_param_air': {'begin_move_time': 0.1,
                              'begin_brake_time': 0.1,
                              'end_brake_time': 0.2,
                              'velocity': 10
                              },
           'hit_stop': True,
           'combo_time': 2
           }
        self.common_param.update(self.custom_param.get('common_param', {}))
        self.core_param = {'hit_range': [
                       8, 5, 4],
           'slash_anim': [
                        'vice_core_01', 'vice_core_02'],
           'slash_end_anim': 'vice_core_01_end',
           'slash_end_anim_len': 1.0,
           'slash_sound': [
                         [
                          'm_8021_weapon1_attack', 'nf'], ['m_8021_weapon1_attack', 'nf']],
           'anim_duration': 0.8,
           'anim_rate': 1.0,
           'play_sound_time': 0.0,
           'interrupt_time': 0.5,
           'begin_attack_time': 0.0,
           'end_attack_time': 0.5,
           'begin_damage_time': 0.0,
           'end_damage_time': 0.5,
           'fire_energy_time': 0.0,
           'gravity': -5.0,
           'move_velocity': 10,
           'move_velocity_air': 10,
           'combo_time': 2
           }
        self.core_param.update(self.custom_param.get('core_param', {}))
        self.hit_bone = self.custom_param.get('hit_bone', 'jian_bone_01')
        mecha_fashion_id = self.ev_g_mecha_fashion_id()
        if mecha_fashion_id in (201802151, ):
            self.hit_bone = []
        self.param_dict = self.common_param
        self.slash_count = len(self.param_dict['slash_anim'])
        return

    def _register_slash_callbacks(self):
        self.reset_sub_states_callback()
        for state_index, anim_name in enumerate(self.param_dict['slash_anim']):
            self._register_slash_state_callbacks(self.param_dict, state_index, anim_name, False)
            self._register_slash_state_callbacks(self.param_dict, state_index + self.slash_count, anim_name, True)

        self.register_substate_callback(self.SLASH_END, 0.0, lambda : self.send_event('E_POST_ACTION', self.param_dict['slash_end_anim'], LOW_BODY, 1))
        self.register_substate_callback(self.SLASH_END, self.param_dict['slash_end_anim_len'], self.end_slash)

    def _register_slash_state_callbacks(self, param, state_index, anim_name, air):
        self.register_substate_callback(state_index, 0.0, self.begin_slash, anim_name, param['anim_rate'])
        self.register_substate_callback(state_index, param['fire_energy_time'] / param['anim_rate'], self.fire_energy)
        self.register_substate_callback(state_index, param['anim_duration'] / param['anim_rate'], self.end_slash)
        self.register_substate_callback(state_index, param['play_sound_time'] / param['anim_rate'], self.play_slash_sound)
        self.register_substate_callback(state_index, param['interrupt_time'] / param['anim_rate'], self.interrupt)
        self.register_substate_callback(state_index, param['begin_attack_time'] / param['anim_rate'], self.begin_attack)
        self.register_substate_callback(state_index, param['end_attack_time'] / param['anim_rate'], self.end_attack)
        self.register_substate_callback(state_index, param['begin_damage_time'] / param['anim_rate'], self.begin_damage)
        self.register_substate_callback(state_index, param['end_damage_time'] / param['anim_rate'], self.end_damage)
        if self.cur_is_sp:
            self.register_substate_callback(state_index, 0.0, self.begin_move)
        else:
            move_param = param['move_param_air' if air else 'move_param']
            self.register_substate_callback(state_index, move_param['begin_move_time'] / param['anim_rate'], self.begin_move)
            if move_param['begin_brake_time'] < move_param['end_brake_time']:
                self.register_substate_callback(state_index, move_param['begin_brake_time'] / param['anim_rate'], self.begin_brake)
                self.register_substate_callback(state_index, move_param['end_brake_time'] / param['anim_rate'], self.end_brake)
            else:
                self.register_substate_callback(state_index, move_param['end_brake_time'] / param['anim_rate'], self.end_brake)

    def _reset_slash_hit_range(self):
        factor = self.ev_g_add_attr(SEC_WEAPON_RANGE_FACTOR_8021)
        range_factor = 1 + self.ev_g_add_attr(SEC_WEAPON_RANGE_FACTOR_8021)
        hit_width, hit_height, hit_depth = self.param_dict['hit_range']
        hit_width *= range_factor * NEOX_UNIT_SCALE
        hit_height *= range_factor * NEOX_UNIT_SCALE
        hit_depth *= range_factor * NEOX_UNIT_SCALE
        self.slash_checker.refresh_hit_range(hit_width, hit_height, hit_depth)

    def init_from_dict(self, unit_obj, bdict, sid, info):
        super(Slash8021, self).init_from_dict(unit_obj, bdict, sid, info)
        self.need_trigger_btn_up_when_action_forbidden = False
        self.is_attacking = False
        self.is_damaging = False
        self.sub_state = self.SLASH_END
        self.is_braking = False
        self.can_interrupt = False
        self.auto_combo = False
        self.btn_pressing = False
        self.is_sp = False
        self.cur_is_sp = False
        self.allow_refresh_is_sp = True
        self.ver_speed = 0
        self.interrupt_states = {MC_MOVE, MC_RUN, MC_JUMP_2, MC_JUMP_3, MC_DASH}
        self.interrupt_states_on_ground = {MC_SHOOT, MC_DRIVER_LEAVING, MC_JUMP_1}
        self.move_dir = None
        self.lock_yaw = False
        self.last_slash_end_time = -1
        self.read_data_from_custom_param()
        hit_width, hit_height, hit_depth = self.param_dict['hit_range']
        hit_width *= NEOX_UNIT_SCALE
        hit_height *= NEOX_UNIT_SCALE
        hit_depth *= NEOX_UNIT_SCALE
        self.slash_checker = SlashChecker(self, self.hit_skill_id, (hit_width, hit_height, hit_depth), self.hit_bone)
        self.enable_param_changed_by_buff()
        self._register_slash_callbacks()
        return

    def refresh_param_changed(self):
        if self.allow_refresh_is_sp:
            self.refresh_is_sp()

    def enter_states(self, state):
        if state in (MC_IMMOBILIZE, MC_DRIVER_LEAVING, MC_DEAD, MC_SUPER_JUMP, MC_BEAT_BACK, MC_FROZEN):
            self.end_button_down()

    def refresh_is_sp(self):
        if self.cur_is_sp == self.is_sp:
            return
        self.cur_is_sp = self.is_sp
        self.param_dict = self.core_param if self.cur_is_sp else self.common_param
        self.slash_count = len(self.param_dict['slash_anim'])
        self._register_slash_callbacks()
        self._reset_slash_hit_range()

    def destroy(self):
        self.end_button_down()
        if self.slash_checker:
            self.slash_checker.destroy()
            self.slash_checker = None
        super(Slash8021, self).destroy()
        return

    @property
    def move_param(self):
        return self.common_param['move_param' if self.sub_state < self.slash_count else 'move_param_air']

    @property
    def move_velocity(self):
        if self.cur_is_sp:
            return self.core_param['move_velocity' if self.sub_state < self.slash_count else 'move_velocity_air']
        else:
            return self.common_param['move_param' if self.sub_state < self.slash_count else 'move_param_air']['velocity']

    def try_next_slash(self):
        if self.sub_state != self.SLASH_END and not self.can_interrupt:
            return False
        self.sub_state = self.SLASH_END
        next_slash_state = self.sub_state + 1
        next_slash_state %= self.slash_count
        if next_slash_state == self.SLASH_ONE:
            cur_time = get_server_time()
            if cur_time - self.last_slash_end_time <= self.param_dict['combo_time']:
                next_slash_state += 1
        if not self.ev_g_on_ground():
            next_slash_state += self.slash_count
        self.refresh_is_sp()
        self.sub_state = next_slash_state
        self.send_event('E_CLEAR_WHITE_STATE', self.sid)
        self.active_self()
        self.is_attacking and self.end_attack()
        self.is_damaging and self.end_damage()
        self.send_event('E_CLEAR_SPEED')
        return True

    def begin_hold(self):
        self.send_event('E_ENTER_SLASH_HOLD')
        if self.ev_g_is_avatar():
            from logic.comsys.mecha_ui.MechaCancelUI import MechaCancelUI
            MechaCancelUI(None, self.end_button_down)
        self.send_event('E_REPLACE_ACTION_TRIGGER_ANIM', (MC_STAND,), self.hold_anim, loop=True)
        self.send_event('E_REPLACE_RUN_ANIM', 'dash_move')
        self.send_event('E_REPLACE_ACTION_TRIGGER_ANIM', (MC_MOVE,), self.hold_move_anim, part=LOW_BODY, blend_dir=8, loop=True)
        return

    def action_btn_down(self):
        if not self.check_can_active():
            return False
        if not self.check_can_cast_skill():
            return False
        self.btn_pressing = True
        if self.is_active and self.sub_state != self.SLASH_END:
            return False
        super(Slash8021, self).action_btn_down()
        self.begin_hold()
        return True

    def action_btn_up(self):
        if not (self.check_can_active() and self.check_can_cast_skill() and self.btn_pressing):
            return False
        self.btn_pressing = False
        if self.sub_state == self.SLASH_END or self.can_interrupt:
            self.end_button_down()
            return self.try_next_slash()
        return False

    def end_button_down(self, *args):
        self.btn_pressing = False
        if self.ev_g_is_avatar():
            global_data.ui_mgr.close_ui('MechaCancelUI')
        self.send_event('E_REPLACE_ACTION_TRIGGER_ANIM', (MC_STAND, MC_MOVE), None)
        self.send_event('E_REPLACE_RUN_ANIM', None)
        return

    def setup_fire_direction(self):
        scn = world.get_active_scene()
        camera = scn.active_camera
        if self.ev_g_is_agent():
            self.fire_forward = self.ev_g_forward()
            self.fire_position = self.ev_g_position()
        else:
            self.fire_forward = camera.rotation_matrix.forward
            self.fire_position = camera.position

    def enter(self, leave_states):
        self.is_attacking = False
        self.is_braking = False
        super(Slash8021, self).enter(leave_states)
        self.send_event('E_IGNORE_RELOAD_ANIM', True)
        self.send_event('E_RESET_ROTATION')
        self.send_event('E_VERTICAL_SPEED', 0)
        self.ver_speed = 0

    def begin_slash(self, anim_name, anim_rate):
        self.lock_yaw = True
        self.sync_cam_yaw_to_model()
        self.allow_refresh_is_sp = False
        self.send_event('E_ENABLE_CAMERA_ROTATE_SYNC_TO_MODEL', False)
        if self.ev_g_is_agent():
            move_dir = self.fire_forward = self.ev_g_forward()
            self.fire_position = self.ev_g_position()
        else:
            global_data.emgr.camera_leave_free_observe_event.emit()
            cam = global_data.game_mgr.scene.active_camera
            cam_dir = cam.rotation_matrix.forward
            move_dir = cam_dir
            self.fire_forward = move_dir
            self.fire_position = cam.position
        if not self.cur_is_sp:
            self.move_dir = move_dir
        self.send_event('E_DO_SKILL', self.hit_skill_id)
        if self.fuel_skill_id and not self.sd.ref_on_ground:
            self.send_event('E_DO_SKILL', self.fuel_skill_id)
        self.send_event('E_ANIM_RATE', LOW_BODY, anim_rate)
        self.send_event('E_POST_ACTION', anim_name, LOW_BODY, 1)
        if self.sd.ref_on_ground:
            self.send_event('E_RESET_GRAVITY')
        elif self.cur_is_sp:
            self.send_event('E_GRAVITY', self.param_dict['gravity'])
        else:
            self.send_event('E_GRAVITY', 0)
        self.can_interrupt = False

    def fire_energy(self):
        skill_obj = self.ev_g_skill(self.hit_skill_id)
        throw_item, stage = skill_obj.add_throwable(self.sub_state % self.slash_count, self.fire_position, self.fire_forward)
        self.send_event('E_CALL_SYNC_METHOD', 'skill_add_throwable', (self.hit_skill_id, (throw_item, stage)))

    def sync_cam_yaw_to_model(self, blend_time=0):
        if self.ev_g_is_agent():
            return
        cam_yaw = global_data.game_mgr.scene.active_camera.rotation_matrix.yaw
        if not blend_time:
            self.sd.ref_logic_trans.yaw_target = cam_yaw
        else:
            self.target_yaw = cam_yaw
            cur_yaw = self.sd.ref_logic_trans.yaw_target
            yaw_diff = cam_yaw - cur_yaw
            self.turn_speed = yaw_diff / blend_time

    def update_yaw(self, dt):
        if self.ev_g_is_agent():
            return
        if not self.can_interrupt or not self.turn_speed:
            return
        cam_yaw = global_data.game_mgr.scene.active_camera.rotation_matrix.yaw + TWO_PI
        cur_yaw = self.sd.ref_logic_trans.yaw_target
        if cam_yaw == cur_yaw:
            return
        yaw_diff = cam_yaw - cur_yaw
        if yaw_diff > pi:
            yaw_diff -= TWO_PI
        elif yaw_diff < -pi:
            yaw_diff += TWO_PI
        yaw_change = self.turn_speed * dt
        if abs(yaw_diff) <= abs(yaw_change):
            self.sd.ref_logic_trans.yaw_target = cam_yaw
        else:
            if yaw_diff < 0:
                yaw_change = -yaw_change
            self.sd.ref_logic_trans.yaw_target = cur_yaw + yaw_change

    def end_slash(self):
        self.allow_refresh_is_sp = True
        self.lock_yaw = False
        self.refresh_is_sp()
        self.send_event('E_ENABLE_CAMERA_ROTATE_SYNC_TO_MODEL', False)
        self.send_event('E_ADD_WHITE_STATE', self.interrupt_states, self.sid)
        if self.btn_pressing:
            self.begin_hold()
        elif self.ev_g_on_ground():
            self.send_event('E_ADD_WHITE_STATE', self.interrupt_states_on_ground, self.sid)
            if self.sd.ref_rocker_dir:
                self.send_event('E_ACTIVE_STATE', MC_MOVE)
            else:
                self.send_event('E_CLEAR_SPEED')
                if self.sub_state == self.SLASH_END:
                    self.send_event('E_ACTIVE_STATE', MC_STAND)
                else:
                    self.sub_state = self.SLASH_END
                    return
        else:
            self.send_event('E_ACTIVE_STATE', MC_JUMP_2)
        self.disable_self()

    def play_slash_sound(self):
        sound_name = self.param_dict['slash_sound'][self.sub_state % self.slash_count]
        self.send_event('E_EXECUTE_MECHA_ACTION_SOUND', 1, sound_name, 0, 0, 1, SOUND_TYPE_MECHA_FIRE)
        self.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', [
         E_EXECUTE_MECHA_ACTION_SOUND, (1, sound_name, 0, 0, 1, SOUND_TYPE_MECHA_FIRE)], True)

    def interrupt(self):
        self.can_interrupt = True
        self.send_event('E_ADD_WHITE_STATE', self.interrupt_states, self.sid)
        if self.ev_g_on_ground():
            self.send_event('E_ADD_WHITE_STATE', self.interrupt_states_on_ground, self.sid)
        self.last_slash_end_time = get_server_time()

    def begin_move(self):
        speed = self.move_velocity * NEOX_UNIT_SCALE
        self.sd.ref_cur_speed = speed

    def begin_brake(self):
        self.is_braking = True
        self.brake_acc = self.move_velocity / (self.move_param['end_brake_time'] - self.move_param['begin_brake_time'])

    def end_brake(self):
        self.is_braking = False
        self.send_event('E_CLEAR_SPEED')

    def begin_attack(self):
        self.is_attacking = True
        self.slash_checker.begin_check(self.param_dict.get('hit_stop', False))

    def end_attack(self):
        self.is_attacking = False
        self.slash_checker.end_check()

    def begin_damage(self):
        self.is_damaging = True
        self.slash_checker.set_damage_settlement_on(True)

    def end_damage(self):
        self.is_damaging = False
        self.slash_checker.set_damage_settlement_on(False)

    def update(self, dt):
        super(Slash8021, self).update(dt)
        self.update_yaw(dt)
        if self.sub_state == self.SLASH_END:
            if self.sd.ref_rocker_dir:
                self.disable_self()
                self.send_event('E_ACTIVE_STATE', MC_MOVE)
            return
        if self.cur_is_sp:
            rocker_dir = self.sd.ref_rocker_dir
            self.send_event('E_MOVE', rocker_dir)
            self.ver_speed -= dt * self.param_dict['gravity']
            self.send_event('E_VERTICAL_SPEED', self.ver_speed)
        elif self.move_dir:
            forward = vector(self.move_dir)
            speed = self.sd.ref_cur_speed
            if self.is_braking and not self.slash_checker.moving_stopped:
                speed -= self.brake_acc * dt
            self.send_event('E_VERTICAL_SPEED', forward.y * speed)
            self.boost_direction = vector(forward)
            if not self.slash_checker.moving_stopped:
                forward.y = 0
                self.send_event('E_SET_WALK_DIRECTION', forward * speed)
                self.sd.ref_cur_speed = speed

    def exit(self, enter_states):
        super(Slash8021, self).exit(enter_states)
        self.sync_cam_yaw_to_model()
        self.send_event('E_ANIM_RATE', LOW_BODY, 1.0)
        self.send_event('E_CLEAR_SPEED')
        self.is_attacking and self.end_attack()
        self.is_damaging and self.end_damage()
        self.sub_state >= self.slash_count and self.send_event('E_RESET_GRAVITY')
        self.send_event('E_RESET_STEP_HEIGHT')
        self.sub_state = self.SLASH_END
        if self.ev_g_immobilized():
            self.send_event('E_POST_ACTION', 'shake', LOW_BODY, 1)
        self.send_event('E_IGNORE_RELOAD_ANIM', False)
        self.send_event('E_ENABLE_CAMERA_ROTATE_SYNC_TO_MODEL', True)

    def on_post_join_mecha(self):
        if self.ev_g_is_avatar():
            self.send_event('E_BEGIN_RECOVER_MP', self.skill_id)

    def begin_agent(self, *_):
        self.send_event('E_BEGIN_RECOVER_MP', self.skill_id)

    def on_sec_weapon_range_factor_8021_change(self, attr, item_id, pre_value, cur_value, source_info):
        self._reset_slash_hit_range()


def __editor_param_setter(self, value, core):
    setattr(self, 'core_param' if core else 'common_param', value)
    if core == bool(self.cur_is_sp):
        self._reset_slash_hit_range()
        self._register_slash_callbacks()
        self.param_dict = self.core_param if core else self.common_param


@editor.state_exporter({('base_jump_height', 'meter'): {'zh_name': '\xe8\xb7\xb3\xe8\xb7\x83\xe9\xab\x98\xe5\xba\xa6'},('recover_time', 'param'): {'zh_name': '\xe8\x90\xbd\xe5\x9c\xb0\xe5\xa7\xbf\xe5\x8a\xbf\xe7\xbb\xb4\xe6\x8c\x81\xe6\x97\xb6\xe9\x97\xb4'},('break_time', 'param'): {'zh_name': '\xe8\x90\xbd\xe5\x9c\xb0\xe5\x90\x8e\xe5\x83\xb5\xe7\x9b\xb4\xe6\x97\xb6\xe9\x97\xb4','param_type': 'float','post_setter': lambda self: self._register_substate_callbacks()
                             },
   ('jump_gravity', 'meter'): {'zh_name': '\xe8\xb7\xb3\xe8\xb7\x83\xe6\x97\xb6\xe9\x87\x8d\xe5\x8a\x9b'},('max_jump_dist', 'meter'): {'zh_name': '\xe8\xb7\xb3\xe8\xb7\x83\xe6\x9c\x80\xe5\xa4\xa7\xe8\xb7\x9d\xe7\xa6\xbb'},('jump_anim_rate', 'param'): {'zh_name': '\xe8\xb5\xb7\xe8\xb7\xb3\xe5\x8a\xa8\xe7\x94\xbb\xe9\x80\x9f\xe5\xba\xa6','param_type': 'float','post_setter': lambda self: self._register_substate_callbacks()
                                 },
   ('fall_anim_rate', 'param'): {'zh_name': '\xe7\xa9\xba\xe4\xb8\xad\xe5\x8a\xa8\xe7\x94\xbb\xe9\x80\x9f\xe5\xba\xa6','param_type': 'float'},('on_ground_anim_rate', 'param'): {'zh_name': '\xe5\x8a\x88\xe6\x96\xa9\xe5\x8a\xa8\xe7\x94\xbb\xe9\x80\x9f\xe5\xba\xa6','param_type': 'float'},('sector_radius', 'meter'): {'zh_name': '\xe8\xbf\x91\xe8\xba\xab\xe4\xbc\xa4\xe5\xae\xb3\xe5\x8d\x8a\xe5\xbe\x84'},('sector_intern', 'param'): {'zh_name': '\xe8\xbf\x91\xe8\xba\xab\xe4\xbc\xa4\xe5\xae\xb3\xe7\xbb\x93\xe7\xae\x97\xe9\xa2\x91\xe7\x8e\x87\xef\xbc\x88\xe7\xa7\x92/\xe6\xac\xa1)'},('wave_length', 'meter'): {'zh_name': '\xe5\x9c\xb0\xe9\x9c\x87\xe6\xb3\xa2\xe9\x95\xbf\xe5\xba\xa6'},('wave_width', 'meter'): {'zh_name': '\xe5\x9c\xb0\xe9\x9c\x87\xe6\xb3\xa2\xe5\xae\xbd\xe5\xba\xa6'},('wave_height', 'meter'): {'zh_name': '\xe5\x9c\xb0\xe9\x9c\x87\xe6\xb3\xa2\xe9\xab\x98\xe5\xba\xa6'},('wave_step_height', 'meter'): {'zh_name': '\xe5\x9c\xb0\xe9\x9c\x87\xe6\xb3\xa2\xe7\x88\xac\xe5\x9d\xa1\xe9\xab\x98\xe5\xba\xa6'},('wave_sim_step', 'param'): {'zh_name': '\xe5\x9c\xb0\xe9\x9c\x87\xe6\xb3\xa2\xe6\xa8\xa1\xe6\x8b\x9f\xe6\xae\xb5\xe6\x95\xb0'},('wave_block_ray_count', 'param'): {'zh_name': '\xe5\xb0\x84\xe7\xba\xbf\xe6\x95\xb0\xe9\x87\x8f','param_type': 'int'},('wave_block_min_count', 'param'): {'zh_name': '\xe6\x9c\x80\xe4\xbd\x8e\xe9\x98\xbb\xe6\x8c\xa1\xe6\x95\xb0\xe9\x87\x8f','explain': '\xe8\x87\xb3\xe5\xb0\x91\xe6\x9c\x89\xe8\xbf\x99\xe4\xb9\x88\xe5\xa4\x9a\xe5\xb0\x84\xe7\xba\xbf\xe8\xa2\xab\xe9\x98\xbb\xe6\x8c\xa1\xe6\x97\xb6\xef\xbc\x8c\xe5\x9c\xb0\xe9\x9c\x87\xe6\xb3\xa2\xe5\x88\xa4\xe5\xae\x9a\xe4\xb8\xba\xe8\xa2\xab\xe9\x98\xbb\xe6\x8c\xa1','param_type': 'int'},('wave_block_ray_height', 'meter'): {'zh_name': '\xe5\xb0\x84\xe7\xba\xbf\xe7\xa6\xbb\xe5\x9c\xb0\xe9\xab\x98\xe5\xba\xa6','explain': '\xe5\x88\xa4\xe5\xae\x9a\xe9\x98\xbb\xe6\x8c\xa1\xe7\x9a\x84\xe5\xb0\x84\xe7\xba\xbf\xe7\x9a\x84\xe7\xa6\xbb\xe5\x9c\xb0\xe9\xab\x98\xe5\xba\xa6\xef\xbc\x88\xe7\xb1\xb3\xef\xbc\x89'},('wave_sfx_interval', 'param'): {'zh_name': '\xe5\x86\xb2\xe5\x87\xbb\xe6\xb3\xa2\xe7\x89\xb9\xe6\x95\x88\xe6\x98\xbe\xe7\xa4\xba\xe9\x97\xb4\xe9\x9a\x94','param_type': 'float','explain': '\xe5\x86\xb2\xe5\x87\xbb\xe6\xb3\xa2\xe6\xaf\x8f\xe6\xae\xb5\xe7\x89\xb9\xe6\x95\x88\xe5\x87\xba\xe7\x8e\xb0\xe4\xb9\x8b\xe9\x97\xb4\xe7\x9a\x84\xe9\x97\xb4\xe9\x9a\x94\xe6\x97\xb6\xe9\x97\xb4'},('wave_down_detect', 'meter'): {'zh_name': '\xe5\x9c\xb0\xe9\x9c\x87\xe6\xb3\xa2\xe8\xb5\xb7\xe5\xa7\x8b\xe4\xbd\x8d\xe7\xbd\xae\xe4\xb8\x8b\xe6\x8e\xa2\xe8\xb7\x9d\xe7\xa6\xbb'}})
class SlashJump8021(StateBase):
    JUMP_UP = 0
    JUMP_FALL = 1
    JUMP_GROUND = 2
    BIND_EVENT = {'E_SKILL_INIT_COMPLETE': ('on_skill_init_complete', 10),
       'E_UPDATE_SKILL_ATTR': ('on_skill_attr_update', 10),
       'E_IMMOBILIZED': 'end_button_down',
       'E_ON_FROZEN': 'end_button_down',
       'E_ENTER_STATE': 'enter_states',
       'E_ENTER_SLASH_HOLD': 'end_button_down'
       }

    def init_from_dict(self, unit_obj, bdict, sid, state_info):
        super(SlashJump8021, self).init_from_dict(unit_obj, bdict, sid, state_info)
        self.need_trigger_btn_up_when_action_forbidden = False
        self.skill_id = self.custom_param.get('skill_id', 802152)
        self.sector_skill_id = self.custom_param.get('sector_skill_id', 802154)
        self.wave_skill_id = self.custom_param.get('wave_skill_id', 802155)
        self.base_jump_height = self.custom_param.get('base_jump_height', 15) * NEOX_UNIT_SCALE
        self.recover_time = self.custom_param.get('recover_time', 1)
        self.jump_gravity = self.custom_param.get('jump_gravity', 100) * NEOX_UNIT_SCALE
        self.max_jump_dist = self.custom_param.get('max_dist', 70) * NEOX_UNIT_SCALE
        self.break_states = status_utils.convert_status(self.custom_param.get('break_states', {MC_MOVE, MC_SHOOT, MC_SECOND_WEAPON_ATTACK, MC_JUMP_1, MC_DASH}))
        self.break_time = self.custom_param.get('break_time', 0.5)
        self.onground_sfx_type = self.custom_param.get('onground_sfx_type', None)
        self.onground_sfx_time = self.custom_param.get('onground_sfx_time', (0.1, 0.2,
                                                                             0.3,
                                                                             0.4))
        self.sector_radius = self.custom_param.get('sector_radius', 5.0) * NEOX_UNIT_SCALE
        self.wave_length = self.custom_param.get('wave_length', 20.0) * NEOX_UNIT_SCALE
        self.wave_width = self.custom_param.get('wave_width', 5.0) * NEOX_UNIT_SCALE
        self.wave_height = self.custom_param.get('wave_height', 2.0) * NEOX_UNIT_SCALE
        self.wave_step_height = self.custom_param.get('wave_step_height', 4.0) * NEOX_UNIT_SCALE
        self.wave_sim_step = self.custom_param.get('wave_sim_step', 4)
        self.wave_block_ray_count = self.custom_param.get('wave_block_ray_count', 5)
        self.wave_block_min_count = self.custom_param.get('wave_block_min_count', 3)
        self.wave_block_ray_height = self.custom_param.get('wave_block_ray_height', 2) * NEOX_UNIT_SCALE
        self.wave_sfx_interval = self.custom_param.get('wave_sfx_interval', 0.2)
        self.wave_down_detect = self.custom_param.get('wave_down_detect', 3) * NEOX_UNIT_SCALE
        self.hold_anim = self.custom_param.get('hold_anim', 'dash_02')
        self.hold_move_anim = self.custom_param.get('hold_move_anim', 'dash_move')
        self.jump_anim = self.custom_param.get('hold_anim', 'dash_03')
        self.jump_anim_len = self.custom_param.get('jump_anim_len', 0.367)
        self.jump_anim_rate = self.custom_param.get('jump_anim_rate', 1.0) or 1.0
        self.jump_loop_anim = self.custom_param.get('fall_anim', 'dash_04')
        self.jump_loop_anim_rate = self.custom_param.get('fall_anim_rate', 1.0)
        self.fall_anim = self.custom_param.get('on_ground_anim', 'dash_05')
        self.fall_anim_rate = self.custom_param.get('on_ground_anim_rate', 1.0)
        self.on_ground_anim = self.custom_param.get('on_ground_anim', 'dash_06')
        self.on_ground_anim_rate = self.custom_param.get('on_ground_anim_rate', 1.0)
        self.on_ground_time = 0
        self.sub_state = -1
        self.vertical_speed = 0
        self.detecting = False
        self.target_pos = None
        self.sector_hitted_list = []
        self.hit_phantom = []
        self.sector_intern = self.custom_param.get('sector_intern', 1.0)
        self.sector_timer_is_on = False
        self.sector_timer = 0
        skill_obj = self.ev_g_skill(self.skill_id)
        if skill_obj:
            data = skill_obj._data or {}
            ext_info = data.get('ext_info', {})
            jump_distance_rate = ext_info.get('jump_distance_rate', 0)
            if jump_distance_rate > 1.0:
                self.max_jump_dist *= jump_distance_rate
            jump_height_rate = ext_info.get('jump_height_rate', 0)
            if jump_height_rate > 1.0:
                self.base_jump_height *= jump_height_rate
        self._register_substate_callbacks()
        return

    def _register_substate_callbacks(self):
        self.reset_sub_states_callback()
        self.register_substate_callback(self.JUMP_GROUND, self.break_time, lambda : self.send_event('E_ADD_WHITE_STATE', self.break_states, self.sid))
        self.register_substate_callback(self.JUMP_UP, self.jump_anim_len / self.jump_anim_rate, self.on_jump_anim_finish)

    def on_jump_anim_finish(self):
        self.send_event('E_ANIM_RATE', LOW_BODY, self.jump_loop_anim_rate)
        self.send_event('E_POST_ACTION', self.jump_loop_anim, LOW_BODY, 1)

    def enter_states(self, state):
        if state in (MC_IMMOBILIZE, MC_DRIVER_LEAVING, MC_DEAD, MC_SUPER_JUMP, MC_BEAT_BACK):
            self.end_button_down()

    def destroy(self):
        self.end_button_down()
        if self.detecting:
            detection_utils.stop_jump_pos_detect(self)
        self.unregist_event('E_FALL', self.on_fall)
        self.unregist_event('E_ON_TOUCH_GROUND', self.on_ground)
        super(SlashJump8021, self).destroy()

    def on_skill_init_complete(self):
        skill_obj = self.ev_g_skill(self.skill_id)
        if not skill_obj:
            return
        data = skill_obj._data
        self.max_jump_dist = self.custom_param.get('max_dist', 70) * NEOX_UNIT_SCALE * data.get('ext_info', {}).get('jump_distance_rate', 1)
        self.base_jump_height = self.custom_param.get('base_jump_height', 15) * NEOX_UNIT_SCALE * data.get('ext_info', {}).get('jump_height_rate', 1)

    def on_skill_attr_update(self, skill_id, *args):
        if skill_id == self.skill_id:
            skill_obj = self.ev_g_skill(self.skill_id)
            if not skill_obj:
                return
            data = skill_obj._data
            self.max_jump_dist = self.custom_param.get('max_dist', 70) * NEOX_UNIT_SCALE * data.get('ext_info', {}).get('jump_distance_rate', 1)
            self.base_jump_height = self.custom_param.get('base_jump_height', 15) * NEOX_UNIT_SCALE * data.get('ext_info', {}).get('jump_height_rate', 1)

    def action_btn_down(self):
        if not self.check_can_active():
            return False
        else:
            if not self.check_can_cast_skill():
                return False
            self.send_event('E_ENTER_SLASHJUMP_HOLD')
            if not self.detecting:
                if self.ev_g_is_avatar():
                    from logic.comsys.mecha_ui.MechaCancelUI import MechaCancelUI
                    MechaCancelUI(None, self.end_button_down, True)
                self.detecting = True
                detection_utils.start_jump_pos_detect(self, self.max_jump_dist, detect_callback=self.cal_jump_param)
                detection_utils.detect_jump_pos_wrapper()
                self.send_event('E_REPLACE_ACTION_TRIGGER_ANIM', (MC_STAND,), self.hold_anim, loop=True)
                self.send_event('E_REPLACE_RUN_ANIM', 'dash_move')
                self.send_event('E_REPLACE_ACTION_TRIGGER_ANIM', (MC_MOVE,), self.hold_move_anim, part=LOW_BODY, blend_dir=8, loop=True)
                if self.ev_g_is_avatar():
                    global_data.emgr.camera_leave_free_observe_event.emit()
            super(SlashJump8021, self).action_btn_down()
            return True

    def action_btn_up(self):
        if not self.detecting:
            return
        if self.ev_g_is_agent():
            self.target_pos = self.ev_g_rocket_jump_pos()
        else:
            self.target_pos = detection_utils.get_valid_jump_pos()
        if self.target_pos:
            self.active_self()
        self.end_button_down()
        super(SlashJump8021, self).action_btn_up()

    def enter(self, leave_states):
        super(SlashJump8021, self).enter(leave_states)
        self.send_event('E_IGNORE_RELOAD_ANIM', True)
        self.camp_id = self.ev_g_camp_id()
        if self.skill_id:
            self.send_event('E_DO_SKILL', self.skill_id)
        self.sub_state = self.JUMP_UP
        self.send_event('E_ANIM_RATE', LOW_BODY, self.jump_anim_rate)
        self.send_event('E_POST_ACTION', self.jump_anim, LOW_BODY, 1)
        if self.target_pos is not None:
            move_dir = self.cal_jump_param(self.target_pos, False)
        else:
            move_dir = math3d.vector(0, 0, 0)
        self.send_event('E_SET_WALK_DIRECTION', move_dir)
        self.send_event('E_GRAVITY', self.jump_gravity)
        self.send_event('E_JUMP', self.vertical_speed)
        self.send_event('E_JET_CAMERA_SHAKE')
        self.regist_event('E_FALL', self.on_fall)
        self.regist_event('E_ON_TOUCH_GROUND', self.on_ground)
        self.target_pos = None
        self.sector_hitted_list = []
        self.hit_phantom = []
        return

    def check_transitions(self):
        if self.sub_state == self.JUMP_GROUND:
            if self.elapsed_time - self.on_ground_time >= self.recover_time:
                self.disable_self()
                return MC_STAND
            rocker_dir = self.sd.ref_rocker_dir
            if rocker_dir and not rocker_dir.is_zero:
                return MC_MOVE

    def exit(self, enter_states):
        super(SlashJump8021, self).exit(enter_states)
        self.send_event('E_IGNORE_RELOAD_ANIM', False)
        self.send_event('E_CLEAR_WHITE_STATE', self.sid)
        self.skill_id and self.send_event('E_END_SKILL', self.skill_id)
        self.unregist_event('E_FALL', self.on_fall)
        self.unregist_event('E_ON_TOUCH_GROUND', self.on_ground)
        self.send_event('E_ANIM_RATE', LOW_BODY, 1.0)

    def on_fall(self, *args):
        if self.sub_state == self.JUMP_GROUND:
            return
        self.sub_state = self.JUMP_FALL
        self.unregist_event('E_FALL', self.on_fall)
        self.send_event('E_ANIM_RATE', LOW_BODY, self.fall_anim_rate)
        self.send_event('E_POST_ACTION', self.fall_anim, LOW_BODY, 1)
        sound_name = ('m_8021_hack_emit', 'nf')
        self.send_event('E_EXECUTE_MECHA_ACTION_SOUND', 1, sound_name, 0, 0, 1, SOUND_TYPE_MECHA_FIRE)
        self.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', [
         E_EXECUTE_MECHA_ACTION_SOUND, (1, sound_name, 0, 0, 1, SOUND_TYPE_MECHA_FIRE)], True)
        self.start_sector_timer()

    def on_ground(self, *args):
        if self.sub_state != self.JUMP_FALL:
            self.unregist_event('E_FALL', self.on_fall)
        self.send_event('E_JET_CAMERA_SHAKE')
        self.send_event('E_ANIM_RATE', LOW_BODY, self.on_ground_anim_rate)
        self.send_event('E_POST_ACTION', self.on_ground_anim, LOW_BODY, 1, blend_time=0)
        sound_name = ('m_8021_hack_touchground', 'nf')
        self.send_event('E_EXECUTE_MECHA_ACTION_SOUND', 1, sound_name, 0, 0, 1, SOUND_TYPE_MECHA_FIRE)
        self.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', [
         E_EXECUTE_MECHA_ACTION_SOUND, (1, sound_name, 0, 0, 1, SOUND_TYPE_MECHA_FIRE)], True)
        self.sub_state = self.JUMP_GROUND
        self.send_event('E_CLEAR_SPEED')
        self.on_ground_time = self.elapsed_time
        self.sound_drive.run_end()
        sector_targets = self.do_sector_skill(True)
        self.sector_timer_is_on = False
        if self.do_wave_skill() and sector_targets:
            start_pos = self.ev_g_position()
            self.send_event('E_DO_SKILL', self.wave_skill_id, sector_targets, (start_pos.x, start_pos.y, start_pos.z))

    def start_sector_timer(self):
        self.do_sector_skill()
        self.sector_timer = 0
        self.sector_timer_is_on = True

    def update(self, dt):
        super(SlashJump8021, self).update(dt)
        if self.sector_timer_is_on:
            self.sector_timer += dt
            if self.sector_timer >= self.sector_intern:
                self.do_sector_skill()
                self.sector_timer -= self.sector_intern

    def do_sector_skill(self, on_ground=False):
        from logic.gcommon.skill.client.SkillSector import SkillSector
        start_pos = self.ev_g_position()
        direction = self.ev_g_forward()
        scn = world.get_active_scene()
        col = col_object(SPHERE, vector(self.sector_radius, 0, 0), GROUP_DYNAMIC_SHOOTUNIT, GROUP_DYNAMIC_SHOOTUNIT)
        col.position = start_pos
        ret = scn.scene_col.static_test(col, -1, GROUP_DYNAMIC_SHOOTUNIT, INCLUDE_FILTER) or []
        target_ids = {}
        hit_cid = self.ev_g_human_base_col_id()
        relative_ids = self.sd.ref_mecha_relative_cols
        self_cids = [col.cid, hit_cid]
        if relative_ids:
            self_cids.extend(relative_ids)
        break_conf = confmgr.get('break_data', str(self.sector_skill_id), default={})
        impulse_power = break_conf.get('cBreakPower', 0)
        for hit_col in ret:
            if hit_col.cid in self_cids:
                continue
            if global_data.emgr.scene_is_shoot_obj.emit(hit_col.cid):
                res = global_data.emgr.scene_find_unit_event.emit(hit_col.cid)
                if res and res[0] and res[0].__class__.__name__ == 'LHouse':
                    pass
                continue
            if res and res[0] and hit_col.cid in global_data.phantoms:
                if res[0] not in self.hit_phantom:
                    self.hit_phantom.append(res[0])
                    do_hit_phantom(self, res[0])
                continue
            if res and res[0] and res[0] != global_data.player.logic:
                eid = res[0].id
                if eid not in target_ids and eid not in self.sector_hitted_list:
                    if self.ev_g_is_agent():
                        lcheck = self.unit_obj if 1 else global_data.mecha.logic
                        valid, dist = SkillSector.check_valid(eid, start_pos, direction, scn, lcheck, False)
                        if valid:
                            target_ids[eid] = dist
                            self.sector_hitted_list.append(eid)
                    if res[0].__class__.__name__ == 'LField':
                        break
                    trigger_show_outline(res[0], self.unit_obj.id)
            if impulse_power > 0:
                is_ragdoll_part = hit_col.__class__.__name__ == 'rigid_body'
                break_item_info = [
                 {'model_col_name': hit_col.model_col_name,
                    'point': hit_col.position,
                    'normal': hit_col.position - col.position,
                    'power': impulse_power,
                    'break_type': BREAK_TRIGGER_TYPE_WEAPON
                    }]
                if is_ragdoll_part:
                    global_data.emgr.scene_handle_break_ragdoll_part.emit(break_item_info)
                else:
                    global_data.emgr.scene_add_break_objs.emit(break_item_info, True)

        if target_ids:
            self.send_event('E_DO_SKILL', self.sector_skill_id, target_ids, (start_pos.x, start_pos.y, start_pos.z))
        return target_ids

    def do_wave_skill(self):
        hit_target_dict = {}
        scene_col = global_data.game_mgr.scene.scene_col
        hit_by_ray = scene_col.hit_by_ray
        if not callable(hit_by_ray):
            return
        else:
            model = self.ev_g_model()
            if not model or not model.valid:
                return
            col_node_list = []
            step_len = self.wave_length / self.wave_sim_step
            step_vec = self.ev_g_forward()
            step_vec.normalize(step_len)
            first_step = vector(step_vec)
            first_step.normalize(step_len / 2.0)
            start_pos = self.ev_g_position()
            hit_ret = hit_by_ray(start_pos, start_pos - math3d.vector(0, self.wave_down_detect, 0), 0, GROUP_CAMERA_COLL, GROUP_CAMERA_COLL, INCLUDE_FILTER, False)
            if hit_ret[0]:
                start_pos = hit_ret[1]
            start_pos += first_step
            end_pos = vector(start_pos)
            last_node_y = start_pos.y
            for i in range(self.wave_sim_step + 1):
                start_pos.y = last_node_y + self.wave_step_height
                end_pos.y = last_node_y - self.wave_step_height
                hit_ret = hit_by_ray(start_pos, end_pos, 0, GROUP_CAMERA_COLL, GROUP_CAMERA_COLL, INCLUDE_FILTER, True)
                if hit_ret[0]:
                    node_pos = None
                    for point, _, _, _, obj in hit_ret[1]:
                        res = global_data.emgr.scene_find_unit_event.emit(obj.cid)
                        if res and res[0] and res[0].MASK & DEATH_DOOR_MECHA_TAG_VALUE:
                            continue
                        if node_pos is None or point.y > node_pos.y:
                            node_pos = point

                    if node_pos is None:
                        break
                    last_node_y = node_pos.y
                    col_node_list.append(node_pos + vector(0, self.wave_height / 2, 0))
                else:
                    if col_node_list:
                        col_node_list.append(col_node_list[-1] + step_vec)
                    break
                start_pos += step_vec
                end_pos += step_vec

            if not col_node_list:
                return True
            my_pos = self.ev_g_position()
            col_len = step_len + NEOX_UNIT_SCALE
            col_size = vector(self.wave_width, self.wave_height, col_len)
            node_pos_rot_list = []
            world_up = vector(0, 1, 0)
            ray_height_vec = vector(0, self.wave_block_ray_height, 0)
            block_group = GROUP_CAMERA_COLL
            for i in range(len(col_node_list) - 1):
                node_pos = col_node_list[i]
                next_node_pos = col_node_list[i + 1]
                node_forward = next_node_pos - node_pos
                right = node_forward.cross(world_up)
                right_offset = vector(right)
                right_offset.normalize(self.wave_width / 2.0)
                left = -right_offset
                left.normalize(self.wave_width / (self.wave_block_ray_count - 1))
                ray_begin = node_pos + ray_height_vec
                ray_end = next_node_pos + ray_height_vec
                block_count = 0
                col_len_frac = 0
                for ray_idx in range(self.wave_block_ray_count):
                    hit, _, _, frac, _, obj = hit_by_ray(ray_begin + right_offset, ray_end + right_offset, 0, block_group, block_group, INCLUDE_FILTER, False)
                    if hit and global_data.emgr.scene_is_shoot_obj.emit(obj.cid)[0]:
                        res = global_data.emgr.scene_find_unit_event.emit(obj.cid)
                        if res and res[0] and res[0].__class__.__name__ == 'LMecha':
                            hit = False
                    if hit:
                        block_count += 1
                        if frac > col_len_frac:
                            col_len_frac = frac
                    else:
                        col_len_frac = 1
                    right_offset += left

                if col_len_frac <= 0:
                    break
                col_size.z = node_forward.length + NEOX_UNIT_SCALE
                col = col_object(BOX, col_size, GROUP_DYNAMIC_SHOOTUNIT, GROUP_DYNAMIC_SHOOTUNIT)
                node_normal = right.cross(node_forward)
                if node_normal.y < 0:
                    node_normal = -node_normal
                node_forward.normalize(col_len * col_len_frac * 0.5)
                col.position = node_pos + node_forward
                col.rotation_matrix = matrix.make_orient(node_forward, node_normal)
                ret = scene_col.static_test(col, -1, GROUP_DYNAMIC_SHOOTUNIT, INCLUDE_FILTER) or []
                hit_thing = False
                for hit_col in ret:
                    if not global_data.emgr.scene_is_shoot_obj.emit(hit_col.cid)[0]:
                        continue
                    res = global_data.emgr.scene_find_unit_event.emit(hit_col.cid)
                    if res and res[0] and res[0].MASK & BLOCK_TAG_VALUE:
                        continue
                    if res and res[0] and hit_col.cid in global_data.phantoms:
                        if res[0] not in self.hit_phantom:
                            self.hit_phantom.append(res[0])
                            do_hit_phantom(self, res[0])
                        continue
                    unit_obj = res[0]
                    if not unit_obj:
                        continue
                    eid = unit_obj.id
                    if unit_obj.ev_g_is_campmate(self.camp_id):
                        continue
                    target_pos = unit_obj.ev_g_position()
                    if not target_pos:
                        continue
                    if block_count:
                        hit, _, _, _, _, obj = hit_by_ray(ray_begin, target_pos + ray_height_vec, 0, block_group, block_group, INCLUDE_FILTER, False)
                        if hit and global_data.emgr.scene_is_shoot_obj.emit(obj.cid)[0]:
                            res = global_data.emgr.scene_find_unit_event.emit(obj.cid)
                            if res and res[0] and res[0].__class__.__name__ == 'LMecha':
                                hit = False
                        if hit:
                            continue
                    dist = abs(target_pos - my_pos)
                    hit_target_dict[eid] = dist
                    hit_thing = True

                if block_count == 0 or hit_thing:
                    node_pos_rot_list.append((col.position - vector(0, self.wave_height / 2, 0), col.rotation_matrix))
                if block_count >= self.wave_block_min_count:
                    break

            if hit_target_dict:
                start_pos = self.ev_g_position()
                self.send_event('E_DO_SKILL', self.wave_skill_id, hit_target_dict, (start_pos.x, start_pos.y, start_pos.z))
            if node_pos_rot_list:
                self.send_event('E_8021_SHOW_SHOCKWAVE', node_pos_rot_list)
            return

    def cal_jump_param(self, target_pos, show_track=True):
        end_pos = target_pos
        start_pos = self.ev_g_position()
        delta_dir = end_pos - start_pos
        h = self.base_jump_height / self.sd.ref_gravity_scale
        delta_s = vector(delta_dir.x, 0, delta_dir.z).length
        delta_h = abs(delta_dir.y)
        h_up = delta_h + h if delta_dir.y > 0 else h
        real_gravity = self.jump_gravity * self.sd.ref_gravity_scale
        t_up = math.sqrt(2 * h_up / real_gravity)
        h_fall = delta_h + h if delta_dir.y < 0 else h
        t_fall = math.sqrt(2 * h_fall / real_gravity)
        self.vertical_speed = abs(t_up * real_gravity)
        self.horizon_speed = delta_s / (t_up + t_fall)
        forward = end_pos - start_pos
        forward.y = 0
        if forward.is_zero:
            forward = vector(0, 0, 1)
        else:
            forward.normalize()
        move_dir = forward * self.horizon_speed
        if show_track:
            self.send_event('E_SHOW_JUMP_TRACK', 'effect/fx/niudan/tishitexiao_jiantou.sfx', start_pos, vector(move_dir.x, self.vertical_speed, move_dir.z), -real_gravity, target_pos)
        return move_dir

    def end_button_down(self, *args):
        if not self.detecting:
            return
        else:
            if self.ev_g_is_avatar():
                global_data.ui_mgr.close_ui('MechaCancelUI')
            self.send_event('E_REPLACE_ACTION_TRIGGER_ANIM', (MC_STAND, MC_MOVE), None)
            self.send_event('E_REPLACE_RUN_ANIM', None)
            self.send_event('E_SLOW_DOWN', False)
            self.detecting = False
            detection_utils.stop_jump_pos_detect(self)
            self.send_event('E_HIDE_JUMP_TRACK')
            self.send_event('E_ACTION_UP', self.bind_action_id)
            return


from logic.gcommon.behavior.MoveLogic import Run
from .StateBase import clamp
import time

@editor.state_exporter({('stop_anim_cost_time', 'param'): {'zh_name': '\xe6\x92\xad\xe6\x94\xbe\xe5\x90\x8e\xe6\x91\x87\xe5\x8a\xa8\xe4\xbd\x9c\xe6\x9c\x80\xe5\xb0\x91\xe8\xb7\x91\xe6\xad\xa5\xe6\x97\xb6\xe9\x97\xb4'}})
class Run8021(Run):

    def read_data_from_custom_param(self):
        super(Run8021, self).read_data_from_custom_param()
        self.stop_anim_cost_time = self.custom_param.get('stop_anim_cost_time', 3.0)

    def init_from_dict(self, unit_obj, bdict, sid, state_info):
        self.exit_run_time_stamp = time.time() - 999.0
        self.enter_state_running_time_stamp = self.exit_run_time_stamp
        super(Run8021, self).init_from_dict(unit_obj, bdict, sid, state_info)

    def update(self, dt):
        StateBase.update(self, dt)
        rocker_dir = self.sd.ref_rocker_dir
        rocker_stop = not rocker_dir or rocker_dir.is_zero
        can_run = self.sd.ref_can_run
        if self.show_stop_anim and rocker_stop and self.sub_state != self.STATE_STOP:
            self.sub_state = self.STATE_STOP
        if self.sub_state == self.STATE_STOP:
            rocker_dir = None
        if self.last_rocker_dir != rocker_dir:
            self.last_rocker_dir = rocker_dir
            self.send_event('E_ACTION_MOVE')
        cur_speed = self.sd.ref_cur_speed
        speed_scale = self.ev_g_get_speed_scale() or 1
        max_speed = speed_scale * self.run_speed
        acc = rocker_dir and not rocker_dir.is_zero
        cur_speed += dt * (self.move_acc if acc and can_run else self.brake_acc)
        cur_speed = clamp(cur_speed, 0, max_speed)
        self.sd.ref_cur_speed = cur_speed
        self.send_event('E_MOVE', rocker_dir)
        if self.enable_dynamic_speed_rate:
            self.send_event('E_ANIM_RATE', LOW_BODY, cur_speed / self.run_speed * self.dynamic_speed_rate)
        return

    def begin_run_anim(self):
        super(Run8021, self).begin_run_anim()
        self.enter_state_running_time_stamp = time.time()

    def begin_run_stop_anim(self):
        self.sound_drive.run_end()
        if time.time() - self.enter_state_running_time_stamp < self.stop_anim_cost_time:
            self.end_run_stop_anim()
            return
        super(Run8021, self).begin_run_stop_anim()


from logic.gcommon.behavior.ShootLogic import WeaponFire

class WeaponFire8021(WeaponFire):

    def init_from_dict(self, unit_obj, bdict, sid, state_info):
        super(WeaponFire8021, self).init_from_dict(unit_obj, bdict, sid, state_info)
        self.forbid_ik = True