# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComMoveSyncSender.py
from __future__ import absolute_import
from ..UnitCom import UnitCom
from logic.gcommon import time_utility as t_util
import math3d
import world
import collision
from ..component_const import ACC_F_YAW, ACC_V_DIR, ACC_F_PITCH, ITVL_FRAME, T_PREDICT, ACC_F_CAM_YAW, ACC_F_CAM_PITCH
from ..component_const import MAX_ITVL_TICK_SYNC, ITVL_MIX_FRAME_YAW, ITVL_TICK_SYNC

def __check__yaw--- This code section failed: ---

  52       0  LOAD_GLOBAL           0  't_util'
           3  LOAD_ATTR             1  'time'
           6  CALL_FUNCTION_0       0 
           9  STORE_FAST            2  't'

  55      12  LOAD_FAST             0  'mp_state'
          15  LOAD_ATTR             2  'get'
          18  LOAD_CONST            1  't_pre_yaw'
          21  LOAD_CONST            2  ''
          24  CALL_FUNCTION_2       2 
          27  STORE_FAST            3  't_pre_yaw'

  57      30  LOAD_FAST             2  't'
          33  LOAD_FAST             3  't_pre_yaw'
          36  LOAD_GLOBAL           3  'ITVL_MIX_FRAME_YAW'
          39  BINARY_ADD       
          40  COMPARE_OP            0  '<'
          43  POP_JUMP_IF_FALSE    50  'to 50'

  58      46  LOAD_CONST            5  (0, 0)
          49  RETURN_END_IF    
        50_0  COME_FROM                '43'

  60      50  LOAD_FAST             2  't'
          53  LOAD_FAST             1  'mp_cache'
          56  STORE_SUBSCR     

  62      57  LOAD_GLOBAL           4  'abs'
          60  LOAD_FAST             1  'mp_cache'
          63  LOAD_GLOBAL           5  'ACC_F_YAW'
          66  BINARY_SUBSCR    
          67  CALL_FUNCTION_1       1 
          70  LOAD_CONST            3  0.1
          73  COMPARE_OP            4  '>'
          76  POP_JUMP_IF_FALSE    83  'to 83'

  63      79  LOAD_CONST            6  (1, 1)
          82  RETURN_END_IF    
        83_0  COME_FROM                '76'

  65      83  LOAD_CONST            7  (0, 0)
          86  RETURN_VALUE     
          -1  RETURN_LAST      

Parse error at or near `STORE_SUBSCR' instruction at offset 56


def __check__pitch--- This code section failed: ---

  70       0  LOAD_GLOBAL           0  't_util'
           3  LOAD_ATTR             1  'time'
           6  CALL_FUNCTION_0       0 
           9  STORE_FAST            2  't'

  73      12  LOAD_FAST             0  'mp_state'
          15  LOAD_ATTR             2  'get'
          18  LOAD_CONST            1  't_pre_pitch'
          21  LOAD_CONST            2  ''
          24  CALL_FUNCTION_2       2 
          27  STORE_FAST            3  't_pre_pitch'

  75      30  LOAD_FAST             2  't'
          33  LOAD_FAST             3  't_pre_pitch'
          36  LOAD_GLOBAL           3  'ITVL_MIX_FRAME_YAW'
          39  BINARY_ADD       
          40  COMPARE_OP            0  '<'
          43  POP_JUMP_IF_FALSE    50  'to 50'

  76      46  LOAD_CONST            5  (0, 0)
          49  RETURN_END_IF    
        50_0  COME_FROM                '43'

  78      50  LOAD_FAST             2  't'
          53  LOAD_FAST             1  'mp_cache'
          56  STORE_SUBSCR     

  80      57  LOAD_GLOBAL           4  'abs'
          60  LOAD_FAST             1  'mp_cache'
          63  LOAD_GLOBAL           5  'ACC_F_PITCH'
          66  BINARY_SUBSCR    
          67  CALL_FUNCTION_1       1 
          70  LOAD_CONST            3  0.1
          73  COMPARE_OP            4  '>'
          76  POP_JUMP_IF_FALSE    83  'to 83'

  81      79  LOAD_CONST            6  (1, 1)
          82  RETURN_END_IF    
        83_0  COME_FROM                '76'

  83      83  LOAD_CONST            7  (0, 0)
          86  RETURN_VALUE     
          -1  RETURN_LAST      

Parse error at or near `STORE_SUBSCR' instruction at offset 56


