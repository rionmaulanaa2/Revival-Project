# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/com_character_ctrl/ComBehavior.py
from __future__ import absolute_import
import six
from logic.gcommon.component.UnitCom import UnitCom
from logic.gcommon.common_utils import status_utils
from ....cdata.mecha_status_config import *
from logic.gcommon.common_const import buff_const as bconst
from logic.gutils import character_ctrl_utils
from logic.gutils.behavior_utils import get_state
import logic.gcommon.cdata.status_config as status_config
import logic.gcommon.cdata.mecha_status_config as mecha_status_config
from logic.gcommon import editor
import game3d
import copy
BORN_ANIM_LIMIT = {}

@editor.com_exporter('\xe8\xa1\x8c\xe4\xb8\xba\xe7\xbb\x84\xe4\xbb\xb6', {('cur_state', 'string'): {'zh_name': '\xe5\xbd\x93\xe5\x89\x8d\xe7\x8a\xb6\xe6\x80\x81','getter': lambda self: ' '.join([ character_ctrl_utils.get_status_num_2_desc(self)[state_id] for state_id in self._cur_state ])
                             }
   })
class ComBehavior(UnitCom):
    JUMP_STATE = (
     MC_JUMP_1, MC_JUMP_2, MC_JUMP_3)
    DASH_STATE = (
     MC_DASH,)
    BIND_EVENT = {'E_MODEL_LOADED': 'on_model_load_complete',
       'E_ANIMATOR_LOADED': 'on_load_animator_complete',
       'E_ACTIVE_STATE': 'on_active_state',
       'E_REMOVE_TRIGGER_STATE': 'on_remove_trigger_state',
       'G_IS_IN_TRIGGER_STATE': 'is_in_trigger_state',
       'E_DISABLE_STATE': 'on_disable_state',
       'G_TRY_ENTER': 'try_enter_state',
       'G_TRY_EXIT': 'try_exit_state',
       'E_TRY_DRAG': 'try_drag',
       'E_DOUBLE_CLICK': 'set_double_click_state',
       'G_IS_ENABLE_BEHAVIOR': 'is_enable_behavior',
       'E_ENABLE_BEHAVIOR': 'on_enable_behavior',
       'E_DISABLE_BEHAVIOR': 'on_disable_behavior',
       'E_CLEAR_BEHAVIOR': 'on_clear_behavior',
       'E_SWITCH_BEHAVIOR': 'on_switch_behavior',
       'E_SHAPESHIFT': 'on_shape_shift',
       'G_SHAPE_ID': 'on_get_shape_id',
       'E_REFRESH_STATE_PARAM': 'refresh_state_param',
       'E_RESET_STATE_PARAM': 'reset_state_param',
       'G_STATE_PARAM_TYPE': 'get_state_param_type',
       'E_REPLACE_STATE_PARAM': 'replace_state_param',
       'E_REPLACE_ACTION_TRIGGER_ANIM': 'replace_action_trigger_anim',
       'G_ALL_STATE': 'on_get_all_st',
       'G_CUR_STATE': 'on_get_cur_st',
       'G_SHAPE_SHIFT': 'on_get_shape_shift',
       'G_BEHAVIOR_CONFIG': 'get_behavior_config',
       'G_BIND_SKILL': 'get_state_skill_id',
       'E_UPDATE_CUSTOM_PARAM': 'update_custom_param',
       'G_IS_JUMP': 'is_jump',
       'G_IS_DASH': 'is_dash',
       'E_STATE_SPEED_SCALE': 'set_state_speed_scale',
       'E_SWITCHING_ACTION': 'on_switching_action',
       'E_SET_SPEED_SCALE': 'on_set_speed_scale',
       'G_GET_SPEED_SCALE': 'on_get_speed_scale',
       'E_ON_LOSE_CONNECT': 'on_lose_connect',
       'E_SET_TICK_INVERVAL': 'on_set_tick_interval',
       'E_FORCE_UPDATE': 'update_state',
       'E_DUMP_STATE': 'dump_state',
       'G_STATE_NEED_TRIGGER_BTN_UP_WHEN_ACTION_FORBIDDEN': 'get_trigger_btn_up_when_action_forbidden'
       }

    def __init__(self):
        super(ComBehavior, self).__init__()
        self.is_com_behavior = True
        self._bdict = None
        self._st_states = set([])
        self._states = {}
        self._cur_state = set()
        self._passive_trigger_state = set()
        self._passive_leave_state = set()
        self._passive_trigger_state_on_exit = set()
        self._npc_id = None
        self._on_update_exit = False
        self._state_action_map = {}
        self._tick_time_cnt = 0
        self._tick_interval = 0
        self._speed_scale = 1
        self.status_config = None
        return

    def init_from_dict(self, unit_obj, bdict):
        super(ComBehavior, self).init_from_dict(unit_obj, bdict)
        self._bdict = bdict
        self.sd.ref_states = self._states
        self.sd.ref_force_inherit_cam_transformation = False
        if self.sd.ref_is_mecha or self.unit_obj.is_monster():
            self.status_config = mecha_status_config
        else:
            self.status_config = status_config
        self._npc_id = bdict.get('behavior_npc_id') or bdict.get('npc_id', None)
        self._shape_shift = bdict.get('shapeshift', '')
        self._state_param_type = str(self._npc_id)
        self._default_state = bdict.get('default_state', self.status_config.MC_STAND)
        global_data.use_behavior_editor = global_data.is_inner_server and game3d.get_platform() == game3d.PLATFORM_WIN32
        if self._shape_shift:
            self.on_switch_behavior('{}_{}'.format(self._npc_id, self._shape_shift))
        else:
            self.init_state(unit_obj, bdict)
            if self.unit_obj.__class__.__name__ == 'LMechaTrans':
                self.set_default_state(self.status_config.MC_STAND)
        self.sd.ref_cur_state_camera = None
        self.sd.ref_high_priority_cam = None
        return

    def on_set_tick_interval(self, interval):
        self._tick_interval = interval

    def init_state_action_map(self):
        self._state_action_map = {}
        action_conf = character_ctrl_utils.get_action_config(self, self.on_get_shape_id())
        if action_conf:
            status_desc_2_num = character_ctrl_utils.get_status_desc_2_num(self)
            for key, val in six.iteritems(action_conf['action_map']):
                self._state_action_map[status_desc_2_num[val]] = key

    def on_init_complete(self):
        for state in six.itervalues(self._states):
            state.on_init_complete()

        self.detect_const()
        if self.unit_obj.__class__.__name__ == 'LMotorcycle':
            self.ev_g_trans_status(self.status_config.MC_STAND, sync=True)

    def on_post_init_complete(self, bdict):
        for state in six.itervalues(self._states):
            state.on_post_init_complete(bdict)

    def destroy(self):
        super(ComBehavior, self).destroy()
        self.need_update = False
        self.destroy_state()

    def detect_const(self):
        if not self.ev_g_is_avatar():
            return
        global_data.anticheat_utils.detect_const()

    def init_state(self, unit_obj, bdict):
        self.init_state_action_map()
        self._st_states = set([])
        behavior_info = self.get_behavior_config()
        for sid in six.iterkeys(behavior_info):
            self._st_states.add(sid)

        bdict['all_valid_state'] = self._st_states
        for sid, info in six.iteritems(behavior_info):
            state = get_state(info.get('action_state', 'StateBase'))
            if state:
                info = behavior_info.get(sid, {})
                bdict['bind_action_id'] = self._state_action_map.get(sid, None)
                state.status_config = self.status_config
                state.init_from_dict(unit_obj, bdict, sid, info)
                self._states[sid] = state

        return

    def replace_state_param(self, replaced_state, state, include_camera_param=False):
        if replaced_state in self._states and state in self._states:
            param_info = self.get_param_config(self._state_param_type)
            info = param_info.get(state, {})
            if info:
                self._states[replaced_state].refresh_action_param(info.get('action_param', None), info.get('custom_param', None))
                self._states[replaced_state].refresh_sound_param(info.get('sound_param', []))
                include_camera_param and self._states[replaced_state].refresh_camera_param(info.get('state_camera', {}))
        return

    def refresh_state_param(self, param_type='buff', include_camera_param=False):
        new_param_info = self.get_param_config(param_type)
        for sid, info in six.iteritems(new_param_info):
            if not info.get('need_ext_cond', 0):
                if sid == self.status_config.MC_SHOOT:
                    self._states[sid].try_weapon_attack_end()
                self._states[sid].refresh_action_param(info.get('action_param', None), info.get('custom_param', None))
                self._states[sid].refresh_sound_param(info.get('sound_param', []))
                include_camera_param and self._states[sid].refresh_camera_param(info.get('state_camera', {}))

        self._state_param_type = param_type
        self.detect_const()
        return

    def reset_state_param(self, param_type='buff', include_camera_param=False):
        behavior_info = self.get_behavior_config()
        new_param_info = self.get_param_config(param_type)
        for sid in six.iterkeys(new_param_info):
            info = behavior_info[sid]
            if sid == self.status_config.MC_SHOOT:
                self._states[sid].try_weapon_attack_end()
            self._states[sid].refresh_action_param(info.get('action_param', None), info.get('custom_param', None))
            self._states[sid].refresh_sound_param(info.get('sound_param', []))
            include_camera_param and self._states[sid].refresh_camera_param(info.get('state_camera', {}))

        if self._state_param_type.find('_') > 0:
            self._state_param_type = self._state_param_type.split('_')[0]
        else:
            self._state_param_type = str(self._npc_id)
        self.detect_const()
        return

    def get_state_param_type(self):
        return self._state_param_type

    def replace_action_trigger_anim(self, sid_list, anim, **kwargs):
        if type(sid_list) == int:
            sid_list = (
             sid_list,)
        for sid in sid_list:
            state = self._states.get(sid, None)
            state and state.replace_action_trigger_anim(anim, **kwargs)

        return

    def remove_not_register_state(self, states):
        if self.sd.ref_is_mecha:
            return states
        new_states = set()
        for state_id in states:
            if state_id in self._states:
                new_states.add(state_id)

        return new_states

    def dump_state(self):
        state_dict = {}
        for one_state_id in self._cur_state:
            one_state = self._states[one_state_id]
            state_dict[one_state] = one_state.is_active

        log_error('test--ComBehavior.dump_state--npc_id =', self._npc_id, '--need_update =', self.need_update, '--_passive_trigger_state =', self.ev_g_get_state_desc(self._passive_trigger_state), '--_passive_trigger_state_on_exit =', self.ev_g_get_state_desc(self._passive_trigger_state_on_exit), '--len(_cur_state) =', len(self._cur_state), '--_cur_state =', self.ev_g_get_state_desc(self._cur_state), '--state_dict =', state_dict, '--is_enable_behavior =', self.is_enable_behavior(), '--unit_obj =', self.unit_obj)

    def update_state(self, dt):
        if self._tick_interval > 0:
            self._tick_time_cnt += dt
            if self._tick_time_cnt < self._tick_interval:
                return
            dt = self._tick_time_cnt
            self._tick_time_cnt = 0
        dummy_state = self._passive_trigger_state & self._passive_leave_state
        self._passive_leave_state -= dummy_state
        self._passive_trigger_state -= dummy_state
        target_state = self._passive_trigger_state
        self._passive_trigger_state = set()
        target_state -= self._cur_state
        for state_id in self._cur_state:
            next_sid = self._states[state_id].check_transitions()
            if next_sid and next_sid in self._states:
                target_state.add(next_sid)

        passive_leave_state = self._passive_leave_state
        self._passive_leave_state = set()
        for state_id in passive_leave_state:
            if state_id not in self._states:
                log_error('Invalid mecha state_id {0}!!!!!!!!!!!!!!!!!!!!'.format(state_id))
                continue
            self.ev_g_cancel_state(state_id, sync=True)

        for state_id in target_state:
            if state_id not in self._states:
                log_error('Invalid mecha state_id {0}!!!!!!!!!!!!!!!!!!!!'.format(state_id))
                continue
            self.ev_g_trans_status(state_id, sync=True)

        cur_state = self.ev_g_get_all_state()
        cur_state = self.remove_not_register_state(cur_state)
        leave_state = self._cur_state - cur_state
        new_state = cur_state - self._cur_state
        self._on_update_exit = True
        for state_id in leave_state:
            self._states[state_id].exit(new_state)

        self._on_update_exit = False
        self._passive_trigger_state |= self._passive_trigger_state_on_exit
        self._passive_trigger_state_on_exit = set()
        for state_id in new_state:
            self._states[state_id].enter(leave_state)

        for state_id in cur_state:
            state = self._states[state_id]
            state.delta_time += dt
            if state.delta_time >= state.tick_interval:
                state.update(state.delta_time)
                state.delta_time = 0

        self._cur_state = copy.copy(cur_state)
        for state in self._cur_state:
            if state == self.status_config.MC_STAND or self.ev_g_is_cover_state(self.status_config.MC_STAND, state):
                return
        else:
            self._passive_trigger_state.add(self.status_config.MC_STAND)

    def destroy_state(self):
        for state in six.itervalues(self._states):
            state.destroy()

        self._states.clear()

    def tick(self, delta):
        self.update_state(delta)

    def on_model_load_complete(self, model):
        pass

    def on_load_animator_complete(self, *args):
        if self.sd.ref_is_agent:
            self.need_update = True
        if self.ev_g_is_avatar() and self.ev_g_immobilized():
            self._default_state = MC_IMMOBILIZE
        if self.unit_obj.is_monster():
            if self.unit_obj.id in BORN_ANIM_LIMIT:
                return
            BORN_ANIM_LIMIT[self.unit_obj.id] = True
            self.set_default_state(self._default_state)
        elif self.ev_g_is_avatar() or self.sd.ref_is_agent:
            self.set_default_state(self._default_state)

    def on_active_state(self, sid):
        if self._on_update_exit:
            if sid in self._states:
                self._passive_trigger_state_on_exit.add(sid)
            return
        if sid in self._states:
            self._passive_trigger_state.add(sid)

    def on_remove_trigger_state(self, sid):
        if sid in self._passive_trigger_state:
            self._passive_trigger_state.remove(sid)
        if sid in self._passive_trigger_state_on_exit:
            self._passive_trigger_state_on_exit.remove(sid)

    def is_in_trigger_state(self, sid):
        return sid in self._passive_trigger_state

    def on_disable_state(self, sid):
        if isinstance(sid, int):
            self._passive_leave_state.add(sid)
        else:
            self._passive_leave_state |= set(sid)

    def try_enter_state(self, sid):
        if sid in self._states:
            return self._states[sid].action_btn_down()

    def set_double_click_state(self, sid):
        if sid in self._states:
            return self._states[sid].action_btn_double_click()

    def try_exit_state(self, sid):
        if sid in self._states:
            return self._states[sid].action_btn_up()

    def try_drag(self, sid):
        if sid in self._states:
            return self._states[sid].action_btn_drag()

    def get_behavior_config(self):
        npc_id = str(self._npc_id)
        data = status_utils.get_behavior_config(npc_id)
        return data.get_behavior(npc_id)

    def get_param_config(self, param_type='buff'):
        npc_id = str(self._npc_id)
        data = status_utils.get_behavior_config(npc_id)
        return data.get_behavior(param_type)

    def is_enable_behavior(self):
        return self.need_update

    def on_enable_behavior(self, force=False):
        if self.ev_g_is_avatar() or self.sd.ref_is_agent or force:
            self.need_update = True
            self.send_event('E_ENABLE_SYNC', True)
            self.send_event('E_ENABLE_MOVE_SYNC_SENDER', True)
        else:
            self.need_update = False

    def on_disable_behavior(self):
        self.need_update = False

    def set_default_state(self, state_id):
        self.send_event('E_RESET_STATE', state_id=state_id)
        if state_id in self._states:
            self._cur_state.add(state_id)
            default_state = self._states[state_id]
            default_state.enter(set())
            default_state.update(0.01)
        else:
            log_error('Invalid  default_state %s !!!!!!!!!!!!!!!!!!!!' % state_id)

    def on_switch_behavior(self, npc_id, default_state_id=None, keep_pitch=False):
        if default_state_id is None:
            default_state_id = self.status_config.MC_STAND
        self._passive_trigger_state = set()
        self._passive_leave_state = set()
        for state_id in self._cur_state:
            new_states = set([default_state_id])
            self._states[state_id].exit(new_states)

        for state in six.itervalues(self._states):
            if state.bind_action_id:
                self.send_event('E_STOP_POLLER', state.bind_action_id)

        self._cur_state = set()
        self.destroy_state()
        self._npc_id = npc_id
        self._bdict['keep_pitch'] = keep_pitch
        self.init_state(self.unit_obj, self._bdict)
        self.on_init_complete()
        self.set_default_state(default_state_id)
        for state in six.itervalues(self._states):
            if state.bind_action_id:
                self.send_event('E_CHECK_START_POLLER', state.bind_action_id)

        return

    def on_clear_behavior(self):
        self.send_event('E_RESET_STATE')
        self.send_event('E_NOTIFY_CLEAR_RESET')
        self._passive_trigger_state = set()
        self._passive_leave_state = set()
        for state_id in self._cur_state:
            self._states[state_id].exit(set())

        self._cur_state = set()
        if self.ev_g_ignore_recovery_anim():
            return
        if self.status_config.MC_STAND in self._states:
            self._states[self.status_config.MC_STAND].enter(set())
            self._states[self.status_config.MC_STAND].update(0.01)

    def on_get_all_st(self):
        return self._st_states

    def on_get_cur_st(self):
        return self._cur_state

    def on_shape_shift(self, shift):
        self._shape_shift = shift

    def on_get_shape_shift(self):
        return self._shape_shift

    def is_jump(self):
        return self.ev_g_is_in_any_state(self.JUMP_STATE)

    def is_dash(self):
        return self.ev_g_is_in_any_state(self.DASH_STATE)

    def update_custom_param(self, state_id, key, value):
        state = self._states.get(state_id, None)
        if state:
            state.custom_param[key] = value
        return

    def on_switching_action(self, old_status, new_status, keep_alive):
        status_node = self._states.get(old_status, None)
        if not status_node:
            return
        else:
            if not keep_alive:
                if old_status in self._cur_state:
                    self.on_disable_state(old_status)
                if hasattr(status_node, 'on_action_switched'):
                    status_node.on_action_switched()
                elif status_node.__class__.__name__ == 'WeaponFire':
                    if status_node.want_to_fire:
                        status_node.action_btn_up()
                    else:
                        status_node.try_weapon_attack_end()
                else:
                    if type(new_status) in (int,):
                        new_status = {
                         new_status}
                    status_node.exit(new_status)
            return

    def set_state_speed_scale(self, sid, scale):
        state = self._states.get(sid, None)
        if state:
            state.set_state_speed_scale(scale)
        return

    def get_state_skill_id(self, sid):
        if sid in self._states:
            return self._states[sid].get_bind_skill_id()

    def on_set_speed_scale(self, scale):
        self._speed_scale = scale

    def on_get_speed_scale(self):
        return self._speed_scale

    def on_get_shape_id(self):
        return str(self._npc_id)

    def on_lose_connect(self):
        if self.ev_g_ignore_recovery_anim():
            return
        else:
            cur_states = self.ev_g_get_all_state()
            if MC_MECHA_BOARDING not in cur_states or MC_DRIVER_LEAVING not in cur_states:
                if self.ev_g_get_buff(bconst.BUFF_GLOBAL_KEY, bconst.BUFF_ID_BALL_STATE):
                    pass
                elif self.status_config.MC_STAND in self._states:
                    self._states[self.status_config.MC_STAND].enter(set())
                    self._states[self.status_config.MC_STAND].update(0.01)
                    self.send_event('E_CLEAR_UP_BODY_ANIM')
                    self.send_event('E_POST_EXTERN_ACTION', None, False, level=1)
                    self.send_event('E_POST_EXTERN_ACTION', None, False, level=2)
            return

    def get_trigger_btn_up_when_action_forbidden(self, state_id):
        if state_id in self._states:
            return self._states[state_id].need_trigger_btn_up_when_action_forbidden
        return False