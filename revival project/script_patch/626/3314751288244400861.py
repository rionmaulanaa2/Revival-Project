# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/NeutralShopSurvivalBattle.py
from __future__ import absolute_import
from logic.entities.Battle import Battle
from logic.entities.SurvivalBattle import SurvivalBattle
from mobile.common.rpcdecorator import rpc_method, CLIENT_STUB
from mobile.common.RpcMethodArgs import Uuid, List, Str, Dict, Int, Float, Bool
from logic.gcommon.common_const import battle_const

class NeutralShopSurvivalBattle(SurvivalBattle):

    def __init__(self, entityid):
        super(NeutralShopSurvivalBattle, self).__init__(entityid)
        from logic.comsys.battle.NeutralShopBattle.NeutralShopBattleData import NeutralShopBattleData
        NeutralShopBattleData()
        self._candy_tips_timer = None
        return

    def on_destroy(self):
        if global_data.neutral_shop_battle_data:
            global_data.neutral_shop_battle_data.finalize()
        if self._candy_tips_timer:
            global_data.game_mgr.unregister_logic_timer(self._candy_tips_timer)
            self._candy_tips_timer = None
        return

    @rpc_method(CLIENT_STUB, (Uuid('entity_id'), Dict('goods_buy_history'), Dict('shop_last_buy_goods'), Dict('shop_last_bought_refresh_id')))
    def update_player_bought_history(self, entity_id, goods_buy_history, shop_last_buy_goods, shop_last_bought_refresh_id):
        self.on_update_player_bought_history(entity_id, goods_buy_history, shop_last_buy_goods, shop_last_bought_refresh_id)

    def on_update_player_bought_history(self, entity_id, goods_buy_history, shop_last_buy_goods, shop_last_bought_refresh_id):
        global_data.neutral_shop_battle_data.update_shop_buy_history(entity_id, goods_buy_history, shop_last_buy_goods, shop_last_bought_refresh_id)

    @rpc_method(CLIENT_STUB, (Uuid('entity_id'), Int('money_left')))
    def update_player_left_money(self, entity_id, money_left):
        self.on_update_player_left_money(entity_id, money_left)

    def on_update_player_left_money(self, entity_id, money_left):
        global_data.neutral_shop_battle_data.update_entity_ace_coins(entity_id, money_left)

    @rpc_method(CLIENT_STUB, (Float('refresh_timestamp'),))
    def update_shop_refresh_timestamp(self, refresh_timestamp):
        self.on_update_shop_refresh_timestamp(refresh_timestamp)

    def on_update_shop_refresh_timestamp(self, refresh_timestamp):
        global_data.neutral_shop_battle_data.update_shop_refresh_time(refresh_timestamp)
        from logic.gcommon.time_utility import get_server_time
        cur_t = get_server_time()
        remain_time = refresh_timestamp - cur_t
        from common.utils.timer import CLOCK
        if remain_time > 0:
            self._candy_tips_timer = global_data.game_mgr.register_logic_timer(self.show_candy_tips, interval=remain_time, mode=CLOCK, times=1)
        else:
            log_error('error:update_shop_refresh_timestamp', refresh_timestamp, cur_t, remain_time)

    def show_candy_tips(self):
        self._candy_tips_timer = None
        from logic.gcommon.common_const import battle_const
        global_data.emgr.battle_event_message.emit(None, message_type=battle_const.UP_NODE_CANDY_SHOP)
        return