# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/sunshine/SunshineSDK/SunshineRpc/simplerpc/jsonrpc/utils.py
import inspect
from .... import PY2, text_type

class JSONSerializable(object):

    @classmethod
    def from_data(cls, data):
        if not isinstance(data, dict):
            raise ValueError('data should be dict')
        return cls(**data)


def is_invalid_params(func, *args, **kwargs):
    if not inspect.isfunction(func):
        return True
    funcargs, varargs, varkwargs, defaults = inspect.getargspec(func)
    if defaults:
        funcargs = funcargs[:-len(defaults)]
    if args and len(args) != len(funcargs):
        return True
    if kwargs and set(kwargs.keys()) != set(funcargs):
        return True
    if not args and not kwargs and funcargs:
        return True
    return False


def DecodeList(data, encoding):
    rv = []
    for item in data:
        if isinstance(item, text_type):
            item = item.encode(encoding)
        elif isinstance(item, list):
            item = DecodeList(item, encoding)
        elif isinstance(item, dict):
            item = DecodeDict(item, encoding)
        rv.append(item)

    return rv


def DecodeDict(data, encoding):
    rv = {}
    items = data.iteritems() if PY2 else data.items()
    for key, value in items:
        if isinstance(key, text_type):
            key = key.encode(encoding)
        if isinstance(value, text_type):
            value = value.encode(encoding)
        elif isinstance(value, list):
            value = DecodeList(value, encoding)
        elif isinstance(value, dict):
            value = DecodeDict(value, encoding)
        rv[key] = value

    return rv