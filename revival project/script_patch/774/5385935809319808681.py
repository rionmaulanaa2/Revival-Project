# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComMoveSyncSender2.py
from __future__ import absolute_import
import six_ex
from ..UnitCom import UnitCom
from logic.gcommon import time_utility as t_util
import time as org_time
import math3d
import world
import collision
from logic.gutils.sync.SyncTrigger import SyncTrigger, DT_WIN_DEFAULT, DT_WIN_MID, DT_WIN_LARGE
import logic.gcommon.common_const.animation_const as animation_const
from logic.gcommon.common_utils.parachute_utils import STAGE_NONE, STAGE_FREE_DROP, STAGE_PARACHUTE_DROP, STAGE_PLANE, STAGE_LAND
from logic.gcommon.common_const.sync_const import SYNC_TRIGGER_NAME_EULER, SYNC_ITPLER_NAME_ROT, VEL_MOVE_FORWARD_SEND, SENDER_MODE_NORMAL, SENDER_MODE_ROTATION_ONLY, SENDER_MODE_BALL_CTRL, SENDER_MODE_PARACHUTE_SIMULATE_FOLLOWING
from logic.gcommon.common_const import water_const
from logic.gcommon.const import NEOX_UNIT_SCALE
from logic.gcommon.const import USE_FLOAT_REDUCE
import logic.gcommon.common_utils.float_reduce_util as fl_reduce
from ...cdata.status_config import ST_SWIM
import logic.gcommon.common_utils.bcast_utils as bcast
from logic.gcommon.common_const.battle_const import TRY_TELE_POS_REASON_NORMAL, MOVE_X_LIMIT, MOVE_Y_LIMIT, MOVE_Z_LIMIT
import logic.gcommon.common_const.battle_const as battle_const
T_LOCK_NO_DROP_DMG = 3.0
ADJUST_Y_OFFSET = 5 * NEOX_UNIT_SCALE
MP_NAME_2_COM = {SYNC_TRIGGER_NAME_EULER: ('ComMoveSyncEulerSender', 'client'),
   SYNC_ITPLER_NAME_ROT: ('ComMoveSyncRotSender', 'client')
   }
STUCK_REASON = (
 battle_const.TRY_TELE_POS_REASON_DEFAULT, battle_const.TRY_TELE_POS_REASON_HMAP, battle_const.TRY_TELE_POS_REASON_NORMAL)

