# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/Improvise/ImproviseTopScoreUI.py
from __future__ import absolute_import
import six
from six.moves import range
from common.const.uiconst import SMALL_MAP_ZORDER, UI_VKB_NO_EFFECT
from common.uisys.basepanel import BasePanel
from logic.gcommon import time_utility as tutil
import math
from logic.gcommon.common_const.battle_const import ROUND_TYPE_PURE_HUMAN
from logic.gutils.role_head_utils import get_head_photo_res_path, get_role_default_photo, get_mecha_photo
MAX_POINTS = 5
MAX_TEAM_SIZE = 3

class ImproviseTopScoreUI(BasePanel):
    PANEL_CONFIG_NAME = 'battle_3v3/3v3_top_score'
    DLG_ZORDER = SMALL_MAP_ZORDER
    UI_VKB_TYPE = UI_VKB_NO_EFFECT
    PROG_AMPLIFIED_TAG = 31415926
    GLOBAL_EVENT = {'update_battle_round_end_ts': '_refresh_count_down',
       'battle_new_round': '_on_battle_new_round',
       'scene_camera_player_setted_event': '_on_scene_camera_player_setted',
       'update_battle_group_points_dict': '_on_update_battle_group_points_dict',
       'update_improvise_battle_group_hp_dict': '_on_update_improvise_battle_group_hp_dict'
       }
    UI_ACTION_EVENT = {'btn_top.OnClick': '_toggle_score_details'
       }

    def on_init_panel(self):
        self._init_parameters()
        self._init_panel()

    def _init_parameters(self):
        self.is_warning = False

    def _init_panel(self):
        self.panel.RecordAnimationNodeState('alarm')
        self._init_group_points(self.panel.jindu_me)
        self._init_group_points(self.panel.jindu_other)
        self._refresh_both_group_points(global_data.improvise_battle_data.get_group_points_dict(), global_data.cam_lplayer)
        self._refresh_both_hp_data(global_data.improvise_battle_data.get_group_hp_dict(), global_data.cam_lplayer)
        self._refresh_count_down(global_data.improvise_battle_data.get_cur_round_end_ts())
        self.panel.nd_mode.setVisible(False)

    def on_finalize_panel(self):
        pass

    def _on_battle_new_round(self, prev, now, mode):
        from logic.client.const import game_mode_const
        if mode != game_mode_const.GAME_MODE_IMPROVISE:
            return
        self.panel.nd_mode.setVisible(False)

    def _on_scene_camera_player_setted(self):
        self._refresh_both_group_points(global_data.improvise_battle_data.get_group_points_dict(), global_data.cam_lplayer)
        self._refresh_both_hp_data(global_data.improvise_battle_data.get_group_hp_dict(), global_data.cam_lplayer)

    def _on_update_battle_group_points_dict(self, points_dict):
        self._refresh_both_group_points(points_dict, global_data.cam_lplayer)

    def _on_update_improvise_battle_group_hp_dict(self, data):
        self._refresh_both_hp_data(data, global_data.cam_lplayer)

    def _init_group_points(self, group_point_node):
        group_point_node.RecordAnimationNodeState('amplify')
        group_point_node._amplified = False
        group_point_node.list_jindu_win.SetInitCount(MAX_POINTS)

    def _refresh_both_group_points(self, group_points_dict, self_lplayer):
        if self_lplayer is None:
            return
        else:
            self_group_id = self_lplayer.ev_g_group_id()
            if self_group_id is None:
                return
            self_points = group_points_dict.get(self_group_id, 0)
            self._refresh_group_points(self.panel.jindu_me, self_points)
            for group_id, points in six.iteritems(group_points_dict):
                if group_id != self_group_id:
                    oppo_points = points
                    break
            else:
                oppo_points = 0

            self._refresh_group_points(self.panel.jindu_other, oppo_points)
            return

    def _refresh_group_points(self, group_point_node, cur_points):
        for i in range(group_point_node.list_jindu_win.GetItemCount()):
            node = group_point_node.list_jindu_win.GetItem(i)
            node.img_win.setVisible(i + 1 <= cur_points)

        if cur_points + 1 != global_data.improvise_battle_data.get_max_win_round_cnt():
            group_point_node.StopAnimation('amplify')
            group_point_node.RecordAnimationNodeState('amplify')
            group_point_node._amplified = False
            group_point_node.stopActionByTag(self.PROG_AMPLIFIED_TAG)
        elif not group_point_node.IsPlayingAnimation('amplify') and not group_point_node._amplified:
            group_point_node.PlayAnimation('amplify')
            anim_time = group_point_node.GetAnimationMaxRunTime('amplify')

            def cb():
                group_point_node._amplified = True

            group_point_node.DelayCallWithTag(anim_time, cb, self.PROG_AMPLIFIED_TAG)

    def _refresh_both_hp_data(self, group_hp_data, self_lplayer):
        if self_lplayer is None:
            return
        else:
            self_group_id = self_lplayer.ev_g_group_id()
            self_hp_data = group_hp_data.get(self_group_id, {})
            for group_id, hp_data in six.iteritems(group_hp_data):
                if group_id != self_group_id:
                    oppo_group_id = group_id
                    oppo_hp_data = hp_data
                    break
            else:
                oppo_group_id = None
                oppo_hp_data = {}

            self._refresh_single_hp_data(self.panel.prog_me, self.panel.lab_score_blue, self.panel.list_mech_blue, self_hp_data, self_group_id, self_lplayer.id)
            self._refresh_single_hp_data(self.panel.prog_other, self.panel.lab_score_red, self.panel.list_mech_red, oppo_hp_data, oppo_group_id, self_lplayer.id)
            return

    def _refresh_single_hp_data(self, prog_node, lab_score_node, avatar_list_node, single_group_hp_data, group_id, self_pid):
        cur_hp_sum = 0.0
        cur_max_hp_sum = 0.0
        if single_group_hp_data:
            for pid, hp_data in six.iteritems(single_group_hp_data):
                cur_hp_sum += hp_data.get('hp', 0.0)
                cur_max_hp_sum += hp_data.get('max_hp', 0.0)

        lab_score_node.SetString(str(int(cur_hp_sum)))
        perc = 100.0 if cur_max_hp_sum == 0.0 else cur_hp_sum / cur_max_hp_sum * 100.0
        prog_node.SetPercentage(perc)
        score_details_data = global_data.improvise_battle_data.get_score_details_data()
        self._refresh_single_avatar_list(avatar_list_node, score_details_data.get(group_id, []), single_group_hp_data, self_pid)

    def _refresh_single_avatar_list(self, list_node, single_group_score_details, single_group_hp_data, self_pid):
        indices = list(range(len(single_group_score_details)))
        if single_group_score_details:
            idx = -1
            for i, score_details in enumerate(single_group_score_details):
                pid, name, is_alive, kill_num, kill_mecha_num, role_id, is_mvp, assist_total, called_mecha_id, score = score_details
                if pid == self_pid:
                    idx = i
                    break

            if idx != -1 and idx != 0:
                popped_idx = indices.pop(idx)
                indices.insert(0, popped_idx)
        list_node.SetInitCount(MAX_TEAM_SIZE)
        for i in range(MAX_TEAM_SIZE):
            node = list_node.GetItem(i)
            if i >= len(single_group_score_details):
                node.setVisible(False)
                continue
            node.setVisible(True)
            real_idx = indices[i]
            score_details = single_group_score_details[real_idx]
            pid, name, is_alive, kill_num, kill_mecha_num, role_id, is_mvp, assist_total, called_mecha_id, score = score_details
            hp_data = single_group_hp_data.get(pid, {})
            mecha_type_id = hp_data.get('in_mecha_type', 0)
            is_defeated = hp_data.get('is_defeated', False)
            in_mecha = mecha_type_id > 0
            if in_mecha:
                photo_no = get_mecha_photo(mecha_type_id)
            else:
                photo_no = get_role_default_photo(role_id)
            avatar_icon_path = get_head_photo_res_path(photo_no)
            if in_mecha:
                node.temp_1.img_people.setVisible(False)
                node.temp_1.img_head.setVisible(True)
                node.temp_1.img_head.SetDisplayFrameByPath('', avatar_icon_path)
            else:
                node.temp_1.img_head.setVisible(False)
                node.temp_1.img_people.setVisible(True)
                node.temp_1.img_people.SetDisplayFrameByPath('', avatar_icon_path)
            node.temp_1.nd_clip.SetOptimize(False)
            node.img_mine.setVisible(self_pid == pid)
            node.temp_1.img_broken.setVisible(is_defeated)

    def _refresh_count_down(self, end_ts):
        left_time = max(0.0, end_ts - tutil.get_server_time_battle())

        def refresh_time(pass_time, left_time=left_time):
            left_time = left_time - pass_time
            if left_time <= 30 and not self.is_warning:
                self.panel.lab_time_new.SetColor('#SR')
                self.panel.PlayAnimation('alarm')
                self.is_warning = True
            left_time = int(math.ceil(left_time))
            left_time = tutil.get_delta_time_str(left_time)[4:]
            self.panel.lab_time_new.SetString(left_time)
            self.panel.lab_time_vx.SetString(left_time)

        def refresh_time_finish():
            left_time = tutil.get_delta_time_str(0)[4:]
            self.panel.lab_time_new.SetString(left_time)
            self.panel.lab_time_vx.SetString(left_time)
            self.panel.StopAnimation('alarm')
            self.panel.RecoverAnimationNodeState('alarm')

        self.panel.lab_time_new.SetColor('#BW')
        self.panel.StopAnimation('alarm')
        self.panel.RecoverAnimationNodeState('alarm')
        self.is_warning = False
        self.panel.lab_time_new.StopTimerAction()
        self.panel.lab_time_new.TimerAction(refresh_time, left_time, callback=refresh_time_finish, interval=1)
        refresh_time(0.0)

    def _toggle_score_details(self, *args):
        ui_inst = global_data.ui_mgr.get_ui('ImproviseScoreDetailsUI')
        if ui_inst:
            global_data.ui_mgr.close_ui('ImproviseScoreDetailsUI')
        else:
            global_data.ui_mgr.show_ui('ImproviseScoreDetailsUI', 'logic.comsys.battle.Improvise')