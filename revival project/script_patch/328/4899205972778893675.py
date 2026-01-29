# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComHumanDriverGhost.py
from __future__ import absolute_import
from ..UnitCom import UnitCom
from logic.gcommon import time_utility as time
import math3d
import world
import logic.gutils.track_reader
from ...cdata import status_config
from logic.gcommon.common_const import buff_const as bconst
ITVL_YAW_TRI = 1

class ComHumanDriverGhost(UnitCom):
    BIND_EVENT = {'E_GHOST_ACTION_DELTA_YAW': '_on_yaw',
       'E_DIRECT_ROTATE': '_on_yaw',
       'E_ROTATE_MODEL': '_on_yaw',
       'E_ACTION_SET_YAW': '_on_action_set_yaw',
       'E_SET_YAW': '_on_set_yaw',
       'G_YAW': '_get_yaw',
       'G_POSITION': '_get_position',
       'G_GHOST_POSITION': '_get_position',
       'E_POSITION': '_set_position',
       'E_CTRL_SWIM': 'on_swim',
       'E_CTRL_STOP_SWIM': 'stop_swim',
       'E_HORI_SPD_DIR': '_set_hori_spd_dir',
       'G_WALK_DIRECTION': 'get_move_dir',
       'G_HUMAN_MOVE_DIR': 'get_move_dir',
       'G_INPUT_MOVE_DIR': 'get_input_move_dir',
       'G_CHAR_WAITING': '_get_character_waiting',
       'G_BALL_ACTIVE': ('_is_in_ball_mode', -1),
       'E_ON_BEING_OBSERVE': '_on_observe',
       'E_ON_LEAVE_MECHA': '_on_leave_mecha',
       'E_ON_POST_JOIN_MECHA': '_on_post_join_mecha',
       'E_ON_SYNC_LOD_DIS': '_on_set_sync_lod_dis'
       }

    def __init__(self):
        super(ComHumanDriverGhost, self).__init__(need_update=False)
        self._yaw = 0
        self._yaw_tri_cnt = 0
        self._yaw_cache = 0
        self._move_dir = math3d.vector(0, 0, 0)
        self._climb_timer_id = 0
        self._climb_time = 0.0
        self._climb_type = 0
        self._climb_rotation = 0
        self._climb_pos = math3d.vector(0, 0, 0)
        self.track_reader = logic.gutils.track_reader.TrackReader()
        self._being_ob = False
        self._sync_lod_dis = 0

    def init_from_dict(self, unit_obj, bdict):
        super(ComHumanDriverGhost, self).init_from_dict(unit_obj, bdict)
        if G_POS_CHANGE_MGR:
            self.regist_pos_change(self._set_position)

    def on_post_init_complete(self, bdict):
        self._init_position(bdict)
        f_yaw = self.ev_g_attr_get('human_yaw', 0) or 0
        self.send_event('E_ACTION_SET_YAW', f_yaw)

    def destroy(self):
        if G_POS_CHANGE_MGR:
            self.unregist_pos_change(self._set_position)
        super(ComHumanDriverGhost, self).destroy()

    def _get_position(self):
        return self._position

    def _set_position(self, position):
        self._position = position

    def _get_yaw(self):
        return self._yaw

    def _on_yaw(self, dt_yaw, force=False):
        self._yaw += dt_yaw
        self._yaw_cache += dt_yaw
        self._yaw_tri_cnt -= 1
        if self._yaw_tri_cnt > 0 and not self._being_ob and self._sync_lod_dis > 400:
            return
        self._yaw_tri_cnt = ITVL_YAW_TRI
        self.send_event('E_ACTION_YAW', self._yaw_cache, force)
        self._yaw_cache = 0

    def _on_set_yaw(self, yaw, *args):
        self.send_event('E_ACTION_SET_YAW', yaw)

    def _on_action_set_yaw(self, yaw):
        if yaw is None:
            return
        else:
            self._yaw = yaw
            return

    def _on_set_sync_lod_dis(self, lod_dis):
        self._sync_lod_dis = lod_dis

    def _init_position(self, bdict):
        if 'parachute_position' in bdict:
            pos = bdict.get('parachute_position')
        elif 'position' in bdict:
            pos = bdict.get('position')
        else:
            pos = self.ev_g_attr_set('entity_init_position') or (0, 0, 0)
        self._position = math3d.vector(*pos)
        if self._position.is_zero:
            import traceback
            traceback.print_stack()
            log_error('ComHumanDriverGhost  position init by (0,0,0)')
            return
        if G_POS_CHANGE_MGR:
            self.notify_pos_change(self._position, True)
        else:
            self.send_event('E_POSITION', self._position)

    def _on_climb(self, climb_type, climb_pos, climb_rotation):
        self._climb_type = climb_type
        self._climb_pos = climb_pos
        self._climb_rotation = climb_rotation
        cur_pos = self.ev_g_position()
        yaw = self.ev_g_yaw()
        self.track_reader.read_track('test', yaw, cur_pos, self._climb_pos)
        pos = self.track_reader.get_cur_pos(0.0)
        if self._climb_timer_id:
            global_data.game_mgr.unregister_logic_timer(self._climb_timer_id)
        import common.utils.timer as timer
        self._climb_timer_id = global_data.game_mgr.register_logic_timer(self._climb_tick, 1, times=90, mode=timer.LOGIC)
        self._climb_time = time.time()
        self.send_event('E_ACTION_SWITCH_TO_CLIMB', self._climb_type, self._climb_pos, self.track_reader.get_track_time())

    def _climb_tick(self):
        pos, is_end = self.track_reader.get_cur_pos(time.time() - self._climb_time)
        if G_POS_CHANGE_MGR:
            self.notify_pos_change(pos)
        else:
            self.send_event('E_POSITION', pos)
        if is_end:
            import logic.gcommon.const as g_const
            global_data.game_mgr.unregister_logic_timer(self._climb_timer_id)
            self._climb_timer_id = 0

    def on_swim(self):
        self.ev_g_status_try_trans(status_config.ST_SWIM)

    def stop_swim(self):
        self.ev_g_cancel_state(status_config.ST_SWIM)

    def _set_hori_spd_dir(self, hori_dir):
        if abs(hori_dir.z) < 0.01:
            hori_dir = math3d.vector(hori_dir.x, 0, 0)
        self._move_dir = hori_dir

    def get_move_dir(self):
        return self._move_dir

    def get_input_move_dir(self, *args):
        return (
         self._move_dir, None)

    def _get_character_waiting(self):
        return False

    def _is_in_ball_mode(self):
        in_ball = self.ev_g_get_buff(bconst.BUFF_GLOBAL_KEY, bconst.BUFF_ID_BALL_STATE)
        return in_ball is not None and len(in_ball) > 0

    def _ghost_in_observe(self):
        return self._being_ob

    def _on_observe(self, is_ob):
        self._being_ob = is_ob
        target = self.ev_g_control_target()
        if target and target.logic and target.logic is not self.unit_obj:
            target.logic.send_event('E_ON_BEING_OBSERVE', self._being_ob)

    def _on_leave_mecha(self):
        if not self.sd.ref_is_mecha:
            return
        self._being_ob = False

    def _on_post_join_mecha(self, *args):
        if not self.sd.ref_is_mecha:
            return
        from mobile.common.EntityManager import EntityManager
        driver = EntityManager.getentity(self.sd.ref_driver_id)
        if driver and driver.logic and driver.logic.ev_g_in_observe():
            self._being_ob = True
        else:
            self._being_ob = False