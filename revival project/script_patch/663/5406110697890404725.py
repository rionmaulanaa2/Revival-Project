# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/sunshine/SunshineSDK/SunshineRpc/simplerpc/serializers/msgpack_serializer.py
import msgpack
from msgpack.bson_msgpack import msgpackext
from msgpack.bson_msgpack import ext_hook
try:
    from msgpack import packb, unpackb
except ImportError:
    from msgpack.embed import packb, unpackb

from functools import partial
from .serializer import AbstractSerializer

class MsgPackSerializer(AbstractSerializer):
    if msgpack.version >= (1, 0, 0):
        load = partial(unpackb, raw=False, strict_map_key=False)
        dump = partial(packb, use_bin_type=False)
    else:
        load = partial(unpackb, encoding='utf-8', ext_hook=ext_hook)
        dump = partial(packb, default=msgpackext)