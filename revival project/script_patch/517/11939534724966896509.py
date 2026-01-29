# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/map/map_widget/MapTrainWidget.py
from __future__ import absolute_import
import six
from six.moves import range
from .MapScaleInterface import MapScaleInterface
from logic.client.const import game_mode_const
from common.utils.cocos_utils import ccp
from common.utils.timer import CLOCK
from logic.gcommon.const import NEOX_UNIT_SCALE
import math
import math3d
import world
import cc
from common.uisys.uielment.CCNode import CCNode
from logic.gutils.map_utils import get_map_config

class PartTrainStationMapMark(MapScaleInterface):

    def __init__(self, parent_nd, ctrl_widget, idx):
        super(PartTrainStationMapMark, self).__init__(parent_nd, ctrl_widget)
        self.map_panel = ctrl_widget
        self._nd = global_data.uisystem.load_template_create('map/ccb_map_train_station')
        self.parent_nd.AddChild('', self._nd)
        self._nd.setVisible(True)
        self.station_idx = idx
        self.init_panel()

    def init_panel(self):
        station_data = global_data.train_battle_mgr.get_station_node(self.station_idx)
        if station_data:
            pos_3 = self.trans_world_position_ex(station_data.get('station_pos', [0, 0, 0]))
            pos_2 = ccp(pos_3.x, pos_3.y)
            self.set_position(pos_2)
            self._nd.lab_num.SetString(str(self.station_idx))


class PartTrainMapMark(MapScaleInterface):
    INIT_DIST = 100
    MAX_X = 1800
    MAX_Y = 950
    NODE_MARGIN = 24

    def __init__(self, parent_nd, ctrl_widget):
        super(PartTrainMapMark, self).__init__(parent_nd, ctrl_widget)
        self.map_panel = ctrl_widget
        self._nd = global_data.uisystem.load_template_create('map/ccb_map_trian')
        self.parent_nd.AddChild('', self._nd)
        self.sp_dir = ccp(0, 1)
        self._nd.setVisible(False)
        self._visible_node = None
        self._is_atk = False
        self.timer = None
        self.init_train_timer()
        return

    def init_train_timer(self):
        if self.timer:
            global_data.game_mgr.unregister_logic_timer(self.timer)
        self.timer = global_data.game_mgr.register_logic_timer(self.update_train_pos, interval=0.2, times=-1, mode=CLOCK)

    def update_train_pos(self):
        if not global_data.train_battle_mgr:
            return
        cam_lplayer = global_data.cam_lplayer
        if not cam_lplayer:
            return
        train_carriage = global_data.train_battle_mgr.get_train_carriage()
        if not train_carriage:
            return
        carriage_pos = train_carriage.sd.ref_carriage_pos
        move_dir = train_carriage.sd.ref_dir
        player_position = cam_lplayer.ev_g_position()
        if not carriage_pos or not move_dir or not player_position:
            return
        pos = [
         carriage_pos.x, carriage_pos.y, carriage_pos.z]
        self._nd.setVisible(True)
        self._nd.nd_dir.setVisible(True)
        pos_3 = self.trans_world_position_ex(pos)
        pos_2 = ccp(pos_3.x, pos_3.y)
        self.set_position(pos_2)
        mark_pos = pos_2
        mark_uv_pos = ccp(mark_pos.x, mark_pos.y)
        pos_player = [
         player_position.x, player_position.y, player_position.z]
        player_pos = self.trans_world_position_ex(pos_player)
        max_x, max_y = self.MAX_X, self.MAX_Y
        dist = 110
        if 950 - player_pos.y > dist:
            offset = 0
        else:
            offset = dist * (1.0 - (950.0 - player_pos.y) / dist)
        dist += offset
        view_left_x = max(0, player_pos.x - dist)
        view_right_x = min(max_x, player_pos.x + dist)
        view_upper_y = min(950, player_pos.y + dist)
        view_lower_y = max(0, player_pos.y - dist)
        if view_left_x <= pos_2.x <= view_right_x:
            if view_lower_y <= pos_2.y <= view_upper_y:
                forward = train_carriage.logic.ev_g_model_forward()
                cos_f_to_d = forward.dot(move_dir)
                dir = forward * cos_f_to_d
                dir.is_zero or dir.normalize()
            cc_dir = ccp(dir.x, dir.z)
            degree = cc_dir.getAngle(self.sp_dir) * 180 / math.pi
            self._nd.nd_dir.setRotation(degree)
            return
        margin = 0
        left_x = view_left_x + margin
        right_x = view_right_x - margin
        upper_y = view_upper_y - margin
        lower_y = view_lower_y + margin
        start_x, start_y = player_pos.x, player_pos.y
        end_x, end_y = mark_uv_pos.x, mark_uv_pos.y
        x_delta = end_x - start_x
        y_delta = end_y - start_y
        border_x = right_x if x_delta >= 0 else left_x
        bx_delta = border_x - start_x
        x_ratio = bx_delta / x_delta if x_delta != 0 else 0
        border_z = upper_y if y_delta >= 0 else lower_y
        by_delta = border_z - start_y
        z_ratio = by_delta / y_delta if y_delta != 0 else 0
        ratio = min(x_ratio, z_ratio)
        pos_4 = ccp(start_x + x_delta * ratio, start_y + y_delta * ratio)
        mark_uv_pos.subtract(player_pos)
        degree = mark_uv_pos.getAngle(self.sp_dir) * 180 / math.pi
        self._nd.nd_dir.setRotation(degree)
        self.set_position(pos_4)

    def destroy(self):
        super(PartTrainMapMark, self).destroy()
        if self.timer:
            global_data.game_mgr.unregister_logic_timer(self.timer)


