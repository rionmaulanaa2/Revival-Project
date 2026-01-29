# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/mobile/mobilerpc/Compressor.py
from __future__ import absolute_import
from ..mobilelog.LogManager import LogManager
import zlib

class Compressor(object):

    def __init__(self):
        self.comp_obj = zlib.compressobj()
        self.decomp_obj = zlib.decompressobj()

    def compress(self, data):
        return self.comp_obj.compress(data) + self.comp_obj.flush(2)

    def decompress(self, data):
        return self.decomp_obj.decompress(data)