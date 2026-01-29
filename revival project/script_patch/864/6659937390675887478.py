# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/mobile/common/CustomMessageBroker.py
from __future__ import absolute_import
from collections import defaultdict
from ..mobilelog.LogManager import LogManager
from .RpcIndex import RpcIndexer
CMSG_TYPE_GAME_CRASH = 1

class CustomMessageBroker(object):
    _logger = LogManager.get_logger('server.CustomMessageBroker')
    _dispatch_map = defaultdict(set)

    @staticmethod
    def register(msg_id, func):
        if func in CustomMessageBroker._dispatch_map[msg_id]:
            return
        CustomMessageBroker._dispatch_map[msg_id].add(func)

    @staticmethod
    def unregister(msg_id, func):
        if msg_id not in CustomMessageBroker._dispatch_map:
            return
        CustomMessageBroker._dispatch_map[msg_id].discard(func)

    @staticmethod
    def dispatch(msg_id, parameters=None):
        if msg_id not in CustomMessageBroker._dispatch_map:
            return
        for func in CustomMessageBroker._dispatch_map[msg_id]:
            if parameters:
                func(parameters)
            else:
                func()