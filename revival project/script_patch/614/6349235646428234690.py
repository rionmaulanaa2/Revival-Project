# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/mobile/client/GateClient.py
from __future__ import absolute_import
import six_ex
from ..common.proto_python import client_gate_pb2
from ..common.proto_python import common_pb2
from ..mobilelog.LogManager import LogManager
from ..common.Md5OrIndexCodec import Md5OrIndexDecoder
from ..common.EntityFactory import EntityFactory
from ..mobilerpc.ChannelClient import ChannelClient
from ..common.IdManager import IdManager
from ..client.ServerProxy import ServerProxy
from ..common.EntityManager import EntityManager
from ..common.RpcIndex import RpcIndexer, CLIENT_SALT
import sys
from ..mobilerpc.Compressor import Compressor
from ..common.ProtoEncoder import ProtoEncoder
DEVICE_ID = str(IdManager.genid())

class GateClient(client_gate_pb2.IGateClient):
    ST_INIT = 0
    ST_CONNECTING = 1
    ST_RECONNECTING = 3
    ST_CONNECT_FAILED = 4
    ST_CONNECT_SUCCESSED = 5
    ST_DISCONNECTED = 6
    CB_ON_CONNECT_FAILED = 1
    CB_ON_CONNECT_SUCCESSED = 2
    CB_ON_DISCONNECTED = 3
    CB_ON_CONNECT_REPLY = 4
    CB_ON_RELIABLE_MESSAGE_CANNOT_SENT = 5

    def __init__(self, host, ip, clientconf):
        client_gate_pb2.IGateClient.__init__(self)
        self.client = ChannelClient(host, ip, self)
        self.logger = LogManager.get_logger('server.GateClient')
        self.status = GateClient.ST_INIT
        self.in_reconnect_status = False
        self.reconnect_data = None
        self.gatestub = None
        self.tb_handler = None
        self.proto_encoder = ProtoEncoder(clientconf.get('proto', 'BSON'))
        enforce_encryption = bool(clientconf.get('enforce_encryption', False))
        loginkeypath = clientconf.get('loginkeypath', None)
        key_content = clientconf.get('loginkeycontent', None)
        use_keyczar = bool(clientconf.get('use_keyczar', None))
        self.zipped_enable = clientconf.get('zipped_channel', 0)
        self.received_seq = 0
        self.use_message_cache = False
        self.session_padding_min_len = 16
        self.session_padding_max_len = 64
        self.con_type = common_pb2.ConnectServerReply.BUSY
        self.sessionseed = client_gate_pb2.SessionSeed()
        if enforce_encryption:
            if use_keyczar:
                from ..common.SessionEncrypter import LoginKeyEncrypter
                self.keyencrypter = LoginKeyEncrypter(loginkeypath)
            else:
                from ..common.SessionEncrypter import LoginKeyEncrypterNokeyczar
                self.keyencrypter = LoginKeyEncrypterNokeyczar(loginkeypath, key_content)
        else:
            self.keyencrypter = None
        self.on_event_callback_dict = {GateClient.CB_ON_CONNECT_FAILED: set(),
           GateClient.CB_ON_CONNECT_SUCCESSED: set(),
           GateClient.CB_ON_DISCONNECTED: set(),
           GateClient.CB_ON_CONNECT_REPLY: set(),
           GateClient.CB_ON_RELIABLE_MESSAGE_CANNOT_SENT: set()
           }
        return

    def enable_message_cache(self):
        self.use_message_cache = True

    def set_session_padding_length(self, min_len, max_len):
        self.session_padding_min_len = min_len
        self.session_padding_max_len = max_len

    def start_game(self, timeout):
        self.reset_rpc_salt()
        self.received_seq = 0
        self.status = GateClient.ST_CONNECTING
        self._connect(self.channel_cb, timeout)

    def resume_game(self, timeout, entityid, authmsg):
        self.reset_rpc_salt()
        self.status = GateClient.ST_RECONNECTING
        self.reconnect_data = {'entityid': entityid,'bin_authmsg': self.proto_encoder.encode(authmsg)}
        cb = lambda rpc_channel: self.channel_cb(rpc_channel)
        self._connect(cb, timeout)

    def _connect(self, channel_cb, timeout):
        try:
            self.client.connect(channel_cb, timeout)
        except:
            self.logger.log_last_except()
            channel_cb(None)

        return

    def disconnect(self):
        self.client.disconnect()

    def channel_cb(self, rpc_channel):
        if self.status == GateClient.ST_CONNECT_FAILED:
            if rpc_channel:
                self.disconnect()
            return
        else:
            if rpc_channel is None:
                self.status = GateClient.ST_CONNECT_FAILED
                callback_set = self.on_event_callback_dict[GateClient.CB_ON_CONNECT_FAILED].copy()
                [ cb for cb in callback_set if cb() ]
                return
            callback_set = self.on_event_callback_dict[GateClient.CB_ON_CONNECT_SUCCESSED].copy()
            [ cb for cb in callback_set if cb() ]
            self.in_reconnect_status = self.status == GateClient.ST_RECONNECTING
            self.status = GateClient.ST_CONNECT_SUCCESSED
            self.gatestub = client_gate_pb2.IGateService_Stub(rpc_channel)
            rpc_channel.reg_listener(self)
            if self.keyencrypter:
                self._session_seed_request()
            else:
                self._on_rpc_channel_establised(rpc_channel)
            return

    def _on_rpc_channel_establised(self, rpc_channel):
        if self.in_reconnect_status:
            self._reconnect_server(rpc_channel, self.reconnect_data)
        else:
            self._connect_server(rpc_channel)

    def register_on_event_callback(self, cb_type, callback):
        self.on_event_callback_dict[cb_type].add(callback)

    def unregister_on_event_callback(self, cb_type, callback):
        self.on_event_callback_dict[cb_type].discard(callback)

    def get_event_callback_list(self, cb_type):
        return list(self.on_event_callback_dict[cb_type])

    def _increase_seq(self):
        self.received_seq += 1

    def _session_seed_request(self):
        void = common_pb2.Void()
        self.gatestub.seed_request(None, void)
        return

    def seed_reply(self, _controller, seed, _done):
        self.sessionseed = seed
        rpc_channel = _controller.rpc_channel
        self._send_session_key(rpc_channel)

    def _send_session_key(self, rpc_channel):
        sessionkey = client_gate_pb2.SessionKey()
        import Crypto
        import random
        from Crypto.Hash import SHA
        rand = random.Random()
        random = Crypto.Random.new()
        ph_len = rand.randint(self.session_padding_min_len, self.session_padding_max_len)
        sessionkey.random_padding_header = random.read(ph_len)
        seed = random.read(32)
        key = SHA.new(seed).digest()
        sessionkey.session_key = key
        sessionkey.seed = six_ex.long_type(self.sessionseed.seed)
        pt_len = rand.randint(self.session_padding_min_len, self.session_padding_max_len)
        sessionkey.random_padding_tail = random.read(pt_len)
        encryptstr = client_gate_pb2.EncryptString()
        encryptstr.encryptstr = self.keyencrypter.encrypte(sessionkey.SerializeToString())
        self.gatestub.session_key(None, encryptstr)
        from ..common.SessionEncrypter import ARC4Crypter
        rpc_channel.set_crypter(ARC4Crypter(sessionkey.session_key), ARC4Crypter(sessionkey.session_key))
        return

    def session_key_ok(self, _controller, void, _done):
        self._on_rpc_channel_establised(_controller.rpc_channel)

    def on_channel_disconnected(self, rpc_channel):
        self.status = GateClient.ST_DISCONNECTED
        self.in_reconnect_status = False
        callback_set = self.on_event_callback_dict[GateClient.CB_ON_DISCONNECTED].copy()
        [ cb for cb in callback_set if cb() ]

    def _get_device_id(self):
        return DEVICE_ID

    def _connect_server(self, rpc_channel):
        request = common_pb2.ConnectServerRequest()
        request.type = common_pb2.ConnectServerRequest.NEW_CONNECTION
        request.deviceid = self._get_device_id()
        self.gatestub.connect_server(None, request)
        if self.zipped_enable:
            rpc_channel.set_compressor(Compressor())
        self.con_type = common_pb2.ConnectServerReply.BUSY
        return

    def _reconnect_server(self, rpc_channel, reconnect_data):
        entityid = reconnect_data['entityid']
        bin_authmsg = reconnect_data['bin_authmsg']
        request = common_pb2.ConnectServerRequest()
        request.type = common_pb2.ConnectServerRequest.RE_CONNECTION
        request.deviceid = self._get_device_id()
        request.entityid = IdManager.id2bytes(entityid)
        request.authmsg = bin_authmsg
        self.gatestub.connect_server(None, request)
        if self.zipped_enable:
            rpc_channel.set_compressor(Compressor())
        return

    def _on_reliable_message_cannot_sent(self, op_code):
        callback_set = self.on_event_callback_dict[GateClient.CB_ON_RELIABLE_MESSAGE_CANNOT_SENT].copy()
        [ cb for cb in callback_set if cb(op_code) ]

    def _get_new_server_proxy(self, stub):
        if self.use_message_cache:
            from .CachedServerProxy import CachedServerProxy
            sp = CachedServerProxy(stub, self.proto_encoder)
            sp.reg_reliable_message_cannot_sent_cb(self._on_reliable_message_cannot_sent)
            return sp
        else:
            return ServerProxy(stub, self.proto_encoder)

    def _reset_server_proxies(self, avatar_id=None):

        def _reset_server_proxy(entity):
            if not entity.server or not entity.server.is_cachable():
                server_proxy = self._get_new_server_proxy(self.gatestub)
                server_proxy.setowner(entity)
                entity.set_server(server_proxy)
            else:
                entity.server.set_stub(self.gatestub)

        if avatar_id:
            entity = EntityManager.getentity(avatar_id)
            if entity:
                _reset_server_proxy(entity)
            else:
                self.logger.error('no avata exist !!!!!!!!!!!! %s', avatar_id)
        else:
            for entity in six_ex.values(EntityManager._entities):
                _reset_server_proxy(entity)

    def connect_reply(self, _controller, reply, _done):
        self.con_type = reply.type
        if self.con_type == common_pb2.ConnectServerReply.RECONNECT_SUCCEEDED:
            ret = self._deal_reconnect_reply(reply)
            if not ret:
                self.con_type = common_pb2.ConnectServerReply.RECONNECT_FAILED
        callback_set = self.on_event_callback_dict[GateClient.CB_ON_CONNECT_REPLY].copy()
        if len(callback_set) == 0:
            return
        [ cb for cb in callback_set if cb(self.con_type) ]

    def _deal_reconnect_reply(self, reply):
        avatar_id = IdManager.bytes2id(reply.entityid) if reply.HasField('entityid') else None
        self._reset_server_proxies(avatar_id)
        avt = EntityManager.getentity(avatar_id)
        if avt is None:
            self.logger.error('Cannot find avatar when reconnect. id=%s' % avatar_id)
            return False
        else:
            if not avt.server or not avt.server.stub:
                self.logger.error('Avatar stub is not avilable. id=%s' % avatar_id)
                return False
            extramsg = self.proto_encoder.decode(reply.extramsg) if reply.HasField('extramsg') else None
            avt.on_reconnected(extramsg)
            return True

    def create_entity(self, _controller, entityinfo, _done):
        self._increase_seq()
        index = entityinfo.type.index
        if index >= 0:
            try:
                entityType = RpcIndexer.INDEX2RPC[index]
            except:
                raise RuntimeError('Failed To Decode %s(%s) EntityType With Raw [%s] Index [%d]' % (self.__class__.__name__, entityinfo.id, entityinfo.type.md5, index))

            should_send_rpc_salt = False
        else:
            entityType = entityinfo.type.md5
            should_send_rpc_salt = True
        entityid = IdManager.bytes2id(entityinfo.id)
        content_dict = self.proto_encoder.decode(entityinfo.info)
        entity = EntityFactory.instance().create_entity(entityType, entityid)
        if entity != None:
            server_proxy = self._get_new_server_proxy(self.gatestub)
            server_proxy.setowner(entity)
            entity.set_server(server_proxy)
            if should_send_rpc_salt:
                server_proxy.call_server_method('set_send_rpc_salt', {'s': RpcIndexer.RECV_RPC_SALT})
            try:
                entity.init_from_dict(content_dict)
                entity.on_entity_creation()
            except Exception:
                self._handle_last_traceback('create_entity:%s(%s) failed' % (entityType, str(entityid)))

        else:
            self.logger.error('create_entity:%s(%s) failed', entityType, str(entityid))
            return
        return

    def entity_message(self, _controller, entitymsg, _done):
        if entitymsg.reliable:
            self._increase_seq()
        try:
            entityid = IdManager.bytes2id(entitymsg.id)
        except:
            self.logger.error('entity_message, entityid %s', entitymsg.id)
            return

        entity = EntityManager.getentity(entityid)
        if entity is None:
            self.logger.error('entityMessage, entity with id %s not found', entityid)
            return
        else:
            index = entitymsg.method.index
            if index >= 0:
                try:
                    methodname = RpcIndexer.INDEX2RPC[index]
                except:
                    raise RuntimeError('Failed To Decode %s(%s) RPC Call With Raw [%s] Index [%d]' % (self.__class__.__name__, entityid, entitymsg.method.md5, index))

            else:
                entity.server.call_server_method('set_send_rpc_salt', {'s': RpcIndexer.RECV_RPC_SALT})
                methodname = entitymsg.method.md5
            if methodname is None:
                self.logger.error('entityMessage  method is not found in Md5OrIndexDecoder')
                return
            method = getattr(entity, methodname, None)
            if method is None:
                self.logger.error('entityMessage  entity:%s method:%s is not available to server', entity, methodname)
                return
            try:
                parameters = self.proto_encoder.decode(entitymsg.parameters)
                method(parameters)
            except:
                self._handle_last_traceback('entity_message:call entity method %s has exception' % method)

            return

    def destroy_entity(self, _controller, entityinfo, _done):
        self._increase_seq()
        entityid = IdManager.bytes2id(entityinfo.id)
        entity = EntityManager.getentity(entityid)
        if entity is not None:
            try:
                entity.destroy()
            except Exception:
                self._handle_last_traceback('destroy_entity: %s(%s) failed' % (entity.__class__.__name__, entityid))
                return

        return

    def reset(self, host=None, port=None):
        self.client.reset(host, port)
        self.gatestub = None
        self.reset_rpc_salt()
        return

    def reset_rpc_salt(self):
        not RpcIndexer.is_recv_indexed() and RpcIndexer.set_recv_rpc_salt(CLIENT_SALT)
        RpcIndexer.is_send_indexed() and RpcIndexer.set_send_rpc_salt(None)
        return

    def set_traceback_handler(self, handler):
        self.tb_handler = handler

    def _handle_last_traceback(self, err_str=None):
        if self.tb_handler is not None:
            t, v, tb = sys.exc_info()
            self.tb_handler(t, v, tb)
        self.logger.log_last_except()
        if err_str is not None:
            self.logger.error(err_str)
        return

    def chat_to_client(self, _controller, outbandinfo, _done):
        pass

    def dispatch_filter_message(self, _controller, filtermsg, _done):
        from ..common.FilterMessageBroker import FilterMessageBroker
        try:
            methodname, need_reg_index = Md5OrIndexDecoder.decode(filtermsg.method)
        except:
            self._handle_last_traceback('dispatch_filter_message has exception')
            return

        if methodname is None:
            self.logger.error('filterMessage  method is not found in Md5OrIndexDecoder')
            return
        else:
            try:
                parameters = self.proto_encoder.decode(filtermsg.parameters)
                FilterMessageBroker.dispatch(methodname, parameters)
            except:
                self._handle_last_traceback('filterMessage:call entity method %s has exception' % methodname)

            return

    def custom_message(self, _controller, custommsg, _done):
        pass

    def forward_aoi_info(self, _controller, aoiinfo, _done):
        from ..client import ClientRepo
        from ..client import ClientAoIData
        ClientAoIData.parse_collector_from_string(ClientRepo.aoi_updates_dispatcher, aoiinfo.info)