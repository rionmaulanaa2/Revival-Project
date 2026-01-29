# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/ctypes/WpThrowable.py
from __future__ import absolute_import
from .Weapon import Weapon
from logic.gcommon.const import ATK_THROWABLE
from logic.gcommon.common_const.weapon_const import WP_THROWABLE

class WpThrowable(Weapon):

    def __init__(self, weapon_data, battle):
        super(WpThrowable, self).__init__(weapon_data)
        self.iAtkMode = ATK_THROWABLE
        self.iType = self._data['item_id']

    def get_config(self, *args):
        if self._conf:
            return self._conf
        _conf = {}
        if G_IS_CLIENT:
            import common.cfg.confmgr as confmgr
            d = confmgr.get('grenade_config', str(self.iType))
            if not d:
                pass
            else:
                _conf.update(d)
        self._conf = _conf
        return self._conf

    def get_kind(self):
        return WP_THROWABLE