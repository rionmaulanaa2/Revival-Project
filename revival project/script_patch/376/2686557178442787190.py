# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/avatarmembers/impTriggerGift.py
from __future__ import absolute_import
import six
from mobile.common.rpcdecorator import rpc_method, CLIENT_STUB
from mobile.common.RpcMethodArgs import Str, Int, Bool, Dict, List
from logic.gcommon import time_utility as tutil
from logic.gcommon.common_const import shop_const
from logic.gutils import mall_utils
from logic.comsys.charge_ui.GiftBoxSkinUI import GiftBoxSkinUI
from logic.comsys.charge_ui.GiftBoxItemUI import GiftBoxItemUI
from logic.gutils import trigger_gift_utils
from logic.gcommon.common_const import scene_const

class GiftBox(object):

    def __init__(self, bdict):
        self._id = 0
        self._start_time = 0
        self._goods_list = []
        self._discount = 1
        self._intro_params = []
        self._last_show_time = 0
        self._push_client_time = 0
        self._total_price = -1
        self.init_from_dict(bdict)

    def init_from_dict(self, bdict):
        self._id = str(bdict.get('id', 0))
        self._start_time = bdict.get('st', 0)
        self._goods_list = [ str(goods_id) for goods_id in bdict.get('gl', []) ]
        self._discount = bdict.get('dis', 1)
        self._intro_params = bdict.get('ip', [])
        self._push_client_time = bdict.get('pct', 0)
        self._original_price = bdict.get('ori_pri', 0)
        self._discount_price = bdict.get('dis_pri', 0)

    def get_logic_dict(self):
        from logic.gcommon.common_const.shop_const import GIFTBOX_TRIGGER_TYPE
        return {'id': self._id,
           'goods_list': self._goods_list,
           'intro_params': self._intro_params,
           'discount': self._discount,
           'total_price': self._total_price,
           'expire_time': self._start_time + shop_const.TRIGGER_GIFT_DURATION_TIME,
           'original_price': self._original_price,
           'discount_price': self._discount_price,
           'gift_type': GIFTBOX_TRIGGER_TYPE
           }

    def is_valid(self):
        if self.is_expired():
            return False
        if not trigger_gift_utils.is_valid_discount_value(self._discount):
            return False
        for goods_id in self._goods_list:
            if not mall_utils.is_good_opened(goods_id):
                return False

        if self._original_price <= 0 or self._discount_price <= 0:
            return False
        return True

    def get_id(self):
        return self._id

    def is_expired(self):
        if tutil.get_server_time() > self._start_time + shop_const.TRIGGER_GIFT_DURATION_TIME:
            return True
        return False

    def get_recommend_type(self):
        recommend_type = self._intro_params[0] if self._intro_params else None
        return trigger_gift_utils.get_gift_recommend_type(recommend_type)

    def set_last_show_time(self, timestamp):
        self._last_show_time = timestamp

    def get_last_show_time(self):
        return self._last_show_time

    def get_push_client_time(self):
        return self._push_client_time


