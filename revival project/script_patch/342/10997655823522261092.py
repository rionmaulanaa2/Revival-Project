# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/share/ComHidingData.py
from __future__ import absolute_import
from ..UnitCom import UnitCom
from .ComHealth import ComHealth

class ComHidingData(UnitCom):
    BIND_EVENT = {'E_HIDING_ADD_SOUL': '_add_soul',
       'E_HIDING_DEL_SOUL': '_del_soul',
       'G_HIDING_DEL_SOUL': '_del_soul',
       'G_HIDING_SOUL': '_get_soul'
       }

    def __init__(self):
        super(ComHidingData, self).__init__()
        self._soul_id = None
        return

    def init_from_dict(self, unit_obj, bdict):
        super(ComHidingData, self).init_from_dict(unit_obj, bdict)
        self._soul_id = bdict.get('soul_id', None)
        return

    def get_client_dict(self):
        cdict = {}
        if self._soul_id is not None:
            cdict['soul_id'] = self._soul_id
        return cdict

    def _add_soul(self, soul_id):
        if self._soul_id is not None:
            return False
        else:
            self._soul_id = soul_id
            return True

    def _del_soul(self):
        if self._soul_id is None:
            return
        else:
            ret = self._soul_id
            self._soul_id = None
            return ret

    def _get_soul(self):
        return self._soul_id