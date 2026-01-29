# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/com_simple_sync/ComSimpleMoveSyncReceiver.py
from __future__ import absolute_import
from logic.gcommon.component.UnitCom import UnitCom
import math3d
import math
FLAG_MOVE = 1
FLAG_ROT = 2

class ComSimpleMoveSyncReceiver(UnitCom):
    BIND_EVENT = {'E_SIMPLE_SYNC_MOVE': '_on_simple_sync_move',
       'E_SIMPLE_SYNC_TELPORT': '_on_simple_sync_telport',
       'G_CTRL_DIR': '_get_ctrl_direction',
       'G_IS_MOVE': '_is_move',
       'G_CTRL_POSITION': '_get_ctrl_position',
       'G_ROTATION_MATRIX': '_get_rotation_matrix',
       'G_IS_POS_INITED': '_is_pos_inited'
       }

    def __init__(self):
        super(ComSimpleMoveSyncReceiver, self).__init__()
        self._move_dir = None
        self._to_pos = None
        self._to_rot = None
        self._flag_move = 0
        self._flag_rot = 0
        return

    def on_post_init_complete(self, bdict):
        super(ComSimpleMoveSyncReceiver, self).on_post_init_complete(bdict)
        if 'move_info' in bdict:
            self._init_move_info(bdict['move_info'])

    def _init_move_info(self, move_info):
        self._on_simple_sync_telport(move_info)

    def _get_ctrl_position(self):
        return self._to_pos or math3d.vector(0, 0, 0)

    def _is_pos_inited(self):
        return self._to_pos is not None

    def _get_rotation_matrix(self):
        return self._to_rot or math3d.matrix()

    def _on_simple_sync_move(self, move_info):
        pos = move_info[1]
        yaw = move_info[2]
        v3d_pos = math3d.vector(*pos)
        rot_mat = math3d.matrix.make_rotation_y(yaw)
        self._to_pos = v3d_pos
        self._to_rot = rot_mat
        self._flag_move = FLAG_MOVE
        self.need_update = True
        self.send_event('E_SET_ROTATION_MATRIX', rot_mat)
        self._move_dir = math3d.vector(0, 0, 1)
        self.send_event('E_MOVE', self._move_dir)

    def _is_move(self):
        return self._flag_move != 0

    def _on_simple_sync_telport(self, move_info):
        pos = move_info[1]
        yaw = move_info[2]
        v3d_pos = math3d.vector(*pos)
        rot_mat = math3d.matrix.make_rotation_y(yaw)
        self._to_pos = v3d_pos
        self._to_rot = rot_mat
        if G_POS_CHANGE_MGR:
            self.notify_pos_change(v3d_pos)
        else:
            self.send_event('E_POSITION', v3d_pos)
        self.send_event('E_SET_ROTATION_MATRIX', rot_mat)
        self._stop_move()

    def _get_ctrl_direction(self):
        return self._move_dir

    def _tick_move(self, dt):
        if not self._flag_move:
            return
        ref_delta = 1.0 / 30.0
        ref_max_tick_step = 1.8
        max_tick_step = ref_max_tick_step * dt / ref_delta
        cur_pos = self.ev_g_position()
        if not cur_pos:
            return
        new_pos = math3d.vector(0, 0, 0)
        ref_ratio = 0.2
        ratio = ref_ratio * dt / ref_delta
        new_pos.intrp(cur_pos, self._to_pos, ratio)
        delta = new_pos - cur_pos
        if delta.length < 0.3:
            self._stop_move()
        elif delta.length > max_tick_step:
            delta.normalize()
            delta = delta * max_tick_step
            new_pos = cur_pos + delta
            if self._to_rot:
                rot_forward = self._to_rot.forward
                delta = math3d.vector(delta.x, 0, delta.z)
                if delta.is_zero:
                    delta = self._to_rot.forward
                else:
                    delta.normalize()
                if delta.cross(rot_forward).is_zero:
                    if (delta + rot_forward).is_zero:
                        forward = math3d.vector(0, 0, -1)
                    else:
                        forward = math3d.vector(0, 0, 1)
                else:
                    mat = math3d.matrix.make_rotation_between(self._to_rot.forward, delta)
                    forward = mat.forward
                self._move_dir = forward
                if math.isnan(self._move_dir.length):
                    self._move_dir = math3d.vector(0, 0, 1)
                self.send_event('E_MOVE', self._move_dir)
        if G_POS_CHANGE_MGR:
            self.notify_pos_change(new_pos)
        else:
            self.send_event('E_POSITION', new_pos)

    def _stop_move(self):
        self._move_dir = None
        self.send_event('E_MOVE_STOP')
        self._flag_move = 0
        self._try_stop_tick()
        return

    def _tick_rot(self, dt):
        pass

    def _try_stop_tick(self):
        if self._flag_move or self._flag_rot:
            return
        self.need_update = False

    def tick(self, dt):
        self._tick_rot(dt)
        self._tick_move(dt)