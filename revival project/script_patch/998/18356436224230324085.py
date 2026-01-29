# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/map/map_widget/BigMapMarkBtnWidget.py
from __future__ import absolute_import
from __future__ import print_function
from common.utils.cocos_utils import ccp
from logic.gutils import map_utils

class BigMapMarkBtnWidget(object):

    def __init__(self, panel):
        super(BigMapMarkBtnWidget, self).__init__()
        self.map_panel = panel
        self.init_event(panel)

    def init_event(self, panel):
        self.init_btn_draw(panel)
        self.init_clear_btn(panel)
        self.init_btn_locate(panel)
        self.map_panel.btn_clear.setVisible(map_utils.check_can_draw_mark_or_route())
        self.map_panel.btn_draw.setVisible(map_utils.check_can_draw_mark_or_route())

    def set_route_and_mark_visible(self, visible):
        self.map_panel.btn_draw.setVisible(visible)
        self.map_panel.btn_clear.setVisible(visible)

    def destroy(self):
        self.map_panel = None
        return

    def init_clear_btn(self, panel):
        btn = panel.btn_clear
        btn.SetSwallowTouch(True)
        btn.BindMethod('OnClick', self.on_click_btn_clear)

    def init_btn_locate(self, panel):
        btn = panel.btn_local_locate
        btn.SetSwallowTouch(True)
        btn.BindMethod('OnClick', self.on_click_btn_locate)

    def init_btn_draw(self, ui_obj):
        btn_draw = ui_obj.panel.btn_draw
        btn_draw.SetSwallowTouch(True)
        btn_draw.EnableCustomState(True)
        btn_draw.BindMethod('OnClick', self.on_click_btn_draw)

    def on_click_btn_draw(self, btn, *args):
        self.map_panel.switch_touch_mode()

    def on_click_btn_clear(self, btn, *args):
        player = global_data.player
        if player and player.logic:
            player.logic.send_event('E_TRY_DRAW_MAP_ROUTE', [])
            player.logic.send_event('E_TRY_CLEAR_SELF_MAP_MARK')
        print('clear drawn route')
        self.map_panel.route_board.on_update()

    def on_click_btn_locate(self, btn, *args):
        print('click btn locate')
        cam_lplayer = global_data.cam_lplayer
        if not cam_lplayer:
            return
        widget = self.map_panel._get_player_map_locate(cam_lplayer.id)
        if not widget:
            return
        map_pos = widget.get_position()
        if map_pos:
            map_scale = self.map_panel.cur_map_scale
            self.map_panel.panel.sv_map.CenterWithPos(map_pos.x * map_scale, map_pos.y * map_scale)

    def trans_world_position_ex(self, tuple_world_pos):
        from logic.gutils.map_utils import get_map_uv_ex
        uv = get_map_uv_ex(tuple_world_pos)
        content_size = self.map_panel.map_nd.nd_scale_up.GetContentSize()
        return ccp(uv[0] * content_size[0], uv[1] * content_size[1])

    def move_to_locate(self, pos):
        map_pos = self.trans_world_position_ex(pos)
        if map_pos:
            map_scale = self.map_panel.cur_map_scale
            self.map_panel.panel.sv_map.CenterWithPos(map_pos.x * map_scale, map_pos.y * map_scale)