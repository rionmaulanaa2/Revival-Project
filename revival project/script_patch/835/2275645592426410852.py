# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/com_bunker/ComBunkSidewaysAppearance.py
from __future__ import absolute_import
import math3d
from logic.client.const.camera_const import POSTURE_RIGHT_SIDEWAYS, POSTURE_LEFT_SIDEWAYS, POSTURE_UP_SIDEWAYS
from logic.gcommon.component.UnitCom import UnitCom
from logic.gcommon.const import NEOX_UNIT_SCALE
SW_RIGHT = POSTURE_RIGHT_SIDEWAYS
SW_LEFT = POSTURE_LEFT_SIDEWAYS
SW_UP = POSTURE_UP_SIDEWAYS
HOZ_VECTOR = math3d.vector(1, 0, 1)
FORWARD_DIR = math3d.vector(0, 0, 1)
BUNKER_MIN_WIDTH = 0.6 * NEOX_UNIT_SCALE

class ComBunkerSidewaysAppearance(UnitCom):
    BIND_EVENT = {'E_TRY_RIGHT_SIDEWAYS': 'enter_right_sideways_pos',
       'E_TRY_LEFT_SIDEWAYS': 'enter_left_sideways_pos',
       'E_TRY_UP_SIDEWAYS': 'enter_up_sideways_pos'
       }

    def __init__(self):
        super(ComBunkerSidewaysAppearance, self).__init__()

    def init_from_dict(self, unit_obj, bdict):
        super(ComBunkerSidewaysAppearance, self).init_from_dict(unit_obj, bdict)

    def destroy(self):
        super(ComBunkerSidewaysAppearance, self).destroy()

    def enter_right_sideways_pos(self):
        pass

    def enter_left_sideways_pos(self):
        pass

    def enter_up_sideways_pos(self):
        pass