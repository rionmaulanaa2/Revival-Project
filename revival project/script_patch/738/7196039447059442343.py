# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/NeutralShopBattle/NeutralShopBattleData.py
from __future__ import absolute_import
from common.framework import Singleton
from common.cfg import confmgr
from logic.gcommon.const import NEOX_UNIT_SCALE
from logic.client.const import game_mode_const
from common.utils import timer
from logic.comsys.battle.Death.DeathBattleUtils import pnpoly
import cc

class NeutralShopRecord(object):

    def __init__(self):
        self.goods_buy_history = {}
        self.shop_last_buy_goods = {}
        self.shop_last_bought_refresh_id = {}

    def update(self, goods_buy_history, shop_last_buy_goods, shop_last_bought_refresh_id):
        self.goods_buy_history = goods_buy_history
        self.shop_last_buy_goods = shop_last_buy_goods
        self.shop_last_bought_refresh_id = shop_last_bought_refresh_id


class NeutralShopBattleData(Singleton):
    ALIAS_NAME = 'neutral_shop_battle_data'

    def init(self):
        self.init_parameters()

    def init_parameters(self):
        self._entity_ace_coins_dict = {}
        self._shop_history = {}
        self._shop_refresh_time = 0

    def on_finalize(self):
        self.init_parameters()

    def update_entity_ace_coins(self, entity_id, coins):
        self._entity_ace_coins_dict[entity_id] = coins
        global_data.emgr.update_shop_entity_ace_coins_event.emit(entity_id, coins)

    def get_entity_ace_coins(self, entity_id):
        ace_coin = self._entity_ace_coins_dict.get(entity_id, None)
        if ace_coin is None:
            log_error('entity_id %s ace coin has no data!' % str(entity_id))
            ace_coin = 0
        return ace_coin

    def update_shop_buy_history(self, player_entity_id, goods_buy_history, shop_last_buy_goods, shop_last_bought_refresh_id):
        player_entity_id = str(player_entity_id)
        if player_entity_id not in self._shop_history:
            self._shop_history[player_entity_id] = NeutralShopRecord()
        shop_record = self._shop_history[player_entity_id]
        shop_record.update(goods_buy_history, shop_last_buy_goods, shop_last_bought_refresh_id)
        global_data.emgr.update_shop_buy_history_event.emit(player_entity_id, goods_buy_history, shop_last_buy_goods, shop_last_bought_refresh_id)

    def get_shop_buy_history(self, shop_entity_id, shop_refresh_id, player_entity_id):
        player_entity_id = str(player_entity_id)
        shop_record = self._shop_history.get(player_entity_id)
        if not shop_record:
            return ({}, {})
        else:
            last_buy_shop_refresh_id = shop_record.shop_last_bought_refresh_id.get(shop_entity_id, None)
            if shop_refresh_id == last_buy_shop_refresh_id:
                return (shop_record.goods_buy_history, shop_record.shop_last_buy_goods.get(shop_entity_id, {}))
            return (shop_record.goods_buy_history, {})

    def update_shop_refresh_time(self, refresh_time):
        self._shop_refresh_time = refresh_time
        global_data.emgr.update_shop_refresh_time_event.emit(refresh_time)

    def get_shop_refresh_time(self):
        return self._shop_refresh_time