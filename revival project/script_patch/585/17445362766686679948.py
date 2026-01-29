# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/map/MidMapUINew.py
from __future__ import absolute_import
from common.const.uiconst import NORMAL_LAYER_ZORDER
from logic.comsys.map.MapBaseUINew import MapBaseUI
MAP_VIEW_RANGE = 800

class MidMapUI(MapBaseUI):
    PANEL_CONFIG_NAME = 'map/map_mid'
    DLG_ZORDER = NORMAL_LAYER_ZORDER
    IS_PLAY_OPEN_SOUND = False
    UI_ACTION_EVENT = {'btn_map_mid.OnClick': 'on_close_btn'
       }

    def on_init_panel(self, *args, **kwargs):
        self.enable_common_marks_animation(True)
        super(MidMapUI, self).on_init_panel(*args, **kwargs)

    def init_parameters(self, **kwargs):
        dist = self.get_world_distance_in_map(MAP_VIEW_RANGE)
        self.view_dist = dist
        scale = self.calc_map_show_scale(dist, dist)
        kwargs['scale'] = scale
        super(MidMapUI, self).init_parameters(**kwargs)
        self.init_sub_component()
        self.init_map_offset = kwargs.get('center_pos')

    def on_init_complete(self):
        pass

    def init_sub_component(self):
        self.init_touch_layer_widget()

    def init_player_widget(self):
        super(MidMapUI, self).init_player_widget()
        self.player_info_widget.set_follow_player_enable(True)

    def init_touch_layer_widget(self):
        from logic.comsys.map.map_widget.MidMapTouchLayerWidget import MidMapTouchLayerWidget
        self.touch_layer_widget = MidMapTouchLayerWidget(self)

    def init_event(self):
        super(MidMapUI, self).init_event()
        if self.init_map_offset:
            self.panel.sv_map.SetContentOffset(self.init_map_offset)
        else:
            center_pos = self.map_nd.CalcPosition('50%', '50%')
            self.panel.sv_map.CenterWithPos(center_pos[0], center_pos[1])
        self.panel.sv_map.setSwallowTouches(True)
        global_data.emgr.on_mid_map_mark += self.on_mid_map_mark

    def on_mid_map_mark(self, mark_type):
        self.touch_layer_widget and self.touch_layer_widget.on_mid_map_mark(mark_type)

    def on_close_btn(self, *args):
        self.close()

    def on_finalize_panel(self):
        self.destroy_widget('touch_layer_widget')
        super(MidMapUI, self).on_finalize_panel()