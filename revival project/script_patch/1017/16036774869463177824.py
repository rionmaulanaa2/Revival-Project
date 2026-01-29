# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/ffa/FFAScoreUI.py
from __future__ import absolute_import
from common.const.uiconst import SMALL_MAP_ZORDER
from common.uisys.basepanel import BasePanel
from logic.comsys.battle import BattleUtils
from logic.gcommon import time_utility as tutil
from logic.gcommon.common_const import battle_const
import math
RNAK_TXT = {1: 'st',2: 'nd',
   3: 'rd'
   }
from common.const import uiconst

class FFAScoreUI(BasePanel):
    PANEL_CONFIG_NAME = 'battle_ffa/battle_score_brief'
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
        self.play_data_cfg = global_data.game_mode.get_cfg_data('play_data')
        self.last_point_off = 0
        self.left_30_seconds = False
        self.left_10_seconds = False
        return

    def on_finalize_panel(self):
        self.panel.lab_time.StopTimerAction()
        global_data.ui_mgr.close_ui('FFAFinishCountDown')

    def init_panel(self):
        self.update_timestamp()
        if global_data.ffa_battle_data:
            self.update_group_score_data(global_data.ffa_battle_data.get_group_score_data())

    def toggle_score_details(self, *args):
        ui_inst = global_data.ui_mgr.get_ui('FFAScoreDetailsUI')
        if ui_inst:
            global_data.ui_mgr.close_ui('FFAScoreDetailsUI')
        else:
            global_data.ui_mgr.show_ui('FFAScoreDetailsUI', 'logic.comsys.battle.ffa')

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
        if global_data.ffa_battle_data:
            self.update_group_score_data(global_data.ffa_battle_data.get_group_score_data())

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
        cur_count = len(data)
        last_count = self.panel.list_score.GetItemCount()
        self.panel.list_score.SetInitCount(cur_count)
        my_group_id = player.ev_g_group_id()
        settle_point = self.play_data_cfg.get('settle_point')
        first_point = 0
        for index, widget in enumerate(self.panel.list_score.GetAllItem()):
            rank, group_id, point = data[index]
            if rank == 1:
                first_point = point
            widget.lab_rank.SetString(''.join([str(rank), RNAK_TXT.get(rank, 'th')]))
            widget.lab_score.SetString(str(point))
            widget.nd_self.setVisible(my_group_id == group_id)
            widget.nd_1st.setVisible(rank == 1)
            widget.lab_rank.setVisible(not rank == 1)
            widget.lab_rank.SetColor('#SS' if my_group_id == group_id else '#SW')
            widget.nd_cover.setVisible(not bool(index % 2))
            if rank == 1 and point == 10 and not self.first_point_10:
                widget.PlayAnimation('show_10point')
                self.first_point_10 = True

        point_off = settle_point - first_point
        if 0 < point_off <= 3 and self.last_point_off != point_off:
            msg = {'i_type': battle_const.FFA_COUNT_POINT,'show_num': point_off,'last_show_num': min(point_off + 1, 3),
               'set_num_func': 'set_show_normal_point_num'
               }
            global_data.emgr.show_battle_main_message.emit(msg, battle_const.MAIN_NODE_COMMON_INFO)
            self.last_point_off = point_off
        if cur_count != last_count:
            w, h = self.nd_score.GetContentSize()
            self.nd_score.SetContentSize(self.ITEM_WIDTH * cur_count, h)
            self.nd_score.ResizeAndPosition(include_self=False)

    def on_count_down(self):
        revive_time = BattleUtils.get_battle_left_time()

        def refresh_time(pass_time):
            left_time = revive_time - pass_time
            if left_time <= 30 and not self.left_30_seconds:
                msg = {'i_type': battle_const.BATTLE_LEFT_TIME}
                global_data.emgr.show_battle_main_message.emit(msg, battle_const.MAIN_NODE_COMMON_INFO)
                self.left_30_seconds = True
            if left_time <= 10 and not self.left_10_seconds:
                ui = global_data.ui_mgr.show_ui('FFAFinishCountDown', 'logic.comsys.battle.ffa')
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