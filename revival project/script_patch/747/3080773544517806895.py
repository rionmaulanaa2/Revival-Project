# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/avatarmembers/impGoldGift.py
from __future__ import absolute_import
import six
from mobile.common.rpcdecorator import rpc_method, CLIENT_STUB
from mobile.common.RpcMethodArgs import Str, List, Bool, Int
from logic.gcommon import time_utility as tutil

class impGoldGift(object):

    def _init_goldgift_from_dict(self, bdict):
        self._friend_gold_gift = {int(str_uid):timestamp for str_uid, timestamp in six.iteritems(bdict.get('friend_gold_gift', {}))}
        self._send_friend_gold_gift_uids = set([ int(str_uid) for str_uid in six.iterkeys(bdict.get('send_friend_gold_gift_data', {})) ])
        self._is_recv_friend_gold_gift_limit = bdict.get('is_recv_friend_gold_gift_limit', False)

    @rpc_method(CLIENT_STUB, ())
    def reset_gold_gift_per_day(self):
        self._send_friend_gold_gift_uids = set()
        self._is_recv_friend_gold_gift_limit = False
        global_data.emgr.message_send_friend_gold_gift.emit()

    def is_recv_friend_gold_gift_limit(self):
        return self._is_recv_friend_gold_gift_limit

    def can_send_gold_gift(self, uid):
        if len(self._send_friend_gold_gift_uids) > 10:
            return False
        return uid not in self._send_friend_gold_gift_uids

    def has_send_gold_gift(self, uid):
        return uid in self._send_friend_gold_gift_uids

    def get_friend_gold_gift(self):
        return self._friend_gold_gift

    def request_send_friend_gold_gift(self, uid):
        if uid in self._send_friend_gold_gift_uids:
            return False
        self.call_server_method('request_send_friend_gold_gift', (uid,))
        return True

    @rpc_method(CLIENT_STUB, (Int('uid'), Bool('result')))
    def respon_send_friend_gold_gift(self, uid, result):
        if result:
            self._send_friend_gold_gift_uids.add(uid)
            player_inf = global_data.message_data.get_player_simple_inf(uid) or {}
            name = player_inf.get('char_name', '')
            self.notify_client_message((pack_text(3204, {'name': name}),))
        else:
            self.notify_client_message((pack_text(3208),))
        global_data.emgr.message_send_friend_gold_gift.emit()

    @rpc_method(CLIENT_STUB, (Int('uid'), Int('timestamp')))
    def on_friend_gold_gift(self, uid, timestamp):
        self._friend_gold_gift[uid] = timestamp
        global_data.emgr.message_on_friend_gold_gift.emit()

    def request_receive_all_friend_gold_gift(self):
        if not self._friend_gold_gift:
            return False
        self.call_server_method('request_receive_all_friend_gold_gift', ())
        return True

    @rpc_method(CLIENT_STUB, (List('receive_uids'), Bool('result'), Bool('is_recv_limt')))
    def respon_receive_all_friend_gold_gift(self, receive_uids, result, is_recv_limt):
        from logic.comsys.message import GoldFeedback
        self._is_recv_friend_gold_gift_limit = is_recv_limt
        if result:
            for uid in receive_uids:
                self._friend_gold_gift.pop(uid, None)
                self._send_friend_gold_gift_uids.add(uid)

            GoldFeedback.GoldFeedback(None)
        elif not receive_uids:
            self._friend_gold_gift.clear()
        global_data.emgr.message_recv_friend_gold_gift.emit()
        return

    def request_receive_friend_gold_gift(self, uid):
        if uid not in self._friend_gold_gift:
            return False
        self.call_server_method('request_receive_friend_gold_gift', (uid,))
        return True

    @rpc_method(CLIENT_STUB, (Int('uid'), Bool('result'), Bool('is_recv_limt')))
    def respon_receive_friend_gold_gift(self, uid, result, is_recv_limt):
        from logic.comsys.message import GoldFeedback
        self._is_recv_friend_gold_gift_limit = is_recv_limt
        self._friend_gold_gift.pop(uid, None)
        self._send_friend_gold_gift_uids.add(uid)
        global_data.emgr.message_recv_friend_gold_gift.emit()
        if result:
            GoldFeedback.GoldFeedback(None, uid=uid)
        return