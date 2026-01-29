# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/Train/TrainTransitionUI.py
from __future__ import absolute_import
from logic.comsys.battle.BattleTransitionUI import BattleTransitionUI
from logic.gcommon import time_utility

class TrainTransitionUI(BattleTransitionUI):
    PANEL_CONFIG_NAME = 'battle_push_train/battle_push_train_round_end'

    def init_score_widget(self):
        if not global_data.battle:
            return
        max_length = global_data.train_battle_mgr.get_mode_max_length()
        old_atk_group_id = global_data.battle.get_old_atk_group_id()
        old_def_group_id = global_data.battle.get_old_def_group_id()
        my_group_id = global_data.battle.get_my_group_id()
        last_round_left_time = global_data.battle.get_last_round_left_time()
        last_round_dis = global_data.battle.get_last_round_dis()
        left_time = time_utility.get_delta_time_str(int(last_round_left_time))[3:]
        last_dis_percent = last_round_dis / float(max_length) * 100
        if last_dis_percent < 1:
            last_dis_percent = 0
        elif last_dis_percent > 99.5:
            last_dis_percent = 100
        else:
            last_dis_percent = int(last_dis_percent)
        if old_atk_group_id == my_group_id:
            self.panel.nd_blue.lab_distance.SetString('{}%'.format(last_dis_percent))
            self.panel.nd_blue.lab_time.SetString(str(left_time))
            self.panel.nd_red.bar_red.lab_distance.SetString('0%')
            self.panel.nd_red.bar_red.lab_time.SetString('05:00')
        else:
            self.panel.nd_red.bar_red.lab_distance.SetString('{}%'.format(last_dis_percent))
            self.panel.nd_red.bar_red.lab_time.SetString(str(left_time))
            self.panel.nd_blue.lab_distance.SetString('0%')
            self.panel.nd_blue.lab_time.SetString('05:00')
        self.panel.lab_round.SetString(get_text_by_id(17495).format(1))