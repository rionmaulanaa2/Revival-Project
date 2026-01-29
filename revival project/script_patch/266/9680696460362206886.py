# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/pve/ComPveItemSet.py
from __future__ import absolute_import
from logic.gcommon.component.UnitCom import UnitCom

class ComPveItemSet(UnitCom):
    BIND_EVENT = {'E_UPDATE_PVE_ITEM_SET': 'on_update_pve_item_set',
       'G_PVE_ITEM_SET': 'get_pve_item_set'
       }

    def __init__(self):
        super(ComPveItemSet, self).__init__()
        self.item_set = set([])

    def init_from_dict(self, unit_obj, bdict):
        super(ComPveItemSet, self).init_from_dict(unit_obj, bdict)
        self.item_set = set(bdict.get('pve_item_set', []))

    def on_update_pve_item_set(self, item_list):
        if len(item_list) > len(self.item_set):
            for item_no in item_list:
                if item_no not in self.item_set:
                    global_data.emgr.pve_update_item_set.emit(item_no)
                    break

        self.item_set = set(item_list)

    def get_pve_item_set(self):
        return self.item_set