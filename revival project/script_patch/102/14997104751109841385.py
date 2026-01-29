# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComFirepower.py
from __future__ import absolute_import
from ..UnitCom import UnitCom
from common.cfg import confmgr
import logic.gcommon.time_utility as tutil

class ComFirepower(UnitCom):
    BIND_EVENT = {'E_SYNC_FIREPOWER': '_sync_firepower'
       }

    def __init__(self):
        super(ComFirepower, self).__init__(need_update=True)
        conf = confmgr.get('death_battle_config', 'Firepower', 'Content')
        self._fight_state_time = conf.get('fight_state_time', {}).get('value', 0)
        self._fight_dec = conf.get('fight_dec', {}).get('value', 0)
        self._no_fight_dec = conf.get('not_fight_dec', {}).get('value', 0)

    def init_from_dict(self, unit_obj, bdict):
        super(ComFirepower, self).init_from_dict(unit_obj, bdict)
        self._cur_power = bdict.get('firepower', 0)
        self._last_fight_time = bdict.get('firepower_last_fight', 0)

    def _sync_firepower(self, cur_power, is_fight):
        self._cur_power = cur_power
        if is_fight:
            self._last_fight_time = tutil.time()
        self.refresh_ui()

    def tick(self, dt):
        if self._cur_power <= 0:
            return
        now = tutil.time()
        if now - self._last_fight_time < self._fight_state_time:
            dec = self._fight_dec
        else:
            dec = self._no_fight_dec
        self._cur_power = max(0, self._cur_power - dec * dt)
        self.refresh_ui()

    def refresh_ui(self):
        if not global_data.cam_lplayer:
            return
        if global_data.cam_lplayer.id == self.unit_obj.id:
            ui = global_data.ui_mgr.get_ui('DeathAttentionUI')
            if ui:
                ui.set_fire_power(self._cur_power)