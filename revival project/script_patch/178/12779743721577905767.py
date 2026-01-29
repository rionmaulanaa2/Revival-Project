# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/pve/rank/PVERankSingleSpeedPageUI.py
from __future__ import absolute_import
from logic.comsys.battle.pve.rank.PVESingleBaseRankWidget import PVESingleBaseRankWidget
from logic.gcommon.common_const.rank_const import SEASON_REFRESH, MONTH_REFRESH
from logic.gcommon.common_const.pve_const import NORMAL_DIFFICUTY, PVE_RANK_SPEED_PERSONAL
from logic.gcommon.common_const.pve_rank_const import PVE_RANK_1_ALL, PVE_RANK_2_TEAM, PVE_RANK_3_TEAM, PVE_RANK_1_FRIEND, PVE_CONFIG_KEY_LIST_TYPE, PVE_CONFIG_KEY_IS_FRIEND, PVE_CONFIG_KEY_PLAYER_CNT

class PVERankSingleSpeedPageUI(PVESingleBaseRankWidget):
    RANK_PAGE_TYPE = PVE_RANK_SPEED_PERSONAL

    def __init__(self, parent_panel, parent_node, template_pos, rank_config, page_config=None):
        self.parent_panel = parent_panel
        self.parent = parent_node
        super(PVERankSingleSpeedPageUI, self).__init__(rank_config, page_config)
        self.custom_show()

    def custom_show(self):
        self._template_root.list_rank_list.setVisible(True)
        self._template_root.temp_mine.setVisible(True)
        self._template_root.list_rank_list_team.setVisible(False)
        self._template_root.temp_mine_team.setVisible(False)

    def load_page_panel(self):
        self._template_root = global_data.uisystem.load_template_create('pve/rank/i_pve_rank_speed', parent=self.parent)
        self.list_rank = self._template_root.list_rank_list
        self.temp_mine = self._template_root.temp_mine

    def init_choose_list(self):
        self.cur_sel_condition.init_type_choose_list()
        self.cur_sel_condition.init_disfficulty_choose_list()
        self.cur_sel_condition.init_chapter_choose_list()
        models = self.player_cnt_models(self.get_choosed_list_type())
        self.cur_sel_condition.init_player_cnt_choose_list(models)

    @staticmethod
    def get_default_config():
        config = {'chapter': 1,
           'mecha_id': 0,
           'difficulty': NORMAL_DIFFICUTY,
           'list_type': MONTH_REFRESH,
           'player_cnt': 1,
           'is_friend': False
           }
        return config

    def player_cnt_models(self, _list_type):
        if _list_type == SEASON_REFRESH:
            models = [
             PVE_RANK_1_ALL, PVE_RANK_1_FRIEND]
        else:
            models = [
             PVE_RANK_1_ALL, PVE_RANK_2_TEAM, PVE_RANK_3_TEAM, PVE_RANK_1_FRIEND]
        return models

    def reload_play_cnt_conf(self, _list_type):
        models = self.player_cnt_models(_list_type)
        self.cur_sel_condition.init_player_cnt_choose_list(models)
        player_cnt = self.get_choosed_player_cnt()
        if _list_type == SEASON_REFRESH and player_cnt > 1:
            self.cur_sel_condition.modify_config_data({PVE_CONFIG_KEY_IS_FRIEND: False,PVE_CONFIG_KEY_PLAYER_CNT: 1})

    def on_choosed_config_refresh_ui(self, rank_type, source_key, config):
        if source_key == PVE_CONFIG_KEY_LIST_TYPE:
            _list_type = config.get(PVE_CONFIG_KEY_LIST_TYPE)
            self.reload_play_cnt_conf(_list_type)
        super(PVERankSingleSpeedPageUI, self).on_choosed_config_refresh_ui(rank_type, source_key, config)