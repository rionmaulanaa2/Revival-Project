# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/item/InventoryView.py
from __future__ import absolute_import
from functools import cmp_to_key
from . import item_sorter
from . import item_const as iconst
from logic.gcommon.item import item_utility

class InventoryView(object):

    def __init__(self):
        self._order_type = item_sorter.SORTER_TYPE_ITEM_NO
        self._item_list = []

    def is_view_item(self, item):
        raise NotImplementedError

    def update(self, item_list):
        self._item_list = []
        for item in item_list:
            if item is not None and self.is_view_item(item):
                self._item_list.append(item)

        self._sort()
        return

    def set_order_type(self, order_type):
        self._order_type = order_type
        self._sort()

    def get_view_item_list(self, refresh=False, filter=None):
        if refresh:
            self.update(self._item_list)
        item_list = []
        if filter is not None:
            item_list = [ item for item in self._item_list if not item.is_lock() ]
        else:
            item_list = self._item_list
        return item_list

    def get_view_name(self):
        return self.__class__.__name__

    def get_order_type(self):
        return self._order_type

    def _sort(self):
        cmp_func = item_sorter.SORTER_DICT[self._order_type]
        self._item_list.sort(key=cmp_to_key(cmp_func))


class InvViewAllItem(InventoryView):

    def is_view_item(self, item):
        if item is not None:
            return True
        else:
            return False
            return


class InvViewKnapsack(InventoryView):

    def is_view_item(self, item):
        if item is not None:
            return item.is_knapsack_item()
        else:
            return False
            return


class InvViewHead(InventoryView):

    def is_view_item(self, item):
        if item is not None:
            return item.is_head_item()
        else:
            return False
            return


class InvViewBodice(InventoryView):

    def is_view_item(self, item):
        if item is not None:
            return item.is_bodice_item()
        else:
            return False
            return


class InvViewBottoms(InventoryView):

    def is_view_item(self, item):
        if item is not None:
            return item.is_bottoms_item()
        else:
            return False
            return


class InvViewHeadFrame(InventoryView):

    def is_view_item(self, item):
        if item is not None:
            return item.is_head_frame()
        else:
            return False
            return


class InvViewHeadPhoto(InventoryView):

    def is_view_item(self, item):
        if item is not None:
            return item.is_head_photo()
        else:
            return False
            return


class InvViewHouseWallPicture(InventoryView):

    def is_view_item(self, item):
        if item is not None:
            return item_utility.is_wall_picture(item.item_no)
        else:
            return False
            return


class InvViewRedPointItem(InventoryView):

    def is_view_item(self, item):
        if item is not None:
            return item_utility.is_red_point_item(item.item_no)
        else:
            return False
            return


class InvViewChatItem(InventoryView):

    def is_view_item(self, item):
        if item is not None:
            return item.is_chat_item()
        else:
            return False
            return