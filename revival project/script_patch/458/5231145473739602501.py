# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/scene_background/GetWeaponDisplayBG.py
from __future__ import absolute_import
from .BackgroundUI import BackgroundUI

class GetWeaponDisplayBG(BackgroundUI):
    PANEL_CONFIG_NAME = 'common/get_item/get_weapon_bg'

    def on_init_panel(self):
        self.panel.RecordAnimationNodeState('show_s')
        self.panel.RecordAnimationNodeState('show_a')
        self.panel.RecordAnimationNodeState('show_b')
        self.panel.RecordAnimationNodeState('loop_s')
        self.panel.RecordAnimationNodeState('loop_a')
        self.panel.RecordAnimationNodeState('loop_b')
        self.show_anim = None
        self.loop_anim = None
        return

    def on_finalize_panel(self):
        pass

    def play_anim(self, show_anim, loop_anim):
        if self.show_anim:
            self.panel.RecoverAnimationNodeState(self.show_anim)
        if self.loop_anim:
            self.panel.StopAnimation(self.loop_anim)
            self.panel.RecoverAnimationNodeState(self.loop_anim)
        self.panel.PlayAnimation(show_anim, force_resume=True)
        self.panel.PlayAnimation(loop_anim, force_resume=True)
        self.show_anim = show_anim
        self.loop_anim = loop_anim

    def start_render(self):
        global_data.scene_background.start_render(-1)

    def stop_render(self):
        global_data.scene_background.stop_render()