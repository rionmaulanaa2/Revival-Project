# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/ArmRace/ArmRaceScoreUI.py
from __future__ import absolute_import
from common.const.uiconst import SMALL_MAP_ZORDER
from common.uisys.basepanel import BasePanel
from logic.comsys.battle import BattleUtils
from logic.gcommon import time_utility as tutil
from logic.gcommon.common_const import battle_const
from logic.gutils.role_head_utils import get_head_photo_res_path, get_role_default_photo
import math
import cc
from common.const import uiconst

class ArmRaceScoreUI(BasePanel):
    PANEL_CONFIG_NAME = 'battle_arms_race/battle_score_brife'
    DLG_ZORDER = SMALL_MAP_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    ITEM_WIDTH = 50
    UI_ACTION_EVENT = {'nd_score.OnClick': 'toggle_score_details'
       }

    def on_init_panel(self):
        self.init_parameters()
        self.init_event()
        self.init_panel()

    def init_parameters(self):
        self.player = None
        self.first_point_10 = False
        self.max_level = len(global_data.battle.get_armrace_level_weapom())
        self.last_point_off = 0
        self.left_30_seconds = False
        self.left_10_seconds = False
        self.role_data = {}
        return

    def on_finalize_panel(self):
        self.panel.lab_time.StopTimerAction()
        global_data.ui_mgr.close_ui('ArmRaceFinishCountDown')

    def init_panel(self):
        self.update_timestamp()
        if global_data.armrace_battle_data:
            self.update_group_score_data(global_data.armrace_battle_data.get_group_score_data())

    def toggle_score_details(self, *args):
        ui_inst = global_data.ui_mgr.get_ui('ArmRaceScoreDetailsUI')
        if ui_inst:
            global_data.ui_mgr.close_ui('ArmRaceScoreDetailsUI')
        else:
            global_data.ui_mgr.show_ui('ArmRaceScoreDetailsUI', 'logic.comsys.battle.ArmRace')

    def init_event(self):
        emgr = global_data.emgr
        econf = {'update_battle_timestamp': self.update_timestamp,
           'update_group_score_data': self.update_group_score_data,
           'scene_observed_player_setted_event': self.update_observed_player
           }
        emgr.bind_events(econf)

    def update_timestamp(self, *args):
        self.on_count_down()

    def update_observed_player(self, ltarget):
        self.player = ltarget
        if global_data.armrace_battle_data:
            self.update_group_score_data(global_data.armrace_battle_data.get_group_score_data())

    def update_group_score_data(self, data):
        if not data:
            return
        if self.player:
            player = self.player
        else:
            if global_data.player:
                player = global_data.player.logic
            if not player:
                return
        role_data = {}
        cur_count = len(data)
        last_count = self.panel.list_score.GetItemCount()
        self.panel.list_score.SetInitCount(cur_count)
        my_group_id = player.ev_g_group_id()
        max_level = self.max_level
        first_point_num = 0
        for index, widget in enumerate(self.panel.list_score.GetAllItem()):
            rank, group_id, point, role_id, kill_num, is_die, has_buff, now_level_kill = data[index]
            role_data[group_id] = (point, now_level_kill)
            if point == max_level:
                first_point_num += 1
            if point > max_level:
                widget.lab_level.SetString('LV.Max')
            else:
                widget.lab_level.SetString(get_text_by_id(17249).format(point))
            if index % 2:
                widget.nd_kill_even.lab_kill.SetString(str(kill_num))
            else:
                widget.nd_kill_odd.lab_kill.SetString(str(kill_num))
            if now_level_kill == 1:
                widget.progress_head.SetPercent(50)
            else:
                widget.progress_head.SetPercent(0)
            widget.img_self.setVisible(my_group_id == group_id)
            widget.img_arrow.setVisible(my_group_id == group_id)
            widget.img_die.setVisible(is_die)
            widget.nd_1st.setVisible(rank == 1)
            photo_no = get_role_default_photo(role_id[0])
            avatar_icon_path = get_head_photo_res_path(photo_no)
            widget.temp_head.img_head.SetDisplayFrameByPath('', avatar_icon_path)

            @widget.temp_head.unique_callback()
            def OnClick(btn, touch):
                self.toggle_score_details()

            widget.nd_buff.setVisible(has_buff)
            if rank == 1 and point == max_level and not self.first_point_10:
                widget.PlayAnimation('show_10point')
                self.first_point_10 = True
            last_point, last_level_kill = (0, 0)
            if self.role_data and group_id in self.role_data:
                last_point, last_level_kill = self.role_data[group_id][0], self.role_data[group_id][1]
            if point > max_level:
                widget.img_max.setVisible(True)
                widget.lab_max.SetString('LV.Max')
            elif point == max_level:
                widget.img_max.setVisible(True)
                widget.lab_max.SetString(get_text_by_id(17249).format(max_level))
            elif (last_level_kill == 0 or point != last_point) and now_level_kill == 1:
                widget.PlayAnimation('show_half')
            elif (last_level_kill == 1 or point != last_point) and now_level_kill == 0:
                widget.PlayAnimation('disappear')
                if point == max_level:
                    widget.img_max.setVisible(True)
                    widget.lab_max.SetString(get_text_by_id(17249).format(max_level))
                    widget.PlayAnimation('show_full_max')

        self.role_data = role_data
        if first_point_num and first_point_num > self.last_point_off:
            global_data.emgr.battle_event_message.emit(first_point_num, message_type=battle_const.UP_NODE_ARMRACE_UZI)
        self.last_point_off = first_point_num
        if cur_count != last_count:
            w, h = self.nd_score.GetContentSize()
            self.nd_score.SetContentSize(self.ITEM_WIDTH * cur_count, h)
            self.nd_score.ResizeAndPosition(include_self=False)

    def on_count_down(self):
        revive_time = BattleUtils.get_battle_left_time()

        def refresh_time(pass_time):
            left_time = revive_time - pass_time
            if left_time <= 30 and not self.left_30_seconds:
                msg = {'i_type': battle_const.ARMRACE_LEFT_TIME}
                global_data.emgr.show_battle_main_message.emit(msg, battle_const.MAIN_NODE_COMMON_INFO)
                self.left_30_seconds = True
            if left_time <= 10 and not self.left_10_seconds:
                ui = global_data.ui_mgr.show_ui('ArmRaceFinishCountDown', 'logic.comsys.battle.ArmRace')
                ui.on_delay_close(left_time)
                global_data.emgr.left_ten_second_event.emit()
                self.left_10_seconds = True
            left_time = int(math.ceil(left_time))
            left_time = tutil.get_delta_time_str(left_time)[3:]
            self.panel.lab_time.SetString(left_time)

        def refresh_time_finsh():
            left_time = tutil.get_delta_time_str(1)[3:]
            self.panel.lab_time.SetString(left_time)

        self.panel.lab_time.StopTimerAction()
        refresh_time(0)
        self.panel.lab_time.TimerAction(refresh_time, revive_time, callback=refresh_time_finsh, interval=1)