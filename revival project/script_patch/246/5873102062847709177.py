# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/pve/rank/PVERankSpeedPageProxyUI.py
from __future__ import absolute_import
from logic.gcommon.common_const.rank_const import MONTH_REFRESH
from logic.gcommon.common_const.pve_const import NORMAL_DIFFICUTY, PVE_RANK_SPEED_PERSONAL, PVE_RANK_SPEED_TEAM
from logic.comsys.battle.pve.rank.PVERankSingleSpeedPageUI import PVERankSingleSpeedPageUI
from logic.comsys.battle.pve.rank.PVERankTeamSpeedPageUI import PVERankTeamSpeedPageUI
import six_ex

class PVERankSpeedPageProxyUI(object):

    def __init__(self, parent_panel, parent_node, template_pos, rank_config):
        self.parent_panel = parent_panel
        self.parent = parent_node
        self.rank_config = rank_config
        self.template_pos = template_pos
        self.page_map = {}
        self._has_binded_event = False
        self.process_event(True)
        self.switch_rank_page(rank_config[4]['rank_type'])

    def process_event(self, is_bind):
        if self._has_binded_event == is_bind:
            return
        emgr = global_data.emgr
        econf = {'on_switch_pve_rank_player_cnt': self._on_switch_pve_rank_player_cnt
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)
        self._has_binded_event = is_bind

    def set_visible(self, is_show):
        for page_type in six_ex.keys(self.page_map):
            page_widget = self.page_map[page_type]
            if self.cur_rank_type == page_type:
                page_widget.set_visible(is_show)
            else:
                page_widget.set_visible(False)

    def destroy(self):
        self.process_event(False)
        for page_type in six_ex.keys(self.page_map):
            page_widget = self.page_map[page_type]
            page_widget.destroy()

        self.page_map = {}
        self.cur_rank_type = None
        self.parent_panel = None
        self.parent = None
        self.rank_config = None
        return

    def _on_switch_pve_rank_player_cnt(self, page_config):
        self._is_friend = page_config.get('is_friend', False)
        self._player_cnt = page_config.get('player_cnt', 1)
        if self._player_cnt > 1:
            page_config['list_type'] = MONTH_REFRESH
        page_type = PVE_RANK_SPEED_PERSONAL if self._player_cnt <= 1 else PVE_RANK_SPEED_TEAM
        self.switch_rank_page(page_type, page_config)

    def switch_rank_page(self, page_type, page_config=None):
        self.cur_rank_type = page_type
        if page_type not in self.page_map:
            self.load_page_panel(page_type, page_config)
        else:
            page_widget = self.page_map[page_type]
            page_widget.load_page_config(page_config)
            page_widget.set_visible(True)
        for _rank_type in six_ex.keys(self.page_map):
            if _rank_type == page_type:
                continue
            page_widget = self.page_map[_rank_type]
            page_widget.set_visible(False)

    def load_page_panel(self, page_type, page_config=None):
        if page_type in self.page_map:
            return
        if page_type == PVE_RANK_SPEED_PERSONAL:
            _page_config = page_config if page_config else PVERankSingleSpeedPageUI.get_default_config()
            self.page_map[page_type] = PVERankSingleSpeedPageUI(self.parent_panel, self.parent, self.template_pos, self.rank_config, _page_config)
        elif page_type == PVE_RANK_SPEED_TEAM:
            _page_config = page_config if page_config else PVERankTeamSpeedPageUI.get_default_config()
            self.page_map[page_type] = PVERankTeamSpeedPageUI(self.parent_panel, self.parent, self.template_pos, self.rank_config, _page_config)
        else:
            raise (
             'error rank type', page_type)

    def get_list_rank(self):
        page_widget = self.page_map[self.cur_rank_type]
        return page_widget.get_list_rank()

    def check_sview(self):
        page_widget = self.page_map[self.cur_rank_type]
        if page_widget:
            page_widget.check_sview()

    def get_question_btn(self):
        page_widget = self.page_map[self.cur_rank_type]
        if page_widget:
            return page_widget.get_question_btn()
        else:
            return None

    def get_page_model_ctrl_key(self):
        page_widget = self.page_map[self.cur_rank_type]
        if page_widget:
            return page_widget.get_page_model_ctrl_key()
        else:
            return None