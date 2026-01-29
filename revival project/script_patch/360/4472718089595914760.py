# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/Train/TrainMarkUI.py
from __future__ import absolute_import
import six
from six.moves import range
from logic.gcommon.const import NEOX_UNIT_SCALE
from logic.gutils import screen_utils
import math3d
import cc
import math
import copy
from common.uisys.basepanel import BasePanel
from common.const.uiconst import SMALL_MAP_ZORDER, UI_VKB_NO_EFFECT
from common.platform.device_info import DeviceInfo
from logic.gcommon import time_utility as tutil
from common.utils.ui_utils import get_scale
from common.utils.cocos_utils import getScreenSize
OFFSET_Y = 40

class TrainStationMarkWidget(object):

    def __init__(self, panel, ui_template):
        self.panel = panel
        self._nd = global_data.uisystem.load_template_create(ui_template)
        self._nd.setVisible(True)
        self.panel.AddChild('', self._nd)
        self.init_parameters()
        self.init_timer()

    def init_parameters(self):
        self._station_pos = None
        self._timer = None
        device_info = DeviceInfo()
        self.screen_size = getScreenSize()
        self.is_can_full_screen = device_info.is_can_full_screen()
        self.screen_angle_limit = math.atan(self.screen_size.height / 2.0 / (self.screen_size.width / 2.0)) * 180 / math.pi
        self.scale_data = {'scale_90': (get_scale('90w'), get_scale('280w')),'scale_40': (
                      get_scale('40w'), get_scale('120w')),
           'scale_left': (
                        get_scale('90w'), get_scale('300w')),
           'scale_right': (
                         get_scale('90w'), get_scale('200w')),
           'scale_up': (
                      get_scale('90w'), get_scale('120w')),
           'scale_low': (
                       get_scale('90w'), get_scale('120w'))
           }
        train_node_data = global_data.train_battle_mgr.get_all_station_node()
        self.train_stop_nodes = global_data.train_battle_mgr.get_stop_nodes()
        self.train_node_dis = [ train_node_data[i + 1].get('track_dis') for i in range(len(train_node_data)) ]
        self.train_station_pos = train_node_data
        self.train_length = global_data.train_battle_mgr.get_rail_length()
        return

    def init_timer(self):
        self.clear_run_timer()
        self._timer = global_data.game_mgr.get_logic_timer().register(func=self.update_nd, interval=1)

    def update_station(self):
        if not global_data.train_battle_mgr or not global_data.battle:
            return
        train_carriage = global_data.train_battle_mgr.get_train_carriage()
        if not train_carriage:
            return
        dis = train_carriage.sd.ref_target_dis
        if not dis:
            return
        stat_idx = self.get_next_station_pos(dis)
        last_round_dis = global_data.battle.get_last_round_dis()
        if last_round_dis == -1:
            last_round_next_station = -1
        else:
            last_round_dis = int(3680.0 + last_round_dis) % int(global_data.train_battle_mgr.get_rail_length())
            last_round_next_station = self.get_next_station_pos(last_round_dis)
            last_round_next_station = min(last_round_next_station, 2)
        if stat_idx != last_round_next_station:
            if stat_idx == 1:
                self._station_pos = self.train_station_pos.get(2).get('station_pos', [0, 0, 0])
            else:
                self._station_pos = self.train_station_pos.get(3).get('station_pos', [0, 0, 0])
        else:
            self._station_pos = train_carriage.logic.ev_g_rail_pos_from_dis(last_round_dis)

    def update_nd(self):
        self.update_station()
        self.update_group_state()
        if self._station_pos:
            self.update_nd_pos(self._station_pos)

    def update_nd_pos(self, pos):
        cam = global_data.game_mgr.scene.active_camera
        if not cam:
            return
        position = math3d.vector(*pos)
        position.y += OFFSET_Y
        is_in_screen, end_pos, angle = screen_utils.world_pos_to_screen_pos(self._nd, position, self.screen_size, self.screen_angle_limit, self.is_can_full_screen, self.scale_data)
        dist = cam.position - position
        dist = dist.length / NEOX_UNIT_SCALE
        self._nd.setPosition(end_pos)
        lplayer = global_data.cam_lplayer
        if lplayer:
            self._nd.nd_rotate.setVisible(not is_in_screen)
            if not is_in_screen:
                self._nd.nd_rotate.setRotation(angle + 90)

    def update_group_state(self):
        if not global_data.battle:
            return
        atk_group_id = global_data.battle.get_atk_group_id()
        my_group_id = global_data.battle.get_my_group_id()
        self._is_atk = atk_group_id == my_group_id
        if self._is_atk:
            self._nd.bar_red.setVisible(False)
            self._nd.bar_blue.setVisible(True)
        else:
            self._nd.bar_red.setVisible(True)
            self._nd.bar_blue.setVisible(False)

    def get_next_station_pos(self, train_dis):
        last_station_idx = -1
        for idx in range(len(self.train_node_dis) - 1):
            if train_dis >= self.train_node_dis[idx] and train_dis < self.train_node_dis[idx + 1]:
                return idx + 1
            if self.train_node_dis[idx] > self.train_node_dis[idx + 1]:
                last_station_idx = idx

        last_stat = train_dis - self.train_node_dis[last_station_idx]
        forward_stat = self.train_node_dis[last_station_idx + 1] - train_dis
        last_stat = last_stat + self.train_length if last_stat < 0 else last_stat
        forward_stat = forward_stat + self.train_length if forward_stat < 0 else forward_stat
        return last_station_idx + 1

    def clear_run_timer(self):
        self._timer and global_data.game_mgr.get_logic_timer().unregister(self._timer)
        self._timer = None
        return

    def destroy(self):
        self.clear_run_timer()


