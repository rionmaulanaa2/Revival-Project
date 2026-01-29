# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/parts/PartScriptLowFPS.py
from __future__ import absolute_import
from . import ScenePart
import game3d

class PartScriptLowFPS(ScenePart.ScenePart):
    INIT_EVENT = {'app_frame_rate_changed_event': 'on_frame_rate_changed',
       'settle_stage_event': 'on_battle_end'
       }

    def __init__(self, scene, name):
        super(PartScriptLowFPS, self).__init__(scene, name)
        self._has_enter = False

    def on_enter(self):
        self._has_enter = True
        self._enable_low_fps()

    def on_exit(self):
        global_data.game_mgr.enable_low_script_update(False)

    def on_battle_end(self, *args):
        self.on_exit()

    def on_frame_rate_changed(self):
        self._enable_low_fps()

    def _enable_low_fps(self):
        import world
        if self._has_enter and global_data.server_enable_low_fps and hasattr(world.model, 'rotate_delta_in_time'):
            global_data.game_mgr.enable_low_script_update(game3d.get_frame_rate() > 90)