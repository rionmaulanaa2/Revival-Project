# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/common/live/live_page_cache.py
from __future__ import absolute_import
import six
import six_ex
from six.moves import range

class LivePageCache(object):

    def __init__(self, start_index):
        self.init(start_index)

    def init(self, start_index):
        self._start_page = start_index
        self._total_page = 0
        self._page_size = 20
        self._cache_size = 0
        self._page_cache = {}
        self._has_total_page = True
        self._page_expire_time_dict = {}

    def destroy(self):
        self.clear()

    def set_has_total_page(self, has_total):
        self._has_total_page = has_total

    def set_total_page(self, total_page):
        self._total_page = total_page

    def get_total_page(self):
        if self._has_total_page:
            return self._total_page
        else:
            if self._page_cache:
                return max(six_ex.keys(self._page_cache))
            return 0

    def add_page(self, page, content):
        if page is None:
            if self._page_cache:
                page = max(six_ex.keys(self._page_cache)) + 1
            else:
                page = 1
        self._page_cache[page] = content
        self._add_checked_page(page, content)
        return

    def _add_checked_page(self, page, content):
        self._cache_size += len(content)

    def clear(self):
        self._page_cache = {}
        self._page_expire_time_dict = {}
        self._cache_size = 0
        self.set_total_page(0)

    def get_next_page_index(self):
        if not self._has_total_page:
            if self._page_cache:
                max_index = max(six_ex.keys(self._page_cache))
                if self._page_cache[max_index]:
                    return max_index + 1
                else:
                    return max_index

            else:
                return 1
        cur_next = self._start_page + len(self._page_cache)
        max_index = self._total_page - 1 + self._start_page
        max_index = max(max_index, self._start_page)
        if cur_next >= max_index:
            return max_index
        else:
            return cur_next

    def get_page(self, page):
        if self.check_page_expired(page):
            if page in self._page_cache:
                del self._page_cache[page]
            if page in self._page_expire_time_dict:
                del self._page_expire_time_dict[page]
        if self.has_page(page):
            return self._page_cache[page]
        else:
            return None
            return None

    def has_page(self, page):
        return page in self._page_cache

    def set_page_expire_time_dict(self, page, expire_time):
        self._page_expire_time_dict[page] = expire_time

    def check_page_expired(self, page):
        if page not in self._page_expire_time_dict:
            return False
        else:
            expire_time = self._page_expire_time_dict[page]
            from logic.gcommon import time_utility as tutil
            cur_time = tutil.get_server_time()
            return expire_time < cur_time

    def clear_expired_pages(self):
        for page in six.iterkeys(self._page_cache):
            if self.check_page_expired(page):
                if page in self._page_cache:
                    del self._page_cache[page]
                if page in self._page_expire_time_dict:
                    del self._page_expire_time_dict[page]

    def _index_to_page(self, live_index):
        all_sum = 0
        for page_index in range(self._start_page, self._start_page + len(self._page_cache)):
            cur_page = self._page_cache[page_index]
            if live_index + 1 <= all_sum + len(cur_page):
                return (page_index, live_index - all_sum)
            all_sum += len(cur_page)

        return (None, None)