# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/map/map_widget/MapGulagAreaWidget.py
from __future__ import absolute_import
import six
from logic.gcommon.const import NEOX_UNIT_SCALE
from logic.comsys.map.map_widget import MapScaleInterface
from common.cfg import confmgr
from common.utils.cocos_utils import ccp

class GulagAreaMapMark(MapScaleInterface.MapScaleInterface):

    def __init__(self, parent_nd, ctrl_widget):
        super(GulagAreaMapMark, self).__init__(parent_nd, ctrl_widget)
        self._nd = global_data.uisystem.load_template_create('map/i_map_gulag_area')
        self.parent_nd.AddChild('gulag_area', self._nd, Z=2)
        self.map_panel = ctrl_widget
        self.is_small_map = 'SmallMap' in ctrl_widget.__class__.__name__
        self._nd.lab_title.setVisible(not self.is_small_map)

    def init_area(self, min_x, min_z, max_x, max_z):
        self.set_position(ccp(1722, 1820))
        self._nd.img_mark.lab_title.ReConfPosition()

    def on_map_scale(self, map_scale):
        if self.is_small_map:
            return
        self._nd.lab_title.setScale(1.0 / map_scale)


class MapGulagAreaWidget(object):

    def __init__(self, panel, parent_nd):
        self.map_panel = panel
        self.parent_nd = parent_nd
        self.gulag_area_nd_dict = {}
        self.init_nd()

    def init_nd(self):
        revive_game_area_info = confmgr.get('game_mode/gulag/play_data', 'revive_game_area')
        for area_id, area_info in six.iteritems(revive_game_area_info):
            self.gulag_area_nd_dict[area_id] = GulagAreaMapMark(self.parent_nd, self.map_panel)
            min_x, min_z, max_x, max_z, _ = area_info['area']
            self.gulag_area_nd_dict[area_id].init_area(min_x, min_z, max_x, max_z)

    def destroy(self):
        for area_id, area_nd in six.iteritems(self.gulag_area_nd_dict):
            area_nd.destroy()

        self.gulag_area_nd_dict = {}