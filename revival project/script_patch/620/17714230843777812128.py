# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/LobbyNPC.py
from __future__ import absolute_import
from .BaseClientEntity import BaseClientEntity

class LobbyNPC(BaseClientEntity):

    def init_from_dict(self, bdict):
        self._data = bdict
        self.place_id = None
        return

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

    def on_add_to_place(self, place_id):
        logic_type = self.get_logic_type()
        self.logic = logic_type(self, self.get_battle())
        self.logic.init_from_dict(self._data)
        self._data = None
        self.place_id = place_id
        return

    def on_remove_from_place(self):
        if self.logic:
            self.logic.destroy()
            self.logic = None
        self.place_id = None
        return

    def destroy(self):
        if self.place_id:
            self.on_remove_from_place()
        super(BaseClientEntity, self).destroy()