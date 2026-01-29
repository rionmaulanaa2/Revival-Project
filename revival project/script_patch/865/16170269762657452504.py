# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/avatarmembers/impMeow.py
from __future__ import absolute_import
from mobile.common.rpcdecorator import rpc_method, CLIENT_STUB
from mobile.common.RpcMethodArgs import Bool, Int, Str
from logic.gcommon.cdata import meow_capacity_config
from logic.gcommon.item import item_const

class impMeow(object):

    def _init_meow_from_dict(self, bdict):
        self._meow_capacity_lvs = bdict.get('meow_capacity_lvs', {})
        self._meow_week_carry_num = bdict.get('meow_week_carry_num', 0)

    def get_meow_capacity_lv(self, capacity_type):
        return self._meow_capacity_lvs.get(capacity_type, meow_capacity_config.capacity_init_lv)

    def update_meow_capacity_lv(self, capacity_type, lv):
        self._meow_capacity_lvs[capacity_type] = lv
        global_data.emgr.update_meow_capacity_lv.emit()

    def upgrade_meow_capacity(self, capacity_type):
        if not global_data.player:
            return
        if capacity_type not in meow_capacity_config.capacity_type_set:
            return
        cur_lv = self.get_meow_capacity_lv(capacity_type)
        next_lv = cur_lv + 1
        max_lv = meow_capacity_config.get_capacity_max_lv(capacity_type)
        if cur_lv < meow_capacity_config.capacity_init_lv or next_lv > max_lv:
            return
        need_item_num = meow_capacity_config.get_capacity_price(capacity_type, next_lv)
        if not global_data.player.has_enough_item(item_const.LOBBY_ITEM_NO_MEOW_COIN, need_item_num):
            return
        self.call_server_method('upgrade_meow_capacity', (capacity_type,))

    @rpc_method(CLIENT_STUB, (Bool('ret'), Str('capacity_type'), Int('lv')))
    def upgrade_meow_capacity_result(self, ret, capacity_type, lv):
        if ret:
            self.update_meow_capacity_lv(capacity_type, lv)

    def get_meow_week_info(self):
        from logic.gutils.item_utils import get_item_max_count_weekly
        from logic.gcommon.item.item_const import ITEM_NO_MEOW_COIN
        return (
         self._meow_week_carry_num, get_item_max_count_weekly(ITEM_NO_MEOW_COIN))

    @rpc_method(CLIENT_STUB, (Int('carry_num'),))
    def update_meow_week_carry_num(self, carry_num):
        self._meow_week_carry_num = carry_num