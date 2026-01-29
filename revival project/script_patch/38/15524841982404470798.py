# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/avatarmembers/impSecretOrder.py
from __future__ import absolute_import
from six.moves import range
from mobile.common.rpcdecorator import rpc_method, CLIENT_STUB
from mobile.common.RpcMethodArgs import Int, Dict, List, Str, Bool
from logic.gcommon.common_const import activity_const as acconst
from logic.gcommon.common_const import notice_const
from logic.gcommon.ctypes.Record import Record
from logic.gcommon.ctypes.RewardRecord import RewardRecord
from logic.gcommon.common_const.battlepass_const import SECRET_ORDER_FREE, SECRET_ORDER_PAY

class impSecretOrder(object):

    def _init_secretorder_from_dict(self, bdict):
        self.secretorder_period = bdict.get('secretorder_period', 0)
        self.secretorder_point = bdict.get('secretorder_point', 0)
        self.secretorder_lv = bdict.get('secretorder_lv', 1)
        self.secretorder_types = bdict.get('secretorder_types', [])
        self.secretorder_reward_record = RewardRecord()
        self.secretorder_reward_record.init_from_dict(bdict.get('secretorder_reward_record', {}))
        self.daily_secretorder_point = bdict.get('daily_secretorder_point', 0)

    @rpc_method(CLIENT_STUB, (Int('secretorder_lv'),))
    def update_secretorder_data(self, secretorder_lv):
        self.secretorder_lv = secretorder_lv
        global_data.emgr.small_bp_update_lv.emit()
        global_data.emgr.refresh_activity_redpoint.emit()

    def active_secretorder_type(self):
        pass

    @rpc_method(CLIENT_STUB, (Str('reward_type'),))
    def on_active_secretorder_type(self, reward_type):
        self.secretorder_types.append(reward_type)
        global_data.emgr.small_bp_open_type.emit()

    def receive_secretorder_reward(self, secretorder_lv):
        self.call_server_method('receive_secretorder_reward', (secretorder_lv,))

    def receive_small_bp_reward_with_type(self, small_bp_lv, reward_type):
        self.call_server_method('receive_secretorder_reward', (reward_type, small_bp_lv))

    def receive_small_bp_reward(self):
        self.call_server_method('receive_all_secretorder_reward')

    @rpc_method(CLIENT_STUB, (Bool('ret'), Str('reward_type'), Int('secretorder_lv')))
    def receive_secretorder_reward_ret(self, ret, reward_type, secretorder_lv):
        if ret:
            self.secretorder_reward_record.setdefault(reward_type, Record())
            self.secretorder_reward_record[reward_type].record(secretorder_lv)
            global_data.emgr.small_bp_update_award.emit()

    @rpc_method(CLIENT_STUB, (Bool('ret'),))
    def receive_all_secretorder_reward_ret(self, ret):
        if ret:
            for lv in range(1, self.secretorder_lv + 1):
                for reward_type in [SECRET_ORDER_FREE, SECRET_ORDER_PAY]:
                    if reward_type == SECRET_ORDER_PAY and not self.secretorder_types:
                        continue
                    self.secretorder_reward_record.setdefault(reward_type, Record())
                    self.secretorder_reward_record[reward_type].record(lv)

            global_data.emgr.small_bp_update_award.emit()

    @rpc_method(CLIENT_STUB, (Int('now_period'),))
    def on_new_secretorder_period_start(self, new_period):
        self.secretorder_period = new_period
        self.secretorder_types = []
        self.secretorder_lv = 1
        self.secretorder_reward_record.clear()
        global_data.emgr.small_bp_new_period_start.emit()

    def has_buy_higher_small_bp(self):
        return len(global_data.player.secretorder_types) > 0

    def activate_small_bp_lv(self, add_lv):
        self.call_server_method('buy_secretorder_lv', (add_lv,))