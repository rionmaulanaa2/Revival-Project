# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComMoveSyncReceiver.py
from __future__ import absolute_import
from ..UnitCom import UnitCom
import math3d
from ..component_const import MAX_ITVL_TICK_SYNC, ITVL_MIX_FRAME_PITCH, ITVL_MIX_FRAME_YAW
import logic.gcommon.common_const.animation_const as animation_const
from logic.gcommon import time_utility as t_util
from ...cdata import status_config as st_const
from logic.gcommon.common_const.water_const import WATER_DEEP_LEVEL
from logic.gcommon.common_const.ai_const import MOVE_TYPE_PATHING, MOVE_TYPE_FAST_PATHING, MOVE_TYPE_NORMAL
from ...cdata import speed_physic_arg
import logic.gcommon.const as const
import logic.gcommon.common_const.collision_const as collision_const
import collision
MAX_FOLLOW_TARGET_POS = 40
MAX_FOLLOW_TARGET_DISTANCE = 600.0 * const.NEOX_UNIT_SCALE
MID_FOLLOW_TARGET_POS = 5
MID_FOLLOW_TARGET_DISTANCE = 150.0 * const.NEOX_UNIT_SCALE
CHECK_HEIGHT = math3d.vector(0, const.NEOX_UNIT_SCALE, 0)
MOVE_TYPE_TEST_AUTO_PATH = 996
DIRECT_GO_LIMIT_PATH_LEN = 5
MP_ALWAYS_FOWARD_VALUE = {MOVE_TYPE_NORMAL: const.MOVE_TO_MODE_NONE,
   MOVE_TYPE_PATHING: const.MOVE_TO_MODE_ALWAYS_FORWARD,
   MOVE_TYPE_FAST_PATHING: const.MOVE_TO_MODE_ALWAYS_FORWARD,
   MOVE_TYPE_TEST_AUTO_PATH: const.MOVE_TO_MODE_ALWAYS_FORWARD_WITH_CAM
   }

