# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/ADCrystal/ADCrystalEndStatisticsUI.py
from __future__ import absolute_import
from logic.comsys.battle.Crystal.CrystalEndStatisticsUI import CrystalEndStatisticsUI
from logic.gcommon.common_const.battle_const import BATTLE_SETTLE_REASON_NORMAL, BATTLE_SETTLE_REASON_OTHER_GROUP_QUIT, ADCRYSTAL_LORE_DAMAGE_DIFF, ADCRYSTAL_LORE_TIME_DIFF
import math
from logic.gcommon import time_utility as tutil

class ADCrystalEndStatisticsUI(CrystalEndStatisticsUI):
    PANEL_CONFIG_NAME = 'end/end_statistics_crystal2'

    def init_is_win_ending(self, settle_dict):
        self.draw_ending = settle_dict.get('is_draw', False)
        reason = settle_dict.get('settle_reason', BATTLE_SETTLE_REASON_NORMAL)
        extra_detail = settle_dict.get('extra_detail', {})
        crystal_point_dict = extra_detail.get('group_crystal_point_dict', {})
        crystal_damage_dict = extra_detail.get('group_crystal_damage_dict', {})
        crystal_time_dict = extra_detail.get('group_left_time_dict', {})
        early_settle_flag = extra_detail.get('early_settle_flag')
        self_group_id = self._get_self_group_id()
        self_point = crystal_point_dict.get(str(self_group_id), 0)
        other_point = self.get_other_group_value(str(self_group_id), crystal_point_dict, 0)
        self_damage = crystal_damage_dict.get(str(self_group_id), 0)
        other_damage = self.get_other_group_value(str(self_group_id), crystal_damage_dict, 0)
        self_time = crystal_time_dict.get(str(self_group_id), 0)
        other_time = self.get_other_group_value(str(self_group_id), crystal_time_dict, 0)
        other_quit = reason == BATTLE_SETTLE_REASON_OTHER_GROUP_QUIT
        bigger_point = self_point > other_point
        equal_point = self_point == other_point
        bigger_damage = self_point == 0 and equal_point and self_damage > other_damage
        bigger_time = self_point > 0 and equal_point and self_time > other_time
        self.win_ending = not self.draw_ending and (other_quit or bigger_point or bigger_damage or bigger_time)
        equal_point = self_point == other_point
        if not self.win_ending or not equal_point or early_settle_flag:
            self.knock_down_ending = False
        elif self_point > 0:
            self.knock_down_ending = 1 < self_time - other_time < ADCRYSTAL_LORE_TIME_DIFF
        else:
            self.knock_down_ending = 1 < self_damage - other_damage < ADCRYSTAL_LORE_DAMAGE_DIFF

    def init_game_result(self):
        settle_dict = self._settle_dict
        extra_detail = settle_dict.get('extra_detail', {})
        crystal_hp_percent_dict = extra_detail.get('group_crystal_hp_percent', {})
        crystal_time_dict = extra_detail.get('group_left_time_dict', {})
        self_group_id = self._get_self_group_id()
        self_hp = crystal_hp_percent_dict.get(str(self_group_id), 0)
        other_hp = self.get_other_group_value(str(self_group_id), crystal_hp_percent_dict, 0)
        self_hp = int(min(math.ceil(100.0 * self_hp), 100))
        other_hp = int(min(math.ceil(100.0 * other_hp), 100))
        self_hp = '{}%'.format(self_hp)
        other_hp = '{}%'.format(other_hp)
        self_time = crystal_time_dict.get(str(self_group_id), 0)
        other_time = self.get_other_group_value(str(self_group_id), crystal_time_dict, 0)
        self_time = tutil.get_delta_time_str(int(self_time))[3:]
        other_time = tutil.get_delta_time_str(int(other_time))[3:]
        self.panel.lab_score_blue.SetString(self_hp)
        self.panel.lab_score_red.SetString(other_hp)
        self.panel.lab_time_blue.SetString(self_time)
        self.panel.lab_time_red.SetString(other_time)
        if self.win_ending:
            if self.knock_down_ending:
                self.panel.nd_score.img_result.SetDisplayFrameByPath('', 'gui/ui_res_2/txt_pic/text_pic_en/txt_tdm_konckout.png')
            else:
                self.panel.nd_score.img_result.SetDisplayFrameByPath('', 'gui/ui_res_2/txt_pic/text_pic_en/txt_tdm_win.png')
        elif self.draw_ending:
            self.panel.nd_score.img_result.SetDisplayFrameByPath('', 'gui/ui_res_2/txt_pic/text_pic_en/txt_tdm_deuce.png')
        else:
            self.panel.nd_score.img_result.SetDisplayFrameByPath('', 'gui/ui_res_2/txt_pic/text_pic_en/txt_tdm_fail.png')