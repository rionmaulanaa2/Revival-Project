# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/avatarmembers/impWeeklyCard.py
from __future__ import absolute_import
from logic.gcommon import time_utility as tutil
from logic.gcommon.common_const import activity_const as acconst
from mobile.common.rpcdecorator import rpc_method, CLIENT_STUB
from mobile.common.RpcMethodArgs import Bool, Int
from common.platform.appsflyer import Appsflyer
from common.platform.appsflyer_const import AF_WEEKCARD

class impWeeklyCard(object):

    def _init_weeklycard_from_dict(self, bdict):
        self._weeklycard = bdict.get('weeklycard', 0)
        self._gold_weeklycard = bdict.get('gold_weeklycard', 0)
        self._weeklycard_daily = bdict.get('weeklycard_daily')
        self._weeklycard_times = bdict.get('weeklycard_times')
        self._weeklycard_payed = bdict.get('weeklycard_payed', False)

    def has_gold_weeklycard(self):
        return self._gold_weeklycard > tutil.get_server_time()

    def get_gold_weeklycard_time(self):
        return self._gold_weeklycard

    def has_weeklycard(self):
        return self._weeklycard > tutil.get_server_time()

    def get_weeklycard_time(self):
        return self._weeklycard

    def try_get_weeklycard_daily_reward(self):
        self.call_server_method('get_weeklycard_daily_reward', ())

    @rpc_method(CLIENT_STUB, (Bool('state'),))
    def update_weeklycard_daily(self, state):
        self._weeklycard_daily = state
        global_data.emgr.update_weekly_card_info.emit()

    @rpc_method(CLIENT_STUB, ())
    def update_weeklycard_sunday(self):
        self._weeklycard_payed = False

    @rpc_method(CLIENT_STUB, (Int('weeklycard'), Int('weeklycard_times')))
    def on_add_weeklycard(self, weeklycard, weeklycard_times):
        self._weeklycard = weeklycard
        self._weeklycard_times = weeklycard_times
        self._weeklycard_payed = True
        global_data.emgr.update_weekly_card_info.emit()
        global_data.emgr.role_add_card_attr_update_event.emit()
        Appsflyer().advert_track_event(AF_WEEKCARD)

    @rpc_method(CLIENT_STUB, (Int('gold_weeklycard'),))
    def on_add_gold_weeklycard(self, gold_weeklycard):
        self._gold_weeklycard = gold_weeklycard

    def is_first_time_buy_weeklycard(self):
        return self._weeklycard_times == 0

    def get_weekly_card_buy_count(self):
        return self._weeklycard_times

    def get_weeklycard_payed(self):
        return self._weeklycard_payed