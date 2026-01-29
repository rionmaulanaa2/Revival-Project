# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/mobile/simplerpc/defaultservice/EntityMessageWrapper.py
from __future__ import absolute_import
import sys
from ..SimpleServiceManager import SimpleServiceManager, SIMPLE_RPC_METHOD
from ..rpc_code import RPC_CODE
from ..simplerpc_common import SERVICE_CENTER_ID, addTimer, addRepeatTimer, HEART_TIMEOUT, LogManager
from ...common.proto_python import common_pb2
from ...common.IdManager import IdManager
from ...common.EntityManager import EntityManager
from ...distserver.game import GameServerRepo
WID = 'E_M_S'

class EntityMessageService(object):

    def __init__(self):
        self._logger = LogManager.get_logger('EntityMessageService')
        self._id = WID
        SimpleServiceManager.add_service(self._id, self)

    @SIMPLE_RPC_METHOD()
    def e_s(self, src_address_info, entity_id, method_name, params):
        if entity_id is None:
            entity = GameServerRepo.game_event_callback
        else:
            des_entityid = IdManager.bytes2id(entity_id)
            entity = EntityManager.getentity(des_entityid)
        if not entity:
            return
        else:
            method = getattr(entity, method_name, None)
            if not method:
                self._logger.error('visit a not exist method, %s', method_name)
                return
            mailbox = common_pb2.EntityMailbox()
            mailbox.entityid, mailbox.serverinfo.ip, mailbox.serverinfo.port, mailbox.serverinfo.servername, mailbox.serverinfo.svrtype, mailbox.serverinfo.dip, mailbox.serverinfo.dport = src_address_info
            try:
                method(mailbox, params)
            except:
                self._logger.log_last_except()
                self._logger.error('entity_message:call entity method %s has exception', method)

            return

    @SIMPLE_RPC_METHOD(response=True)
    def b_s(self, response, src_address_info, entity_id, method_name, params):
        if entity_id is None:
            entity = GameServerRepo.game_event_callback
        else:
            des_entityid = IdManager.bytes2id(entity_id)
            entity = EntityManager.getentity(des_entityid)
        if not entity:
            self._logger.error('visit a not exist entity, %s', des_entityid)
            response.send_response(code=RPC_CODE.NOT_ENTITY, error='%s entity not exist' % des_entityid)
            return
        else:
            method = getattr(entity, method_name, None)
            if not method:
                response.send_response(code=RPC_CODE.NOT_METHOD, error='%s method not exist' % method_name)
                return
            mailbox = common_pb2.EntityMailbox()
            mailbox.entityid, mailbox.serverinfo.ip, mailbox.serverinfo.port, mailbox.serverinfo.servername, mailbox.serverinfo.svrtype, mailbox.serverinfo.dip, mailbox.serverinfo.dport = src_address_info
            try:
                method((response, mailbox), params)
            except:
                self._logger.log_last_except()
                self._logger.error('entity_message:call entity method %s has exception', method)
                if not response.send:
                    response.send_response(code=RPC_CODE.EXEC_ERROR, error='execute error')

            return