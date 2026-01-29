# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/com_ai_ctrl/ComRemoteMonsterMove.py
from __future__ import absolute_import
from __future__ import print_function
from .ComRemoteMove import ComRemoteMove
from math import pi
from logic.gcommon.cdata.pve_monster_status_config import MC_MOVE
from math3d import vector
from logic.gutils.pve_utils import H_OFFSET
from common.cfg import confmgr

class ComRemoteMonsterMove(ComRemoteMove):
    BIND_EVENT = ComRemoteMove.BIND_EVENT.copy()
    BIND_EVENT.update({'E_DEATH': 'on_die',
       'E_HEALTH_HP_EMPTY': 'on_die'
       })

    def init_from_dict(self, unit_obj, bdict):
        super(ComRemoteMonsterMove, self).init_from_dict(unit_obj, bdict)
        if self._is_pve_monster:
            self._tick_interval = 0.2
            self.sd.ref_is_pve_monster = True
        else:
            self.sd.ref_is_pve_monster = False
        self.conf = confmgr.get('monster_data', 'Monster', 'Content', str(self._npc_id))
        self.pitch_offset = self.conf.get('PitchOffset', 0)
        self.pitch_range = self.conf.get('PitchRange', [0, 0])
        self.handle_sunshine()

    def handle_sunshine(self):
        if not global_data.use_sunshine:
            return
        p = global_data.sunshine_monster_col_dict
        if not p:
            return
        m_id = p.get('monster_id', 0)
        if m_id == self._npc_id:
            self.pitch_offset = p.get('pitch_offset', 0)
            self.pitch_range = p.get('pitch_range', [0, 0])

    def on_die(self, *_):
        self.need_update = False
        self.move_stop()

    def check_move_error(self, delta):
        if self._last_track is None:
            return
        else:
            m_pos = self.ev_g_position()
            if m_pos == self._last_born and not self._is_pve_monster:
                self.send_event('E_CLEAR_SPEED')
                self.send_event('E_MOVE_ROCK', vector(0, 0, 0), True)
                if self._move_target:
                    self._move_queue.insert(0, self._move_target)
                return
            dist = self._last_track - m_pos
            dist.y = 0
            if dist.length < 0.5:
                self._stuck_time += delta
                if self._stuck_time >= 0.5:
                    self._stuck_time = 0
                    self.move_stop(-1)
            else:
                self._last_track = m_pos
                self._stuck_time = 0
            return

    def on_tick_move(self):
        if self._move_target is None and self._move_queue:
            self._move_to_target()
        enemy_pos = self.ev_g_enemy_pos()
        change_pitch = True
        need_smooth = not enemy_pos
        if self._is_pve_monster:
            need_smooth = False
            if self._face_mode == 1:
                if self._move_target and enemy_pos:
                    pos = enemy_pos
                else:
                    pos = self._move_target
                    change_pitch = False
            elif self._face_mode == 2:
                if enemy_pos:
                    pos = enemy_pos
                else:
                    pos = self._move_target
                    change_pitch = False
            else:
                pos = self._move_target
                change_pitch = False
            if isinstance(pos, (list, tuple)):
                pos = vector(*pos)
            if pos:
                pos = vector(pos.x, pos.y + H_OFFSET, pos.z)
        else:
            pos = enemy_pos if enemy_pos else self._move_target
        if pos:
            self.face_to(pos, need_smooth, change_pitch)
        return

    def face_to(self, pos, smooth=False, change_pitch=True):
        if pos is None:
            return
        else:
            if isinstance(pos, (list, tuple)):
                pos = vector(*pos)
            cur_pos = self.ev_g_model_position() + vector(0, self.pitch_offset, 0)
            move_dir = pos - cur_pos
            if move_dir.is_zero:
                return
            if self._is_stun:
                return
            if self._smooth_timer:
                return
            yaw = move_dir.yaw
            self.send_event('E_CAM_YAW', yaw)
            self.send_event('E_ACTION_SYNC_YAW', yaw)
            if change_pitch:
                pitch = move_dir.pitch
                if global_data.debug_pve_pitch:
                    print(pitch)
                if self.pitch_range:
                    pitch_min, pitch_max = self.pitch_range
                    if pitch_min and pitch_max:
                        pitch = pitch_min if pitch < pitch_min else pitch
                        pitch = pitch_max if pitch > pitch_max else pitch
                self.send_event('E_CAM_PITCH', pitch)
                self.send_event('E_ACTION_SYNC_HEAD_PITCH', pitch)
            self._on_face_action()
            return

    def handle_blend_dir(self, m_yaw):
        if self._blend_dir == 1:
            m_dir = 'walk_f'
        elif self._blend_dir == 4:
            if pi * 0.25 <= m_yaw < pi * 0.75:
                m_dir = 'walk_f'
            elif pi * 0.75 <= m_yaw < pi * 1.25:
                m_dir = 'walk_l'
            elif pi * 1.25 <= m_yaw < pi * 1.75:
                m_dir = 'walk_b'
            else:
                m_dir = 'walk_r'
        elif self._blend_dir == 2:
            if m_yaw <= pi:
                m_dir = 'walk_f'
            else:
                m_dir = 'walk_b'
        elif self._blend_dir == 6:
            if 0 <= m_yaw < pi * 0.33:
                m_dir = 'walk_fr'
            elif pi * 0.33 <= m_yaw < pi * 0.66:
                m_dir = 'walk_f'
            elif pi * 0.66 <= m_yaw < pi:
                m_dir = 'walk_fl'
            elif pi <= m_yaw < pi * 1.33:
                m_dir = 'walk_bl'
            elif pi * 1.33 <= m_yaw < pi * 1.66:
                m_dir = 'walk_b'
            else:
                m_dir = 'walk_br'
        else:
            return
        self.send_event('E_REPLACE_ACTION_TRIGGER_ANIM', MC_MOVE, m_dir, blend_dir=1)