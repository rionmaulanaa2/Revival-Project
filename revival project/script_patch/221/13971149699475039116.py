# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/pve/rank/PVERankTeamSpeedPageUI.py
from __future__ import absolute_import
from logic.comsys.battle.pve.rank.PVETeamBaseRankWidget import PVETeamBaseRankWidget
from logic.gcommon.common_const.rank_const import MONTH_REFRESH
from logic.gcommon.common_const.pve_const import NORMAL_DIFFICUTY, PVE_RANK_SPEED_TEAM

class PVERankTeamSpeedPageUI(PVETeamBaseRankWidget):
    RANK_PAGE_TYPE = PVE_RANK_SPEED_TEAM

    def __init__(self, parent_panel, parent_node, template_pos, rank_config, page_config=None):
        self.parent_panel = parent_panel
        self.parent = parent_node
        super(PVERankTeamSpeedPageUI, self).__init__(rank_config, page_config)
        self.custom_show()

    def custom_show(self):
        self._template_root.list_rank_list.setVisible(False)
        self._template_root.temp_mine.setVisible(False)
        self._template_root.list_rank_list_team.setVisible(True)
        self._template_root.temp_mine_team.setVisible(True)

    def load_page_panel(self):
        self._template_root = global_data.uisystem.load_template_create('pve/rank/i_pve_rank_speed', parent=self.parent)
        self.list_rank = self._template_root.list_rank_list_team
        self.temp_mine = self._template_root.temp_mine_team

    def init_choose_list(self):
        self._template_root.lab_title_time.setVisible(True)
        self._template_root.temp_choose_type.setVisible(False)
        self._template_root.temp_title_choose_type.setVisible(False)
        self.cur_sel_condition.init_disfficulty_choose_list()
        self.cur_sel_condition.init_chapter_choose_list()
        self.cur_sel_condition.init_player_cnt_choose_list()

    @staticmethod
    def get_default_config():
        config = {'chapter': 1,
           'mecha_id': 0,
           'difficulty': NORMAL_DIFFICUTY,
           'list_type': MONTH_REFRESH,
           'player_cnt': 2,
           'is_friend': False
           }
        return config