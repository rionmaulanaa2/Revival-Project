# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/avatarmembers/impFriendHelp.py
from __future__ import absolute_import
from hashlib import sha1
import json
from mobile.mobilerpc import SimpleHttpClient2, HttpBase
import game3d
from logic.gcommon.common_utils.local_text import get_cur_lang_name
from logic.gcommon.common_const import rank_const
from logic.gcommon import time_utility
from common import http
import six

class impFriendHelp(object):

    def _init_friendhelp_from_dict(self, bdict):
        self.FRD_HELP_URL = 'https://interact2.webapp.easebar.com/g93nashare'
        self.FRD_HELP_KEY = 'NzVBgAVZjOArcDA88qcRW89xgBPwytKT'
        self.httpclient = SimpleHttpClient2.SimpleAsyncHTTPClient2(max_clients=1)
        self.frd_share_url = None
        self.frd_thumbup = 0
        self.rank_version = 0
        self.last_req_time = 0
        return

    def _on_login_friendhelp_success(self):
        pass

    def init_basic_share_info(self):
        pass

    def request_share_url(self):
        pass

    def request_friendhelp_count(self):
        self.init_basic_share_info()
        now = time_utility.time()
        if now - self.last_req_time < 30:
            return
        self.last_req_time = now
        sign_key = self.user_id + self.share_type + self.FRD_HELP_KEY
        sign = sha1(six.ensure_binary(sign_key)).hexdigest()
        fields = {'uid': self.user_id,
           'share_type': self.share_type,
           'sign': sign
           }

        def cb(result, url, *args):
            rep = json.loads(result)
            status = rep.get('status', None)
            if status == 'OK':
                old_frd_thumbup = self.frd_thumbup
                self.frd_thumbup = rep.get('thumbup', 0)
                if old_frd_thumbup < self.frd_thumbup:
                    global_data.emgr.update_frd_thumbup.emit()
                    self.call_server_method('update_frd_thumbup', (self.frd_thumbup,))
            return

        url = '{0}/cus_game_query'.format(self.FRD_HELP_URL)
        http.request(url, callback=cb, fields=fields)

    def request_friendhelp_rank(self, count):
        self.init_basic_share_info()
        fields = {'limit': count
           }

        def cb(result, url, *args):
            rep = json.loads(result)
            success = rep.get('success', False)
            if success:
                ranks = rep.get('ranks', [])
                rank_list = list()
                for rank_data in ranks:
                    uid = rank_data.get('uid', None)
                    if not uid:
                        continue
                    name = rank_data.get('etc_info', {}).get('nickname', 'BLANK')
                    thumbup = rank_data.get('thumbup', 0)
                    rank_list.append([uid, name, thumbup])

                rank_type = rank_const.RANK_TYPE_FRIEND_HELP
                global_data.message_data.set_rank_data(rank_type, 0, count, 0, rank_list)
            return

        url = '{0}/query_rank'.format(self.FRD_HELP_URL)
        http.request(url, callback=cb, fields=fields)

    def get_frd_thumbup(self):
        return self.frd_thumbup

    def get_frd_share_url(self):
        return self.frd_share_url