# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/map/map_widget/MapMagicRegionWidget.py
from __future__ import absolute_import
import six
from logic.gcommon.const import NEOX_UNIT_SCALE
from logic.comsys.map.map_widget import MapScaleInterface
CIRCLE_PIC = [
 'gui/ui_res_2/battle/map/img_circle_blue.png', 'gui/ui_res_2/battle/map/img_circle_red.png']
CIRCLE_VX_PIC = ['gui/ui_res_2/battle/map/img_scan_blue.png', 'gui/ui_res_2/battle/map/img_scan_red.png']

class RegionMapMark(MapScaleInterface.MapScaleInterface):

    def __init__(self, parent_nd, ctrl_widget, region_id):
        super(RegionMapMark, self).__init__(parent_nd, ctrl_widget)
        self._nd = global_data.uisystem.load_template_create('map//i_map_hunter_circle')
        self._nd.PlayAnimation('show')
        self._nd.img_circle.setVisible(False)
        self.parent_nd.AddChild('magic_region', self._nd, Z=2)
        self.map_panel = ctrl_widget
        self.region_id = region_id
        self.refresh_region_circle()

    def init_region_circle(self, w_pos, w_r):
        size = self.map_panel.get_world_distance_in_map(w_r * 2 / NEOX_UNIT_SCALE)
        w, _ = self._nd.img_circle.GetContentSize()
        self._nd.img_circle.setScale(size / w)
        self.set_world_position_ex(w_pos)
        self._nd.img_circle.setVisible(True)

    def remove_region_circle(self):
        self._nd.img_circle.setVisible(False)

    def refresh_region_circle(self):
        params = global_data.magic_sur_battle_mgr.get_region_param(self.region_id)
        if params:
            w_pos, w_r, data = params
            if w_pos and w_r:
                self.init_region_circle(w_pos, w_r)
        else:
            self._nd.img_circle.setVisible(False)

    def on_map_scale(self, map_scale):
        pass


class MapMagicRegionWidget(object):

    def __init__(self, panel, parent_nd):
        self.map_panel = panel
        self.parent_nd = parent_nd
        self.magic_region_nd_dict = {}
        self.region_pools = []
        self.init_nd()
        self.process_event(True)

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'init_magic_region': self.init_region_circle,
           'remove_magic_region': self.remove_region_circle
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def init_nd(self):
        all_region_ids = global_data.magic_sur_battle_mgr.get_all_region_ids()
        for r_id in all_region_ids:
            self.init_region_circle(r_id)

    def init_region_circle(self, region_id):
        params = global_data.magic_sur_battle_mgr.get_region_param(region_id)
        if not params:
            return
        w_pos, w_r, data = params
        if region_id not in self.magic_region_nd_dict:
            self.magic_region_nd_dict[region_id] = RegionMapMark(self.parent_nd, self.map_panel, region_id)
            self.magic_region_nd_dict[region_id].init_region_circle(w_pos, w_r)

    def remove_region_circle(self, region_id):
        if region_id in self.magic_region_nd_dict:
            self.magic_region_nd_dict[region_id].remove_region_circle()
            self.magic_region_nd_dict[region_id].destroy()
            del self.magic_region_nd_dict[region_id]

    def destroy(self):
        self.process_event(False)
        for region_id, region_nd in six.iteritems(self.magic_region_nd_dict):
            region_nd.destroy()

        self.magic_region_nd_dict = {}