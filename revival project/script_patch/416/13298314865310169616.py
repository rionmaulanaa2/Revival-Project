# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/observe_ui/BattleWinnersUI.py
from __future__ import absolute_import
from common.const import uiconst
from common.uisys.basepanel import BasePanel
from common.const.uiconst import NORMAL_LAYER_ZORDER

class BattleWinnersUI(BasePanel):
    PANEL_CONFIG_NAME = 'end/end_win_br'
    DLG_ZORDER = NORMAL_LAYER_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    UI_ACTION_EVENT = {'btn_exit.OnClick': 'on_click_exit_btn'
       }

    def on_init_panel(self, *args, **kwargs):
        self.hide_main_ui()
        self._exit_callback = None
        return

    def set_winner_names(self, winner_names, rank):
        self.panel.observe_win.setVisible(True)
        name = ', '.join(winner_names)
        self.panel.lab_observe_name.SetStringWithAdapt(name)
        if rank == 1:
            anim_name = 'appear_first_new'
            node = self.panel.nd_first if G_IS_NA_PROJECT else self.panel.nd_first_new
        elif rank == 2:
            anim_name = 'appear_second'
            node = self.panel.nd_second
        else:
            anim_name = 'appear_others'
            node = self.panel.nd_others
        self.panel.PlayAnimation('end')
        self.panel.PlayAnimation(anim_name)
        node.setVisible(True)
        if not G_IS_NA_PROJECT and rank <= 5:
            self.panel.PlayAnimation('victory_show')
        if rank > 2:
            self.panel.lab_rank.setVisible(True)
            self.panel.lab_rank.SetString(str(rank))
        else:
            self.panel.lab_rank.setVisible(False)

    def set_exit_callback(self, callback):
        self._exit_callback = callback

    def on_finalize_panel(self):
        self._exit_callback = None
        self.show_main_ui()
        return

    def on_click_exit_btn(self, *args):
        if self._exit_callback:
            self._exit_callback()
        elif global_data.player:
            global_data.player.quit_battle()
        self.close()