# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/Train/TrainObserveEndUI.py
from __future__ import absolute_import
import six
from logic.comsys.observe_ui.DeathObserveEndUI import DeathObserveEndUI
from logic.gcommon.common_const.battle_const import BATTLE_SETTLE_REASON_NORMAL, BATTLE_SETTLE_REASON_OTHER_GROUP_QUIT, ADCRYSTAL_LORE_TIME_DIFF, ADCRYSTAL_LORE_DAMAGE_DIFF
import math
from logic.gcommon import time_utility as tutil

class TrainObserveEndUI(DeathObserveEndUI):

    def cal_result_display_para(self, settle_dict):
        self_group_id = global_data.player.logic.ev_g_group_id()
        group_dict = settle_dict.get('group_points')
        self_score = group_dict.get(str(self_group_id), 0)
        other_score = 0
        for g_id in six.iterkeys(group_dict):
            if g_id != str(self_group_id):
                other_score = group_dict[g_id]

        score_anim = 'score'
        round_res_time = settle_dict.get('round_res_time', {})
        if global_data.battle and global_data.battle.get_atk_group_id() == self_group_id:
            self_left_time = round_res_time.get('1', 0)
            other_left_time = round_res_time.get('0', 0)
        else:
            self_left_time = round_res_time.get('0', 0)
            other_left_time = round_res_time.get('1', 0)
        if self_left_time == 0 and other_left_time == 0 and self_score > other_score and self_score - other_score < 50:
            anim = 'knockout'
            sound_name = 'bt_godlike'
        elif self_score > other_score or self_score == other_score and self_left_time > other_left_time:
            anim = 'win'
            sound_name = 'bt_victory'
        elif self_score < other_score or self_score == other_score and self_left_time > other_left_time:
            anim = 'defeat'
            score_anim = 'defeat_score'
            sound_name = 'bt_failure'
        elif self_score == other_score and other_left_time == self_left_time:
            anim = 'deuce'
            sound_name = 'bt_draw'
        else:
            anim = 'defeat'
            score_anim = 'defeat_score'
            sound_name = 'bt_failure'
        return (
         anim, score_anim, sound_name)

    def begin_show(self, settle_dict):
        self_group_id = global_data.player.logic.ev_g_group_id()
        group_dict = settle_dict.get('group_points', {})
        round_res_time = settle_dict.get('round_res_time', {})
        self_score = group_dict.get(str(self_group_id), -1)
        other_score = -1
        for g_id in six.iterkeys(group_dict):
            if g_id != str(self_group_id):
                other_score = group_dict[g_id]

        if global_data.battle and global_data.battle.get_atk_group_id() == self_group_id:
            self_left_time = round_res_time.get('1', 0)
            other_left_time = round_res_time.get('0', 0)
        else:
            self_left_time = round_res_time.get('0', 0)
            other_left_time = round_res_time.get('1', 0)
        max_score = global_data.train_battle_mgr.get_mode_max_length()
        self_score = int(self_score / float(max_score) * 100.0)
        other_score = int(other_score / float(max_score) * 100.0)
        self.panel.nd_score.lab_score_blue.SetString('{}%'.format(self_score))
        self.panel.nd_score.lab_score_red.SetString('{}%'.format(other_score))
        self_left_time = tutil.get_delta_time_str(int(self_left_time))[3:]
        other_left_time = tutil.get_delta_time_str(int(other_left_time))[3:]
        self.panel.lab_time_blue.SetString(str(self_left_time))
        self.panel.lab_time_red.SetString(str(other_left_time))
        anim, score_anim, sound_name = self.cal_result_display_para(settle_dict)
        global_data.sound_mgr.play_ui_sound(sound_name)
        self.panel.PlayAnimation(anim)
        self.panel.PlayAnimation('end')
        self.show_score_timer = global_data.game_mgr.register_logic_timer(self.show_score, interval=28, times=1, args=(score_anim,))

    def show_score(self, score_anim):
        super(TrainObserveEndUI, self).show_score(score_anim)
        self.panel.PlayAnimation('show_push_train_data')

    def get_other_group_value(self, self_group_id, group_dict, default_val=0):
        for group_id in six.iterkeys(group_dict):
            if group_id != self_group_id:
                return group_dict[group_id]

        return default_val