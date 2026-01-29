# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/avatarmembers/impShop.py
from __future__ import absolute_import
import six
from mobile.common.RpcMethodArgs import Dict, List, Str, Int
from mobile.common.rpcdecorator import rpc_method, CLIENT_STUB
from common.cfg import confmgr
from logic.gcommon.const import SHOP_GOODS_LOTTERY, SHOP_GOODS_TRIGGER_GIFT
from logic.gcommon.item.lobby_item_type import L_ITEM_TYPE_ROLE_SKIN, L_ITEM_TYPE_MECHA_SKIN, L_ITEM_TYPE_MECHA
from common.platform.appsflyer import Appsflyer
import common.platform.appsflyer_const as af_const
from logic.client.const.mall_const import NORMAL_LOTTERY_LIST_ID
from logic.gutils import item_utils
from logic.gcommon.item import item_const
from logic.gutils.charm_utils import show_charm_up_tips_and_update_charm_value
from logic.gcommon.common_const.log_const import RECOMMEND_ITEM_STATE_BUY_ITEM
import time
from logic.gcommon.common_const import log_const
from logic.gutils.mall_utils import is_global_limit_goods
from logic.gcommon.common_const.rank_luck_const import luck_goods_set

class impShop(object):
    LOTTERY_HISTORY_REQUEST_MIN_INTERVAL = 2.5

    def _init_shop_from_dict(self, bdict):
        self.requested_buy_goods = False
        self.requesting_lucky_goods = False
        self.buy_num_all_dict = bdict.get('buy_num_all_dict', {})
        self.buy_num_permanent_dict = bdict.get('buy_num_permanent_dict', {})
        self.buy_num_per_lottery = bdict.get('buy_num_per_lottery', {})
        self.buy_num_per_day_dict = bdict.get('buy_num_per_day_dict', {})
        self.buy_num_per_week_dict = bdict.get('buy_num_per_week_dict', {})
        self.buy_num_per_sunday_dict = bdict.get('buy_num_per_sunday_dict', {})
        self.buy_num_per_month_dict = bdict.get('buy_num_per_month_dict', {})
        self.buy_num_per_season_dict = bdict.get('buy_num_per_season_dict', {})
        self.exchange_reminder = bdict.get('exchange_reminder', {})
        self.lottery_history_dict = {}
        self.lottery_history_prev_request_time = {}
        self.anniversary_discount_info = bdict.get('anniversary_gift', {})
        self.newbie_gift_expire_ts = bdict.get('newbie_gift_expire_ts', None)
        self.lottery_num_per_day_dict = bdict.get('lottery_num_per_day_dict', {})
        self.excluded_lottery = bdict.get('excluded_lottery', [])
        self.shop_lucky_goods = bdict.get('shop_lucky_goods', {})
        self.recommend_shop_items = bdict.get('recommend_shop_items', {})
        self.cache_buy_recommend_goods = None
        self.recommend_accessories = bdict.get('recommend_accessories', {})
        self.cache_buy_recommend_collocation_goods = []
        self.has_open_recommend_collocation = False
        self.global_buy_info = {}
        return

    @rpc_method(CLIENT_STUB, ())
    def reset_shop_per_day(self):
        self.buy_num_per_day_dict = {}
        self.lottery_num_per_day_dict = {}

    @rpc_method(CLIENT_STUB, ())
    def reset_shop_per_week(self):
        self.buy_num_per_week_dict = {}

    @rpc_method(CLIENT_STUB, ())
    def reset_shop_per_sunday(self):
        self.buy_num_per_sunday_dict = {}

    @rpc_method(CLIENT_STUB, ())
    def reset_shop_per_month(self):
        self.buy_num_per_month_dict = {}

    @rpc_method(CLIENT_STUB, (Dict('data'),))
    def reset_shop_per_season(self, data):
        self.buy_num_per_season_dict = data

    def get_per_week_num(self, goods_id):
        return self.buy_num_per_week_dict.get(goods_id, 0)

    def get_per_day_num(self, goods_id):
        return self.buy_num_per_day_dict.get(goods_id, 0)

    def get_buy_num_all(self, goods_id):
        return self.buy_num_all_dict.get(goods_id, 0)

    def get_newbie_gift_expire_ts(self):
        return self.newbie_gift_expire_ts

    def get_lottery_per_day_num(self, lottery_id):
        return self.lottery_num_per_day_dict.get(lottery_id, 0)

    def get_excluded_lottery(self):
        return self.excluded_lottery

    def is_over_max_buy_num_per_lottery(self, lottery_id, goods_id):
        max_buy_num_per_lottery = confmgr.get('mall_config', goods_id, 'max_buy_num_per_lottery')
        if max_buy_num_per_lottery is None:
            return False
        else:
            num = self.buy_num_per_lottery.get(goods_id, {}).get(lottery_id, 0)
            return max_buy_num_per_lottery <= num

    def buy_goods(self, goods_id, goods_num, goods_payment, gift_uid=None, need_show=None, discount_item_id=None, extra_info=None):
        import logic.gutils.mall_utils as mall_utils
        if gift_uid is None:
            gift_uid = self.uid if 1 else gift_uid
            goods_payment_type = mall_utils.get_payment_type(goods_payment)
            if need_show is None:
                need_show = mall_utils.get_goods_item_need_show(goods_id)
            extra_info = extra_info or {}
        goods_list = [
         (
          goods_id, goods_num, goods_payment_type, gift_uid, need_show, discount_item_id, extra_info)]
        self.call_server_method('buy_goods', (goods_list,))
        self.requested_buy_goods = True
        self.requesting_lucky_goods = str(goods_id) in luck_goods_set
        return

    def buy_multi_goods(self, goods_info_list):
        import logic.gutils.mall_utils as mall_utils
        buy_goods_list = []
        for goods_info in goods_info_list:
            goods_id = goods_info.get('goods_id')
            goods_num = goods_info.get('goods_num')
            goods_payment_type = mall_utils.get_payment_type(goods_info.get('goods_payment_type'))
            gift_uid = goods_info.get('gift_uid', self.uid)
            need_show = goods_info.get('need_show', mall_utils.get_goods_item_need_show(goods_id))
            discount_item_id = goods_info.get('discount_item_id', None)
            extra_info = goods_info.get('extra_info', {})
            buy_goods_list.append((goods_id, goods_num, goods_payment_type, gift_uid, need_show, discount_item_id, extra_info))

        if buy_goods_list:
            self.call_server_method('buy_goods', (buy_goods_list,))
            self.requested_buy_goods = True
        return

    @rpc_method(CLIENT_STUB, (List('fail_goods_list'),))
    def buy_goods_failed(self, fail_goods_list):
        for goods_id, pay_num, goods_type, err_code in fail_goods_list:
            if goods_type is None:
                mall_conf = confmgr.get('mall_config', goods_id, default={})
                goods_type = mall_conf.get('item_type', 0)
            if goods_type == SHOP_GOODS_LOTTERY:
                global_data.emgr.lottery_data_ready.emit(False)
                self.notify_client_message((pack_text(err_code),))
                global_data.ui_mgr.close_ui('OpenBoxUI')
            else:
                self.notify_client_message((pack_text(err_code),))

        return

    @rpc_method(CLIENT_STUB, (Dict('buy_num_dict'), List('goods_list'), Dict('extra_info')))
    def buy_goods_result(self, buy_num_dict, goods_list, extra_info):
        print (
         'buy_num_dict', buy_num_dict, goods_list)
        print ('extra_info', extra_info)
        self.buy_num_all_dict.update(buy_num_dict.get('buy_num_all_dict', {}))
        buy_num_per_lottery = buy_num_dict.get('buy_num_per_lottery', {})
        for goods_id, lottery_dict in six.iteritems(buy_num_per_lottery):
            if goods_id not in self.buy_num_per_lottery:
                self.buy_num_per_lottery[goods_id] = lottery_dict
            else:
                self.buy_num_per_lottery[goods_id].update(lottery_dict)

        self.buy_num_per_day_dict.update(buy_num_dict.get('buy_num_per_day_dict', {}))
        self.buy_num_per_week_dict.update(buy_num_dict.get('buy_num_per_week_dict', {}))
        self.buy_num_per_month_dict.update(buy_num_dict.get('buy_num_per_month_dict', {}))
        self.buy_num_per_season_dict.update(buy_num_dict.get('buy_num_per_season_dict', {}))
        self.buy_num_permanent_dict.update(buy_num_dict.get('buy_num_permanent_dict', {}))
        self.buy_num_per_sunday_dict.update(buy_num_dict.get('buy_num_per_sunday_dict', {}))
        self.lottery_num_per_day_dict.update(buy_num_dict.get('lottery_num_per_day_dict', {}))
        for goods_id, pay_num, goods_type, need_show, reward_list, reason, payment, lucky_list in goods_list:
            if is_global_limit_goods(goods_id):
                if goods_id in self.global_buy_info:
                    self.global_buy_info[goods_id] += pay_num
                else:
                    self.global_buy_info[goods_id] = pay_num

        global_data.emgr.buy_good_success.emit()
        global_data.emgr.buy_good_success_with_list.emit(goods_list)
        import logic.gutils.mall_utils as mall_utils
        for goods_id, pay_num, goods_type, need_show, reward_list, reason, payment, lucky_list in goods_list:
            if lucky_list:
                self.shop_lucky_goods[lucky_list[0]] = lucky_list[1]
                if str(goods_id) in luck_goods_set:
                    self.requesting_lucky_goods = False
            if goods_type == SHOP_GOODS_LOTTERY:
                self._appsflyer_lottery(goods_id)
                item_list = []
                origin_list = []
                extra_data = {}
                bingo_index_list = []
                max_rare_degree = item_const.RARE_DEGREE_0
                for reward_dict in reward_list:
                    item_dict = reward_dict.get('item_dict', {})
                    chips_source = reward_dict.get('chips_source', {})
                    bingo_index = reward_dict.get('extra_data', {}).get('bingo_grid', None)
                    if bingo_index is not None:
                        bingo_index_list.append(bingo_index)
                    for item_no, item_num in six.iteritems(item_dict):
                        origin_data = []
                        if chips_source and item_no in chips_source:
                            chip_source_data = chips_source[item_no]
                            for origin_item_no in six.iterkeys(chip_source_data):
                                origin_item_num, chip_num = chip_source_data[origin_item_no]
                                origin_data.append([origin_item_no, origin_item_num])
                                rare_degree = item_utils.get_item_rare_degree(origin_item_no, origin_item_num, ignore_imporve=True)

                        else:
                            rare_degree = item_utils.get_item_rare_degree(item_no, item_num, ignore_imporve=True)
                        max_rare_degree = max(max_rare_degree, rare_degree)
                        if len(origin_data):
                            data = origin_data[0] if 1 else None
                            item_list.append([item_no, item_num])
                            origin_list.append(data)

                if bingo_index_list:
                    extra_data['bingo_index_list'] = bingo_index_list
                if max_rare_degree:
                    extra_info['max_rare_degree'] = max_rare_degree
                log_error('[-----------Lottery-----------] Receiving lottery result')
                global_data.emgr.receive_lottery_result.emit(item_list, origin_list, extra_data, extra_info=extra_info)
                log_error('[-----------Lottery-----------] Base lottery data has been set')
            else:
                if goods_type == SHOP_GOODS_TRIGGER_GIFT:
                    need_show = mall_utils.get_goods_item_need_show(goods_id)
                for reward_dict in reward_list:
                    chips_source = reward_dict.get('chips_source', {})
                    if need_show == item_const.ITEM_SHOW_TYPE_ITEM or chips_source:
                        self.offer_reward_imp(reward_dict, reason)
                    else:
                        self.parse_charm_reward_item(reward_dict)
                    items = reward_dict.get('item_dict', {})
                    ext_show_items = {}
                    for item_no in six.iterkeys(items):
                        item_type = item_utils.get_lobby_item_type(item_no)
                        if need_show == item_const.ITEM_SHOW_TYPE_MODEL and not chips_source:
                            if not global_data.ui_mgr.get_ui('GetModelDisplayUI'):
                                global_data.ui_mgr.show_ui('GetModelDisplayUI', 'logic.comsys.mall_ui')
                            global_data.emgr.show_new_model_item.emit(item_no, extra_info={'payment': payment})
                        elif need_show == item_const.ITEM_SHOW_TYPE_WEAPON_OR_VEHICLE and not chips_source:
                            if not global_data.ui_mgr.get_ui('GetWeaponDisplayUI'):
                                global_data.ui_mgr.show_ui('GetWeaponDisplayUI', 'logic.comsys.mall_ui')
                            global_data.emgr.show_new_weapon_skin.emit(item_no)
                        if item_type == L_ITEM_TYPE_MECHA:
                            self._appsflyer_shop_mecha()
                        elif item_type == L_ITEM_TYPE_MECHA_SKIN or item_type == L_ITEM_TYPE_ROLE_SKIN:
                            self._appsflyer_shop_fashion()
                        elif item_no == 50101159:
                            ext_show_items[item_no] = items[item_no]

                    if ext_show_items:
                        self.offer_reward_imp({'item_dict': ext_show_items}, reason)

            if mall_utils.goods_can_use(goods_id) and not mall_utils.not_show_use_ui(goods_id):
                from logic.comsys.mall_ui.BuyConfirmUIInterface import groceries_use_confirmUI
                groceries_use_confirmUI(goods_id, pay_num)
            if self.cache_buy_recommend_goods == goods_id:
                self.sa_log_recommend_item(RECOMMEND_ITEM_STATE_BUY_ITEM, item_id=int(goods_id), cost=payment)
            elif goods_id in self.cache_buy_recommend_collocation_goods:
                self.sa_log_recommend_collocation_buy(goods_id, payment)

        self.requested_buy_goods = False
        return

    def lottery_receive_all_lv_reward(self):
        self.call_server_method('receive_all_lv_reward', ())

    def _appsflyer_lottery(self, goods_id):
        mall_conf = confmgr.get('mall_config', goods_id, default={})
        unit_num = mall_conf.get('num', 1)
        item_no = mall_conf.get('item_no', None)
        if item_no != NORMAL_LOTTERY_LIST_ID:
            if unit_num == 1:
                Appsflyer().advert_track_event(af_const.AF_LOTTERY)
            elif unit_num == 10:
                Appsflyer().advert_track_event(af_const.AF_LOTTERY10)
        return

    def _appsflyer_shop_mecha(self):
        Appsflyer().advert_track_event(af_const.AF_MECHABUY)

    def _appsflyer_shop_fashion(self):
        Appsflyer().advert_track_event(af_const.AF_FASHIONBUY)

    def add_exchange_reminder(self, goods_id, need_remind):
        self.exchange_reminder[str(goods_id)] = need_remind
        self.call_server_method('add_exchange_reminder', (str(goods_id), need_remind))

    def has_exchange_reminder(self, goods_id):
        goods_id = str(goods_id)
        if goods_id not in self.exchange_reminder:
            default_tips = confmgr.get('mall_config', goods_id, 'default_tips', default=0)
            if default_tips:
                return True
            return False
        return self.exchange_reminder.get(goods_id, False)

    def parse_charm_reward_item(self, reward_dict):
        charm_items = []
        items = reward_dict.get('item_dict', {})
        for item_no, item_num in six.iteritems(items):
            charm_items.append((item_no, item_num))

        show_charm_up_tips_and_update_charm_value(charm_items)

    def get_goods_lucky_discount_data(self, goods_id):
        goods_data = confmgr.get('mall_config', goods_id, default={})
        max_lucky = goods_data.get('lucky_discount', None)
        if max_lucky is None:
            return (None, None, None)
        else:
            lucky, discount = self.shop_lucky_goods.get(goods_id, [0, None])
            return (
             max_lucky, lucky, 1 if discount is None else discount)

    def reset_request_lottery_history_time(self, lottery_id):
        if lottery_id is None:
            return
        else:
            if lottery_id in self.lottery_history_prev_request_time:
                del self.lottery_history_prev_request_time[lottery_id]
            return

    def request_lottery_history(self, lottery_id, force=False):
        if not force:
            prev_requiest_time = self.lottery_history_prev_request_time.get(lottery_id, None)
            if prev_requiest_time is not None and time.time() - prev_requiest_time < self.LOTTERY_HISTORY_REQUEST_MIN_INTERVAL:
                return
        self.call_server_method('request_lottery_history', (lottery_id,))
        self.lottery_history_prev_request_time[lottery_id] = time.time()
        return

    @rpc_method(CLIENT_STUB, (Str('lottery_id'), List('lottery_history')))
    def respon_lottery_history(self, lottery_id, lottery_history):
        if lottery_history:
            lottery_history.reverse()
        self.lottery_history_dict[lottery_id] = lottery_history
        global_data.emgr.lottery_history_updated.emit(lottery_id)

    def get_lottery_history(self, lottery_id):
        return self.lottery_history_dict.get(lottery_id, None)

    @rpc_method(CLIENT_STUB, (Dict('recommend_shop_items'),))
    def update_recommend_item(self, recommend_shop_items):
        self.recommend_shop_items = recommend_shop_items

    def get_recommend_shop_list(self):
        if global_data.player and hasattr(global_data.player, 'get_setting_2'):
            from logic.gcommon.common_const.ui_operation_const import MALL_RECOMMEND
            if not global_data.player.get_setting_2(MALL_RECOMMEND):
                return {}
        return self.recommend_shop_items

    def sa_log_recommend_item(self, state, show_item_list=(), item_id=0, cost=None):
        log_info = {'state': state}
        if show_item_list:
            log_info['show_item_list'] = show_item_list
        if item_id:
            log_info['item_id'] = item_id
        if cost:
            log_info['cost'] = cost
        self.call_server_method('client_sa_log', ('ShopRec', log_info))

    @rpc_method(CLIENT_STUB, (Dict('anniversary_discount_info'),))
    def update_anniversary_discount_info(self, discount_info):
        self.anniversary_discount_info = discount_info

    def get_us_anniversary_discount_info(self):
        return self.anniversary_discount_info

    def sa_log_anniversary_gift(self, state, item_id=None):
        log_info = {'state': state,
           'item_id': item_id
           }
        self.call_server_method('client_sa_log', ('AnniversaryGift', log_info))

    def sa_log_anniversary_gift_state_open(self):
        self.sa_log_anniversary_gift(log_const.RECOMMEND_ITEM_STATE_OPEN)

    def sa_log_anniversary_gift_state_buy(self, goods_id):
        goods_id_list = self.anniversary_discount_info.get('goods', [])
        if goods_id in goods_id_list:
            self.sa_log_anniversary_gift(log_const.RECOMMEND_ITEM_STATE_BUY_ITEM, goods_id)

    @rpc_method(CLIENT_STUB, (List('collocation_list'),))
    def update_recommend_collocation(self, collocation_list):
        self.recommend_accessories = collocation_list

    def get_recommend_collocation(self):
        return self.recommend_accessories

    def sa_log_recommend_collocation(self, state, goods_id=None, cost=0):
        if not self.recommend_accessories:
            return
        log_info = {'state': state}
        if state == log_const.RECOMMEND_COLLOCATION_ITEM_STATE_BUY:
            log_info['item_id'] = goods_id
            log_info['cost'] = cost
        self.call_server_method('client_sa_log', ('CollocationRec', log_info))

    def sa_log_recommend_collocation_open(self):
        if not self.has_open_recommend_collocation:
            self.sa_log_recommend_collocation(log_const.RECOMMEND_COLLOCATION_ITEM_STATE_OPEN)
            self.has_open_recommend_collocation = True

    def sa_log_recommend_collocation_buy(self, goods_id, cost):
        self.sa_log_recommend_collocation(log_const.RECOMMEND_COLLOCATION_ITEM_STATE_BUY, goods_id, cost)

    @rpc_method(CLIENT_STUB, (Int('ret_code'), Dict('global_buy_info')))
    def resp_global_buy_info(self, ret_code, global_buy_info):
        if ret_code != 0:
            log_error('resp_global_buy_info error, ret_code: %s' % ret_code)
            return
        self.global_buy_info.update(global_buy_info)
        global_data.emgr.global_buy_info_updated_event.emit()

    def get_global_buy_info(self):
        return self.global_buy_info

    def req_global_buy_info(self, goods_ids):
        self.call_server_method('req_global_buy_info', (goods_ids,))

    def get_requesting_lucky_goods(self):
        return self.requesting_lucky_goods

    @rpc_method(CLIENT_STUB, (Dict('buy_num_dict'),))
    def update_buy_num_limit(self, buy_num_dict):
        self.buy_num_all_dict.update(buy_num_dict.get('buy_num_all_dict', {}))