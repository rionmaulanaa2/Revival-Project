# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/map/map_widget/MapKothPartInfoWidget.py
from __future__ import absolute_import
import six
from six.moves import range
from logic.comsys.map.map_widget import MapScaleInterface
from mobile.common.EntityManager import EntityManager
from common.utils.cocos_utils import ccp
from common.utils.timer import CLOCK
from logic.gcommon.const import NEOX_UNIT_SCALE
from logic.gcommon.common_utils.local_text import get_text_by_id
import math
CAMP_IMG = [
 'gui/ui_res_2/battle/koth/img_basement_blue.png',
 'gui/ui_res_2/battle/koth/img_basement_red.png',
 'gui/ui_res_2/battle/koth/img_basement_purple.png',
 'gui/ui_res_2/battle/koth/img_basement_white.png']
CAMP_COLOR = ['#DB', '#DR', '#DP', '#SW', '#SW', '#SW']
TOWER_IMG = ['gui/ui_res_2/battle/koth/icon_koth_blue.png',
 'gui/ui_res_2/battle/koth/icon_koth_red.png',
 'gui/ui_res_2/battle/koth/icon_koth_purple.png',
 'gui/ui_res_2/battle/koth/icon_koth_white.png']

class CampPartMapMark(MapScaleInterface.MapScaleInterface):

    def __init__(self, parent_nd, ctrl_widget):
        super(CampPartMapMark, self).__init__(parent_nd, ctrl_widget)
        self._nd = global_data.uisystem.load_template_create('map/i_map_basement_koth')
        self.parent_nd.AddChild('', self._nd, Z=2)
        self.map_panel = ctrl_widget
        self._nd.lab_koth.setVisible(False)
        self._nd.lab_basement.setVisible(True)

    def on_update(self, data):
        uid, poision, camp_data = data
        self.uid = uid
        self.set_world_position_ex(poision)
        self._nd.img_basement.SetDisplayFrameByPath('', CAMP_IMG[camp_data.side])
        cfg = global_data.game_mode.get_cfg_data('play_data')
        length = cfg.get('camp0%d_base_length' % camp_data.camp_id)
        width = cfg.get('camp0%d_base_width' % camp_data.camp_id)
        if length and width:
            rel_length = self.map_panel.get_world_distance_in_map(length / NEOX_UNIT_SCALE * 2)
            rel_width = self.map_panel.get_world_distance_in_map(width / NEOX_UNIT_SCALE * 2)
            self._nd.img_basement.SetContentSize(rel_length, rel_width)
        self._nd.lab_basement.SetColor(CAMP_COLOR[camp_data.side])
        self._nd.lab_basement.SetPosition('50%', '50%')
        self._nd.lab_basement.SetString(get_text_by_id(8040 + camp_data.side))

    def on_map_scale(self, map_scale):
        self._nd.lab_basement.setScale(1.0 / map_scale)


class MapRectMark(MapScaleInterface.MapScaleInterface):

    def __init__(self, parent_nd, ctrl_widget):
        super(MapRectMark, self).__init__(parent_nd)
        self._nd = global_data.uisystem.load_template_create('map/i_map_basement_koth')
        self.parent_nd.AddChild('', self._nd, Z=2)
        self.map_panel = ctrl_widget
        self._nd.lab_koth.setVisible(False)

    def set_size(self, poision, length, width):
        self.set_world_position_ex(poision)
        if length and width:
            rel_length = self.map_panel.get_world_distance_in_map(length / NEOX_UNIT_SCALE * 2)
            rel_width = self.map_panel.get_world_distance_in_map(width / NEOX_UNIT_SCALE * 2)
            self._nd.img_basement.SetContentSize(rel_length, rel_width)


class OccupyPartMapMark(MapScaleInterface.MapScaleInterface):

    def __init__(self, parent_nd, ctrl_widget):
        super(OccupyPartMapMark, self).__init__(parent_nd, ctrl_widget)
        self._nd = global_data.uisystem.load_template_create('map/i_map_basement_koth')
        self.parent_nd.AddChild('', self._nd, Z=2)
        self.map_panel = ctrl_widget

    def on_map_scale(self, map_scale):
        self._nd.lab_koth.setScale(1.0 / map_scale)

    def on_update(self, data):
        self.occupy_id, = data
        relative_fraction_id = global_data.king_battle_data.get_occupy_camp_side(self.occupy_id)
        occupy_cfg = global_data.game_mode.get_cfg_data('king_occupy_data')
        occupy_data = occupy_cfg.get(str(self.occupy_id), {})
        if not occupy_data:
            return
        poision = occupy_data.get('center')
        area = occupy_data.get('area')
        name = occupy_data.get('show_text_id')
        length = abs(area[1][0] - area[0][0])
        width = abs(area[1][1] - area[0][1])
        self.set_world_position_ex(poision)
        self._nd.img_basement.SetDisplayFrameByPath('', CAMP_IMG[relative_fraction_id])
        if length and width:
            rel_length = self.map_panel.get_world_distance_in_map(length / NEOX_UNIT_SCALE)
            rel_width = self.map_panel.get_world_distance_in_map(width / NEOX_UNIT_SCALE)
            self._nd.img_basement.SetContentSize(rel_length, rel_width)
        self._nd.lab_koth.SetString(get_text_by_id(name))
        if relative_fraction_id == -1:
            self._nd.lab_koth.SetColor('#SW')
        else:
            self._nd.lab_koth.SetColor(CAMP_COLOR[relative_fraction_id])
        self._nd.lab_koth.SetPosition('4', '100%')

    def on_change_side(self):
        relative_fraction_id = global_data.king_battle_data.get_occupy_camp_side(self.occupy_id)
        self._nd.img_basement.SetDisplayFrameByPath('', CAMP_IMG[relative_fraction_id])
        if relative_fraction_id == -1:
            self._nd.lab_koth.SetColor('#SW')
        else:
            self._nd.lab_koth.SetColor(CAMP_COLOR[relative_fraction_id])


