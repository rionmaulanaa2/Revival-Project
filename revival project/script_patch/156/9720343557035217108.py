# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/com_lobby_char/ComClimbLobby.py
from __future__ import absolute_import
from logic.gcommon.component.UnitCom import UnitCom
import logic.gcommon.common_const.animation_const as animation_const
import logic.gutils.track_reader
import math3d
import logic.gcommon.common_const.collision_const as collision_const
from logic.gcommon.cdata import status_config
import time
import logic.gcommon.const as g_const
import logic.gcommon.common_utils.bcast_utils as bcast

class ComClimbLobby(UnitCom):
    BIND_EVENT = {'E_ACTION_SWITCH_TO_CLIMB': 'on_action_climb',
       'E_ANIMATOR_LOADED': 'on_load_animator_complete',
       'E_CLIMB': '_on_climb',
       'G_IS_CLIMB': '_is_in_climb'
       }

    def __init__(self):
        super(ComClimbLobby, self).__init__()
        self._action_climb_type = None
        self._climb_state = animation_const.CLIMB_STATE_NONE
        self._clim_up_duration = 0
        self._in_climb = False
        self._climb_timer_id = 0
        self._climb_time = 0.0
        self._climb_type = 0
        self._climb_rotation = 0
        self._climb_pos = math3d.vector(0, 0, 0)
        self._track_reader = logic.gutils.track_reader.TrackReader()
        return

    def init_from_dict(self, unit_obj, bdict):
        super(ComClimbLobby, self).init_from_dict(unit_obj, bdict)

    def destroy(self):
        self._clean_climb_timer()
        super(ComClimbLobby, self).destroy()

    def on_load_animator_complete(self, *args):
        animator = self.ev_g_animator()
        if not animator:
            return
        self.send_event('E_REGISTER_ANIM_ACTIVE', animation_const.BEGIN_CLIM_UP_EVENT, self._begin_clim_up)
        self.send_event('E_REGISTER_ANIM_STATE_EXIT', animation_const.END_CLIM_UP_EVENT, self._end_clim_up)
        self.send_event('E_REGISTER_ANIM_STATE_EXIT', animation_const.END_CLIM_STAND_BARRIER_EVENT, self._end_climb_stand_barrier)
        self._set_climb_state(self._climb_state)

    def _is_in_climb(self):
        return self._in_climb

    def _on_enter_climb_state(self):
        character = self.sd.ref_character
        if character and hasattr(character, 'setIsEnableTestPos'):
            character.setIsEnableTestPos(False)
        from logic.gcommon.common_const.lobby_ani_const import STATE_CLIMB
        self.send_event('E_SET_ANIMATOR_INT_STATE', 'state_idx', STATE_CLIMB)

    def _on_exit_climb_state(self):
        character = self.sd.ref_character
        if character and hasattr(character, 'setIsEnableTestPos'):
            character.setIsEnableTestPos(True)

    def _try_trans_status(self, status):
        from logic.gutils.lobby_jump_utils import can_climb
        if not can_climb(self.unit_obj):
            return False
        return True

    def _on_climb(self, *args):
        self._climb_type = args[0]
        self._climb_pos = args[1]
        self._climb_rotation = args[2]
        can_climb = self._try_trans_status(status_config.ST_CLIMB)
        if not can_climb:
            return
        else:
            self._in_climb = True
            self._on_enter_climb_state()
            self.send_event('E_ACTION_SYNC_CLIMB', self._climb_type, self._climb_pos, self._climb_rotation)
            cur_pos = self.ev_g_position()
            if cur_pos is None:
                return
            yaw = self.ev_g_model_yaw()
            self._track_reader.read_track('test', yaw, cur_pos, self._climb_pos)
            self._clean_climb_timer()
            import common.utils.timer as timer
            self._climb_timer_id = global_data.game_mgr.register_logic_timer(self._climb_tick, 1, times=90, mode=timer.LOGIC)
            self._climb_time = time.time()
            if not (self._climb_type == g_const.CLIMB_TO_TOP_STAND or self._climb_type == g_const.THROW_OVER_TO_TOP_STAND):
                width = collision_const.CHARACTER_CLIMB_WIDTH
                height = collision_const.CHARACTER_CLIMB_HEIGHT
                self.send_event('E_RESIZE_DRIVER_CHARACTER', width, height, collision_const.ALIGN_TYPE_DOWN)
            self.send_event('E_ACTION_SWITCH_TO_CLIMB', self._climb_type, self._climb_pos, self._track_reader.get_track_time())
            return

    def _climb_tick(self):
        pos, is_end = self._track_reader.get_cur_pos(time.time() - self._climb_time)
        self.send_event('E_FOOT_POSITION', pos)
        if is_end:
            self.send_event('E_ACTION_SYNC_CLIMB_TRACK_END')
            self._clean_climb_timer()
            if not (self._climb_type == g_const.CLIMB_TO_TOP_STAND or self._climb_type == g_const.THROW_OVER_TO_TOP_STAND):
                import common.utils.timer as timer
                self._climb_timer_id = global_data.game_mgr.register_logic_timer(self._climb_move_tick, 1, times=30, mode=timer.LOGIC)
            else:
                self._on_climb_finished()

    def _on_climb_finished(self):
        prev_val = self._in_climb
        self._in_climb = False
        if prev_val:
            self._on_exit_climb_state()
        self.send_event('E_CHECK_CONTINUE_MOVE')
        self.send_event('E_ON_END_CLIMB')

    def _clean_climb_timer(self):
        if self._climb_timer_id:
            global_data.game_mgr.unregister_logic_timer(self._climb_timer_id)
        self._climb_timer_id = 0

    def _climb_move_tick(self):
        from logic.gcommon.cdata import speed_physic_arg
        from logic.gcommon.const import NEOX_UNIT_SCALE
        move_dir = math3d.vector(0, 0, speed_physic_arg.climb_move) * math3d.matrix.make_rotation_y(self._climb_rotation)
        self.send_event('E_CHARACTER_WALK', move_dir)
        player_pos = self.ev_g_position()
        if (self._climb_pos - player_pos).length_sqr > g_const.LEAVE_CLIMB_POINT_DISTANCE ** 2:
            width = collision_const.CHARACTER_STAND_WIDTH
            height = collision_const.CHARACTER_STAND_HEIGHT
            self.send_event('E_RESIZE_DRIVER_CHARACTER', width, height, collision_const.ALIGN_TYPE_DOWN)
            self._clean_climb_timer()
            self._on_climb_finished()

    def on_action_climb(self, *arg):
        import logic.gcommon.const as const
        climb_pos = arg[1]
        self._action_climb_type = arg[0]
        self._clim_up_duration = arg[2]
        self.send_event('E_SWITCH_STATUS', animation_const.STATE_CLIMB, False)
        self._set_climb_state(animation_const.CLIMB_STATE_CLIMB_UP)

    def _set_climb_state(self, climb_state):
        self._climb_state = climb_state
        self.send_event('E_SET_ANIMATOR_INT_STATE', 'climb_state', climb_state)

    def _get_climb_state(self):
        return self._climb_state

    def _begin_clim_up(self, arg, node_name):
        animator = self.ev_g_animator()
        if animator:
            source_node = animator.find(node_name)
            actual_anim_time = self._clim_up_duration or 0.1
            time_scale = source_node.duration / actual_anim_time
            source_node.timeScale = time_scale

    def _end_clim_up(self, arg, node_name):
        animator = self.ev_g_animator()
        if animator:
            source_node = animator.find(node_name)
            source_node.timeScale = 1
        self._set_climb_state(animation_const.CLIMB_STATE_STAND_BARRIER)

    def _end_climb_stand_barrier(self, *args):
        self._set_climb_state(animation_const.CLIMB_STATE_ON_GROUND)