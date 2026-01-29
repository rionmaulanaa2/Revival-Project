# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/Improvise/ImproviseRoundSettleUI.py
from __future__ import absolute_import
import six
from six.moves import range
from common.const.uiconst import NORMAL_LAYER_ZORDER, UI_VKB_NO_EFFECT
from common.uisys.basepanel import BasePanel
from logic.comsys.battle.ffa.FFAFinishCountDownWidget import FFAFinishCountDownWidget
SETTLE_WIN = 1
SETTLE_DRAW = 2
SETTLE_LOSE = 3

class ImproviseRoundSettleUI(BasePanel):
    PANEL_CONFIG_NAME = 'battle_3v3/3v3_danju_end'
    DLG_ZORDER = NORMAL_LAYER_ZORDER
    UI_VKB_TYPE = UI_VKB_NO_EFFECT
    IS_FULLSCREEN = True
    UI_ACTION_EVENT = {'nd_touch_layer.OnClick': '_on_click_close'
       }

    def on_init_panel(self, settle_result, group_points_dict, self_group_id, delay_close_time=0.0, click_close_cb=None):
        delay_close_time = max(0.0, delay_close_time)
        self._self_group_id = self_group_id
        self._delay_close_time = delay_close_time
        self._click_close_cb = click_close_cb
        if delay_close_time > 0:

            def cb():
                self.close()

            self.panel.DelayCall(delay_close_time, cb)
            self.panel.nd_time.setVisible(True)
            self._widget = FFAFinishCountDownWidget(self.panel.nd_time)
            self._widget.on_init_panel()
            self._widget.on_delay_close(delay_close_time)
            self.panel.lab_score.setVisible(False)
        else:
            self.panel.nd_time.setVisible(False)
            self._widget = None
            self.panel.lab_score.setVisible(True)
        self._init_view()
        self._refresh_view(group_points_dict)
        score_anim = 'score'
        if settle_result == SETTLE_DRAW:
            anim = 'deuce'
            sound_name = 'bt_draw'
        elif settle_result == SETTLE_WIN:
            anim = 'win'
            sound_name = 'bt_victory'
        else:
            anim = 'defeat'
            score_anim = 'defeat_score'
            sound_name = 'bt_failure'
        global_data.sound_mgr.play_ui_sound(sound_name)
        self.panel.PlayAnimation(anim)
        self.panel.PlayAnimation('end')
        self.show_score_timer = global_data.game_mgr.register_logic_timer(self.show_score, interval=28, times=1, args=(score_anim,))
        return

    def on_finalize_panel(self):
        if self._widget:
            self._widget.on_finalize_panel()
        self._widget = None
        self.panel.stopAllActions()
        if self.show_score_timer:
            global_data.game_mgr.unregister_logic_timer(self.show_score_timer)
            self.show_score_timer = None
        return

    def _init_view(self):
        max_win = global_data.improvise_battle_data.get_max_win_round_cnt()
        self.panel.list_blue.SetInitCount(max_win)
        self.panel.list_red.SetInitCount(max_win)

    def _on_click_close(self, *args):
        if self._delay_close_time > 0:
            return
        if callable(self._click_close_cb):
            self._click_close_cb()
        self.close()

    def _refresh_view(self, group_points_dict):
        self_score = group_points_dict.get(self._self_group_id, 0)
        other_score = 0
        for g_id in six.iterkeys(group_points_dict):
            if g_id != self._self_group_id:
                other_score = group_points_dict[g_id]

        self.panel.lab_score_blue.SetString(str(self_score))
        self.panel.lab_score_red.SetString(str(other_score))
        lsts = (
         self.panel.list_blue, self.panel.list_red)
        scores = (self_score, other_score)
        for i, lst in enumerate(lsts):
            score = scores[i]
            for i in range(lst.GetItemCount()):
                item = lst.GetItem(i)
                item.img_win.setVisible(i + 1 <= score)

    def show_score(self, score_anim):
        self.show_score_timer = None
        if self and self.is_valid():
            self.panel.PlayAnimation(score_anim)
        return