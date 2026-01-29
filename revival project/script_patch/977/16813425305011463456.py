# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/parts/PartHDRAdaptManager.py
from __future__ import absolute_import
from . import ScenePart
import math3d
import weakref
import C_file
import struct
import math
import render
CHUNK_SIZE = 832
HALF_CHUNK_SIZE = CHUNK_SIZE / 2

class PartHDRAdaptManager(ScenePart.ScenePart):
    INIT_EVENT = {'scene_hdr_eye_adapt_enable': 'hdr_eye_adapt_enable',
       'on_player_parachute_stage_changed': 'player_parachute_stage_changed'
       }

    def __init__(self, scene, name):
        super(PartHDRAdaptManager, self).__init__(scene, name, True)
        self._is_eye_adapt_on = False
        self._is_use_realtime_light = False
        self._scene_prefix = 'scene/bw_all05/bw_all05_content/lumens'
        self._target_light = 100
        self._target_factor = 1.0
        self._last_factor = 1.0
        self._cur_factor = 1.0
        self.cam = None
        self._a1 = None
        self._b1 = None
        self._a2 = None
        self._b2 = None
        self._min_factor = None
        self._max_factor = None
        self._split_light = None
        self.all_load_chunk_lights = {}
        self.all_load_chunk_lights_padding = {}
        self.load_chunk_light_list = []
        return

    def on_enter(self):
        global_data.game_mgr.scene.set_eye_adapt_enable(False)
        global_data.game_mgr.scene.set_adapt_factor(1.0)

    def player_parachute_stage_changed(self, stage):
        pass

    def hdr_eye_adapt_enable(self):
        pass