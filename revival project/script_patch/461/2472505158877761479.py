# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/avatarmembers/impChanceGift.py
from __future__ import absolute_import
from __future__ import print_function
import six
from mobile.common.rpcdecorator import rpc_method, CLIENT_STUB
from mobile.common.RpcMethodArgs import Str, Int, Bool, Dict, List
from logic.gcommon import time_utility as tutil
from logic.gcommon.common_const import shop_const
from logic.gutils import mall_utils
from logic.comsys.charge_ui.GiftBoxSkinUI import GiftBoxSkinUI
from logic.comsys.charge_ui.GiftBoxItemLotteryUI import GiftBoxItemLotteryUI
from logic.gutils.scene_utils import is_in_lobby
from logic.gcommon.common_const import scene_const
from logic.comsys.charge_ui.GiftBoxBattlePassUI import GiftBoxBattlePassUI

class ChanceGiftBox(object):

    def __init__(self, bdict):
        self._id = 0
        self._start_time = 0
        self._item_info = {}
        self._push_client_time = 0
        self._discount_price = -1
        self._last_show_time = 0
        self._goods_id = 0
        self._cash_only = 0
        self._payment = 0
        self._opened = 0
        self.init_from_dict(bdict)

    def init_from_dict(self, bdict):
        self._id = bdict.get('id', 0)
        self._start_time = bdict.get('st', 0)
        self._item_info = bdict.get('item_info', 1)
        self._push_client_time = bdict.get('pct', 0)
        self._goods_id = bdict.get('goods_id', 0)
        self._payment = bdict.get('payment', 0)
        self._discount_price = bdict.get('dis_pri', -1)
        self._cash_only = self._item_info.get('cash_only', 0)
        self._opened = bdict.get('opened', 0)

    def get_logic_dict(self):
        from logic.gcommon.common_const.shop_const import GIFTBOX_CHANCE_TYPE
        dic = {'id': self._id,
           'goods_list': [
                        self._goods_id],
           'discount': self.get_discount(),
           'expire_time': self._start_time + shop_const.TRIGGER_GIFT_DURATION_TIME,
           'discount_price': self._discount_price,
           'gift_type': GIFTBOX_CHANCE_TYPE,
           'cash_only': self._cash_only,
           'chance_gift_no': self._item_info.get('gift_type', 0),
           'gift_level': self._item_info.get('gift_level', 0),
           'opened': self._opened,
           'virtual_discount': self._item_info.get('virtual_discount', [])
           }
        if self.get_chance_gift_no() == shop_const.CHANCE_GIFT_BATTLE_PASS_GIFT_TYPE:
            dic.update({'template_name': 'temp_btn_gifts_02'})
        elif self._cash_only:
            dic.update({'show_discount': 0.2})
        return dic

    def get_chance_gift_no(self):
        return self._item_info.get('gift_type', 0)

    def set_push_client_time(self, timestamp):
        self._push_client_time = timestamp

    def get_sell_price(self):
        return self._discount_price

    def get_payment(self):
        return self._payment

    def get_discount(self):
        discount = self._item_info.get('discount', 0)
        return discount / 100.0

    def get_goods_id(self):
        return self._goods_id

    def has_associate_goods(self):
        return self._goods_id and self._goods_id != '0'

    def get_push_client_time(self):
        return self._push_client_time

    def get_id(self):
        return self._id

    def is_expired(self):
        if tutil.get_server_time() > self._start_time + shop_const.TRIGGER_GIFT_DURATION_TIME:
            return True
        return False

    def is_valid(self):
        if self.is_expired():
            return False
        if not 0 < (shop_const.TRIGGER_GIFT_MIN_DISCOUNT <= self.get_discount() <= 1):
            return False
        if not self.has_associate_goods():
            return True
        if not mall_utils.is_good_opened(self.get_goods_id()):
            return False
        if self._payment <= 0:
            return False
        if self.get_sell_price() <= 0:
            return False
        return True

    def set_last_show_time(self, timestamp):
        self._last_show_time = timestamp

    def get_last_show_time(self):
        return self._last_show_time

    def has_opened(self):
        return self._opened

    def mark_as_opened(self):
        self._opened = 1


