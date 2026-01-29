# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/avatarmembers/impUdataGift.py
from __future__ import absolute_import
from mobile.common.rpcdecorator import rpc_method, CLIENT_STUB
from mobile.common.RpcMethodArgs import Str, Int, Bool, Dict, List
from logic.gcommon.common_const import shop_const
from logic.client.udata_gift import LotteryTenTry

class impUdataGift(object):

    def _init_udatagift_from_dict(self, bdict):
        lottery_10_try = bdict.get('udata_lottery_10_try', None)
        self._udata_lottery_gift = LotteryTenTry(lottery_10_try) if lottery_10_try else None
        return

    @rpc_method(CLIENT_STUB, (Dict('info'),))
    def update_lottery_10_try(self, info):
        if self._udata_lottery_gift:
            if not info:
                self._udata_lottery_gift = None
            else:
                self._udata_lottery_gift.update_from_dict(info)
                self._udata_lottery_gift.preview_reward()
        else:
            self._udata_lottery_gift = LotteryTenTry(info)
        global_data.emgr.lottery_ten_try_update.emit()
        return

    def determine_lottery_10_try(self, lottery_id, trigger):
        if not self._udata_lottery_gift or not self._udata_lottery_gift.wait_determine(lottery_id):
            return False
        if trigger:
            self.call_server_method('determine_lottery_10_try', ())
        return True

    def click_lottery_10_try_result(self):
        self.call_server_method('enter_lottery_10_try', ())

    def get_lottery_10_try_gift(self):
        return self._udata_lottery_gift