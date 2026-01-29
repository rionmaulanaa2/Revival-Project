# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/map/map_widget/MidMapTouchLayerWidget.py
from __future__ import absolute_import
from logic.gcommon.common_const.battle_const import MARK_NORMAL, MAP_POS_NO_Y
from logic.vscene.parts.gamemode.GMDecorator import execute_by_mode
from logic.client.const import game_mode_const
from logic.gutils import map_utils

class MidMapTouchLayerWidget(object):

    def __init__(self, panel):
        super(MidMapTouchLayerWidget, self).__init__()
        self.map_panel = panel
        self.pressed_wpos = None
        self.init_scroll_touch_event()
        return

    def destroy(self):
        self.map_panel = None
        return

    def on_layer_touch_begin(self, layer, touch):
        self.pressed_wpos = touch.getLocation()

    def on_layer_pressed(self, layer):
        if not map_utils.check_can_draw_mark_or_route():
            return
        ui_inst = global_data.ui_mgr.get_ui('QuickMarkUI')
        if ui_inst:
            ui_inst.on_begin(self.pressed_wpos)
            ui_inst.enable_mid_map(True)

    def on_layer_touch_drag(self, layer, touch):
        if not map_utils.check_can_draw_mark_or_route():
            return
        ui_inst = global_data.ui_mgr.get_ui('QuickMarkUI')
        if ui_inst and ui_inst.isVisible():
            ui_inst.on_drag(touch.getLocation())

    def on_layer_touch_end(self, layer, touch):
        if not map_utils.check_can_draw_mark_or_route():
            return
        else:
            ui_inst = global_data.ui_mgr.get_ui('QuickMarkUI')
            if ui_inst and ui_inst.isVisible():
                ui_inst.on_end(touch.getLocation())
                ui_inst.enable_mid_map(False)
            else:
                self.mark_map(touch.getLocation(), MARK_NORMAL)
            self.pressed_wpos = None
            return

    def on_mid_map_mark(self, mark_type):
        if not self.pressed_wpos:
            return
        self.mark_map(self.pressed_wpos, mark_type)

    def mark_map(self, touch_wpos, mark_type):
        map_pos = self.map_panel.map_nd.convertToNodeSpace(touch_wpos)
        if map_pos and global_data.player and global_data.player.logic:
            part_map = global_data.game_mgr.scene.get_com('PartMap')
            v3d_scn_pos = part_map.get_map_pos_in_world(map_pos)
            v3d_scn_pos.y = MAP_POS_NO_Y
            global_data.player.logic.send_event('E_TRY_DRAW_MAP_MARK', mark_type, v3d_scn_pos)
            if MARK_NORMAL == mark_type:
                global_data.sound_mgr.play_ui_sound('ui_confirm_location')

    @execute_by_mode(False, (game_mode_const.GAME_MODE_DEATHS,))
    def init_scroll_touch_event(self):
        touch_layer = self.map_panel.touch_layer
        touch_layer.SetPressEnable(True)
        touch_layer.BindMethod('OnBegin', self.on_layer_touch_begin)
        touch_layer.BindMethod('OnPressed', self.on_layer_pressed)
        touch_layer.BindMethod('OnDrag', self.on_layer_touch_drag)
        touch_layer.BindMethod('OnEnd', self.on_layer_touch_end)