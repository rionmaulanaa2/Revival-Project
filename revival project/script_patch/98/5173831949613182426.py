# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/Settle/GVGEndUI.py
from __future__ import absolute_import
import six
from logic.gcommon.ctypes.BattleReward import BattleReward
from logic.comsys.battle.Death.DeathEndUI import DeathEndUI

class GVGEndUI(DeathEndUI):

    def begin_show(self, settle_dict, finish_cb):
        self.finish_cb = finish_cb
        self._old_lv = settle_dict.get('lv')
        self._old_exp = settle_dict.get('exp')
        battle_reward = BattleReward()
        battle_reward.init_from_dict(settle_dict.get('reward', {}))
        self._add_exp = battle_reward.exp
        self_group_id = global_data.player.logic.ev_g_group_id()
        group_dict = settle_dict.get('group_points_dict')
        self_score = group_dict.get(str(self_group_id), 0)
        other_score = 0
        for g_id in six.iterkeys(group_dict):
            if g_id != str(self_group_id):
                other_score = group_dict[g_id]

        self.panel.nd_score.lab_score_blue.SetString(str(self_score))
        self.panel.nd_score.lab_score_red.SetString(str(other_score))
        score_anim = 'score'
        if settle_dict.get('is_draw', False):
            anim = 'deuce'
            sound_name = 'bt_draw'
        elif settle_dict.get('rank', 2) == 1:
            if settle_dict.get('is_lore', False):
                anim = 'knockout'
                sound_name = 'bt_godlike'
            else:
                anim = 'win'
                sound_name = 'bt_victory'
        else:
            anim = 'defeat'
            score_anim = 'defeat_score'
            sound_name = 'bt_failure'
        global_data.sound_mgr.play_ui_sound(sound_name)
        self.panel.PlayAnimation(anim)
        self.panel.PlayAnimation('end')
        self.show_score_timer = global_data.game_mgr.register_logic_timer(self.show_score, interval=28, times=1, args=(
         score_anim,))