class ComMoveSyncReceiver(UnitCom):
    BIND_EVENT = {'E_ACTION_SYNC_RC_DIR': '_action_sync_dir',
       'E_ACTION_SYNC_RC_YAW': '_action_sync_yaw',
       'E_ACTION_SYNC_RC_HEAD_PITCH': '_action_sync_head_pitch',
       'E_ACTION_SYNC_RC_JUMP': '_action_sync_jump',
       'E_ACTION_SYNC_RC_STATUS': '_action_sync_status',
       'G_CAM_PITCH': '_get_cam_pitch',
       'E_AGONY': '_on_agony',
       'E_ON_SAVED': '_on_saved',
       'E_REVIVE': '_on_revive',
       'G_ACTION_SYNC_RC_LIST': '_get_sync_dir_list',
       'G_CHECK_SYNC_DIR_LIST': '_check_sync_dir_list',
       'E_MOVE_ENABLE': '_enable_move',
       'E_ON_JOIN_MECHA': '_on_join_mecha',
       'E_CLEAR_MOVE_TO_POS': '_on_clear_move_to_pos'
       }

    def __init__(self):
        super(ComMoveSyncReceiver, self).__init__(need_update=True)
        self._cur_pd_pos = None
        self._lst_to_pos = []
        self._cnt_pathing = 0
        self._cur_move_type = MOVE_TYPE_NORMAL
        self._cam_pitch = 0
        self._can_move = True
        return

    def init_from_dict(self, unit_obj, bdict):
        super(ComMoveSyncReceiver, self).init_from_dict(unit_obj, bdict)
        self._is_agony = bdict.get('is_agony', False)

    def _on_agony(self, *args):
        self._is_agony = True

    def _on_saved(self, *args):
        self._is_agony = False

    def _on_revive(self, *args):
        self._is_agony = False

    def _on_join_mecha(self, mecha_id, *args):
        self.clear_pos()

    def _on_clear_move_to_pos(self, *args):
        self.clear_pos()

    def destroy(self):
        super(ComMoveSyncReceiver, self).destroy()

    def tick(self, dt):
        if not self._can_move:
            return
        self._follow_new(dt)

    def _follow_to_last_one(self):
        if not self._lst_to_pos:
            return
        v3d_pos, i_move_type, v3d_pos_dir = self.pop_pos()
        always_foward = MP_ALWAYS_FOWARD_VALUE.get(i_move_type, const.MOVE_TO_MODE_ALWAYS_FORWARD)
        f_spd = self.trans_move_state(i_move_type)
        self.send_event('E_AI_MOVE_TO', v3d_pos, f_spd, always_foward, v3d_pos_dir)

    def _can_go_direct(self, v3d_pos, i_move_type):
        cur_pos = self.ev_g_position()
        if not cur_pos:
            return False
        scn = self.scene
        if not scn:
            return False
        if i_move_type == MOVE_TYPE_TEST_AUTO_PATH:
            return False
        if i_move_type == MOVE_TYPE_NORMAL and len(self._lst_to_pos) < DIRECT_GO_LIMIT_PATH_LEN:
            return False
        chect_begin = cur_pos + math3d.vector(0, 1, 0)
        check_end = v3d_pos + math3d.vector(0, 1, 0)
        result = scn.scene_col.hit_by_ray(chect_begin, check_end, 0, collision_const.GROUP_CHARACTER_INCLUDE, collision_const.GROUP_CHARACTER_INCLUDE, collision.INCLUDE_FILTER, False)
        if result[0]:
            return False
        chect_begin = chect_begin + CHECK_HEIGHT
        check_end = check_end + CHECK_HEIGHT
        result = scn.scene_col.hit_by_ray(chect_begin, check_end, 0, collision_const.GROUP_CHARACTER_INCLUDE, collision_const.GROUP_CHARACTER_INCLUDE, collision.INCLUDE_FILTER, False)
        if result[0]:
            return False
        return True

    def push_pos(self, v3d_pos, i_move_type, v3d_pos_dir):
        if self._can_go_direct(v3d_pos, i_move_type):
            f_spd = self.trans_move_state(i_move_type)
            always_foward = MP_ALWAYS_FOWARD_VALUE.get(i_move_type, const.MOVE_TO_MODE_ALWAYS_FORWARD)
            self.send_event('E_AI_MOVE_TO', v3d_pos, f_spd, always_foward, v3d_pos_dir)
            self.clear_pos()
            return
        self._lst_to_pos.append((v3d_pos, i_move_type, v3d_pos_dir))
        if i_move_type == MOVE_TYPE_PATHING:
            self._cnt_pathing += 1

    def pop_pos(self):
        tp_to = self._lst_to_pos.pop(0)
        if tp_to[1] == MOVE_TYPE_PATHING:
            self._cnt_pathing -= 1
        return tp_to

    def clear_pos(self):
        self._lst_to_pos = []
        self._cnt_pathing = 0

    def _follow_new(self, dt):
        if not self._lst_to_pos:
            return
        cur_pos = self.ev_g_position()
        _to_pos = self.ev_g_target_pos()
        if not cur_pos:
            return
        if _to_pos and (cur_pos - _to_pos).length > 2.0:
            return
        self._follow_to_last_one()

    def _get_cam_pitch(self):
        return self._cam_pitch

    def check_phys(self):
        if not self.ev_g_char_waiting():
            return
        self.ev_g_char_resume_col()

    def _get_sync_dir_list(self):
        return self._lst_to_pos

    def _check_sync_dir_list(self):
        if not self._lst_to_pos:
            return False
        self._follow_to_last_one()
        return True

    def _action_sync_dir(self, v3d_pos, i_move_type=MOVE_TYPE_PATHING, v3d_pos_dir=None):
        self.check_phys()
        cur_pos = self.ev_g_position()
        if cur_pos is None:
            return
        else:
            if self._cur_move_type != MOVE_TYPE_NORMAL and i_move_type == MOVE_TYPE_NORMAL:
                self.send_event('E_STOP_MOVE_TO')
                self.clear_pos()
            if self._cnt_pathing >= MID_FOLLOW_TARGET_POS:
                self.send_event('E_CTRL_FORCE_MOVE_STOP')
                return
            self.push_pos(v3d_pos, i_move_type, v3d_pos_dir)
            _target_pos = self.ev_g_target_pos()
            if not _target_pos:
                self._follow_new(0)
            return

    def trans_move_state(self, i_move_type):
        self._cur_move_type = i_move_type
        f_spd = 0
        move_st = animation_const.MOVE_STATE_WALK
        water_status = self.sd.ref_water_status
        if water_status >= WATER_DEEP_LEVEL:
            self.send_event('E_CHANGE_MOVE_STATE', move_st)
            return f_spd
        if self._is_agony:
            move_st = animation_const.MOVE_STATE_WALK
        elif self.ev_g_get_state(st_const.ST_STAND):
            if i_move_type == MOVE_TYPE_FAST_PATHING:
                move_st = animation_const.MOVE_STATE_RUN
            else:
                move_st = animation_const.MOVE_STATE_WALK
        elif self.ev_g_get_state(st_const.ST_CROUCH):
            if i_move_type == MOVE_TYPE_FAST_PATHING:
                move_st = animation_const.MOVE_STATE_RUN
            else:
                move_st = animation_const.MOVE_STATE_WALK
        self.send_event('E_CHANGE_MOVE_STATE', move_st)
        if move_st == animation_const.MOVE_STATE_RUN:
            f_spd = speed_physic_arg.empty_hand_run
        return f_spd

    def _action_sync_yaw(self, f_yaw, f_dt=0):
        cur_yaw = self.ev_g_yaw()
        if cur_yaw is None:
            return
        else:
            dt_yaw = f_yaw - cur_yaw
            if not dt_yaw:
                return

            def cb(dt_per):
                if abs(dt_per) < 0.001:
                    return True
                self.send_event('E_DELTA_YAW', dt_per)

            self.send_event('E_CLIENT_INTER_PUT', 'it_yaw', dt_yaw, ITVL_MIX_FRAME_YAW, cb)
            return

    def _action_sync_head_pitch(self, f_pitch):
        dt_pitch = f_pitch - self._cam_pitch

        def cb(dt_per):
            if abs(dt_per) < 0.001:
                return True
            self.send_event('E_DELTA_PITCH', dt_per)
            self._cam_pitch += dt_per

        if dt_pitch:
            self.send_event('E_CLIENT_INTER_PUT', 'it_pitch', dt_pitch, ITVL_MIX_FRAME_PITCH, cb)

    def _action_sync_jump(self, jump_state):
        if self.ev_g_get_state(st_const.ST_SWIM):
            return
        self.check_phys()
        if jump_state:
            self.send_event('E_CTRL_JUMP')

    def _action_sync_status(self, status):
        if self.ev_g_get_state(st_const.ST_SWIM):
            return
        if status in animation_const.MP_STATUS_2_EVENT:
            event = animation_const.MP_STATUS_2_EVENT[status]
            self.send_event(event)
        if status in (animation_const.STATE_JUMP,):
            return
        self.send_event('E_SWITCH_STATUS', status)

    def _enable_move(self, enable):
        self._can_move = enable