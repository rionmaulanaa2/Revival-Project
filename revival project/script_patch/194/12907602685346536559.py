# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/mall_ui/LobbyMallData.py
from __future__ import absolute_import
import math
from common.cfg import confmgr
from common.utils import timer
from common.framework import Singleton
from logic.gutils import mall_utils
from logic.gcommon import time_utility
from logic.client.const import mall_const
from logic.vscene.parts.gamemode.GMDecorator import halt_by_create_login
import six

class LobbyMallData(Singleton):
    ALIAS_NAME = 'lobby_mall_data'

    def init(self):
        self.init_parameters()
        self.init_mall_tag_conf()
        self.init_mall_recommendations()
        self.process_event(True)

    def init_parameters(self):
        self.send_log_timer = None
        self.mall_tag_conf = {}
        self.sdk_charge_info = {}
        self.charge_list_info = []
        self.is_pc_pay = mall_utils.is_pc_global_pay()
        if not self.get_charge_info():
            self.request_charge_info()
        self._next_check_dc_change_idx = -1
        self._check_dc_type_status_change_timer = None
        return

    def on_finalize(self):
        self.clear_timer()
        self._clear_check_dc_type_status_change_timer()
        self.init_parameters()
        self.process_event(False)

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'update_charge_info_by_sdk': self.on_update_charge_info_by_sdk,
           'buy_good_success_with_list': self.on_buy_good_success_with_list
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def _init_check_dc_type_status_change(self):
        mall_on_dc_type_ts_asc = confmgr.get('mall_on_dc_type_ts_asc', 'content', default=None)
        if not mall_on_dc_type_ts_asc:
            return
        else:
            cur_ts = time_utility.get_server_time()
            for idx, on_dc_type_ts_info in enumerate(mall_on_dc_type_ts_asc):
                ts = on_dc_type_ts_info[0]
                time_type = on_dc_type_ts_info[1]
                goods_id = on_dc_type_ts_info[2]
                discount_type = on_dc_type_ts_info[3]
                if cur_ts <= ts:
                    self._next_check_dc_change_idx = idx
                    break

            if self._next_check_dc_change_idx != -1:
                self._check_dc_type_status_change_timer = global_data.game_mgr.register_logic_timer(func=self._check_dc_type_status_change_func, mode=timer.CLOCK, interval=1)
            return

    def _check_dc_type_status_change_func(self):
        if self._next_check_dc_change_idx == -1:
            self._clear_check_dc_type_status_change_timer()
            return
        else:
            mall_on_dc_type_ts_asc = confmgr.get('mall_on_dc_type_ts_asc', 'content', default=None)
            if not mall_on_dc_type_ts_asc:
                return
            cur_ts = time_utility.get_server_time()
            while True:
                if self._next_check_dc_change_idx >= len(mall_on_dc_type_ts_asc):
                    break
                on_dc_type_ts_info = mall_on_dc_type_ts_asc[self._next_check_dc_change_idx]
                ts = on_dc_type_ts_info[0]
                if cur_ts > ts:
                    time_type = on_dc_type_ts_info[1]
                    goods_id = on_dc_type_ts_info[2]
                    discount_type = on_dc_type_ts_info[3]
                    global_data.emgr.mall_goods_discount_status_update.emit(discount_type, goods_id, time_type)
                    global_data.emgr.mall_goods_discount_rp_update.emit()
                    self._next_check_dc_change_idx = self._next_check_dc_change_idx + 1
                else:
                    break

            if self._next_check_dc_change_idx >= len(mall_on_dc_type_ts_asc):
                self._clear_check_dc_type_status_change_timer()
                self._next_check_dc_change_idx = -1
            return

    def _clear_check_dc_type_status_change_timer(self):
        self._check_dc_type_status_change_timer and global_data.game_mgr.unregister_logic_timer(self._check_dc_type_status_change_timer)
        self._check_dc_type_status_change_timer = None
        return

    def is_same_day_utc8(self, lhs, rhs):
        if lhs == rhs:
            return True
        else:
            if lhs is None or rhs is None:
                return False
            epoch = 0
            delta = time_utility.ONE_HOUR_SECONS * 8
            epoch = epoch - delta
            l_secs_elapsed_since_epoch = lhs - epoch
            r_secs_elapsed_since_epoch = rhs - epoch
            return int(math.ceil(l_secs_elapsed_since_epoch / time_utility.ONE_DAY_SECONDS)) == int(math.ceil(r_secs_elapsed_since_epoch / time_utility.ONE_DAY_SECONDS))

    def init_mall_tag_conf(self):
        _conf = confmgr.get('mall_tag_conf')
        tab_conf = {}
        for page_index, value in six.iteritems(_conf):
            if page_index == '__doc__':
                continue
            if value.get('show_in_mall') == '0':
                continue
            sub_show_in_mall_val = value.get('sub_show_in_mall_val')
            if sub_show_in_mall_val:
                has_show_sub_tab = False
                for sub_value in six.itervalues(sub_show_in_mall_val):
                    if sub_value == 1:
                        has_show_sub_tab = True
                        break

                if not has_show_sub_tab:
                    continue
                tab_conf[page_index] = {}
                for sub_page_index, sub_value in six.iteritems(value):
                    if sub_show_in_mall_val.get(sub_page_index) == 0:
                        continue
                    tab_conf[page_index][sub_page_index] = sub_value

            else:
                tab_conf[page_index] = value

        self.mall_tag_conf = tab_conf

    def init_mall_recommendations(self):
        recommended_goods_ids = set()
        recommend_confs = confmgr.get('mall_recommend_conf', default={})
        for goods_id, recommend_conf in six.iteritems(recommend_confs):
            if goods_id == '__doc__':
                continue
            if recommend_conf.get('iType', -1) == mall_const.RECOMMEND_NEW_BANNER_ID:
                continue
            open_dates = recommend_conf.get('open_timestamp')
            if open_dates and not time_utility.check_in_time_range((open_dates,)):
                continue
            if not mall_utils.is_good_opened(goods_id):
                continue
            recommended_goods_ids.add(goods_id)

        self.recommended_goods_ids = recommended_goods_ids
        mall_utils.clean_outdated_new_recommendations()
        new_arrival_goods_ids = set()
        arrival_confs = confmgr.get('c_mall_new_arrival_conf', default={})
        arrival_dict = global_data.message_data.get_seting_inf(mall_const.SETTING_NEW_ARRIVALS) or {}
        for goods_id, arrival_conf in six.iteritems(arrival_confs):
            if goods_id == '__doc__':
                continue
            if not mall_utils.is_good_opened(goods_id):
                continue
            if not arrival_dict.get(goods_id):
                new_arrival_goods_ids.add(goods_id)

        self.new_arrival_goods_ids = new_arrival_goods_ids
        mall_utils.clean_outdated_new_arrivals()

    @halt_by_create_login
    def init_red_point(self):
        for page in six.iterkeys(self.mall_tag_conf):
            has_sub_page = False
            for sub_page in six.iterkeys(self.mall_tag_conf[page]):
                if not sub_page.isdigit():
                    continue
                has_sub_page = True
                mall_utils.check_setting_goods(page, sub_page)

            if not has_sub_page:
                mall_utils.check_setting_goods(page)

    def get_mall_tag_conf(self):
        return self.mall_tag_conf

    def on_buy_good_success_with_list(self, goods_list):
        if not self.recommended_goods_ids:
            return
        for goods_id, pay_num, goods_type, need_show, reward_list, reason, payment, lucky_list in goods_list:
            if goods_id in self.recommended_goods_ids:
                global_data.emgr.mall_new_recommendation_update.emit()
                break

    def has_new_recommendations(self):
        for goods_id in self.recommended_goods_ids:
            if mall_utils.should_recommendation_marked_as_new(goods_id):
                return True

        return False

    def is_item_of_recommendations(self, p_item_no):
        for goods_id in self.recommended_goods_ids:
            item_no = mall_utils.get_goods_item_no(goods_id)
            if item_no is not None and item_no == p_item_no:
                return True

        return False

    def get_recommended_goods_ids(self):
        return self.recommended_goods_ids

    def get_new_arrivals_goods_ids(self):
        return self.new_arrival_goods_ids

    def remove_new_arrivals_goods_id(self, goods_id):
        if goods_id in self.new_arrival_goods_ids:
            self.new_arrival_goods_ids.remove(goods_id)

    def on_update_charge_info_by_sdk(self, info):
        self.sdk_charge_info = info
        global_data.emgr.update_charge_info.emit()

    def get_sdk_charge_info(self):
        return self.sdk_charge_info

    def request_charge_info(self):
        if not global_data.channel:
            return
        import hmac
        import hashlib
        import json
        game_id = global_data.channel.get_prop_str('JF_GAMEID')
        if not game_id:
            return
        platform = global_data.channel.get_platform()
        url = global_data.channel.get_prop_str('UNISDK_JF_GAS3_URL')
        url = ''.join([url, 'query_product', '?platform=%s' % platform])
        str2sign = ''.join(['GET', '/%s/sdk/query_product?platform=%s' % (game_id, platform)])
        key = global_data.channel.get_prop_str('JF_LOG_KEY')
        key = six.ensure_binary(key)
        str2sign = six.ensure_binary(str2sign)
        sign = hmac.new(key, str2sign, hashlib.sha256).hexdigest()
        headers = {'X-Client-Sign': sign}
        from common import http

        def cb(result, url, args):
            if result:
                d = json.loads(result)
                self.charge_list_info = d.get('product_list', [])
                global_data.emgr.update_charge_info.emit()
                self.clear_timer()

        http.request(url, header=headers, callback=cb)
        mall_const_list = []
        mall_const_list.extend(self.get_goods_list_by_name('WEEKLY_CARD_GOODS'))
        mall_const_list.extend(self.get_goods_list_by_name('MONTH_CARD_GOODS'))
        mall_const_list.extend(mall_const.ADVANCE_RENEWAL_MONTH_CARD_GOODS)
        mall_const_list.extend(mall_const.WEEKLY_COINS_SPEEDUP_GOODS)
        mall_const_list.extend(mall_const.WEEKLY_MECHA_LEVELUP_GOODS)
        mall_const_list.extend(mall_const.NEW_ROLE_6_GOODS)
        mall_const_list.extend(mall_const.NEW_ROLE_12_GOODS)
        mall_const_list.extend(mall_const.NEW_ROLE_30_GOODS)
        mall_const_list.extend(mall_const.GROWTH_FUND_GOODS)
        mall_const_list.extend(mall_const.EXCLUSIVE_GIFT_GOODS)
        mall_const_list.extend(mall_const.SUMMER_GO)
        mall_const_list.extend(mall_const.SUMMER_DISCOUNT_CHARGE_GOODS)
        mall_const_list.extend(mall_const.HALLOWEEN_GO)
        mall_const_list.extend(mall_const.GENERIC_MECHA_SKIN_DISCOUNT_CHARGE_GOODS)
        mall_const_list.extend(mall_const.ACTIVITY_NILE_GOODS)
        mall_const_list.extend(mall_const.ACTIVITY_GO_LOTTERY)
        mall_const_list.extend(mall_const.ACTIVITY_TEMP_GO)
        mall_const_list.extend(mall_const.ACTIVITY_DALIY_CHARGE)
        mall_const_list.extend(mall_const.ACTIVITY_2023_SPRING_SKIN)
        mall_const_list.extend(mall_const.ACTIVITY_S14_COLLECTION_PACKET)
        all_goods = []
        all_goods.extend(mall_utils.get_charge_goods_id())
        all_goods.extend(mall_utils.check_all_art_collection_goods_id())
        all_goods.extend(mall_utils.get_activity_goods_id(mall_const_list))
        global_data.channel.query_product(all_goods)
        self.send_log()

    def clear_timer(self):
        self.send_log_timer and global_data.game_mgr.get_logic_timer().unregister(self.send_log_timer)
        self.send_log_timer = None
        return

    def send_log(self):

        def _send():
            from logic.gutils.salog import SALog
            salog_writer = SALog.get_instance()
            salog_writer.write(SALog.QUERY_PRODUCT_LAG)

        self.clear_timer()
        self.send_log_timer = global_data.game_mgr.get_logic_timer().register(func=_send, mode=timer.CLOCK, interval=5, times=1)

    def get_charge_info(self):
        import re
        charge_info = []
        avail_goods_id = mall_utils.get_charge_goods_id()
        for info in self.charge_list_info:
            if info['goodsid'] in avail_goods_id:
                charge_info.append(info)

        def _sort--- This code section failed: ---

 338       0  LOAD_DEREF            0  're'
           3  LOAD_ATTR             0  'findall'
           6  LOAD_CONST            1  '\\.dq\\D*(\\d+)'
           9  LOAD_CONST            2  'goodsid'
          12  BINARY_SUBSCR    
          13  CALL_FUNCTION_2       2 
          16  STORE_FAST            1  'res'

 339      19  LOAD_GLOBAL           1  'int'
          22  LOAD_FAST             1  'res'
          25  LOAD_CONST            3  ''
          28  BINARY_SUBSCR    
          29  CALL_FUNCTION_1       1 
          32  RETURN_VALUE     
          -1  RETURN_LAST      

