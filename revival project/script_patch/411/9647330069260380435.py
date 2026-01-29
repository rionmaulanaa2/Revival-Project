# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/map/map_widget/MapBeaconTowerMarkWidget.py
from __future__ import absolute_import
import six
from logic.comsys.map.map_widget import MapScaleInterface
import logic.gcommon.common_const.battle_const as bconst
from logic.gcommon.common_utils.math3d_utils import tp_to_v3d
BEACON_MARK_OCCUPY_PIC = [
 'gui/ui_res_2/battle/map/icon_tower.png',
 'gui/ui_res_2/battle/map/icon_tower.png',
 'gui/ui_res_2/battle/map/icon_tower.png']
BEACON_MARK_NEUTRAL_PIC = 'gui/ui_res_2/battle/map/icon_tower2.png'

class BeaconTowerMark(MapScaleInterface.MapScaleInterface):

    def __init__(self, parent_nd, panel, world_pos):
        super(BeaconTowerMark, self).__init__(parent_nd, panel)
        self._nd = global_data.uisystem.load_template_create('map/i_map_tower')
        map_pos = self.trans_world_position(world_pos)
        self.set_position(map_pos)
        self.parent_nd.AddChild('', self._nd)
        self._nd.setScale(1.0 / panel.cur_map_scale)

    def on_update(self, state, faction_id):
        if state == bconst.BEACON_NEUTRAL:
            self._nd.sp_circle.SetDisplayFrameByPath('', BEACON_MARK_NEUTRAL_PIC)
            self._nd.StopAnimation('active')
        elif state == bconst.BEACON_OCCUPIED and faction_id is not None:
            side = global_data.king_battle_data.get_side_by_faction_id(faction_id)
            if 0 <= side <= 2:
                self._nd.sp_circle.SetDisplayFrameByPath('', BEACON_MARK_OCCUPY_PIC[side])
                self._nd.PlayAnimation('active')
        return


class MapBeaconTowerMarkWidget(object):

    def __init__(self, panel, parent_nd, view=None):
        super(MapBeaconTowerMarkWidget, self).__init__()
        self.map_panel = panel
        self.parent_nd = parent_nd
        self.beacon_tower_marks = {}
        self.process_event(True)
        self.init_widgets()

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'update_beacon_tower_mark_event': self._update_nd_info
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def init_widgets(self):
        for entity_id, beacon_tower_info in six.iteritems(global_data.king_battle_data.beacon_tower_dict):
            self._update_nd_info(entity_id, beacon_tower_info)

    def _add_beacon_tower_mark(self, beacon_tower_id, pos):
        if beacon_tower_id is None or pos is None:
            return
        else:
            mark = BeaconTowerMark(self.parent_nd, self.map_panel, pos)
            self.beacon_tower_marks[beacon_tower_id] = mark
            return mark

    def _update_nd_info(self, beacon_tower_id, beacon_tower_info):
        return
        pos = tp_to_v3d(beacon_tower_info.get('point'))
        state = beacon_tower_info.get('state')
        faction_id = beacon_tower_info.get('faction_id')
        mark = self.beacon_tower_marks.get(beacon_tower_id, None)
        if not mark:
            mark = self._add_beacon_tower_mark(beacon_tower_id, pos)
        mark.on_update(state, faction_id)
        return

    def destroy(self):
        self.beacon_tower_marks.clear()