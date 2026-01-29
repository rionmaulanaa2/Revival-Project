# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/ctypes/PageTable.py
from __future__ import absolute_import
from __future__ import print_function
import six
from six.moves import range

class PageTable(object):

    def __init__(self, page_size=20):
        self._page_size = page_size
        self._data = [[]]
        self._max_page_idx = 0
        self._item_pos_dict = {}

    def __len__(self):
        return len(self._item_pos_dict)

    def get_max_page(self):
        return self._max_page_idx

    def get(self, key, default=None):
        if key not in self._item_pos_dict:
            return default
        page_idx, item_idx = self._item_pos_dict[key]
        return self._data[page_idx][item_idx]

    def __getitem__(self, item):
        return self.get(item)

    def _add(self, key, value):
        if key in self._item_pos_dict:
            return
        lst_page = self._data[self._max_page_idx]
        if len(lst_page) >= self._page_size:
            self._max_page_idx += 1
            self._data.append([])
        self._data[self._max_page_idx].append((key, value))
        self._item_pos_dict[key] = [
         self._max_page_idx, len(self._data[self._max_page_idx]) - 1]

    def __setitem__(self, key, value):
        if key in self._item_pos_dict:
            page_idx, item_idx = self._item_pos_dict[key]
            self._data[page_idx][item_idx] = (key, value)
        else:
            self._add(key, value)

    def update(self, _data):
        for key, value in six.iteritems(_data):
            self.__setitem__(key, value)

    def pop(self, key, default=None):
        if key not in self._item_pos_dict:
            return default
        else:
            page_idx, item_idx = self._item_pos_dict[key]
            _, value = self._data[page_idx][item_idx]
            self._item_pos_dict.pop(key, None)
            if page_idx == self._max_page_idx and item_idx == len(self._data[page_idx]) - 1:
                self._del_lst_item()
                return value
            lst_ley, lst_value = self._data[self._max_page_idx][-1]
            self._data[page_idx][item_idx] = [lst_ley, lst_value]
            self._item_pos_dict[lst_ley] = [page_idx, item_idx]
            self._del_lst_item()
            return value

    def _del_lst_item(self):
        self._data[self._max_page_idx].pop(-1)
        if len(self._data[self._max_page_idx]) == 0 and self._max_page_idx > 0:
            self._max_page_idx -= 1

    def get_page_data(self, page_idx):
        if page_idx > self._max_page_idx:
            return []
        return self._data[page_idx]

    def destory(self):
        self._data = []


if __name__ == '__main__':
    import random
    page_table = PageTable(10)
    for i in range(100):
        page_table.update({i: i})

    for r in random.sample(range(100), 8):
        page_table.pop(r)
        print(page_table[r])
        for i in range(11):
            print(page_table.get_page_data(i))