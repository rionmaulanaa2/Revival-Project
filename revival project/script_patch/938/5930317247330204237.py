# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/behavior/EditorCustomLogic.py
from .StateBase import StateBase
from logic.gcommon.cdata.mecha_status_config import *
from logic.gcommon.common_const.character_anim_const import *
from logic.gutils.character_ctrl_utils import get_forward_by_rocker_and_camera, AirWalkDirectionSetter
from logic.gcommon import editor
import math3d

@editor.state_exporter({('stage_count', 'param'): {'zh_name': '\xe9\x98\xb6\xe6\xae\xb5\xe6\x95\xb0\xe9\x87\x8f','post_setter': lambda self: self._update_stage_parameters(from_editor=True)
                              },
   ('stage_orders', 'param'): {'zh_name': '\xe9\x98\xb6\xe6\xae\xb5\xe6\x89\xa7\xe8\xa1\x8c\xe9\xa1\xba\xe5\xba\x8f','explain': '\xe4\xb8\x8d\xe5\xa1\xab\xe5\xb0\xb1\xe6\x8c\x89\xe7\x85\xa7\xe5\xa1\xab\xe5\x86\x99\xe9\xa1\xba\xe5\xba\x8f\xef\xbc\x8c\xe5\xa6\x82\xe6\x9e\x9c\xe5\xa1\xab\xe7\x9a\x84\xe8\xaf\x9d\xef\xbc\x8c\xe7\xbc\x96\xe5\x8f\xb7\xe8\xa6\x81\xe4\xbb\x8e0\xe5\xbc\x80\xe5\xa7\x8b','post_setter': lambda self: self._register_callbacks()
                               },
   ('stage_parameters', 'param'): {'zh_name': '\xe9\x98\xb6\xe6\xae\xb5\xe5\x8f\x82\xe6\x95\xb0','post_setter': lambda self: self._register_callbacks(),
                                   'structure': lambda self: self._get_stage_param_structure()}
   })
