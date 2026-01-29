# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/gvg/GVGJudgeResultUI.py
from __future__ import absolute_import
from common.const.uiconst import NORMAL_LAYER_ZORDER
from common.uisys.basepanel import BasePanel
from common.const import uiconst
import time

class GVGJudgeResultUI(BasePanel):
    PANEL_CONFIG_NAME = 'battle_gvg/gvg_loading'
    IS_FULLSCREEN = True
    DLG_ZORDER = NORMAL_LAYER_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT

    def on_init_panel(self, *args, **kwargs):
        self.bg_ui = None
        self._end_callback = None
        self._show_time = time.time() + 1000

        @self.panel.callback()
        def OnClick(btn, touch):
            if time.time() - self._show_time > 0.5:
                self.close()

        return

    def begin_result_show(self):
        self._show_time = time.time()
        from logic.comsys.battle.gvg.GVGLoadingUI import GVGLoadingUI
        self.bg_ui = GVGLoadingUI(self.panel)
        self.bg_ui.on_init_panel()
        self.panel.img_mecha_bar_player.setScale(0)
        self.panel.img_bar_enemy_1.img_mecha_bar_1.img_mecha_bar_other.setScale(0)
        self.panel.img_bar_teamate.img_mecha_bar_3.img_mecha_bar_other.setScale(0)
        self.panel.img_bar_enemy_2.img_mecha_bar_1.img_mecha_bar_other.setScale(0)
        self.panel.img_bar_player.img_loading_bar.setScale(0)
        self.panel.img_bar_enemy_1.img_loading_bar.setScale(0)
        self.panel.img_bar_teamate.img_loading_bar.setScale(0)
        self.panel.img_bar_enemy_2.img_loading_bar.setScale(0)

    def set_settle_dict(self, settle_dict):
        win_ending = settle_dict.get('rank', 2) == 1
        draw_ending = settle_dict.get('is_draw', False)
        if not (global_data.battle and global_data.battle.is_friend_group(global_data.battle.observed_target_id)):
            win_ending = not win_ending
        if draw_ending:
            self.panel.nd_blue_vorf.img_win.setVisible(True)
            self.panel.nd_red_vorf.img_win.setVisible(True)
            self.panel.nd_blue_vorf.img_fail.setVisible(False)
            self.panel.nd_red_vorf.img_fail.setVisible(False)
        elif win_ending:
            self.panel.nd_blue_vorf.img_win.setVisible(True)
            self.panel.nd_red_vorf.img_win.setVisible(False)
            self.panel.nd_blue_vorf.img_fail.setVisible(False)
            self.panel.nd_red_vorf.img_fail.setVisible(True)
        else:
            self.panel.nd_blue_vorf.img_win.setVisible(False)
            self.panel.nd_red_vorf.img_win.setVisible(True)
            self.panel.nd_blue_vorf.img_fail.setVisible(True)
            self.panel.nd_red_vorf.img_fail.setVisible(False)

    def set_end_callback(self, callback):
        self._end_callback = callback

    def on_finalize_panel(self):
        if self._end_callback:
            self._end_callback()
        if self.bg_ui:
            self.bg_ui = None
        return