# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/mecha_ui/MechaWarningUI.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
from common.const.uiconst import UI_TYPE_MESSAGE
EXCEPT_HIDE_UI_LIST = [
 'MechaHpInfoUI', 'HpInfoUI', 'MoveRockerTouchUI', 'MoveRockerUI', 'PVETipsUI']
from common.const import uiconst

class MechaWarningUI(BasePanel):
    PANEL_CONFIG_NAME = 'battle_mech/mech_warn_break'
    DLG_ZORDER = UI_TYPE_MESSAGE - 1
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    IS_FULLSCREEN = True
    UI_ACTION_EVENT = {}

    def on_init_panel(self):
        self.panel.setLocalZOrder(self.DLG_ZORDER)
        self.init_parameters()
        self.disappearing = False

    def finished(self):
        self.leave_screen()

    def enter_screen(self):
        super(MechaWarningUI, self).enter_screen()
        cam_lplayer = global_data.cam_lplayer
        if cam_lplayer and (cam_lplayer.ev_g_is_pure_mecha() or cam_lplayer.ev_g_is_hunter_mecha()):
            txt_id = 862025
        else:
            txt_id = 80192
        self.panel.lab_1.SetString(txt_id)
        self.panel.SetTimeOut(1.2, self.finished)
        self.panel.PlayAnimation('break')
        self.hide_main_ui(exceptions=EXCEPT_HIDE_UI_LIST, exception_types=(UI_TYPE_MESSAGE,))
        global_data.emgr.set_move_rocker_opacity_event.emit(0)

    def leave_screen(self):
        super(MechaWarningUI, self).leave_screen()
        self.show_main_ui()
        self.panel.lab_1.SetString('')
        global_data.emgr.set_move_rocker_opacity_event.emit(255)

    def on_finalize_panel(self):
        self.show_main_ui()

    def init_parameters(self):
        emgr = global_data.emgr
        if global_data.player:
            self.on_player_setted(global_data.player.logic)
        emgr.scene_player_setted_event += self.on_player_setted
        econf = {}
        emgr.bind_events(econf)

    def on_player_setted(self, player):
        if not player:
            self.leave_screen()