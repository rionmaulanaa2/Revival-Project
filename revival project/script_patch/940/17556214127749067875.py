# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/avatarmembers/impBrandLevel.py
from __future__ import absolute_import
from common.cfg import confmgr
from mobile.common.rpcdecorator import rpc_method, CLIENT_STUB
from mobile.common.RpcMethodArgs import Int, Bool
from logic.gcommon.item import item_const
from logic.gcommon.common_const.activity_const import BRAND_CNT

class impBrandLevel(object):

    def _init_brandlevel_from_dict(self, bdict):
        self.brand_level = bdict.get('brand_level', 1)
        self.open_brand_by_level = bdict.get('open_brand_by_level', {})
        self.core_reward_st = bdict.get('core_reward_st', {})
        self.core_brand_record = bdict.get('core_brand_record', {})

    def try_open_brand(self, level, row, column):
        if level != self.brand_level:
            return
        else:
            idx = row * BRAND_CNT + column
            if idx >= BRAND_CNT * BRAND_CNT:
                return
            if idx in self.open_brand_by_level.get(str(level), []):
                return
            core_reward_st = self.core_reward_st.get(str(level), None)
            if core_reward_st and (core_reward_st == item_const.ITEM_RECEIVED or core_reward_st == item_const.ITEM_UNRECEIVED):
                return
            self.call_server_method('open_brand', (level, row, column))
            return

    @rpc_method(CLIENT_STUB, (Int('level'), Int('row'), Int('column'), Bool('open_core_reward')))
    def open_brand_ret(self, level, row, column, open_core_reward):
        self.on_open_brand_ret(level, row, column, open_core_reward)

    def on_open_brand_ret(self, level, row, column, open_core_reward):
        self.open_brand_by_level.setdefault(str(level), [])
        idx = row * BRAND_CNT + column
        self.open_brand_by_level[str(level)].append(idx)
        if open_core_reward:
            if self.brand_level < 3:
                self.brand_level += 1
            self.core_reward_st[str(level)] = item_const.ITEM_UNRECEIVED
            self.core_brand_record[str(level)] = idx
        elif level != self.brand_level:
            return
        global_data.emgr.open_brand_succ_event.emit(level, row, column, open_core_reward)

    def receive_brand_core_reward(self, level):
        if level > self.brand_level:
            return
        reward_st = self.core_reward_st.get(str(level), item_const.ITEM_UNGAIN)
        if reward_st != item_const.ITEM_UNRECEIVED:
            return
        self.call_server_method('receive_brand_core_reward', (level,))

    @rpc_method(CLIENT_STUB, (Int('level'),))
    def receive_brand_core_reward_succ(self, level):
        self.on_receive_brand_core_reward_succ(level)

    def on_receive_brand_core_reward_succ(self, level):
        self.core_reward_st[str(level)] = item_const.ITEM_RECEIVED
        global_data.emgr.receive_brand_core_reward_succ.emit(level)