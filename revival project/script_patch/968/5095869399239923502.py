# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/mecha_ui/MechaExecute.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
from common.const.uiconst import UI_TYPE_MESSAGE
EXCEPT_HIDE_UI_LIST = [
 'MechaHpInfoUI', 'HpInfoUI']
from common.const import uiconst

class MechaExecute(BasePanel):
    PANEL_CONFIG_NAME = 'battle_mech/mech_ending_empty'
    DLG_ZORDER = UI_TYPE_MESSAGE - 1
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    IS_FULLSCREEN = True
    UI_ACTION_EVENT = {}

    def on_init_panel(self):
        self.panel.setLocalZOrder(self.DLG_ZORDER)
        self.init_parameters()
        self.hide_main_ui(exceptions=EXCEPT_HIDE_UI_LIST, exception_types=(UI_TYPE_MESSAGE,))
        self.panel.PlayAnimation('in')
        self.disappearing = False

    def on_finalize_panel(self):
        self.show_main_ui()
        self.player = None
        return

    def init_parameters(self):
        emgr = global_data.emgr
        if global_data.player:
            self.on_player_setted(global_data.player.logic)
        emgr.scene_player_setted_event += self.on_player_setted
        econf = {}
        emgr.bind_events(econf)

    def on_player_setted(self, player):
        if not player:
            self.close()

    def disappear(self):
        self.panel.PlayAnimation('out')
        delay = self.panel.GetAnimationMaxRunTime('out')
        self.panel.SetTimeOut(delay, lambda : self.close())
        self.disappearing = True