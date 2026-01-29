# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/com_ai_ctrl/ComRemoteMove.py
from __future__ import absolute_import
from logic.gcommon.component.UnitCom import UnitCom
from math3d import vector, rotation, euler_to_rotation
import math
import logic.gcommon.common_const.ai_const as ai_const
from logic.client.const.rocker_const import RUNNING_ANGLE
from logic.gcommon.common_const import scene_const
from common.utils.timer import RELEASE
from logic.gcommon.const import NEOX_UNIT_SCALE
from logic.gcommon import editor
MAX_LERP_DURATION = 0.2
MIN_LERP_ANGLE = math.pi / 180
CIRCLE_ANGLE = math.pi * 2

@editor.com_exporter('\xe8\xbf\x9c\xe7\xa8\x8b\xe6\x8e\xa7\xe5\x88\xb6\xe7\xbb\x84\xe4\xbb\xb6', {('move_target', 'string'): {'zh_name': '\xe7\xa7\xbb\xe5\x8a\xa8\xe7\x9b\xae\xe6\xa0\x87','getter': lambda self: str(self._move_target)
                               }
   })
class ComRemoteMove(UnitCom):
    BIND_EVENT = {'T_DEATH': 'on_die',
       'E_CLEAR_MOVE_QUEUE': 'clear_move_queue',
       'E_CTRL_FORCE_MOVE': 'force_move',
       'E_BEGIN_AGENT_AI': 'begin_agent',
       'E_END_AGENT_AI': 'end_agent',
       'E_CTRL_FACE_TO': 'face_to',
       'E_CTRL_MOVE_TO': 'move_to',
       'E_CTRL_MOVE_TO_LIST': 'move_to_list',
       'E_CTRL_MOVE_STOP': 'move_stop',
       'E_CTRL_FOOT_POSITION': 'ctrl_foot_position',
       'E_CHECK_CONTINUE_MOVE': 'check_continue_move',
       'E_CTRL_JUMP_MOVE_TO': 'jump_move_to',
       'E_POSITION': 'on_pos_changed',
       'E_CTRL_FORCE_MOVE_STOP': 'force_move_stop',
       'E_ON_TOUCH_GROUND': 'on_ground',
       'E_CTRL_FACE_MODE': 'ctrl_face_mode',
       'E_CTRL_RUN_MODE': 'ctrl_run_mode',
       'E_CTRL_BLEND_DIR': 'ctrl_blend_dir',
       'E_STUN_STATE': 'on_stun_state'
       }
    TICK_INTERVAL = 0.2
    ANGLE_OFFSET = math.cos(math.radians(2))

    def __init__(self):
        super(ComRemoteMove, self).__init__()
        self._delta = 0
        self._stuck_time = 0
        self._move_target = None
        self._move_queue = []
        self._last_pos = None
        self._move_syn = 0
        self._limit_move_syn = -1
        self._npc_id = None
        self._last_track = None
        self._last_born = None
        self._reach_offset = NEOX_UNIT_SCALE
        self._smooth_face_pos = None
        self._smooth_duration = None
        self._smooth_delta = None
        self._smooth_timer = None
        self._face_mode = None
        self._run_mode = False
        self._blend_dir = 1
        self._is_stun = False
        self._tick_interval = ComRemoteMove.TICK_INTERVAL
        self.move_dir = None
        return

    def init_from_dict(self, unit_obj, bdict):
        super(ComRemoteMove, self).init_from_dict(unit_obj, bdict)
        self._npc_id = bdict.get('npc_id', None)
        self._is_pve_monster = bdict.get('is_pve_monster', False)
        if G_POS_CHANGE_MGR:
            self.regist_pos_change(lambda pos, *args: global_data.game_mgr.next_exec(self.on_pos_changed, pos, *args))
        if self.unit_obj.is_robot():
            self._reach_offset = ai_const.REACH_OFFSET
        return

    def destroy(self):
        super(ComRemoteMove, self).destroy()

    def begin_agent(self, *_):
        self.need_update = True

    def end_agent(self, *_):
        self.need_update = False
        self._delta = 0
        self._stuck_time = 0
        self._move_target = None
        self._move_queue = []
        self._last_pos = None
        self._move_syn = 0
        self._limit_move_syn = -1
        return

    def clear_move_queue(self):
        self._move_queue = []

    def on_die(self, *_):
        self.need_update = False
        self.move_stop()

    def in_move_state(self):
        return False

    def on_pos_changed(self, pos, *args):
        if self._move_target is None:
            return
        else:
            dist = pos - self._move_target
            dist.y = 0.0
            if dist.length <= self._reach_offset:
                self.move_to_target_callback()
            elif self.in_move_state():
                if self._smooth_timer:
                    return
                self.try_exec_block_move(pos)
            return

    def try_exec_block_move(self, pos):
        if self._last_pos is None:
            self._last_pos = pos
            return
        else:
            move_dir = self._move_target - self._last_pos
            direct = pos - self._last_pos
            if direct.is_zero:
                return
            self._last_pos = pos
            block_jump = False
            if direct.x * move_dir.x < 0 or direct.z * move_dir.z < 0:
                block_jump = True
            elif direct.x == 0.0 or direct.z == 0.0:
                block_jump = True
            else:
                move_dir.y = 0.0
                direct.y = 0.0
                dot = move_dir.dot(direct)
                if dot < move_dir.length * direct.length * self.ANGLE_OFFSET:
                    block_jump = True
            if block_jump:
                self.exec_block_move()
                self._last_pos = None
            return

    def on_ground(self, *_):
        self._last_pos = None
        self.on_tick_move()
        return

    def move_to(self, pos, move_syn=None):
        if move_syn is None:
            move_syn = self._move_syn + 1
        if move_syn == self._limit_move_syn:
            return
        else:
            if move_syn != self._move_syn:
                self._move_syn = move_syn
            if isinstance(pos, (list, tuple)):
                pos = vector(*pos)
            if not self.sd.ref_is_agent:
                return
            self._move_queue.append(pos)
            self.on_tick_move()
            return

    def move_to_list(self, pos_list):
        if not self.sd.ref_is_agent:
            return
        else:
            self._move_target = None
            self._move_queue = []
            for pos in pos_list:
                if isinstance(pos, (list, tuple)):
                    pos = vector(*pos)
                self._move_queue.append(pos)

            self.send_event('E_MOVE_TO_LIST', pos_list)
            self.on_tick_move()
            return

    def jump_move_to(self, pos):
        pos = vector(*pos)
        if not self.sd.ref_is_agent:
            return
        self.face_to(pos)
        self.send_event('E_MOVE_ROCK', vector(0, 0, 1), True)
        self.regist_event('E_ON_TOUCH_GROUND', self.jump_move_to_callback)

    def jump_move_to_callback(self, *_):
        self.unregist_event('E_ON_TOUCH_GROUND', self.jump_move_to_callback)
        self.send_event('E_CLEAR_SPEED')
        self.send_event('E_MOVE_ROCK', vector(0, 0, 0), True)
        self.send_event('E_SYNC_STATE_DATA', 'jump_move_land', 2)

    def move_stop(self, state=0):
        self.send_event('E_CLEAR_SPEED')
        self.send_event('E_MOVE_ROCK', vector(0, 0, 0), True)
        if self._move_target:
            self._move_target = None
        self._last_pos = None
        self._last_track = None
        if self._move_queue:
            self._move_queue = []
        self.send_event('E_SYNC_AGENT_DATA', ai_const.AI_AGENT_MOVE, state)
        self.send_event('E_MOVE_TO_LIST', [])
        return

    def ctrl_foot_position(self, pos):
        self.move_stop()
        v3d_pos = vector(*pos)
        self.send_event('E_FOOT_POSITION', v3d_pos)

    def check_continue_move(self):
        self._move_to_target()

    def tick(self, delta):
        self._delta += delta
        if self._delta < self._tick_interval:
            return
        self.check_move_error(self._delta)
        self.on_tick_move()
        self._delta = 0

    def on_sync_water(self):
        if self._move_target:
            scn = self.scene
            cur_pos = self.ev_g_model_position()
            material_index = scn.get_scene_info_2d(cur_pos.x, cur_pos.z)
            if material_index == scene_const.MTL_DEEP_WATER:
                self.send_event('E_SYNC_AGENT_DATA', ai_const.AI_AGENT_WATER, 1)
            else:
                self.send_event('E_SYNC_AGENT_DATA', ai_const.AI_AGENT_WATER, 0)

    def force_move_stop(self):
        self._limit_move_syn = self._move_syn
        self.move_stop()

    def ctrl_face_mode(self, face_mode):
        self._face_mode = face_mode

    def ctrl_run_mode(self, run_mode):
        self._run_mode = run_mode

    def ctrl_blend_dir(self, blend_dir):
        self._blend_dir = blend_dir

    def force_move(self, syn):
        if self._move_syn > 0 and self._move_syn <= syn:
            self._move_syn = 0

    def check_move_error(self, delta):
        if self._last_track is None:
            return
        else:
            m_pos = self.ev_g_position()
            if m_pos == self._last_born:
                self.send_event('E_CLEAR_SPEED')
                self.send_event('E_MOVE_ROCK', vector(0, 0, 0), True)
                if self._move_target:
                    self._move_queue.insert(0, self._move_target)
                return
            dist = self._last_track - m_pos
            dist.y = 0
            if dist.length < 0.5:
                self.move_stop(-1)
            else:
                self._last_track = m_pos
            return

    def on_tick_move(self):
        if self._move_target is None and self._move_queue:
            self._move_to_target()
        enemy_pos = self.ev_g_enemy_pos()
        pos = enemy_pos if enemy_pos else self._move_target
        if pos:
            self.face_to(pos, not enemy_pos)
        return

    def exec_block_move(self):
        pass

    def face_to(self, pos, smooth=True, change_pitch=True):
        if pos is None:
            return
        else:
            if isinstance(pos, (list, tuple)):
                pos = vector(*pos)
            cur_pos = self.ev_g_model_position()
            move_dir = pos - cur_pos
            self.move_dir = move_dir
            if move_dir.is_zero:
                return
            if self._is_stun:
                return
            if self._smooth_timer:
                return
            if smooth:
                if pos == self._smooth_face_pos:
                    yaw = move_dir.yaw
                    pitch = move_dir.pitch
                    self.send_event('E_CAM_YAW', yaw)
                    self.send_event('E_ACTION_SYNC_YAW', yaw)
                    self.send_event('E_CAM_PITCH', pitch)
                    self.send_event('E_ACTION_SYNC_HEAD_PITCH', pitch)
                    self._on_face_action()
                else:
                    self._smooth_face_pos = pos
                    cur_forward = self.ev_g_forward()
                    yaw = move_dir.yaw - cur_forward.yaw
                    angle = math.fabs(yaw)
                    if angle == 0.0:
                        return
                    self._smooth_duration = 0.3 * angle / math.pi
                    self._smooth_delta = yaw / self._smooth_duration
                    self._smooth_timer = global_data.game_mgr.get_post_logic_timer().register(func=self._interpolate_yaw, interval=1, times=-1, timedelta=True)
            else:
                yaw = move_dir.yaw
                self.send_event('E_CAM_YAW', yaw)
                self.send_event('E_ACTION_SYNC_YAW', yaw)
                if change_pitch:
                    pitch = move_dir.pitch
                    pitch = -0.4 if pitch < -0.4 else pitch
                    pitch = 0.4 if pitch > 0.4 else pitch
                    self.send_event('E_CAM_PITCH', pitch)
                    self.send_event('E_ACTION_SYNC_HEAD_PITCH', pitch)
                self._on_face_action()
            return

    def _interpolate_yaw(self, dt):
        if self._smooth_duration > dt:
            yaw_value = self._smooth_delta * dt
            self._smooth_duration -= dt
        else:
            yaw_value = self._smooth_delta * self._smooth_duration
            self._smooth_duration = 0.0
        self.send_event('E_CAM_YAW', yaw_value + self.move_dir.yaw)
        self.send_event('E_ACTION_SYNC_YAW', yaw_value + self.move_dir.yaw)
        self._on_face_action()
        if self._smooth_duration == 0.0:
            self._smooth_timer = None
            return RELEASE
        else:
            return

    def _on_face_action(self):
        if self._move_target:
            cur_pos = self.ev_g_model_position()
            if cur_pos is None:
                return
            direct = self._move_target - cur_pos
            direct.y = 0.0
            if direct.is_zero:
                return
            direct.normalize()
            cur_rot = self.ev_g_rotation()
            cur_forward, cur_right = cur_rot.get_forward(), cur_rot.get_right()
            x = direct.dot(cur_right)
            z = direct.dot(cur_forward)
            m_yaw = math.atan2(z, x)
            m_yaw = m_yaw if m_yaw > 0 else m_yaw + 2 * math.pi
            if self.unit_obj.is_monster():
                if self._is_pve_monster:
                    self.handle_blend_dir(m_yaw)
                    self.send_event('E_MOVE_ROCK', vector(x, 0, z), self._run_mode)
                else:
                    self.send_event('E_MOVE_ROCK', vector(x, 0, z), False)
            elif m_yaw > RUNNING_ANGLE / 2 and m_yaw < RUNNING_ANGLE:
                self.send_event('E_MOVE_ROCK', vector(x, 0, z), True)
            else:
                self.send_event('E_MOVE_ROCK', vector(x, 0, z), False)
            self._last_pos = None
        return

    def _move_to_target(self):
        if not self._move_queue:
            return
        else:
            target = self._move_queue.pop(0)
            scene = global_data.game_mgr.get_cur_scene()
            if scene is None:
                self.send_event('E_TRY_SERVER_ACTION', 'E_AI_CANCEL_AGENT')
                return
            if not scene.check_landscape_has_load_detail_collision(target):
                self.send_event('E_TRY_SERVER_ACTION', 'E_AI_CANCEL_AGENT')
                return
            cur_pos = self.ev_g_position()
            if (cur_pos - target).length < self._reach_offset:
                return
            self._move_target = target
            self.send_event('E_SET_MOVE_TARGET', target)
            self._last_track = cur_pos
            self._last_born = cur_pos
            self.send_event('E_SYNC_AGENT_DATA', ai_const.AI_AGENT_MOVE, 1)
            self._last_pos = None
            return

    def move_to_target_callback(self):
        self._last_track = None
        if self._move_queue:
            if self._move_target:
                self._move_target = None
            self.on_tick_move()
        else:
            self.move_stop()
        return

    def handle_blend_dir(self, m_yaw):
        pass

    def on_stun_state(self, is_stun):
        self._is_stun = is_stun