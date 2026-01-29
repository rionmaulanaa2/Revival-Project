# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/Crystal/CrystalEndUI.py
from __future__ import absolute_import
import six
from logic.comsys.battle.Death.DeathEndUI import DeathEndUI
from logic.gcommon.ctypes.BattleReward import BattleReward
from logic.gcommon.common_const.battle_const import BATTLE_SETTLE_REASON_NORMAL, BATTLE_SETTLE_REASON_OTHER_GROUP_QUIT
import math
from logic.gutils.template_utils import init_crystal_icon_list
from logic.gcommon.common_const.battle_const import CRYSTAL_LORE_DAMAGE

class CrystalEndUI(DeathEndUI):

    def begin_show(self, settle_dict, finish_cb):
        self.finish_cb = finish_cb
        self._old_lv = settle_dict.get('lv')
        self._old_exp = settle_dict.get('exp')
        battle_reward = BattleReward()
        battle_reward.init_from_dict(settle_dict.get('reward', {}))
        self._add_exp = battle_reward.exp
        self_group_id = global_data.player.logic.ev_g_group_id()
        extra_detail = settle_dict.get('extra_detail', {})
        crystal_point_dict = extra_detail.get('group_crystal_point_dict')
        crystal_damage_dict = extra_detail.get('group_crystal_damage_dict')
        crystal_hp_percent_dict = extra_detail.get('group_crystal_hp_percent', {})
        self_group_crystal_point = crystal_point_dict.get(str(self_group_id), 0)
        other_group_crystal_point = self.get_other_group_value(str(self_group_id), crystal_point_dict, 0)
        self_group_crystal_damage = crystal_damage_dict.get(str(self_group_id), 0)
        other_group_crystal_damage = self.get_other_group_value(str(self_group_id), crystal_damage_dict, 0)
        self_crystal_hp_percent = crystal_hp_percent_dict.get(str(self_group_id), 0)
        other_crystal_hp_percent = self.get_other_group_value(str(self_group_id), crystal_hp_percent_dict, 0)
        init_crystal_icon_list(3, other_group_crystal_point, self.panel.list_icon_blue)
        init_crystal_icon_list(3, self_group_crystal_point, self.panel.list_icon_red)
        self_crystal_hp_percent = int(min(math.ceil(100.0 * self_crystal_hp_percent), 100))
        other_crystal_hp_percent = int(min(math.ceil(100.0 * other_crystal_hp_percent), 100))
        self.panel.nd_score.lab_score_blue.SetString('{}%'.format(self_crystal_hp_percent))
        self.panel.nd_score.lab_score_red.SetString('{}%'.format(other_crystal_hp_percent))
        reason = settle_dict.get('settle_reason', BATTLE_SETTLE_REASON_NORMAL)
        score_anim = 'score'
        if reason == BATTLE_SETTLE_REASON_OTHER_GROUP_QUIT:
            win_end = True
        elif self_group_crystal_point > other_group_crystal_point:
            win_end = True
        elif self_group_crystal_damage - other_group_crystal_damage >= 1:
            win_end = True
        else:
            win_end = False
        equal_crysal_point = self_group_crystal_point == other_group_crystal_point
        equal_damage = math.fabs(self_group_crystal_damage - other_group_crystal_damage) < 1
        draw_end = settle_dict.get('is_draw')
        if draw_end is None:
            draw_end = not win_end and equal_crysal_point and equal_damage
        knockout_end = 1 <= self_group_crystal_damage - other_group_crystal_damage < CRYSTAL_LORE_DAMAGE
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
        self.show_score_timer = global_data.game_mgr.register_logic_timer(self.show_score, interval=28, times=1, args=(score_anim,))
        return

    def show_score(self, score_anim):
        super(CrystalEndUI, self).show_score(score_anim)
        self.panel.PlayAnimation('show_crystal_icon')

    def get_other_group_value(self, self_group_id, group_dict, default_val=0):
        for group_id in six.iterkeys(group_dict):
            if group_id != self_group_id:
                return group_dict[group_id]

        return default_val