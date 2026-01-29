# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/map/map_widget/MapMoveRangeRectWidget.py
from __future__ import absolute_import
from logic.comsys.map.map_widget import MapScaleInterface
from mobile.common.EntityManager import EntityManager
from common.utils.cocos_utils import ccp
from common.utils.timer import CLOCK
from logic.gcommon.const import NEOX_UNIT_SCALE
from logic.gcommon.common_utils.local_text import get_text_by_id
import math
import math3d

class MoreRangeMapMark(MapScaleInterface.MapScaleInterface):

    def __init__(self, parent_nd, ctrl_widget):
        super(MoreRangeMapMark, self).__init__(parent_nd, ctrl_widget)
        self._nd = global_data.uisystem.load_template_create('map/i_map_basement_koth')
        self.parent_nd.AddChild('', self._nd, Z=2)
        self.map_panel = ctrl_widget
        self._nd.lab_koth.setVisible(False)
        self._nd.lab_basement.setVisible(False)
        self.init_range()

    def init_range(self):
        battle = global_data.battle
        if not battle:
            return
        born_data = global_data.game_mode.get_born_data()
        range_data = born_data[str(battle.area_id)].get('move_range')
        min_x = min(range_data[0][0], range_data[1][0])
        max_x = max(range_data[0][0], range_data[1][0])
        min_z = min(range_data[0][1], range_data[1][1])
        max_z = max(range_data[0][1], range_data[1][1])
        center_x = (min_x + max_x) * 0.5
        center_z = (min_z + max_z) * 0.5
        center = (center_x, 0.0, center_z)
        self.set_world_position_ex(center)
        self._nd.img_basement.SetDisplayFrameByPath('', 'gui/ui_res_2/battle/koth/img_basement_red.png')
        length = max_x - min_x
        width = max_z - min_z
        rel_length = self.map_panel.get_world_distance_in_map(length / NEOX_UNIT_SCALE)
        rel_width = self.map_panel.get_world_distance_in_map(width / NEOX_UNIT_SCALE)
        self._nd.img_basement.SetContentSize(rel_length, rel_width)

    def on_map_scale(self, map_scale):
        self._nd.lab_basement.setScale(1.0 / map_scale)


class MapMoveRangeRectWidget:

    def __init__(self, panel, parent_nd):
        self.map_panel = panel
        self.parent_nd = parent_nd
        self.move_range_widget = None
        self.process_event(True)
        self.init_widgets()
        return

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {}
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def destroy(self):
        self.process_event(False)
        self.move_range_widget and self.move_range_widget.destroy()
        self.move_range_widget = None
        return

    def init_widgets(self):
        self.move_range_widget = MoreRangeMapMark(self.parent_nd, self.map_panel)