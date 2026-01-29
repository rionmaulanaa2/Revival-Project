# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/avatarmembers/impCDKey.py
from __future__ import absolute_import
from mobile.common.rpcdecorator import rpc_method, CLIENT_STUB
from mobile.common.RpcMethodArgs import Int
from logic.gcommon import time_utility
import math
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.client.const.mall_const import CDKEY_GIFT_CODE2_TIP, CDKEY_GIFT_DEFAULT_ERR_TIP

class impCDKey(object):

    def _init_cdkey_from_dict(self, bdict):
        self._enable_cdkey_gift = bdict.get('enable_cdkey_gift', False)

    def active_cdkey_gift(self, sn):
        self.call_server_method('active_cdkey_gift', (sn,))

    @rpc_method(CLIENT_STUB, (Int('retcode'),))
    def active_gift_ret(self, retcode):
        tip_text = CDKEY_GIFT_CODE2_TIP.get(retcode, CDKEY_GIFT_DEFAULT_ERR_TIP)
        global_data.game_mgr.show_tip(get_text_by_id(tip_text))

    def has_enable_cdkey_gift(self):
        return self._enable_cdkey_gift