class impChanceGift(object):

    def _init_chancegift_from_dict(self, bdict):
        chance_gifts = {str(gift_id):ChanceGiftBox(gift_data) for gift_id, gift_data in six.iteritems(bdict.get('remain_chance_gifts', {}))}
        self._all_chance_gifts = {gift_id:gift_box for gift_id, gift_box in six.iteritems(chance_gifts) if gift_box.is_valid()}
        global_data.emgr.finish_advance_ui_list_event += self._on_chance_gift_check_show_event
        global_data.emgr.on_lottery_ended_event += self._on_chance_gift_check_show_event

    @rpc_method(CLIENT_STUB, (Dict('gift_info'),))
    def on_add_chance_gift(self, gift_info):
        gift_box = ChanceGiftBox(gift_info)
        if not gift_box.is_valid():
            return
        if gift_box.get_id() in self._all_chance_gifts:
            return
        self._all_chance_gifts[gift_box.get_id()] = gift_box
        if global_data.is_inner_server:
            print('\xe9\x9d\x9e\xe9\x85\x8b\xe7\xa4\xbc\xe5\x8c\x85: ' + gift_info.get('id', 0) + '  ' + gift_info.get('goods_id', 0))
        self._try_show_chance_gift_ui(gift_box.get_id())

    @rpc_method(CLIENT_STUB, (Str('gift_id'), Int('result_code')))
    def on_buy_chance_gift_result(self, gift_id, result_code):
        if result_code == 12024:
            global_data.game_mgr.show_tip(get_text_by_id(12024))
            return
        if result_code == 608312:
            global_data.game_mgr.show_tip(get_text_by_id(608312))
        self._remove_chance_gift(gift_id)

    def buy_chance_gift(self, gift_id):
        if not gift_id:
            return
        if gift_id not in self._all_chance_gifts:
            return
        self.call_server_method('buy_chance_gift', (gift_id,))

    def open_chance_gift(self, gift_id):
        if not gift_id:
            return
        gift_box = self._all_chance_gifts.get(gift_id)
        if not gift_box or gift_box.has_opened():
            return
        self.call_server_method('open_chance_gift', (gift_id,))
        gift_box.mark_as_opened()

    def get_battle_pass_chance_gift(self):
        for gift_id, gift_box in six.iteritems(self._all_chance_gifts):
            if not gift_box or gift_box.is_expired():
                continue
            if gift_box.get_chance_gift_no() != shop_const.CHANCE_GIFT_BATTLE_PASS_GIFT_TYPE:
                continue
            if gift_box.has_opened():
                return gift_box.get_logic_dict()

        return None

    def _can_show_chance_gift_in_scene(self):
        forbidden_ui_list = [
         'OpenBoxUI', 'ModeBanPickUI']
        for ui_name in forbidden_ui_list:
            ui = global_data.ui_mgr.get_ui(ui_name)
            if ui:
                return False

        return True

    def _try_show_chance_gift_ui(self, gift_id):
        if not global_data.lobby_mall_data:
            log_error('_try_show_chance_gift_ui: can not find lobby_mall_data', self.is_in_battle())
            return False
        else:
            if not self._can_show_chance_gift_in_scene():
                return False
            gift_box = self._all_chance_gifts.get(gift_id)
            if not gift_box or gift_box.is_expired():
                return False
            if gift_box.get_chance_gift_no() == shop_const.CHANCE_GIFT_BATTLE_PASS_GIFT_TYPE:
                GiftBoxBattlePassUI(None, gift_box.get_logic_dict(), False)
                gift_box.set_last_show_time(tutil.get_server_time())
            else:
                GiftBoxItemLotteryUI(None, gift_box.get_logic_dict())
                gift_box.set_last_show_time(tutil.get_server_time())
            return True

    def _hide_chance_gift_ui(self, gift_id):
        global_data.emgr.lobby_remove_giftbox_entry.emit(gift_id)
        global_data.ui_mgr.close_ui('GiftBoxItemLotteryUI')

    def _remove_chance_gift(self, gift_id):
        if gift_id in self._all_chance_gifts:
            del self._all_chance_gifts[gift_id]
        self._hide_chance_gift_ui(gift_id)

    def _on_chance_gift_check_show_event(self):
        try:
            for gift_id, gift_box in six.iteritems(self._all_chance_gifts):
                if not gift_box or gift_box.is_expired():
                    continue
                if gift_box.get_last_show_time() > 0:
                    continue
                if self._try_show_chance_gift_ui(gift_id):
                    break

        except Exception as e:
            log_error('_on_lobby_scene_event exception=%s', str(e))

    def get_chance_gift_for_lobby_entry(self):
        for gift_id, gift_box in six.iteritems(self._all_chance_gifts):
            if not gift_box or gift_box.is_expired():
                continue
            return gift_box.get_logic_dict()

        return {}

    def show_chance_gift_ui(self, gift_id):
        self._try_show_chance_gift_ui(gift_id)

    def on_chance_gift_expire(self, gift_id):
        self._remove_chance_gift(gift_id)

    def try_show_battle_pass_chance_gift(self, quit_buy):
        for gift_id, gift_box in six.iteritems(self._all_chance_gifts):
            if not gift_box or gift_box.is_expired():
                continue
            if gift_box.get_chance_gift_no() == shop_const.CHANCE_GIFT_BATTLE_PASS_GIFT_TYPE:
                GiftBoxBattlePassUI(None, gift_box.get_logic_dict(), quit_buy)
                gift_box.set_last_show_time(tutil.get_server_time())
                break

        return