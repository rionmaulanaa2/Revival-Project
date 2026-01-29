# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/rank/ScoreRankWidget.py
from __future__ import absolute_import
from logic.comsys.rank.BaseRankWidget import BaseRankWidget
from logic.gcommon.common_const import rank_const, rank_battle_score_const
from logic.gutils import role_head_utils
from logic.gutils import season_utils
from logic.comsys.message.PlayerSimpleInf import BTN_TYPE_TEAM
from cocosui import cc, ccui, ccs
from logic.gcommon.common_const import friend_const, chat_const
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gutils import template_utils
from logic.gutils import follow_utils
SCORE_RANK_WIDGET_TYPE_NORMAL = 0
SCORE_RANK_WIDGET_TYPE_TDM = 1
SCORE_RANK_WIDGET_TYPE_GVG = 2
team_rank_map = [
 rank_const.RANK_TYPE_SOLO_OVERALL_SCORE,
 rank_const.RANK_TYPE_SQUAD_OVERALL_SCORE]
team_mode_infos = (2148, 2150)

class ScoreRankWidget(BaseRankWidget):

    def __init__(self, parent_panel, nd, template_pos, rank_info):
        super(ScoreRankWidget, self).__init__(rank_info)
        self.parent_panel = parent_panel
        self.nd = nd
        self._template_root = global_data.uisystem.load_template_create('rank/i_rank_score_list', parent=nd)
        self._template_root.setPosition(template_pos)
        self.list_rank = self._template_root.list_rank_list
        self.score_rank_widget_type = rank_info[2]
        self.cur_rank_type = None
        self.top_panel_type = None
        self.team_mode_index = 0
        self.cur_rank_area = None
        self.init_list()
        self.init_rank_area_choose()
        self.init_top_panel()
        return

    def init_top_panel(self):
        temp_top = self._template_root.temp_top
        if self.score_rank_widget_type in (SCORE_RANK_WIDGET_TYPE_TDM, SCORE_RANK_WIDGET_TYPE_GVG):
            temp_top.btn_chose_mode.setVisible(False)
            return

        @temp_top.btn_chose_mode.unique_callback()
        def OnClick(*args):
            flag = temp_top.list_btn.isVisible()
            temp_top.list_btn.setVisible(not flag)
            temp_top.open.icon_open.setRotation(flag or 180 if 1 else 0)

        from logic.gutils import template_utils
        mode_option = [ {'name': get_text_by_id(team_size_text),'mode': idx} for idx, team_size_text in enumerate(team_mode_infos)
                      ]

        def call_back(index):
            if self.team_mode_index != index:
                self.team_mode_index = index
                self.request_rank_data()
            self.refresh_top_title(mode_option[index].get('name', ''))
            temp_top.list_btn.setVisible(False)

        def arrow_cb(arrow, vis):
            arrow.setRotation(180 if vis else 0)

        template_utils.init_common_choose_list_2(temp_top.list_btn, temp_top.open.icon_open, mode_option, call_back, arrow_cb=arrow_cb)
        DEFAULT_SHOW_TEAM_MODE_INDEX = 0
        self.team_mode_index = DEFAULT_SHOW_TEAM_MODE_INDEX
        self.request_rank_data()

    def refresh_top_title(self, mode_info):
        temp_top = self._template_root.temp_top
        temp_top.btn_chose_mode.SetText(mode_info)

    def request_rank_data(self):
        cur_rank_type = self.get_cur_rank_type()
        self.cur_rank_type = cur_rank_type
        super(ScoreRankWidget, self).request_rank_data()

    def get_cur_rank_type(self):
        if self.score_rank_widget_type == SCORE_RANK_WIDGET_TYPE_NORMAL:
            return team_rank_map[self.team_mode_index]
        else:
            if self.score_rank_widget_type == SCORE_RANK_WIDGET_TYPE_TDM:
                return rank_const.RANK_TYPE_DEATH_OVERALL_SCORE
            return rank_battle_score_const.RANK_TYPE_OVERALL_SCORE_122

    def refresh_item(self, panel, data):
        rank = int(data[3] + 1)
        if rank >= 1 and rank <= 3:
            panel.img_rank.SetDisplayFrameByPath('', template_utils.get_clan_rank_num_icon(rank))
            panel.img_rank.setVisible(True)
            panel.lab_rank.setVisible(False)
        else:
            panel.img_rank.setVisible(False)
            panel.lab_rank.setVisible(True)
            panel.lab_rank.setString(str(rank))
        panel.lab_player_name.setString(str(data[1][0]))
        role_head_utils.init_role_head(panel.player_role_head, data[1][2], data[1][3])
        social_friend = self._message_data.get_social_friend_by_uid(friend_const.SOCIAL_ID_TYPE_LINEGAME, data[0])
        if self.cur_rank_area == rank_const.LINE_FRIEND_RANK and social_friend and data[0] != global_data.player.uid:
            icon = '<img="{}",scale=0.65>'.format(chat_const.LINE_ICON)
            desc_content = '#SW{}#n#DG{}#n'.format(icon, self._message_data.get_line_friend_name(social_friend.get('social_id')))
            panel.lab_dec.SetString(desc_content)
            panel.lab_dec.setVisible(True)
            panel.lab_player_name.SetPosition('50%-82', '50%+10')
        else:
            panel.lab_dec.setVisible(False)
            panel.lab_player_name.SetPosition('50%-82', '50%-2')
        if data[2]:
            panel.lab_number.setString(str(data[2][0]))
        else:
            panel.lab_number.SetString(15051)
        follow_utils.refresh_rank_list_follow_status(panel, data[0], str(data[1][0]))
        self.add_player_simple_callback(panel.player_role_head, data, self._template_root.img_list_pnl)
        self.add_reques_model_info(panel, data[0])