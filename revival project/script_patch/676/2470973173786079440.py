# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/ADCrystal/ADCrystalEndUI.py
from __future__ import absolute_import
import six
from logic.comsys.battle.Death.DeathEndUI import DeathEndUI
from logic.gcommon.ctypes.BattleReward import BattleReward
from logic.gcommon.common_const.battle_const import BATTLE_SETTLE_REASON_NORMAL, BATTLE_SETTLE_REASON_OTHER_GROUP_QUIT, ADCRYSTAL_LORE_TIME_DIFF, ADCRYSTAL_LORE_DAMAGE_DIFF
import math
from logic.gcommon import time_utility as tutil

class ADCrystalEndUI(DeathEndUI):

    def begin_show(self, settle_dict, finish_cb):
        self.finish_cb = finish_cb
        self._old_lv = settle_dict.get('lv')
        self._old_exp = settle_dict.get('exp')
        battle_reward = BattleReward()
        battle_reward.init_from_dict(settle_dict.get('reward', {}))
        self._add_exp = battle_reward.exp
        draw_end = settle_dict.get('is_draw')
        self_group_id = global_data.player.logic.ev_g_group_id()
        extra_detail = settle_dict.get('extra_detail', {})
        crystal_time_dict = extra_detail.get('group_left_time_dict')
        crystal_damage_dict = extra_detail.get('group_crystal_damage_dict')
        crystal_hp_percent_dict = extra_detail.get('group_crystal_hp_percent', {})
        crystal_point_dict = extra_detail.get('group_crystal_point_dict', {})
        early_settle_flag = extra_detail.get('early_settle_flag')
        self_damage = crystal_damage_dict.get(str(self_group_id), 0)
        other_damage = self.get_other_group_value(str(self_group_id), crystal_damage_dict, 0)
        self_point = crystal_point_dict.get(str(self_group_id), 0)
        other_point = self.get_other_group_value(str(self_group_id), crystal_point_dict, 0)
        self_time = crystal_time_dict.get(str(self_group_id), 0)
        other_time = self.get_other_group_value(str(self_group_id), crystal_time_dict, 0)
        self_time_str = tutil.get_delta_time_str(int(self_time))[3:]
        other_time_str = tutil.get_delta_time_str(int(other_time))[3:]
        self.panel.nd_score.nd_crystal2.lab_time_blue.SetString(self_time_str)
        self.panel.nd_score.nd_crystal2.lab_time_red.SetString(other_time_str)
        self_hp_percent = crystal_hp_percent_dict.get(str(self_group_id), 0)
        other_hp_percent = self.get_other_group_value(str(self_group_id), crystal_hp_percent_dict, 0)
        self_hp_percent = int(min(math.ceil(100.0 * self_hp_percent), 100))
        other_hp_percent = int(min(math.ceil(100.0 * other_hp_percent), 100))
        self.panel.nd_score.lab_score_blue.SetString('{}%'.format(self_hp_percent))
        self.panel.nd_score.lab_score_red.SetString('{}%'.format(other_hp_percent))
        reason = settle_dict.get('settle_reason', BATTLE_SETTLE_REASON_NORMAL)
        score_anim = 'score'
        other_quit = reason == BATTLE_SETTLE_REASON_OTHER_GROUP_QUIT
        bigger_point = self_point > other_point
        equal_point = self_point == other_point
        bigger_damage = self_point == 0 and equal_point and self_damage > other_damage
        bigger_time = self_point > 0 and equal_point and self_time > other_time
        win_end = not draw_end and (other_quit or bigger_point or bigger_damage or bigger_time)
        if not win_end or not equal_point or early_settle_flag:
            knockout_end = False
        elif self_point > 0:
            knockout_end = 1 < other_time - self_time < ADCRYSTAL_LORE_TIME_DIFF
        else:
            knockout_end = 1 < self_damage - other_damage < ADCRYSTAL_LORE_DAMAGE_DIFF
        if win_end:
            if knockout_end:
                anim = 'knockout'
                sound_name = 'bt_godlike'
            else:
                anim = 'win'
                sound_name = 'bt_victory'
        elif draw_end:
            anim = 'deuce'
            sound_name = 'bt_draw'
        else:
            anim = 'defeat'
            score_anim = 'defeat_score'
            sound_name = 'bt_failure'
        global_data.sound_mgr.play_ui_sound(sound_name)
        self.panel.PlayAnimation(anim)
        self.panel.PlayAnimation('end')
        self.show_score_timer = global_data.game_mgr.register_logic_timer(self.show_score, interval=28, times=1, args=(
         score_anim,))

    def show_score(self, score_anim):
        super(ADCrystalEndUI, self).show_score(score_anim)
        self.panel.PlayAnimation('show_crystal_time')

    def get_other_group_value(self, self_group_id, group_dict, default_val=0):
        for group_id in six.iterkeys(group_dict):
            if group_id != self_group_id:
                return group_dict[group_id]

        return default_val