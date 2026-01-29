# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComBeacon8031BloodUI.py
from __future__ import absolute_import
from logic.gcommon.component.client.ComMechaBloodUI import ComMechaBloodUI

class ComBeacon8031BloodUI(ComMechaBloodUI):

    def init_from_dict(self, unit_obj, bdict):
        super(ComBeacon8031BloodUI, self).init_from_dict(unit_obj, bdict)
        self.owner_id = bdict.get('owner_eid', None)
        return

    def _get_socket(self):
        return ('fx_xb', 40)

    def _blood_bar_load_callback(self, model, *args):
        if not model:
            return
        super(ComBeacon8031BloodUI, self)._blood_bar_load_callback(model, *args)
        if global_data.mecha and global_data.mecha.id == self.owner_id:
            return
        if global_data.player and global_data.player.logic and not self.ev_g_is_campmate(global_data.player.logic.ev_g_camp_id()):
            self._on_show_hp_info_warpper()