class PartTrainPointerLine(MapScaleInterface):

    def __init__(self, panel):
        super(PartTrainPointerLine, self).__init__(panel.map_nd, panel)
        self.dir_widgets = [self.map_panel.map_nd.sv_safe_dir5, self.map_panel.map_nd.sv_safe_dir6]
        self.content_heights = []
        for dir_widget in self.dir_widgets:
            dir_widget.setTouchEnabled(False)
            self.content_heights.append(dir_widget.getContentSize().height)

        self.update_timer = None
        self.start_map_pos = None
        self.end_map_pos = None
        self.activate_idx = None
        train_node_data = global_data.train_battle_mgr.get_all_station_node()
        self.stop_nodes = global_data.train_battle_mgr.get_stop_nodes()
        self.train_node_dis = [ train_node_data[i + 1].get('track_dis') for i in range(len(train_node_data)) ]
        self.train_station_pos = train_node_data
        self.train_length = global_data.train_battle_mgr.get_rail_length()
        self.process_event(True)
        self.start_timer()
        return

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'show_last_round_info_event': self.update_group_state,
           'update_train_around_state': self.on_update_train_around_state
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def start_timer(self):
        if self.update_timer:
            global_data.game_mgr.unregister_logic_timer(self.update_timer)
        self.update_group_state()
        self.update_timer = global_data.game_mgr.register_logic_timer(self.route_update, 0.2, mode=2)

    def on_update_train_around_state(self, num_atk, num_def):
        self.update_group_state()

    def update_group_state(self):
        if not global_data.battle:
            self.activate_idx = 0
            return
        if global_data.battle.get_atk_group_id() == global_data.battle.get_my_group_id():
            self.activate_idx = 0
        else:
            self.activate_idx = 1

    def route_update(self):
        self.hide_direction()
        if not global_data.train_battle_mgr:
            return
        train_carriage = global_data.train_battle_mgr.get_train_carriage()
        if not train_carriage:
            return
        dis = train_carriage.sd.ref_target_dis
        carriage_pos = train_carriage.sd.ref_carriage_pos
        if not dis or not carriage_pos:
            return
        start = carriage_pos
        stat_idx = self.get_next_station_pos(dis)
        if stat_idx == 1:
            end = self.train_station_pos.get(2).get('station_pos', [0, 0, 0])
        else:
            end = self.train_station_pos.get(3).get('station_pos', [0, 0, 0])
        self.show_direction_by_world_pos(start, end)

    def show_direction(self, start_map_pos, end_map_pos):
        self.start_map_pos = start_map_pos
        self.end_map_pos = end_map_pos
        self.dir_widgets[self.activate_idx].setVisible(True)
        self.update_direction()

    def hide_direction(self):
        for dir_widget in self.dir_widgets:
            dir_widget.setVisible(False)

    def show_direction_by_world_pos(self, start, end):
        start_map_position = self.trans_world_position(start)
        round_map_position = self.trans_world_position_ex(end)
        self.show_direction(start_map_position, round_map_position)

    def destroy(self):
        self.hide_direction()
        self.dir_widgets = None
        if self.update_timer:
            global_data.game_mgr.unregister_logic_timer(self.update_timer)
            self.update_timer = None
        self.process_event(False)
        super(PartTrainPointerLine, self).destroy()
        return

    def update_direction(self):
        if not (self.start_map_pos and self.end_map_pos):
            return
        self.update_widget_scale()
        start_map_pos = cc.Vec2(self.start_map_pos)
        diff_vec = cc.Vec2(self.end_map_pos)
        diff_vec.subtract(start_map_pos)
        lens = diff_vec.getLength()
        diff_vec.normalize()
        widget_scale = self.dir_widgets[self.activate_idx].getScale()
        start_omit_length = 10
        diff_vec.scale(start_omit_length)
        start_map_pos.add(diff_vec)
        self.dir_widgets[self.activate_idx].setPosition(start_map_pos)
        angle = diff_vec.getAngle()
        self.dir_widgets[self.activate_idx].setRotation(-angle * 180 / 3.1415)
        actual_lens = (lens - start_omit_length) / widget_scale
        if actual_lens < 20:
            self.hide_direction()
            return
        self.dir_widgets[self.activate_idx].SetContentSize(actual_lens, self.content_heights[0])

    def get_next_station_pos(self, train_dis):
        last_stat_idx = -1
        for idx in range(len(self.train_node_dis) - 1):
            if train_dis >= self.train_node_dis[idx] and train_dis < self.train_node_dis[idx + 1]:
                return idx + 1
            if self.train_node_dis[idx] > self.train_node_dis[idx + 1]:
                last_stat_idx = idx

        last_stat = train_dis - self.train_node_dis[last_stat_idx]
        forward_stat = self.train_node_dis[last_stat_idx + 1] - train_dis
        last_stat = last_stat + self.train_length if last_stat < 0 else last_stat
        forward_stat = forward_stat + self.train_length if forward_stat < 0 else forward_stat
        return last_stat_idx + 1

    def update_widget_scale(self):
        self.dir_widgets[self.activate_idx].setScale(1.0 / self.map_panel.cur_map_scale)

    def on_map_scale(self, scale):
        self.update_direction()


