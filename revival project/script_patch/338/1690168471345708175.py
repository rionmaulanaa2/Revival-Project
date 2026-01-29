# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/system/SenderSystem.py
from __future__ import absolute_import
from .SystemBase import SystemBase, FPS_30
from ..client.ComSyncSenderData import ComSyncSenderData
from ..client.ComMoveSyncSender2 import ComMoveSyncSender2

class SenderSystem(SystemBase):

    def __init__(self):
        super(SenderSystem, self).__init__(FPS_30)
        self._handlers = {}

    def interested_type(self):
        return (
         ComSyncSenderData,)

    def handler_types(self):
        return [
         ComMoveSyncSender2.HANDLER_TYPE]

    def tick(self, dt):
        for unit_obj in self._element_list:
            handler = self._handlers.get(unit_obj)
            if handler:
                handler.tick_data(dt)

    def add_handler(self, handler_type, handler):
        self._handlers[handler.unit_obj] = handler

    def remove_handler(self, handler_type, handler):
        del self._handlers[handler.unit_obj]