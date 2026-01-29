# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/map/map_widget/MapGravityRegionWidget.py
from __future__ import absolute_import
from logic.gutils import gravity_mode_utils
from logic.gcommon.const import NEOX_UNIT_SCALE
from logic.comsys.map.map_widget import MapScaleInterface
CIRCLE_PIC = [
 'gui/ui_res_2/battle/map/img_circle_blue.png', 'gui/ui_res_2/battle/map/img_circle_red.png']
CIRCLE_VX_PIC = ['gui/ui_res_2/battle/map/img_scan_blue.png', 'gui/ui_res_2/battle/map/img_scan_red.png']

class RegionMapMark(MapScaleInterface.MapScaleInterface):

    def __init__(self, parent_nd, ctrl_widget, type):
        super(RegionMapMark, self).__init__(parent_nd, ctrl_widget)
        self._nd = global_data.uisystem.load_template_create('map/i_map_moon_circle')
        self._nd.PlayAnimation('show')
        self._nd.img_circle.setVisible(False)
        self.parent_nd.AddChild('gravity_region', self._nd, Z=2)
        self.map_panel = ctrl_widget
        self.gravity_type = type
        index = 0 if gravity_mode_utils.is_less_gravity(type) else 1
        self._nd.img_circle.SetDisplayFrameByPath('', CIRCLE_PIC[index])
        self._nd.vx_img_circle.SetDisplayFrameByPath('', CIRCLE_VX_PIC[index])
        self._nd.img_circle.setVisible(False)

    def init_region_circle(self, w_pos, w_r):
        size = self.map_panel.get_world_distance_in_map(w_r * 2 / NEOX_UNIT_SCALE)
        w, _ = self._nd.img_circle.GetContentSize()
        self._nd.img_circle.setScale(size / w)
        self.set_world_position_ex(w_pos)
        self._nd.img_circle.setVisible(True)

    def on_map_scale(self, map_scale):
        pass


class MapGravityRegionWidget(object):

    def __init__(self, panel, parent_nd):
        self.map_panel = panel
        self.parent_nd = parent_nd
        self.less_gravity_region_nd = []
        self.over_gravity_region_nd = []
        self.aero_less_gravity_region_nd = []
        self.process_event(True)
        self.init_region_circle(gravity_mode_utils.LESS_GRAVITY)
        self.init_region_circle(gravity_mode_utils.OVER_GRAVITY)
        self.init_region_circle(gravity_mode_utils.AERO_LESS_GRAVITY)

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'init_gravity_region': self.init_region_circle,
           'remove_gravity_region': self.remove_region_circle
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def init_region_circle(self, type):
        self.remove_region_circle(type)
        if global_data.gravity_sur_battle_mgr:
            params = global_data.gravity_sur_battle_mgr.get_region_param(type) if 1 else None
            return params or None
        else:
            for index, info in enumerate(params):
                w_pos, w_r, level = info
                if type == gravity_mode_utils.LESS_GRAVITY:
                    nd = RegionMapMark(self.parent_nd, self.map_panel, gravity_mode_utils.LESS_GRAVITY)
                    self.less_gravity_region_nd.append(nd)
                    nd.init_region_circle(w_pos, w_r)
                if type == gravity_mode_utils.OVER_GRAVITY:
                    nd = RegionMapMark(self.parent_nd, self.map_panel, gravity_mode_utils.OVER_GRAVITY)
                    self.over_gravity_region_nd.append(nd)
                    nd.init_region_circle(w_pos, w_r)
                if type == gravity_mode_utils.AERO_LESS_GRAVITY:
                    nd = RegionMapMark(self.parent_nd, self.map_panel, gravity_mode_utils.AERO_LESS_GRAVITY)
                    self.aero_less_gravity_region_nd.append(nd)
                    nd.init_region_circle(w_pos, w_r)

            return

    def remove_region_circle(self, type=None):
        if type == gravity_mode_utils.LESS_GRAVITY or type is None:
            for nd in self.less_gravity_region_nd:
                nd.destroy()

            self.less_gravity_region_nd = []
        if type == gravity_mode_utils.OVER_GRAVITY or type is None:
            for nd in self.over_gravity_region_nd:
                nd.destroy()

            self.over_gravity_region_nd = []
        if type == gravity_mode_utils.AERO_LESS_GRAVITY or type is None:
            for nd in self.aero_less_gravity_region_nd:
                nd.destroy()

            self.aero_less_gravity_region_nd = []
        return

    def destroy(self):
        self.process_event(False)
        self.remove_region_circle()