# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComMechaRepair.py
from __future__ import absolute_import
from ..UnitCom import UnitCom
from ...cdata import mecha_status_config
from logic.gcommon.common_const.mecha_const import REPAIR_FULL_ROUND, REPAIR_ROUND_ITVL
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gcommon.const import NEOX_UNIT_SCALE
MAX_REPAIR_ENERGY = REPAIR_FULL_ROUND * REPAIR_ROUND_ITVL

class ComMechaRepair(UnitCom):
    BIND_EVENT = {'E_MECHA_HEALING': '_start_healing',
       'E_CANCEL_HEALING': '_cancel_healing',
       'G_REPAIR_ENGERY': '_get_repair_energy'
       }

    def __init__(self):
        super(ComMechaRepair, self).__init__()
        self._start_healing_pos = None
        self._repairing = False
        return

    def destroy(self):
        super(ComMechaRepair, self).destroy()

    def init_from_dict(self, unit_obj, bdict):
        super(ComMechaRepair, self).init_from_dict(unit_obj, bdict)
        self.repair_energy = bdict.get('repair_energy', MAX_REPAIR_ENERGY)

    def _start_healing(self):
        if not self.ev_g_status_try_trans(mecha_status_config.MC_HEALING):
            return False
        else:
            self._repairing = True
            self._start_healing_pos = self.ev_g_position()
            if G_POS_CHANGE_MGR:
                self.unit_obj.regist_pos_change(self._mecha_move_helper, 0.1)
            else:
                self.unit_obj.regist_event('E_POSITION', self._mecha_move_helper)
            if global_data.player and global_data.player.logic:
                global_data.player.logic.send_event('E_SHOW_PROGRESS', 3, None, get_text_by_id(10145), self._finish_healing, self._cancel)
            self.send_event('E_CALL_SYNC_METHOD', 'mecha_start_repair', (), True)
            return True

    def _finish_healing(self):
        if not self._repairing:
            return
        self.send_event('E_CALL_SYNC_METHOD', 'mecha_finish_repair', (), True)
        self.ev_g_cancel_state(mecha_status_config.MC_HEALING)
        if G_POS_CHANGE_MGR:
            self.unit_obj.unregist_pos_change(self._mecha_move_helper)
        else:
            self.unit_obj.unregist_event('E_POSITION', self._mecha_move_helper)
        self.send_event('E_MECHA_REPAIR_ENERGY_CHANGED', -REPAIR_ROUND_ITVL)
        self._repairing = False

    def _cancel(self, *args):
        self.send_event('E_CANCEL_HEALING')

    def _cancel_healing(self):
        self.ev_g_cancel_state(mecha_status_config.MC_HEALING)
        if G_POS_CHANGE_MGR:
            self.unit_obj.unregist_pos_change(self._mecha_move_helper)
        else:
            self.unit_obj.unregist_event('E_POSITION', self._mecha_move_helper)
        if global_data.player and global_data.player.logic:
            global_data.player.logic.send_event('E_CLOSE_PROGRESS')

    def _mecha_move_helper(self, new_pos, interrupt_dist=5 * NEOX_UNIT_SCALE):
        if self._start_healing_pos:
            if (new_pos - self._start_healing_pos).length > interrupt_dist:
                self._cancel_healing()
        else:
            self._start_healing_pos = new_pos

    def _get_repair_energy(self):
        return self.repair_energy