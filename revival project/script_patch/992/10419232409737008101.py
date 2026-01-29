# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/map/map_widget/MapFFAInfoWidget.py
from __future__ import absolute_import
import six
from logic.comsys.map.map_widget import MapScaleInterface
from mobile.common.EntityManager import EntityManager
from common.utils.cocos_utils import ccp
from logic.gcommon.const import NEOX_UNIT_SCALE
import math
import math3d
CROWN_ICON = 'gui/ui_res_2/battle/ffa/icon_ffa_ace.png'
ENEMY_HIT_ICON = 'gui/ui_res_2/battle/map/icon_enemy.png'

class EntityMapMark(MapScaleInterface.MapScaleInterface):
    HIDE_TAG = 10001

    def __init__(self, parent_nd, ctrl_widget, scale=1):
        super(EntityMapMark, self).__init__(parent_nd)
        self._nd = global_data.uisystem.load_template_create('map/i_map_loacte_koth')
        self.parent_nd.AddChild('', self._nd, Z=2)
        self._nd.setScale(scale / ctrl_widget.cur_map_scale)
        self.set_show(False)

    def set_display_frame_by_path(self, path):
        self._nd.icon_koth_locate.SetDisplayFrameByPath('', path)

    def on_update(self, position):
        x, z = position
        tuple_pos = (x, 0, z)
        self.set_world_position_ex(tuple_pos)
        if not self._nd.isVisible():
            self.set_show(True)

    def set_show(self, show):
        self._nd.setVisible(show)

    def show_with_time(self, time):
        self.set_show(True)
        self._nd.stopActionByTag(self.HIDE_TAG)
        self._nd.DelayCallWithTag(time, self.set_show, self.HIDE_TAG, False)


class MapFFAInfoWidget(object):
    HIDE_TAG = 10001

    def __init__(self, panel, parent_nd):
        self.map_panel = panel
        self.parent_nd = parent_nd
        self.top_entity_widgets = []
        self.enemy_entity_widgets = {}
        self.top_player = {}
        self.process_event(True)

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'update_top_group_info': self.update_top_group_info,
           'campmate_make_damage_event': self.show_hit_map_mark
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def destroy(self):
        self.process_event(False)
        for widget in six.itervalues(self.enemy_entity_widgets):
            widget.destroy()

        self.enemy_entity_widgets = {}
        self.top_player = {}
        for widget in self.top_entity_widgets:
            widget.destroy()

        self.top_entity_widgets = []

    def update_top_group_info(self, group_id, soul_data):
        self.top_player = soul_data
        new_top_entity_widgets = []
        for widget in self.top_entity_widgets:
            widget.set_show(False)

        for entity_id, pos in six.iteritems(soul_data):
            if global_data.cam_lplayer and global_data.cam_lplayer.ev_g_is_campmate_by_eid(entity_id):
                if self.top_entity_widgets:
                    widget = self.top_entity_widgets.pop(0)
                    new_top_entity_widgets.append(widget)
                continue
            if not self.top_entity_widgets:
                widget = EntityMapMark(self.parent_nd, self.map_panel)
            else:
                widget = self.top_entity_widgets.pop(0)
                widget.set_show(True)
            widget.set_display_frame_by_path(CROWN_ICON)
            widget.on_update(pos)
            new_top_entity_widgets.append(widget)

        self.top_entity_widgets = new_top_entity_widgets

    def show_hit_map_mark(self, entity_logic):
        if not entity_logic:
            return
        entity_id = entity_logic.unit_obj.id
        if entity_logic.ev_g_is_in_mecha():
            entity_id = entity_logic.sd.ref_driver_id
        if entity_id in self.top_player:
            return
        if entity_id not in self.enemy_entity_widgets:
            widget = EntityMapMark(self.parent_nd, self.map_panel)
            widget.set_display_frame_by_path(ENEMY_HIT_ICON)
            self.enemy_entity_widgets[entity_id] = widget
        pos = entity_logic.ev_g_position()
        if pos:
            self.enemy_entity_widgets[entity_id].on_update((pos.x, pos.z))
            self.enemy_entity_widgets[entity_id].show_with_time(3)