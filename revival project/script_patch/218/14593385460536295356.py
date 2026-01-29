# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/avatarmembers/impVote.py
from __future__ import absolute_import
import six
import data
from logic.gutils import micro_webservice_utils
from mobile.common.rpcdecorator import rpc_method, CLIENT_STUB
from mobile.common.RpcMethodArgs import Bool, Str, Int
from logic.gcommon.common_const.web_const import COUNT_SERVICE_REQ_ADD, COUNT_SERVICE_REQ_GET_REAL, COUNT_SERVICE_REQ_GET_VIRTUAL, COUNT_SERVICE_REQ_GET
import time
from common.cfg import confmgr

class impVote(object):

    def _init_vote_from_dict(self, bdict):
        self._vote_dict = {}
        self._vote_key_list = []
        self._count_service_data = {}

    def _on_login_vote_success(self):
        self._count_service_data = confmgr.get('count_service_data', default={})
        for key, _ in six.iteritems(self._count_service_data):
            if self.check_vote_time(key):
                self._vote_key_list.append(key)

        for key in self._vote_key_list:
            self.get_vote_data(key)

    def check_vote_time(self, key):
        from logic.gcommon import time_utility
        now = time_utility.time()
        start_time = self._count_service_data.get(key, {}).get('start_time', 0)
        end_time = self._count_service_data.get(key, {}).get('end_time', 0)
        if start_time <= now and end_time >= now:
            return True
        return False

    def do_vote(self, item_id, cnt, vote_key):
        if not self.check_vote_time(vote_key):
            return
        if self.get_item_num_by_no(item_id) > 0:
            self.call_server_method('request_vote', (item_id, cnt, vote_key))
            vote_data = self._vote_dict.setdefault(vote_key, {})
            vote_data.setdefault('cnt', 0)
            vote_data['cnt'] += cnt

    @rpc_method(CLIENT_STUB, (Bool('status'), Int('cnt'), Str('vote_key')))
    def response_vote(self, status, cnt, vote_key):
        if status:
            micro_webservice_utils.micro_service_request('CountService', {'req_type': COUNT_SERVICE_REQ_ADD,'cid': vote_key,'aval': cnt})

    def get_vote_data(self, vote_key):
        if not self.check_vote_time(vote_key):
            if global_data.is_inner_server:
                global_data.game_mgr.show_tip('\xe8\xae\xa1\xe7\xa5\xa8\xe6\x97\xb6\xe9\x97\xb4\xe8\xbf\x87\xe4\xba\x86\xef\xbc\x8c\xe6\xb4\xbb\xe5\x8a\xa8\xe8\xbf\x98\xe5\xbc\x80\xe7\x9d\x80\xef\xbc\x8c\xe6\xa3\x80\xe6\x9f\xa5\xe4\xb8\x8b\xe8\xa1\xa8\xe9\x87\x8c\xe5\xa1\xab\xe7\x9a\x84\xe6\x97\xb6\xe9\x97\xb4\xef\xbc\x81\xef\xbc\x81\xef\xbc\x81')
            return 0
        vote_data = self._vote_dict.get(vote_key)
        if not vote_data or time.time() - vote_data.get('last_requset_time', 0) >= 5:
            self._vote_dict.setdefault(vote_key, {})
            self._vote_dict[vote_key]['last_requset_time'] = time.time()
            micro_webservice_utils.micro_service_request('CountService', {'req_type': COUNT_SERVICE_REQ_GET_VIRTUAL,'cid': vote_key}, self.get_vote_data_cb)
        if vote_data:
            return vote_data.get('cnt', 0)
        return 0

    def get_vote_data_cb(self, res, rawdata=None):
        if rawdata:
            vote_key = rawdata.get('cid', None) if 1 else None
            return vote_key or None
        else:
            if res and res.get('msg', '') == 'success':
                data = res.get('data', {})
                if vote_key:
                    vote_data = self._vote_dict.setdefault(vote_key, {})
                    vote_data.setdefault('cnt', 0)
                    vote_data['cnt'] = max(data, self._vote_dict[vote_key]['cnt'])
            return