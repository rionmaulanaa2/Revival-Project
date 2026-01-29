# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/behavior/TransformLogic.py
from __future__ import absolute_import
import six
from .StateBase import StateBase, clamp
from logic.gcommon.cdata.mecha_status_config import *
from mobile.common.EntityManager import EntityManager
from logic.gcommon.common_const import animation_const
import world
import math3d
import logic.gcommon.common_utils.bcast_utils as bcast
from logic.gcommon.common_utils import status_utils
from logic.gcommon import editor
DEFAULT_SUB_STATE = 0

@editor.state_exporter({('break_time', 'param'): {'zh_name': '\xe5\x8f\x98\xe8\xba\xab\xe6\x8f\x90\xe5\x89\x8d\xe6\x89\x93\xe6\x96\xad\xe6\x97\xb6\xe9\x97\xb4'}})
class Transform(StateBase):
    BIND_EVENT = {'E_ANIMATOR_LOADED': ('on_update_anim_param', 10),
       'E_RESET_CAMERA_STATE': 'reset_camera_state'
       }

    def init_from_dict(self, unit_obj, bdict, sid, state_info):
        super(Transform, self).init_from_dict(unit_obj, bdict, sid, state_info)
        self.transforming = False
        self.npc_id = bdict.get('npc_id', 8001)
        self.timer_rate = self.custom_param.get('timer_rate', 1)
        self.transform_id = self.custom_param['trans_id']
        self.anim_time = self.custom_param.get('anim_time', 2)
        self.twist_y_bone = self.custom_param.get('twist_y_bone', ('biped spine', 'biped head'))
        self.twist_x_bone = self.custom_param.get('twist_x_bone', ('biped spine', 'biped head'))
        self.upbody_bone = self.custom_param.get('upbody_bone', 'biped spine')
        self.camera_state = self.custom_param.get('camera_state', None)
        self.default_states = self.custom_param.get('default_states', None)
        self.break_time = self.custom_param.get('break_time', None)
        self.break_states = status_utils.convert_status(self.custom_param.get('break_states', set()))
        self.register_substate()
        return

    def register_substate(self):
        if self.break_time:
            self.register_substate_callback(DEFAULT_SUB_STATE, self.break_time, self.add_break_state)
        else:
            self.reset_sub_states_callback()

    def on_init_complete(self):
        super(Transform, self).on_init_complete()
        shapeshift = self.ev_g_shape_shift()
        if shapeshift:
            action_switch = self.custom_param.get('action_switch', {})
            for action, state_id in six.iteritems(action_switch):
                self.send_event('E_SWITCH_ACTION', action, state_id)

    def on_update_anim_param(self, *args):
        self.send_event('E_TWIST_YAW_PARAM', self.twist_y_bone[0], self.twist_y_bone[1])
        self.send_event('E_TWIST_PITCH_PARAM', self.twist_x_bone[0], self.twist_x_bone[1])
        subtree = (('biped root', 0), (self.upbody_bone, 1))
        self.send_event('E_UPBODY_BONE', subtree)

    def action_btn_down(self):
        if not self.check_can_active():
            return False
        if self.transforming:
            return False
        self.transforming = True
        shapeshift = 'trans' if self.transform_id.find('trans') > 0 else ''
        self.send_event('E_CALL_SYNC_METHOD', 'mecha_shapeshift', (shapeshift,), True)
        self.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', [bcast.E_SWITCH_BEHAVIOR, (self.transform_id, self.sid)], True)
        cur_yaw, cur_pitch = self.ev_g_yaw() or 0, self.ev_g_cam_pitch() or 0
        self.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', [bcast.S_ATTR_SET, ('human_yaw', cur_yaw)], True)
        self.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', [bcast.S_ATTR_SET, ('head_pitch', cur_pitch)], True)
        self.send_event('S_ATTR_SET', 'human_yaw', cur_yaw)
        self.send_event('S_ATTR_SET', 'head_pitch', cur_pitch)
        if self.unit_obj.__class__.__name__ != 'LMechaTrans':
            self.send_event('E_CLEAR_SPEED')
        self.send_event('E_RESET_ROTATION', 0)
        self.send_event('E_SWITCH_BEHAVIOR', self.transform_id, self.sid, True)
        return True

    def enter(self, leave_states):
        self.sub_state = DEFAULT_SUB_STATE
        self.transforming = True
        self.on_update_anim_param()
        self.handle_transform()
        self.reset_camera_state()
        shapeshift = '' if self.transform_id.find('trans') > 0 else 'trans'
        self.send_event('E_SHAPESHIFT', shapeshift)
        self.send_event('E_ACTION_YAW', 0)
        self.send_event('E_ACTION_PITCH', 0)
        self.send_event('E_CLEAR_UP_BODY_ANIM')
        self.sync_timer_rate_to_anim(True)
        super(Transform, self).enter(leave_states)

    def add_break_state(self, *args):
        self.send_event('E_ADD_WHITE_STATE', self.break_states, self.sid)
        self.transforming = False
        if MC_MOVE in self.break_states:
            move_dir, move_state = self.ev_g_input_move_dir()
            if move_dir and not move_dir.is_zero:
                self.send_event('E_ACTIVE_STATE', MC_MOVE)

    def check_transitions(self):
        handle_name = 'handle_transition_{}'.format(self.npc_id)
        d = globals()
        if handle_name in d:
            handle = d[handle_name]
            if handle:
                return handle(self)

    def exit(self, enter_states):
        self.transforming = False
        super(Transform, self).exit(enter_states)

    def handle_transform(self):
        handle_name = 'handle_recover_{}'.format(self.npc_id) if self.transform_id.find('_trans') > 0 else 'handle_transform_{}'.format(self.npc_id)
        d = globals()
        if handle_name in d:
            handle = d[handle_name]
            if handle:
                handle(self, self.custom_param)

    def reset_camera_state(self):
        if self.camera_state and self.ev_g_is_avatar():
            global_data.player.logic.send_event('E_MECHA_CAMERA', self.camera_state)

    def transition_to_stand(self):
        if self.elapsed_time > self.anim_time:
            self.disable_self()
            speed_value = self.ev_g_speed()
            if speed_value is not None and speed_value > 0:
                max_run_speed = self.ev_g_max_run_speed() or 0
                max_walk_speed = self.ev_g_max_walk_speed() or 0
                if speed_value > max_walk_speed:
                    if speed_value > max_run_speed:
                        speed_value = max_run_speed
                    if self.ev_g_status_check_pass(MC_RUN):
                        return MC_RUN
                elif self.ev_g_status_check_pass(MC_MOVE):
                    return MC_MOVE
            return MC_STAND
        else:
            return


def handle_transition_8005(self):
    return self.transition_to_stand()


def handle_transition_8501(self):
    return self.transition_to_stand()


def handle_transition_8502(self):
    return self.transition_to_stand()


def handle_transition_8503(self):
    return self.transition_to_stand()


def handle_transition_8504(self):
    return self.transition_to_stand()


def handle_transform_8005(self, args):
    if self.ev_g_is_avatar():
        self.send_event('E_USE_MECHA_SPECIAL_FORM_SENSITIVITY', True)
    self.send_event('E_INIT_SHOOT_MODE')
    driver = EntityManager.getentity(self.sd.ref_driver_id)
    if driver and driver.logic:
        driver.logic.send_event('E_SEAT_ON_MECHA', True, self.unit_obj.id)


def handle_recover_8005(self, args):
    if self.ev_g_is_avatar():
        global_data.emgr.on_cancel_reload_event.emit()
        self.send_event('E_USE_MECHA_SPECIAL_FORM_SENSITIVITY', False)
    driver = EntityManager.getentity(self.sd.ref_driver_id)
    if driver and driver.logic:
        driver.logic.send_event('E_SEAT_ON_MECHA', False)