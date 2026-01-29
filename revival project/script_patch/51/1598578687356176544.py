# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gutils/sync/SyncTrigger.py
from __future__ import absolute_import
from __future__ import print_function
from logic.gcommon import time_utility as time
from .SimulateBox import SimulateBox
from .TriggerBox import TriggerBox
from .TriggerBoxCam import TriggerBoxCam
import math3d
from logic.gcommon.common_const.sync_const import MAX_ITVL_SILENT
from logic.gcommon.const import NEOX_UNIT_SCALE
from logic.gcommon.common_const.battle_const import MOVE_LENGTH_LIMIT
from logic.gcommon.common_const import battle_const
import logic.gcommon.common_utils.float_reduce_util as fl_reduce
DEBUG = 1
ITVL_CHECK_TRIGGER = 0.2
DT_WIN_DEFAULT = 0.05
DT_WIN_MID = 0.3
DT_WIN_LARGE = 0.5
VEL_SUDDENLY_CHANGE = 1.0 * NEOX_UNIT_SCALE

def default_callback(*args, **argv):
    print('--- default_callback', args, argv)


class SyncTrigger(object):
    CNT_ASK = 5

    def __init__(self):
        super(SyncTrigger, self).__init__()
        self._enable = True
        self._cur_vel = math3d.vector(0, 0, 0)
        self._cur_acc = math3d.vector(0, 0, 0)
        self._cur_yaw = 0
        self._cur_pitch = 0
        self._cur_t = time.time()
        self._t_last_all = 0
        self._pre_tri_all = None
        self._tp_agl = None
        self._tp_pos = None
        self._tp_yaw = None
        self._tp_pitch = None
        self.dt_win = DT_WIN_DEFAULT
        self.ask_cnt = 0
        self.handle = {'vel': default_callback,
           'acc': default_callback,
           'agl': default_callback,
           'v_y': default_callback,
           'all': default_callback,
           'yaw': default_callback,
           'pitch': default_callback,
           'head_pitch': default_callback,
           'ask_pos': default_callback
           }
        self.handle_input = {'pos': self.input_pos,
           'acc': self.input_acc,
           'agl': self.input_agl,
           'vel': self.input_vel,
           'v_y': self.input_v_y,
           'yaw': self.input_yaw,
           'pitch': self.input_pitch,
           'head_pitch': self.input_head_pitch,
           'stop': self.input_stop
           }
        self._sim_ghost = SimulateBox()
        self._sim_real = SimulateBox()
        self._box_yaw = TriggerBoxCam(min_itvl=0.1, min_delta=0.1, max_stay=0.5)
        self._box_yaw.set_callback(self.on_tri_yaw)
        self._box_head_pitch = TriggerBox(min_itvl=0.2, min_delta=0.2, max_stay=0.5)
        self._box_head_pitch.set_callback(self.on_tri_head_pitch)
        self._box_pitch = TriggerBox(min_itvl=0.2, min_delta=0.2, max_stay=0.5)
        self._box_pitch.set_callback(self.on_tri_pitch)
        self._t_tri_yaw = 0
        self._t_tri_pitch = 0
        self._cache_diff = None
        self._upload_big_pos_err_cnt = 0
        return

    def destroy(self):
        self.handle = None
        self.handle_input = None
        self._box_yaw.destroy()
        self._box_yaw = None
        self._box_head_pitch.destroy()
        self._box_head_pitch = None
        self._box_pitch.destroy()
        self._box_pitch = None
        return

    def set_callback(self, key, func):
        self.handle[key] = func

    def cancel_callback(self, key):
        if key in self.handle:
            self.handle[key] = default_callback

    def get_vel(self):
        return self._cur_vel

    def get_acc(self):
        return self._cur_acc

    def get_cur_time(self):
        return self._cur_t

    def get_cur_pos(self):
        if self._tp_pos:
            return self._tp_pos[0]
        else:
            return None

    def set_enable(self, enable):
        self._enable = enable

    def restart(self):
        self.set_enable(True)
        self.clear_pos()

    def stop(self):
        self.set_enable(False)

    def set_collect_win(self, dt_win):
        self.dt_win = dt_win

    def error_input(self, data):
        log_error('[SyncTrigger] Error input : {}'.format(data))
        raise Exception('[SyncTrigger] Error input !!!')

    def input(self, key, data, *args, **kwargs):
        if not self._enable:
            return
        func = self.handle_input.get(key, self.error_input)
        func(data, *args, **kwargs)

    def clear_pos(self):
        self._tp_pos = None
        self._cur_vel = math3d.vector(0, 0, 0)
        self._cur_acc = math3d.vector(0, 0, 0)
        return

    def input_pos(self, v3d_pos, force=False, tri=True, vel=None):
        if not isinstance(v3d_pos, math3d.vector):
            log_error('SyncTrigger input_pos: invalid input - {}'.format(v3d_pos))
            return
        else:
            if not self.is_legal_pos(v3d_pos):
                return
            t = time.time()
            self._cur_t = t
            if self._tp_pos is None:
                self._tp_pos = (
                 v3d_pos, t)
                return
            v3d_delta = v3d_pos - self._tp_pos[0]
            t_delta = t - self._tp_pos[1]
            if v3d_delta.is_zero:
                if t_delta < 0.2:
                    self._cache_diff = 0.001
                    return
                if self._cur_acc.length == 0 or self._cur_vel.length == 0:
                    self._tp_pos = (
                     v3d_pos, t)
                    self.input_stop(v3d_pos)
                    return
            if vel:
                v3d_vel = vel
                if abs(v3d_vel.y) < 0.1 and t_delta > 0.0333:
                    v3d_vel.y = v3d_delta.y / t_delta
                v_diff_len = (v3d_vel - self._cur_vel).length
            elif t_delta > 0:
                v3d_vel = v3d_delta * (1.0 / t_delta)
                v_diff_len = (v3d_vel - self._cur_vel).length
            else:
                v3d_vel = self._cur_vel
                v_diff_len = 0
            if t_delta < self.dt_win and v_diff_len < VEL_SUDDENLY_CHANGE and not force:
                return
            self._tp_pos = (v3d_pos, t)
            self.input_vel(v3d_vel)
            return

    def check_vel_pass(self, v3d_vel, t_delta):
        a = (v3d_vel - self._cur_vel) * (1.0 / t_delta)
        if abs(a.y) > 500.0 or v3d_vel.y > 230.0:
            return False
        return True

    def input_acc(self, v3d_acc, force=False, tri=True):
        self._cur_acc = v3d_acc
        if tri:
            self.check_trigger()

    def input_vel(self, v3d_vel, force=False, tri=True):
        self._cur_vel = v3d_vel
        if self._tp_pos:
            self._tp_pos = (
             self._tp_pos[0], time.time())
        if tri:
            self.check_trigger()

    def input_v_y(self, y, tri=True):
        vel = self._cur_vel
        self._cur_vel = math3d.vector(vel.x, y, vel.z)
        if tri:
            self.check_trigger()

    def input_agl(self, v3d_agl):
        pass

    def input_yaw(self, f_yaw):
        t = time.time()
        self._box_yaw.input(t, f_yaw)

    def input_head_pitch(self, f_head_pitch):
        t = time.time()
        self._box_head_pitch.input(t, f_head_pitch)

    def input_pitch(self, f_pitch):
        t = time.time()
        self._box_pitch.input(t, f_pitch)

    def input_stop(self, v3d_pos):
        if not isinstance(v3d_pos, math3d.vector):
            log_error('SyncTrigger input_pos: invalid 2 input - {}'.format(v3d_pos))
            return
        if not self.is_legal_pos(v3d_pos):
            return
        if self._cur_vel == math3d.vector(0, 0, 0) and self._cur_acc == math3d.vector(0, 0, 0):
            if self._tp_pos and (v3d_pos - self._tp_pos[0]).length < 1:
                return
        self._cur_vel = math3d.vector(0, 0, 0)
        self._cur_acc = math3d.vector(0, 0, 0)
        self._tp_pos = (v3d_pos, time.time())
        self.tri_all()

    def force_pos_stop(self, v3d_pos):
        if not isinstance(v3d_pos, math3d.vector):
            log_error('SyncTrigger input_pos: invalid 3 input - {}'.format(v3d_pos))
            return
        if not self.is_legal_pos(v3d_pos):
            return
        self._cur_vel = math3d.vector(0, 0, 0)
        self._cur_acc = math3d.vector(0, 0, 0)
        self._tp_pos = (v3d_pos, time.time())
        self.tri_all()

    def refresh_acc(self):
        pass

    def refresh_agl(self):
        pass

    def is_moving(self):
        if not self._cur_vel.is_zero or not self._cur_acc.is_zero:
            return True
        return False

    def check_trigger(self):
        t_pred = 1.0
        t = self._cur_t
        if not self._tp_pos:
            return
        if self._t_last_all + MAX_ITVL_SILENT < t:
            self._sim_real.set_all(t, self._tp_pos[0], self._cur_vel, self._cur_acc)
            self._sim_ghost.set_all(t, self._tp_pos[0], self._cur_vel, self._cur_acc)
            self.tri_all()
            return
        sim_pos_gh = self._sim_ghost.get_sim_pos(t + t_pred)
        self._sim_real.set_all(t, self._tp_pos[0], self._cur_vel, self._cur_acc)
        sim_pos_rl = self._sim_real.get_sim_pos(t + t_pred)
        diff = (sim_pos_rl - sim_pos_gh).length
        if diff > 8.0:
            self._sim_ghost.set_all(t, self._tp_pos[0], self._cur_vel, self._cur_acc)
            self.tri_all()
        else:
            self._cache_diff = diff

    def trigger_vel_pred(self):
        pass

    def update_with_data(self, dt, data):
        if not self._enable:
            return
        t = global_data.game_time_wrapped
        self._box_yaw.input(t, data.yaw_head + data.yaw_offset, False)
        self.update(dt)

    def update(self, dt):
        if not self._enable or not self._tp_pos:
            return
        now = global_data.game_time_wrapped
        self._box_pitch.check_trigger(now)
        self._box_yaw.check_trigger(now)
        self._box_head_pitch.check_trigger(now)
        if not self._cur_vel.is_zero:
            if now - self._tp_pos[1] > 0.1 or self._cache_diff:
                self.tri_ask()
                return
        self.check_trigger()

    def tri_ask(self):
        self.ask_cnt += 1
        if self.ask_cnt >= self.CNT_ASK:
            self.ask_cnt = 0
            func_ask = self.handle['ask_pos']
            func_ask()

    def tri_all(self):
        tp_all = (
         self._tp_pos[0], self._cur_vel, self._cur_acc)
        if tp_all == self._pre_tri_all:
            return
        t = time.time()
        self.ask_cnt = 0
        self._t_last_all = t
        self._pre_tri_all = tp_all
        func_all = self.handle['all']
        func_all(*tp_all)

    def on_tri_yaw(self, t, f_yaw):
        func_yaw = self.handle['yaw']
        func_yaw(t, f_yaw)

    def on_tri_pitch(self, t, f_pitch):
        func_pitch = self.handle['pitch']
        func_pitch(f_pitch)

    def on_tri_head_pitch(self, t, f_head_pitch):
        func_pitch = self.handle['head_pitch']
        func_pitch(f_head_pitch)

    def is_legal_pos(self, v3d_pos):
        if not v3d_pos:
            return False
        if v3d_pos.length < MOVE_LENGTH_LIMIT:
            return True
        return False

    def test_draw(self):
        if self._cur_vel is None:
            return
        else:
            p1 = global_data.player.logic.ev_g_position()
            p2 = p1 + self._cur_vel * 2.0
            self.draw_line(p1, p2)
            return

    def draw_line--- This code section failed: ---

 503       0  LOAD_CONST            1  ''
           3  LOAD_CONST            0  ''
           6  IMPORT_NAME           0  'world'
           9  STORE_FAST            4  'world'

 504      12  LOAD_GLOBAL           1  'hasattr'
          15  LOAD_GLOBAL           2  'mp_draw'
          18  CALL_FUNCTION_2       2 
          21  POP_JUMP_IF_TRUE     36  'to 36'

 505      24  BUILD_MAP_0           0 
          27  LOAD_FAST             0  'self'
          30  STORE_ATTR            2  'mp_draw'
          33  JUMP_FORWARD          0  'to 36'
        36_0  COME_FROM                '33'

 507      36  LOAD_FAST             3  'tag'
          39  LOAD_FAST             0  'self'
          42  LOAD_ATTR             2  'mp_draw'
          45  COMPARE_OP            6  'in'
          48  POP_JUMP_IF_FALSE    87  'to 87'

 508      51  LOAD_FAST             0  'self'
          54  LOAD_ATTR             2  'mp_draw'
          57  LOAD_FAST             3  'tag'
          60  BINARY_SUBSCR    
          61  LOAD_ATTR             3  'destroy'
          64  CALL_FUNCTION_0       0 
          67  POP_TOP          

 509      68  LOAD_FAST             0  'self'
          71  LOAD_ATTR             2  'mp_draw'
          74  LOAD_ATTR             4  'pop'
          77  LOAD_FAST             3  'tag'
          80  CALL_FUNCTION_1       1 
          83  POP_TOP          
          84  JUMP_FORWARD          0  'to 87'
        87_0  COME_FROM                '84'

 511      87  LOAD_FAST             1  'start'
          90  UNARY_NOT        
          91  POP_JUMP_IF_TRUE    101  'to 101'
          94  LOAD_FAST             2  'end'
          97  UNARY_NOT        
        98_0  COME_FROM                '91'
          98  POP_JUMP_IF_FALSE   105  'to 105'

 512     101  LOAD_CONST            0  ''
         104  RETURN_END_IF    
       105_0  COME_FROM                '98'

 513     105  LOAD_FAST             4  'world'
         108  LOAD_ATTR             5  'get_active_scene'
         111  CALL_FUNCTION_0       0 
         114  STORE_FAST            5  'scene'

 514     117  LOAD_FAST             4  'world'
         120  LOAD_ATTR             6  'primitives'
         123  LOAD_FAST             5  'scene'
         126  CALL_FUNCTION_1       1 
         129  STORE_FAST            6  'obj'

 515     132  LOAD_FAST             6  'obj'
         135  LOAD_ATTR             7  'create_line'
         138  LOAD_FAST             1  'start'
         141  BUILD_TUPLE_1         1 
         144  LOAD_FAST             2  'end'
         147  BUILD_TUPLE_1         1 
         150  LOAD_CONST            3  65280
         153  BUILD_TUPLE_3         3 
         156  BUILD_LIST_1          1 
         159  CALL_FUNCTION_1       1 
         162  POP_TOP          

 517     163  LOAD_FAST             6  'obj'
         166  LOAD_FAST             0  'self'
         169  LOAD_ATTR             2  'mp_draw'
         172  LOAD_FAST             3  'tag'
         175  STORE_SUBSCR     

Parse error at or near `CALL_FUNCTION_2' instruction at offset 18