# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/mobile/simplerpc/DirectProxy.py
from __future__ import absolute_import
import six_ex
import sys
from .rpc_code import RPC_CODE
from .DirectEntityRpcProcessor import DirectEntityRpcProcessor
from .simplerpc_common import CON_TYPE
from .simplerpc_common import LogManager
from ..common.proto_python import client_gate_pb2
from ..common.IdManager import IdManager
from ..common.mobilecommon import asiocore
from datetime import date
EXIST_CLIENTS = set()
dummy_handler = lambda *args, **kwargs: None

class DirectProxy(object):

    def __init__(self, client_avatar, server_entityid, address, conf, cb=None, sync_handler=None, sync_misty_handler=None):
        super(DirectProxy, self).__init__()
        self.logger = LogManager.get_logger('DirectEntityClient')
        self._server_entity_idbytes = IdManager.id2bytes(server_entityid)
        self.server_entityid = server_entityid
        self._client_avatar = client_avatar
        self.server_address = address
        self._bind_token = conf.get('bind_token', None)
        self._key_content = conf.get('key_content', None)
        self._key_path = conf.get('key_path', None)
        self._con_type = conf.get('con_type', 'TCP').upper()
        self._compressor_type = conf.get('compressor_type', 'ZLIB').upper()
        if global_data.feature_mgr.is_support_oodle_v2() and not asiocore.is_oodle_dict_ready():
            self._compressor_type = 'ZLIB'
        self._oodnet_up_dict_path = conf.get('oodnet_up_dict_path', '')
        self._oodnet_down_dict_path = conf.get('oodnet_down_dict_path', '')
        con_type = CON_TYPE[self._con_type]
        self._rpc = DirectEntityRpcProcessor(False, con_type, tb_handler=sys.excepthook)
        if sync_handler:
            self._rpc.set_handle_sync(sync_handler, sync_misty_handler)
        self._connection = None
        self._bind_cb = cb
        self._bind_ok = False
        self._lose_bind_cbs = []
        self._is_close = False
        self.session_padding_min_len = 1
        self.session_padding_max_len = 4
        EXIST_CLIENTS.add(self)
        self._init_seed()
        return

    def is_close(self):
        return self._is_close

    def get_con_type(self):
        return self._con_type

    def get_connection(self):
        return self._connection

    def _handle_connection_close(self):
        EXIST_CLIENTS.discard(self)
        self._is_close = True
        if self._client_avatar:
            self._client_avatar.set_battle_server(None)
            self._client_avatar = None
        if self._bind_ok:
            self._bind_ok = False
            for cb in self._lose_bind_cbs:
                try:
                    cb()
                except:
                    self.logger.log_last_except()

            self._lose_bind_cbs = []
        if self._connection:
            self._connection.entity = None
            self._connection = None
            self._close_rpc()
        return

    def _handle_binding_close(self):
        EXIST_CLIENTS.discard(self)
        self._is_close = True
        if self._client_avatar:
            self._client_avatar.set_battle_server(None)
            self._client_avatar = None
        if self._bind_cb:
            cb = self._bind_cb
            self._bind_cb = None
            cb(RPC_CODE.CLOSE)
        if self._connection:
            self._connection.entity = None
            self._connection = None
            self._close_rpc()
        return

    def _fire_bind_cb(self, code):
        if self._client_avatar is None:
            code = RPC_CODE.CLOSE
        if code == RPC_CODE.OK:
            self._bind_ok = True
            self._client_avatar.set_battle_server(self)
            self._connection.del_disconnect_cb(self._handle_binding_close)
            self._connection.add_disconnect_cb(self._handle_connection_close)
        else:
            self.close(code)
            self._client_avatar = None
        if self._bind_cb:
            cb = self._bind_cb
            self._bind_cb = None
            cb(code)
        return

    def _init_seed(self):
        seed_future = self._rpc.request_rpc(self.server_address, '', 'request_seed', args=(self._compressor_type,), need_reply=True)

        def _seed_reply(code, error, args):
            connection = self._rpc.get_connection(self.server_address)
            if code == RPC_CODE.OK:
                self._connection = connection
                if self._connection:
                    self._connection.add_disconnect_cb(self._handle_binding_close)
                    if isinstance(args, list):
                        seed, enable_compress = args
                    else:
                        seed, enable_compress = args, True
                    if enable_compress:
                        if self._compressor_type == 'OODLE':
                            self._connection.set_compressor_type(asiocore.compressor_type.oodle)
                            self._connection.set_oodnet_dict_path(str(self._oodnet_up_dict_path), str(self._oodnet_down_dict_path))
                        self._connection.enable_compressor(True)
                    self._init_key(seed)
                else:
                    self.logger.error('request seed error, no connection exist')
                    self._fire_bind_cb(RPC_CODE.CONNECT_FAIL)
            else:
                self.logger.error('request seed error %s', error)
                self._fire_bind_cb(code)
                if connection:
                    connection.close()

        seed_future.add_listener(_seed_reply)

    def _init_key(self, server_seed):
        if self._is_close:
            self._fire_bind_cb(RPC_CODE.CLOSE)
            return
        import Crypto
        import random
        from Crypto.Hash import SHA
        import Crypto.Random
        sessionkey = client_gate_pb2.SessionKey()
        rand = random.Random()
        random = Crypto.Random.new()
        ph_len = rand.randint(self.session_padding_min_len, self.session_padding_max_len)
        sessionkey.random_padding_header = random.read(ph_len)
        seed = random.read(32)
        key = SHA.new(seed).digest()
        sessionkey.session_key = key
        sessionkey.seed = six_ex.long_type(server_seed)
        pt_len = rand.randint(self.session_padding_min_len, self.session_padding_max_len)
        sessionkey.random_padding_tail = random.read(pt_len)
        from ..common import SessionEncrypter
        keyencrypter = SessionEncrypter.LoginKeyEncrypterNokeyczar(self._key_path, self._key_content)
        data = keyencrypter.encrypte(sessionkey.SerializeToString())
        self._connection.delay_enable_encrypt(key)
        fu = self._connection.request_rpc('', 'check_seed', args=[data], need_reply=True)

        def _check_seed_cb(code, error, args):
            if code == RPC_CODE.OK:
                self._do_bind_server_entity()
            else:
                self.logger.error('init encrypter key error')
                self._fire_bind_cb(code)

        fu.add_listener(_check_seed_cb)

    def _do_bind_server_entity(self):
        if self._is_close:
            self._fire_bind_cb(RPC_CODE.CLOSE)
            return
        args = [
         self._server_entity_idbytes, IdManager.id2bytes(self._client_avatar.id), self._bind_token]
        fu = self._connection.request_rpc('', 'bind_entity', args=args, need_reply=True)
        self._connection.entity = self._client_avatar

        def _cb(code, error, res):
            if code == RPC_CODE.OK:
                pass
            else:
                if self._connection:
                    self._connection.entity = None
                self.logger.error('bind server entity fail , %s', error)
            self._fire_bind_cb(code)
            return

        fu.add_listener(_cb)

    def add_lose_bind_cb(self, cb):
        if not self._bind_ok:
            raise Exception('add lose bind cb fail, but not bind any server entity')
        self._lose_bind_cbs.append(cb)

    def call_server_method_direct(self, method_name, parameters=None, entityid=None):
        if self._bind_ok and not self._is_close:
            self._connection.request_rpc('', '', args=[method_name, parameters, entityid])
        else:
            raise Exception('call rpc in a connection do not bind any server entity')

    def call_server_method_direct_misty(self, method_name, parameters=None, entityid=None):
        if self._bind_ok and not self._is_close:
            self._connection.request_rpc_misty('', '', args=[method_name, parameters, entityid])
        else:
            raise Exception('call rpc in a connection do not bind any server entity..')

    def _close_rpc(self):
        if self._rpc:
            self._rpc.set_handle_sync(dummy_handler, dummy_handler)
            self._rpc = None
        return

    def close(self, code=None):
        if self._is_close:
            return
        else:
            self._is_close = True
            self._bind_ok = False
            self._lose_bind_cbs = []
            EXIST_CLIENTS.discard(self)
            if self._client_avatar:
                self._client_avatar.set_battle_server(None)
                self._client_avatar = None
            if self._bind_cb:
                cb = self._bind_cb
                self._bind_cb = None
                cb(code or RPC_CODE.CLOSE)
            if self._connection:
                self._connection.entity = None
                self._connection.close()
                self._connection = None
                self._close_rpc()
            return


def create_direct_proxy(client_avatar, server_entityid, address, conf, cb=None):
    for client in EXIST_CLIENTS:
        if client.server_address == address and client.server_entityid == server_entityid:
            raise Exception('client already exist, may in connecting or binding finish')

    return DirectProxy(client_avatar, server_entityid, address, conf, cb)