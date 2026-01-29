# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/behavior/PVEMonsterHitLogic.py
from __future__ import absolute_import
from .MonsterStateBase import MonsterStateBase
from logic.gcommon.common_const.character_anim_const import UP_BODY
import math3d
from logic.gutils.pve_utils import get_aim_pos

class MonsterHitBase(MonsterStateBase):
    BIND_EVENT = {'E_ACTIVE_PARAM_STATE': 'pre_check_param'
       }

    def pre_check_param(self, state, *args):
        if state != self.sid:
            return
        else:
            if not self.check_can_active():
                return False
            self.editor_handle()
            self.target_id, self.target_pos = args
            self.target_pos = math3d.vector(*self.target_pos) if self.target_pos else None
            self.active_self()
            return

    def init_from_dict(self, unit_obj, bdict, sid, state_info):
        super(MonsterHitBase, self).init_from_dict(unit_obj, bdict, sid, state_info)
        self.init_params()

    def init_params(self):
        self.target_id = None
        self.target_pos = None
        return

    def editor_handle(self):
        pass

    def enter(self, leave_states):
        super(MonsterHitBase, self).enter(leave_states)
        self.send_event('E_ANIM_RATE', UP_BODY, self.hit_anim_rate)
        if self.hit_anim:
            self.send_event('E_POST_ACTION', self.hit_anim, UP_BODY, 1)
        self.send_event('E_CTRL_FACE_TO', get_aim_pos(self.target_id, self.target_pos), False)

    def check_transitions(self):
        if self.elapsed_time > self.hit_anim_dur / self.hit_anim_rate:
            self.disable_self()

    def update(self, dt):
        super(MonsterHitBase, self).update(dt)

    def exit(self, enter_states):
        self.send_event('E_CALL_SYNC_METHOD', 'pve_end_hit', (), True)
        self.send_event('E_ANIM_RATE', UP_BODY, 1.0)
        self.send_event('E_CLEAR_UP_BODY_ANIM')
        super(MonsterHitBase, self).exit(enter_states)


class MonsterHit(MonsterHitBase):

    def init_params(self):
        super(MonsterHit, self).init_params()
        self.hit_anim = self.custom_param.get('hit_anim', None)
        self.hit_anim_dur = self.custom_param.get('hit_anim_dur', 0.7)
        self.hit_anim_rate = self.custom_param.get('hit_anim_rate', 1.0)
        return

    def editor_handle(self):
        if global_data.use_sunshine:
            self.init_params()