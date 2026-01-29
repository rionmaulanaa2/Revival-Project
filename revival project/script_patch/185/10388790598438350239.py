# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComMoveSyncAnimRateSender.py
from __future__ import absolute_import
from ..UnitCom import UnitCom
from logic.gcommon import time_utility as t_util
from logic.gutils.sync.TriggerBox import TriggerBox
from logic.gcommon.common_const.character_anim_const import UP_BODY, LOW_BODY

class ComMoveSyncAnimRateSender(UnitCom):
    BIND_EVENT = {'E_ACTION_SYNC_ANIM_RATE': '_on_sync_anim_rate'
       }

    def __init__(self):
        super(ComMoveSyncAnimRateSender, self).__init__(need_update=True)
        self._upper_trigger = TriggerBox(min_itvl=0.2, min_delta=0.5, max_stay=0.4)
        self._upper_trigger.set_callback(self.on_tri_rate_upper)
        self._lower_trigger = TriggerBox(min_itvl=0.2, min_delta=0.5, max_stay=0.4)
        self._lower_trigger.set_callback(self.on_tri_rate_lower)

    def destroy(self):
        self._upper_trigger.destroy()
        self._lower_trigger.destroy()
        super(ComMoveSyncAnimRateSender, self).destroy()

    def init_from_dict(self, unit_obj, bdict):
        super(ComMoveSyncAnimRateSender, self).init_from_dict(unit_obj, bdict)

    def _on_sync_anim_rate(self, part_of_body, f_rate):
        t = t_util.time()
        if part_of_body == UP_BODY:
            self._upper_trigger.input(t, f_rate)
        else:
            self._lower_trigger.input(t, f_rate)

    def on_tri_rate_upper(self, t, f_rate):
        self.send_event('E_CALL_SYNC_METHOD', 'on_sync_anim_rate', (UP_BODY, f_rate), True)

    def on_tri_rate_lower(self, t, f_rate):
        self.send_event('E_CALL_SYNC_METHOD', 'on_sync_anim_rate', (LOW_BODY, f_rate), True)

    def tick(self, dt):
        now = global_data.game_time_wrapped
        self._upper_trigger.check_trigger(now)
        self._lower_trigger.check_trigger(now)