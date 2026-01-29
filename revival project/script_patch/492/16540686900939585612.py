# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/avatarmembers/impYueka.py
from __future__ import absolute_import
from common.cfg import confmgr
from mobile.common.rpcdecorator import rpc_method, CLIENT_STUB
from mobile.common.RpcMethodArgs import Bool, Int
from logic.gcommon import time_utility
from common.platform.appsflyer import Appsflyer
from common.platform.appsflyer_const import AF_CONTINUE_MONTHCARD, AF_MONTHCARD
from logic.gcommon.common_const import shop_const
from logic.gcommon.common_const import activity_const

class impYueka(object):

    def _init_yueka_from_dict(self, bdict):
        self.yueka_daily = bdict.get('yueka_daily')
        self._yueka_time = bdict.get('yueka_time', 0)
        self._yueka_buy_times = bdict.get('yueka_buy_times', 0)
        self._yueka_daily_yuanbao_cnt = bdict.get('yueka_daily_yuanbao_cnt', 0)
        self._yueka_test = bdict.get('yueka_daily_test_group', False)
        conf = confmgr.get('c_activity_config', activity_const.ACTIVITY_YUEKA_HALF_PRICE_ART_COLLECT_SINGLE_LOTTERY, default={})
        self._yueka_test_end_time = conf.get('cEndTime', 0)

    def has_yueka(self):
        return time_utility.get_server_time() < self._yueka_time

    def is_yueka_test(self):
        if time_utility.time() > self._yueka_test_end_time:
            return False
        return self._yueka_test

    def get_yueka_time(self):
        return self._yueka_time

    def try_get_yueka_daily_reward(self):
        self.call_server_method('get_yueka_daily_reward', ())

    @rpc_method(CLIENT_STUB, (Bool('state'),))
    def update_yueka_daily(self, state):
        self.yueka_daily = state
        global_data.emgr.update_month_card_info.emit()

    @rpc_method(CLIENT_STUB, (Int('yueka_time'), Int('yueka_buy_times'), Bool('is_continue')))
    def on_add_yueka(self, yueka_time, yueka_buy_times, is_continue):
        self._yueka_time = yueka_time
        self._yueka_buy_times = yueka_buy_times
        if is_continue:
            Appsflyer().advert_track_event(AF_CONTINUE_MONTHCARD)
        else:
            Appsflyer().advert_track_event(AF_MONTHCARD)
        global_data.emgr.update_month_card_info.emit()
        global_data.emgr.role_add_card_attr_update_event.emit()
        global_data.emgr.refresh_activity_redpoint.emit()

    def is_first_time_buy_yueka(self):
        return self._yueka_buy_times == 0

    def has_yueka_lottery_discount(self, lottery_id, discount_item_no=shop_const.GOOD_ID_LOTTERY_HALF_PRICE):
        if not self.is_yueka_test() and discount_item_no == shop_const.GOODS_ID_ART_COLLECTION_LOTTERY_HALF_PRICE:
            return False
        if self.is_yueka_test() and discount_item_no == shop_const.GOOD_ID_LOTTERY_HALF_PRICE:
            return False
        if self._yueka_time <= time_utility.get_time():
            return False
        if self.get_per_day_num(str(discount_item_no)) > 0:
            return False
        if self.is_over_max_buy_num_per_lottery(str(lottery_id), str(discount_item_no)):
            return False
        return True

    def get_yueka_buy_count(self):
        return self._yueka_buy_times

    @rpc_method(CLIENT_STUB, (Int('cnt'),))
    def update_yueka_yuanbao_cnt(self, cnt):
        self._yueka_daily_yuanbao_cnt = cnt
        global_data.emgr.update_month_card_info.emit()

    def get_yueka_yuanbao_cnt(self):
        return self._yueka_daily_yuanbao_cnt

    def yueka_daily_yuanbao(self):
        return self._yueka_daily_yuanbao_cnt > 0