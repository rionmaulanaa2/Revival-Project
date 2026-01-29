# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/behavior/Logic8006.py
from __future__ import absolute_import
from .ShootLogic import AccumulateShoot
from .JumpLogic import JumpUp, MAX_JUMP_STAGE, JumpUpPure, FallPure, SuperJumpUpPure
from .StateBase import StateBase
from .MountLogic import Mount
from logic.gutils.character_ctrl_utils import AirHorizontalOffsetSpeedSetter
from logic.gcommon.cdata.mecha_status_config import *
from logic.gcommon.const import NEOX_UNIT_SCALE
from logic.gcommon import editor
from copy import deepcopy
MECHA_8006_SS = 201800653

class AccumulateShoot8006(AccumulateShoot):

    def read_data_from_custom_param(self):
        super(AccumulateShoot8006, self).read_data_from_custom_param()
        self.hide_submesh = self.custom_param.get('hide_submesh', None)
        if self.hide_submesh:
            hide_submesh_state = self.hide_submesh.get('state', 0)
            hide_submesh_time = self.hide_submesh.get('time', 0)
            self.hide_submesh_list = self.hide_submesh.get('submesh', None)
            if self.ev_g_mecha_fashion_id() == MECHA_8006_SS:
                self.hide_submesh_list = deepcopy(self.hide_submesh_list)
                special_sub_mesh_list = []
                for sub_mesh_name in self.hide_submesh_list:
                    special_sub_mesh_list.append(sub_mesh_name + '1')

                self.hide_submesh_list.extend(special_sub_mesh_list)

            def hide_submesh_callback():
                self.send_event('E_HIDE_SUB_MESH', self.hide_submesh_list)

            self.register_substate_callback(hide_submesh_state, hide_submesh_time, hide_submesh_callback)
        return


class RecoverSecondWeapon(StateBase):
    BIND_EVENT = {'E_FORCE_RECOVER_BIRD': 'on_force_recover_bird'
       }

    def init_from_dict(self, unit_obj, bdict, sid, state_info):
        super(RecoverSecondWeapon, self).init_from_dict(unit_obj, bdict, sid, state_info)
        self.anim_time = self.custom_param.get('anim_duration', 1)

    def enter(self, leave_states):
        super(RecoverSecondWeapon, self).enter(leave_states)
        bone_tree = (('biped root', 0), ('biped l clavicle', 1))
        self.send_event('E_POST_EXTERN_ACTION', 'bird_04', True, subtree=bone_tree)

    def on_force_recover_bird(self):
        show_submesh = self.custom_param.get('show_submesh', None)
        if show_submesh:
            if self.ev_g_mecha_fashion_id() == MECHA_8006_SS:
                new_submesh_list = deepcopy(show_submesh)
                for sub_mesh_name in show_submesh:
                    new_submesh_list.append(sub_mesh_name + '1')

                show_submesh = new_submesh_list
            self.send_event('E_SHOW_SUB_MESH', show_submesh)
        return

    def check_transitions(self):
        if self.elapsed_time > self.anim_time:
            self.disable_self()

    def exit(self, enter_states):
        super(RecoverSecondWeapon, self).exit(enter_states)
        self.send_event('E_POST_EXTERN_ACTION', None, False)
        return


