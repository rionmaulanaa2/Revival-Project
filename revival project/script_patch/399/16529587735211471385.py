# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/avatarmembers/impEnlist.py
from __future__ import absolute_import
from __future__ import print_function
import six
from mobile.common.rpcdecorator import rpc_method, CLIENT_STUB
from mobile.common.RpcMethodArgs import Dict, Int, Bool
from logic.gcommon import time_utility as tutil
from logic.gcommon.item import item_const
from data import c_recruit_data

class impEnlist(object):

    def _init_enlist_from_dict(self, bdict):
        self._enlist_from_uid = bdict.get('enlist_from_uid', 0)
        self._enlist_uids = set(bdict.get('enlist_uids', []))
        self._enlist_data = bdict.get('enlist_data', {})
        self._enlist_score = bdict.get('enlist_score', 0)
        self._enlist_reward_sts = set(bdict.get('enlist_reward_sts', []))
        self._enlist_verify_gift = bdict.get('enlist_verify_gift', 0)

    def get_enlist_score(self):
        return self._enlist_score

    def get_enlist_uids(self):
        return self._enlist_uids

    def has_enlist_verify_gift(self):
        if not self._enlist_verify_gift and self._enlist_from_uid:
            return True
        return False

    def get_enlist_from_uid(self):
        return self._enlist_from_uid

    def get_enlist_data(self, uid):
        return self._enlist_data.get(str(uid), 0)

    def try_enlist_from_code(self, code):
        print('>>> try_enlist_from_code', code)
        self.call_server_method('try_enlist_from_code', (code,))

    @rpc_method(CLIENT_STUB, (Int('enlist_from_uid'),))
    def on_enlist_verify(self, enlist_from_uid):
        print('>>> on_enlist_verify', enlist_from_uid)
        if enlist_from_uid < 0:
            return
        self._enlist_from_uid = enlist_from_uid
        global_data.emgr.message_on_enlist_verify.emit()

    def generate_enlist_code(self):
        return str(self.uid)

    def get_enlist_reward_st(self, score):
        if score in self._enlist_reward_sts:
            return item_const.ITEM_RECEIVED
        else:
            if score <= self._enlist_score:
                return item_const.ITEM_UNRECEIVED
            return item_const.ITEM_UNGAIN

    def receive_enlist_reward(self, score):
        self.call_server_method('receive_enlist_reward', (int(score),))

    @rpc_method(CLIENT_STUB, (Int('score'), Bool('ret')))
    def receive_enlist_reward_ret(self, score, ret):
        if ret:
            self._enlist_reward_sts.add(score)
        global_data.emgr.message_on_enlist_reward.emit()

    def receive_enlist_verify_gift(self):
        print('>>> receive_enlist_verify_gift')
        if self._enlist_verify_gift or not self._enlist_from_uid:
            return
        self.call_server_method('receive_enlist_verify_gift')

    @rpc_method(CLIENT_STUB, (Int('reward_id'), Bool('ret')))
    def receive_enlist_verify_gift_ret(self, reward_id, ret):
        if ret:
            self._enlist_verify_gift = reward_id
        global_data.emgr.message_on_enlist_verify_gift.emit()

    @rpc_method(CLIENT_STUB, (Int('Uid'), Int('score')))
    def receive_enlist_score(self, uid, score):
        self._enlist_data.setdefault(str(uid), 0)
        self._enlist_data[str(uid)] += score
        self._enlist_score += score
        global_data.emgr.message_on_enlist_score.emit()

    def on_enlist_share(self):
        self.call_server_method('enlist_share')

    @rpc_method(CLIENT_STUB, (Int('to_uid'),))
    def on_enlist_succ(self, to_uid):
        self._enlist_uids.add(to_uid)
        global_data.emgr.message_on_enlist_my.emit()

    def is_enlist_reward_all_received(self):
        reward_content = c_recruit_data.GetEnlistReward()
        for s_score in six.iterkeys(reward_content):
            if int(s_score) not in self._enlist_reward_sts:
                return False

        return True