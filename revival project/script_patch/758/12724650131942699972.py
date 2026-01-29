# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/map/map_widget/MapFlagBasePointerLineWidget.py
from __future__ import absolute_import
from logic.comsys.map.map_widget import MapScaleInterface
import cc
from logic.entities.Battle import Battle
import math3d
import common.utils.timer as timer

class MapFlagBasePointerLineWidget(MapScaleInterface.MapScaleInterface):

    def __init__(self, panel):
        super(MapFlagBasePointerLineWidget, self).__init__(panel.map_nd, panel)
        self.dir_widgets = [self.map_panel.map_nd.sv_safe_dir5, self.map_panel.map_nd.sv_safe_dir6]
        self.content_heights = []
        for dir_widget in self.dir_widgets:
            dir_widget.setTouchEnabled(False)
            self.content_heights.append(dir_widget.getContentSize().height)

        self.update_timer = None
        self.picker_id = None
        self.picker_faction = None
        self.start_map_pos = None
        self.end_map_pos = None
        self.activate_idx = None
        self.process_event(True)
        battle_data = global_data.death_battle_data
        if battle_data:
            self.update_status(battle_data.picker_id, battle_data.flag_faction)
        self.start_timer()
        return

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'flagsnatch_flag_recover': self.on_flag_recover,
           'flagsnatch_flag_pick_up': self.on_flag_pick_up
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def start_timer(self):
        if self.update_timer:
            return
        self.update_timer = global_data.game_mgr.register_logic_timer(self.route_update, 0.1, mode=timer.CLOCK)

    def on_flag_recover(self, *args):
        self.update_status(None, None)
        return

    def on_flag_pick_up(self, picker_id, picker_faction, **args):
        self.update_status(picker_id, picker_faction)

    def update_status(self, picker_id, picker_faction):
        self.picker_id = picker_id
        self.picker_faction = picker_faction
        if not picker_id:
            self.activate_idx = None
        elif self.picker_faction == global_data.player.logic.ev_g_group_id():
            self.activate_idx = 0
        else:
            self.activate_idx = 1
        return

    def route_update(self):
        self.hide_direction()
        if not global_data.battle or not global_data.death_battle_data or not self.picker_faction:
            return
        self.flag_id = global_data.death_battle_data.flag_ent_id
        flag_ent = global_data.battle.get_entity(self.flag_id)
        flag_base_ent = global_data.death_battle_data.get_flag_base_ent_by_faction(self.picker_faction)
        if not flag_ent or not flag_base_ent:
            return
        start = flag_ent.logic.ev_g_position()
        end = flag_base_ent.logic.ev_g_position()
        self.show_direction_by_world_pos(start, end, self.activate_idx)

    def show_direction(self, start_map_pos, end_map_pos, act_idx):
        self.start_map_pos = start_map_pos
        self.end_map_pos = end_map_pos
        self.dir_widgets[act_idx].setVisible(True)
        self.update_direction(act_idx)

    def hide_direction(self):
        for dir_widget in self.dir_widgets:
            dir_widget.setVisible(False)

    def show_direction_by_world_pos(self, start, end, act_idx):
        start_map_position = self.trans_world_position(start)
        round_map_position = self.trans_world_position(end)
        self.show_direction(start_map_position, round_map_position, act_idx)

    def destroy(self):
        self.hide_direction()
        self.dir_widgets = None
        if self.update_timer:
            global_data.game_mgr.unregister_logic_timer(self.update_timer)
            self.update_timer = None
        self.process_event(False)
        super(MapFlagBasePointerLineWidget, self).destroy()
        return

    def update_direction(self, act_idx):
        if not (self.start_map_pos and self.end_map_pos) or act_idx is None:
            return
        else:
            self.update_widget_scale(act_idx)
            start_map_pos = cc.Vec2(self.start_map_pos)
            diff_vec = cc.Vec2(self.end_map_pos)
            diff_vec.subtract(start_map_pos)
            lens = diff_vec.getLength()
            diff_vec.normalize()
            widget_scale = self.dir_widgets[act_idx].getScale()
            start_omit_length = 10
            diff_vec.scale(start_omit_length)
            start_map_pos.add(diff_vec)
            self.dir_widgets[act_idx].setPosition(start_map_pos)
            angle = diff_vec.getAngle()
            self.dir_widgets[act_idx].setRotation(-angle * 180 / 3.1415)
            actual_lens = (lens - start_omit_length) / widget_scale
            if actual_lens < 20:
                self.hide_direction()
                return
            self.dir_widgets[act_idx].SetContentSize(actual_lens, self.content_heights[act_idx])
            return

    def update_widget_scale(self, act_idx):
        self.dir_widgets[act_idx].setScale(1.0 / self.map_panel.cur_map_scale)

    def on_map_scale(self, scale):
        self.update_direction(self.activate_idx)