# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/items_book_ui/ItemsBookOwnBtnWidget.py
from __future__ import absolute_import
import six

class ItemsBookOwnBtnWidget(object):

    def __init__(self, own_btn, callback, need_cache=False, def_val=False, custom_own_func=None, key_func=None):
        self.own_btn = own_btn
        self._own_switch = def_val
        self.need_cache = need_cache
        self.cache_dict = {}
        self.callback = callback
        self.custom_own_func = custom_own_func
        self.key_func = key_func if key_func else (lambda key: key)
        if self.own_btn:
            self.own_btn.BindMethod('OnClick', self.on_click_own_btn)
            self.own_btn.SetSelect(self._own_switch)

    def has_item(self, item_no, update_cache=False):
        item_no = self.key_func(item_no)
        if not item_no:
            return False
        else:
            item_no = int(item_no)
            if self.need_cache and not update_cache:
                return self.cache_dict.get(item_no, False)
            ret = False
            if self.custom_own_func:
                ret = self.custom_own_func(item_no)
            elif global_data.player:
                ret = global_data.player.has_item_by_no(int(item_no))
            if self.need_cache:
                self.cache_dict[item_no] = ret
            return ret

    def on_click_own_btn(self, btn, touch):
        if callable(self.callback):
            self._own_switch = not self._own_switch
            self.own_btn.SetSelect(self._own_switch)
            self.callback(self._own_switch)

    def destroy(self):
        self.own_btn = None
        self.key_func = None
        self.custom_own_func = None
        self.cache_dict = {}
        self.callback = None
        return

    def get_data_has_own(self, data, update_cache=False):
        if type(data) in (list, tuple):
            return [ i for i in data if self.has_item(i, update_cache) ]
        else:
            if type(data) == dict:
                new_dict = {}
                for key, item_list in six.iteritems(data):
                    new_dict.setdefault(key, [])
                    new_dict[key] = [ i for i in item_list if self.has_item(i, update_cache) ]

                return new_dict
            return None

    def update_cache(self, data):
        if self.need_cache:
            self.get_data_has_own(data, update_cache=True)

    def get_own_switch(self):
        return self._own_switch