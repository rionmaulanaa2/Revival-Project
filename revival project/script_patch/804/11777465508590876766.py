# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComDeathDoorBloodSimUI.py
from __future__ import absolute_import
from .ComBloodSimUI import ComBloodSimUI
import math3d

class ComDeathDoorBloodSimUI(ComBloodSimUI):

    def init_from_dict(self, unit_obj, bdict):
        self.npc_id = bdict.get('npc_id')
        super(ComDeathDoorBloodSimUI, self).init_from_dict(unit_obj, bdict)
        door_cfg_data = global_data.game_mode.get_cfg_data('door_data')
        self.blood_height = door_cfg_data.get(str(self.npc_id), {}).get('blood_height')

    def get_simui_pos(self):
        return math3d.vector(0, self.blood_height, 0) * self.ev_g_door_rot_mat()