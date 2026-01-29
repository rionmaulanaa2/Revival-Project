# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/sunshine/SunshineSDK/SunshineRpc/simplerpc/serializers/json_serializer.py
import json
from .serializer import AbstractSerializer
from .... import PY3

class JsonSerializer(AbstractSerializer):
    if PY3:

        @classmethod
        def dump(cls, data):
            out = json.dumps(data)
            return out.encode()

        @classmethod
        def load(cls, binData):
            return json.loads(binData.decode())

    else:
        load = staticmethod(json.loads)
        dump = staticmethod(json.dumps)