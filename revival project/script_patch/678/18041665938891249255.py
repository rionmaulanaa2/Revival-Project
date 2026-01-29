# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/com_ai_ctrl/ComRemoteMechaMove.py
from __future__ import absolute_import
from .ComRemoteMove import ComRemoteMove
from logic.gcommon.common_const import ai_const
from logic.gcommon.cdata import mecha_status_config as st_const
from logic.gcommon.common_const import buff_const as bconst

class ComRemoteMechaMove(ComRemoteMove):
    BIND_EVENT = ComRemoteMove.BIND_EVENT.copy()
    BIND_EVENT.update({'E_DEATH': 'on_die',
       'E_HEALTH_HP_EMPTY': 'on_die'
       })
    ST_MOVE = (
     st_const.MC_MOVE, st_const.MC_RUN)

    def __init__(self):
        super(ComRemoteMechaMove, self).__init__()

    def destroy(self):
        super(ComRemoteMechaMove, self).destroy()

    def exec_block_move(self):
        if self.unit_obj.is_monster():
            self.move_stop()
        else:
            if self.unit_obj.ev_g_has_buff_by_id(bconst.BUFF_ID_8034_GROUNDED):
                return
            self.send_event('E_CTRL_ACTION_START', ai_const.CTRL_ACTION_JUMP)

    def in_move_state(self):
        return self.ev_g_is_in_any_state(self.ST_MOVE)

    def on_die(self, *_):
        self.need_update = False
        self.move_stop()

    def on_tick_move(self):
        if self._move_target is None and self._move_queue:
            self._move_to_target()
        enemy_pos = self.ev_g_enemy_pos()
        mecha_id = self.ev_g_mecha_id()
        if self._need_free_sign(mecha_id):
            pos = self._move_target
        else:
            pos = enemy_pos if enemy_pos else self._move_target
        if pos:
            self.face_to(pos, not enemy_pos)
        return

    def _need_free_sign(self, mecha_id):
        if mecha_id == 8011 and self.ev_g_in_dragon_shape() and not self.ev_g_is_in_attack_time():
            return True
        if mecha_id == 8017 and not self.ev_g_is_in_attack_time():
            return True
        return False