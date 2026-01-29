# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/com_mecha_appearance/ComFlightFormClient.py
from __future__ import absolute_import
from logic.gcommon.component.UnitCom import UnitCom
from logic.comsys.archive.archive_manager import ArchiveManager
from common.utils.timer import RELEASE, CLOCK
from logic.client.const.camera_const import FREE_MODEL, OBSERVE_FREE_MODE
from logic.gcommon.common_const.mecha_const import STATE_HUMANOID, STATE_LEVITATE, STATE_INJECT
from logic.gcommon.const import PART_WEAPON_POS_MAIN2, PART_WEAPON_POS_MAIN3, PART_WEAPON_POS_MAIN4
import math3d
import time
FREE_CAMERA_MODE = {
 FREE_MODEL, OBSERVE_FREE_MODE}
STATE_TO_AIM_HELPER_WEAPON_POS_MAP = {STATE_HUMANOID: None,
   STATE_LEVITATE: PART_WEAPON_POS_MAIN2,
   STATE_INJECT: PART_WEAPON_POS_MAIN3
   }
STATE_TO_ACTION = {STATE_HUMANOID: None,
   STATE_LEVITATE: 'action5',
   STATE_INJECT: 'action6'
   }
MAIN_WEAPON_AIM_HELPER_STATE_SET = frozenset([STATE_LEVITATE, STATE_INJECT])

