# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/map/map_widget/MapParadropMarkWidget.py
from __future__ import absolute_import
from logic.comsys.map.map_widget import MapScaleInterface
from common.utils.cocos_utils import ccp
from logic.gcommon.const import NEOX_UNIT_SCALE
import math
from common.utils.timer import CLOCK
from logic.gcommon.time_utility import time
from mobile.common.EntityManager import EntityManager
from common.cfg import confmgr

class MapParadropMarkWidget(MapScaleInterface.MapScaleInterface):
    TICK_TIME = 1
    TICK_LIFE = 60
    NODE_MARGIN = 24

    def __init__(self, panel, parent_nd, view):
        super(MapParadropMarkWidget, self).__init__(parent_nd, panel)
        self._nd = global_data.uisystem.load_template_create('battle_koth/i_airdrop_mark')
        self.parent_nd.AddChild('', self._nd, Z=2)
        self._nd.setAnchorPoint(ccp(0.5, 0.5))
        self._paradrop_pos = None
        self._paradrop_id = None
        self.sp_dir = ccp(0, 1)
        self._paradrop_tick = 0
        self.timer_id = None
        self.view = view
        self._nd.nd_mark.setVisible(False)
        self._nd.nd_mark2.setVisible(True)
        self._nd.setVisible(False)
        message_ui = global_data.ui_mgr.get_ui('BattleInfoParadrop')
        if message_ui and message_ui.min_position_data:
            timestamp, paradrop_id, position = message_ui.min_position_data
            pase_time = time() - timestamp
            if 0 < pase_time < MapParadropMarkWidget.TICK_LIFE:
                self.add_paradrop_mark(paradrop_id, position, pase_time)
        global_data.emgr.scene_add_paradrop += self.add_paradrop_mark
        global_data.emgr.scene_del_paradrop += self.del_paradrop_mark
        return

    def del_paradrop_mark(self, paradrop_id):
        if self._paradrop_id == paradrop_id:
            self._paradrop_id = None
            self._paradrop_pos = None
            if self.timer_id:
                global_data.game_mgr.unregister_logic_timer(self.timer_id)
                self.timer_id = None
            self._nd.setVisible(False)
        return

    def add_paradrop_mark(self, paradrop_id, paradrop_position, min_paradrop_no, pase_time=0):
        paradrop_conf = confmgr.get('paradrop_data', str(min_paradrop_no), default={})
        pics = paradrop_conf.get('paradrop_direct_pic')
        if pics and len(pics) == 2:
            mark_pic, nd_rotate_pic = pics
            self._nd.nd_mark2.icon.SetDisplayFrameByPath('', mark_pic)
            self._nd.nd_mark2.nd_rotate.bar.SetDisplayFrameByPath('', nd_rotate_pic)
        self._paradrop_id = paradrop_id
        self._paradrop_pos = self.trans_world_position(paradrop_position)
        self._paradrop_tick = pase_time - MapParadropMarkWidget.TICK_TIME
        if not self.timer_id:
            self.timer_id = global_data.game_mgr.register_logic_timer(self.on_update, MapParadropMarkWidget.TICK_TIME, mode=CLOCK)
        self.on_update()

    def on_update(self):
        if not self._paradrop_pos:
            self._nd.setVisible(False)
            return
        self._paradrop_tick += MapParadropMarkWidget.TICK_TIME
        if self._paradrop_tick >= MapParadropMarkWidget.TICK_LIFE and self.timer_id:
            self.del_paradrop_mark(self._paradrop_id)
            return
        cam_lplayer = global_data.cam_lplayer
        if not self.map_panel.isVisible():
            return
        if not cam_lplayer:
            self._nd.setVisible(False)
            return
        player_position = cam_lplayer.ev_g_position()
        if not player_position:
            self._nd.setVisible(False)
            return
        player_pos = self.trans_world_position(player_position)
        paradrop_pos = ccp(self._paradrop_pos.x, self._paradrop_pos.y)
        size, dist = self.view
        max_x, max_y = size
        view_left_x = max(0, player_pos.x - dist)
        view_right_x = min(max_x, player_pos.x + dist)
        view_upper_y = min(max_y, player_pos.y + dist)
        view_lower_y = max(0, player_pos.y - dist)
        if view_left_x <= paradrop_pos.x <= view_right_x and view_lower_y <= paradrop_pos.y <= view_upper_y:
            self._nd.setVisible(False)
            return
        margin = MapParadropMarkWidget.NODE_MARGIN
        left_x = view_left_x + margin
        right_x = view_right_x - margin
        upper_y = view_upper_y - margin
        lower_y = view_lower_y + margin
        start_x, start_y = player_pos.x, player_pos.y
        end_x, end_y = paradrop_pos.x, paradrop_pos.y
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
        paradrop_pos.subtract(player_pos)
        degree = paradrop_pos.getAngle(self.sp_dir) * 180 / math.pi
        self._nd.nd_mark2.nd_rotate.setRotation(degree)
        self._nd.setVisible(True)

    def destroy(self):
        global_data.emgr.scene_add_paradrop -= self.add_paradrop_mark
        global_data.emgr.scene_del_paradrop -= self.del_paradrop_mark
        if self.timer_id:
            global_data.game_mgr.unregister_logic_timer(self.timer_id)
            self.timer_id = None
        super(MapParadropMarkWidget, self).destroy()
        return