Parse error at or near `CALL_FUNCTION_2' instruction at offset 13

        charge_info.sort(key=_sort)
        return charge_info

    def get_activity_sale_info(self, goods_list):
        if type(goods_list) in (str, six.text_type):
            goods_list = self.get_goods_list_by_name(goods_list)
        avail_goods_id = mall_utils.get_activity_goods_id(goods_list)
        for info in self.charge_list_info:
            if info['goodsid'] in avail_goods_id:
                return info

    def get_activity_sale_info_list(self, goods_list):
        if type(goods_list) in (str, six.text_type):
            goods_list = self.get_goods_list_by_name(goods_list)
        ordered_info_lst = []
        avail_goods_id = mall_utils.get_activity_goods_id(goods_list)
        for jelly_goods_id in goods_list:
            if jelly_goods_id not in avail_goods_id:
                continue
            for info in self.charge_list_info:
                if info['goodsid'] == jelly_goods_id:
                    ordered_info_lst.append((jelly_goods_id, info))

        return ordered_info_lst

    def get_goods_list_by_name(self, goods_list_name):
        goods_list = getattr(mall_const, goods_list_name, [])
        if self.is_pc_pay:
            pc_goods_list_name = 'PC_' + goods_list_name
            pc_goods_list = getattr(mall_const, pc_goods_list_name, None)
            if pc_goods_list:
                goods_list = pc_goods_list
        return goods_list