class TrainMarkWidget(object):

    def __init__(self, panel, ui_template):
        self.panel = panel
        self._nd = global_data.uisystem.load_template_create(ui_template)
        self._nd.setVisible(True)
        self.panel.AddChild('', self._nd)
        if global_data.aim_transparent_mgr:
            global_data.aim_transparent_mgr.add_target_node(self.__class__.__name__, [self._nd])
        self.init_parameters()
        self.init_panel()
        self.init_timer()

    def init_parameters(self):
        self._timer = None
        self._visible_node = None
        device_info = DeviceInfo()
        self.screen_size = getScreenSize()
        self.is_can_full_screen = device_info.is_can_full_screen()
        self.screen_angle_limit = math.atan(self.screen_size.height / 2.0 / (self.screen_size.width / 2.0)) * 180 / math.pi
        self.scale_data = {'scale_90': (get_scale('90w'), get_scale('280w')),'scale_40': (
                      get_scale('40w'), get_scale('120w')),
           'scale_left': (
                        get_scale('90w'), get_scale('300w')),
           'scale_right': (
                         get_scale('90w'), get_scale('200w')),
           'scale_up': (
                      get_scale('90w'), get_scale('120w')),
           'scale_low': (
                       get_scale('90w'), get_scale('120w'))
           }
        return

    def init_panel(self):
        pass

    def init_timer(self):
        self.clear_run_timer()
        self._timer = global_data.game_mgr.get_logic_timer().register(func=self.update_nd, interval=1)

    def update_nd(self):
        if not self._visible_node:
            self.update_group_state()
            return
        if not global_data.train_battle_mgr:
            return
        carriage = global_data.train_battle_mgr.get_train_carriage()
        if not carriage:
            return
        pos = carriage.sd.ref_carriage_pos
        if pos:
            self.update_nd_pos(pos)

    def update_nd_pos(self, pos):
        cam = global_data.game_mgr.scene.active_camera
        if not cam:
            return
        position = math3d.vector(pos)
        position.y += OFFSET_Y
        is_in_screen, end_pos, angle = screen_utils.world_pos_to_screen_pos(self._nd, position, self.screen_size, self.screen_angle_limit, self.is_can_full_screen, self.scale_data)
        dist = cam.position - position
        dist = dist.length / NEOX_UNIT_SCALE
        self._nd.setPosition(end_pos)
        lplayer = global_data.cam_lplayer
        if lplayer:
            self._nd.nd_rotate.setVisible(not is_in_screen)
            if not is_in_screen:
                self._nd.nd_rotate.setRotation(angle + 90)

    def update_around_state(self, num_atk, num_def):
        if not self._visible_node:
            return
        self._nd.bar_red.setVisible(bool(num_def))
        self._nd.lab_num_red.SetString(str(num_def))
        self._nd.bar_blue.setVisible(bool(num_atk))
        self._nd.lab_num_blue.SetString(str(num_atk))
        if num_atk == num_def and num_atk and num_def:
            self._nd.nd_mark_blue.setVisible(False)
            self._nd.nd_mark_red.setVisible(False)
            self._nd.nd_mark_yellow.setVisible(True)
            self._nd.nd_mark_yellow.img_mask.lab_camp.SetString(17575)
        elif num_def < num_atk:
            self._nd.nd_mark_yellow.setVisible(False)
            if self._is_atk:
                self._nd.nd_mark_blue.setVisible(True)
                self._nd.nd_mark_red.setVisible(False)
                self._nd.nd_mark_blue.img_mask.lab_camp.SetString(17574)
            else:
                self._nd.nd_mark_blue.setVisible(False)
                self._nd.nd_mark_red.setVisible(True)
                self._nd.nd_mark_red.img_mask.lab_camp.SetString(17574)
        elif not num_atk and not num_def:
            self._nd.nd_mark_yellow.setVisible(False)
            if self._is_atk:
                self._nd.nd_mark_blue.setVisible(True)
                self._nd.nd_mark_red.setVisible(False)
                self._nd.nd_mark_blue.img_mask.lab_camp.SetString(17825)
            else:
                self._nd.nd_mark_blue.setVisible(False)
                self._nd.nd_mark_red.setVisible(True)
                self._nd.nd_mark_red.img_mask.lab_camp.SetString(17826)
        else:
            self._nd.nd_mark_yellow.setVisible(False)
            if self._is_atk:
                self._nd.nd_mark_blue.setVisible(False)
                self._nd.nd_mark_red.setVisible(True)
                self._nd.nd_mark_red.img_mask.lab_camp.SetString(17827)
            else:
                self._nd.nd_mark_blue.setVisible(True)
                self._nd.nd_mark_red.setVisible(False)
                self._nd.nd_mark_blue.img_mask.lab_camp.SetString(17828)

    def update_group_state(self):
        if not global_data.battle:
            return
        atk_group_id = global_data.battle.get_atk_group_id()
        my_group_id = global_data.battle.get_my_group_id()
        self._is_atk = atk_group_id == my_group_id
        self._visible_node = self._nd.nd_mark_blue
        if self._is_atk:
            self._nd.bar_red.SetDisplayFrameByPath('', 'gui/ui_res_2/battle_push_train/bar_battle_push_score_red.png')
            self._nd.bar_blue.SetDisplayFrameByPath('', 'gui/ui_res_2/battle_push_train/bar_battle_push_score_blue.png')
        else:
            self._nd.bar_red.SetDisplayFrameByPath('', 'gui/ui_res_2/battle_push_train/bar_battle_push_score_blue.png')
            self._nd.bar_blue.SetDisplayFrameByPath('', 'gui/ui_res_2/battle_push_train/bar_battle_push_score_red.png')

    def clear_run_timer(self):
        self._timer and global_data.game_mgr.get_logic_timer().unregister(self._timer)
        self._timer = None
        return

    def destroy(self):
        self.clear_run_timer()


