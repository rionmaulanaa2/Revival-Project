# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/mobile/mobilerpc/MobileRequest.py
from __future__ import absolute_import
from struct import unpack

class request(object):

    def __init__(self):
        super(request, self).__init__()
        self.size = ''
        self.data = ''

    def get_size(self):
        try:
            return unpack('<I', self.size)[0]
        except:
            return -1

    def reset(self):
        self.size = ''
        self.data = ''


class request_parser(object):
    SIZE_BYTES = 4
    ST_SIZE = 0
    ST_DATA = 1
    MAX_DATA_LEN = 16777215

    def __init__(self):
        super(request_parser, self).__init__()
        self.max_data_len = self.MAX_DATA_LEN
        self.need_bytes = request_parser.SIZE_BYTES
        self.state = request_parser.ST_SIZE

    def reset(self):
        self.state = request_parser.ST_SIZE
        self.need_bytes = request_parser.SIZE_BYTES

    def set_max_data(self, size):
        self.max_data_len = size

    def parse(self, request, data, skip=0):
        l = len(data) - skip
        head_len = 0
        if self.state == request_parser.ST_SIZE:
            if l < self.need_bytes:
                request.size += data[skip:]
                self.need_bytes -= l
                return (
                 2, l)
            request.size += data[skip:skip + self.need_bytes]
            data_len = request.get_size()
            if data_len < 1:
                return (0, l)
            if data_len > self.max_data_len:
                return (0, l)
            self.state = request_parser.ST_DATA
            head_len = self.need_bytes
            self.need_bytes += data_len
        if self.state == request_parser.ST_DATA:
            if self.need_bytes > l:
                request.data += data[skip + head_len:]
                self.need_bytes -= l
                return (
                 2, l)
            else:
                request.data += data[skip + head_len:skip + self.need_bytes]
                consum = self.need_bytes
                self.reset()
                return (
                 1, consum)

        return (0, 0)