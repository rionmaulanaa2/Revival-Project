# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/mobile/common/FilterMessageBroker.py
from __future__ import absolute_import
from collections import defaultdict
from ..mobilelog.LogManager import LogManager
from .RpcIndex import RpcIndexer

class FilterMessageBroker(object):
    _logger = LogManager.get_logger('server.EntityManager')
    _dispatch_map = defaultdict(set)

    @staticmethod
    def register(methodname, func):
        RpcIndexer.register_rpc(methodname)
        if func in FilterMessageBroker._dispatch_map[methodname]:
            return
        FilterMessageBroker._dispatch_map[methodname].add(func)

    @staticmethod
    def unregister(methodname, func):
        if methodname not in FilterMessageBroker._dispatch_map:
            return
        FilterMessageBroker._dispatch_map[methodname].discard(func)

    @staticmethod
    def dispatch(methodname, parameters=None):
        if methodname not in FilterMessageBroker._dispatch_map:
            FilterMessageBroker._logger.error('--------- dispatch methodname %s no func callable ---', methodname)
            return
        for func in FilterMessageBroker._dispatch_map[methodname]:
            if parameters:
                func(parameters)
            else:
                func()