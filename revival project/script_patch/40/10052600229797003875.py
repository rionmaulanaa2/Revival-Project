# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/avatarmembers/impNotice.py
from __future__ import absolute_import
from mobile.common.rpcdecorator import rpc_method, CLIENT_STUB
from mobile.common.RpcMethodArgs import Int, Dict
from logic.gcommon.common_const import notice_const

class impNotice(object):

    def _init_notice_from_dict(self, bdict):
        self.notice_reward_map = dict()

    @rpc_method(CLIENT_STUB, (Int('notify_type'), Dict('notify_data'), Int('notice_idx')))
    def notify_delay_notice(self, notify_type, notify_data, notice_idx):
        if notify_type == notice_const.NOTICE_REWARD:
            item_no = notify_data['item_no']
            self.notice_reward_map[item_no] = notice_idx

    def trigger_delay_notice(self, notice_idx):
        self.call_server_method('trigger_delay_notice', (notice_idx,))

    def trigger_delay_notice_by_item_no(self, item_no):
        notice_idx = self.notice_reward_map.get(item_no, None)
        if notice_idx:
            self.trigger_delay_notice(notice_idx)
            self.notice_reward_map.pop(item_no)
        return