# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/parts/PartTestBase.py
from __future__ import absolute_import
from . import ScenePart

class PartTestBase(ScenePart.ScenePart):

    def __init__(self, scene, name, need_update=False):
        super(PartTestBase, self).__init__(scene, name, need_update)
        global_data.game_mgr.remove_patch_ui()
        global_data.game_mgr.init_ingame_env()