# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/avatarmembers/impLoginRecord.py
from __future__ import absolute_import
from mobile.common.RpcMethodArgs import Str
from mobile.common.rpcdecorator import rpc_method, CLIENT_STUB
from mobile.common.RpcMethodArgs import Str, MailBox, Dict, Int, Bool, Uuid, List
from logic.gcommon.common_utils.local_text import get_cur_text_lang
from logic.gcommon import time_utility as tutil

class impLoginRecord(object):

    def _init_loginrecord_from_dict(self, bdict):
        char_name = self.get_name()
        uid = self.uid
        host_num = global_data.channel.get_host_num()
        record_value = {'uid': uid,'char_name': char_name,'host_num': host_num}
        global_data.achi_mgr.save_login_account_data_value('login_history', record_value)