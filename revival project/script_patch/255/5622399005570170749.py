# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/parts/PartWanfa.py
from __future__ import absolute_import
from . import ScenePart

class PartWanfa(ScenePart.ScenePart):

    def __init__(self, scene, name):
        super(PartWanfa, self).__init__(scene, name)
        self.wanfa_instance = None
        return

    def on_enter(self):
        battle_name = global_data.battle.__class__.__name__
        from logic.wanfa.WanfaManager import init_wanfa
        self.wanfa_instance = init_wanfa(battle_name)

    def on_exit(self):
        if self.wanfa_instance:
            self.wanfa_instance.destroy()
        self.wanfa_instance = None
        return