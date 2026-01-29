# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gutils/EntityPool.py
from __future__ import absolute_import
import six
from collections import defaultdict
from mobile.common.EntityFactory import EntityFactory
from mobile.common.IdManager import IdManager
entity_factory = EntityFactory.instance()

class EntityPool(object):
    _cache_dict = defaultdict(list)

    @staticmethod
    def create_entity(entitytype, entityid=None):
        if entitytype in EntityPool._cache_dict and EntityPool._cache_dict[entitytype]:
            entity = EntityPool._cache_dict[entitytype].pop()
            entityid = IdManager.genid() if entityid is None else entityid
            entity.reuse(entityid)
        else:
            entity = entity_factory.create_entity(entitytype, entityid)
        return entity

    @staticmethod
    def destroy_entity(entity):
        if entity.is_cacheable():
            EntityPool._cache_dict[entity.__class__.__name__].append(entity)
            entity.cache()
        else:
            entity.destroy()

    @staticmethod
    def clear():
        for entity_list in six.itervalues(EntityPool._cache_dict):
            for entity in entity_list:
                entity.destroy()

        EntityPool._cache_dict.clear()

    @staticmethod
    def dump():
        for entitytype, entity_list in six.iteritems(EntityPool._cache_dict):
            pass