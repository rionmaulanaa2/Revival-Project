# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/Attachable.py
from __future__ import absolute_import
from ext_package.ext_decorator import ext_clear_fashion_key
from .NPC import NPC

class Attachable(NPC):

    def __init__(self, entity_id=None):
        super(Attachable, self).__init__(entity_id)

    @ext_clear_fashion_key
    def init_from_dict(self, bdict):
        super(Attachable, self).init_from_dict(bdict)

    def on_add_to_battle(self, battle_id):
        super(Attachable, self).on_add_to_battle(battle_id)