class MapTrainWidget(object):

    def __init__(self, panel, parent_nd):
        self.map_panel = panel
        self.parent_nd = parent_nd
        self.init_parameters()
        self.process_event(True)
        self.create_train_smallmap_mark()
        self.create_train_station_mark()
        self.create_train_line()

    def init_parameters(self):
        self.train_mark = None
        self.train_line = None
        self.station_mark = {}
        return

    def create_train_smallmap_mark(self):
        self.train_mark = PartTrainMapMark(self.parent_nd, self.map_panel)

    def create_train_station_mark(self):
        for idx in range(3):
            self.station_mark[idx + 1] = PartTrainStationMapMark(self.parent_nd, self.map_panel, idx + 1)

    def create_train_line(self):
        self.train_line = PartTrainPointerLine(self.map_panel)

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'update_train_small_map_icon': self.on_net_reconnect
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def on_net_reconnect(self, *args):
        if self.train_mark:
            self.train_mark.init_train_timer()
        if self.train_line:
            self.train_line.start_timer()

    def destroy(self):
        if self.train_mark:
            self.train_mark.destroy()
        self.train_mark = None
        if self.station_mark:
            for idx, mark in six.iteritems(self.station_mark):
                mark.destroy()

        if self.train_line:
            self.train_line.destroy()
        self.train_line = None
        self.station_mark = None
        self.process_event(False)
        return