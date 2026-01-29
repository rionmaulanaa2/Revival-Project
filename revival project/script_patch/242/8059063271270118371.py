# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/mall_ui/MallDisplayDiscountItemListWidget.py
from __future__ import absolute_import
import six_ex
from functools import cmp_to_key
from logic.comsys.mall_ui.MallDisplayItemListWidget import MallDisplayItemListWidget
from common.cfg import confmgr
from logic.gutils import mall_utils
from logic.gutils import item_utils

class MallDisplayDiscountItemListWidget(MallDisplayItemListWidget):

    def get_mall_items(self):
        items = six_ex.keys(self.goods_price_infos)
        items.sort(key=cmp_to_key(self._sort_cmp))

        def get_sort_list(goods_id):
            prices = mall_utils.get_mall_item_price(goods_id)
            has_limit_time_stamp = False
            for price_info in prices:
                limit_left_timestamp = price_info.get('limit_left_timestamp', 0)
                if limit_left_timestamp > 0:
                    has_limit_time_stamp = True
                    break

            has_yueka_discount = mall_utils.get_goods_yueka_discount(goods_id) is not None
            has_discount_tickets = bool(mall_utils.get_usable_dicount_items(goods_id))
            return (
             not has_limit_time_stamp, not has_yueka_discount, not has_discount_tickets)

        def _type_sort(goods_id_a, goods_id_b):
            tags_a = get_sort_list(goods_id_a)
            tags_b = get_sort_list(goods_id_b)
            return six_ex.compare(tags_a, tags_b)

        items.sort(key=cmp_to_key(_type_sort))

        def _owned_sort(goods_id):
            return mall_utils.item_has_owned_by_goods_id(goods_id)

        items.sort(key=_owned_sort)
        if self.btn_filter_select:
            final_items = []
            for goods_id in items:
                if not _owned_sort(goods_id):
                    final_items.append(goods_id)

            items = final_items
        if self.cur_filter_item_no:
            final_items = []
            for goods_id in items:
                belong_id = item_utils.get_lobby_item_belong_no(goods_id)
                if belong_id == self.cur_filter_item_no:
                    final_items.append(goods_id)

            items = final_items
        return items