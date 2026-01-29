# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/com_character_ctrl/ComInput.py
from __future__ import absolute_import
import six
from logic.gcommon.component.UnitCom import UnitCom
from logic.gutils import character_ctrl_utils
import math3d

class ComInput(UnitCom):
    BIND_EVENT = {'E_ENABLE_BEHAVIOR': ('on_enable_behavior', 100),
       'E_MOVE_ROCK_STATE': 'on_rocker_state',
       'E_MOVE_ROCK': 'on_rocker_move',
       'E_MOVE_ROCK_DIR': 'on_rocker_move_dir',
       'E_ROCK_STOP': 'on_rocker_stop',
       'G_IS_ACTION_DOWN': 'check_action_btn_down',
       'G_ACTION_DOWN': 'on_action_btn_down',
       'E_ACTION_UP': 'on_action_btn_up',
       'E_ACTION_DRAG': 'on_action_drag',
       'E_DELTA_YAW': 'on_camera_yaw',
       'E_DELTA_PITCH': 'on_camera_pitch',
       'E_SWITCH_ACTION': 'on_switch_action',
       'E_SET_ACTION_VISIBLE': 'on_set_action_visible',
       'E_SWITCH_BEHAVIOR': 'on_switch_behavior',
       'E_DISABLE_BEHAVIOR': 'on_disable_behavior',
       'E_STOP_POLLER': 'stop_poller',
       'E_CHECK_START_POLLER': 'check_start_poller',
       'G_GET_ACTION_BY_STATUS': 'on_get_action_by_status',
       'G_GET_STATUS_BY_ACTION': 'on_get_status_by_action',
       'G_ACTION_STATUS': 'on_get_action_status',
       'E_ALL_ACTION_UP': 'on_all_action_btn_up',
       'E_SET_ROCKER_RADIUS': 'set_rocker_radius',
       'E_SET_ROCKER_MOVE_DIST': 'set_rocker_move_dist',
       'E_DISABLE_ROCKER_ANIM_DIR': 'on_disable_rocker_anim_dir',
       'G_IS_MAIN_ACTION': '_is_main_action',
       'G_IS_SUB_ACTION': '_is_sub_action',
       'E_ENABLE_ROCKER_MOVE': 'enable_rocker_move',
       'G_ACTION_NEED_TRIGGER_UP_WHEN_FORBIDDEN': 'get_action_need_trigger_up_when_forbidden'
       }

    def __init__(self):
        super(ComInput, self).__init__()
        self.sd.ref_rocker_dir = None
        self.sd.ref_can_run = False
        self.rocker_anim_dir_disabled = False
        self.sd.ref_rocker_radius = 110
        self.sd.ref_rocker_move_dist = 0
        self.sd.ref_rocker_move_percent = 0
        self.sd.ref_effective_camera_rot = None
        self.sd.ref_rocker_run_state = False
        self._enable_move = True
        self.action_btn_down = {}
        self.action_map = {}
        self.action_auto_check_timer = {}
        self.poller_btn = {}
        self.action_disabled = {}
        return

    def init_from_dict(self, unit_obj, bdict):
        super(ComInput, self).init_from_dict(unit_obj, bdict)
        self.sd.ref_effective_camera_rot = math3d.matrix_to_rotation(self.scene.active_camera.rotation_matrix)

    def map_actions(self, shape_id=None):
        poller_actions = self.stop_all_timer()
        shape_id = shape_id or self.ev_g_shape_id()
        action_conf = character_ctrl_utils.get_action_config(self, shape_id)
        if action_conf:
            status_desc_2_num = character_ctrl_utils.get_status_desc_2_num(self)
            for key, val in six.iteritems(action_conf['action_map']):
                self.action_map[key] = status_desc_2_num[val]
                self.poller_btn[key] = key in action_conf.get('poller_btn', [])
                if key in self.action_btn_down:
                    if not self.poller_btn[key]:
                        self.action_btn_down[key] = False
                else:
                    self.action_btn_down[key] = False
                self.action_auto_check_timer[key] = None

        for action_id in poller_actions:
            self.start_poller(action_id)

        return

    def on_switch_behavior(self, shape_id, *args):
        self.map_actions(shape_id)

    def on_init_complete(self):
        self.map_actions()

    def on_disable_behavior(self):
        for timer_id in six.itervalues(self.action_auto_check_timer):
            if timer_id:
                global_data.game_mgr.unregister_logic_timer(timer_id)

        self.action_auto_check_timer = {}

    def stop_all_timer(self, *args):
        poller_actions = []
        for action_id, timer_id in six.iteritems(self.action_auto_check_timer):
            if timer_id:
                poller_actions.append(action_id)
                global_data.game_mgr.unregister_logic_timer(timer_id)
                timer_id = None

        return poller_actions

    def destroy(self):
        for timer_id in six.itervalues(self.action_auto_check_timer):
            if timer_id:
                global_data.game_mgr.unregister_logic_timer(timer_id)

        self.action_auto_check_timer = {}
        super(ComInput, self).destroy()

    def on_enable_behavior(self, *args):
        self.sd.ref_effective_camera_rot = math3d.matrix_to_rotation(self.scene.active_camera.rotation_matrix)

    def on_rocker_move_dir(self, rocker_dir):
        self.sd.ref_rocker_dir = rocker_dir
        if not self.rocker_anim_dir_disabled:
            self.send_event('E_CHANGE_ANIM_MOVE_DIR', rocker_dir.x, rocker_dir.z)

    def on_rocker_state(self, rocker_state):
        self.sd.ref_rocker_run_state = rocker_state

    def enable_rocker_move(self, enable):
        self._enable_move = enable

    def on_rocker_move(self, rocker_dir, can_run):
        if not self._enable_move:
            return
        self.sd.ref_rocker_dir = rocker_dir
        self.sd.ref_can_run = can_run
        if not self.rocker_anim_dir_disabled:
            self.send_event('E_CHANGE_ANIM_MOVE_DIR', rocker_dir.x, rocker_dir.z)

    def on_rocker_stop(self):
        self.sd.ref_rocker_dir = None
        self.sd.ref_can_run = False
        if not self.rocker_anim_dir_disabled:
            self.send_event('E_CHANGE_ANIM_MOVE_DIR', 0, 0)
        return

    def check_action_btn_down(self, action):
        return self.action_btn_down.get(action, False)

    def on_action_btn_down(self, action, is_double_click=False):
        if action in self.action_map:
            if action in self.action_disabled:
                return
            self.action_btn_down[action] = True
            ret = self.ev_g_try_enter(self.action_map[action])
            if is_double_click:
                self.send_event('E_DOUBLE_CLICK', self.action_map[action])
            if self.poller_btn[action]:
                self.start_poller(action)
            if ret:
                if self._is_main_action(action) or self._is_sub_action(action):
                    if self.ev_g_is_avatar():
                        global_data.emgr.avatar_mecha_main_or_sub_atk_start.emit()
                    return
            return ret

    def on_action_btn_up(self, action):
        if action in self.action_map:
            if action in self.action_disabled:
                return
            self.action_btn_down[action] = False
            if self.poller_btn[action]:
                self.stop_poller(action)
            return self.ev_g_try_exit(self.action_map[action])

    def on_all_action_btn_up(self):
        for action in six.iterkeys(self.action_map):
            if self.action_btn_down[action]:
                self.on_action_btn_up(action)

    def on_action_drag(self, action):
        if action not in self.action_map:
            return
        if self.action_btn_down[action]:
            self.send_event('E_TRY_DRAG', self.action_map[action])

    def on_camera_yaw(self, delta):
        self.send_event('E_ROTATE', delta)
        self.sd.ref_effective_camera_rot = math3d.matrix_to_rotation(self.scene.active_camera.rotation_matrix)

    def on_camera_pitch(self, delta):
        self.send_event('E_PITCH', delta)
        self.sd.ref_effective_camera_rot = math3d.matrix_to_rotation(self.scene.active_camera.rotation_matrix)

    def on_get_action_status(self, action):
        return self.action_btn_down[action]

    def on_get_action_by_status(self, status):
        for action, config_status in six.iteritems(self.action_map):
            if config_status == status:
                return action

    def on_get_status_by_action(self, action):
        return self.action_map.get(action, None)

    def on_switch_action(self, action, status, keep_alive=True):
        old_status = self.action_map.get(action, None)
        if isinstance(status, str):
            status_desc_2_num = character_ctrl_utils.get_status_desc_2_num(self)
            self.action_map[action] = status_desc_2_num[status]
        else:
            self.action_map[action] = status
        if old_status is not None:
            self.send_event('E_SWITCHING_ACTION', old_status, self.action_map[action], keep_alive)
        shape_id = self.ev_g_shape_id()
        action_conf = character_ctrl_utils.get_action_config(self, shape_id)
        if action_conf:
            self.poller_btn[action] = action in action_conf.get('poller_btn', [])
        return

    def check_enter_action(self, *args):
        action_id, = args
        self.ev_g_try_enter(self.action_map[action_id])

    def start_poller(self, action_id):
        if action_id in self.action_auto_check_timer and self.action_auto_check_timer[action_id]:
            global_data.game_mgr.unregister_logic_timer(self.action_auto_check_timer[action_id])
        self.action_auto_check_timer[action_id] = global_data.game_mgr.register_logic_timer(self.check_enter_action, interval=1, args=[action_id], times=-1)

    def stop_poller(self, action_id):
        if action_id in self.action_auto_check_timer and self.action_auto_check_timer[action_id]:
            global_data.game_mgr.unregister_logic_timer(self.action_auto_check_timer[action_id])
            self.action_auto_check_timer[action_id] = None
        return

    def check_start_poller(self, action_id):
        if action_id in self.action_map:
            if action_id in self.action_disabled:
                return
        if self.check_action_btn_down(action_id):
            if action_id in self.action_auto_check_timer and self.action_auto_check_timer[action_id]:
                return
            if self.poller_btn[action_id]:
                self.start_poller(action_id)

    def on_set_action_visible(self, action, visible, force=False):
        if not visible:
            if action in self.action_map:
                self.on_action_btn_up(action)
            self.action_disabled[action] = True
        elif action in self.action_disabled:
            del self.action_disabled[action]

    def set_rocker_radius(self, radius):
        self.sd.ref_rocker_radius = radius

    def set_rocker_move_dist(self, dist):
        self.sd.ref_rocker_move_dist = min(dist, self.sd.ref_rocker_radius)
        self.sd.ref_rocker_move_percent = self.sd.ref_rocker_move_dist / self.sd.ref_rocker_radius

    def on_disable_rocker_anim_dir(self, flag):
        self.rocker_anim_dir_disabled = flag

    def _is_main_action(self, action_id):
        s = {
         'action1', 'action2', 'action3'}
        return action_id in s

    def _is_sub_action(self, action_id):
        return action_id == 'action4'

    def get_action_need_trigger_up_when_forbidden(self, action_id):
        if action_id in self.action_map:
            state_id = self.action_map[action_id]
            return self.ev_g_state_need_trigger_btn_up_when_action_forbidden(state_id)
        return False