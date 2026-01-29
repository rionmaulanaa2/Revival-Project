# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivityAICoCreation.py
from __future__ import absolute_import
from __future__ import print_function
import json
from re import S
from logic.client.const import mall_const
from logic.gutils import template_utils
from logic.gutils import item_utils
from logic.gutils import activity_utils
from common.cfg import confmgr
from logic.comsys.activity.ActivityTemplate import ActivityBase
from common import http
from hashlib import sha1
import six
import six.moves.urllib.request
import six.moves.urllib.parse
import six.moves.urllib.error
from mobile.mobilerpc import HttpBase, SimpleHttpClient2
from logic.gcommon import time_utility

class ActivityAICoCreation(ActivityBase):

    def on_init_panel(self):
        self.last_request = 0

        @self.panel.btn_go.unique_callback()
        def OnClick(btn, touch):
            self.get_share_url()

    def get_share_url(self):
        now = time_utility.get_time()
        if now - self.last_request < 10:
            return
        self.last_request = now
        player = global_data.player
        if not player:
            return
        url = 'https://test-g93ai.webapp.163.com/get_share_url' if global_data.is_inner_server else 'https://g93ai.webapp.163.com/get_share_url'
        headimg = player.get_head_frame()
        hostnum = global_data.channel.get_host_num()
        nick = player.get_name()
        role_id = player.uid
        level = player.get_lv()
        key = 'xcTUvqDbf0QZedfqN1C6kC2LsWTV8r6N'
        sign_str = str(headimg) + str(hostnum) + str(level) + str(nick) + str(role_id) + key
        sign = sha1(six.ensure_binary(sign_str)).hexdigest()
        doc = {'headimg': headimg,
           'hostnum': hostnum,
           'nick': str(nick),
           'role_id': str(role_id),
           'level': str(level),
           'sign': sign
           }
        http = SimpleHttpClient2.SimpleAsyncHTTPClient2()
        param = six.moves.urllib.parse.urlencode(doc)
        host = 'test-g93ai.webapp.163.com' if global_data.is_inner_server else 'g93ai.webapp.163.com'
        request = HttpBase.HttpRequest(host, 'GET', url + '?' + param, usessl=True)
        cb = lambda req, rep: self.get_url_cb(req, rep)
        http.http_request(request, 4, cb)

    def get_url_cb(self, req, rep):
        import game3d
        self.last_request = 0
        if rep is None or rep.header is None:
            return
        else:
            header = rep.header.dict
            body = rep.body
            try:
                content = json.loads(body)
            except Exception as e:
                print('[AICoCreation] json loads error:[%s]' % str(e))
                return

            url = content.get('share_url', None)
            game3d.open_url(str(url).strip())
            return