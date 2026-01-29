# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/mobile/common/RpcIndex.py
from __future__ import absolute_import
from __future__ import print_function
from six.moves import range
from hashlib import md5
from ..mobilelog.LogManager import LogManager
_logger = LogManager.get_logger('RpcIndexer')
VERIFY_TAG = '_v_e_r_i_f_y_'
CLIENT_SALT = '0'

class RpcIndexer(object):
    RPC2INDEX = {VERIFY_TAG: 0}
    INDEX2RPC = {}
    RECV_RPC_SALT = None
    SEND_RPC_SALT = None
    SEND_CACHE = {}

    @staticmethod
    def clear_recv():
        RpcIndexer.RPC2INDEX = {VERIFY_TAG: 0}
        RpcIndexer.INDEX2RPC = {}
        RpcIndexer.RECV_RPC_SALT = None
        return

    @staticmethod
    def register_rpc--- This code section failed: ---

  45       0  LOAD_GLOBAL           0  'RpcIndexer'
           3  LOAD_ATTR             1  'RPC2INDEX'
           6  LOAD_ATTR             2  'setdefault'
           9  LOAD_ATTR             1  'RPC2INDEX'
          12  CALL_FUNCTION_2       2 
          15  POP_TOP          

Parse error at or near `CALL_FUNCTION_2' instruction at offset 12

    @staticmethod
    def calculate_rpc_index(name, salt):
        import six
        m = md5()
        m.update(six.ensure_binary(name + salt))
        b = m.digest()
        if six.PY3:
            return ((b[-4] & 127) << 24) + (b[-3] << 16) + (b[-2] << 8) + b[-1]
        else:
            return ((ord(b[-4]) & 127) << 24) + (ord(b[-3]) << 16) + (ord(b[-2]) << 8) + ord(b[-1])

    @staticmethod
    def recv_rpc_index(name):
        return RpcIndexer.calculate_rpc_index(name, RpcIndexer.RECV_RPC_SALT)

    @staticmethod
    def send_rpc_index(name):
        index = RpcIndexer.SEND_CACHE.get(name, None)
        if index is None:
            index = RpcIndexer.SEND_CACHE[name] = RpcIndexer.calculate_rpc_index(name, RpcIndexer.SEND_RPC_SALT)
        return index

    @staticmethod
    def calculate_recv_rpc_salt():
        if RpcIndexer.RECV_RPC_SALT is not None:
            raise RuntimeError('RPC Salt Should Not Be Changed.')
        for RpcIndexer.RECV_RPC_SALT in range(65535):
            RpcIndexer.RECV_RPC_SALT = str(RpcIndexer.RECV_RPC_SALT)
            RpcIndexer.INDEX2RPC = {}
            for rpcname in RpcIndexer.RPC2INDEX:
                index = RpcIndexer.recv_rpc_index(rpcname)
                if index in RpcIndexer.INDEX2RPC:
                    break
                RpcIndexer.INDEX2RPC[index] = rpcname
                RpcIndexer.RPC2INDEX[rpcname] = index
            else:
                _logger.info('RPC Salt is %s', RpcIndexer.RECV_RPC_SALT)
                break

        else:
            RpcIndexer.RECV_RPC_SALT = None
            raise RuntimeError('Cannot Find Proper RPC Salt.')

        return

    @staticmethod
    def is_recv_indexed():
        return RpcIndexer.RECV_RPC_SALT is not None

    @staticmethod
    def is_send_indexed():
        return RpcIndexer.SEND_RPC_SALT is not None

    @staticmethod
    def set_recv_rpc_salt(salt):
        if RpcIndexer.RECV_RPC_SALT is not None:
            raise RuntimeError('RPC Salt Should Not Be Changed.')
        RpcIndexer.RECV_RPC_SALT = str(salt)
        RpcIndexer.INDEX2RPC = {}
        for rpcname in RpcIndexer.RPC2INDEX:
            index = RpcIndexer.recv_rpc_index(rpcname)
            if index in RpcIndexer.INDEX2RPC:
                raise RuntimeError('RECV RPC Salt %s Is Illegal.' % salt)
            RpcIndexer.INDEX2RPC[index] = rpcname
            RpcIndexer.RPC2INDEX[rpcname] = index

        return

    @staticmethod
    def set_send_rpc_salt(salt):
        if salt and RpcIndexer.is_send_indexed():
            if RpcIndexer.SEND_RPC_SALT == salt:
                return
            raise RuntimeError('Setting Different RPC SALT %s %s' % (RpcIndexer.SEND_RPC_SALT, salt))
        RpcIndexer.SEND_RPC_SALT = salt or None
        RpcIndexer.SEND_CACHE.clear()
        return

    @staticmethod
    def try_encode(name):
        if RpcIndexer.is_send_indexed():
            index = RpcIndexer.send_rpc_index(name)
            raw = ''
        else:
            index = -1
            raw = name
        if index == 764692373:
            print('RRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRR', name)
        return (index, raw)


class RpcSendIndexer(object):

    def __init__(self, salt):
        object.__init__(self)
        self._salt = salt
        self._name_cache = dict()

    def try_encode(self, name):
        try:
            index = self._name_cache[name]
        except:
            index = RpcIndexer.calculate_rpc_index(name, self._salt)
            self._name_cache[name] = index

        if index == 764692373:
            print('RRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRR', name)
        return (index, '')


_RPC_SEND_INDEXERS = dict()

def GET_RPC_SENDER_INDEXER(salt):
    try:
        return _RPC_SEND_INDEXERS[salt]
    except:
        _RPC_SEND_INDEXERS[salt] = RpcSendIndexer(salt)
        return _RPC_SEND_INDEXERS[salt]