@editor.state_exporter({('can_try_glide_in_advance_time', 'param'): {'zh_name': '\xe5\x85\x81\xe8\xae\xb8\xe9\xa2\x84\xe5\xad\x98\xe6\xbb\x91\xe7\xbf\x94\xe6\x93\x8d\xe4\xbd\x9c\xe6\x97\xb6\xe9\x97\xb4\xe7\x82\xb9'}})
class JumpUp8006(JumpUpPure):

    def read_data_from_custom_param(self):
        super(JumpUp8006, self).read_data_from_custom_param()
        self.can_try_glide_in_advance_time = self.custom_param.get('can_try_glide_in_advance', 0.2)

    def init_from_dict(self, unit_obj, bdict, sid, info):
        super(JumpUp8006, self).init_from_dict(unit_obj, bdict, sid, info)
        self.sd.ref_need_glide_in_advance = False

    def _action_btn_down(self):
        if self.is_active:
            if self.sd.ref_cur_jump_count < self.cur_max_continual_jump_count:
                self._do_jump()
            elif self.elapsed_time >= self.can_try_glide_in_advance_time:
                self.sd.ref_need_glide_in_advance = True
            return True
        if not self.check_can_cast_skill():
            return False
        if not self.check_can_active():
            if self.cur_max_continual_jump_count > 1:
                if self.sd.ref_cur_jump_count == 0:
                    jump_count_when_enter = 1
                else:
                    jump_count_when_enter = self.sd.ref_cur_jump_count
                if jump_count_when_enter < self.cur_max_continual_jump_count:
                    if self.ev_g_enable_jump_in_air(self.sid):
                        self.jump_count_when_enter = jump_count_when_enter
                        self.active_self()
                        return True
            return False
        if self.cur_max_continual_jump_count > 1:
            if self.sd.ref_cur_jump_count == 0:
                if not self.ev_g_on_ground() and not self.sd.ref_in_coyote_time:
                    jump_count_when_enter = 1
                else:
                    jump_count_when_enter = 0
            else:
                jump_count_when_enter = self.sd.ref_cur_jump_count
        else:
            jump_count_when_enter = 0
        if jump_count_when_enter < self.cur_max_continual_jump_count:
            self.jump_count_when_enter = jump_count_when_enter
            self.active_self()
            return True
        return False

    def action_btn_down(self):
        ret = self._action_btn_down()
        if ret:
            return True
        cur_states = self.ev_g_cur_state()
        if MC_JUMP_2 in cur_states:
            return self.ev_g_try_enter_glide()
        if MC_GLIDE in cur_states:
            return self.ev_g_try_leave_glide()
        if MC_SUPER_JUMP in cur_states:
            if self.ev_g_try_glide_in_advance_in_super_jump_up():
                self.sd.ref_need_glide_in_advance = True
                return True
        return False

    def enter(self, leave_states):
        super(JumpUp8006, self).enter(leave_states)
        self.sd.ref_need_glide_in_advance = False

    def exit(self, enter_states):
        super(JumpUp8006, self).exit(enter_states)
        self.sd.ref_need_glide_in_advance = False


class Fall8006(FallPure):

    def on_fall(self, *args):
        if self.sd.ref_need_glide_in_advance:
            self.sd.ref_need_glide_in_advance = False
            if self.ev_g_try_enter_glide():
                return
        if not self.check_can_active():
            return
        self.active_self()


