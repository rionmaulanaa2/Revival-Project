# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComMoveSyncClient.py
from __future__ import absolute_import
from ..UnitCom import UnitCom
from logic.gcommon.component.EventStop import ESTOP
from logic.gcommon.const import NEOX_UNIT_SCALE
from logic.gcommon import time_utility as t_util
from time import time as sys_time
import math3d

class ComMoveSyncClient(UnitCom):
    BIND_EVENT = {'E_ACTION_SYNC_RB_POS': '_on_roll_back_pos',
       'G_RB_INFO': '_get_roll_back_info',
       'E_ON_RB_DONE': '_on_rb_done',
       'G_WALK_STATE': '_get_walk_state',
       'E_ACTION_SYNC_RC_ALL': ('_on_sync_pos', -999),
       'E_ACTION_SYNC_RC_TELEPORT': ('_on_sync_pos', -999)
       }

    def __init__(self):
        super(ComMoveSyncClient, self).__init__()
        self._need_rb = False
        self._server_pos = None
        self._rb_reason = None
        self._walk_state = set()
        self._pos_idx = 0
        self._pos_invalid_cnt = 0
        self._pos_detect_timer_id = 0
        self._init_time = t_util.time()
        return

    def init_from_dict(self, unit_obj, bdict):
        super(ComMoveSyncClient, self).init_from_dict(unit_obj, bdict)
        self._walk_state = bdict.get('walk_st', ())
        position = bdict.get('position') or (0, 0, 0)
        self.sd.ref_server_pos = math3d.vector(*position)

    def on_init_complete(self):
        if self.unit_obj.__class__.__name__ == 'LPuppet' and not global_data.player.is_in_global_spectate() and global_data.battle.__class__.__name__ == 'DeathBattle':
            self._start_pos_detect_timer()

    def destroy(self):
        self._server_pos = None
        self.sd.ref_server_pos = None
        self._stop_pos_detect_timer()
        super(ComMoveSyncClient, self).destroy()
        return

    def _on_roll_back_pos(self, lst_pos, i_reason=None):
        self._need_rb = True
        self._server_pos = lst_pos
        self._rb_reason = i_reason
        self.send_event('E_DO_RB_POS', lst_pos, i_reason)

    def _get_roll_back_info(self):
        if self._need_rb:
            return (self._server_pos, self._rb_reason)

    def _on_rb_done(self):
        self._need_rb = False

    def _get_walk_state(self):
        return self._walk_state

    def _on_sync_pos(self, t, idx, v3d_pos, *args):
        if idx <= self._pos_idx:
            return ESTOP
        self._pos_idx = idx
        self.sd.ref_server_pos = v3d_pos

    def _detect_sync_pos(self):
        if self.ev_g_ctrl_mecha():
            return
        else:
            logic_pos = self.ev_g_position()
            if not logic_pos or not self.sd.ref_server_pos:
                return
            diff = (logic_pos - self.sd.ref_server_pos).length
            if diff > NEOX_UNIT_SCALE * 5:
                self._pos_invalid_cnt += 1
                if 3 <= self._pos_invalid_cnt <= 10:
                    f = lambda p: (int(p.x), int(p.y), int(p.z)) if p else p
                    svr_pos = f(self.sd.ref_server_pos)
                    cli_pos = f(logic_pos)
                    recv_com = self.unit_obj.get_com('ComMoveSyncReceiver2')
                    recv_com_info = (recv_com._enable, recv_com.run_tick, f(recv_com._pos)) if recv_com else None
                    inplt_com = self.sd.ref_logic_movement
                    inplt_com_info = (inplt_com.src_t, f(inplt_com.cur_pos), len(inplt_com.buffer)) if inplt_com else None
                    model_info = (
                     self.ev_g_model() is not None, self.ev_g_animator() is not None)
                    info = (
                     self._pos_invalid_cnt, int(diff), self._init_time, svr_pos, cli_pos, self.sd.ref_teleport_info, recv_com_info, inplt_com_info, model_info)
                    global_data.player.logic.send_event('E_CALL_SYNC_METHOD', 'report_invalid_pos', (self.unit_obj.id, info))
            else:
                self._pos_invalid_cnt = 0
            return

    def _start_pos_detect_timer(self):
        self._stop_pos_detect_timer()
        from common.utils.timer import CLOCK
        from random import random
        interval = random() + 5
        self._pos_detect_timer_id = global_data.game_mgr.register_logic_timer(self._detect_sync_pos, interval, mode=CLOCK)

    def _stop_pos_detect_timer(self):
        if self._pos_detect_timer_id:
            global_data.game_mgr.unregister_logic_timer(self._pos_detect_timer_id)
            self._pos_detect_timer_id = 0