class TrainMarkUI(BasePanel):
    PANEL_CONFIG_NAME = 'battle/empty'
    DLG_ZORDER = SMALL_MAP_ZORDER
    UI_VKB_TYPE = UI_VKB_NO_EFFECT

    def on_init_panel(self):
        self.init_parameters()
        self.process_event(True)
        self.panel.setLocalZOrder(1)

    def on_finalize_panel(self):
        self.train_mark_widget and self.train_mark_widget.destroy()
        self.train_station_widget and self.train_station_widget.destroy()
        self.process_event(False)

    def init_parameters(self):
        self.train_mark_widget = TrainMarkWidget(self.panel, 'battle_push_train/i_battle_push_train_camp_mark_all')
        self.train_station_widget = TrainStationMarkWidget(self.panel, 'battle_push_train/i_battle_push_train_mark_destination')

    def on_update_train_around_state(self, num_atk, num_def):
        from logic.gutils import judge_utils
        if not global_data.player:
            return
        if not global_data.player.logic:
            return
        from logic.gutils import judge_utils
        if judge_utils.is_ob() or global_data.player.is_in_global_spectate() or global_data.player.logic.ev_g_is_in_spectate():
            self.train_mark_widget.update_group_state()
        self.train_mark_widget.update_around_state(num_atk, num_def)

    def update_train_mark_group_state(self):
        if not self.train_mark_widget:
            return
        self.train_mark_widget.update_group_state()

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'update_train_around_state': self.on_update_train_around_state,
           'show_last_round_info_event': self.update_train_mark_group_state
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)