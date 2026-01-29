# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/parts/PartTestMecha.py
from __future__ import absolute_import
from . import PartTestBase
import math3d
import world
import game3d
import time

class PartTestMecha(PartTestBase.PartTestBase):

    def __init__(self, scene, name):
        super(PartTestMecha, self).__init__(scene, name)
        global_data.enable_save_energy_mode = False

    def test_model(self):
        scene = self.scene()
        scene.load_env('default_nx2_mobile2.xml')
        scene.background_color = 2434092
        mecha = world.model('model_new\\mecha\\8004\\8004\\l1.gim', scene)
        mecha.position = math3d.vector(0, -20, 50)
        mecha.scale = math3d.vector(0.5, 0.5, 0.5)
        mecha.render_level = -1
        mecha = world.model('model_new\\mecha\\8002\\8002\\l1.gim', scene)
        mecha.position = math3d.vector(25, -20, 50)
        mecha.scale = math3d.vector(0.5, 0.5, 0.5)
        mecha.render_level = -1
        mecha = world.model('model_new\\mecha\\8008\\8008\\l1.gim', scene)
        mecha.position = math3d.vector(-25, -20, 50)
        mecha.scale = math3d.vector(0.5, 0.5, 0.5)
        mecha.render_level = -1
        mecha = world.model('model_new\\mecha\\8004\\8004\\l1.gim', scene)
        mecha.position = math3d.vector(0, -35, 100)
        mecha.scale = math3d.vector(0.5, 0.5, 0.5)
        mecha.render_level = -1
        mecha = world.model('model_new\\mecha\\8002\\8002\\l1.gim', scene)
        mecha.position = math3d.vector(25, -35, 100)
        mecha.scale = math3d.vector(0.5, 0.5, 0.5)
        mecha.render_level = -1
        mecha = world.model('model_new\\mecha\\8008\\8008\\l1.gim', scene)
        mecha.position = math3d.vector(-25, -35, 100)
        mecha.scale = math3d.vector(0.5, 0.5, 0.5)
        mecha.render_level = -1
        self.target_fps = 10

        def check_set_resolution():
            if game3d.get_frame_rate() != self.target_fps:
                game3d.set_frame_rate(self.target_fps)

        global_data.game_mgr.get_logic_timer().register(func=check_set_resolution, interval=10, times=-1)

    def on_enter(self):
        self.test_model()

    def on_exit(self):
        pass

    def set_quality(self, value):
        self.scene().set_macros({'IS_IN_BATTLE': '1'})
        if value == 3:
            self.scene().set_macros({'ENABLE_FAST_MODE': '0'})
        else:
            self.scene().set_macros({'ENABLE_FAST_MODE': '1'})
        global_data.gsetting.set_quality(value)
        self.scene().enable_hdr(False)

    def set_fps(self, value):
        self.target_fps = value