# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/common/uisys/item_caches_without_check.py
from __future__ import absolute_import
import six
import world
from common.framework import SingletonBase
import game3d

class ItemCacheWithOutCheck(SingletonBase):
    ALIAS_NAME = 'item_cache_without_check'

    def init(self):
        self.cache = {}

    def pop_item_by_json(self, json_path, use_func, custom_info=None):
        if global_data.is_low_mem_mode:
            return None
        else:
            key = self.generate_json_key(json_path, custom_info)
            if key in self.cache:
                panel_list = self.cache[key]
                if len(panel_list) <= 0:
                    return None
                panel = panel_list.pop()
                if len(panel_list) == 0:
                    del self.cache[key]
                else:
                    self.cache[key] = panel_list
                if use_func:
                    use_func(panel)
                if panel and panel.isValid():
                    panel.release()
                return panel
            return None
            return None

    def put_back_item_to_cache(self, panel, json_path, custom_info=None):
        if global_data.is_low_mem_mode:
            return None
        else:
            key = self.generate_json_key(json_path, custom_info)
            if not self.check_can_put_back(panel, json_path, custom_info):
                return None
            panel.retain()
            if panel.getParent():
                panel.Detach()
            panel.RecursionResetNodeConfAttr()
            if key in self.cache:
                self.cache[key].append(panel)
            else:
                self.cache[key] = [
                 panel]
            return None

    def check_can_put_back(self, panel, json_path, custom_info=None):
        if global_data.is_low_mem_mode:
            return False
        if not (panel and panel.isValid()):
            return False
        if panel.getReferenceCount() <= 0:
            log_error('Should put back the orignal node!!!', json_path)
            return False
        return True

    def generate_json_key(self, json_path, custom_info):
        if not custom_info:
            return json_path
        key = json_path + '_' + str(hash(str(custom_info)))
        return key

    def clear_cache(self):
        for key, panel_list in six.iteritems(self.cache):
            for panel in panel_list:
                if panel and not panel.IsDestroyed():
                    panel.Destroy()
                    panel.release()

        self.cache = {}

    def clear_cache_by_json(self, json_path, custom_info):
        key = self.generate_json_key(json_path, custom_info)
        if key in self.cache:
            panel_list = self.cache[key]
            for panel in panel_list:
                if panel and not panel.IsDestroyed():
                    panel.Destroy()
                    panel.release()

            del self.cache[key]

    def get_template_cache_size(self, json_path, custom_info=None):
        if global_data.is_low_mem_mode:
            return 0
        key = self.generate_json_key(json_path, custom_info)
        if key in self.cache:
            panel_list = self.cache[key]
            return len(panel_list)
        return 0