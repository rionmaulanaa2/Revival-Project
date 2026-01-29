# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/Settle/EndAnimUI.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
from common.const.uiconst import NORMAL_LAYER_ZORDER_1
from logic.client.const import game_mode_const
import cc
from logic.gcommon.common_const import battle_const
from common.const import uiconst

class EndAnimUI(BasePanel):
    PANEL_CONFIG_NAME = 'end/end_win_br'
    DLG_ZORDER = NORMAL_LAYER_ZORDER_1
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT

    def on_init_panel(self, rank, on_animate_finished_cb=None, dead_reason=None):
        self.panel.nd_victory.setVisible(False)
        self._on_animate_finished_cb = on_animate_finished_cb

        def callback():
            if callable(self._on_animate_finished_cb):
                self._on_animate_finished_cb()

        if rank == 1:
            anim_name = 'appear_first_new'
            if global_data.game_mode.is_mode_type(game_mode_const.GAME_MODE_SURVIVALS):
                global_data.emgr.play_anchor_voice.emit('101_winner')
            sound_name = 'bt_victory'
        elif rank == 2:
            anim_name = 'appear_second'
            sound_name = 'bt_draw'
        else:
            anim_name = 'appear_others'
            sound_name = 'bt_failure'
            if not G_IS_NA_PROJECT and rank <= 5:
                sound_name = 'bt_draw'
            self.panel.lab_rank.SetString(str(rank))
        global_data.sound_mgr.play_ui_sound(sound_name)
        self.hide_main_ui(exceptions=('EndContinueUI', 'EndDeathReplayUI'))
        if rank <= 3:
            self.panel.img_rank_tails.SetDisplayFrameByPath('', 'gui/ui_res_2/fight_end/text_rd.png')
        else:
            self.panel.img_rank_tails.SetDisplayFrameByPath('', 'gui/ui_res_2/fight_end/text_th.png')
        if dead_reason is not None and dead_reason > 0 and dead_reason == battle_const.FIGHT_INJ_SIGNAL:
            self.panel.nd_signal.setVisible(True)
        else:
            self.panel.nd_signal.setVisible(False)
        action_list = []
        action_list.append(cc.CallFunc.create(lambda : self.panel.PlayAnimation(anim_name)))
        if not G_IS_NA_PROJECT and rank <= 5:
            self.panel.nd_victory.setVisible(True)
            action_list.append(cc.CallFunc.create(lambda : self.panel.PlayAnimation('victory_show')))
        action_list.append(cc.DelayTime.create(self.panel.GetAnimationMaxRunTime(anim_name)))
        action_list.append(cc.CallFunc.create(callback))
        self.panel.runAction(cc.Sequence.create(action_list))
        return

    def on_finalize_panel(self):
        self.show_main_ui()