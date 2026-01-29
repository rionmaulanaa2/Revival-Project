# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/com_shop/ComNeutralShopLogic.py
from __future__ import absolute_import
from logic.gcommon.component.UnitCom import UnitCom
from mobile.common.EntityManager import EntityManager
import world
import math3d

class ComNeutralShopLogic(UnitCom):
    BIND_EVENT = {'E_SHOP_SELL_GOODS_CHANGE': '_on_shop_sell_goods_change',
       'G_SHOP_SELL_GOODS_INFO': '_get_shop_sell_goods_info',
       'E_BUY_GOODS': '_buy_goods'
       }

    def __init__(self):
        super(ComNeutralShopLogic, self).__init__()
        self._sell_goods = {}
        self._refresh_id = None
        self._shop_no = None
        return

    def init_from_dict(self, unit_obj, bdict):
        self._sell_goods = bdict.get('sell_goods', {})
        self._refresh_id = bdict.get('refresh_id', None)
        self._shop_no = bdict.get('shop_no', None)
        super(ComNeutralShopLogic, self).init_from_dict(unit_obj, bdict)
        return

    def _on_shop_sell_goods_change(self, sell_goods, refresh_id):
        self._sell_goods = sell_goods
        self._refresh_id = refresh_id
        global_data.emgr.update_neutral_shop_goods_change_event.emit(self.unit_obj.id, self._refresh_id, self._sell_goods)

    def _get_shop_sell_goods_info(self):
        return (
         self._sell_goods, self._refresh_id)

    def _buy_goods(self, player_id, goods_list):
        if player_id and goods_list:
            self.send_event('E_CALL_SYNC_METHOD', 'buy_goods', (player_id, goods_list))