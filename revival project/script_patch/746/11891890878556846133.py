# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/mobile/client/ServerProxy.py
from __future__ import absolute_import
from ..common.IdManager import IdManager
from ..mobilelog.LogManager import LogManager
from ..common.proto_python.common_pb2 import EntityMessage, ServiceMessage, ServiceId, ForwardAoiInfo, CustomMessage
from ..common.RpcIndex import RpcIndexer

class ServerProxy(object):

    def __init__(self, stub, proto_encoder):
        super(ServerProxy, self).__init__()
        self.logger = LogManager.get_logger('ServerProxy')
        self.stub = stub
        stub.rpc_channel.reg_listener(self)
        self.owner = None
        self.owner_id_bytes = None
        self.proto_encoder = proto_encoder
        return

    def setowner(self, owner):
        self.owner = owner
        self.owner_id_bytes = IdManager.id2bytes(self.getownerid()) if owner else None
        return

    def call_server_method(self, methodname, parameters=None, entityid=None):
        entityid = entityid and IdManager.id2bytes(entityid) if 1 else self.owner_id_bytes
        if entityid == None:
            self.logger.error(' call_server_method not find owner %s, need pass entityid to call %s', str(self.owner), methodname)
            return
        else:
            entitymsg = EntityMessage()
            entitymsg.id = entityid
            entitymsg.method.index, entitymsg.method.md5 = RpcIndexer.try_encode(methodname)
            if parameters != None:
                entitymsg.parameters = self.proto_encoder.encode(parameters)
            self.stub.entity_message(None, entitymsg)
            return

    def call_soul_method(self, methodname, parameters=None, entityid=None):
        entityid = entityid and IdManager.id2bytes(entityid) if 1 else self.owner_id_bytes
        if entityid == None:
            self.logger.error(' call_soul_method not find owner %s, need pass entityid to call %s', str(self.owner), methodname)
            return
        else:
            entitymsg = EntityMessage()
            entitymsg.id = entityid
            entitymsg.method.index, entitymsg.method.md5 = RpcIndexer.try_encode(methodname)
            if parameters != None:
                entitymsg.parameters = self.proto_encoder.encode(parameters)
            self.stub.soul_message(None, entitymsg)
            return

    def custom_message(self, routetype=None, strid='', intid=-1, msg=None):
        custommsg = CustomMessage()
        if msg != None:
            custommsg.msg = msg
        if routetype != None:
            custommsg.route.type = routetype
        if strid != '':
            custommsg.route.strid = strid
        if intid != -1:
            custommsg.route.intid = intid
        self.stub.custom_message(None, custommsg)
        return

    def getownerid(self):
        if self.owner:
            return self.owner.id
        else:
            return None

    def on_channel_disconnected(self, _rpc_channel):
        self.owner.on_lose_server()
        self.owner.set_server(None)
        self.owner = None
        self.destroy()
        return

    def destroy(self):
        self.stub.rpc_channel.unreg_listener(self)
        self.stub = None
        self.owner = None
        return

    def is_cachable(self):
        return False

    def send_aoi_posdir_info(self, id, posdir):
        from . import ClientAoIData
        info = ForwardAoiInfo()
        info.id = IdManager.id2bytes(id)
        info.info = ClientAoIData.serialized_posdir_to_string(posdir)
        self.stub.forward_aoi_pos_info(None, info)
        return

    def send_aoi_posdir_info_raw(self, id, info):
        info = ForwardAoiInfo()
        info.id = IdManager.id2bytes(id)
        info.info = info
        self.stub.forward_aoi_pos_info(None, info)
        return


class AsioServerProxy(object):

    def __init__(self, stub, proto_encoder):
        super(AsioServerProxy, self).__init__()
        self.stub = stub
        self.owner = None
        self.owner_id_bytes = None
        self.logger = LogManager.get_logger('AsioServerProxy')
        self.proto_encoder = proto_encoder
        return

    def setowner(self, owner):
        self.owner = owner
        self.owner_id_bytes = IdManager.id2bytes(self.getownerid()) if owner else None
        return

    def call_server_method(self, methodname, parameters=None, entityid=None):
        entityid = entityid and IdManager.id2bytes(entityid) if 1 else self.owner_id_bytes
        if entityid == None:
            self.logger.error('call_server_method: not find owner %s, need entityid %s', str(self.owner), methodname)
            return
        else:
            localid = -1
            index, raw = RpcIndexer.try_encode(methodname)
            args = '' if parameters is None else self.proto_encoder.encode(parameters)
            self.stub.dispatch_rpc('send_entity_message', entityid, raw, index, args, True, localid)
            return

    def call_soul_method(self, methodname, parameters=None, entityid=None):
        entityid = entityid and IdManager.id2bytes(entityid) if 1 else self.owner_id_bytes
        if entityid == None:
            self.logger.error('call_soul_method: not find owner %s, need entityid %s', str(self.owner), methodname)
            return
        else:
            localid = -1
            index, raw = RpcIndexer.try_encode(methodname)
            args = '' if parameters is None else self.proto_encoder.encode(parameters)
            self.stub.dispatch_rpc('send_soul_message', entityid, raw, index, args, True, localid)
            return

    def getownerid(self):
        if self.owner:
            return self.owner.id
        else:
            return None

    def on_channel_disconnected(self):
        self.owner.on_lose_server()
        self.owner.set_server(None)
        self.setowner(None)
        self.destroy()
        return

    def destroy(self):
        self.stub = None
        self.setowner(None)
        return

    def is_cachable(self):
        return False