# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/map/map_widget/MapGooseBearMapWidget.py
from __future__ import absolute_import
from six.moves import range
from logic.comsys.map.map_widget import MapScaleInterface
from common.utils.cocos_utils import ccp

class MapPartMark(MapScaleInterface.MapScaleInterface):

    def __init__(self, parent_nd, ctrl_widget):
        super(MapPartMark, self).__init__(parent_nd)
        self.map_panel = ctrl_widget
        self._nd = global_data.uisystem.load_template_create('battle_happy_push/i_battle_happy_push_map')
        self.parent_nd.AddChild('', self._nd)
        m_w, _ = self.map_panel.map_img.map_content_size
        d_w, _ = self._nd.GetContentSize()
        self._nd.setScale(1.0 * m_w / d_w)
        pos_3 = self.trans_world_position_ex((0, 0, 0))
        pos_2 = ccp(pos_3.x, pos_3.y)
        self.set_position(pos_2)

    def on_update(self):
        bat = global_data.battle
        if bat:
            for i in range(4):
                i += 1
                nd = getattr(self._nd, 'map_%d' % i)
                nd.setVisible(i not in bat.collapse_region)
                if bat.collapse_timestamp_info:
                    will_collapse_region, _ = bat.collapse_timestamp_info
                    if will_collapse_region not in bat.collapse_region and i == will_collapse_region:
                        nd.SetDisplayFrameByPath('', 'gui/ui_res_2/battle_happy_push/img_happy_push_map_red.png')
                else:
                    nd.SetDisplayFrameByPath('', 'gui/ui_res_2/battle_happy_push/img_happy_push_map_blue.png')


class MapGooseBearMapWidget:

    def __init__(self, panel, parent_nd):
        self.map_panel = panel
        self.parent_nd = parent_nd
        self.map_widget = None
        self.process_event(True)
        self.update_nd()
        return

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'goosebear_warn_collapse_event': self.update_nd,
           'goosebear_do_collapse_event': self.update_nd,
           'scene_observed_player_setted_event': self._on_scene_observed_player_setted
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def destroy(self):
        self.process_event(False)
        if self.map_widget:
            self.map_widget.destroy()
        self.map_widget = None
        return

    def update_nd(self):
        if not self.map_widget:
            self.map_widget = MapPartMark(self.parent_nd, self.map_panel)
        self.map_widget.on_update()

    def _on_scene_observed_player_setted(self, lplayer):
        self.update_nd()