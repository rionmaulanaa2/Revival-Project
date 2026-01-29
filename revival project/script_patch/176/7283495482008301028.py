# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/map/map_widget/MapEnemyInfoWidget.py
from __future__ import absolute_import
from six.moves import range
from logic.comsys.map.map_widget import MapScaleInterface
from common.utils.cocos_utils import ccp
from common.utils.timer import CLOCK
import math

class MapMark(MapScaleInterface.MapScaleInterface):
    NODE_MARGIN = 12

    def __init__(self, parent_nd, ctrl_widget):
        super(MapMark, self).__init__(parent_nd)
        self._nd = global_data.uisystem.load_template_create('map/ccb_enemy_locate')
        self.parent_nd.AddChild('', self._nd, Z=2)
        self._nd.setScale(1.0 / ctrl_widget.cur_map_scale)
        self.sp_dir = ccp(0, 1)

    def on_update(self, pos, view):
        if not view:
            return
        cam_lplayer = global_data.cam_lplayer
        if not cam_lplayer:
            return
        player_position = cam_lplayer.ev_g_position()
        if not player_position:
            return
        player_pos = self.trans_world_position(player_position)
        enemy_pos_3 = self.trans_world_position(pos)
        enemy_pos_2 = ccp(enemy_pos_3.x, enemy_pos_3.y)
        size, dist = view
        max_x, max_y = size
        view_left_x = max(0, player_pos.x - dist)
        view_right_x = min(max_x, player_pos.x + dist)
        view_upper_y = min(max_y, player_pos.y + dist)
        view_lower_y = max(0, player_pos.y - dist)
        if view_left_x <= enemy_pos_2.x <= view_right_x and view_lower_y <= enemy_pos_2.y <= view_upper_y:
            self._nd.icon_enemy.SetDisplayFrameByPath('', 'gui/ui_res_2/battle/map/icon_enemy.png')
            self.set_position(enemy_pos_2)
            return
        self._nd.icon_enemy.SetDisplayFrameByPath('', 'gui/ui_res_2/battle/map/icon_enemy2.png')
        margin = self.NODE_MARGIN
        left_x = view_left_x + margin
        right_x = view_right_x - margin
        upper_y = view_upper_y - margin
        lower_y = view_lower_y + margin
        start_x, start_y = player_pos.x, player_pos.y
        end_x, end_y = enemy_pos_2.x, enemy_pos_2.y
        x_delta = end_x - start_x
        y_delta = end_y - start_y
        border_x = right_x if x_delta >= 0 else left_x
        bx_delta = border_x - start_x
        x_ratio = bx_delta / x_delta if x_delta != 0 else 0
        border_z = upper_y if y_delta >= 0 else lower_y
        by_delta = border_z - start_y
        z_ratio = by_delta / y_delta if y_delta != 0 else 0
        ratio = min(x_ratio, z_ratio)
        self.set_position(ccp(start_x + x_delta * ratio, start_y + y_delta * ratio))
        enemy_pos_2.subtract(player_pos)
        degree = enemy_pos_2.getAngle(self.sp_dir) * 180 / math.pi
        self._nd.icon_enemy.setRotation(degree)


class MapEnemyInfoWidget:

    def __init__(self, panel, parent_nd, view=None):
        self.map_panel = panel
        self.parent_nd = parent_nd
        self.view = view
        self.enemy_widgets = []
        self.pos_lst = []
        self.timer_id = 0
        self.process_event(True)

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'scene_enemy_mark': self.update_nd_position,
           'scene_scan_enemy': self.scan_enemy
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def clear_timer(self):
        self.timer_id and global_data.game_mgr.unregister_logic_timer(self.timer_id)

    def destroy(self):
        self.process_event(False)
        for widget in self.enemy_widgets:
            widget.destroy()

        self.enemy_widgets = []
        self.pos_lst = []
        self.clear_timer()

    def trans_world_position(self, world_pos):
        from logic.gutils.map_utils import get_map_uv
        uv = get_map_uv(world_pos)
        content_size = self.parent_nd.GetContentSize()
        return ccp(uv[0] * content_size[0], uv[1] * content_size[1])

    def scan_enemy(self):
        self.show_scan()

    def show_scan(self):
        cam_lplayer = global_data.cam_lplayer
        if not cam_lplayer:
            return
        player_position = cam_lplayer.ev_g_position()
        if not player_position:
            return
        player_pos = self.trans_world_position(player_position)
        self.map_panel.panel.sv_map.GetContainer().nd_scan.setVisible(True)
        self.map_panel.panel.sv_map.GetContainer().PlayAnimation('show_scan')
        self.map_panel.panel.sv_map.GetContainer().nd_scan.setPosition(player_pos)

    def update_nd_position(self, pos_lst):
        self.pos_lst = pos_lst
        off_num = len(pos_lst) - len(self.enemy_widgets)
        if off_num < 0:
            for _ in range(abs(off_num)):
                widget = self.enemy_widgets.pop()
                widget.destroy()

        elif off_num > 0:
            for _ in range(abs(off_num)):
                widget = MapMark(self.parent_nd, self.map_panel)
                self.enemy_widgets.append(widget)

        self.refresh_enemy_widgets()

    def refresh_enemy_widgets(self):
        if not self.pos_lst:
            self.clear_timer()
            return
        for i, pos in enumerate(self.pos_lst):
            self.enemy_widgets[i].set_world_position(pos)

        if not self.timer_id:
            self.timer_id = global_data.game_mgr.register_logic_timer(self.on_update, 1, mode=CLOCK)
        self.on_update()

    def on_update(self):
        for i, pos in enumerate(self.pos_lst):
            self.enemy_widgets[i].on_update(pos, self.view)