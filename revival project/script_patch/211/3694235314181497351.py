# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/parts/PartLobbyEyeAdapt.py
from __future__ import absolute_import
from . import ScenePart
import math3d
import game3d
import world
import math
REGION_NAMES = {'box_zsy01_01': 1.1,
   'box_zsy01_02': 1.1,
   'box_zsy01_03': 1.1,
   'box_zsy02_01': 1.1,
   'box_zsy02_02': 1.1,
   'box_zsy02_03': 1.1
   }
DEFAULT_FACTOR = 0.9

class PartLobbyEyeAdapt(ScenePart.ScenePart):

    def __init__(self, scene, name):
        super(PartLobbyEyeAdapt, self).__init__(scene, name, need_update=True)
        self._last_adapt_factor = DEFAULT_FACTOR
        self._cur_adapt_factor = DEFAULT_FACTOR
        self._target_factor = DEFAULT_FACTOR

    def init_events(self):
        pass

    def on_enter(self):
        pass

    def on_exit(self):
        pass

    def on_update(self, dt):
        player = global_data.lobby_player
        if not player:
            return False
        scn = global_data.game_mgr.scene
        if not scn:
            return
        pos = player.ev_g_model_position()
        if not pos:
            return
        count = 0
        sum_adapt_factor = 0
        self._target_factor = DEFAULT_FACTOR
        for rname in REGION_NAMES:
            flag = self.check_in_region(rname, pos)
            if flag:
                sum_adapt_factor += REGION_NAMES[rname]
                count += 1

        if count:
            self._target_factor = float(sum_adapt_factor) / count
        self._cur_adapt_factor = (self._target_factor - self._cur_adapt_factor) / 30.0 + self._cur_adapt_factor
        scn.set_adapt_factor(self._cur_adapt_factor)

    def check_in_region(self, rname, pos):
        scn = global_data.game_mgr.scene
        m = scn.get_model(rname)
        if m and m.valid:
            transform_mat = m.world_transformation
            transform_mat.inverse()
            lpos = pos * transform_mat
            if lpos.x >= -1 and lpos.x <= 1 and lpos.y >= -1 and lpos.y <= 1 and lpos.z >= -1 and lpos.z <= 1:
                return True
        else:
            return False