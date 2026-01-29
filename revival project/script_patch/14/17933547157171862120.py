# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/map/map_widget/MapZombieFFAInfoWidget.py
from __future__ import absolute_import
import six
from logic.comsys.map.map_widget.MapFFAInfoWidget import EntityMapMark
from logic.comsys.map.map_widget.MapFFAInfoWidget import CROWN_ICON, ENEMY_HIT_ICON
CAMPMATE_ICON = 'gui/ui_res_2/battle/map/icon_teammate.png'
ENEMY_HIT_SHOW_THREE_SECOND = 3

class MapZombieFFAInfoWidget(object):
    HIDE_TAG = 65537

    def __init__(self, panel, parent_nd):
        self.map_panel = panel
        self.parent_nd = parent_nd
        self.top_entity_widgets = []
        self.entity_2_widgets = {}
        self.top_players = {}
        self.campmate_widgets = {}
        self.process_event(True)

    def destroy(self):
        self.process_event(False)
        for widget in self.top_entity_widgets:
            widget.destroy()

        for widget in six.itervalues(self.entity_2_widgets):
            widget.destroy()

        self.top_entity_widgets = []
        self.top_players.clear()
        self.campmate_widgets.clear()
        self.entity_2_widgets.clear()

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'update_top_group_info': self.update_top_group_info,
           'campmate_make_damage_event': self.show_hit_map_mark,
           'zombieffa_update_camp_status': self.update_campmate_status
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def update_top_group_info(self, group_id, soul_data):
        cam_lplayer = global_data.cam_lplayer
        if not cam_lplayer:
            return
        self.top_players = soul_data
        pre_top_entity_widgets = self.top_entity_widgets
        new_top_entity_widgets = []
        for widget in pre_top_entity_widgets:
            widget.set_show(False)

        for entity_id, pos in six.iteritems(soul_data):
            if cam_lplayer.ev_g_is_campmate_by_eid(entity_id):
                if pre_top_entity_widgets:
                    widget = pre_top_entity_widgets.pop(0)
                    new_top_entity_widgets.append(widget)
                continue
            if not pre_top_entity_widgets:
                widget = EntityMapMark(self.parent_nd, self.map_panel)
            else:
                widget = self.top_entity_widgets.pop(0)
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
        if entity_id in self.top_players:
            return
        widget = self.gen_entity_widget(entity_id)
        widget.set_display_frame_by_path(ENEMY_HIT_ICON)
        pos = entity_logic.ev_g_position()
        if pos:
            widget.on_update((pos.x, pos.z))
            widget.show_with_time(ENEMY_HIT_SHOW_THREE_SECOND)

    def update_campmate_status(self):
        camp_status = global_data.zombieffa_battle_data.get_camp_status()
        for widget in six.itervalues(self.campmate_widgets):
            widget.set_show(False)

        pre_camp_widgets = self.campmate_widgets
        new_camp_widgets = {}
        for eid, pos, is_in_mecha in camp_status:
            widget = pre_camp_widgets.get(eid) or self.gen_entity_widget(eid)
            self._update_campmate_widget(widget, pos, is_in_mecha)
            new_camp_widgets[eid] = widget

        self.campmate_widgets = new_camp_widgets

    def _update_campmate_widget(self, widget, pos, is_in_mecha):
        if not is_in_mecha:
            return
        widget.set_display_frame_by_path(CAMPMATE_ICON)
        widget.on_update(pos)

    def gen_entity_widget(self, entity_id):
        if entity_id not in self.entity_2_widgets:
            widget = EntityMapMark(self.parent_nd, self.map_panel)
            self.entity_2_widgets[entity_id] = widget
        return self.entity_2_widgets[entity_id]