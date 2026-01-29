# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/MontageSDK/Lib/msgpack/embed.py
from __future__ import absolute_import
try:
    from _cmsgpack_packer import Packer
    from _cmsgpack_unpacker import unpack, unpackb, Unpacker
except ImportError:
    from msgpack.fallback import Packer, unpack, unpackb, Unpacker

def pack(o, stream, **kwargs):
    packer = Packer(**kwargs)
    stream.write(packer.pack(o))


def packb(o, **kwargs):
    return Packer(**kwargs).pack(o)


load = unpack
loads = unpackb
dump = pack
dumps = packb