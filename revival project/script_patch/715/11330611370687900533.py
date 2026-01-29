# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/map/map_widget/MapGranbelmRegionWidget.py
from __future__ import absolute_import
from logic.comsys.map.map_widget import MapScaleInterface
from logic.gcommon.const import NEOX_UNIT_SCALE
from logic.comsys.map.map_widget import MapScaleInterface

class RegionMapMark(MapScaleInterface.MapScaleInterface):

    def __init__(self, parent_nd, ctrl_widget):
        super(RegionMapMark, self).__init__(parent_nd, ctrl_widget)
        self._nd = global_data.uisystem.load_template_create('map/i_map_moon_circle')
        self._nd.PlayAnimation('show')
        self._nd.img_circle.setVisible(False)
        self.parent_nd.AddChild('granbelm_rune_region', self._nd, Z=2)
        self.map_panel = ctrl_widget
        self.refresh_region_circle()

    def init_region_circle(self, w_pos, w_r, level):
        size = self.map_panel.get_world_distance_in_map(w_r * 2 / NEOX_UNIT_SCALE)
        w, _ = self._nd.img_circle.GetContentSize()
        self._nd.img_circle.setScale(size / w)
        self.set_world_position_ex(w_pos)
        self._nd.img_circle.setVisible(True)

    def remove_region_circle(self, level):
        self._nd.img_circle.setVisible(False)

    def refresh_region_circle(self):
        param_list = global_data.gran_sur_battle_mgr.get_region_param()
        if param_list:
            w_pos = param_list[0]
            w_r = param_list[1]
            level = param_list[2]
            if w_pos and w_r:
                self.init_region_circle(w_pos, w_r, level)
        else:
            self._nd.img_circle.setVisible(False)

    def on_map_scale(self, map_scale):
        pass


class MapGranbelmRegionWidget(object):

    def __init__(self, panel, parent_nd):
        self.map_panel = panel
        self.parent_nd = parent_nd
        self.region_nd = None
        self.init_nd()
        self.process_event(True)
        return

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'init_granbelm_rune_region': self.init_region_circle,
           'remove_granbelm_rune_region': self.remove_region_circle
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def init_nd(self):
        self.region_nd = RegionMapMark(self.parent_nd, self.map_panel)

    def init_region_circle(self, w_pos, w_r, level):
        if self.region_nd:
            self.region_nd.init_region_circle(w_pos, w_r, level)

    def remove_region_circle(self, level):
        if self.region_nd:
            self.region_nd.remove_region_circle(level)

    def destroy(self):
        self.process_event(False)
        self.region_nd and self.region_nd.destroy()
        self.region_nd = None
        return