@editor.state_exporter({('max_glide_duration', 'param'): {'zh_name': '\xe6\xbb\x91\xe7\xbf\x94\xe6\x9c\x80\xe5\xa4\xa7\xe6\x8c\x81\xe7\xbb\xad\xe6\x97\xb6\xe9\x97\xb4'},('glide_vertical_speed', 'meter'): {'zh_name': '\xe6\xbb\x91\xe7\xbf\x94\xe4\xb8\x8b\xe8\x90\xbd\xe9\x80\x9f\xe5\xba\xa6'},('h_speed_ratio', 'param'): {'zh_name': '\xe6\xb0\xb4\xe5\xb9\xb3\xe5\x81\x8f\xe7\xa7\xbb\xe9\x80\x9f\xe5\xba\xa6\xe7\xbb\xa7\xe6\x89\xbf\xe7\x8e\x87'},('h_offset_speed', 'meter'): {'zh_name': '\xe6\xb0\xb4\xe5\xb9\xb3\xe5\x81\x8f\xe7\xa7\xbb\xe6\x9c\x80\xe5\xa4\xa7\xe9\x80\x9f\xe5\xba\xa6'},('h_offset_acc', 'meter'): {'zh_name': '\xe6\xb0\xb4\xe5\xb9\xb3\xe5\x81\x8f\xe7\xa7\xbb\xe5\x8a\xa0\xe9\x80\x9f\xe5\xba\xa6'},('h_offset_dec', 'meter'): {'zh_name': '\xe6\xb0\xb4\xe5\xb9\xb3\xe5\x81\x8f\xe7\xa7\xbb\xe5\x87\x8f\xe9\x80\x9f\xe5\xba\xa6'},('max_h_offset_dec_duration', 'param'): {'zh_name': '\xe5\x87\x8f\xe9\x80\x9f\xe5\x88\xb0\xe6\xb0\xb4\xe5\xb9\xb3\xe5\x81\x8f\xe7\xa7\xbb\xe6\x9c\x80\xe5\xa4\xa7\xe9\x80\x9f\xe5\xba\xa6\xe7\x9a\x84\xe6\x9c\x80\xe5\xa4\xa7\xe6\x97\xb6\xe9\x97\xb4'}})
class Glide(StateBase):
    BIND_EVENT = {'G_TRY_ENTER_GLIDE': 'on_try_enter_glide',
       'G_TRY_LEAVE_GLIDE': 'on_try_leave_glide',
       'E_FUEL_EXHAUSTED': 'on_fuel_exhausted',
       'E_ADD_GLIDE_TIME': 'on_modify_glide_duration_add_scale'
       }

    def read_data_from_custom_param(self):
        self.skill_id = self.custom_param.get('skill_id', 800654)
        self.max_glide_duration = self.custom_param.get('max_glide_duration', 2.0)
        self.glide_vertical_speed = self.custom_param.get('glide_vertical_speed', -10) * NEOX_UNIT_SCALE

    def init_from_dict(self, unit_obj, bdict, sid, info):
        super(Glide, self).init_from_dict(unit_obj, bdict, sid, info)
        self.read_data_from_custom_param()
        self.air_horizontal_offset_speed_setter = AirHorizontalOffsetSpeedSetter(self)
        self.need_leave_glide = False
        self.check_on_ground_interval = 0.3
        self.check_on_ground_flag = 0
        self.glide_duration_add_scale = 0
        self.cur_max_glide_duration = self.max_glide_duration
        self.h_offset_speed_factor = 0
        self.enable_param_changed_by_buff()

    def refresh_param_changed(self):
        initial_h_offset_speed = self.custom_param.get('h_offset_speed', 10) * NEOX_UNIT_SCALE
        self.h_offset_speed = initial_h_offset_speed * (1.0 + self.h_offset_speed_factor)

    def enter(self, leave_states):
        super(Glide, self).enter(leave_states)
        if not self.check_can_cast_skill() or self.ev_g_on_ground():
            self.need_leave_glide = True
            return
        self.air_horizontal_offset_speed_setter.reset()
        self.check_on_ground_flag = 0
        self.send_event('E_DO_SKILL', self.skill_id)
        self.send_event('E_GRAVITY', 0)
        self.send_event('E_VERTICAL_SPEED', self.glide_vertical_speed)
        self.send_event('E_SET_ACTION_SELECTED', 'action5', True)
        self.send_event('E_REFRESH_SPREAD_AIM_UI')

    def update(self, dt):
        super(Glide, self).update(dt)
        self.air_horizontal_offset_speed_setter.execute(dt)
        self.check_on_ground_flag += dt
        if self.check_on_ground_flag >= self.check_on_ground_interval:
            if self.ev_g_on_ground():
                self.send_event('E_LOGIC_ON_GROUND', -self.ev_g_vertical_speed())
            self.check_on_ground_flag = 0

    def check_transitions(self):
        if self.need_leave_glide or self.elapsed_time > self.cur_max_glide_duration:
            if self.ev_g_on_ground():
                if self.sd.ref_rocker_dir and not self.sd.ref_rocker_dir.is_zero:
                    new_state = MC_MOVE
                else:
                    new_state = MC_STAND
            else:
                new_state = MC_JUMP_2
            self.send_event('E_ADD_WHITE_STATE', {new_state}, self.sid)
            return new_state

    def exit(self, enter_states):
        super(Glide, self).exit(enter_states)
        self.need_leave_glide = False
        self.send_event('E_END_SKILL', self.skill_id)
        self.send_event('E_RESET_GRAVITY')
        self.send_event('E_SET_ACTION_SELECTED', 'action5', False)
        self.send_event('E_REFRESH_SPREAD_AIM_UI')

    def refresh_action_param(self, action_param, custom_param):
        super(Glide, self).refresh_action_param(action_param, custom_param)
        self.custom_param = custom_param
        self.read_data_from_custom_param()
        self.air_horizontal_offset_speed_setter.initialize()
        self.refresh_param_changed()
        self.on_modify_glide_duration_add_scale(0)

    def refresh_sound_param(self, sound_param, *args, **kwargs):
        super(Glide, self).refresh_sound_param(sound_param, need_restart_when_active=False)

    def on_try_enter_glide(self):
        if self.is_active:
            return True
        if self.ev_g_on_ground():
            return True
        if not self.check_can_active():
            return False
        if not self.check_can_cast_skill():
            return False
        self.active_self()
        return True

    def on_try_leave_glide(self):
        if not self.is_active:
            return True
        self.need_leave_glide = True
        return True

    def on_fuel_exhausted(self):
        if self.is_active:
            self.need_leave_glide = True

    def on_modify_glide_duration_add_scale(self, scale):
        self.glide_duration_add_scale += scale
        self.cur_max_glide_duration = self.max_glide_duration * (1.0 + self.glide_duration_add_scale)