class impTriggerGift(object):
    RECOMMEND_TYPE_2_UI = {shop_const.TRIGGER_GIFT_RECOMMEND_TYPE_SKIN: GiftBoxSkinUI,
       shop_const.TRIGGER_GIFT_RECOMMEND_TYPE_OTHER_ITEMS: GiftBoxItemUI
       }

    def _init_triggergift_from_dict(self, bdict):
        trigger_gifts = {str(gift_id):GiftBox(gift_data) for gift_id, gift_data in six.iteritems(bdict.get('remain_trigger_gifts', {}))}
        self._all_trigger_gifts = {gift_id:gift_box for gift_id, gift_box in six.iteritems(trigger_gifts) if gift_box.is_valid()}
        global_data.emgr.finish_advance_ui_list_event += self._on_lobby_scene_event

    @rpc_method(CLIENT_STUB, (Dict('gift_info'),))
    def on_add_trigger_gift(self, gift_info):
        gift_box = GiftBox(gift_info)
        if not gift_box.is_valid():
            return
        if gift_box.get_id() in self._all_trigger_gifts:
            return
        self._all_trigger_gifts[gift_box.get_id()] = gift_box
        self._try_show_trigger_gift_ui(gift_box.get_id())

    @rpc_method(CLIENT_STUB, (Str('gift_id'), Int('result_code')))
    def on_buy_trigger_gift_result(self, gift_id, result_code):
        if result_code == 12024:
            global_data.game_mgr.show_tip(get_text_by_id(12024))
            return
        if result_code == 608312:
            global_data.game_mgr.show_tip(get_text_by_id(608312))
        self._remove_trigger_gift(gift_id)

    def buy_trigger_gift(self, gift_id):
        if not gift_id:
            return
        if gift_id not in self._all_trigger_gifts:
            return
        self.call_server_method('buy_trigger_gift', (gift_id,))

    def on_trigger_gift_expire(self, gift_id):
        self._remove_trigger_gift(gift_id)

    def _can_show_trigger_gift_in_scene(self):
        cnt_scene = global_data.game_mgr.scene
        if not cnt_scene:
            return False
        if cnt_scene.get_type() != scene_const.SCENE_LOBBY:
            return False
        return True

    def _on_lobby_scene_event(self):
        try:
            for gift_id, gift_box in six.iteritems(self._all_trigger_gifts):
                if not gift_box or gift_box.is_expired():
                    continue
                if gift_box.get_last_show_time() > 0:
                    continue
                if self._try_show_trigger_gift_ui(gift_id):
                    break

        except Exception as e:
            log_error('_on_lobby_scene_event exception=%s', str(e))

    def get_trigger_gift_for_lobby_entry(self):
        for gift_id, gift_box in six.iteritems(self._all_trigger_gifts):
            if not gift_box or gift_box.is_expired():
                continue
            return gift_box.get_logic_dict()

        return {}

    def _try_show_trigger_gift_ui(self, gift_id):
        if not self._can_show_trigger_gift_in_scene():
            return False
        else:
            gift_box = self._all_trigger_gifts.get(gift_id)
            if not gift_box or gift_box.is_expired():
                return False
            ui = global_data.ui_mgr.get_ui('LobbyUI')
            if ui:
                show_gift_id = ui.get_showing_trigger_gift_id()
                if show_gift_id is not None and show_gift_id != '':
                    return False
            for recommend_type, ui_cls in six.iteritems(impTriggerGift.RECOMMEND_TYPE_2_UI):
                if ui_cls:
                    ui_name = ui_cls.__class__.__name__
                    if global_data.ui_mgr.get_ui(ui_name):
                        return False

            recommend_type = gift_box.get_recommend_type()
            ui_cls = impTriggerGift.RECOMMEND_TYPE_2_UI.get(recommend_type)
            if ui_cls:
                ui_cls(None, gift_box.get_logic_dict())
                gift_box.set_last_show_time(tutil.get_server_time())
                return True
            return False

    def show_trigger_gift_ui(self, gift_id):
        gift_box = self._all_trigger_gifts.get(gift_id)
        if not gift_box or gift_box.is_expired():
            global_data.game_mgr.show_tip(get_text_by_id(608312))
            return False
        else:
            recommend_type = gift_box.get_recommend_type()
            ui_cls = impTriggerGift.RECOMMEND_TYPE_2_UI.get(recommend_type)
            if not ui_cls:
                return False
            ui_name = ui_cls.__class__.__name__
            if global_data.ui_mgr.get_ui(ui_name):
                global_data.ui_mgr.close_ui(ui_name)
            ui_cls(None, gift_box.get_logic_dict())
            gift_box.set_last_show_time(tutil.get_server_time())
            return True

    def _hide_trigger_gift_ui(self, gift_id):
        global_data.emgr.lobby_remove_giftbox_entry.emit(gift_id)
        gift_box = self._all_trigger_gifts.get(gift_id)
        if not gift_box:
            return
        ui_cls = impTriggerGift.RECOMMEND_TYPE_2_UI.get(gift_box.get_recommend_type())
        if not ui_cls:
            return
        ui_name = ui_cls.__name__
        if global_data.ui_mgr.get_ui(ui_name):
            global_data.ui_mgr.close_ui(ui_name)

    def _remove_trigger_gift(self, gift_id):
        self._hide_trigger_gift_ui(gift_id)
        if gift_id in self._all_trigger_gifts:
            del self._all_trigger_gifts[gift_id]