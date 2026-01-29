# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/mobile/common/Md5OrIndexCodec.py
from __future__ import absolute_import
from ..mobilelog.LogManager import LogManager
import hashlib
import binascii
_logger = LogManager.get_logger('server.Md5OrIndexCodec')
DEBUG_MODE = 0

class Md5Cache(object):
    _str_to_md5 = {}
    _md5_to_str = {}

    @staticmethod
    def get_md5(string):
        md5 = Md5Cache._str_to_md5.get(string, None)
        if md5 == None:
            if DEBUG_MODE:
                Md5Cache._str_to_md5[string] = string
                Md5Cache._md5_to_str[string] = string
            else:
                md5Gen = hashlib.md5()
                import six
                md5Gen.update(six.ensure_binary(string))
                md5 = md5Gen.digest()
                Md5Cache._str_to_md5[string] = md5
                Md5Cache._md5_to_str[md5] = string
        return md5

    @staticmethod
    def get_str(md5):
        return Md5Cache._md5_to_str.get(md5, None)


MAX_STATIC_INDEX = 100000

class StaticIndexCache(object):
    _str_to_index = {}
    _index_to_str = {}

    @staticmethod
    def load_dict(_dictfile):
        raise Exception('Not implemented!')

    @staticmethod
    def get_string(index):
        return StaticIndexCache._index_to_str.get(index, None)

    @staticmethod
    def get_index--- This code section failed: ---

  79       0  LOAD_GLOBAL           0  'StaticIndexCache'
           3  LOAD_ATTR             1  '_str_to_index'
           6  LOAD_ATTR             2  'get'
           9  LOAD_ATTR             1  '_str_to_index'
          12  CALL_FUNCTION_2       2 
          15  RETURN_VALUE     
          -1  RETURN_LAST      

Parse error at or near `CALL_FUNCTION_2' instruction at offset 12


class Md5OrIndexDecoder(object):
    _max_id = MAX_STATIC_INDEX + 1
    _str_to_index = {}
    _index_to_str = {}

    @staticmethod
    def register_str(string):
        if string in Md5OrIndexDecoder._str_to_index:
            return
        index = Md5OrIndexDecoder._max_id
        Md5Cache.get_md5(string)
        Md5OrIndexDecoder._max_id += 1
        Md5OrIndexDecoder._index_to_str[index] = string
        Md5OrIndexDecoder._str_to_index[string] = index

    @staticmethod
    def decode(md5_index):
        index = md5_index.index
        if index > 0:
            if index <= MAX_STATIC_INDEX:
                string = StaticIndexCache.get_string(index)
            else:
                string = Md5OrIndexDecoder._index_to_str.get(index, None)
            if string == None:
                _logger.error('decode: string for index %d not found', index)
            return (string, False)
        else:
            if DEBUG_MODE:
                string = md5_index.md5
            else:
                string = Md5Cache.get_str(md5_index.md5)
            if string == None:
                _logger.error('decode: MD5 %s for string not found', binascii.hexlify(md5_index.md5))
                return (
                 string, False)
            md5_index.index = StaticIndexCache.get_index(string)
            if md5_index.index <= 0:
                md5_index.index = Md5OrIndexDecoder._str_to_index.get(string, 0)
            return (string, True)
            return

    @staticmethod
    def raw_decode(md5, index):
        if index > 0:
            if index <= MAX_STATIC_INDEX:
                string = StaticIndexCache.get_string(index)
            else:
                string = Md5OrIndexDecoder._index_to_str.get(index, None)
            if string == None:
                _logger.error('decode: string for index %d not found', index)
            return (string, False, -1)
        else:
            if DEBUG_MODE:
                string = md5
            else:
                string = Md5Cache.get_str(md5)
            if string == None:
                _logger.error('decode: MD5 %s for string not found', binascii.hexlify(md5))
                return (
                 string, False, -1)
            index = StaticIndexCache.get_index(string)
            if index <= 0:
                index = Md5OrIndexDecoder._str_to_index.get(string, 0)
            return (string, True, index)
            return


class Md5OrIndexEncoder(object):

    def __init__(self):
        super(Md5OrIndexEncoder, self).__init__()
        self.str_to_index = {}

    def addindex(self, md5, index):
        if DEBUG_MODE:
            string = md5
        else:
            string = Md5Cache.get_str(md5)
        _logger.debug('addindex :  %s, %d', string, index)
        if string and index > 0:
            self.str_to_index[string] = index

    def encode(self, md5_index, string):
        index = StaticIndexCache.get_index(string)
        if index <= 0:
            index = self.str_to_index.get(string, 0)
        if index > 0:
            md5_index.index = index
        elif DEBUG_MODE:
            md5_index.md5 = string
        else:
            md5 = Md5Cache.get_md5(string)
            md5_index.md5 = md5
        return md5_index

    def raw_encode(self, string):
        index = StaticIndexCache.get_index(string)
        if index <= 0:
            index = self.str_to_index.get(string, 0)
        if index > 0:
            return (index, '')
        else:
            if DEBUG_MODE:
                return (0, string)
            return (
             0, Md5Cache.get_md5(string))

    def reset(self):
        self.str_to_index = {}