# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/avatarmembers/impLevel.py
from __future__ import absolute_import
from mobile.common.rpcdecorator import rpc_method, CLIENT_STUB
from mobile.common.RpcMethodArgs import Int, List
from logic.gcommon.ctypes.Record import Record

class impLevel(object):

    def _init_level_from_dict(self, bdict):
        self.lv = bdict.get('lv', 1)
        self.exp = bdict.get('exp', 0)
        self.lv_reward_record = Record(bdict.get('lv_reward_record', {}))
        self.duo_exp_point = bdict.get('duo_exp_point', 0)
        self.duo_exp_timestamp = bdict.get('duo_exp_timestamp', 0)

    def get_lv(self):
        return self.lv

    def get_exp(self):
        return self.exp

    def get_dup_exp_point(self):
        return self.duo_exp_point

    def get_duo_exp_timestamp(self):
        return self.duo_exp_timestamp

    @rpc_method(CLIENT_STUB, (Int('lv'), Int('exp')))
    def reset_lv(self, lv, exp):
        self.lv = lv
        self.exp = exp
        self.lv_reward_record.clear()

    def receive_lv_reward(self, lv):
        if self.lv < lv or self.lv_reward_record.is_record(lv):
            return False
        self.call_server_method('receive_lv_reward', (lv,))
        return True

    def receive_all_lv_reward(self):
        self.call_server_method('receive_all_lv_reward', ())

    @rpc_method(CLIENT_STUB, (Int('last_reward_lv'), List('lv_rewards')))
    def update_lv_rewards(self, last_reward_lv, lv_rewards):
        self.lv_reward_record.update(last_reward_lv, set(lv_rewards))

    def accept_to_add_exp(self):
        self.call_server_method('accept_to_add_exp', ())