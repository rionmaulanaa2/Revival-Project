# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/Flag/FlagTopScoreUI.py
from __future__ import absolute_import
import six
from common.const.uiconst import SMALL_MAP_ZORDER
from common.uisys.basepanel import BasePanel
from logic.comsys.battle import BattleUtils
from logic.gcommon import time_utility as tutil
import math
import math3d
from common.const import uiconst
import common.utils.timer as timer

class FlagTopScoreUI(BasePanel):
    PANEL_CONFIG_NAME = 'battle_flagsnatch/fight_flag_top_score'
    DLG_ZORDER = SMALL_MAP_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    UI_ACTION_EVENT = {'nd_score.OnClick': 'toggle_score_details'
       }

    def on_init_panel(self):
        self.init_parameters()
        self.init_event()
        self.init_panel()

    def on_finalize_panel(self):
        self.panel.lab_time.StopTimerAction()
        self.process_event(False)
        self.flag_left_cursor_pos = None
        self.flag_right_cursor_pos = None
        if self.flag_pop_timer:
            global_data.game_mgr.unregister_logic_timer(self.flag_pop_timer)
        return

    def init_panel(self):
        self.img_flag_blue = self.panel.img_bgblue.img_flagblue
        self.img_flag_red = self.panel.img_bgred.img_flagred
        self.img_flag_blue.setVisible(False)
        self.img_flag_red.setVisible(False)
        self.panel.RecordAnimationNodeState('alarm')
        self.panel.nd_prog_blue.prog_blue.SetPercentage(0)
        self.panel.nd_prog_red.prog_red.SetPercentage(0)
        if global_data.death_battle_data:
            self.update_group_score(global_data.death_battle_data.get_group_score_data())
            self.update_timestamp()
        if global_data.player and global_data.player.logic:
            if not global_data.player.logic.ev_g_is_in_spectate():
                global_data.player.logic.send_event('E_DEATH_GUIDE_CHOOSE_WEAPON_UI')

    def init_event(self):
        self.process_event(True)

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'update_battle_timestamp': self.update_timestamp,
           'update_group_score_data': self.update_group_score,
           'scene_observed_player_setted_event': self._on_scene_observed_player_setted,
           'flagsnatch_flag_moved': self._on_flag_moved,
           'flagsnatch_flag_planting_succeed': self._on_flag_planting_succeed,
           'flagsnatch_flag_recover': self._on_flag_recover,
           'flagsnatch_flag_pick_up': self._on_flag_picked
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def _on_flag_picked(self, picker_id, picker_faction):
        if picker_faction == global_data.player.logic.ev_g_group_id():
            self.panel.ing_noflag.ing_blueflag.setVisible(True)
        else:
            self.panel.ing_noflag.ing_redflag.setVisible(True)

    def _on_flag_recover(self, *args):
        self.panel.ing_noflag.ing_blueflag.setVisible(False)
        self.panel.ing_noflag.ing_redflag.setVisible(False)

    def _on_flag_planting_succeed(self, planter_id, planter_faction):
        player_faction = global_data.player.logic.ev_g_group_id()
        if self.flag_pop_timer:
            global_data.game_mgr.unregister_logic_timer(self.flag_pop_timer)
        if planter_faction == player_faction:
            self.img_flag_blue.setVisible(True)
            self.panel.StopAnimation('flagblue')
            self.panel.PlayAnimation('flagblue')
            self.flag_pop_timer = global_data.game_mgr.register_logic_timer(lambda node=self.img_flag_blue: self.set_node_invisible(node), 30, times=1, mode=timer.LOGIC)
        else:
            self.img_flag_red.setVisible(True)
            self.panel.StopAnimation('flagred')
            self.panel.PlayAnimation('flagred')
            self.flag_pop_timer = global_data.game_mgr.register_logic_timer(lambda node=self.img_flag_red: self.set_node_invisible(node), 30, times=1, mode=timer.LOGIC)

    def set_node_invisible(self, node):
        node.setVisible(False)

    def _on_flag_moved(self, flag_pos):
        if not self.do_flag_ui_move:
            return
        else:
            if not self.faction_to_flag_base_id:
                self.faction_to_flag_base_id = global_data.death_battle_data.faction_to_flag_base_id
                if not self.faction_to_flag_base_id:
                    return
            if global_data.cam_lplayer:
                player_faction = global_data.cam_lplayer.ev_g_camp_id()
            else:
                player_faction = global_data.player.logic.ev_g_camp_id()
            player_base_id = self.faction_to_flag_base_id.get(player_faction, None)
            other_team_base_id = None
            for faction_id, base_id in six.iteritems(self.faction_to_flag_base_id):
                if faction_id != player_faction:
                    other_team_base_id = base_id
                    break

            player_base = global_data.battle.get_entity(player_base_id)
            other_team_base = global_data.battle.get_entity(other_team_base_id)
            if not player_base or not other_team_base:
                return
            player_base_pos = player_base.logic.ev_g_hp_position()
            other_team_base_pos = other_team_base.logic.ev_g_hp_position()
            if not player_base_pos or not other_team_base_pos:
                return
            dis_to_player_base = (player_base_pos - flag_pos).length
            dis_to_other_base = (other_team_base_pos - flag_pos).length
            percent = dis_to_player_base / (dis_to_other_base + dis_to_player_base)
            new_pos = math3d.vector2(self.flag_left_cursor_pos.x, self.flag_left_cursor_pos.y)
            new_pos.x += self.flag_cursor_dis_x * percent
            self.panel.ing_noflag.SetPosition(new_pos.x, new_pos.y)
            return

    def _on_scene_observed_player_setted(self, ltarget):
        self.update_name(ltarget)
        if global_data.death_battle_data:
            self.update_group_score(global_data.death_battle_data.get_group_score_data())

    def init_parameters(self):
        self.cfg_data = global_data.game_mode.get_cfg_data('play_data')
        self.update_name(None)
        self.is_warning = False
        self.left_10_seconds = False
        self.flag_left_cursor_pos = self.panel.img_bgblue.getPosition()
        self.flag_right_cursor_pos = self.panel.img_bgred.getPosition()
        self.flag_cursor_dis_x = self.flag_right_cursor_pos.x - self.flag_left_cursor_pos.x
        self.faction_to_flag_base_id = None
        self.do_flag_ui_move = True
        self.flag_pop_timer = None
        self.img_flag_blue = None
        self.img_flag_red = None
        return

    def update_name(self, ltarget):
        if global_data.player and global_data.player.logic:
            self.group_id = global_data.player.logic.ev_g_group_id()
        if ltarget:
            self.group_id = ltarget.ev_g_group_id()

    def update_timestamp(self, *args):
        if global_data.player and global_data.player.in_local_battle():
            return
        self.on_count_down()

    def update_group_score(self, data):
        bat = global_data.player.get_battle()
        if not bat:
            return
        total_point = bat.get_settle_point()
        if not total_point:
            return
        for g_id in six.iterkeys(data):
            if g_id == self.group_id:
                blue_score = self.panel.nd_score.lab_score_blue.getString()
                self.panel.nd_score.lab_score_blue.SetString(str(data[g_id]))
                if blue_score != str(data[g_id]):
                    self.panel.StopAnimation('blue_up')
                    self.panel.PlayAnimation('blue_up')
                percent = 100.0 * data[g_id] / total_point
                self.panel.prog_blue.SetPercentage(percent)
                self.panel.nd_light_blue.img_light_blue.SetPosition('{}%'.format(str(100 - percent)), '{}%'.format(str(percent)))
            else:
                red_score = self.panel.nd_score.lab_score_red.getString()
                self.panel.nd_score.lab_score_red.SetString(str(data[g_id]))
                if red_score != str(data[g_id]):
                    self.panel.StopAnimation('red_up')
                    self.panel.PlayAnimation('red_up')
                percent = 100.0 * data[g_id] / total_point
                self.panel.prog_red.SetPercentage(percent)
                self.panel.nd_light_red.img_light_red.SetPosition('{}%'.format(str(percent)), '{}%'.format(str(percent)))

    def toggle_score_details(self, *args):
        ui_inst = global_data.ui_mgr.get_ui('FlagScoreDetailsUI')
        if ui_inst:
            global_data.ui_mgr.close_ui('FlagScoreDetailsUI')
        else:
            global_data.ui_mgr.show_ui('FlagScoreDetailsUI', 'logic.comsys.battle.Flag')

    def on_count_down(self):
        revive_time = BattleUtils.get_battle_left_time()

        def refresh_time(pass_time):
            if global_data.death_battle_data and global_data.death_battle_data.is_ready_state:
                return
            left_time = revive_time - pass_time
            if left_time <= 30 and not self.is_warning:
                self.panel.lab_time.SetColor('#SR')
                self.panel.PlayAnimation('alarm')
                self.is_warning = True
            elif left_time > 30 and self.is_warning:
                self.panel.lab_time.SetColor('##BC')
                self.panel.StopAnimation('alarm')
                self.panel.RecoverAnimationNodeState('alarm')
                self.is_warning = False
            if left_time <= 10 and not self.left_10_seconds:
                ui = global_data.ui_mgr.show_ui('FFAFinishCountDown', 'logic.comsys.battle.ffa')
                ui.on_delay_close(left_time)
                self.left_10_seconds = True
            left_time = int(math.ceil(left_time))
            left_time = tutil.get_delta_time_str(left_time)[3:]
            self.panel.lab_time.SetString(left_time)
            self.panel.lab_time_vx.SetString(left_time)

        def refresh_time_finsh():
            left_time = tutil.get_delta_time_str(0)[3:]
            self.panel.lab_time.SetString(left_time)

        self.panel.lab_time.SetColor('#BC')
        self.panel.StopAnimation('alarm')
        self.panel.RecoverAnimationNodeState('alarm')
        self.is_warning = False
        self.panel.lab_time.StopTimerAction()
        refresh_time(0)
        self.panel.lab_time.TimerAction(refresh_time, revive_time, callback=refresh_time_finsh, interval=1)

    def set_my_group_score(self, score):
        self.panel.nd_score.lab_score_blue.SetString(str(score))