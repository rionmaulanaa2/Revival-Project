# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/Hiding.py
from __future__ import absolute_import
from .NPC import NPC

class Hiding(NPC):

    def __init__(self, entity_id=None):
        super(Hiding, self).__init__(entity_id)

    def init_from_dict(self, bdict):
        super(Hiding, self).init_from_dict(bdict)

    def on_add_to_battle(self, battle_id):
        from mobile.common.EntityManager import EntityManager
        super(Hiding, self).on_add_to_battle(battle_id)
        hide_puppet_id = self.logic.ev_g_puppet()
        hide_puppet = None
        if hide_puppet_id:
            hide_puppet = EntityManager.getentity(hide_puppet_id)
        if hide_puppet:
            hide_puppet.logic.send_event('E_ENTER_HIDING')
        return