def __check__dir--- This code section failed: ---

  91       0  LOAD_GLOBAL           0  't_util'
           3  LOAD_ATTR             1  'time'
           6  CALL_FUNCTION_0       0 
           9  STORE_FAST            2  't'

  93      12  LOAD_FAST             0  'mp_state'
          15  LOAD_ATTR             2  'get'
          18  LOAD_CONST            1  't_pre_dir'
          21  LOAD_CONST            2  ''
          24  CALL_FUNCTION_2       2 
          27  STORE_FAST            3  't_pre_dir'

  95      30  LOAD_FAST             2  't'
          33  LOAD_FAST             3  't_pre_dir'
          36  LOAD_GLOBAL           3  'ITVL_MIX_FRAME_YAW'
          39  BINARY_ADD       
          40  COMPARE_OP            0  '<'
          43  POP_JUMP_IF_FALSE    50  'to 50'

  96      46  LOAD_CONST            8  (0, 0)
          49  RETURN_END_IF    
        50_0  COME_FROM                '43'

  98      50  LOAD_FAST             2  't'
          53  LOAD_FAST             1  'mp_cache'
          56  STORE_SUBSCR     

 100      57  LOAD_FAST             1  'mp_cache'
          60  LOAD_GLOBAL           4  'ACC_V_DIR'
          63  BINARY_SUBSCR    
          64  STORE_FAST            4  'arr_dirs'

 101      67  LOAD_FAST             4  'arr_dirs'
          70  LOAD_CONST            2  ''
          73  BINARY_SUBSCR    
          74  STORE_FAST            5  'first'

 102      77  LOAD_FAST             1  'mp_cache'
          80  LOAD_ATTR             2  'get'
          83  LOAD_CONST            3  'pre_dir'
          86  LOAD_GLOBAL           5  'math3d'
          89  LOAD_ATTR             6  'vector'
          92  LOAD_CONST            2  ''
          95  LOAD_CONST            2  ''
          98  LOAD_CONST            2  ''
         101  CALL_FUNCTION_3       3 
         104  CALL_FUNCTION_2       2 
         107  STORE_FAST            6  'pre_dir'

 103     110  LOAD_FAST             1  'mp_cache'
         113  LOAD_ATTR             2  'get'
         116  LOAD_CONST            4  'delta'
         119  LOAD_GLOBAL           5  'math3d'
         122  LOAD_ATTR             6  'vector'
         125  LOAD_CONST            2  ''
         128  LOAD_CONST            2  ''
         131  LOAD_CONST            2  ''
         134  CALL_FUNCTION_3       3 
         137  CALL_FUNCTION_2       2 
         140  STORE_FAST            7  'delta'

 104     143  LOAD_GLOBAL           7  'len'
         146  LOAD_FAST             4  'arr_dirs'
         149  CALL_FUNCTION_1       1 
         152  STORE_FAST            8  'l'

 106     155  LOAD_FAST             5  'first'
         158  LOAD_ATTR             8  'length'
         161  LOAD_CONST            5  5.0
         164  COMPARE_OP            4  '>'
         167  POP_JUMP_IF_FALSE   174  'to 174'

 107     170  LOAD_CONST            9  (1, 1)
         173  RETURN_END_IF    
       174_0  COME_FROM                '167'

 109     174  LOAD_FAST             8  'l'
         177  LOAD_CONST            7  2
         180  COMPARE_OP            0  '<'
         183  POP_JUMP_IF_FALSE   190  'to 190'

 111     186  LOAD_CONST           10  (1, 1)
         189  RETURN_END_IF    
       190_0  COME_FROM                '183'

 115     190  LOAD_CONST           11  (1, 1)
         193  RETURN_VALUE     
          -1  RETURN_LAST      

Parse error at or near `STORE_SUBSCR' instruction at offset 56


MP_ACC_ZERO = {ACC_F_YAW: 0.0,
   ACC_F_PITCH: 0.0,
   ACC_V_DIR: []}

def get_zero--- This code section failed: ---

 128       0  LOAD_GLOBAL           0  'MP_ACC_ZERO'
           3  LOAD_ATTR             1  'get'
           6  LOAD_ATTR             1  'get'
           9  CALL_FUNCTION_2       2 
          12  RETURN_VALUE     
          -1  RETURN_LAST      

Parse error at or near `CALL_FUNCTION_2' instruction at offset 9


