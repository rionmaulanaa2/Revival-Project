# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/NewbieMechaTipsUI.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
from common.const.uiconst import DIALOG_LAYER_ZORDER_1, UI_TYPE_MESSAGE, UI_VKB_NO_EFFECT
from logic.vscene.parts.gamemode.GMDecorator import execute_by_mode
from logic.client.const import game_mode_const
import cc

class NewbieMechaTipsUI(BasePanel):
    PANEL_CONFIG_NAME = 'guide/guide_new_player'
    DLG_ZORDER = DIALOG_LAYER_ZORDER_1
    UI_VKB_TYPE = UI_VKB_NO_EFFECT

    def on_init_panel(self, *args, **kwargs):
        self.panel.temp_new_player_tips.setVisible(False)
        self.panel.temp_speedup.setVisible(False)
        self.panel.RecordAnimationNodeState('speed_new')
        self.showed_newbie_mecha_tips = global_data.achi_mgr.get_cur_user_archive_data('showed_newbie_mecha_tips', default=0)

    def on_finalize_panel(self):
        global_data.achi_mgr.set_cur_user_archive_data('showed_newbie_mecha_tips', 0)

    @execute_by_mode(True, (game_mode_const.GAME_MODE_SURVIVALS,))
    def show_newbie_mecha_tips(self, player_id):
        if not global_data.player or not global_data.player.logic:
            return
        else:
            if global_data.player.logic.ev_g_spectate_target():
                return
            if self.showed_newbie_mecha_tips == 1:
                return
            if player_id is None:
                return
            if global_data.player.id == player_id:
                self.show_first_call_speedup_tip()
                global_data.achi_mgr.set_cur_user_archive_data('showed_newbie_mecha_tips', 1)
                self.showed_newbie_mecha_tips = 1
            elif global_data.player.get_total_cnt() != 0:
                self.show_teammate_speedup_tip()
                global_data.achi_mgr.set_cur_user_archive_data('showed_newbie_mecha_tips', 1)
                self.showed_newbie_mecha_tips = 1
            return

    def show_first_call_speedup_tip(self):
        self.panel.temp_new_player_tips.lab_tips.SetString(5160)
        self.panel.temp_new_player_tips.setVisible(True)
        self.process_speed_new_anim(True)
        self.panel.runAction(cc.Sequence.create([
         cc.DelayTime.create(5),
         cc.CallFunc.create(lambda : self.panel.temp_new_player_tips.lab_tips.SetString(5161)),
         cc.DelayTime.create(5),
         cc.CallFunc.create(lambda : self.panel.temp_new_player_tips.setVisible(False))]))

    def process_speed_new_anim(self, show=False):
        mecha_ui = global_data.ui_mgr.get_ui('MechaUI')
        if not mecha_ui:
            return
        if show:
            mecha_ui.show_speed_new_anim()
        else:
            mecha_ui.stop_speed_new_anim()

    def show_teammate_speedup_tip(self):
        self.panel.temp_speedup.setVisible(True)
        self.panel.temp_speedup.SetTimeOut(5.0, lambda : self.panel.temp_speedup.setVisible(False))