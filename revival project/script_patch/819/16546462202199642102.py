# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/BattleInfo/BattleRightTopUIPC.py
from __future__ import absolute_import
from .BattleRightTopUI import BattleRightTopBaseUI
from logic.comsys.battle.BattleInfo.CommunicateWidget import CommunicateWidgetPC
from logic.client.const import game_mode_const
from logic.vscene.parts.gamemode.GMDecorator import execute_by_mode
from logic.gcommon.cdata.round_competition import check_is_in_competition_battle

class BattleRightTopUIPC(BattleRightTopBaseUI):
    PANEL_CONFIG_NAME = 'battle/fight_right_top_pc'
    UI_ACTION_EVENT = {'btn_observed.OnClick': 'on_click_observed_btn',
       'btn_report.OnClick': 'on_click_report_btn'
       }
    HOT_KEY_FUNC_MAP_SHOW = {'switch_mic': {'node': 'btn_speak.temp_pc'},'switch_speaker': {'node': 'btn_sound.temp_pc'},'show_spectate_info': {'node': 'btn_observed.temp_pc'}}

    def on_init_panel(self, *args, **kwargs):
        super(BattleRightTopUIPC, self).on_init_panel()
        self.init_observe_widget()
        self.modify_btn_report()

    def init_observe_widget(self):
        if self.panel.nd_observed_details:
            self.panel.nd_observed_details.setVisible(False)

    def on_click_observed_btn(self, *args):
        nd_detail = self.panel.nd_observed_details
        nd_detail.setVisible(not nd_detail.isVisible())

    def exercise_field_modify(self):
        mode_type = global_data.game_mode.get_mode_type()
        if mode_type == game_mode_const.GAME_MODE_EXERCISE:
            self.panel.btn_observed.setVisible(False)

    def ob_modify(self):
        if self.is_ob():
            self.panel.btn_speak.setVisible(False)
            self.panel.btn_sound.setVisible(False)
            self.panel.btn_observed.setVisible(False)
            self.panel.btn_report.setVisible(False)

    def init_communicate_widget(self):
        self.communicate_widget = CommunicateWidgetPC(self.panel)

    def leave_screen(self):
        super(BattleRightTopUIPC, self).leave_screen()
        global_data.ui_mgr.close_ui('BattleRightTopUIPC')

    @execute_by_mode(True, (game_mode_const.GAME_MODE_EXERCISE,))
    def modify_panel_position(self, in_mecha=False):
        pass

    def modify_btn_report(self):
        is_in_global_spectate = global_data.player.is_in_global_spectate() if global_data.player else True
        if check_is_in_competition_battle() and not is_in_global_spectate:
            self.panel.btn_report.setVisible(True)
        else:
            self.panel.btn_report.setVisible(False)

    def on_click_report_btn(self, *args):
        from logic.gcommon.common_const.log_const import REPORT_FROM_TYPE_COMPETITION, REPORT_CLASS_BATTLE
        if check_is_in_competition_battle():
            ui = global_data.ui_mgr.show_ui('RoundCompetitionReportUI', 'logic.comsys.report')
            ui.report_battle_users([], False, False)
            ui.request_report_name_list()
            ui.set_report_class(REPORT_CLASS_BATTLE)
            ui.set_extra_report_info('', '', REPORT_FROM_TYPE_COMPETITION)