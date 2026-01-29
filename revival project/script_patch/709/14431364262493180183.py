# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/avatarmembers/impBattleItem.py
from __future__ import absolute_import
from mobile.common.rpcdecorator import rpc_method, CLIENT_STUB
from mobile.common.RpcMethodArgs import Dict, List, Int, Str

class impBattleItem(object):

    def _init_battleitem_from_dict(self, bdict):
        self.battle_item_fashion = bdict.get('battle_item_fashion', {})
        self.battle_effect_item = bdict.get('battle_effect_item', {})

    def try_dress_battle_item_fashion(self, item_no, fashion_dict):
        self.call_server_method('dress_battle_item_fashion', (item_no, fashion_dict))

    @rpc_method(CLIENT_STUB, (Int('item_no'), Dict('fashion_dict')))
    def on_set_battle_item_fashion(self, item_no, fashion_dict):
        self.battle_item_fashion[str(item_no)] = fashion_dict
        global_data.emgr.player_item_update_event.emit()

    def get_battle_item_fashion(self):
        return self.battle_item_fashion

    def try_equip_battle_effect_item(self, effect_type, effect_id):
        self.call_server_method('equip_battle_effect_item', (effect_type, effect_id))

    @rpc_method(CLIENT_STUB, (Str('effect_type'), Int('effect_id')))
    def on_equip_battle_effect_item(self, effect_type, effect_id):
        self.battle_effect_item[effect_type] = effect_id
        global_data.emgr.player_item_update_event.emit()

    def get_battle_effect_item(self):
        return self.battle_effect_item

    def get_battle_effect_item_by_type(self, effect_type):
        from logic.gcommon.item import item_const
        default_dict = {item_const.BATTLE_EFFECT_KILL: item_const.DEFAULT_KILL_EFFECT
           }
        return self.battle_effect_item.get(effect_type, 0) or default_dict.get(effect_type, 0)