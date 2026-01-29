# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/pve/ComPveMechaBreakthrough.py
from __future__ import absolute_import
from logic.gcommon.component.UnitCom import UnitCom

class ComPveMechaBreakthrough(UnitCom):
    BIND_EVENT = {'E_SET_MECHA_BREAKTHROUGH_STATE': 'set_mecha_breakthrough_state',
       'G_MECHA_BREAKTHROUGH_DATA': 'get_mecha_breakthrough_state'
       }

    def __init__(self):
        super(ComPveMechaBreakthrough, self).__init__()
        self._slot_level_dict = {}

    def init_from_dict(self, unit_obj, bdict):
        super(ComPveMechaBreakthrough, self).init_from_dict(unit_obj, bdict)
        self._slot_level_dict = bdict.get('slot_level_dict', {})

    def set_mecha_breakthrough_state(self, state_dict):
        self._slot_level_dict.update(state_dict)
        global_data.emgr.pve_update_break_event.emit(state_dict)

    def get_mecha_breakthrough_state(self):
        return self._slot_level_dict

    def destroy(self):
        self._slot_level_dict = None
        super(ComPveMechaBreakthrough, self).destroy()
        return