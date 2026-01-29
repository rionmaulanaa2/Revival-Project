# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/share/ComHealthSync.py
from __future__ import absolute_import
from .ComHealth import ComHealth

class ComHealthSync(ComHealth):
    BIND_EVENT = ComHealth.BIND_EVENT.copy()
    BIND_EVENT.update({'E_HEALTH_HP_CHANGE': 'sync_hp'
       })

    def sync_hp(self, hp, mod):
        if G_IS_SERVER:
            self.send_event('E_CALL_SYNC_METHOD', 'on_hp_change', (hp,), False, True)