class TowerPartMapMark(MapScaleInterface.MapScaleInterface):

    def __init__(self, parent_nd, ctrl_widget):
        super(TowerPartMapMark, self).__init__(parent_nd)
        self._nd = global_data.uisystem.load_template_create('map/ccb_enemy_locate')
        self.parent_nd.AddChild('', self._nd, Z=2)
        self.map_panel = ctrl_widget

    def on_update(self, data):
        self.occupy_id, = data
        self._nd.icon_enemy.SetDisplayFrameByPath('', TOWER_IMG[global_data.king_battle_data.get_occupy_camp_side(self.occupy_id)])
        occupy_cfg = global_data.game_mode.get_cfg_data('king_occupy_data')
        occupy_data = occupy_cfg.get(str(self.occupy_id), {})
        if not occupy_data:
            return
        poision = occupy_data.get('position')
        self.set_world_position_ex(poision)

    def on_change_side(self):
        self._nd.icon_enemy.SetDisplayFrameByPath('', TOWER_IMG[global_data.king_battle_data.get_occupy_camp_side(self.occupy_id)])


class MapKothPartInfoWidget:

    def __init__(self, panel, parent_nd):
        self.map_panel = panel
        self.parent_nd = parent_nd
        self.part_camp_widgets = {}
        self.neutral_shop_widgets = []
        self.occupy_widgets = {}
        self.occupy_tower_widgets = {}
        self.process_event(True)
        self.init_widgets()

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'update_camp_occupy_info': self.update_nd_info
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def destroy(self):
        self.process_event(False)
        for widget in six.itervalues(self.part_camp_widgets):
            widget.destroy()

        for widget in self.neutral_shop_widgets:
            widget.destroy()

        for widget in six.itervalues(self.occupy_widgets):
            widget.destroy()

        for widget in six.itervalues(self.occupy_tower_widgets):
            widget.destroy()

        self.neutral_shop_widgets = []
        self.part_camp_widgets = {}
        self.occupy_widgets = {}

    def init_widgets(self):
        cfg = global_data.game_mode.get_cfg_data('play_data')
        for camp_id, data in six.iteritems(global_data.king_battle_data.get_camp()):
            widget = CampPartMapMark(self.parent_nd, self.map_panel)
            self.part_camp_widgets[camp_id] = widget
            key = 'camp0%d_base_center' % camp_id
            pos = cfg.get(key)
            if pos:
                self.part_camp_widgets[camp_id].on_update((camp_id, pos, data))

        occupy_ids = cfg.get('king_point_list', [])
        for occupy_id in occupy_ids:
            widget = OccupyPartMapMark(self.parent_nd, self.map_panel)
            self.occupy_widgets[occupy_id] = widget
            self.occupy_widgets[occupy_id].on_update((occupy_id,))
            widget = TowerPartMapMark(self.parent_nd, self.map_panel)
            self.occupy_tower_widgets[occupy_id] = widget
            self.occupy_tower_widgets[occupy_id].on_update((occupy_id,))

    def init_shop_region(self):
        cfg = global_data.game_mode.get_cfg_data('play_data')
        SHOP_NUM = 3
        for i in range(SHOP_NUM):
            pos = cfg.get('neutral0%d_shop_center' % (i + 1))
            length = cfg.get('neutral0%d_shop_length' % (i + 1))
            width = cfg.get('neutral0%d_shop_width' % (i + 1))
            if pos:
                widget = MapRectMark(self.parent_nd, self.map_panel)
                widget.set_size(pos, length, width)
                self.neutral_shop_widgets.append(widget)

    def update_nd_info(self):
        for widget in six.itervalues(self.occupy_widgets):
            widget and widget.on_change_side()

        for widget in six.itervalues(self.occupy_tower_widgets):
            widget and widget.on_change_side()