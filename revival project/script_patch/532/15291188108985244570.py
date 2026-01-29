# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/avatarmembers/impReturn.py
from __future__ import absolute_import
from mobile.common.rpcdecorator import rpc_method, CLIENT_STUB
from mobile.common.RpcMethodArgs import List, Str
from logic.gcommon import time_utility as tutil
import common.utils.timer as timer

class impReturn(object):

    def _init_return_from_dict(self, bdict):
        self._return_buff_timestamp = bdict.get('return_buff_timestamp', 0)
        self._returntask_end_time = bdict.get('returntask_end_time', 0)
        self._return_discount_item = bdict.get('return_discount_item', [])
        self._return_bought_goods = bdict.get('return_bought_goods', None)
        self._mecha_gift_return_timestamp = bdict.get('mecha_gift_return_timestamp', 0)
        self._check_due_timer = None
        if self._return_buff_timestamp > 0:

            def buff_due_check_func():
                if tutil.get_server_time() < self._return_buff_timestamp:
                    return
                global_data.emgr.role_return_buff_update.emit()
                self._clear_due_timer()

            self._check_due_timer = global_data.game_mgr.register_logic_timer(buff_due_check_func, interval=33, times=-1, mode=timer.CLOCK)
        return

    def _destroy_return(self):
        self._clear_due_timer()

    def _clear_due_timer(self):
        if self._check_due_timer:
            global_data.game_mgr.unregister_logic_timer(self._check_due_timer)
            self._check_due_timer = None
        return

    def in_return(self):
        return tutil.get_server_time() < self._return_buff_timestamp

    def get_return_buff_due_time(self):
        return self._return_buff_timestamp

    def get_return_buff_left_time(self):
        return max(0, self._return_buff_timestamp - tutil.get_server_time())

    def has_return_task(self):
        return tutil.get_server_time() < self._returntask_end_time

    def get_return_task_left_time(self):
        return max(0, self._returntask_end_time - tutil.get_server_time())

    def get_return_mecha_gift_task_trigger_time(self):
        return self._mecha_gift_return_timestamp

    @rpc_method(CLIENT_STUB, (List('discount_item'),))
    def update_return_discount_item(self, discount_item):
        self._return_discount_item = discount_item

    def buy_return_goods_with_index(self, index):
        self.call_server_method('buy_return_goods', (index,))

    @rpc_method(CLIENT_STUB, (Str('goods_id'),))
    def buy_return_goods(self, goods_id):
        self._return_bought_goods = goods_id
        global_data.emgr.update_return_bought_goods_event.emit()

    def get_return_discount_item(self):
        return self._return_discount_item

    def get_new_return_buy_goods_id(self):
        return self._return_bought_goods