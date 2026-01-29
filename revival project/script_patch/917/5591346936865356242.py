# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/common/uisys/UIPool.py
from __future__ import absolute_import
import six
from common.framework import SingletonBase
from collections import defaultdict

class UIPool(SingletonBase):
    ALIAS_NAME = 'ui_pool'
    MAX_CACHE_SIZE = 3

    def init(self):
        self._cache_dict = defaultdict(list)
        self._cache_size_dict = {}

    def clear(self):
        for ui_cache_list in six.itervalues(self._cache_dict):
            for ui in ui_cache_list:
                ui.Destroy()
                ui.release()

        self._cache_dict.clear()
        self._cache_size_dict.clear()

    def __load_ui(self, json_path):
        try:
            ui = global_data.uisystem.load_template_create(json_path)
        except:
            log_error('[UIPool] %s created failed' % json_path)
            return

        ui.retain()
        ui.__cache_key = json_path
        return ui

    def preload_ui(self, json_path_list):
        for json_path in json_path_list:
            if json_path in self._cache_dict:
                if len(self._cache_dict[json_path]) < self._cache_size_dict.get(json_path, 0):
                    continue
            ui = self.__load_ui(json_path)
            if ui:
                ui.RecursionRecordNodeConfAttr()
                self._cache_dict[json_path].append(ui)

    def create_ui(self, json_path, parent, repos=True, resize=True):
        ui_cache_list = self._cache_dict.get(json_path, None)
        if ui_cache_list:
            ui = ui_cache_list.pop()
        else:
            ui = self.__load_ui(json_path)
            ui.RecursionRecordNodeConfAttr()
        parent.AddChild('', ui)
        ui.RecursionResetNodeConfAttr(repos, resize)
        return ui

    def destroy_ui(self, ui):
        json_path = ui.__cache_key
        max_cache_size = self._cache_size_dict.get(json_path, UIPool.MAX_CACHE_SIZE)
        if json_path in self._cache_dict and len(self._cache_dict[json_path]) >= max_cache_size:
            ui.Destroy()
            ui.release()
        else:
            if ui.getParent():
                ui.Detach()
            self._cache_dict[json_path].append(ui)

    def set_cache_size_dict(self, dict):
        self._cache_size_dict.update(dict)