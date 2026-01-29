# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/pve/ComPveMechaReset.py
from __future__ import absolute_import
from logic.gcommon.component.UnitCom import UnitCom

class ComPveMechaReset(UnitCom):
    BIND_EVENT = {'G_PVE_MECHA_RESET_TIME': '_get_pve_mecha_reset_time'
       }

    def __init__(self):
        super(ComPveMechaReset, self).__init__()
        self._pve_mecha_reset_time = 0

    def init_from_dict(self, unit_obj, bdict):
        super(ComPveMechaReset, self).init_from_dict(unit_obj, bdict)
        self._pve_mecha_reset_time = bdict.get('pve_mecha_reset_time', 0)
        if self._pve_mecha_reset_time > 0:
            global_data.ui_mgr.show_ui('PVEShopMechaUI', 'logic.comsys.battle.pve')

    def _get_pve_mecha_reset_time(self):
        return self._pve_mecha_reset_time