# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/observe_ui/DeathObserveEndUI.py
from __future__ import absolute_import
import six
from common.const.uiconst import NORMAL_LAYER_ZORDER
from common.uisys.basepanel import BasePanel
from common.cfg import confmgr
from logic.gcommon.common_const.battle_const import BATTLE_SETTLE_REASON_SURRENDER, BATTLE_SETTLE_REASON_NORMAL, BATTLE_SETTLE_REASON_OTHER_GROUP_QUIT, TDM_KNOCKOUT_LAST_POINT_MAX_INTERVAL
from common.const import uiconst

class DeathObserveEndUI(BasePanel):
    PANEL_CONFIG_NAME = 'end/end_tdm'
    DLG_ZORDER = NORMAL_LAYER_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    UI_ACTION_EVENT = {'nd_touch_layer.OnClick': 'on_click_next'
       }

    def on_init_panel(self):
        self.hide_main_ui()
        self.show_score_timer = None
        return

    def on_finalize_panel(self):
        self.show_main_ui()
        self.panel.stopAllActions()
        if self.show_score_timer:
            global_data.game_mgr.unregister_logic_timer(self.show_score_timer)
            self.show_score_timer = None
        return

    def begin_show(self, settle_dict):
        self_group_id = global_data.player.logic.ev_g_group_id()
        group_dict = settle_dict.get('group_points')
        self_score = group_dict.get(str(self_group_id), 0)
        other_score = 0
        last_point_got_interval = settle_dict.get('last_point_got_intv_dict', {}).get(str(self_group_id), TDM_KNOCKOUT_LAST_POINT_MAX_INTERVAL)
        for g_id in six.iterkeys(group_dict):
            if g_id != str(self_group_id):
                other_score = group_dict[g_id]

        self.panel.nd_score.lab_score_blue.SetString(str(self_score))
        self.panel.nd_score.lab_score_red.SetString(str(other_score))
        reason = settle_dict.get('settle_reason', BATTLE_SETTLE_REASON_NORMAL)
        score_anim = 'score'
        if reason == BATTLE_SETTLE_REASON_SURRENDER:
            is_surrender = self_group_id == settle_dict.get('surrender_group_id', None)
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
        global_data.sound_mgr.play_ui_sound(sound_name)
        self.panel.PlayAnimation(anim)
        self.panel.PlayAnimation('end')
        self.show_score_timer = global_data.game_mgr.register_logic_timer(self.show_score, interval=28, times=1, args=(score_anim,))
        return

    def show_score(self, score_anim):
        self.show_score_timer = None
        if self and self.is_valid():
            self.panel.PlayAnimation(score_anim)
        return

    def on_click_next(self, *args):
        self.exit()

    def exit(self, *args):
        if global_data.player is not None:
            global_data.player.quit_battle(True)
        self.close()
        return