@editor.state_exporter({('can_try_glide_in_advance_time', 'param'): {'zh_name': '\xe5\x85\x81\xe8\xae\xb8\xe9\xa2\x84\xe5\xad\x98\xe6\xbb\x91\xe7\xbf\x94\xe6\x93\x8d\xe4\xbd\x9c\xe6\x97\xb6\xe9\x97\xb4\xe7\x82\xb9'}})
class SuperJumpUp8006(SuperJumpUpPure):
    BIND_EVENT = SuperJumpUpPure.BIND_EVENT.copy()
    BIND_EVENT.update({'G_TRY_GLIDE_IN_ADVANCE_IN_SUPER_JUMP_UP': 'on_try_glide_in_advance'
       })

    def read_data_from_custom_param(self):
        super(SuperJumpUp8006, self).read_data_from_custom_param()
        self.can_try_glide_in_advance_time = self.custom_param.get('can_try_glide_in_advance', 0.3)

    def on_try_glide_in_advance(self):
        if self.is_active and self.elapsed_time > self.can_try_glide_in_advance_time:
            return True
        return False


class DashBuff(StateBase):
    SUB_ST_NONE = 0
    SUB_ST_START = 1
    SUB_ST_IDLE = 2
    SUB_ST_END = 3
    BIND_EVENT = {'E_START_ALL_AROUND_SPEED_BUFF': 'buff_start',
       'E_STOP_ALL_AROUND_SPEED_BUFF': 'buff_stop'
       }

    def init_from_dict(self, unit_obj, bdict, sid, info):
        super(DashBuff, self).init_from_dict(unit_obj, bdict, sid, info)
        self.tick_interval = self.custom_param.get('tick_interval', 0.2)
        self.skill_id = self.custom_param.get('skill_id', 80590)
        tail_start = self.custom_param.get('tail_start', None)
        self.tail_start_anim = tail_start[0]
        self.tail_start_time = tail_start[1]
        tail_idle = self.custom_param.get('tail_idle', None)
        self.tail_idle_anim = tail_idle[0]
        tail_end = self.custom_param.get('tail_end', None)
        self.tail_end_anim = tail_end[0]
        self.tail_end_time = tail_end[1]
        self.tail_bone_tree = self.custom_param.get('tail_bone_tree', None)
        self.buff_left_time = 0
        self.dashing = False
        self.to_idle_delay_info = None

        def start_callback():
            self.sub_state = self.SUB_ST_IDLE
            self.send_event('E_POST_EXTERN_ACTION', self.tail_idle_anim, True, level=2, subtree=self.tail_bone_tree, loop=True)

        self.register_substate_callback(self.SUB_ST_START, self.tail_start_time, start_callback)

        def end_callback():
            self.send_event('E_POST_EXTERN_ACTION', None, False, level=2)
            self.disable_self()
            return

        self.register_substate_callback(self.SUB_ST_END, self.tail_end_time, end_callback)
        return

    def enter(self, leave_states):
        super(DashBuff, self).enter(leave_states)
        self.sub_state = self.SUB_ST_NONE
        self.send_event('E_DO_SKILL', self.skill_id)

    def action_btn_down(self):
        if self.is_active:
            return False
        if not self.check_can_active():
            return False
        if not self.ev_g_can_cast_skill(self.skill_id):
            return False
        self.active_self()

    def buff_start(self, buff_id, data, left_time):
        if left_time < 0:
            self.buff_stop()
            return
        if self.is_active or not self.is_active and self.check_can_active():
            if self.dashing:
                self.buff_left_time = left_time
                real_idle_time = (self.buff_left_time or 0) - self.tail_end_time
                if real_idle_time <= 0:
                    self.idle_to_end()
                else:
                    self.to_idle_delay_info and self.cancel_delay_call(self.to_idle_delay_info)
                    self.to_idle_delay_info = self.delay_call(real_idle_time, self.idle_to_end)
                if not self.is_active:
                    self.active_self()
            else:
                self.dashing = True
                self.send_event('E_SET_ACTION_VISIBLE', self.bind_action_id, False)
                self.send_event('E_REFRESH_STATE_PARAM')
                self.buff_left_time = left_time
                self.sub_state = self.SUB_ST_START
                self.send_event('E_POST_EXTERN_ACTION', self.tail_start_anim, True, level=2, subtree=self.tail_bone_tree, loop=False)
                real_idle_time = (self.buff_left_time or 0) - self.tail_end_time
                if real_idle_time <= 0:
                    self.idle_to_end()
                else:
                    self.to_idle_delay_info = self.delay_call(real_idle_time, self.idle_to_end)
                if not self.is_active:
                    self.active_self()

    def buff_stop(self):
        if self.dashing:
            self.send_event('E_SET_ACTION_VISIBLE', self.bind_action_id, True)
            self.send_event('E_RESET_STATE_PARAM')
            self.send_event('E_POST_EXTERN_ACTION', None, False, level=2)
            self.dashing = False
            self.to_idle_delay_info = None
        self.disable_self()
        return

    def idle_to_end(self):
        self.sub_state = self.SUB_ST_END
        self.send_event('E_POST_EXTERN_ACTION', self.tail_end_anim, True, level=2, subtree=self.tail_bone_tree, loop=False)

    def update(self, dt):
        super(DashBuff, self).update(dt)
        partcam = global_data.game_mgr.scene.get_com('PartCamera')
        if partcam:
            camera_state = partcam.get_cur_camera_state_type()
            if self._cur_camera and self._cur_camera != camera_state:
                self.enter_camera(self._cur_camera)

    def exit(self, enter_states):
        super(DashBuff, self).exit(enter_states)
        if self.dashing:
            self.send_event('E_SET_ACTION_VISIBLE', self.bind_action_id, True)
            self.send_event('E_RESET_STATE_PARAM')
            self.send_event('E_POST_EXTERN_ACTION', None, False, level=2)
            self.dashing = False
        return