class ComFlightFormClient(UnitCom):
    BIND_EVENT = {'E_SET_FLIGHT_STATE': 'set_flight_state',
       'G_IS_FLIGHT': 'get_is_flight',
       'G_IS_INJECT': 'get_is_inject',
       'E_FUEL_EXHAUSTED': 'end_flight',
       'E_ON_POST_JOIN_MECHA': ('on_post_join_mecha', 99),
       'E_SHOW_FLIGHT_BOOST_GUIDE': 'show_flight_boost_guide',
       'E_SET_INJECT_BRAKE_PARAM': 'set_inject_brake_parameters',
       'E_ENABLE_INJECT_BRAKE_MOVE': 'enable_inject_brake_move',
       'G_INJECT_BRAKE_WALK_DIRECTION': 'get_inject_brake_walk_direction',
       'E_ACTIVATE_FLIGHT_AIM_HELPER': 'activate_flight_aim_helper',
       'E_WEAPON_CHANGED': 'on_weapon_changed',
       'E_ACC_SKILL_BEGIN': 'missile_aim_helper_on',
       'E_ACC_SKILL_END': 'missile_aim_helper_off',
       'E_SET_SERVER_FLIGHT_STATE': 'set_server_flight_state',
       'G_IS_FLIGHT_IN_SERVER': 'get_is_flight_in_server',
       'G_ENABLE_TURN_SOUND': 'get_is_flight_in_server',
       'G_ENABLE_FLY_SOUND': 'get_is_flight_in_server',
       'E_ABORT_INJECT': 'abort_inject',
       'G_INJECT_ABORTED': 'get_inject_aborted',
       'E_FORCE_TRANS_TO_HUMAN': 'end_flight'
       }

    def __init__(self):
        super(ComFlightFormClient, self).__init__(need_update=False)
        self.end_flight_timer = None
        self.inject_brake_timer = None
        self.inject_brake_start_stamp = 0
        self.ini_speed = 0
        self.inject_brake_walk_direction = math3d.vector(0, 0, 0)
        self.boost_inject_dir = math3d.vector(0, 0, 0)
        self.inject_brake_speed = 200
        self.cur_state = STATE_HUMANOID
        self.archive_data = ArchiveManager().get_archive_data(str(global_data.player.uid) + 'Hurricane')
        self.main_weapon_aim_helper_activated = False
        self.main_weapon_aim_helper_weapon_pos = None
        self.second_weapon_aim_helper_activated = False
        self.second_weapon_aim_helper_weapon_pos = None
        self.server_state = STATE_HUMANOID
        self.response_timer = None
        self._last_pos = None
        self._last_forward = None
        self._abort_inject = False
        return

    def init_from_dict(self, unit_obj, bdict):
        super(ComFlightFormClient, self).init_from_dict(unit_obj, bdict)
        self.server_state = bdict.get('flight_state', STATE_HUMANOID)
        self.cur_state = STATE_HUMANOID
        self.auto_move = False
        global_data.emgr.camera_switch_to_state_event += self.set_camera_state

    def on_post_init_complete(self, bdict):
        self.on_weapon_changed(PART_WEAPON_POS_MAIN4)

    def destroy(self):
        self._release_end_flight_timer()
        self._release_inject_brake_timer()
        self._cancel_response_timer()
        global_data.emgr.camera_switch_to_state_event -= self.set_camera_state
        super(ComFlightFormClient, self).destroy()

    def set_camera_state(self, state, old_cam_type, is_finish_switch):
        self.send_event('E_ENTER_FREE_CAMERA', state in FREE_CAMERA_MODE, is_finish_switch)
        self.send_event('E_LEAVE_FREE_CAMERA', state not in FREE_CAMERA_MODE and (old_cam_type in FREE_CAMERA_MODE and is_finish_switch or old_cam_type not in FREE_CAMERA_MODE))

    def set_flight_state(self, state, refresh_brake_timer=True):
        self._handle_action_selected(state)
        refresh_brake_timer and self._begin_inject_brake_timer(state)
        self.cur_state = state
        self._refresh_main_weapon_aim_helper_enabled()

    def get_is_flight(self):
        return self.cur_state in (STATE_LEVITATE, STATE_INJECT)

    def get_is_inject(self):
        return self.cur_state == STATE_INJECT

    def abort_inject(self, abort):
        self._abort_inject = abort

    def get_inject_aborted(self):
        return self._abort_inject

    def end_flight(self):
        self.send_event('E_END_FLIGHT')
        if self.get_is_flight() and not self.ev_g_try_end_flight():
            self._release_end_flight_timer()
            self.end_flight_timer = global_data.game_mgr.register_logic_timer(self._keep_trying_end_flight, interval=1, times=-1)

    def _keep_trying_end_flight(self):
        if self.ev_g_try_end_flight():
            return RELEASE

    def _release_end_flight_timer(self):
        if self.end_flight_timer:
            global_data.game_mgr.unregister_logic_timer(self.end_flight_timer)
            self.end_flight_timer = None
        return

    def on_post_join_mecha(self):
        if not self.ev_g_is_avatar():
            self._is_puppet = True

    def _handle_action_selected(self, state):
        if STATE_TO_ACTION[state]:
            self.send_event('E_SET_ACTION_SELECTED', STATE_TO_ACTION[state], True)
        if STATE_TO_ACTION[self.cur_state]:
            self.send_event('E_SET_ACTION_SELECTED', STATE_TO_ACTION[self.cur_state], False)

    def show_flight_boost_guide(self):
        if global_data.is_pc_mode:
            return
        count = self.archive_data.get('flight_boost_count', 0)
        if count < 3:
            self.archive_data.set_field('flight_boost_count', count + 1)
            from logic.comsys.guide_ui.GuideUI import GuideUI
            GuideUI().show_remote_flight_boost_move(81270, 7)

    def set_inject_brake_parameters(self, *args):
        self.inject_brake_speed = args[0]

    def _begin_inject_brake_timer(self, state):
        self._release_inject_brake_timer()
        if state == STATE_LEVITATE and self.cur_state == STATE_INJECT:
            self.auto_move = True
            self.inject_brake_start_stamp = time.time()
            walk_direction = self.ev_g_get_walk_direction()
            if walk_direction.is_zero:
                return
            self.boost_inject_dir = math3d.vector(walk_direction)
            self.boost_inject_dir.y += self.ev_g_vertical_speed()
            self.boost_inject_dir.normalize()
            if self.boost_inject_dir.x != 0.0:
                self.ini_speed = walk_direction.x / self.boost_inject_dir.x
            else:
                self.ini_speed = walk_direction.z / self.boost_inject_dir.z
            self.inject_brake_timer = global_data.game_mgr.register_logic_timer(self._calculate_inject_brake_speed, interval=1, times=-1)
            self.send_event('E_CALL_SYNC_METHOD', 'hurricane_enter_break', (True,))

    def _calculate_inject_brake_speed(self):
        pass_time = time.time() - self.inject_brake_start_stamp
        cur_speed = self.ini_speed - self.inject_brake_speed * pass_time
        if cur_speed <= 0:
            cur_speed = 0
            self._release_inject_brake_timer()
        self.inject_brake_walk_direction = self.boost_inject_dir * cur_speed
        if self.auto_move:
            walk_direction = math3d.vector(self.inject_brake_walk_direction)
            self.send_event('E_VERTICAL_SPEED', walk_direction.y)
            walk_direction.y = 0
            self.send_event('E_SET_WALK_DIRECTION', walk_direction)

    def _release_inject_brake_timer(self):
        if self.inject_brake_timer:
            global_data.game_mgr.unregister_logic_timer(self.inject_brake_timer)
            self.inject_brake_timer = None
            self.inject_brake_walk_direction = math3d.vector(0, 0, 0)
            self.send_event('E_CALL_SYNC_METHOD', 'hurricane_enter_break', (False,))
        return

    def enable_inject_brake_move(self, flag):
        self.auto_move = flag

    def get_inject_brake_walk_direction(self):
        return self.inject_brake_walk_direction

    def activate_flight_aim_helper(self, flag):
        self.main_weapon_aim_helper_activated = flag
        self._refresh_main_weapon_aim_helper_enabled()

    def on_weapon_changed(self, weapon_pos):
        if weapon_pos == PART_WEAPON_POS_MAIN4:
            second_weapon = self.sd.ref_wp_bar_mp_weapons.get(weapon_pos)
            if hasattr(second_weapon, 'get_is_navigate_enabled') and second_weapon.get_is_navigate_enabled():
                self.second_weapon_aim_helper_activated = True
                return
            if self.second_weapon_aim_helper_weapon_pos:
                self.send_event('E_ENABLE_WEAPON_AIM_HELPER', False, self.second_weapon_aim_helper_weapon_pos)
                self.second_weapon_aim_helper_weapon_pos = None
            self.second_weapon_aim_helper_activated = False
        return

    def _refresh_main_weapon_aim_helper_enabled(self):
        if not self.ev_g_is_avatar():
            return
        else:
            new_weapon_pos = STATE_TO_AIM_HELPER_WEAPON_POS_MAP[self.cur_state] if self.main_weapon_aim_helper_activated else None
            if new_weapon_pos != self.main_weapon_aim_helper_weapon_pos:
                if self.main_weapon_aim_helper_weapon_pos:
                    self.send_event('E_ENABLE_WEAPON_AIM_HELPER', False, self.main_weapon_aim_helper_weapon_pos)
                if new_weapon_pos:
                    self.send_event('E_ENABLE_WEAPON_AIM_HELPER', True, new_weapon_pos)
                self.main_weapon_aim_helper_weapon_pos = new_weapon_pos
            return

    def missile_aim_helper_on(self, weapon_pos):
        if self.main_weapon_aim_helper_weapon_pos:
            self.send_event('E_ENABLE_WEAPON_AIM_HELPER', False, self.main_weapon_aim_helper_weapon_pos, set_need_update=False)
            self.main_weapon_aim_helper_weapon_pos = None
        if self.second_weapon_aim_helper_activated:
            self.send_event('E_ENABLE_WEAPON_AIM_HELPER', True, weapon_pos)
            self.second_weapon_aim_helper_weapon_pos = weapon_pos
        return

    def missile_aim_helper_off(self, *args):
        if self.second_weapon_aim_helper_activated:
            self.send_event('E_ENABLE_WEAPON_AIM_HELPER', False, self.second_weapon_aim_helper_weapon_pos)
        self._refresh_main_weapon_aim_helper_enabled()

    def set_server_flight_state(self, state):
        self.server_state = state
        if state == self.cur_state:
            self._cancel_response_timer()

    def get_is_flight_in_server(self):
        return self.server_state in (STATE_LEVITATE, STATE_INJECT)

    def _start_response_timer(self):
        if hasattr(global_data, 'no_cd') and global_data.no_cd:
            return
        self._cancel_response_timer()
        if self.cur_state != STATE_HUMANOID:
            self.response_timer = global_data.game_mgr.register_logic_timer(self._response_timeout, interval=2, times=1, mode=CLOCK)

    def _response_timeout(self):
        self.end_flight()

    def _cancel_response_timer(self):
        if self.response_timer:
            global_data.game_mgr.unregister_logic_timer(self.response_timer)
            self.response_timer = None
        return