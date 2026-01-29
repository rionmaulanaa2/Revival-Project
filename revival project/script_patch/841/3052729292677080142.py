# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/lobby/LobbyRockerUI.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
from common.const.uiconst import ROCKER_LAYER_ZORDER
from common.utils import ui_utils
from common.utils.cocos_utils import ccp
from cocosui import cc
import math3d
from logic.vscene.parts.ctrl.ShortcutFunctionalityMutex import claim_shortcut_functionality, unclaim_shortcut_functionality, movement_shortcut_names
MOVE_OFFSET = ui_utils.get_scale('10w')
from common.const import uiconst

class LobbyRockerUI(BasePanel):
    PANEL_CONFIG_NAME = 'battle/rocker'
    DLG_ZORDER = ROCKER_LAYER_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT

    def on_init_panel(self):
        self._cur_touch_id = None
        self.init_rocker()
        self.init_event()
        return

    def init_event(self):
        global_data.emgr.movie_start += self.hide_self

    def init_data(self):
        self.spawn_radius = 0
        self.run_bar_radius = 0

    def init_rocker(self):
        self.init_rocker_mapping()
        self.rocker_base_layer.SetNoEventAfterMove(False)
        self.update_spawn_radius()
        self.rocker_base_layer.set_sound_enable(False)
        self.init_touch_callback()
        x, y = self.nd_custom.GetPosition()
        self.nd_custom.SetPosition(x + 50, y + 70)

    def init_rocker_mapping(self):
        self.rocker_base_layer = self.panel.empty_button
        self.rocker_span_node = self.panel.run_bar
        self.rocker_center_node = self.panel.run_button
        self.local_center_pos = self.rocker_center_node.getPosition()

    def init_touch_callback(self):
        self.rocker_base_layer.BindMethod('OnBegin', self.on_touch_begin)
        self.rocker_base_layer.BindMethod('OnDrag', self.on_touch_move)
        self.rocker_base_layer.BindMethod('OnEnd', self.on_touch_end)
        self.rocker_base_layer.BindMethod('OnCancel', self.on_touch_cancel)

    def hide_self(self):
        self.setVisible(False)

    @claim_shortcut_functionality(movement_shortcut_names, 'LobbyRockerUI')
    def on_touch_begin(self, layer, touch):
        if self._cur_touch_id:
            return False
        cur_touch_id = touch.getId()
        self._cur_touch_id = cur_touch_id
        self.finger_down(touch)
        return True

    def on_touch_move(self, layer, touch):
        if layer.GetMovedDistance() < MOVE_OFFSET:
            return
        self.finger_move(touch)

    @unclaim_shortcut_functionality(movement_shortcut_names, 'LobbyRockerUI')
    def on_touch_end(self, layer, touch):
        self._cur_touch_id = None
        touch_info = self.get_touch_info(touch)
        self.finger_up(touch_info)
        return True

    def get_touch_info(self, touch):
        touch_info = {'pos': touch.getLocation(),
           'id': touch.getId(),
           'vec': touch.getDelta()
           }
        return touch_info

    def finger_down(self, touch):
        self.rocker_center_node.setVisible(True)
        self.panel.walk_bar.SetSelect(True)
        self.rocker_center_node.SetSelect(True)

    def finger_up(self, touch):
        self.panel.walk_bar.SetSelect(False)
        self.panel.rocker_light.setVisible(False)
        self.panel.dec_bar_running.setVisible(False)
        self.rocker_center_node.SetSelect(False)
        self.rocker_center_node.setPosition(self.local_center_pos)
        global_data.emgr.trigger_lobby_player_move_stop.emit()

    def finger_move(self, touch):
        from common.cinematic.movie_controller import MovieController
        if MovieController().playing:
            return
        cnt_pos, start_pos = touch.getLocation(), touch.getStartLocation()
        translate = ccp(cnt_pos.x - start_pos.x, cnt_pos.y - start_pos.y)
        self.calc_rocker_pos_in_span(translate)
        if translate.length() > 0:
            translate.normalize()
            v = math3d.vector(translate.x, 0, translate.y)
            global_data.emgr.trigger_lobby_player_move.emit(v)
        else:
            global_data.emgr.trigger_lobby_player_move_stop.emit()

    def calc_rocker_pos_in_span(self, translate):
        trans_len = translate.getLength()
        unit_trans = cc.Vec2(translate)
        if unit_trans.getLength() > 0:
            unit_trans.normalize()
        if trans_len >= self.spawn_radius:
            translate = ccp(unit_trans.x * self.spawn_radius, unit_trans.y * self.spawn_radius)
        span_pos = self.rocker_span_node.ConvertToWorldSpacePercentage(50, 50)
        wpos = ccp(span_pos.x + translate.x, span_pos.y + translate.y)
        lpos = self.rocker_center_node.getParent().convertToNodeSpace(wpos)
        self.rocker_center_node.setPosition(lpos)

    def on_touch_cancel(self, layer, touch):
        return self.on_touch_end(layer, touch)

    def update_spawn_radius(self):
        max_width = self.rocker_span_node.ConvertToWorldSpacePercentage(100, 50).x
        mid_width = self.rocker_span_node.ConvertToWorldSpacePercentage(50, 50).x
        local_radius = 0.9 * (max_width - mid_width)
        self.spawn_radius = local_radius
        max_width = self.panel.run_bar.ConvertToWorldSpacePercentage(100, 50).y
        mid_width = self.panel.run_bar.ConvertToWorldSpacePercentage(50, 50).y
        self.run_bar_radius = max_width - mid_width