# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/GodCamera.py
from __future__ import absolute_import
from .NPC import NPC

class GodCamera(NPC):

    def __init__(self, entity_id=None):
        super(GodCamera, self).__init__(entity_id)
        self.ob_uid = None
        return

    def init_from_dict(self, bdict):
        super(GodCamera, self).init_from_dict(bdict)
        self.ob_uid = bdict.get('ob_uid')

    def on_add_to_battle(self, battle_id):
        super(GodCamera, self).on_add_to_battle(battle_id)

    def get_ob_uid(self):
        return self.ob_uid