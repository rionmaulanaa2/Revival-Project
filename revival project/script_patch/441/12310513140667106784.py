# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComMechaFollow.py
from logic.gcommon.component.UnitCom import UnitCom
from logic.gcommon.const import NEOX_UNIT_SCALE
import math3d
import time

class ComMechaFollow(UnitCom):
    BIND_EVENT = {'E_ENABLE_FOLLOW': 'enable_follow',
       'E_FOLLOW_MECHA': 'update_follow_entity'
       }

    def __init__(self):
        super(ComMechaFollow, self).__init__()
        self.model = None
        self.follower_entity = None
        self.followed_entity = None
        self.is_follower = False
        self.is_followed = False
        self.follow_dis = 5.0
        self.last_position = None
        return

    def init_from_dict(self, unit_obj, bdict):
        super(ComMechaFollow, self).init_from_dict(unit_obj, bdict)
        self.need_update = True
        self.is_avatar = False

    def update_follow_entity(self, follower_entity, followed_entity):
        if not global_data.battle:
            self.is_follower = False
            self.is_followed = False
            return
        self.follower_entity = global_data.battle.get_entity(follower_entity)
        self.followed_entity = global_data.battle.get_entity(followed_entity)
        self.is_avatar = self.ev_g_is_avatar()
        if self.followed_entity and self.follower_entity:
            self.need_update = True
            self.is_follower = self.follower_entity.id == self.unit_obj.id
            self.is_followed = self.followed_entity.id == self.unit_obj.id
            self.send_event('E_SET_CHAR_MASK', 65520)
        else:
            self.is_follower = False
            self.is_followed = False
            self.send_event('E_SET_CHAR_MASK', 15)
        if self.follower_entity:
            follower_entity.send_event('E_SET_SYNC_RECEIVER_ENABLE', False)

    def enable_follow(self, enable):
        if self.sd.ref_enable_follow == enable:
            return
        self.need_update = enable

    def _update_target_pos(self, dt):
        target_forward = self.ev_g_model_forward()
        self.target_pos = self.ev_g_position() + target_forward * self.follow_dis * NEOX_UNIT_SCALE + math3d.vector(0, 0.5, 0)
        self.follower_entity.logic.send_event('E_POSITION', self.target_pos)
        if self.is_avatar:
            self.send_event('E_CALL_SYNC_METHOD', 'update_follow_mecha_sync_info', (self.follower_entity.id, time.time(), [self.target_pos.x, self.target_pos.y, self.target_pos.z], [0, 0, 0], [0, 0, 0]), False, True)

    def _update_self_pos(self, dt):
        target_forward = self.followed_entity.logic.ev_g_model_forward()
        self.target_pos = self.followed_entity.logic.ev_g_position() + target_forward * self.follow_dis * NEOX_UNIT_SCALE + math3d.vector(0, 0.5, 0)
        if self.is_avatar:
            self.send_event('E_FOOT_POSITION', self.target_pos)

    def tick(self, dt):
        if not self.need_update:
            return
        if self.is_follower:
            self._update_self_pos(dt)
        if self.is_followed:
            self._update_target_pos(dt)