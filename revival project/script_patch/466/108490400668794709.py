# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComMoveSyncReceiver2.py
from __future__ import absolute_import
import six_ex
from ..UnitCom import UnitCom
from logic.gcommon import time_utility as t_util
import math3d
from ..component_const import MAX_ITVL_TICK_SYNC, ITVL_MIX_FRAME_PITCH, ITVL_MIX_FRAME_YAW
from logic.gcommon.common_const.sync_const import SYNC_ITPLER_NAME_EULER, SYNC_ITPLER_NAME_ROT
import math
from ...cdata import status_config
from logic.gcommon.const import NEOX_UNIT_SCALE
from logic.gutils.client_unit_tag_utils import register_unit_tag
from logic.gcommon.utility import dummy_cb
import exception_hook
MP_NAME_2_COM = {SYNC_ITPLER_NAME_EULER: ('ComMoveSyncEulerItpler', 'client'),
   SYNC_ITPLER_NAME_ROT: ('ComMoveSyncRotItpler', 'client')
   }
DRAW_ST_SHOW = 1
DRAW_ST_LAZY = 2
DRAW_ST_RESUME = 3
LAZY_TICK_ITVL = 10
RADIUS_LAZY = 20 * NEOX_UNIT_SCALE
RC_LOD_1 = NEOX_UNIT_SCALE * 25
RC_LOD_2 = NEOX_UNIT_SCALE * 60
RC_LOD_3 = NEOX_UNIT_SCALE * 100
g_has_post = False
NEED_HIGH_FRAME_TAG_VALUE = register_unit_tag(('LPuppet', 'LMecha'))

