# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/Occupy/OccupyBattleUI.py
from __future__ import absolute_import
import six
import six_ex
from common.const.uiconst import BASE_LAYER_ZORDER
from logic.comsys.battle.Occupy.OccupyData import PART_FIGHT
from common.uisys.basepanel import BasePanel
from logic.comsys.battle import BattleUtils
from logic.gcommon import time_utility as tutil
from common.const import uiconst
POINT_TXT = {25: [8225, 8226],50: [
      8227, 8228],
   75: [
      8229, 8230],
   90: [
      8231, 8232]
   }

class OccupyBattleUI(BasePanel):
    PANEL_CONFIG_NAME = 'battle_contention/battle_score_upper'
    DLG_ZORDER = BASE_LAYER_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    UI_ACTION_EVENT = {'nd_touch.OnClick': 'toggle_score_details'
       }

    def on_init_panel(self):
        self.init_parameters()
        self.init_event()
        self.init_panel()

    def on_finalize_panel(self):
        self.panel.bar_time.StopTimerAction()
        self.process_event(False)

    def init_parameters(self):
        self.my_last_point = 0
        self.other_last_point = 0
        self.player = global_data.cam_lplayer
        self.control_side = None
        self.is_warning = False
        self.cfg_data = global_data.game_mode.get_cfg_data('play_data')
        self.panel.RecordAnimationNodeState('score_red')
        self.panel.RecordAnimationNodeState('score_blue')
        return

    def init_panel(self):
        for node in [self.panel.progress_blue, self.panel.progress_red]:
            node.SetPercentage(0)

        for node in [self.panel.lab_blue_point, self.panel.lab_red_point]:
            node.SetString('0')

        self.update_timestamp()
        if global_data.death_battle_data:
            self.update_group_score_data(global_data.death_battle_data.get_group_score_data())
            self.update_control_point()

    def init_event(self):
        self.process_event(True)

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'update_battle_timestamp': self.update_timestamp,
           'update_group_score_data': self.update_group_score_data,
           'scene_observed_player_setted_event': self._on_scene_observed_player_setted,
           'update_control_point': self.update_control_point,
           'show_battle_points': self.show_battle_points
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def update_control_point(self):
        control_point_dict = global_data.death_battle_data.part_data
        all_control_point = six_ex.values(control_point_dict)
        if all_control_point:
            one_point = all_control_point[0]
            control_side = one_point.control_side
            if control_side is None:
                return
            if self.control_side != control_side:
                is_fight = control_side == PART_FIGHT
                if is_fight:
                    self.panel.PlayAnimation('score_red')
                    self.panel.PlayAnimation('score_blue')
                else:
                    self.panel.StopAnimation('score_red')
                    self.panel.RecoverAnimationNodeState('score_red')
                    self.panel.StopAnimation('score_blue')
                    self.panel.RecoverAnimationNodeState('score_blue')
            self.control_side = control_side
        return

    def _on_scene_observed_player_setted(self, ltarget):
        self.player = ltarget
        self.my_last_point = 0
        self.other_last_point = 0
        self.control_side = None
        if global_data.death_battle_data:
            self.update_group_score_data(global_data.death_battle_data.get_group_score_data())
            self.update_control_point()
        return

    def update_timestamp(self, *args):
        self.on_count_down()

    def update_group_score_data(self, data):
        if not self.player:
            return
        else:
            total_point = self.cfg_data.get('settle_point')
            if not total_point:
                return
            battle_data = global_data.death_battle_data
            max_progress_side = False
            max_progress = 0
            for group_id, point in six.iteritems(data):
                is_my_side = self.is_my_team(group_id)
                node = self.panel.progress_blue if is_my_side else self.panel.progress_red
                progress = 100.0 * point / total_point
                self.set_progress(node, progress)
                node = self.panel.lab_blue_point if is_my_side else self.panel.lab_red_point
                node.SetString(str(point))
                if is_my_side:
                    if self.my_last_point != point:
                        global_data.emgr.occupy_my_score_up.emit(point - self.my_last_point)
                        self.my_last_point = point
                        self.panel.PlayAnimation('score_blue02')
                elif self.other_last_point != point:
                    self.other_last_point = point
                    self.panel.PlayAnimation('score_red02')
                max_progress = max(progress, max_progress)
                if max_progress == progress:
                    max_progress_side = is_my_side

            if not battle_data.show_remind_ani and max_progress >= 90:
                ani_name = 'near_win_blue' if max_progress_side else 'near_win_red'
                self.panel.PlayAnimation(ani_name)
                battle_data.show_remind_ani = True
            txt_id = None
            if max_progress_side:
                txt_index = 0 if 1 else 1
                if max_progress >= 90:
                    battle_data.show_remind_point[90] = battle_data.show_remind_point.get(90, False) or True
                    txt_id = POINT_TXT[90][txt_index]
            elif max_progress >= 75:
                if not battle_data.show_remind_point.get(75, False):
                    battle_data.show_remind_point[75] = True
                    txt_id = POINT_TXT[75][txt_index]
            elif max_progress >= 50:
                if not battle_data.show_remind_point.get(50, False):
                    battle_data.show_remind_point[50] = True
                    txt_id = POINT_TXT[50][txt_index]
            elif max_progress >= 25:
                if not battle_data.show_remind_point.get(25, False):
                    battle_data.show_remind_point[25] = True
                    txt_id = POINT_TXT[25][txt_index]
            if txt_id:
                from logic.gcommon.common_const.battle_const import UP_NODE_COMMON_RIKO_TIPS
                message_data = {'content_txt': get_text_by_id(txt_id),'delay_time': 3,'template_scale': [1, 1]}
                global_data.emgr.battle_event_message.emit(message_data, message_type=UP_NODE_COMMON_RIKO_TIPS)
            return

    def is_my_team(self, group_id):
        if not self.player:
            return False
        my_group_id = self.player.ev_g_group_id()
        return group_id == my_group_id

    def set_progress(self, node, progress):
        node.SetPercentage(progress)

    def on_count_down(self):
        if global_data.death_battle_data and global_data.death_battle_data.is_ready_state:
            return
        revive_time = BattleUtils.get_battle_left_time()

        def refresh_time(pass_time):
            if global_data.death_battle_data and global_data.death_battle_data.is_ready_state:
                return
            left_time = int(revive_time - pass_time)
            if left_time <= 20 and not self.is_warning:
                self.panel.lab_time.SetColor('#SR')
                self.panel.PlayAnimation('alarm')
                self.is_warning = True
            elif left_time > 20 and self.is_warning:
                self.panel.lab_time.SetColor('#SQ')
                self.panel.StopAnimation('alarm')
                self.is_warning = False
            left_time = tutil.get_delta_time_str(left_time)[3:]
            self.panel.lab_time.SetString(left_time)

        def refresh_time_finsh():
            left_time = tutil.get_delta_time_str(0)[3:]
            self.panel.lab_time.SetString(left_time)

        self.panel.lab_time.SetColor('#SQ')
        self.panel.StopAnimation('alarm')
        self.is_warning = False
        self.panel.bar_time.StopTimerAction()
        self.panel.bar_time.TimerAction(refresh_time, revive_time, callback=refresh_time_finsh)

    def toggle_score_details(self, *args):
        ui_inst = global_data.ui_mgr.get_ui('OccupyScoreDetailsUI')
        if ui_inst:
            global_data.ui_mgr.close_ui('OccupyScoreDetailsUI')
        else:
            global_data.ui_mgr.show_ui('OccupyScoreDetailsUI', 'logic.comsys.battle.Occupy')

    def show_battle_points(self, is_mecha, points):
        self.panel.icon_people.setVisible(not is_mecha)
        self.panel.icon_mecha.setVisible(is_mecha)
        if is_mecha:
            self.panel.StopAnimation('icon_people')
            self.panel.PlayAnimation('icon_mecha')
            self.panel.icon_mecha.lab_number.SetString('+%d' % int(points))
        else:
            self.panel.StopAnimation('icon_mecha')
            self.panel.PlayAnimation('icon_people')
            self.panel.icon_people.lab_number.SetString('+%d' % int(points))