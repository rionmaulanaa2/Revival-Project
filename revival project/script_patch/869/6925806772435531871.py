# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/avatarmembers/impTitle.py
from __future__ import absolute_import
from logic.gcommon.common_const import title_const
from mobile.common.rpcdecorator import rpc_method, CLIENT_STUB
from mobile.common.RpcMethodArgs import Str, Int, Bool, List, Dict
from logic.gutils import title_utils

class impTitle(object):

    def _init_title_from_dict(self, bdict):
        self._cur_title_item_no = bdict.get('title_cur', None)
        return

    def _destroy_title(self):
        self._cur_title_item_no = None
        return

    def get_cur_title(self):
        return self._cur_title_item_no

    def try_set_title(self, title_item_no):
        if title_item_no is None:
            return
        else:
            if not title_utils.is_title(title_item_no):
                return
            self.call_server_method('try_set_title', (title_item_no,))
            return

    def try_take_off_cur_title(self):
        self.call_server_method('take_off_cur_title', ())

    @rpc_method(CLIENT_STUB, (Int('title_item_no'), Int('ret')))
    def on_set_title_ret(self, title_item_no, ret):
        if ret == title_const.TITLE_SET_OK:
            self._set_cur_title(title_item_no)

    @rpc_method(CLIENT_STUB, ())
    def take_off_cur_title(self):
        self._set_cur_title(None)
        return

    def _set_cur_title(self, title_item_no):
        prev = self._cur_title_item_no
        self._cur_title_item_no = title_item_no
        if prev != self._cur_title_item_no:
            global_data.emgr.cur_title_changed.emit(self._cur_title_item_no)