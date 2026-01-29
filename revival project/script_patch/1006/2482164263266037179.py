# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/com_simple_sync/ComSimpleMoveSyncSender.py
from __future__ import absolute_import
from logic.gcommon.component.UnitCom import UnitCom
from logic.gcommon.common_const.collision_const import CHARACTER_STAND_WIDTH, CHARACTER_STAND_HEIGHT, GROUP_CHARACTER_INCLUDE
import math3d
from logic.gcommon.const import NEOX_UNIT_SCALE
import math
from logic.gcommon import time_utility as t_util

class ComSimpleMoveSyncSender(UnitCom):
    MIN_POS_TRI_ITVL = 0.03
    MIN_ROT_TRI_ITVL = 2
    BIND_EVENT = {'E_POSITION': '_on_pos_change',
       'E_SET_ROTATION_MATRIX': 'on_set_rotation_matrix',
       'G_MOVE_INFO': 'get_move_info',
       'E_SEND_TELPORT': '_on_send_telport',
       'E_MODEL_LOADED': '_on_model_load'
       }

    def __init__(self):
        super(ComSimpleMoveSyncSender, self).__init__(True)
        self.last_sent_time = 0
        self._to_send_telport = 0
        self._dirt_pos = None
        self._dirt_rot = False
        self.last_sent_pos = None
        return

    def init_from_dict(self, unit_obj, bdict):
        super(ComSimpleMoveSyncSender, self).init_from_dict(unit_obj, bdict)
        if G_POS_CHANGE_MGR:
            self.regist_pos_change(self._on_pos_change)

    def destroy(self):
        super(ComSimpleMoveSyncSender, self).destroy()
        if G_POS_CHANGE_MGR:
            self.unregist_pos_change(self._on_pos_change)

    def on_set_rotation_matrix(self, rot_mat):
        self._dirt_rot = True

    def _on_model_load(self, model):
        if self._to_send_telport:
            self._to_send_telport = 0
            self._on_send_telport(False)

    def get_move_info(self):
        model = self.ev_g_model()
        if not model:
            return None
        else:
            pos = model.position
            lst_pos = (pos.x, pos.y, pos.z)
            yaw = model.world_rotation_matrix.yaw
            move_info = {1: lst_pos,2: yaw}
            return move_info

    def _on_send_telport(self, is_telport=True):
        model = self.ev_g_model()
        if not model:
            self._to_send_telport = 1
            return
        pos = model.position
        self.tri_send_pos(pos, is_telport=is_telport)

    def _on_pos_change(self, pos):
        if self.last_sent_pos and (pos - self.last_sent_pos).length_sqr < 0.25:
            return
        self._dirt_pos = pos

    def tri_send_pos(self, pos, is_telport=False):
        model = self.ev_g_model()
        if model:
            yaw = model.world_rotation_matrix.yaw
        else:
            yaw = 0
        lst_pos = (
         pos.x, pos.y, pos.z)
        move_info = {1: lst_pos,2: yaw}
        if is_telport:
            move_info[0] = 1
        self._dirt_pos = None
        self._dirt_rot = False
        self.last_sent_time = t_util.time()
        self.last_sent_pos = pos
        owner = self.unit_obj.get_owner()
        owner.sync_visit_move(move_info)
        return

    def tick(self, dt):
        if not self._dirt_pos and not self._dirt_rot:
            return
        now = t_util.time()
        pos_itvl = self.MIN_POS_TRI_ITVL
        if not global_data.is_inner_server:
            pos_itvl = 1
        if self._dirt_pos and now - self.last_sent_time < pos_itvl or self._dirt_rot and now - self.last_sent_time < self.MIN_ROT_TRI_ITVL:
            return
        if global_data.is_inner_server and (not global_data.player or not global_data.player.is_in_visit_mode()):
            return
        pos = self._dirt_pos or self.ev_g_position()
        if not pos:
            return
        self.tri_send_pos(pos, not self.last_sent_time)