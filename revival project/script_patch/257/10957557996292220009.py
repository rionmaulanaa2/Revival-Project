# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/share/ComBuildingData.py
from __future__ import absolute_import
from ..UnitCom import UnitCom
from logic.gcommon.common_const import building_const

class ComBuildingData(UnitCom):
    BIND_EVENT = {'E_BUILDING_CHANGE_HP': 'change_hp',
       'G_BUILDING_CHANGE_HP': 'change_hp',
       'S_BUILDING_HPMAX': 'set_hpmax',
       'E_BUILDING_DONE': 'on_done',
       'G_HP': 'get_hp',
       'G_HP_MAX': 'get_hp_max'
       }

    def init_from_dict(self, unit_obj, bdict):
        super(ComBuildingData, self).init_from_dict(unit_obj, bdict)
        self.building_no = bdict.get('building_no')
        self._hp = bdict.get('hp')
        self._hpmax = bdict.get('max_hp')
        self._status = bdict.get('status')

    def set_hpmax(self, val):
        self._hpmax = val

    def change_hp(self, val):
        self._hp += val
        self._hp = min(self._hp, self._hpmax)
        self._hp = max(self._hp, 0)
        return self._hp

    def on_done(self):
        self._status = building_const.BUILDIND_ST_DONE

    def get_client_dict(self):
        return {'hp': self._hp,
           'max_hp': self._hpmax,
           'status': self._status
           }

    def get_hp(self):
        return self._hp

    def get_hp_max(self):
        return self._hpmax