class CustomDisplacement(StateBase):
    BIND_EVENT = {}

    def read_data_from_custom_param(self):
        self.skill_id = self.custom_param.get('skill_id', None)
        self.stage_count = self.custom_param.get('stage_count', 1)
        self.stage_parameters = self.custom_param.get('stage_parameters', [])
        self._update_stage_parameters()
        print '=============================update value'
        self.stage_orders = self.custom_param.get('stage_orders', [])
        self.sub_state_to_stage_index_map = {}
        self._register_callbacks()
        return

    def delay_refresh_editor_appearance(self):
        self.re_export()
        if global_data.mecha_behavior_editor:
            global_data.mecha_behavior_editor.load_data()
        self.delay_refresh_editor_appearance_timer = None
        return

    def _update_stage_parameters(self, from_editor=False):
        cur_param_count = len(self.stage_parameters)
        for i in range(0, self.stage_count - cur_param_count):
            self.stage_parameters.append({})

        for i in range(0, cur_param_count - self.stage_count):
            self.stage_parameters.pop()

        if from_editor:
            if not self.delay_refresh_editor_appearance_timer:
                self.delay_refresh_editor_appearance_timer = global_data.game_mgr.register_logic_timer(self.delay_refresh_editor_appearance, interval=1, times=1)

    def _get_stage_param_structure(self):
        stage_param_structure = []
        for i in range(self.stage_count):
            sub_structure = dict()
            sub_structure['anim_name'] = {'zh_name': '\xe5\x8a\xa8\xe4\xbd\x9c\xe5\x90\x8d','type': 'string'}
            sub_structure['anim_part'] = {'zh_name': '\xe5\x8a\xa8\xe4\xbd\x9c\xe6\x92\xad\xe6\x94\xbe\xe9\x83\xa8\xe4\xbd\x8d','type': 'string'}
            sub_structure['anim_dir_type'] = {'zh_name': '\xe5\x8a\xa8\xe4\xbd\x9c\xe6\x92\xad\xe6\x94\xbe\xe6\x96\xb9\xe5\x90\x91\xe7\xb1\xbb\xe5\x9e\x8b','type': 'int'}
            sub_structure['anim_loop'] = {'zh_name': '\xe5\x8a\xa8\xe4\xbd\x9c\xe6\x98\xaf\xe5\x90\xa6\xe5\xbe\xaa\xe7\x8e\xaf','type': 'bool'}
            sub_structure['anim_rate'] = {'zh_name': '\xe5\x8a\xa8\xe4\xbd\x9c\xe6\x92\xad\xe6\x94\xbe\xe9\x80\x9f\xe7\x8e\x87','type': 'float'}
            sub_structure['gravity'] = {'zh_name': '\xe9\x87\x8d\xe5\x8a\x9b','explain': '-1\xe4\xb8\xba\xe6\x81\xa2\xe5\xa4\x8d\xe9\xbb\x98\xe8\xae\xa4\xe9\x87\x8d\xe5\x8a\x9b','type': 'int'}
            sub_structure['is_continual_displacement'] = {'zh_name': '\xe6\x98\xaf\xe5\x90\xa6\xe6\x8c\x81\xe7\xbb\xad\xe4\xbd\x8d\xe7\xa7\xbb\xe9\x80\xbb\xe8\xbe\x91','type': 'bool'}
            sub_structure['directly_move'] = {'zh_name': '\xe5\x85\xb3\xe9\x97\xad\xe7\x89\xb9\xe6\xae\x8a\xe4\xbd\x8d\xe7\xa7\xbb\xe9\x80\xbb\xe8\xbe\x91','type': 'bool'}
            sub_structure['jump_speed'] = {'zh_name': '\xe8\xb7\xb3\xe8\xb7\x83\xe9\x80\x9f\xe5\xba\xa6','type': 'float'}
            sub_structure['move_speed'] = {'zh_name': '\xe7\xa7\xbb\xe5\x8a\xa8\xe9\x80\x9f\xe5\xba\xa6','type': 'float'}
            sub_structure['force_rocker_dir'] = {'zh_name': '\xe5\xbc\xba\xe5\x88\xb6\xe6\x91\x87\xe6\x9d\x86\xe6\x96\xb9\xe5\x90\x91','type': 'string'}
            sub_structure['move_without_y'] = {'zh_name': '\xe5\xbf\xbd\xe7\x95\xa5y\xe6\x96\xb9\xe5\x90\x91\xe4\xbd\x8d\xe7\xa7\xbb','type': 'bool'}
            sub_structure['stop_y_speed'] = {'zh_name': '\xe5\x81\x9c\xe6\xad\xa2y\xe6\x96\xb9\xe5\x90\x91\xe4\xbd\x8d\xe7\xa7\xbb','type': 'bool'}
            sub_structure['stop_horizontal_speed'] = {'zh_name': '\xe5\x81\x9c\xe6\xad\xa2\xe6\xb0\xb4\xe5\xb9\xb3\xe6\x96\xb9\xe5\x90\x91\xe4\xbd\x8d\xe7\xa7\xbb','type': 'bool'}
            stage_param_structure.append({'zh_name': '\xe9\x98\xb6\xe6\xae\xb5%d' % i,'type': 'dict','kwargs': {'structure': sub_structure}})

        return stage_param_structure

    def _register_callbacks(self):
        self.reset_sub_states_callback()
        for order_index, stage_index in enumerate(self.stage_orders if self.stage_orders else [ i for i in range(self.stage_count) ]):
            self.sub_state_to_stage_index_map[order_index] = stage_index
            self.register_substate_callback(order_index, 0, self.execute_sub_state_callback)

    def init_from_dict(self, unit_obj, bdict, sid, info):
        super(CustomDisplacement, self).init_from_dict(unit_obj, bdict, sid, info)
        self.read_data_from_custom_param()
        self.gravity_changed = False
        self.is_continual_displacement = False
        self.cur_stage_param = {}
        self.air_walk_direction_setter = AirWalkDirectionSetter(self)
        self.delay_refresh_editor_appearance_timer = None
        return

    def destroy(self):
        if self.air_walk_direction_setter:
            self.air_walk_direction_setter.destroy()
            self.air_walk_direction_setter = None
        super(CustomDisplacement, self).destroy()
        return

    def action_btn_down(self):
        if self.is_active:
            return True
        if not self.check_can_active():
            return False
        if not self.check_can_cast_skill():
            return False
        self.active_self()
        return True

    def enter(self, leave_states):
        super(CustomDisplacement, self).enter(leave_states)
        self.send_event('E_DO_SKILL', self.skill_id)

    def _execute_displacement(self, stage_param):
        if stage_param.get('jump_speed') is not None:
            self.send_event('E_JUMP', stage_param['jump_speed'])
        if stage_param.get('move_speed') is not None:
            move_speed = stage_param['move_speed']
            if 'force_rocker_dir' in stage_param:
                if stage_param['force_rocker_dir'] == 'f':
                    rocker_dir = math3d.vector(0, 0, 1)
                else:
                    rocker_dir = math3d.vector(0, 0, -1)
            else:
                rocker_dir = self.sd.ref_rocker_dir
                if not rocker_dir or rocker_dir.is_zero:
                    rocker_dir = math3d.vector(0, 0, 1)
            forward = self.sd.ref_effective_camera_rot.rotate_vector(rocker_dir)
            if stage_param.get('move_without_y', True):
                forward.y = 0
                forward.normalize()
            walk_direction = forward * move_speed
            if stage_param.get('directly_move', False):
                self.send_event('E_VERTICAL_SPEED', walk_direction.y)
                walk_direction.y = 0
                self.send_event('E_SET_WALK_DIRECTION', walk_direction)
            else:
                self.air_walk_direction_setter.execute(walk_direction)
        if stage_param.get('stop_y_speed'):
            self.send_event('E_VERTICAL_SPEED', 0)
        if stage_param.get('stop_horizontal_speed'):
            self.send_event('E_CLEAR_SPEED')
        return

    def execute_sub_state_callback(self):
        stage_param = self.stage_parameters[self.sub_state_to_stage_index_map[self.sub_state]]
        if stage_param.get('anim_name') is not None:
            part = stage_param.get('anim_part', LOW_BODY)
            if part == 'up':
                part = UP_BODY if 1 else LOW_BODY
                self.send_event('E_ANIM_RATE', part, stage_param.get('anim_rate', 1.0))
                dir_type = stage_param.get('anim_dir_type', 1)
                loop = stage_param.get('anim_loop', False)
                self.send_event('E_POST_ACTION', stage_param['anim_name'], part, dir_type, loop=loop)
            if stage_param.get('gravity') is not None:
                if stage_param['gravity'] == -1:
                    self.send_event('E_RESET_GRAVITY')
                else:
                    self.send_event('E_GRAVITY', stage_param['gravity'])
            self.is_continual_displacement = False
            if stage_param.get('is_continual_displacement', False):
                self.is_continual_displacement = True
                self.cur_stage_param = stage_param
                stage_param.get('directly_move', False) or self.air_walk_direction_setter.reset()
        else:
            self.is_continual_displacement = False
            self._execute_displacement(stage_param)
        return

    def process_nest_sub_state(self):
        self.sub_state += 1
        if self.sub_state == self.stage_count:
            self.disable_self()

    def update(self, dt):
        super(CustomDisplacement, self).update(dt)
        if self.is_continual_displacement:
            self._execute_displacement(self.cur_stage_param)

    def check_transitions(self):
        pass

    def exit(self, enter_states):
        super(CustomDisplacement, self).exit(enter_states)
        if self.gravity_changed:
            self.send_event('E_RESET_GRAVITY')
        self.send_event('E_END_SKILL', self.skill_id)
        self.send_event('E_BEGIN_RECOVER_MP', self.skill_id)