# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/map/map_widget/MapDeathInfoWidget.py
from __future__ import absolute_import
import six
import six_ex
from logic.comsys.map.map_widget import MapScaleInterface
from logic.client.const import game_mode_const
from common.utils.cocos_utils import ccp
from common.utils.timer import CLOCK
from logic.gcommon.const import NEOX_UNIT_SCALE
import math
BTN_FRAMES = [
 'gui/ui_res_2/battle/occupy_mode/occupied_icon_activation_blue.png',
 'gui/ui_res_2/battle/occupy_mode/occupied_icon_activation_red.png']

class BornMapMark(MapScaleInterface.MapScaleInterface):

    def __init__(self, parent_nd, ctrl_widget, id):
        super(BornMapMark, self).__init__(parent_nd)
        self.id = id
        self.map_panel = ctrl_widget
        self._nd = global_data.uisystem.load_template_create('battle_occupy/i_map_basement_spot')
        self.parent_nd.AddChild('', self._nd)
        self.sp_dir = ccp(0, 1)

    def on_update(self, pos, side, scale=1.0):
        x, y, z = pos
        self._nd.img_spot.setScale(scale)
        pos_3 = self.trans_world_position_ex((x, 0, z))
        pos_2 = ccp(pos_3.x, pos_3.y)
        self.set_position(pos_2)
        self._nd.img_spot.SetDisplayFrameByPath('', BTN_FRAMES[side])


class MapDeathInfoWidget:

    def __init__(self, panel, parent_nd):
        self.map_panel = panel
        self.parent_nd = parent_nd
        self.born_widgets = {}
        self.process_event(True)
        self.update_nd()

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'update_death_born_point': self.update_nd,
           'scene_observed_player_setted_event': self._on_scene_observed_player_setted
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def destroy(self):
        self.process_event(False)
        for key in six_ex.keys(self.born_widgets):
            self.born_widgets[key].destroy()

        self.born_widgets = {}

    def update_nd(self):
        if not global_data.death_battle_data:
            return
        born_dict = global_data.death_battle_data.born_data
        self._update(self.born_widgets, born_dict, BornMapMark)

    def _update(self, widgets, data_dict, mark_cls):
        ids = six_ex.keys(data_dict)
        del_parts = set(six_ex.keys(widgets)) - set(ids)
        for id in del_parts:
            if id in widgets:
                widgets[id].destroy()
                del widgets[id]

        born_cfg_data = global_data.game_mode.get_born_data()
        if global_data.death_battle_data.area_id is not None:
            born_info = born_cfg_data[global_data.death_battle_data.area_id]
            other_born_data = born_info.get('other_born_data')
            born_icon_scale = born_info.get('born_icon_scale', [1, 0.3])
            for id, data_obj in six.iteritems(data_dict):
                side = self._get_side(data_obj)
                _x, _y, _z, _r, _idx, _ = data_obj.data
                if id not in widgets:
                    widgets[id] = mark_cls(self.parent_nd, self.map_panel, id)
                widgets[id].on_update((_x, _y, _z), side, scale=born_icon_scale[0])
                if other_born_data:
                    other_born_id = ''.join([str(id), '-', str(_idx)])
                    x, y, z, range = other_born_data[_idx]
                    if other_born_id not in widgets:
                        widgets[other_born_id] = mark_cls(self.parent_nd, self.map_panel, other_born_id)
                    widgets[other_born_id].on_update((x, y, z), side, scale=born_icon_scale[1])

        return

    def _get_side(self, born_data):
        from logic.gutils import yet_another_observe_utils
        ob_unit = yet_another_observe_utils.get_ob_target_unit()
        if ob_unit:
            group_id = ob_unit.ev_g_group_id()
            return born_data.get_side(group_id)
        else:
            return born_data.side

    def _on_scene_observed_player_setted(self, lplayer):
        self.update_nd()