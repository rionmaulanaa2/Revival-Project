# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/Death/DeathEndUI.py
from __future__ import absolute_import
import six
from common.const.uiconst import NORMAL_LAYER_ZORDER
from common.uisys.basepanel import BasePanel
from common.cfg import confmgr
from logic.gcommon.common_const.battle_const import BATTLE_SETTLE_REASON_NORMAL, BATTLE_SETTLE_REASON_OTHER_GROUP_QUIT, TDM_KNOCKOUT_LAST_POINT_MAX_INTERVAL, BATTLE_SETTLE_REASON_SURRENDER
from logic.gcommon.ctypes.BattleReward import BattleReward
from logic.gutils.lv_template_utils import get_lv_upgrade_need_exp
from common.const import uiconst

class DeathEndUI(BasePanel):
    PANEL_CONFIG_NAME = 'end/end_tdm'
    DLG_ZORDER = NORMAL_LAYER_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    UI_ACTION_EVENT = {'nd_touch_layer.OnClick': 'on_click_next'
       }

    def on_init_panel(self, settle_dict, finish_cb=None):
        self.show_score_timer = None
        if settle_dict is not None:
            self.begin_show(settle_dict, finish_cb)
        return

    def on_finalize_panel(self):
        self.panel.stopAllActions()
        if self.show_score_timer:
            global_data.game_mgr.unregister_logic_timer(self.show_score_timer)
            self.show_score_timer = None
        return

    def begin_show(self, settle_dict, finish_cb):
        self.finish_cb = finish_cb
        self._old_lv = settle_dict.get('lv')
        self._old_exp = settle_dict.get('exp')
        battle_reward = BattleReward()
        battle_reward.init_from_dict(settle_dict.get('reward', {}))
        self._add_exp = battle_reward.exp
        self_group_id = global_data.player.logic.ev_g_group_id()
        group_dict = settle_dict.get('group_points_dict', {})
        self_score = group_dict.get(str(self_group_id), 0)
        other_score = 0
        for g_id in six.iterkeys(group_dict):
            if g_id != str(self_group_id):
                other_score = group_dict[g_id]

        self.panel.nd_score.lab_score_blue.SetString(str(self_score))
        self.panel.nd_score.lab_score_red.SetString(str(other_score))
        anim, score_anim, sound_name = self.cal_result_display_para(settle_dict)
        global_data.sound_mgr.play_ui_sound(sound_name)
        self.panel.PlayAnimation(anim)
        self.panel.PlayAnimation('end')
        if score_anim:
            self.show_score_timer = global_data.game_mgr.register_logic_timer(self.show_score, interval=28, times=1, args=(score_anim,))

    def cal_result_display_para(self, settle_dict):
        self_group_id = global_data.player.logic.ev_g_group_id()
        group_dict = settle_dict.get('group_points_dict')
        self_score = group_dict.get(str(self_group_id), 0)
        other_score = 0
        for g_id in six.iterkeys(group_dict):
            if g_id != str(self_group_id):
                other_score = group_dict[g_id]

        last_point_got_interval = settle_dict.get('last_point_got_interval', TDM_KNOCKOUT_LAST_POINT_MAX_INTERVAL)
        reason = settle_dict.get('settle_reason', BATTLE_SETTLE_REASON_NORMAL)
        score_anim = 'score'
        if reason == BATTLE_SETTLE_REASON_SURRENDER:
            is_surrender = settle_dict.get('extra_detail', {}).get('is_surrender', False)
            if is_surrender:
                anim = 'defeat'
                score_anim = 'defeat_score'
                sound_name = 'bt_failure'
            else:
                anim = 'win'
                sound_name = 'bt_victory'
        elif self_score > other_score or reason == BATTLE_SETTLE_REASON_OTHER_GROUP_QUIT:
            if self_score - other_score == 1 and last_point_got_interval < TDM_KNOCKOUT_LAST_POINT_MAX_INTERVAL:
                anim = 'knockout'
                sound_name = 'bt_godlike'
            else:
                anim = 'win'
                sound_name = 'bt_victory'
        elif self_score == other_score:
            anim = 'deuce'
            sound_name = 'bt_draw'
        else:
            anim = 'defeat'
            score_anim = 'defeat_score'
            sound_name = 'bt_failure'
        return (anim, score_anim, sound_name)

    def show_score(self, score_anim):
        self.show_score_timer = None
        if score_anim and self and self.is_valid():
            self.panel.PlayAnimation(score_anim)
        return

    def on_click_next(self, *args):
        if self.finish_cb and callable(self.finish_cb):
            self.finish_cb()
        self.close()

    def show_details(self, *args):
        self.panel.temp_score_details.setVisible(True)

    def hide_details(self, *args):
        self.panel.temp_score_details.setVisible(False)

    def exit(self, *args):
        if global_data.player is not None:
            global_data.player.quit_battle(True)
        self.close()
        return