# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/parts/PartArtCheckUI.py
from __future__ import absolute_import
from . import ScenePart

class PartArtCheckUI(ScenePart.ScenePart):
    ENTER_EVENT = {}

    def __init__(self, scene, name):
        super(PartArtCheckUI, self).__init__(scene, name, False)

    def on_enter(self, *args):
        if global_data.artcheck_human_display_editor:
            return
        from editors import main_window
        main_window.start_human_editor()