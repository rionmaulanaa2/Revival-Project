# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/sunshine/SunshineSDK/SunshineRpc/simplerpc/jsonrpc/dispatcher.py
try:
    from collections.abc import MutableMapping
except ImportError:
    from collections import MutableMapping

class Dispatcher(MutableMapping):

    def __init__(self, prototype=None):
        self.method_map = dict()
        if prototype is not None:
            self.build_method_map(prototype)
        return

    def __getitem__(self, key):
        return self.method_map[key]

    def __setitem__(self, key, value):
        self.method_map[key] = value

    def __delitem__(self, key):
        del self.method_map[key]

    def __len__(self):
        return len(self.method_map)

    def __iter__(self):
        return iter(self.method_map)

    def __repr__(self):
        return repr(self.method_map)

    def add_class(self, cls):
        prefix = cls.__name__.lower() + '.'
        self.build_method_map(cls(), prefix)

    def add_object(self, obj):
        prefix = obj.__class__.__name__.lower() + '.'
        self.build_method_map(obj, prefix)

    def add_dict(self, dict, prefix=''):
        if prefix:
            prefix += '.'
        self.build_method_map(dict, prefix)

    def add_method(self, f, name=None):
        self.method_map[name or f.__name__] = f
        return f

    def build_method_map(self, prototype, prefix=''):
        if not isinstance(prototype, dict):
            prototype = dict(((method, getattr(prototype, method)) for method in dir(prototype) if not method.startswith('_')))
        for attr, method in prototype.items():
            if callable(method):
                self[prefix + attr] = method