@editor.state_exporter({('anim_duration', 'param'): {'zh_name': '\xe5\x8a\xa8\xe7\x94\xbb\xe6\x97\xb6\xe9\x95\xbf','min_val': 1,'max_val': 4},('mount_duration', 'param'): {'zh_name': '\xe4\xb8\x8a\xe6\x9c\xba\xe7\x94\xb2\xe6\x97\xb6\xe9\x97\xb4','min_val': 1,'max_val': 4},('break_time', 'param'): {'zh_name': '\xe4\xb8\x8a\xe6\x9c\xba\xe7\x94\xb2\xe6\x89\x93\xe6\x96\xad\xe7\x82\xb9','min_val': 1,'max_val': 4}})
class Mount8006(Mount):

    def init_from_dict(self, unit_obj, bdict, sid, state_info):
        super(Mount8006, self).init_from_dict(unit_obj, bdict, sid, state_info)
        self.hide_submesh_time = None
        self.had_hided_submesh = False
        self.hide_submesh = self.custom_param.get('hide_submesh', None)
        if self.hide_submesh:
            self.hide_submesh_time = self.hide_submesh.get('time', 0)
            self.hide_submesh_list = self.hide_submesh.get('submesh', None)
            if self.ev_g_mecha_fashion_id() == MECHA_8006_SS:
                self.hide_submesh_list = deepcopy(self.hide_submesh_list)
                special_sub_mesh_list = []
                for sub_mesh_name in self.hide_submesh_list:
                    special_sub_mesh_list.append(sub_mesh_name + '1')

                self.hide_submesh_list.extend(special_sub_mesh_list)
        self.show_submesh_time = None
        self.had_showed_submesh = False
        self.show_submesh = self.custom_param.get('show_submesh', None)
        if self.show_submesh:
            self.show_submesh_time = self.show_submesh.get('time', 0)
            self.show_submesh_list = self.show_submesh.get('submesh', None)
            if self.ev_g_mecha_fashion_id() == MECHA_8006_SS:
                self.show_submesh_list = deepcopy(self.show_submesh_list)
                special_sub_mesh_list = []
                for sub_mesh_name in self.show_submesh_list:
                    special_sub_mesh_list.append(sub_mesh_name + '1')

                self.show_submesh_list.extend(special_sub_mesh_list)
        return

    def update(self, dt):
        super(Mount8006, self).update(dt)
        if self.hide_submesh_time is not None and self.elapsed_time > self.hide_submesh_time and not self.had_hided_submesh:
            self.had_hided_submesh = True
            self.send_event('E_HIDE_SUB_MESH', self.hide_submesh_list, False)
        if self.show_submesh_time is not None and self.elapsed_time > self.show_submesh_time and not self.had_showed_submesh:
            self.had_showed_submesh = True
            self.send_event('E_SHOW_SUB_MESH', self.show_submesh_list, False)
        return

    def exit(self, enter_states):
        super(Mount8006, self).exit(enter_states)
        if not self.had_showed_submesh and self.show_submesh_time is not None:
            self.send_event('E_SHOW_SUB_MESH', self.show_submesh_list, False)
        return