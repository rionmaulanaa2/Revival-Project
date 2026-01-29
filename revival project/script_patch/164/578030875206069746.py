# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/mobile/common/ProtoEncoder.py
from __future__ import absolute_import
from bson import BSON
import six
from msgpack.bson_msgpack import msgpackext
from msgpack.bson_msgpack import ext_hook
from msgpack import DEFAULT_STR_LEN_LIMIT, DEFAULT_ARRAY_LEN_LIMIT, DEFAULT_MAP_LEN_LIMIT, DEFAULT_EXT_LEN_LIMIT
try:
    from msgpack import packb, unpackb
except ImportError:
    from msgpack.embed import packb, unpackb

class ProtoEncoder(object):

    def __init__(self, proto):
        self._encode = None
        self._decode = None
        if proto == 'BSON' or proto == 'bson':
            self._encode = lambda p: BSON.encode(p)
            self._decode = lambda p: BSON(p).decode()
        elif proto == 'msgpack':
            self._encode = --- This code section failed: ---

  24       0  LOAD_GLOBAL           0  'packb'
           3  LOAD_GLOBAL           1  'True'
           6  LOAD_GLOBAL           1  'True'
           9  LOAD_CONST            2  'default'
          12  LOAD_GLOBAL           2  'msgpackext'
          15  CALL_FUNCTION_513   513 
          18  RETURN_VALUE_LAMBDA
          -1  LAMBDA_MARKER    

Parse error at or near `CALL_FUNCTION_513' instruction at offset 15
            if six.PY3:
                self._decode = --- This code section failed: ---

  26       0  LOAD_GLOBAL           0  'unpackb'
           3  LOAD_GLOBAL           1  'ext_hook'
           6  LOAD_CONST            2  'utf-8'
           9  LOAD_CONST            3  'ext_hook'
          12  LOAD_GLOBAL           1  'ext_hook'
          15  LOAD_CONST            4  'max_str_len'

  27      18  LOAD_GLOBAL           2  'DEFAULT_STR_LEN_LIMIT'
          21  LOAD_CONST            5  'max_array_len'

  28      24  LOAD_GLOBAL           3  'DEFAULT_ARRAY_LEN_LIMIT'
          27  LOAD_CONST            6  'max_map_len'

  29      30  LOAD_GLOBAL           4  'DEFAULT_MAP_LEN_LIMIT'
          33  LOAD_CONST            7  'max_ext_len'

  30      36  LOAD_GLOBAL           5  'DEFAULT_EXT_LEN_LIMIT'
          39  CALL_FUNCTION_1537  1537 
          42  RETURN_VALUE_LAMBDA
          -1  LAMBDA_MARKER    

Parse error at or near `CALL_FUNCTION_1537' instruction at offset 39
            else:
                self._decode = --- This code section failed: ---

  32       0  LOAD_GLOBAL           0  'unpackb'
           3  LOAD_GLOBAL           1  'ext_hook'
           6  LOAD_GLOBAL           1  'ext_hook'
           9  LOAD_CONST            2  'max_str_len'

  33      12  LOAD_GLOBAL           2  'DEFAULT_STR_LEN_LIMIT'
          15  LOAD_CONST            3  'max_array_len'

  34      18  LOAD_GLOBAL           3  'DEFAULT_ARRAY_LEN_LIMIT'
          21  LOAD_CONST            4  'max_map_len'

  35      24  LOAD_GLOBAL           4  'DEFAULT_MAP_LEN_LIMIT'
          27  LOAD_CONST            5  'max_ext_len'

  36      30  LOAD_GLOBAL           5  'DEFAULT_EXT_LEN_LIMIT'
          33  CALL_FUNCTION_1281  1281 
          36  RETURN_VALUE_LAMBDA
          -1  LAMBDA_MARKER    

Parse error at or near `CALL_FUNCTION_1281' instruction at offset 33
        return

    def encode(self, parameters):
        if self._encode is not None:
            return self._encode(parameters)
        else:
            return

    def decode(self, parameters):
        if self._decode is not None:
            return self._decode(parameters)
        else:
            return