# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/avatarmembers/impPickableItem.py
from mobile.common.rpcdecorator import rpc_method, CLIENT_STUB
from mobile.common.RpcMethodArgs import Dict
from common.cfg import confmgr

class impPickableItem(object):

    def _init_pickableitem_from_dict(self, bdict):
        self.daily_act_item_limit = bdict.get('daily_act_item_limit', {})

    def get_pickable_item_num_by_battle_bag_id(self, battle_bag_id):
        battle_bag_id = str(battle_bag_id)
        return self.daily_act_item_limit.get(battle_bag_id, 0)

    def get_pickable_item_num_by_lobby_item_id(self, lobby_item_id):
        battle_bag_id = confmgr.get('lobby_item', str(lobby_item_id), 'battle_bag_item')
        if battle_bag_id:
            return self.get_pickable_item_num_by_battle_bag_id(battle_bag_id)
        return 0

    @rpc_method(CLIENT_STUB, (Dict('daily_act_item_limit'),))
    def on_pickable_item_limit_change(self, daily_act_item_limit):
        self.daily_act_item_limit = daily_act_item_limit
        global_data.emgr.on_pickable_item_limit_change.emit()