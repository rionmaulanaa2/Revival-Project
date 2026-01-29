# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/mobile/simplerpc/defaultservice/DirectEntityService.py
from __future__ import absolute_import
import sys
from ..SimpleServiceManager import SIMPLE_RPC_METHOD
from ..rpc_code import RPC_CODE
import random
from ...common.EntityManager import EntityManager
from ...common.IdManager import IdManager
from ...common.rpcdecorator import expose_to_client
from ..simplerpc_common import LogManager

class DirectEntityServiceForServer(object):

    def __init__(self, key_path=None):
        object.__init__(self)
        self.logger = LogManager.get_logger('DirectEntityService')
        self._key_path = key_path
        self._need_check = dict()

    def handle_connection_close(self, con):
        try:
            del self._need_check[con]
        except:
            pass

    @SIMPLE_RPC_METHOD(response=True)
    def request_seed(self, response):
        response.connection.add_disconnect_cb(lambda : self.handle_connection_close(response.connection))
        seed = random.randint(0, 100000000)
        self._need_check[response.connection] = seed
        response.connection.delay_enable_compress()
        response.send_response(code=RPC_CODE.OK, args=seed)

    @SIMPLE_RPC_METHOD(response=True)
    def check_seed(self, response, data):
        from ...common.mobilecommon import asiocore
        now_con = response.connection

        def _decrypte_cb(status, seed, key):
            if not status:
                self.logger.error('decrypte session data error')
                now_con.close()
            elif now_con in self._need_check and seed == self._need_check[now_con]:
                now_con.enable_encrypter(key)
                now_con.check_finish = True
                response.send_response(code=RPC_CODE.OK)
                del self._need_check[now_con]
            else:
                if now_con in self._need_check:
                    self.logger.error('check seed error, seed not correct, %s - %s', seed, self._need_check[now_con])
                now_con.close()

        asiocore.decrypte_session_key(data, _decrypte_cb)

    @SIMPLE_RPC_METHOD(response=True)
    def bind_entity(self, response, entityid_bytes, client_entityid_bytes, bind_token):
        from ...servercommon.ServerEntity import DirectBindEntity
        if not response.connection.check_finish:
            self.logger.error('connection not enable_encrypter')
            response.connection.close()
            return
        entityid = IdManager.bytes2id(entityid_bytes)
        client_entityid = IdManager.bytes2id(client_entityid_bytes)
        server_entity = EntityManager.getentity(entityid)
        if not server_entity:
            response.send_response(code=RPC_CODE.NOT_ENTITY, error='entity not exist ' + str(entityid))
            return
        if not isinstance(server_entity, DirectBindEntity):
            response.send_response(code=RPC_CODE.NOT_ENTITY, error='entity type is not DirectEntityService ' + str(entityid))
            return
        res = server_entity.direct_bind_client(client_entityid, response.connection, bind_token)
        if res:
            response.connection.entity = server_entity
            response.send_response(code=RPC_CODE.OK)
            try:
                server_entity.on_client_bind_success()
            except:
                self.logger.log_last_except()

        else:
            response.send_response(code=RPC_CODE.BAD_TOKEN, error='bind fail')

    @SIMPLE_RPC_METHOD(inject_con=True)
    def entity_message(self, connection, method_name, parameters, entityid):
        owner = connection.entity
        if not connection.check_finish or not owner:
            self.logger.error('connection not enable_encrypter')
            connection.close()
            return
        else:
            if entityid:
                entity = EntityManager.getentity(entityid) if 1 else owner
                if entity is None:
                    try:
                        owner.notify_destroyed_entity(entityid)
                    except:
                        self.logger.log_last_except()
                        self.logger.error('[entity_message] entity with id(%s) destroy failed', entityid)

                    return
                if not owner.is_belong_to(entity.id):
                    if owner.log_not_belong_to(entity.id):
                        self.logger.error('[entity_message] entity with id(%s) not belong to client, methodname: %s', entityid, method_name)
                    return
                method = getattr(entity, method_name, None)
                if not method:
                    self.logger.error('[entity_message] entity:%s  method:%s not exist', entity, method_name)
                    return
                expose_to_client(method) or self.logger.error('[entity_message] entity:%s  method:%s can not invoke by client', entity, method_name)
                return
            try:
                method(owner.id, parameters)
            except:
                self.logger.log_last_except()

            return


class DirectEntityServiceForClient(object):

    def __init__(self, tb_handler=None):
        object.__init__(self)
        self.logger = LogManager.get_logger('DirectEntityServiceForClient')
        self.tb_handler = tb_handler

    def set_traceback_handler(self, handler):
        self.tb_handler = handler

    def _handle_last_traceback(self, err_str=None):
        if self.tb_handler is not None:
            t, v, tb = sys.exc_info()
            self.tb_handler(t, v, tb)
        if err_str is not None:
            self.logger.error(err_str)
        self.logger.log_last_except()
        return

    @SIMPLE_RPC_METHOD(inject_con=True)
    def entity_message(self, connection, method_name, parameters, entity_id=None):
        if not connection.entity:
            self.logger.error('call direct client entity method, but do not bind')
            return
        else:
            if entity_id:
                entity = EntityManager.getentity(entity_id) if 1 else connection.entity
                if entity is None or not entity.is_valid:
                    self.logger.error('entity:%s not exist', entity_id)
                    return
                method = getattr(entity, method_name, None)
                method or self.logger.error('entity:%s  method:%s not exist', entity, method_name)
                return
            try:
                method(parameters)
            except:
                self._handle_last_traceback('entity_message:call entity method %s has exception' % method)

            return