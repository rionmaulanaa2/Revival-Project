# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/system/SystemBase.py
from __future__ import absolute_import
import cython_flag
FPS_30 = 1 / 31.0

class SystemBase(object):

    def __init__(self, tick_step=FPS_30):
        self.tick_dt = 0
        self.tick_step = tick_step
        self._element_list = []
        self._data_dirty = True
        self.ecs_mask = 0
        self.ecs_ignored_mask = 0
        sysmgr = global_data.g_com_sysmgr
        for data_type in self.interested_type():
            self.ecs_mask |= sysmgr.get_mask(data_type)

        for data_type in self.ignored_type():
            self.ecs_ignored_mask |= sysmgr.get_mask(data_type)

    def interested_type(self):
        raise NotImplementedError()

    def ignored_type(self):
        return ()

    def handler_types(self):
        raise NotImplementedError()

    def match_data_and_tick(self, dt):
        if self._data_dirty:
            self._data_dirty = False
            self._element_list = global_data.g_com_sysmgr.get_elements(self.ecs_mask, self.ecs_ignored_mask)
        self.tick(dt)

    def tick(self, dt):
        pass

    def on_add_sys(self):
        pass

    def on_remove_sys(self):
        pass

    def add_handler(self, cls_type, handler):
        pass

    def remove_handler(self, cls_type, handler):
        pass

    def mark_data_dirty(self):
        self._data_dirty = True