# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/mobile/common/EntityFactory.py
from __future__ import absolute_import
import six_ex
from functools import cmp_to_key
from ..mobilelog.LogManager import LogManager
from .mobilecommon import extendabletype
from .RpcIndex import RpcIndexer
import six

class EntityFactory(six.with_metaclass(extendabletype, object)):
    _instance = None

    def __init__(self):
        self.logger = LogManager.get_logger('server.EntityFactory')
        self.entity_classes = {}

    @classmethod
    def instance(cls):
        if cls._instance == None:
            cls._instance = EntityFactory()
        return cls._instance

    def register_entity(self, entitytype, entityclass):
        self.entity_classes[entitytype] = entityclass
        RpcIndexer.register_rpc(entityclass.__name__)
        import inspect
        if six.PY2:
            methods = inspect.getmembers(entityclass, predicate=inspect.ismethod)
        else:
            methods = inspect.getmembers(entityclass, predicate=inspect.isfunction)
        methods.sort(key=cmp_to_key(--- This code section failed: ---

  41       0  LOAD_GLOBAL           0  'six_ex'
           3  LOAD_ATTR             1  'compare'
           6  LOAD_ATTR             1  'compare'
           9  BINARY_SUBSCR    
          10  LOAD_FAST             1  'b'
          13  LOAD_CONST            1  ''
          16  BINARY_SUBSCR    
          17  CALL_FUNCTION_2       2 
          20  RETURN_VALUE_LAMBDA
          -1  LAMBDA_MARKER    

Parse error at or near `BINARY_SUBSCR' instruction at offset 9
))
        for method in methods:
            if not method[0].startswith('_'):
                RpcIndexer.register_rpc(method[0])

    def get_entity_class(self, entitytype):
        EntityClass = None
        if isinstance(entitytype, str):
            EntityClass = self.entity_classes.get(entitytype, None)
        elif isinstance(entitytype, type):
            EntityClass = entitytype
        return EntityClass

    def create_entity(self, entitytype, entityid=None):
        EntityClass = self.get_entity_class(entitytype)
        if not EntityClass:
            self.logger.error('failed to create entity for type %s id %s', str(entitytype), str(entityid))
            return
        else:
            if entityid == None:
                return EntityClass()
            return EntityClass(entityid)
            return