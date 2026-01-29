# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/avatarmembers/impMigrateAccount.py
from __future__ import absolute_import
from __future__ import print_function
import base64
import hashlib
import hmac
import json
from time import time
from common import http
from logic.gutils.micro_webservice_utils import get_micros_service_url
from mobile.common.rpcdecorator import rpc_method, CLIENT_STUB
from mobile.common.RpcMethodArgs import Str

def migrate_result(res, rawdata=None):
    print(('migrate_result', res, rawdata))


class impMigrateAccount(object):

    def _init_migrateaccount_from_dict(self, bdict):
        self.migrate_url = 'https://h5-change-channel.webapp.163.com/apply/view?ticket={}'
        if global_data.is_inner_server:
            self.migrate_url = 'https://h5-change-channel-test.webapp.163.com/apply/view?ticket={}'

    @rpc_method(CLIENT_STUB, (Str('ticket'),))
    def get_migrate_ticket(self, ticket):
        url = self.migrate_url.format(ticket)
        print(('get_migrate_ticket', url))
        import game3d
        game3d.open_url(url)