class ComMoveSyncReceiver2(UnitCom):
    BIND_EVENT = {'E_ACTION_SYNC_RC_ALL': '_on_sync_all',
       'E_ACTION_SYNC_RC_REL': '_on_sync_rel',
       'E_ACTION_SYNC_RC_TELEPORT': '_on_sync_teleport',
       'E_ON_CLEAR_BUFFER': '_on_clear_buffer',
       'E_ACTION_SYNC_RC_YAW': '_on_sync_yaw',
       'E_ACTION_SYNC_RC_HEAD_PITCH': '_on_sync_head_pitch',
       'E_ACTION_SYNC_RC_FORCE_YAW': '_on_rc_force_yaw',
       'E_SYNC_CLEAR_RECEIVER_POS': '_clear_pos',
       'G_SYNC_POSITION': '_get_sync_position',
       'E_ACTION_SYNC_FORWARD': '_move_action_forward',
       'E_ACTION_SYNC_RC_ATTR': '_on_action_sync_rc_attr',
       'G_ACTION_SYNC_ATTR': '_get_action_sync_attr',
       'E_SET_SYNC_RECEIVER_ENABLE': 'set_enable',
       'E_ACTION_SYNC_RC_RESUME_ROLL': '_on_action_sync_rc_resume_roll',
       'E_DEATH': '_on_death',
       'E_ON_BEING_OBSERVE': '_on_observe',
       'E_RC_OFFSET': '_on_rc_offset',
       'E_CLEAR_RC_OFFSET': '_on_clear_rc_offset',
       'E_PARACHUTE_STATUS_CHANGED': 'on_parachute_stage_changed',
       'E_ENABLE_PARACHUTE_SIMULATE_FOLLOWING': '_enable_parachute_simulate_following',
       'E_REFRESH_MOVE_TICK_METHOD': 'on_refresh_tick_method',
       'E_REFRESH_HIGH_FRAME_TICK_TIMER': 'on_refresh_high_frame_tick_timer',
       'G_SYNC_LOD_DIS': '_get_sync_lod_dis',
       'G_SPEED': 'on_get_speed',
       'G_GET_WALK_DIRECTION': 'get_walk_direction'
       }

    def __init__(self):
        super(ComMoveSyncReceiver2, self).__init__()
        self._enable = True
        self._run_tick = False
        self.need_high_frame = False
        self.high_frame_tick_timer = -1
        self.high_frame_tick_timer_refreshed = False
        self._to_yaw = None
        self.mp_itplers = {}
        self._last_forward = math3d.vector(0, 0, 0)
        self.sync_attr = {}
        self.idx_pos = 0
        self.idx_rel_pos = 0
        self._move_dir_cal_time = 0
        self._st_lazy = DRAW_ST_SHOW
        self._layz_cnt = LAZY_TICK_ITVL
        self._dis_2_cam = 0
        self._rc_off = None
        self._noti_pos = self._noti_pos_normal
        self._parachute_simulate_follow_enabled = False
        self._clear_pos()
        self._is_human = False
        return

    def init_from_dict(self, unit_obj, bdict):
        super(ComMoveSyncReceiver2, self).init_from_dict(unit_obj, bdict)
        self._is_human = unit_obj.__class__.__name__ == 'LPuppet'
        itpler_lst = [
         SYNC_ITPLER_NAME_EULER]
        self.set_enable_sync_itpler(itpler_lst)
        self.high_frame_tick_timer_refreshed = False

    def on_init_complete--- This code section failed: ---

 144       0  LOAD_FAST             0  'self'
           3  LOAD_ATTR             0  'ev_g_attr_get'
           6  LOAD_CONST            1  'rc_offset'
           9  LOAD_CONST            0  ''
          12  CALL_FUNCTION_2       2 
          15  STORE_FAST            1  '_rc_off'

 145      18  LOAD_FAST             1  '_rc_off'
          21  POP_JUMP_IF_FALSE    45  'to 45'

 146      24  LOAD_GLOBAL           2  'math3d'
          27  LOAD_ATTR             3  'vector'
          30  LOAD_FAST             1  '_rc_off'
          33  CALL_FUNCTION_VAR_0     0 
          36  LOAD_FAST             0  'self'
          39  STORE_ATTR            4  '_rc_off'
          42  JUMP_FORWARD          0  'to 45'
        45_0  COME_FROM                '42'

 148      45  LOAD_FAST             0  'self'
          48  LOAD_ATTR             5  'unit_obj'
          51  LOAD_ATTR             6  'get_com'
          54  LOAD_CONST            2  'ComMoveSyncReceiver2Stash'
          57  CALL_FUNCTION_1       1 
          60  STORE_FAST            2  'stash_com'

 149      63  LOAD_FAST             2  'stash_com'
          66  POP_JUMP_IF_FALSE   137  'to 137'

 150      69  LOAD_FAST             2  'stash_com'
          72  LOAD_ATTR             7  'get_sync_rc_all_params'
          75  CALL_FUNCTION_0       0 
          78  STORE_FAST            3  'params'

 151      81  LOAD_FAST             3  'params'
          84  POP_JUMP_IF_FALSE   118  'to 118'

 152      87  LOAD_FAST             3  'params'
          90  UNPACK_SEQUENCE_2     2 
          93  STORE_FAST            4  'args'
          96  STORE_FAST            5  'kwargs'

 153      99  LOAD_FAST             0  'self'
         102  LOAD_ATTR             8  '_on_sync_all'
         105  LOAD_FAST             4  'args'
         108  LOAD_FAST             5  'kwargs'
         111  CALL_FUNCTION_VAR_KW_0     0 
         114  POP_TOP          
         115  JUMP_FORWARD          0  'to 118'
       118_0  COME_FROM                '115'

 154     118  LOAD_FAST             0  'self'
         121  LOAD_ATTR             5  'unit_obj'
         124  LOAD_ATTR             9  'del_com'
         127  LOAD_CONST            2  'ComMoveSyncReceiver2Stash'
         130  CALL_FUNCTION_1       1 
         133  POP_TOP          
         134  JUMP_FORWARD          0  'to 137'
       137_0  COME_FROM                '134'

 156     137  LOAD_FAST             0  'self'
         140  LOAD_ATTR             5  'unit_obj'
         143  LOAD_ATTR            10  'MASK'
         146  LOAD_GLOBAL          11  'NEED_HIGH_FRAME_TAG_VALUE'
         149  BINARY_AND       
         150  POP_JUMP_IF_FALSE   178  'to 178'
         153  LOAD_FAST             0  'self'
         156  LOAD_ATTR            12  'sd'
         159  LOAD_ATTR            13  'ref_is_robot'
         162  UNARY_NOT        
       163_0  COME_FROM                '150'
         163  POP_JUMP_IF_FALSE   178  'to 178'

 157     166  LOAD_GLOBAL          14  'True'
         169  LOAD_FAST             0  'self'
         172  STORE_ATTR           15  'need_high_frame'
         175  JUMP_FORWARD          0  'to 178'
       178_0  COME_FROM                '175'

 159     178  LOAD_GLOBAL          16  'getattr'
         181  LOAD_GLOBAL           3  'vector'
         184  LOAD_GLOBAL          14  'True'
         187  CALL_FUNCTION_3       3 
         190  POP_JUMP_IF_FALSE   332  'to 332'

 160     193  LOAD_FAST             0  'self'
         196  LOAD_ATTR            17  'ev_g_position'
         199  CALL_FUNCTION_0       0 
         202  LOAD_FAST             0  'self'
         205  STORE_ATTR           18  '_cur_sim_pos'

 161     208  LOAD_FAST             0  'self'
         211  LOAD_ATTR             5  'unit_obj'
         214  LOAD_ATTR            19  'add_com'
         217  LOAD_CONST            4  'ComDataLogicMovement'
         220  LOAD_CONST            5  'client'
         223  CALL_FUNCTION_2       2 
         226  STORE_FAST            6  'com'

 162     229  LOAD_FAST             6  'com'
         232  JUMP_IF_FALSE_OR_POP   263  'to 263'
         235  LOAD_FAST             6  'com'
         238  LOAD_ATTR            20  'init_from_dict'
         241  LOAD_FAST             0  'self'
         244  LOAD_ATTR             5  'unit_obj'
         247  BUILD_MAP_1           1 
         250  LOAD_FAST             0  'self'
         253  LOAD_ATTR            18  '_cur_sim_pos'
         256  LOAD_CONST            6  'position'
         259  STORE_MAP        
         260  CALL_FUNCTION_2       2 
       263_0  COME_FROM                '232'
         263  POP_TOP          

 164     264  LOAD_FAST             0  'self'
         267  LOAD_ATTR             5  'unit_obj'
         270  LOAD_ATTR            19  'add_com'
         273  LOAD_CONST            7  'ComDataLogicMovementRel'
         276  LOAD_CONST            5  'client'
         279  CALL_FUNCTION_2       2 
         282  STORE_FAST            6  'com'

 165     285  LOAD_FAST             6  'com'
         288  JUMP_IF_FALSE_OR_POP   319  'to 319'
         291  LOAD_FAST             6  'com'
         294  LOAD_ATTR            20  'init_from_dict'
         297  LOAD_FAST             0  'self'
         300  LOAD_ATTR             5  'unit_obj'
         303  BUILD_MAP_1           1 
         306  LOAD_FAST             0  'self'
         309  LOAD_ATTR            18  '_cur_sim_pos'
         312  LOAD_CONST            6  'position'
         315  STORE_MAP        
         316  CALL_FUNCTION_2       2 
       319_0  COME_FROM                '288'
         319  POP_TOP          

 166     320  LOAD_GLOBAL          21  'False'
         323  LOAD_FAST             0  'self'
         326  STORE_ATTR           22  'need_add_sub_com'
         329  JUMP_FORWARD          0  'to 332'
       332_0  COME_FROM                '329'
         332  LOAD_CONST            0  ''
         335  RETURN_VALUE     

