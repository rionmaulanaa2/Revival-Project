# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/map/map_widget/MapOccupyInfoWidget.py
from __future__ import absolute_import
import six
import six_ex
from logic.comsys.map.map_widget import MapScaleInterface
from logic.client.const import game_mode_const
from common.utils.cocos_utils import ccp
from common.utils.timer import CLOCK
from logic.gcommon.const import NEOX_UNIT_SCALE
import math
BTN_FRAMES = {'icon': ['gui/ui_res_2/battle/map/icon_neutral.png',
          'gui/ui_res_2/battle/map/icon_defense.png',
          'gui/ui_res_2/battle/map/icon_attack.png',
          'gui/ui_res_2/battle/map/icon_lock.png',
          'gui/ui_res_2/battle/map/icon_seize.png']
   }

class PartMapMark(MapScaleInterface.MapScaleInterface):

    def __init__(self, parent_nd, ctrl_widget, id):
        super(PartMapMark, self).__init__(parent_nd)
        self.id = id
        self.map_panel = ctrl_widget
        self._nd = global_data.uisystem.load_template_create('map/i_map_contention_circle')
        self.parent_nd.AddChild('', self._nd)
        self.sp_dir = ccp(0, 1)

    def on_update(self, data_obj):
        pos = data_obj.data['position']
        range = data_obj.data['range']
        rel_size = self.map_panel.get_world_distance_in_map(range / NEOX_UNIT_SCALE * 2)
        w, _ = self._nd.img_circle.GetContentSize()
        self._nd.img_circle.setScale(rel_size / w)
        pos_3 = self.trans_world_position_ex(pos)
        pos_2 = ccp(pos_3.x, pos_3.y)
        self.set_position(pos_2)
        node = self._nd.icon_empty
        path = BTN_FRAMES['icon'][data_obj.control_side]
        if path:
            node.setVisible(True)
            node.SetDisplayFrameByPath('', path)
        else:
            node.setVisible(False)


class MapOccupyInfoWidget:

    def __init__(self, panel, parent_nd):
        self.map_panel = panel
        self.parent_nd = parent_nd
        self.part_widgets = {}
        self.process_event(True)
        self.update_nd()

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'update_control_point': self.update_nd
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def destroy(self):
        self.process_event(False)
        for key in six_ex.keys(self.part_widgets):
            self.part_widgets[key].destroy()

        self.part_widgets = {}

    def update_nd(self):
        if not global_data.death_battle_data:
            return
        part_dict = global_data.death_battle_data.part_data
        new_controls = set(six_ex.keys(part_dict))
        cur_controls = set(six_ex.keys(self.part_widgets))
        del_controls = cur_controls - new_controls
        for part_id in del_controls:
            widget = self.part_widgets[part_id]
            widget and widget.destroy()
            del self.part_widgets[part_id]

        self._update(self.part_widgets, part_dict, PartMapMark)

    def _update(self, widgets, data_dict, mark_cls):
        for id, data_obj in six.iteritems(data_dict):
            if id not in widgets:
                widgets[id] = mark_cls(self.parent_nd, self.map_panel, id)
            widgets[id].on_update(data_obj)