# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/observe_ui/JudgeObSettleUI.py
from __future__ import absolute_import
import six
import six_ex
from common.uisys.basepanel import BasePanel
from common.const.uiconst import NORMAL_LAYER_ZORDER, NORMAL_LAYER_ZORDER_1
from logic.gcommon.common_const import statistics_const
from logic.client.const import game_mode_const
RANK_IMG_PATH = {1: 'gui/ui_res_2/crew/img_crew_rank_1.png',
   2: 'gui/ui_res_2/crew/img_crew_rank_2.png',
   3: 'gui/ui_res_2/crew/img_crew_rank_3.png'
   }
GVG_RANK_IMG_PATH = {1: 'gui/ui_res_2/txt_pic/text_pic_cn/txt_tdm_win.png',
   2: 'gui/ui_res_2/txt_pic/text_pic_cn/txt_tdm_fail.png'
   }
from common.const import uiconst

class JudgeObSettleUI(BasePanel):
    PANEL_CONFIG_NAME = 'observe/fight_result'
    DLG_ZORDER = NORMAL_LAYER_ZORDER_1
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    UI_ACTION_EVENT = {'btn_back.btn_common_big.OnClick': 'on_go_back_lobby'
       }

    def on_init_panel(self, settle_data):
        self.settle_data = settle_data
        self.bg_ui = global_data.ui_mgr.create_simple_dialog('end/bg_end_full_screen_tdm', NORMAL_LAYER_ZORDER)
        self._is_single_person_battle = False
        battle = global_data.battle
        if battle and battle.is_single_person_battle():
            self._is_single_person_battle = True
        self.init_widget()
        self.hide_main_ui()

    def on_finalize_panel(self):
        if self.bg_ui and self.bg_ui.is_valid():
            self.bg_ui.close()
        self.show_main_ui()

    def init_widget(self):
        if self._is_single_person_battle:
            self.panel.nd_title.PlayAnimation('solo')
        if global_data.game_mode.is_mode_type(game_mode_const.GAME_MODE_SURVIVALS):
            self.panel.nd_title.lab_help.setVisible(not self._is_single_person_battle)
        elif global_data.game_mode.is_mode_type((game_mode_const.GAME_MODE_GVG, game_mode_const.GAME_MODE_DUEL)):
            self.panel.nd_title.RemoveFromParent()
            nd = global_data.uisystem.load_template_create('observe/i_fight_result_info_title_gvg', parent=self.panel.nd_content, name='nd_title')
            self.panel.list_info.SetTemplate('observe/i_fight_result_info_gvg')
        elif global_data.game_mode.is_mode_type(game_mode_const.GAME_MODE_DEATHS):
            self.panel.nd_title.RemoveFromParent()
            nd = global_data.uisystem.load_template_create('observe/i_fight_result_info_title_tdm', parent=self.panel.nd_content, name='nd_title')
            self.panel.list_info.SetTemplate('observe/i_fight_result_info_tdm')
        self.panel.list_info.DeleteAllSubItem()
        self.panel.list_info.SetInitCount(len(self.settle_data))
        for index, team_settle_dict in enumerate(self.settle_data):
            team_settle_nd = self.panel.list_info.GetItem(index)
            if global_data.game_mode.is_mode_type(game_mode_const.GAME_MODE_SURVIVALS):
                self.show_settle_info_of_one_team(team_settle_nd, team_settle_dict)
            elif global_data.game_mode.is_mode_type((game_mode_const.GAME_MODE_GVG, game_mode_const.GAME_MODE_DUEL)):
                self.show_settle_info_of_one_team_gvg(team_settle_nd, team_settle_dict)
            elif global_data.game_mode.is_mode_type(game_mode_const.GAME_MODE_DEATHS):
                pass
            rank = index + 1

    def show_settle_info_of_one_team(self, nd, team_settle_dict):
        team_member_settle_dict = team_settle_dict.get('member_settle_dict', {})
        team_member_info_dict = team_settle_dict.get('member_info', {})
        team_rank = team_settle_dict.get('rank')
        if self._is_single_person_battle:
            nd.PlayAnimation('solo')
        nd.list_info.DeleteAllSubItem()
        nd.list_info.SetInitCount(len(team_member_info_dict))
        for i, (key, member_info) in enumerate(six.iteritems(team_member_info_dict)):
            settle_info_nd = nd.list_info.GetItem(i)
            member_battle_statistics = team_member_settle_dict[key].get('statistics', {})
            member_name = member_info.get('char_name', '')
            member_kill_human_num = member_battle_statistics.get(statistics_const.KILL_HUMAN, 0)
            member_kill_mecha_num = member_battle_statistics.get(statistics_const.KILL_MECHA, 0)
            member_call_mecha_times = member_battle_statistics.get(statistics_const.CALL_MECHA_TIMES, 0)
            member_human_survival_time = member_battle_statistics.get(statistics_const.HUMAN_STATE_TIME, 0)
            mecha_time = member_battle_statistics.get(statistics_const.MECHA_TIME, {})
            if type(mecha_time) is dict:
                if six_ex.values(mecha_time):
                    member_mecha_survival_time = sum(six_ex.values(mecha_time)) if 1 else 0
                else:
                    member_mecha_survival_time = mecha_time
                member_damage_to_mecha = member_battle_statistics.get(statistics_const.DAMAGE_TO_MECHA, 0)
                member_damage_to_human = member_battle_statistics.get(statistics_const.DAMAGE_TO_HUMAN, 0)
                member_save_cnt = member_battle_statistics.get(statistics_const.SAVE_CNT, 0)
                settle_info_nd.lab_name.SetString(member_name)
                settle_info_nd.lab_beat.SetString('%s+%s' % (str(member_kill_human_num), str(member_kill_mecha_num)))
                settle_info_nd.lab_damage.SetString('%d+%d' % (member_damage_to_human, member_damage_to_mecha))
                settle_info_nd.lab_times.SetString('%d+%d' % (round(member_human_survival_time), round(member_mecha_survival_time)))
                settle_info_nd.lab_call.SetString(str(member_call_mecha_times))
                settle_info_nd.lab_help.SetString(str(member_save_cnt))
                settle_info_nd.lab_help.setVisible(not self._is_single_person_battle)

        if team_rank in RANK_IMG_PATH:
            nd.img_rank.SetDisplayFrameByPath('', RANK_IMG_PATH[team_rank])
        else:
            nd.img_rank.setVisible(False)
            nd.lab_rank.setVisible(True)
            nd.lab_rank.SetString(str(team_rank))

    def show_settle_info_of_one_team_gvg(self, nd, team_settle_dict):
        team_member_settle_dict = team_settle_dict.get('member_settle_dict', {})
        team_member_info_dict = team_settle_dict.get('member_info', {})
        team_rank = team_settle_dict.get('rank')
        nd.list_info.DeleteAllSubItem()
        nd.list_info.SetInitCount(len(team_member_info_dict))
        for i, (key, member_info) in enumerate(six.iteritems(team_member_info_dict)):
            settle_info_nd = nd.list_info.GetItem(i)
            member_battle_statistics = team_member_settle_dict[key].get('statistics', {})
            member_name = member_info.get('char_name', '')
            member_kill_mecha_num = member_battle_statistics.get(statistics_const.KILL_MECHA, 0)
            member_damage_to_mecha = member_battle_statistics.get(statistics_const.DAMAGE_TO_MECHA, 0)
            member_assist_damage_mecha = member_battle_statistics.get(statistics_const.ASSIST_MECHA, 0)
            member_received_mecha_hurt = member_battle_statistics.get(statistics_const.MECHA_HURT, 0)
            settle_info_nd.lab_name.SetString(member_name)
            settle_info_nd.lab_beat.SetString('%s' % str(member_kill_mecha_num))
            settle_info_nd.lab_assists.SetString('%d' % member_assist_damage_mecha)
            settle_info_nd.lab_damage.SetString('%d' % round(member_damage_to_mecha))
            settle_info_nd.lab_defense.SetString('%d' % round(member_received_mecha_hurt))

        if team_rank in GVG_RANK_IMG_PATH:
            nd.img_rank.SetDisplayFrameByPath('', GVG_RANK_IMG_PATH[team_rank])
            nd.img_rank.setScale(0.3)
        else:
            nd.img_rank.setVisible(False)
            nd.lab_rank.setVisible(True)
            nd.lab_rank.SetString(str(team_rank))

    def on_go_back_lobby(self, *args):
        if global_data.player:
            global_data.player.quit_battle(True)
        self.close()