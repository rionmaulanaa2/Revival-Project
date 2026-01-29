# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/parts/PartAntiTonemapping.py
from __future__ import absolute_import
from . import ScenePart
import math3d
import game3d
import world
import math

class PartAntiTonemapping(ScenePart.ScenePart):

    def __init__(self, scene, name):
        super(PartAntiTonemapping, self).__init__(scene, name)

    def init_events(self):
        pass

    def on_enter(self):
        bg_model = self.get_scene().get_model('anti_tonemapping_bg')
        if bg_model:
            bg_model.set_rendergroup_and_priority(world.RENDER_GROUP_SKY, 1)
            bg_model.visible = False

    def on_exit(self):
        pass