# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/NPC.py
from __future__ import absolute_import
from .BaseClientEntity import BaseClientEntity

class NPC(BaseClientEntity):

    def init_from_dict(self, bdict):
        self._data = bdict

    def update_from_dict(self, bdict):
        self._data = bdict

    def get_logic_type(self):
        type_name = 'L%s' % self.__class__.__name__
        mod = __import__('logic.units', globals(), locals(), [type_name])
        mod = getattr(mod, type_name, None)
        logic_type = getattr(mod, type_name, None)
        if getattr(logic_type, 'MASK', None) is None:
            logic_type.MASK = 0
        return logic_type

    def on_add_to_battle(self, battle_id):
        super(NPC, self).on_add_to_battle(battle_id)
        logic_type = self.get_logic_type()
        self.logic = logic_type(self, self.get_battle())
        self.logic.init_from_dict(self._data)
        self._data = None
        return

    def on_remove_from_battle(self):
        if self.logic:
            self.logic.destroy()
            self.logic = None
        super(NPC, self).on_remove_from_battle()
        return

    def on_update_to_battle(self, battle_id):
        if self.logic:
            self.logic.update_from_dict(self._data)
        self._data = None
        return

    def call_soul_method(self, methodname, parameters=()):
        if global_data.player:
            global_data.player.call_soul_method(methodname, parameters, self.id)


class CacheableNPC(NPC):

    def is_cacheable(self):
        return True

    def cache(self):
        self._data = None
        super(CacheableNPC, self).cache()
        return


class FullCacheableNPC(NPC):

    def __init__(self, entityid=None):
        super(FullCacheableNPC, self).__init__(entityid)
        self._cache_logic = None
        return

    def is_cacheable(self):
        return True

    def cache(self):
        self._data = None
        super(FullCacheableNPC, self).cache()
        return

    def on_add_to_battle(self, battle_id):
        super(NPC, self).on_add_to_battle(battle_id)
        battle = self.get_battle()
        if self._cache_logic:
            self.logic = self._cache_logic
            self._cache_logic = None
            self.logic.reuse(self, battle)
        else:
            logic_type = self.get_logic_type()
            self.logic = logic_type(self, battle, True)
        self.logic.init_from_dict(self._data)
        self._data = None
        return

    def on_remove_from_battle(self):
        if self.logic:
            self.logic.cache()
            self._cache_logic = self.logic
            self.logic = None
        super(NPC, self).on_remove_from_battle()
        return

    def destroy(self):
        if self._cache_logic:
            self._cache_logic.destroy()
            self._cache_logic = None
        super(FullCacheableNPC, self).destroy()
        return