def acc_check_func--- This code section failed: ---

 133       0  BUILD_MAP_3           3 

 134       3  LOAD_GLOBAL           0  '__check__yaw'
           6  LOAD_GLOBAL           1  'ACC_F_YAW'
           9  STORE_MAP        

 135      10  LOAD_GLOBAL           2  '__check__pitch'
          13  LOAD_GLOBAL           3  'ACC_F_PITCH'
          16  STORE_MAP        

 136      17  LOAD_GLOBAL           4  '__check__dir'
          20  LOAD_GLOBAL           5  'ACC_V_DIR'
          23  STORE_MAP        
          24  STORE_FAST            1  'mp_acc_func'

 138      27  LOAD_FAST             1  'mp_acc_func'
          30  LOAD_ATTR             6  'get'
          33  LOAD_ATTR             1  'ACC_F_YAW'
          36  MAKE_FUNCTION_0       0 
          39  CALL_FUNCTION_2       2 
          42  RETURN_VALUE     
          -1  RETURN_LAST      

Parse error at or near `MAKE_FUNCTION_0' instruction at offset 36


def check_acc(acc_type, mp_state, mp_cache):
    f = acc_check_func(acc_type)
    return f(mp_state, mp_cache)


def pack_acc_val(acc_type, val):
    pass


class ComMoveSyncSender(UnitCom):
    BIND_EVENT = {'E_ACTION_SYNC_YAW': '_dt_f_yaw',
       'E_ACTION_SYNC_HEAD_PITCH': '_dt_f_head_pitch',
       'E_ACTION_SYNC_DIR': '_v_dir',
       'E_ACTION_SYNC_STOP': '_v_stop',
       'E_ACTION_SYNC_STATUS': '_switch_status',
       'E_ACTION_SYNC_JUMP': '_sync_jump',
       'E_ACTION_SYNC_RB_POS': '_on_roll_back_pos',
       'E_STAND': ('_e_stand', 999),
       'E_SQUAT': ('_e_squat', 999),
       'E_GROUND': ('_e_ground', 999),
       'E_DEATH': '_on_death'
       }

    def __init__(self):
        super(ComMoveSyncSender, self).__init__(need_update=True)
        self._enable = False
        self._pre_tick = 0
        self._dy_itvl_sync_all = ITVL_TICK_SYNC
        self._stop = 0
        self.cache_accumulate = MP_ACC_ZERO.copy()
        self.mp_state = {}
        self._draw_rect = []
        self._last_pred_pos = None
        self._last_dir = None
        self._last_yaw = None
        self._last_pitch = None
        return

    def init_cache(self):
        self.cache_accumulate = MP_ACC_ZERO.copy()

    def init_from_dict(self, unit_obj, bdict):
        super(ComMoveSyncSender, self).init_from_dict(unit_obj, bdict)

    def destroy(self):
        super(ComMoveSyncSender, self).destroy()

    def tick(self, dt):
        if not self._enable:
            return
        now = t_util.time()
        if now > self._pre_tick + self._dy_itvl_sync_all:
            self.send_all(from_tick=True)
        self.tick_cache()

    def tick_cache(self):
        pass

    def set_enable(self, enable):
        self._enable = enable

    def _dt_f_yaw(self, yaw):
        self.cache_accumulate[ACC_F_YAW] += yaw
        send, push = check_acc(ACC_F_YAW, self.mp_state, self.cache_accumulate)
        if push:
            self.send_all()
            return
        if not send:
            return
        self.send_acc_type(ACC_F_YAW)

    def _dt_f_head_pitch(self, pitch):
        self.cache_accumulate[ACC_F_PITCH] += pitch
        send, push = check_acc(ACC_F_PITCH, self.mp_state, self.cache_accumulate)
        if push:
            self.send_all()
            return
        if not send:
            return
        self.send_acc_type(ACC_F_PITCH)

    def _v_dir(self, v_dir):
        self.set_enable(True)
        v_dir = self.ev_g_rotation()
        if v_dir.is_zero:
            return
        self._stop = 0
        self.cache_accumulate[ACC_V_DIR] += [v_dir]
        send, push = check_acc(ACC_V_DIR, self.mp_state, self.cache_accumulate)
        if push:
            self.send_all()
            return
        if not send:
            return
        self.send_acc_type(ACC_V_DIR)

    def _v_stop(self, v_dir=math3d.vector(0, 0, 0)):
        self.set_enable(True)
        self._stop = 1
        self.send_all()

    def _switch_status(self, status):
        self.do_sync_status(status)

    def _sync_jump(self, jump_state):
        self.do_sync_jump(jump_state)

    def draw_rect_at_pos(self, arr_pos):
        for obj in self._draw_rect:
            obj.destroy()

        self._draw_rect = []
        scn = world.get_active_scene()
        arr_color = [
         16711680, 65280, 255]
        for i, v3d_pos in enumerate(arr_pos):
            if not v3d_pos:
                continue
            obj = world.primitives(scn)
            l = 8
            p1 = v3d_pos + math3d.vector(l, 0, 0)
            p2 = v3d_pos + math3d.vector(0, 0, -l)
            p3 = v3d_pos + math3d.vector(-l, 0, 0)
            p4 = v3d_pos + math3d.vector(0, 0, l)
            obj.create_poly4([((p1,), (p2,), (p3,), (p4,), arr_color[i % 3])])
            self._draw_rect.append(obj)

    def get_predict_pos(self):
        cur_pos = self.ev_g_position()
        world_dir = self.ev_g_rotation()
        if not world_dir:
            return cur_pos
        if self._stop or world_dir.is_zero:
            return cur_pos
        pred_pos = world_dir * MAX_ITVL_TICK_SYNC + cur_pos
        scn = world.get_active_scene()
        hit, point, normal, fraction, color, objs = scn.scene_col.hit_by_ray(cur_pos, pred_pos)
        if hit:
            len_0 = (pred_pos - cur_pos).length
            len_1 = (point - cur_pos).length
            if len_0 != 0:
                proportion = len_1 / float(len_0)
            else:
                proportion = 0
            return (point, proportion)
        return pred_pos

    def do_sync_jump(self, jump_state):
        self.send_event('E_CALL_SYNC_METHOD', 'mv_act_jump', (jump_state,), True)

    def do_sync_status(self, status):
        self.send_event('E_CALL_SYNC_METHOD', 'swt_act_st', (status,), True)

    def do_sync_dir(self, pred_pos, world_dir, proportion):
        if pred_pos is None or world_dir is None:
            return
        else:
            if self._last_pred_pos and (pred_pos - self._last_pred_pos).length < 0.05:
                return
            args = (
             t_util.time(),
             (
              pred_pos.x, pred_pos.y, pred_pos.z),
             (
              world_dir.x, proportion, world_dir.z))
            self._last_pred_pos = pred_pos
            self._last_dir = world_dir
            self.send_event('E_CALL_SYNC_METHOD', 'acc_dir', args, True, True, False)
            return

    def do_sync_yaw(self, f_yaw):
        if f_yaw == self._last_yaw:
            return
        self._last_yaw = f_yaw
        self.send_event('E_CALL_SYNC_METHOD', 'acc_yaw', (f_yaw,), True, True, False)

    def do_sync_pitch(self, f_pitch):
        if f_pitch == self._last_pitch:
            return
        self._last_pitch = f_pitch
        self.send_event('E_CALL_SYNC_METHOD', 'trigger_head_pitch', (f_pitch,), True, True, False)

    def try_sync_dir(self, from_tick=False):
        pred_pos = self.get_predict_pos()
        if pred_pos is None:
            return
        else:
            if type(pred_pos) is tuple:
                proportion = pred_pos[1]
                pred_pos = pred_pos[0]
            else:
                proportion = 1.0
            world_dir = self.ev_g_rotation()
            if world_dir is None:
                return
            cur_pos = self.ev_g_position()
            if pred_pos == cur_pos:
                world_dir = math3d.vector(0, 0, 0)
            if not from_tick or cur_pos != pred_pos:
                self.do_sync_dir(pred_pos, world_dir, proportion)
            return

    def send_all(self, from_tick=False):
        self._pre_tick = t_util.time()
        self.try_sync_dir(from_tick=from_tick)
        f_yaw = self.ev_g_yaw()
        self.do_sync_yaw(f_yaw)
        f_pitch = self.ev_g_cam_pitch()
        self.do_sync_pitch(f_pitch)
        world_dir = self.ev_g_rotation()
        if not world_dir:
            return
        if world_dir.length < 0.0001:
            self._dy_itvl_sync_all = ITVL_TICK_SYNC * 10
        elif world_dir.length < 10:
            self._dy_itvl_sync_all = ITVL_TICK_SYNC * 4
        else:
            self._dy_itvl_sync_all = ITVL_TICK_SYNC
        self.init_cache()

    def send_acc_type(self, acc_type):
        val = self.cache_accumulate.get(acc_type)
        self.cache_accumulate = get_zero(acc_type)

    def _on_roll_back_pos(self, lst_pos, i_reason=None):
        v3d_pos = math3d.vector(*lst_pos)
        self.send_event('E_FOOT_POSITION', v3d_pos)
        self.send_event('E_CALL_SYNC_METHOD', 'rb_state', (0, ), True, True, False)

    def _on_roll_back(self, rb_data):
        pass

    def _e_stand(self):
        pass

    def _e_squat(self):
        pass

    def _e_ground(self):
        self.try_sync_dir()

    def _on_death(self, *arg):
        self.need_update = False