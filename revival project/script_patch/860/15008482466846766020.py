# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComHitStun.py
from __future__ import absolute_import
from ..UnitCom import UnitCom
import logic.gcommon.time_utility as t_util

class ComHitStun(UnitCom):
    BIND_EVENT = {'S_STUN': 'set_stun',
       'G_STUN': 'get_stun',
       'G_MAX_STUN': 'get_max_stun'
       }

    def __init__(self):
        super(ComHitStun, self).__init__(need_update=False)
        self._stun = 0
        self._max_stun = 0

    def init_from_dict(self, unit_obj, bdict):
        super(ComHitStun, self).init_from_dict(unit_obj, bdict)
        self._max_stun = int(bdict.get('max_stun', 0))
        self._stun = int(bdict.get('stun', self._max_stun))

    def set_stun(self, stun):
        stun = min(max(0, stun), self._max_stun)
        if stun == self._stun:
            return
        mod = stun - self._stun
        self._stun = stun
        self.send_event('E_STUN_CHANGE', self._stun, mod)

    def get_stun(self):
        return self._stun

    def get_max_stun(self):
        return self._max_stun