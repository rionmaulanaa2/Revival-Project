# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/BattleInfo/FightKillNumberUI.py
from __future__ import absolute_import
import six
from common.const.uiconst import BASE_LAYER_ZORDER_1
from logic.comsys.ui_distortor.MechaDistortHelper import MechaDistortHelper
from logic.vscene.parts.gamemode.GMDecorator import execute_by_mode
from logic.client.const import game_mode_const
from logic.gcommon.common_const import battle_const as bconst
from logic.comsys.battle.BattleInfoKill import BattleInfoKill
from logic.comsys.battle.SurviveInfoUI import SurviveInfoUIPC
from common.const import uiconst
from logic.comsys.battle.BattleInfo.SurviveWidget import SurviveWidget

class FightKillNumberUI(MechaDistortHelper, SurviveInfoUIPC):
    DLG_ZORDER = BASE_LAYER_ZORDER_1
    PANEL_CONFIG_NAME = 'battle/fight_kill_number_pc'
    NODE_MESSAGE = {bconst.MED_NODE_KILL_INFO: BattleInfoKill
       }
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT

    def on_init_panel(self, *args, **kwargs):
        super(FightKillNumberUI, self).on_init_panel()
        self.init_parameters()
        self.init_panel_event()
        self.cur_survive_num = None
        self._top_5_nd = None
        self.survive_widget = SurviveWidget(self.on_kill_human_num_change, self.on_kill_mecha_num_change, self.on_assist_mecha_num_change)
        self.adjust_ui()
        global_data.emgr.scene_camera_player_setted_event += self.on_camera_player_setted
        global_data.emgr.update_map_info_widget_event += self.update_alive_player_num
        if not G_IS_NA_PROJECT:
            global_data.emgr.update_alive_player_num_event += self._update_alive_player_num
        return

    def on_finalize_panel(self):
        super(FightKillNumberUI, self).on_finalize_panel()
        self.destroy_widget('survive_widget')
        global_data.emgr.scene_camera_player_setted_event += self.on_camera_player_setted
        global_data.emgr.update_map_info_widget_event -= self.update_alive_player_num
        if not G_IS_NA_PROJECT:
            global_data.emgr.update_alive_player_num_event -= self._update_alive_player_num

    def leave_screen(self):
        super(FightKillNumberUI, self).leave_screen()
        global_data.ui_mgr.close_ui('FightKillNumberUI')

    def do_hide_panel(self):
        super(FightKillNumberUI, self).do_hide_panel()

    def do_show_panel(self):
        super(FightKillNumberUI, self).do_show_panel()
        if global_data.battle:
            self.update_alive_player_num(getattr(global_data.battle, 'alive_player_num', 0))

    @execute_by_mode(False, game_mode_const.Hide_AlivePlayerNum)
    def update_alive_player_num(self, player_num):
        WARNING_ALIVE_NUM = 5
        WARNING_ALINE_NUM_BIG = 20
        if self.panel:
            if global_data.game_mode.is_mode_type(game_mode_const.GAME_MODE_SURVIVALS):
                survive_num_voice = {50: '101_remain_01',20: '101_remain_02',10: '101_remain_03',3: '101_remain_04',2: '101_remain_05'}
                for num, voice in six.iteritems(survive_num_voice):
                    if player_num == num and self.cur_survive_num and player_num < self.cur_survive_num:
                        global_data.emgr.play_anchor_voice.emit(voice)
                        break

            self.cur_survive_num = player_num
            self.panel.lab_survive.setString(str(player_num))
            if not global_data.player:
                return
            battle = global_data.player.get_battle()
            if battle and not battle.is_battle_prepare_stage():
                if player_num < WARNING_ALIVE_NUM:
                    self.panel.lab_survive.SetColor('#SR')
                elif player_num <= WARNING_ALINE_NUM_BIG:
                    self.panel.lab_survive.SetColor('#SR')
                else:
                    self.panel.lab_survive.SetColor('#SK')

    def on_kill_human_num_change(self, kill_num):
        self.panel.lab_kill.SetString(str(kill_num))

    def on_kill_mecha_num_change(self, kill_num):
        if self.panel.nd_gvg.isVisible():
            self.panel.nd_gvg.my_mech_num.SetString(str(kill_num))
        elif self.panel.nd_ffa.isVisible():
            self.panel.nd_ffa.my_mech_num.SetString(str(kill_num))
        else:
            self.panel.lab_mech_kill.SetString(str(kill_num))

    def on_assist_mecha_num_change(self, assist_num):
        if self.panel.nd_gvg.isVisible():
            self.panel.nd_gvg.my_assist_num.SetString(str(assist_num))

    def on_camera_player_setted(self):
        if global_data.player and global_data.player.get_battle():
            self.update_alive_player_num(global_data.player.get_battle().alive_player_num)

    def adjust_ui(self):
        if global_data.game_mode.is_mode_type((game_mode_const.GAME_MODE_DEATHS, game_mode_const.GAME_MODE_IMPROVISE)):
            self.panel.bar_survive.setVisible(False)
            self.panel.bar_kill.SetPosition('0%90', '50%0')
            self.process_chicken_node(True)
            self.panel.nd_gvg.setVisible(False)
        elif global_data.game_mode.is_mode_type((game_mode_const.GAME_MODE_GVG, game_mode_const.GAME_MODE_MECHA_DEATH, game_mode_const.GAME_MODE_DUEL, game_mode_const.GAME_MODE_GOOSE_BEAR)):
            self.panel.bar_survive.setVisible(False)
            self.panel.bar_kill.SetPosition('0%90', '50%0')
            self.process_chicken_node(False)
            self.panel.nd_gvg.setVisible(True)
        elif global_data.game_mode.is_mode_type((game_mode_const.GAME_MODE_FFA, game_mode_const.GAME_MODE_ZOMBIE_FFA, game_mode_const.GAME_MODE_ARMRACE)):
            self.panel.bar_kill.setVisible(False)
            self.panel.bar_survive.setVisible(False)
            self.panel.nd_ffa.setVisible(True)

    def process_chicken_node(self, show=False):
        self.panel.img_kill.setVisible(show)
        self.panel.lab_kill.setVisible(show)
        self.panel.img_mech_kill.setVisible(show)
        self.panel.lab_mech_kill.setVisible(show)

    def _update_alive_player_num(self, player_num):
        from logic.gcommon.common_utils import battle_utils
        if not battle_utils.is_signal_logic():
            return
        if not global_data.game_mode:
            return
        from logic.gutils.judge_utils import is_ob
        if not is_ob():
            if player_num <= 5 and not self._top_5_nd and global_data.game_mode.is_mode_type(game_mode_const.GAME_MODE_SURVIVALS):
                self._top_5_nd = global_data.uisystem.load_template_create('battle/i_fight_top5', self.panel.top_5)
                self._top_5_nd.PlayAnimation('show')