# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/avatarmembers/impSoul.py
from __future__ import absolute_import
from mobile.common.rpcdecorator import rpc_method, CLIENT_STUB
from mobile.common.RpcMethodArgs import Str, Dict, Uuid, Int, Bool

class impSoul(object):

    @rpc_method(CLIENT_STUB, (Str('entity_type'), Dict('entity_dict'), Uuid('entity_id')))
    def soul_create_entity(self, entity_type, entity_dict, entity_id):
        from mobile.common.EntityManager import EntityManager
        from mobile.common.EntityFactory import EntityFactory
        entity = EntityManager.getentity(entity_id)
        if entity is None:
            entity = EntityFactory.instance().create_entity(entity_type, entity_id)
        if entity is not None:
            entity.init_from_dict(entity_dict)
        return

    def local_soul_create_entity(self, entity_type, entity_dict, entity_id):
        from mobile.common.EntityManager import EntityManager
        from mobile.common.EntityFactory import EntityFactory
        entity = EntityManager.getentity(entity_id)
        if entity is None:
            entity = EntityFactory.instance().create_entity(entity_type, entity_id)
        if entity is not None:
            entity.init_from_dict(entity_dict)
        return

    @rpc_method(CLIENT_STUB, (Uuid('entity_id'),))
    def soul_destroy_entity(self, entity_id):
        from mobile.common.EntityManager import EntityManager
        entity = EntityManager.getentity(entity_id)
        if entity is None:
            return
        else:
            entity.destroy()
            return

    @rpc_method(CLIENT_STUB, (Uuid('entity_id'),))
    def soul_destroyed_entity(self, entity_id):
        from mobile.common.EntityManager import EntityManager
        entity = EntityManager.getentity(entity_id)
        if entity is None:
            return
        else:
            battle = self.get_battle()
            if not battle or not battle.destroy_entity(entity_id):
                entity.destroy()
            return

    @rpc_method(CLIENT_STUB, (Str('ip'), Int('port'), Str('token'), Bool('kcp_valid')))
    def direct_bind_soul(self, ip, port, token, kcp_valid):
        global_data.connect_helper.connect_battle(self, ip, port, token, lambda code, con_type, ip=ip, port=port: self.call_server_method('direct_bind_soul_callback', (int(code), con_type, ip, port), False), kcp_valid)

    @rpc_method(CLIENT_STUB, ())
    def direct_unbind_soul(self):
        global_data.connect_helper.disconnect_battle()