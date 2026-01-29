# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/mall_ui/MallDisplayFlashItemListWidget.py
from __future__ import absolute_import
import six_ex
import six
from functools import cmp_to_key
from logic.comsys.mall_ui.MallDisplayItemListWidget import MallDisplayItemListWidget
from logic.gutils import mall_utils
from logic.client.const import mall_const
from common.cfg import confmgr

class MallDisplayFlashItemListWidget(MallDisplayItemListWidget):

    def get_event_conf(self):
        events = super(MallDisplayFlashItemListWidget, self).get_event_conf()
        events.update({'receive_reward_info_from_server_event': self.reset_mall_list})
        return events

    def get_sort_option(self):
        sort_option = [{'name': get_text_local_content(81925)}, {'name': get_text_local_content(12071)}, {'name': get_text_local_content(12072)}]
        sort_cmp = [
         None, lambda a: self.is_show_model(a), lambda a: not self.is_show_model(a)]
        return (
         sort_option, sort_cmp)

    def init_own_filter(self):
        self.panel.btn_show_own.setVisible(False)
        super(MallDisplayFlashItemListWidget, self).init_own_filter()

    def is_show_model(self, goods_id):
        is_item = mall_utils.is_weapon(goods_id) or mall_utils.is_vehicle(goods_id)
        is_role_or_skin = mall_utils.is_driver(goods_id) or mall_utils.is_mecha(goods_id)
        return is_item or is_role_or_skin

    def init_mall_list(self, page_index, sub_page_index=None):
        self._cur_page_index = page_index
        self._cur_sub_page_index = sub_page_index
        goods_items = []
        item_page_conf = confmgr.get('mall_page_config', str(self._cur_page_index), default={})
        if self._cur_sub_page_index is not None:
            goods_items = item_page_conf.get(self._cur_sub_page_index, [])
        else:
            for sub_page_conf in six.itervalues(item_page_conf):
                goods_items.extend(sub_page_conf)

        self.goods_price_infos = {}
        for goods_id in goods_items:
            if not mall_utils.is_good_opened(goods_id):
                continue
            self.goods_price_infos[goods_id] = mall_utils.get_mall_item_price(goods_id)

        mall_conf = confmgr.get('mall_config', default={})
        if global_data.player:
            if G_IS_NA_PROJECT:
                need_consider_lottery_list_ids = [
                 mall_const.SPECIAL_LOTTERY_LIST_ID, mall_const.OVERSEAS_SPECIAL_LOTTERY_LIST_ID]
            else:
                need_consider_lottery_list_ids = [
                 mall_const.CN_SPECIAL_LOTTERY_LIST_ID]
            for lottery_list_id in need_consider_lottery_list_ids:
                probability_up_data = global_data.player.get_reward_probability_up_data(lottery_list_id)
                item_goods_id_map = confmgr.get('preview_{}'.format(lottery_list_id), 'percent_up_item_goods_id')
                if probability_up_data:
                    _, _, _, probability_data = probability_up_data
                    for item in probability_data:
                        item_id = str(item[0])
                        if item_id not in item_goods_id_map:
                            continue
                        goods_id = item_goods_id_map[item_id]
                        if goods_id in mall_conf:
                            self.goods_price_infos[goods_id] = mall_utils.get_mall_item_price(goods_id)

        self.panel.mall_list.set_asyncLoad_tick_time(0)
        self.panel.mall_list.set_asyncLoad_interval_time(0.05)
        self.init_item_filter()
        self.reset_mall_list(is_init=True)
        return

    def get_mall_items(self):
        items = six_ex.keys(self.goods_price_infos)
        items.sort(key=cmp_to_key(lambda a, b: self.mall_price_cmp(b, a)))

        def _new_sort--- This code section failed: ---

  78       0  LOAD_GLOBAL           0  'confmgr'
           3  LOAD_ATTR             1  'get'
           6  LOAD_CONST            1  'c_mall_new_arrival_conf'
           9  LOAD_CONST            2  'cShowNewHint'
          12  LOAD_CONST            3  'default'
          15  LOAD_GLOBAL           2  'False'
          18  CALL_FUNCTION_259   259 
          21  UNARY_NOT        
          22  RETURN_VALUE     
          -1  RETURN_LAST      

Parse error at or near `CALL_FUNCTION_259' instruction at offset 18

        items.sort(key=_new_sort)

        def _owned_sort(goods_id):
            return mall_utils.item_has_owned_by_goods_id(goods_id)

        items.sort(key=_owned_sort)
        if self._sort_cmp:
            final_items = []
            for goods_id in items:
                if self._sort_cmp(goods_id):
                    final_items.append(goods_id)

            items = final_items
        return items