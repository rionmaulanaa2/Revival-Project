# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/sunshine/SunshineSDK/SunshineRpc/simplerpc/transport/tcp/protocol.py
import sys
import struct
HEADER_SIZE = 4
IS_PY3 = sys.version_info.major == 3

class SimpleProtocolFilter(object):

    def __init__(self):
        super(SimpleProtocolFilter, self).__init__()
        self.buf = ''

    def input(self, data):
        self.buf += data
        while len(self.buf) > HEADER_SIZE:
            data_len = struct.unpack('i', self.buf[0:HEADER_SIZE])[0]
            if len(self.buf) >= data_len + HEADER_SIZE:
                content = self.buf[HEADER_SIZE:data_len + HEADER_SIZE]
                self.buf = self.buf[data_len + HEADER_SIZE:]
                yield content
            else:
                break

    @staticmethod
    def pack(content):
        if IS_PY3 and not isinstance(content, bytes):
            content = content.encode()
        return struct.pack('i', len(content)) + content

    @staticmethod
    def unpack--- This code section failed: ---

  50       0  LOAD_GLOBAL           0  'struct'
           3  LOAD_ATTR             1  'unpack'
           6  LOAD_CONST            1  'i'
           9  LOAD_CONST            2  ''
          12  LOAD_GLOBAL           2  'HEADER_SIZE'
          15  SLICE+3          
          16  CALL_FUNCTION_2       2 
          19  STORE_FAST            1  'length'

  51      22  LOAD_FAST             1  'length'
          25  LOAD_CONST            2  ''
          28  BINARY_SUBSCR    
          29  LOAD_FAST             0  'data'
          32  LOAD_GLOBAL           2  'HEADER_SIZE'
          35  SLICE+1          
          36  BUILD_TUPLE_2         2 
          39  RETURN_VALUE     
          -1  RETURN_LAST      

Parse error at or near `CALL_FUNCTION_2' instruction at offset 16


if __name__ == '__main__':
    s = SimpleProtocolFilter()
    r = s.pack('nimei')
    print repr(r)
    u = s.unpack(r)
    g = s.input(r[:1])
    for i in g:
        print i

    g = s.input(r[1:])
    for i in g:
        print i