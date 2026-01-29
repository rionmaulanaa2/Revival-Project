# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/role/PlayerCareerMedalWidget.py
from __future__ import absolute_import
from functools import cmp_to_key
from .PlayerTabBaseWidget import PlayerTabBaseWidget
from logic.gutils import battle_flag_utils
from logic.gutils import career_utils
from logic.gutils import item_utils
from logic.gutils import locate_utils
from logic.gcommon.item.item_const import DEFAULT_FLAG_FRAME
from logic.gutils.template_utils import set_ui_show_picture
from logic.comsys.role.BattleFlagChooseWidget import BattleFlagChooseWidget
from logic.comsys.role.BattleFlagBgChooseWidget import BattleFlagBgChooseWidget
from logic.gcommon.common_const.rank_career_const import MAIN_BRANCH_MEDAL

class PlayerCareerMedalWidget(PlayerTabBaseWidget):
    PANEL_CONFIG_NAME = 'life/i_life_medal'

    def __init__(self, panel):
        super(PlayerCareerMedalWidget, self).__init__(panel)
        self.init_panel()
        self.init_event()

    def init_event(self):
        self.process_event(True)

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {}
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def init_panel(self):
        self._refresh_view(play_appear=False)

    def _refresh_view(self, play_appear=False):
        from logic.comsys.career.CareerMainUI import CareerMainUI
        CareerMainUI.refresh_badge_medal_list(self.panel, self._get_medal_ids(), play_appear=play_appear)

    def _get_medal_ids(self):
        from logic.comsys.career.CareerMainUI import CareerMainUI
        sub_branches = career_utils.get_badge_list_readonly(MAIN_BRANCH_MEDAL)
        sorted_ids = sorted(sub_branches, key=cmp_to_key(CareerMainUI.badge_sorter))
        return sorted_ids

    def on_appear(self):
        self._refresh_view(play_appear=True)

    def on_disappear(self):
        pass

    def destroy(self):
        self.process_event(False)
        super(PlayerCareerMedalWidget, self).destroy()