# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/mobile/client/AsioUdpGateClient.py
from __future__ import absolute_import
from __future__ import print_function
import six_ex
from ..common.proto_python import client_gate_pb2
from ..common.proto_python import common_pb2
from ..mobilelog.LogManager import LogManager
from ..common.EntityFactory import EntityFactory
from ..common.IdManager import IdManager
from mobileProxy import AsioServerProxy
from ..common.EntityManager import EntityManager
from ..common.RpcIndex import RpcIndexer, CLIENT_SALT
from ..common.Md5OrIndexCodec import Md5OrIndexEncoder, Md5OrIndexDecoder
import sys
from ..common.FilterMessageBroker import FilterMessageBroker
from ..common.mobilecommon import asiocore
from ..mobilerpc.AsioUdpChannelClient import AsioUdpChannelClient
DEVICE_ID = str(IdManager.genid())

class AsioUdpGateClient(asiocore.rpc_handler):
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

    def __init__(self, host, ip, clientconf, proto_encoder):
        super(AsioUdpGateClient, self).__init__(asiocore.service_type.gate_client)
        self.logger = LogManager.get_logger('server.AsioUdpGateClient')
        self.status = AsioUdpGateClient.ST_INIT
        self.client = AsioUdpChannelClient(host, ip, self)
        self.in_reconnect_status = False
        self.reconnect_data = None
        self.encoder = Md5OrIndexEncoder()
        self.tb_handler = None
        self.proto_encoder = proto_encoder
        self.enforce_encryption = bool(clientconf.get('enforce_encryption', False))
        self.loginkeypath = clientconf.get('loginkeypath', None)
        self.encrypted = False
        self.zipped_enable = clientconf.get('zipped_channel', 0)
        self.compressor = False
        self.received_seq = 0
        self.use_message_cache = False
        self.session_padding_min_len = 16
        self.session_padding_max_len = 64
        self.con_type = common_pb2.ConnectServerReply.BUSY
        self.sessionseed = None
        if self.enforce_encryption:
            asiocore.set_login_path(self.loginkeypath)
        self.on_event_callback_dict = {AsioUdpGateClient.CB_ON_CONNECT_FAILED: set(),
           AsioUdpGateClient.CB_ON_CONNECT_SUCCESSED: set(),
           AsioUdpGateClient.CB_ON_DISCONNECTED: set(),
           AsioUdpGateClient.CB_ON_CONNECT_REPLY: set(),
           AsioUdpGateClient.CB_ON_RELIABLE_MESSAGE_CANNOT_SENT: set()
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
        self.status = AsioUdpGateClient.ST_CONNECTING
        self._connect(self.channel_cb, timeout)

    def resume_game(self, timeout, entityid, bin_authmsg):
        self.reset_rpc_salt()
        self.status = AsioUdpGateClient.ST_RECONNECTING
        self.reconnect_data = {'entityid': entityid,'bin_authmsg': bin_authmsg}
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
        if not rpc_channel:
            self.status = AsioUdpGateClient.ST_CONNECT_FAILED
            callback_set = self.on_event_callback_dict[AsioUdpGateClient.CB_ON_CONNECT_FAILED].copy()
            [ cb for cb in callback_set if cb() ]
            return
        callback_set = self.on_event_callback_dict[AsioUdpGateClient.CB_ON_CONNECT_SUCCESSED].copy()
        [ cb for cb in callback_set if cb() ]
        self.in_reconnect_status = self.status == AsioUdpGateClient.ST_RECONNECTING
        self.status = AsioUdpGateClient.ST_CONNECT_SUCCESSED
        if self.enforce_encryption:
            self._session_seed_request()
        else:
            self._on_rcp_channel_establised()

    def _on_rcp_channel_establised(self):
        if self.in_reconnect_status:
            self._reconnect_server(self.reconnect_data)
        else:
            self._connect_server()

    def register_on_event_callback(self, cb_type, callback):
        self.on_event_callback_dict[cb_type].add(callback)

    def unregister_on_event_callback(self, cb_type, callback):
        self.on_event_callback_dict[cb_type].discard(callback)

    def get_event_callback_list(self, cb_type):
        return list(self.on_event_callback_dict[cb_type])

    def _increase_seq(self):
        self.received_seq += 1

    def _session_seed_request(self):
        self.dispatch_rpc('send_seed_request')

    def seed_reply(self, seed):
        self.sessionseed = seed
        self._send_session_key()

    def _send_session_key(self):
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
        self.dispatch_rpc('send_session_key', sessionkey.SerializeToString())
        self.enable_encrypter(sessionkey.session_key)
        self.encrypted = True

    def session_key_ok(self):
        self._on_rcp_channel_establised()

    def on_channel_disconnected(self):
        self.status = AsioUdpGateClient.ST_DISCONNECTED
        self.in_reconnect_status = False
        callback_set = self.on_event_callback_dict[AsioUdpGateClient.CB_ON_DISCONNECTED].copy()
        print('on_channel_disconnected set', callback_set)
        [ cb for cb in callback_set if cb() ]

    def _get_device_id(self):
        return DEVICE_ID

    def _connect_server(self):
        self.dispatch_rpc('send_connect_server', common_pb2.ConnectServerRequest.NEW_CONNECTION, self._get_device_id(), '', '')
        if self.zipped_enable:
            self.enable_compressor(True)
            self.compressor = True
        self.con_type = common_pb2.ConnectServerReply.BUSY

    def _reconnect_server(self, rpc_channel, reconnect_data):
        entityid = reconnect_data['entityid']
        bin_authmsg = reconnect_data['bin_authmsg']
        self.dispatch_rpc('send_connect_server', common_pb2.ConnectServerRequest.RE_CONNECTION, self._get_device_id(), IdManager.id2bytes(entityid), bin_authmsg)
        if self.zipped_enable:
            self.enable_compressor(True)
            self.compressor = True

    def _on_reliable_message_cannot_sent(self, op_code):
        callback_set = self.on_event_callback_dict[AsioUdpGateClient.CB_ON_RELIABLE_MESSAGE_CANNOT_SENT].copy()
        [ cb for cb in callback_set if cb(op_code) ]

    def _get_new_server_proxy(self, encoder):
        if self.use_message_cache:
            from .CachedServerProxy import AsioCachedServerProxy
            sp = AsioCachedServerProxy(self, encoder, self.proto_encoder)
            sp.reg_reliable_message_cannot_sent_cb(self._on_reliable_message_cannot_sent)
            return sp
        else:
            return AsioServerProxy(self, encoder, self.proto_encoder)

    def _reset_server_proxies(self, avatar_id=None):
        for entity in six_ex.values(EntityManager._entities):
            if not entity.server or not entity.server.is_cachable():
                server_proxy = self._get_new_server_proxy(self.encoder)
                server_proxy.setowner(entity)
                entity.set_server(server_proxy)
            else:
                entity.server.set_stub(self)

    def connect_reply(self, typ, entityid, extramsg):
        self.con_type = typ
        if self.con_type == common_pb2.ConnectServerReply.RECONNECT_SUCCEEDED:
            ret = self._deal_reconnect_reply(entityid, extramsg)
            if not ret:
                self.con_type = common_pb2.ConnectServerReply.RECONNECT_FAILED
        callback_set = self.on_event_callback_dict[AsioUdpGateClient.CB_ON_CONNECT_REPLY].copy()
        if len(callback_set) == 0:
            return
        [ cb for cb in callback_set if cb(self.con_type) ]

    def _deal_reconnect_reply(self, entityid, extramsg):
        avatar_id = IdManager.bytes2id(entityid) if entityid else None
        self._reset_server_proxies(avatar_id)
        avt = EntityManager.getentity(avatar_id)
        if avt is None:
            self.logger.error('Cannot find avatar when reconnect. id=%s' % avatar_id)
            return False
        else:
            if not avt.server or not avt.server.stub:
                self.logger.error('Avatar stub is not avilable. id=%s' % avatar_id)
                return False
            extramsg = extramsg if extramsg else None
            avt.on_reconnected(extramsg)
            return True

    def chat_to_client(self, message):
        pass

    def create_entity(self, raw, index, eid, info):
        self._increase_seq()
        if index >= 0:
            try:
                entityType = RpcIndexer.INDEX2RPC[index]
            except:
                raise RuntimeError('Failed To Decode %s(%s) EntityType With Raw [%s] Index [%d]' % (self.__class__.__name__, IdManager.bytes2id(eid), raw, index))

            should_send_rpc_salt = False
        else:
            entityType = raw
            should_send_rpc_salt = True
        entityid = IdManager.bytes2id(eid)
        content_dict = self.proto_encoder.decode(info)
        entity = EntityFactory.instance().create_entity(entityType, entityid)
        if entity != None:
            server_proxy = self._get_new_server_proxy(self.encoder)
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

    def entity_message(self, reliable, eid, raw, index, parameters, localid):
        if reliable:
            self._increase_seq()
        try:
            entityid = IdManager.bytes2id(eid)
        except:
            self.logger.error('entity_message, entityid %s, localid %d', eid, localid)
            return

        entity = EntityManager.getentity(entityid)
        if entity is None:
            self.logger.error('entityMessage, entity with id %s not found', entityid)
            return
        else:
            if index >= 0:
                try:
                    methodname = RpcIndexer.INDEX2RPC[index]
                except:
                    raise RuntimeError('Failed To Decode %s(%s) RPC Call With Raw [%s] Index [%d]' % (self.__class__.__name__, entityid, raw, index))

            else:
                entity.server.call_server_method('set_send_rpc_salt', {'s': RpcIndexer.RECV_RPC_SALT})
                methodname = raw
            if methodname is None:
                self.logger.error('entityMessage  method is not found in RpcIndexer')
                return
            method = getattr(entity, methodname, None)
            if method is None:
                self.logger.error('entityMessage  entity:%s method:%s is not available to server', entity, methodname)
                return
            try:
                method(self.proto_encoder.decode(parameters))
            except:
                self._handle_last_traceback('entity_message:call entity method %s has exception' % method)

            return

    def destroy_entity(self, eid):
        self._increase_seq()
        entityid = IdManager.bytes2id(eid)
        entity = EntityManager.getentity(entityid)
        if entity != None:
            try:
                entity.destroy()
            except Exception:
                self._handle_last_traceback('destroy_entity: %s(%s) failed' % (entity.__class__.__name__, entityid))
                return

        return

    def reset(self, host=None, port=None):
        self.client.reset(host, port)
        self.reset_rpc_salt()

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
        print('exception log:')
        self.logger.log_last_except()
        if err_str is not None:
            self.logger.error(err_str)
        return

    def dispatch_filter_message(self, md5, index, parameters):
        try:
            methodname, need_reg_index, index = Md5OrIndexDecoder.raw_decode(md5, index)
        except:
            self._handle_last_traceback('dispatch_filter_message has exception')
            return

        if methodname is None:
            self.logger.error('filterMessage  method is not found in Md5OrIndexDecoder')
            return
        else:
            try:
                parameters = self.proto_encoder.decode(parameters)
                FilterMessageBroker.dispatch(methodname, parameters)
            except:
                self._handle_last_traceback('filterMessage:call entity method %s has exception' % methodname)

            return