Parse error at or near `CALL_FUNCTION_3' instruction at offset 187

    def destroy(self):
        self.unload_all_itpler()
        self.end_high_frame_tick_timer()
        self._noti_pos = dummy_cb
        self.unit_obj.del_com('ComDataLogicMovement')
        self.unit_obj.del_com('ComDataLogicMovementRel')
        super(ComMoveSyncReceiver2, self).destroy()

    def set_enable(self, enable):
        need_resume = enable and not self._enable
        self._enable = enable
        self.run_tick = enable
        if need_resume:
            self._on_clear_buffer()
            self._on_resume()

    def _get_sync_position(self):
        return self._pos

    def _noti_pos_normal(self, v3d_pos):
        if not self._enable:
            return
        if G_POS_CHANGE_MGR:
            self.notify_pos_change(v3d_pos)
        else:
            self.send_event('E_POSITION', v3d_pos)
        if self._rc_off:
            model = self.ev_g_model()
            if model:
                model.position = v3d_pos + self._rc_off

    def _enable_parachute_simulate_following(self, flag):
        self._parachute_simulate_follow_enabled = flag
        self._noti_pos = dummy_cb if flag else self._noti_pos_normal

    def on_get_speed(self):
        if self._vel:
            return self._vel.length
        return 0

    def get_walk_direction(self):
        return self._vel

    def _clear_pos(self):
        self._pos = None
        self._vel = math3d.vector(0, 0, 0)
        self._acc = math3d.vector(0, 0, 0)
        self._cur_sim_pos = None
        return

    def _on_resume(self):
        if self._to_yaw is not None:
            to_yaw = self._to_yaw
            self._to_yaw = None
            self._on_rc_force_yaw(to_yaw)
        if self._cur_sim_pos:
            self._noti_pos(self._cur_sim_pos)
        return

    def _on_rc_force_yaw(self, f_yaw):
        global g_has_post
        if self._enable is False:
            return
        if self.sd.ref_logic_trans:
            self.sd.ref_logic_trans.yaw_target = f_yaw
            self.sd.ref_common_motor.set_yaw_time(-1)
        elif g_has_post is False:
            exception_hook.post_stack('[ECS ERR] unit {} has no ref_logic_trans, is valid {}'.format(type(self.unit_obj), self.is_valid()))
            g_has_post = True

    def _fix_yaw(self, f_yaw):
        cur_yaw = self.ev_g_yaw()
        if cur_yaw is None:
            cur_yaw = 0
        dt_yaw = f_yaw - cur_yaw
        if abs(dt_yaw) > math.pi:
            fix_dt = 2 * math.pi * dt_yaw / abs(dt_yaw) if 1 else 0
            return fix_dt or cur_yaw
        else:
            new_yaw = cur_yaw + fix_dt
            return new_yaw

    def _on_sync_yaw(self, f_yaw, f_dt=0):
        self._to_yaw = f_yaw
        if self._enable is False:
            return
        is_moving = not self._vel.is_zero
        force = True if is_moving or self.sync_attr.get('force_yaw', False) else False
        self.sd.ref_logic_trans.force_turn_body = force
        self.sd.ref_logic_trans.yaw_target = f_yaw
        self.sd.ref_common_motor.set_yaw_time(f_dt)

    def _cb_it_yaw(self, dt_per):
        if abs(dt_per) < 0.001:
            return True
        if self._st_lazy == DRAW_ST_LAZY or self._parachute_simulate_follow_enabled:
            return
        is_moving = not self._vel.is_zero
        force = True if is_moving or self.sync_attr.get('force_yaw', False) else False
        self.sd.ref_logic_trans.yaw_target += dt_per
        rotatedata = self.sd.ref_rotatedata
        rotatedata.force_turn_body = force
        rotatedata.mark_dirty()
        cur_yaw = self.ev_g_yaw()
        rotatedata.yaw = cur_yaw

    def _on_action_sync_rc_resume_roll(self):
        self.send_event('E_ACTION_SYNC_RC_STOP_EULER_ITPL')
        model = self.ev_g_model()
        if model:
            rot = model.rotation_matrix
            yaw = rot.yaw
            new_rot = math3d.matrix_to_rotation(math3d.matrix.make_rotation_y(yaw))
            self.send_event('E_ROTATION', new_rot)

    def _on_death(self, *args, **kwargs):
        if self.sd.ref_is_mecha:
            self._on_action_sync_rc_resume_roll()

    def _on_sync_head_pitch(self, f_head_pitch):
        if self._enable is False:
            return
        cur_head_pitch = self.ev_g_cam_pitch() or 0
        delta_pitch = f_head_pitch - cur_head_pitch
        if self._dis_2_cam > RC_LOD_2:
            self.send_event('E_CLIENT_INTER_DEL', 'it_pitch')
            self.send_event('E_DELTA_PITCH', delta_pitch)
            self.send_event('E_ACTION_PITCH', delta_pitch)
            self.send_event('E_SYNC_CAM_PITCH_NORMAL', f_head_pitch)
        elif delta_pitch:
            self.send_event('E_CLIENT_INTER_PUT', 'it_head_pitch', delta_pitch, ITVL_MIX_FRAME_PITCH * 2, self._cb_it_head_pitch)

    def _cb_it_head_pitch(self, dt_per):
        if not self.unit_obj:
            return
        if abs(dt_per) < 0.001:
            return True
        if self._st_lazy == DRAW_ST_LAZY:
            return
        self.send_event('E_DELTA_PITCH', dt_per)
        self.send_event('E_ACTION_PITCH', dt_per)
        cur_head_pitch = self.ev_g_cam_pitch() or 0
        self.send_event('E_SYNC_CAM_PITCH_NORMAL', cur_head_pitch)

    def _move_action_forward(self, lst_dir):
        if self._enable is None:
            return
        else:
            if not lst_dir:
                return
            v_dir = math3d.vector(*lst_dir)
            if not self._parachute_simulate_follow_enabled:
                self.unit_obj.send_event('E_CHANGE_ANIM_MOVE_DIR', v_dir.x, v_dir.z)
            return

    def _on_action_sync_rc_attr(self, key, val):
        self.sync_attr[key] = val

    def _get_action_sync_attr(self, key):
        return self.sync_attr.get(key)

    def filter_hit_character(self, v3d_pos):
        if not global_data.player:
            return v3d_pos
        lplayer = global_data.player.logic
        if not lplayer:
            return v3d_pos
        c_pos = lplayer.ev_g_position()
        char = lplayer.sd.ref_character
        if not char:
            return v3d_pos
        MIN_FACTOR = 1.2
        h = char.getHeight() * MIN_FACTOR
        r = char.getRadius() * MIN_FACTOR
        if not c_pos:
            return v3d_pos
        moving = lplayer.ev_g_get_state(status_config.ST_MOVE)
        if moving:
            return v3d_pos
        l = (v3d_pos - c_pos).length
        if l > NEOX_UNIT_SCALE:
            return v3d_pos
        dt_hori = math3d.vector(v3d_pos.x - c_pos.x, 0, v3d_pos.z - c_pos.z)
        dt_vert = math3d.vector(0, v3d_pos.y - c_pos.y, 0)
        if dt_hori.length > 2 * r or dt_vert.length > h:
            return v3d_pos
        factor = max(MIN_FACTOR, 2 * r / dt_hori.length) if dt_hori.length else MIN_FACTOR
        if dt_hori.length == 0:
            if dt_vert.y > 0:
                factor = max(MIN_FACTOR, h / dt_vert.y)
            else:
                factor = MIN_FACTOR
        diff = dt_hori + dt_vert
        diff *= factor
        v3d_pos = c_pos + diff
        return v3d_pos

    def _check_lazy_trigger(self, v3d_pos):
        if self._st_lazy == DRAW_ST_RESUME:
            self._st_lazy = DRAW_ST_SHOW
            self._layz_cnt = LAZY_TICK_ITVL
            return False
        mdl = self.ev_g_model()
        if not mdl:
            return False
        scene = self.scene
        if not scene:
            return False
        self._calc_lod(v3d_pos, scene.active_camera.position)
        mat_cam = scene.active_camera.transformation
        v3d_diff = v3d_pos - mat_cam.translation
        if v3d_diff.length < RADIUS_LAZY:
            return False
        if self._st_lazy != DRAW_ST_RESUME and not mdl.is_visible_in_this_frame():
            self._st_lazy = DRAW_ST_LAZY
            return True
        return False

    def _check_lazy_resume(self, v3d_pos):
        scene = self.scene
        if not scene:
            return
        self._calc_lod(v3d_pos, scene.active_camera.position)
        mat_cam = scene.active_camera.transformation
        cam_forward = math3d.vector(mat_cam.forward)
        if cam_forward.is_zero:
            return
        cam_forward.normalize()
        v3d_diff = v3d_pos - mat_cam.translation
        dis = v3d_diff.length
        if dis > RADIUS_LAZY and v3d_diff.dot(cam_forward) / (v3d_diff.length * cam_forward.length) < 0:
            return
        self._st_lazy = DRAW_ST_RESUME
        self._on_resume()

    def _on_observe(self, is_ob):
        if is_ob:
            self._dis_2_cam = 0
        else:

            def delay_check_cam_dis():
                if not self.unit_obj:
                    return
                if self._pos and self.scene:
                    self._calc_lod(self._pos, self.scene.active_camera.position)

            global_data.game_mgr.next_exec(delay_check_cam_dis)

    def _calc_lod(self, v3d_pos, cam_pos):
        self._dis_2_cam = (v3d_pos - cam_pos).length

    def _get_sync_lod_dis(self):
        return self._dis_2_cam

    def _on_sync_rel(self, t, idx, rel_ent_id, v3d_rel_pos, v3d_vel):
        if idx <= self.idx_rel_pos:
            return
        self.idx_rel_pos = idx
        if self.sd.ref_rel_logic_movement:
            self.sd.ref_rel_logic_movement.add_state(t, rel_ent_id, v3d_rel_pos, v3d_vel)

    def _on_sync_all(self, t, idx, v3d_pos, v3d_vel, v3d_acc):
        if idx <= self.idx_pos:
            return
        self.idx_pos = idx
        if self._st_lazy != DRAW_ST_SHOW:
            self._check_lazy_resume(v3d_pos)
        if self.sd.ref_logic_movement:
            self.sd.ref_logic_movement.add_state(t, v3d_pos, v3d_vel, v3d_acc)
        self.run_tick = True
        self._pos = v3d_pos
        self._vel = v3d_vel
        self._acc = v3d_acc

    def _on_clear_buffer(self):
        buffer = self.sd.ref_logic_movement.buffer
        if buffer:
            t, v3d_pos, v3d_vel, v3d_acc = buffer[-1]
            if self.sd.ref_logic_movement:
                self.sd.ref_logic_movement.clear_buffer(t, v3d_pos, v3d_vel, v3d_acc)
                self.sd.ref_logic_movement.add_state(t, v3d_pos, v3d_vel, v3d_acc)

    def _on_sync_teleport(self, t, idx, v3d_pos, v3d_vel, v3d_acc):
        if idx <= self.idx_pos:
            return
        else:
            self.idx_pos = idx
            model = self.ev_g_model()
            pre_model_position = model.world_position if model else None
            if self._st_lazy != DRAW_ST_SHOW:
                self._check_lazy_resume(v3d_pos)
            if self.sd.ref_logic_movement:
                self.sd.ref_logic_movement.clear_buffer(t, v3d_pos, v3d_vel, v3d_acc)
                self.sd.ref_logic_movement.add_state(t, v3d_pos, v3d_vel, v3d_acc)
            self.run_tick = True
            self._pos = v3d_pos
            self._vel = v3d_vel
            self._acc = v3d_acc
            self._noti_pos(v3d_pos)
            f = lambda p: (int(p.x), int(p.y), int(p.z)) if p else p
            now_model_pos = model.world_position if model else None
            self.sd.ref_teleport_info = (t, f(v3d_pos), model is not None, f(pre_model_position), f(now_model_pos), self._enable)
            return

    @property
    def run_tick(self):
        return self._run_tick

    @run_tick.setter
    def run_tick(self, flag):
        if self._run_tick == flag:
            return
        self._run_tick = flag
        if flag:
            if self.need_high_frame and global_data.cam_lplayer and global_data.cam_lplayer.id == global_data.player.id:
                if self.high_frame_tick_timer == -1:
                    self.start_high_frame_tick_timer()
                if self.need_update:
                    self.need_update = False
            else:
                self.end_high_frame_tick_timer()
                self.need_update = True
        else:
            self.need_update = False
            self.end_high_frame_tick_timer()

    def _check_parachute_together(self, avatar):
        avatar_follow_target = avatar.logic.ev_g_parachute_follow_target()
        puppet_follow_target = self.sd.ref_parachute_follow_target
        if avatar_follow_target == self.unit_obj.id or puppet_follow_target == avatar.id or avatar_follow_target == puppet_follow_target:
            return True
        return False

    def _check_puppet_need_high_frame_update(self):
        if not global_data.player or not global_data.player.logic:
            return False
        lavatar = global_data.player.logic
        if not lavatar.ev_g_parachuting():
            return False
        if not self.ev_g_parachuting():
            return False
        if not lavatar.ev_g_is_groupmate(self.unit_obj.id):
            return False
        if self._check_parachute_together(global_data.player):
            return True
        cur_pos = self._cur_sim_pos if self._cur_sim_pos else self.ev_g_position()
        a_pos = lavatar.ev_g_position()
        return a_pos and (a_pos - cur_pos).length < 500.0

    def on_parachute_stage_changed(self, *args):
        if not self.ev_g_is_avatar():
            if self.need_high_frame != self._check_puppet_need_high_frame_update():
                self.need_high_frame = not self.need_high_frame
                self.run_tick = self._run_tick

    def on_refresh_tick_method(self):
        if self.need_high_frame != self._check_puppet_need_high_frame_update():
            self.need_high_frame = not self.need_high_frame
            self.run_tick = self._run_tick

    def start_high_frame_tick_timer(self, need_refresh=True):
        self.high_frame_tick_timer = global_data.game_mgr.get_fix_logic_timer().register(func=self.tick, interval=1, timedelta=True)
        if need_refresh and self.high_frame_tick_timer_refreshed and self.ev_g_has_parachute_follower():
            groupmate_id_list = self.ev_g_groupmate()
            for eid in groupmate_id_list:
                if eid == self.unit_obj.id:
                    continue
                ent = self.battle.get_entity(eid)
                if ent and ent.logic and ent.logic.is_valid():
                    ent.logic.send_event('E_REFRESH_PARACHUTE_FOLLOW_UPDATE_ORDER')

    def end_high_frame_tick_timer(self):
        if self.high_frame_tick_timer > 0:
            global_data.game_mgr.get_fix_logic_timer().unregister(self.high_frame_tick_timer)
            self.high_frame_tick_timer = -1

    def on_refresh_high_frame_tick_timer(self):
        if not self.high_frame_tick_timer_refreshed:
            self.end_high_frame_tick_timer()
            self.start_high_frame_tick_timer(need_refresh=False)
            self.high_frame_tick_timer_refreshed = True

    def tick(self, dt):
        if self._layz_cnt < 0:
            self._layz_cnt = 10
            self._st_lazy = DRAW_ST_RESUME
        self._layz_cnt -= 1
        move_data = self.sd.ref_logic_movement
        move_data_rel = self.sd.ref_rel_logic_movement
        pos = None
        if move_data.dirty:
            move_data.dirty = False
            self._cur_sim_pos = pos = math3d.vector(move_data.cur_pos)
            if self._check_lazy_trigger(pos) and not move_data.itpl_stop:
                return
        pos_rel_adjust = move_data_rel.get_real_pos()
        if pos_rel_adjust and not move_data_rel.overdue_frames == move_data_rel.max_overdue_frames:
            pos = math3d.vector(move_data.cur_pos)
            if pos:
                u = float(move_data_rel.overdue_frames) / move_data_rel.max_overdue_frames
                dis_vec = (pos_rel_adjust - pos).length
                if dis_vec < NEOX_UNIT_SCALE * 10:
                    pos.intrp(pos_rel_adjust, pos, u)
        if self._enable and pos:
            self._noti_pos(pos)
            self.cal_forward()
        return

    def cal_forward(self, force=False):
        now = t_util.get_time()
        if now - self._move_dir_cal_time < 0.04 or force:
            return
        self._move_dir_cal_time = now
        if not self._pos or not self._cur_sim_pos:
            return
        if self._vel.is_zero:
            v_left = self._pos - self._cur_sim_pos
            if v_left.length < 0.2:
                if not self._parachute_simulate_follow_enabled:
                    self.send_event('E_CHANGE_ANIM_MOVE_DIR', 0, 0)
                self._last_forward = math3d.vector(0, 0, 0)
                return
            hori_spd = math3d.vector(v_left.x, 0, v_left.z)
        else:
            hori_spd = math3d.vector(self._vel.x, 0, self._vel.z)
        if hori_spd.is_zero:
            if not self._parachute_simulate_follow_enabled:
                self.send_event('E_CHANGE_ANIM_MOVE_DIR', 0, 0)
            self.send_event('E_HORI_SPD_DIR', math3d.vector(0, 0, 0))
        else:
            yaw = self.ev_g_yaw()
            if not yaw or math.isnan(yaw):
                return
        v_face = math3d.matrix.make_rotation_y(yaw).forward
        v_face.normalize()
        hori_spd.normalize()
        if v_face.cross(hori_spd).is_zero:
            forward = math3d.vector(0, 0, -1) if v_face.dot(hori_spd) < 0 else math3d.vector(0, 0, 1)
        else:
            mat = math3d.matrix.make_rotation_between(v_face, hori_spd)
            forward = mat.forward
            if math.isnan(forward.length):
                forward = math3d.vector(0, 0, 1)
        if self.ev_g_get_state(status_config.ST_SKATE) and not self.ev_g_get_state(status_config.ST_SKATE_MOVE):
            pass
        else:
            if (forward - self._last_forward).length > 0.2:
                self._last_forward = forward
                if not self._parachute_simulate_follow_enabled:
                    self.send_event('E_CHANGE_ANIM_MOVE_DIR', forward.x, forward.z)
            self.send_event('E_HORI_SPD_DIR', forward)

    def set_enable_sync_itpler(self, lst_itpler_name):
        for itpler_name in lst_itpler_name:
            self.load_itpler(itpler_name)

    def set_disable_sync_itpler(self, lst_itpler_name):
        for itpler_name in lst_itpler_name:
            self.unload_itpler(itpler_name)

    def unload_itpler(self, itpler_name):
        if not self.is_itpler_load(itpler_name):
            return
        com_name, com_type = MP_NAME_2_COM[itpler_name]
        self.unit_obj.del_com(com_name)
        self.mp_itplers.pop(itpler_name)

    def load_itpler(self, itpler_name):
        if self.is_itpler_load(itpler_name):
            return
        com_name, com_type = MP_NAME_2_COM[itpler_name]
        self.mp_itplers[itpler_name] = True
        c = self.unit_obj.add_com(com_name, com_type)
        c.init_from_dict(self.unit_obj, {})

    def is_itpler_load(self, itpler_name):
        com_name, com_type = MP_NAME_2_COM[itpler_name]
        if self.unit_obj.get_com(com_name):
            return True
        else:
            return False

    def unload_all_itpler(self):
        if not self.unit_obj:
            log_error('unload_all_itpler but self.unit_obj is None.')
            return
        for itpler_name in six_ex.keys(self.mp_itplers):
            self.unload_itpler(itpler_name)

    def _on_rc_offset(self, tp_off):
        self._rc_off = math3d.vector(*tp_off)
        if self._cur_sim_pos:
            self._noti_pos(self._cur_sim_pos)

    def _on_clear_rc_offset(self):
        self._rc_off = None
        if self._cur_sim_pos:
            self._noti_pos(self._cur_sim_pos)
        return