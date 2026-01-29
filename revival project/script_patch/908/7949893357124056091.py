# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gutils/entity_info_cache_utils.py
from __future__ import absolute_import
import six_ex
import six

class EntityInfoCache(object):
    CONCERNS_VAL = {}

    def __init__(self):
        self._entity_info = {}
        self.init_event()
        self._to_bind_events = {}
        self._binded_event = {}
        self.init_bind_events()

    def init_event(self):
        pass

    def unbind_event(self):
        pass

    def add_player(self, ent_id):
        from mobile.common.EntityManager import EntityManager
        ent = EntityManager.getentity(ent_id)
        if ent and ent.logic:
            self.on_add_player(ent.logic)

    def del_player(self, ent_id):
        from mobile.common.EntityManager import EntityManager
        if ent_id in self._entity_info:
            self.on_before_del_player(ent_id, self._entity_info[ent_id])
            ent = EntityManager.getentity(ent_id)
            if ent and ent.logic:
                self.unbind_player_event(ent.logic)
                del self._binded_event[ent_id]
            del self._entity_info[ent_id]

    def on_before_del_player(self, ent_id, ent_info):
        pass

    def on_add_player(self, lplayer):
        if lplayer.id not in self._entity_info:
            self._entity_info[lplayer.id] = {}
        for event_name, event_conf in six.iteritems(self.CONCERNS_VAL):
            key, def_val = event_conf
            if lplayer:
                self._entity_info[lplayer.id].update({key: lplayer.get_value(event_name)})

        self.bind_player_event(lplayer)

    def bind_player_event(self, lplayer):
        from common.framework import Functor
        if not lplayer:
            return
        else:
            need_binded_event = self.get_bind_events()
            if lplayer.id in self._binded_event:
                return
            self._binded_event[lplayer.id] = {}
            for event_name, event_conf in six.iteritems(need_binded_event):
                func = event_conf.get('func', None)
                if not func:
                    continue
                bind_func = Functor(func, lplayer.id)
                lplayer.regist_event(event_name, bind_func)
                self._binded_event[lplayer.id].update({event_name: bind_func})

            return

    def unbind_player_event(self, lplayer):
        if not lplayer:
            return
        for lplayer.id in self._binded_event:
            for event_name, bind_func in six.iteritems(self._binded_event[lplayer.id]):
                lplayer.unregist_event(event_name, bind_func)

    def unbind_all_player(self):
        from mobile.common.EntityManager import EntityManager
        for pl_id in six_ex.keys(self._entity_info):
            ent = EntityManager.getentity(pl_id)
            if ent and ent.logic:
                self.unbind_player_event(ent.logic)

        self._binded_event = {}

    def init_bind_events(self):
        self._to_bind_events = {}

    def get_bind_events(self):
        return self._to_bind_events

    def regist_bind_event(self, event, func):
        self._to_bind_events[event] = {'func': func}

    def destroy(self):
        self._entity_info = {}
        self.unbind_event()
        self.unbind_all_player()
        self._to_bind_events = {}

    def _get_all_entities(self, entity_type):
        from mobile.common.EntityManager import EntityManager
        all_player = EntityManager.get_entities_by_type(entity_type)
        return all_player

    def update_player_info(self, pid, key, val):
        if pid in self._entity_info:
            self._entity_info[pid].update({key: val})
        else:
            log_error('entity id %s is not in cache!' % pid)

    def get_player_info(self, pid):
        return self._entity_info.get(pid, {})

    def get_all_player_info(self):
        return self._entity_info