# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/map/map_widget/Map3DTouchLayerWidget.py
from __future__ import absolute_import
import cc
from logic.gcommon.common_const.battle_const import MARK_NORMAL
from common.utils.cocos_utils import cocos_pos_to_neox, neox_pos_to_cocos
from logic.gcommon.common_utils.parachute_utils import STAGE_LAUNCH_PREPARE
from common.utils.cocos_utils import ccp
import logic.gutils.map_3d_utils as mutil
from common.utils.ui_utils import get_scale
import math
import game3d
EPS_X = 0.0001
TAN_V = math.tan(52.5 / 180 * math.pi)

class Map3DTouchLayerWidget(object):

    def __init__(self, panel):
        super(Map3DTouchLayerWidget, self).__init__()
        self.map_panel = panel
        self.last_touch_location = None
        self.init_touch_layer_event()
        return

    def destroy(self):
        self.map_panel = None
        return

    def on_layer_touch_begin(self, layer, touch):
        pos = touch.getLocation()
        move_rocker_ui = global_data.ui_mgr.get_ui('MoveRockerUI')
        if move_rocker_ui:
            check_nd = move_rocker_ui.panel.rocker_touch if move_rocker_ui.panel.rocker_touch.isVisible() else move_rocker_ui.rocker_base_layer
            if check_nd.IsPointIn(pos):
                return False
        self.last_touch_location = pos
        return True

    def on_layer_touch_drag(self, layer, touch):
        cur_location = touch.getLocation()
        last_touch_location = cc.Vec2(cur_location)
        cur_location.subtract(self.last_touch_location)
        self.last_touch_location = last_touch_location
        cur_location.x = EPS_X if cur_location.x == 0 else cur_location.x
        if cur_location.getLength() >= 1:
            global_data.emgr.rotate_stage_plane_camera.emit(cur_location)

    def init_touch_layer_event(self):
        touch_layer = self.map_panel.nd_touch
        touch_layer.EnableDoubleClick(False)
        touch_layer.set_sound_enable(False)
        touch_layer.BindMethod('OnBegin', self.on_layer_touch_begin)
        touch_layer.BindMethod('OnDrag', self.on_layer_touch_drag)