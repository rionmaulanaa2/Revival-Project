# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/common/utils/pool_mgr.py
from __future__ import absolute_import
from __future__ import print_function
from common.utils.cache_lru import FixedSizeCacheLRU
from common.framework import Singleton

class PoolMgr(Singleton):
    CATEGORY_SIZE = 30
    MAX_POOL_SIZE = 300
    ITEM_SIZE = 20
    NEED_DESTROY = True

    def init(self):
        self.category_cache = FixedSizeCacheLRU(self.MAX_POOL_SIZE, self.CATEGORY_SIZE, self.ITEM_SIZE, self.NEED_DESTROY)
        super(PoolMgr, self).init()

    def add_item(self, key, item):
        return self.category_cache.add_item(key, item)

    def get_item(self, key):
        return self.category_cache.get_item(key)

    def print_debug_statistics(self):
        print('===== PoolMgr Debug Statistics =====')
        self.category_cache.log_info()
        print('===== PoolMgr Debug Statistics END=====')

    def get_mem_statistics(self):
        info = self.category_cache.get_all_item_mem_info()
        return info

    def check_auto_release(self, interval):
        return self.category_cache.check_auto_del_item(interval)


class SfxPoolMgr(PoolMgr):
    CATEGORY_SIZE = 10
    ITEM_SIZE = 5
    ALIAS_NAME = 'sfx_pool_mgr'

    def get_cached_sfx_map(self):
        return self.category_cache.get_map()


class BulletSfxPoolMgr(PoolMgr):
    CATEGORY_SIZE = 10
    ITEM_SIZE = 5
    ALIAS_NAME = 'bullet_sfx_pool_mgr'

    def get_cached_sfx_map(self):
        return self.category_cache.get_map()


class ModelPoolMgr(PoolMgr):
    CATEGORY_SIZE = 10
    ITEM_SIZE = 5
    ALIAS_NAME = 'model_pool_mgr'

    def get_cached_model_map(self):
        return self.category_cache.get_map()


class ResRefPoolMgr(PoolMgr):
    CATEGORY_SIZE = 5
    ITEM_SIZE = 1
    NEED_DESTROY = False
    ALIAS_NAME = 'mesh_pool_mgr'

    def get_cached_res_ref_map(self):
        return self.category_cache.get_map()