class ComMoveSyncSender2(UnitCom):
    BIND_EVENT = {'E_ACTION_SYNC_YAW': '_dt_f_yaw',
       'E_ACTION_SYNC_FORCE_YAW': '_on_force_yaw',
       'E_ACTION_SYNC_HEAD_PITCH': '_dt_f_head_pitch',
       'E_POSITION': '_on_pos_change',
       'E_SET_POSITION_FORCE': '_on_pos_force_set',
       'E_ACTION_SYNC_STOP': '_v_stop',
       'E_ACTION_SYNC_JUMP': '_jump_change',
       'E_ON_JUMP_STATE_CHANGE': '_on_jump_state_change',
       'E_ACTION_SYNC_GROUND': '_on_ground',
       'E_ACTION_SYNC_STATUS': '_switch_status',
       'E_RECREATE_CHARACTER': 'on_character_recreate',
       'E_CHARACTER_DEACTIVE': '_on_char_deactive',
       'E_CHARACTER_ACTIVE': '_on_char_active',
       'E_DO_RB_POS': '_on_roll_back_pos',
       'G_RB_POS_LOG': 'get_rb_pos_log',
       'E_ACTION_SYNC_CLEAR': '_on_clear_trigger',
       'E_SYNC_MOVE_ITPL_STABLE_X': '_set_itpl_stable_x',
       'E_WATER_EVENT': '_on_water_status',
       'E_ACTION_SYNC_ACC': '_on_action_acc',
       'E_ACTION_SYNC_VEL': '_on_action_vel',
       'E_ACTION_CHECK_POS': '_on_check_pos',
       'E_ACTION_SYNC_ATTR': '_on_action_attr',
       'E_PARACHUTE_STATUS_CHANGED': '_on_parachute_state_changed',
       'E_ENABLE_SYNC_ALL_RECORD': '_enable_sync_all_record',
       'E_SET_ENABLE_INITIATIVE_STOP': '_set_enable_initiative_stop',
       'E_ENABLE_MOVE_SYNC_SENDER': 'set_enable',
       'E_ACTION_IGNORE_NEXT_POS': '_ignore_next_pos',
       'E_ACTIVE_SENDER_MODE': ('_on_active_mode', 999),
       'E_ENABLE_PARACHUTE_SIMULATE_FOLLOWING': '_enable_parachute_simulate_following'
       }
    HANDLER_TYPE = 'SenderHandler'

    def __init__(self):
        super(ComMoveSyncSender2, self).__init__(need_update=True)
        self._enable = True
        self._enable_ask = True
        self.need_update = True
        self._trigger = SyncTrigger()
        self._itpl_x = 0
        self._trigger.set_callback('all', self.on_trigger_all)
        self._trigger.set_callback('ask_pos', self.on_trigger_ask_pos)
        self._trigger.set_callback('yaw', self.on_trigger_yaw)
        self._trigger.set_callback('head_pitch', self.on_trigger_head_pitch)
        self._parachuting = False
        self._in_change_character = False
        self.mp_triggers = {}
        self._cache_pos = None
        self._i_status = None
        self._i_jump_state = None
        self._climb_type = None
        self._climb_pos = None
        self._climb_rotation = None
        self._walk_st = set()
        self._last_pos = None
        self._last_vel = math3d.vector(0, 0, 0)
        self._last_acc = math3d.vector(0, 0, 0)
        self._last_time = None
        self._next_jump = False
        self._last_forward = math3d.vector(0, 0, 0)
        self._cur_forward = math3d.vector(0, 0, 1)
        self._t_last_parachute_drop = 0
        self._t_last_accept = 0
        self._enable_record = False
        self._sync_record = []
        self._mode = SENDER_MODE_NORMAL
        self._do_none_sync = True
        self._enable_sync_yaw = True
        self._enable_initiative_stop = True
        self._enable_param = False
        self._rtt = 0
        return

    def init_from_dict(self, unit_obj, bdict):
        super(ComMoveSyncSender2, self).init_from_dict(unit_obj, bdict)
        if 'position' in bdict:
            self._last_pos = math3d.vector(*bdict['position'])
        if G_POS_CHANGE_MGR:
            self.regist_pos_change(self._on_pos_change)
        self._walk_st = set(self.ev_g_walk_state() or ())
        com = unit_obj.get_com('ComSyncSenderData')
        if not com:
            com = unit_obj.add_com('ComSyncSenderData', 'client')
            com.init_from_dict(unit_obj, {})
        global_data.g_com_sysmgr.add_handler(self)
        self.last_roll_back_log = None
        return

    def on_init_complete(self):
        if self.unit_obj.is_mecha() or self.unit_obj.is_robot():
            self._enable_param = True
        self._try_do_rb_pos()
        global_data.emgr.net_delay_time_event += self.update_network_delay

    def destroy(self):
        global_data.emgr.net_delay_time_event -= self.update_network_delay
        global_data.g_com_sysmgr.remove_handler(self)
        com = self.unit_obj.get_com('ComSyncSenderData')
        if com:
            self.unit_obj.del_com('ComSyncSenderData')
        self._enable = False
        self.unload_all_trigger()
        if G_POS_CHANGE_MGR:
            self.unregist_pos_change(self._on_pos_change)
        self._trigger.stop()
        self._trigger.destroy()
        self._trigger = None
        super(ComMoveSyncSender2, self).destroy()
        return

    def change_parachute_state(self, stage):
        if stage in (STAGE_PLANE,):
            self.set_enable(False)
        else:
            self.set_enable(True)

    def tick_data(self, dt):
        if self.sd.ref_rotatedata:
            self._trigger.update_with_data(dt, self.sd.ref_rotatedata)

    def tick(self, dt):
        pass

    def set_enable(self, enable):
        if enable == self._enable:
            return
        self._enable = enable
        if self._enable:
            self._trigger.restart()
            self.on_trigger_ask_pos()
        else:
            self._trigger.stop()

    def set_ask_enable(self, enable):
        self._enable_ask = enable

    def _set_itpl_stable_x(self, x):
        if x == self._itpl_x:
            return
        self._itpl_x = x
        if self._itpl_x:
            self._trigger.set_collect_win(DT_WIN_MID)
        else:
            self._trigger.set_collect_win(DT_WIN_DEFAULT)

    def _set_enable_initiative_stop(self, enable):
        self._enable_initiative_stop = enable

    def set_enable_sync_trigger(self, lst_trigger_name):
        for trigger_name in lst_trigger_name:
            self.load_trigger(trigger_name)

    def set_disable_sync_trigger(self, lst_trigger_name):
        for trigger_name in lst_trigger_name:
            self.unload_trigger(trigger_name)

    def unload_trigger(self, trigger_name):
        if not self.is_trigger_load(trigger_name):
            return
        com_name, com_type = MP_NAME_2_COM[trigger_name]
        self.unit_obj.del_com(com_name)
        self.mp_triggers.pop(trigger_name)

    def load_trigger(self, trigger_name):
        if self.is_trigger_load(trigger_name):
            return
        com_name, com_type = MP_NAME_2_COM[trigger_name]
        self.mp_triggers[trigger_name] = True
        c = self.unit_obj.add_com(com_name, com_type)
        c.init_from_dict(self.unit_obj, {})

    def is_trigger_load(self, trigger_name):
        com_name, com_type = MP_NAME_2_COM[trigger_name]
        if self.unit_obj.get_com(com_name):
            return True
        else:
            return False

    def unload_all_trigger(self):
        if not self.unit_obj:
            return
        for trigger_name in six_ex.keys(self.mp_triggers):
            self.unload_trigger(trigger_name)

    def _enable_sync_all_record(self, enable):
        self._enable_record = enable
        if not enable:
            import os
            import game3d
            import json
            if len(self._sync_record) == 0:
                return
            record_path = os.path.join(game3d.get_doc_dir(), 'test_00000')
            final_record = []
            start_time = self._sync_record[0][0]
            start_pos = self._sync_record[0][2]
            for info in self._sync_record:
                final_info = []
                final_info.append(info[0] - start_time)
                final_info.append(info[1])
                pos = [info[2][0] - start_pos[0], info[2][1] - start_pos[1], info[2][2] - start_pos[2]]
                if USE_FLOAT_REDUCE:
                    pos = fl_reduce.i3_to_f3(*pos)
                final_info.append(pos)
                val = info[3]
                if USE_FLOAT_REDUCE:
                    val = fl_reduce.i3_to_f3(*val)
                final_info.append(val)
                final_info.append(info[4])
                final_record.append(final_info)

            self._sync_record = []

    def _on_water_status(self, last_status, water_height):
        if last_status > water_const.WATER_MID_LEVEL:
            self._on_ground()

    def _on_clear_trigger(self):
        self._trigger.restart()

    def _adjust_roll_back_pos(self, v3d_pos):
        return v3d_pos

    def _try_do_rb_pos(self):
        rb_info = self.ev_g_rb_info()
        if not rb_info:
            return
        rb_pos, reason = rb_info
        self._on_roll_back_pos(rb_pos, reason)

    def _on_roll_back_pos(self, lst_pos, i_reason=None):
        if i_reason and i_reason in STUCK_REASON:
            self.send_event('E_VERTICAL_SPEED', 0)
            self.send_event('E_CHARACTER_WALK', math3d.vector(0, 0, 0))
        v3d_pos = math3d.vector(*lst_pos)
        if i_reason != TRY_TELE_POS_REASON_NORMAL:
            v3d_pos = self._adjust_roll_back_pos(v3d_pos)
        if self.ev_g_is_character_active() and self.ev_g_get_state(ST_SWIM):
            if self.ev_g_check_is_in_water(up_offset=15 * NEOX_UNIT_SCALE, query_pos=v3d_pos):
                self.send_event('E_UNLIMIT_HEIGHT')
                self.send_event('E_UNLIMIT_LOWER_HEIGHT')
            else:
                self.send_event('E_STOP_SWIM')
        chect_begin = math3d.vector(v3d_pos)
        if self.unit_obj.__class__.__name__ == 'LMotorcycle':
            v3d_pos.y = v3d_pos.y + 15
        chect_begin = chect_begin + math3d.vector(0, 0.1 * NEOX_UNIT_SCALE, 0)
        check_end = math3d.vector(chect_begin)
        check_end = check_end + math3d.vector(0, -2 * NEOX_UNIT_SCALE, 0)
        hit_point_list = []
        is_hit = self.ev_g_hit_by_scene_collision(chect_begin, check_end, is_multi_select=False, hit_point_list=hit_point_list)
        if is_hit and hit_point_list:
            hit_position = hit_point_list[0]
            if hit_position.y > v3d_pos.y:
                v3d_pos.y = hit_position.y + 0.2 * NEOX_UNIT_SCALE
        self.send_event('E_FOOT_POSITION_BY_SYNC', v3d_pos)
        self._on_pos_force_set(v3d_pos)
        self.last_roll_back_log = (
         global_data.game_time, v3d_pos, i_reason, self.scene.active_camera.world_position)
        self.send_event('E_ON_RB_DONE')
        self.send_event('E_CALL_SYNC_METHOD', 'rb_state', (0, ), True, True, False)
        move_state = self.ev_g_move_state()
        if move_state != animation_const.MOVE_STATE_STAND:
            self.send_event('E_CALL_SYNC_METHOD', 'sync_move_state', (move_state,), True)
        if self.ev_g_is_character_active() and self.ev_g_get_state(ST_SWIM):
            foot_position = self.ev_g_foot_position()
            water_height = self.ev_g_water_height()
            if foot_position.y <= water_height:
                self.send_event('E_START_SWIM', water_height)

    def get_rb_pos_log(self):
        return self.last_roll_back_log

    def _on_char_deactive(self):
        self.set_enable(False)

    def _on_char_active(self, *args, **kwargs):
        self.set_enable(True)

    def _on_pos_force_set(self, pos):
        self._trigger.clear_pos()
        self._trigger.input('pos', pos)

    def get_ctrl_pos(self):
        if self._mode == SENDER_MODE_NORMAL:
            char_ctrl = self.sd.ref_character
            if not char_ctrl or not char_ctrl.isActive():
                return None
            return char_ctrl.position
        else:
            if self._mode == SENDER_MODE_BALL_CTRL:
                ball_ctrl = self.sd.ref_ball_driver
                pos = ball_ctrl and ball_ctrl.position
                return pos
            if self._mode == SENDER_MODE_ROTATION_ONLY:
                return self.ev_g_position()
            char_ctrl = self.sd.ref_character
            if not char_ctrl or not char_ctrl.isActive():
                return None
            return char_ctrl.position
            return None

    def get_ctrl_velocity(self, stop_y=False):
        if self._mode == SENDER_MODE_NORMAL:
            char_ctrl = self.sd.ref_character
            if not char_ctrl or not char_ctrl.isActive():
                return None
            velocity = char_ctrl.getWalkDirection()
            vel_y = char_ctrl.verticalVelocity
        elif self._mode == SENDER_MODE_PARACHUTE_SIMULATE_FOLLOWING:
            velocity = self.sd.ref_parachute_follow_velocity
            vel_y = velocity.y
        else:
            ball_ctrl = self.sd.ref_ball_driver
            if not ball_ctrl:
                return None
            velocity = ball_ctrl.linear_velocity
            vel_y = velocity.y
        if velocity.length > 50000:
            return None
        else:
            return math3d.vector(velocity.x, 0 if stop_y is None else vel_y, velocity.z)

    def _on_pos_change(self, pos, force=False):
        if org_time.time() - self._t_last_accept < 0.03:
            return
        if pos == self._cache_pos and not force:
            return
        self._cache_pos = pos
        self._t_last_accept = org_time.time()
        velocity = self.get_ctrl_velocity()
        if not velocity:
            return
        if velocity.is_zero:
            self._trigger.input('stop', pos)
        else:
            self._trigger.input('pos', pos, vel=velocity)
        if self._next_jump and velocity.y:
            self._on_action_acc()
            self._trigger.input('v_y', velocity.y / 1.1)
            self._next_jump = False

    def _v_stop(self):
        if not self._enable_initiative_stop:
            return
        pos = self.get_ctrl_pos()
        if not pos:
            return
        self._trigger.input('stop', pos)

    def _jump_change(self, i_state):
        if i_state != animation_const.JUMP_STATE_IN_AIR:
            return
        self._next_jump = True

    def _on_check_pos(self, stop=False, force=False):
        cur_pos = self._trigger.get_cur_pos()
        pos = self.get_ctrl_pos()
        if not pos:
            return
        if cur_pos and pos != cur_pos:
            if stop:
                self._trigger.force_pos_stop(pos)
            else:
                self._on_pos_change(pos, force)

    def _on_action_acc(self, acc=None):
        if acc is None:
            char_ctrl = self.sd.ref_character
            acc_y = 0 - char_ctrl.getGravity()
        else:
            acc_y = acc
        self._trigger.input('acc', math3d.vector(0, acc_y, 0))
        return

    def _on_action_vel(self, v3d_vel):
        self._trigger.input('vel', v3d_vel)

    def _on_action_attr(self, key, val):
        self.send_event('E_CALL_SYNC_METHOD', 'action_sync_attr', (key, val), False)

    def _on_jump_state_change(self, i_jump_state, *args):
        self._i_jump_state = i_jump_state

    def on_vel_slow(self):
        self._move_forward(self._cur_forward)

    def _move_action_stop(self, *args):
        self._last_forward = math3d.vector(0, 0, 0)

    def _move_forward(self, *args):
        if not self.is_unit_obj_type('LAvatar') or not self._last_vel:
            return
        v_dir = args[0]
        self._cur_forward = v_dir
        l = self._last_vel.length
        diff = v_dir - self._last_forward
        status_need = self._i_status in (animation_const.STATE_STAND, animation_const.STATE_SWIM)
        if not status_need:
            return
        if diff.length < 0.3:
            return
        if l > 5.0:
            return
        lst_dir = (
         v_dir.x, v_dir.y, v_dir.z)
        self.send_event('E_CALL_SYNC_METHOD', 'action_sync_forawrd', (lst_dir,), False)
        self._last_forward = v_dir

    def _on_parachute_state_changed(self, stage):
        from logic.gcommon.common_utils import parachute_utils
        if stage in (parachute_utils.STAGE_PARACHUTE_DROP, parachute_utils.STAGE_LAND):
            self._t_last_parachute_drop = t_util.time()

    def is_drop_protected(self):
        t = t_util.time()
        if t < self._t_last_parachute_drop + T_LOCK_NO_DROP_DMG:
            return True
        attaches = self.ev_g_all_attachable()
        if attaches:
            return True
        return False

    def _on_ground(self, f_vert_vel=None, specific_jump_type=None):
        if self.is_drop_protected():
            f_vert_vel = 0
        pos = self.get_ctrl_pos()
        if not pos:
            return
        velocity = self.get_ctrl_velocity(True)
        if not velocity:
            return
        self._trigger.input('acc', math3d.vector(0, 0, 0), tri=False)
        self._trigger.input('pos', pos, True, vel=velocity)
        self.send_event('E_CALL_SYNC_METHOD', 'on_ground', (f_vert_vel, specific_jump_type), True)

    def on_character_recreate(self, *args):
        pass

    def _switch_status(self, i_status):
        self._i_status = i_status
        self.send_event('E_CALL_SYNC_METHOD', 'swt_act_st', (i_status,), True)

    def _dt_f_yaw(self, f_yaw):
        pass

    def _on_force_yaw(self, f_yaw):
        self.send_event('E_CALL_SYNC_METHOD', 'force_yaw', (f_yaw,), True, False, True)

    def _dt_f_head_pitch(self, *args):
        f_head_pitch = self.ev_g_cam_pitch() or 0
        self._trigger.input('head_pitch', f_head_pitch)

    def on_trigger_ask_pos(self):
        if not self._enable_ask:
            return
        is_jump = self.ev_g_is_jump()
        if is_jump:
            return
        pos = self.get_ctrl_pos()
        if not pos:
            return
        velocity = self.get_ctrl_velocity()
        self._trigger.input('pos', pos, vel=velocity)

    def on_trigger_all(self, v3d_pos, v3d_vel, v3d_acc):
        if not v3d_pos or not self._enable:
            return
        else:
            v3d_pos, v3d_vel, v3d_acc = self.filter_status(v3d_pos, v3d_vel, v3d_acc)
            if v3d_pos is None:
                return
            lst_pos = (
             v3d_pos.x, v3d_pos.y, v3d_pos.z)
            lst_vel = (v3d_vel.x, v3d_vel.y, v3d_vel.z)
            if USE_FLOAT_REDUCE:
                lst_pos = fl_reduce.f3_to_i3(*lst_pos)
                lst_vel = fl_reduce.f3_to_i3(*lst_vel)
            acc = v3d_acc.y
            if self._enable_param:
                self.send_event('E_CALL_SYNC_METHOD', 'update_robot_mecha_info', (self.ev_g_sync_ai_param(),))
            self.sync_walking()
            now = org_time.time()
            dt = 0 if self._last_time is None else fl_reduce.f1_to_i(now - self._last_time)
            args = (t_util.time(), lst_pos, lst_vel, acc, dt)
            self.send_event('E_CALL_SYNC_METHOD', 'move_sync_all', args)
            self.sync_rel_info(lst_vel)
            if self._enable_record:
                self._sync_record.append([t_util.time(), 0, lst_pos, lst_vel, acc])
            if self._last_vel and v3d_vel.length < VEL_MOVE_FORWARD_SEND and self._last_vel.length > VEL_MOVE_FORWARD_SEND:
                self.on_vel_slow()
            self._last_pos = v3d_pos
            self._last_vel = v3d_vel
            self._last_acc = v3d_acc
            self._last_time = now
            return

    def sync_rel_info(self, vel):
        if global_data.carry_mgr.have_base_ent() and global_data.ctrl_target_id == self.unit_obj.id:
            rel_ent_id, v3d_rel_pos = global_data.carry_mgr.player_rel_info
            lst_rel_pos = None
            if rel_ent_id:
                lst_rel_pos = (
                 v3d_rel_pos.x, v3d_rel_pos.y, v3d_rel_pos.z)
                if USE_FLOAT_REDUCE:
                    lst_rel_pos = fl_reduce.f3_to_i3(*lst_rel_pos)
            if self._do_none_sync or lst_rel_pos:
                args = (
                 t_util.time(), rel_ent_id, lst_rel_pos, vel)
                self.send_event('E_CALL_SYNC_METHOD', 'move_sync_rel', args)
            self._do_none_sync = True if lst_rel_pos else False
        return

    def sync_walking(self):
        if not self._walk_st:
            return
        cur_state = self.ev_g_get_all_state()
        flag = bool(cur_state & self._walk_st)
        self.send_event('E_CALL_SYNC_METHOD', 'action_walk', (flag,))

    def filter_status(self, v3d_pos, v3d_vel, v3d_acc):
        if self._i_status == animation_const.STATE_CLIMB:
            if self._climb_type is not None:
                return (None, None, None)
            if self._last_pos and (v3d_pos - self._last_pos).length < 5.0 and not v3d_vel.is_zero and not v3d_acc.is_zero:
                return (None, None, None)
            MAX_CLIMB_VEL_Y = 2.5 * NEOX_UNIT_SCALE
            MAX_CLIMB_VEL_FORWARD = 2.0 * NEOX_UNIT_SCALE
            hori_vel = math3d.vector(v3d_vel.x, 0, v3d_vel.z)
            if v3d_vel.y != 0 and abs(v3d_vel.y) > MAX_CLIMB_VEL_Y:
                vel_y = MAX_CLIMB_VEL_Y * (v3d_vel.y / abs(v3d_vel.y))
            else:
                vel_y = v3d_vel.y
            if hori_vel.length > MAX_CLIMB_VEL_FORWARD:
                hori_vel *= MAX_CLIMB_VEL_FORWARD / hori_vel.length
            v3d_vel = hori_vel + math3d.vector(0, vel_y, 0)
        if self._last_pos:
            if self._last_vel == v3d_vel and self._last_acc == v3d_acc and v3d_vel.length < 0.2 and v3d_acc.is_zero and (v3d_pos - self._last_pos).length < 1.0:
                return (None, None, None)
        return (
         v3d_pos, v3d_vel, v3d_acc)

    def on_trigger_yaw(self, f_dt, f_yaw):
        self._enable_sync_yaw and self.send_event('E_CALL_SYNC_METHOD', 'acc_yaw', (f_yaw, f_dt), True, True, False)

    def on_trigger_head_pitch(self, f_head_pitch):
        self.send_event('E_CALL_SYNC_METHOD', 'trigger_head_pitch', (f_head_pitch,), True, True, False)

    def _refresh_enable_sync_yaw(self):
        self._enable_sync_yaw = self._mode in (SENDER_MODE_NORMAL, SENDER_MODE_ROTATION_ONLY)

    def _on_active_mode(self, mode):
        self._mode = mode
        self._refresh_enable_sync_yaw()
        self._on_clear_trigger()

    def _enable_parachute_simulate_following(self, flag):
        self._mode = SENDER_MODE_PARACHUTE_SIMULATE_FOLLOWING if flag else SENDER_MODE_NORMAL
        self._refresh_enable_sync_yaw()

    def update_network_delay(self, rtt_type, rtt):
        if rtt_type != t_util.TYPE_BATTLE:
            return
        self._rtt = rtt
        self.send_event('E_CALL_SYNC_METHOD', 'sync_rtt', (rtt, t_util.g_stamp_delta_battle))