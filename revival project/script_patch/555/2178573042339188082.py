# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/avatarmembers/impVitality.py
from __future__ import absolute_import
from six.moves import range
from common.cfg import confmgr
from mobile.common.rpcdecorator import rpc_method, CLIENT_STUB
from mobile.common.RpcMethodArgs import Int, Bool, Dict
from logic.gcommon.item import item_const

class impVitality(object):

    def _init_vitality_from_dict(self, bdict):
        self._vitality_lv = bdict.get('day_vitality', {}).get('level', 0)
        self._vitality_point = bdict.get('day_vitality', {}).get('point', 0)
        self._vitality_reward = bdict.get('day_vitality_reward', {})
        self._week_vitality_lv = bdict.get('week_vitality', {}).get('level', 0)
        self._week_vitality_point = bdict.get('week_vitality', {}).get('point', 0)
        self._week_vitality_reward = bdict.get('week_vitality_reward', {})
        self._sum_vitality = bdict.get('sum_vitality', 0)

    def get_vitality_lv(self):
        return self._vitality_lv

    def get_vitality_point(self):
        return self._vitality_point

    def get_week_vitality_lv(self):
        return self._week_vitality_lv

    def get_week_vitality_point(self):
        return self._week_vitality_point

    def get_sum_vitality(self):
        return self._sum_vitality

    @rpc_method(CLIENT_STUB, (Int('new_lv'), Int('new_point'), Int('sum_vitality')))
    def update_day_vitality(self, new_lv, new_point, sum_vitality):
        old_lv = self._vitality_lv
        self._vitality_lv = new_lv
        self._vitality_point = new_point
        global_data.emgr.update_day_vitality_event.emit()
        vitality_conf = confmgr.get('vitality_conf', 'VitalityConfig', 'Content')
        for lv in range(old_lv + 1, new_lv + 1):
            reward = vitality_conf.get(str(lv), {}).get('reward', None)
            if reward:
                self._vitality_reward[str(lv)] = item_const.ITEM_UNRECEIVED
            else:
                self._vitality_reward[str(lv)] = item_const.ITEM_RECEIVED
            global_data.emgr.update_day_vitality_reward_event.emit(lv)

        old_sum_vitality = self._sum_vitality
        self._sum_vitality = sum_vitality
        global_data.emgr.sum_vitality_changed_event.emit()
        self.try_unlock_assess_task(old_sum_vitality, self._sum_vitality)
        return

    def receive_vitality_reward(self, lv):
        reward_st = self._vitality_reward.get(str(lv), item_const.ITEM_UNGAIN)
        if reward_st != item_const.ITEM_UNRECEIVED:
            return
        self.call_server_method('receive_vitality_reward', (int(lv),))

    @rpc_method(CLIENT_STUB, (Int('lv'), Bool('ret')))
    def receive_vitality_reward_ret(self, lv, ret):
        if ret:
            self._vitality_reward[str(lv)] = item_const.ITEM_RECEIVED
            global_data.emgr.update_day_vitality_reward_event.emit(lv)

    def get_vitality_reward_status(self, lv):
        return self._vitality_reward.get(str(lv), item_const.ITEM_UNGAIN)

    @rpc_method(CLIENT_STUB, (Dict('day_vitality'), Dict('day_vitality_reward')))
    def reset_day_vitality(self, day_vitality, day_vitality_reward):
        self._vitality_lv = day_vitality.get('level', 0)
        self._vitality_point = day_vitality.get('point', 0)
        self._vitality_reward = day_vitality_reward
        global_data.emgr.update_day_vitality_event.emit()
        vitality_conf = confmgr.get('vitality_conf', 'VitalityConfig', 'Content')
        for lv in range(1, len(vitality_conf) + 1):
            global_data.emgr.update_day_vitality_reward_event.emit(lv)

    @rpc_method(CLIENT_STUB, (Int('new_lv'), Int('new_point')))
    def update_week_vitality(self, new_lv, new_point):
        old_lv = self._week_vitality_lv
        self._week_vitality_lv = new_lv
        self._week_vitality_point = new_point
        global_data.emgr.update_week_vitality_event.emit()
        vitality_conf = confmgr.get('vitality_conf', 'WeekVitalityConfig', 'Content')
        for lv in range(old_lv + 1, new_lv + 1):
            reward = vitality_conf.get(str(lv), {}).get('reward', None)
            if reward:
                self._week_vitality_reward[str(lv)] = item_const.ITEM_UNRECEIVED
            else:
                self._week_vitality_reward[str(lv)] = item_const.ITEM_RECEIVED
            global_data.emgr.update_week_vitality_reward_event.emit(lv)

        return

    def receive_week_vitality_reward(self, lv):
        reward_st = self._week_vitality_reward.get(str(lv), item_const.ITEM_UNGAIN)
        if reward_st != item_const.ITEM_UNRECEIVED:
            return
        self.call_server_method('receive_week_vitality_reward', (int(lv),))

    @rpc_method(CLIENT_STUB, (Int('lv'), Bool('ret')))
    def receive_week_vitality_reward_ret(self, lv, ret):
        if ret:
            self._week_vitality_reward[str(lv)] = item_const.ITEM_RECEIVED
            global_data.emgr.update_week_vitality_reward_event.emit(lv)

    def get_week_vitality_reward_status(self, lv):
        return self._week_vitality_reward.get(str(lv), item_const.ITEM_UNGAIN)

    @rpc_method(CLIENT_STUB, (Dict('week_vitality'), Dict('week_vitality_reward')))
    def reset_week_vitality(self, week_vitality, week_vitality_reward):
        self._week_vitality_lv = week_vitality.get('level', 0)
        self._week_vitality_point = week_vitality.get('point', 0)
        self._week_vitality_reward = week_vitality_reward
        global_data.emgr.update_week_vitality_event.emit()
        vitality_conf = confmgr.get('vitality_conf', 'WeekVitalityConfig', 'Content')
        for lv in range(1, len(vitality_conf) + 1):
            global_data.emgr.update_week_vitality_reward_event.emit(lv)