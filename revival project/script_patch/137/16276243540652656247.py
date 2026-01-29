# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/items_book_ui/CareerMedalWidget.py
from __future__ import absolute_import
from logic.gutils import career_utils
from logic.gcommon.common_const.rank_career_const import MAIN_BRANCH_MEDAL
from logic.client.const import items_book_const
from logic.comsys.role.PlayerCareerMedalWidget import PlayerCareerMedalWidget

class CareerMedalWidget(PlayerCareerMedalWidget):
    PANEL_CONFIG_NAME = 'undefined'

    def __init__(self, parent, panel):
        self.page_index = items_book_const.MEDAL_ID
        super(CareerMedalWidget, self).__init__(panel)
        self.update_collect_count()

    def update_collect_count(self):
        all_list = career_utils.get_badge_list_readonly(MAIN_BRANCH_MEDAL)
        all_cunt = len(all_list)
        own_cunt = 0
        for _id in all_list:
            has, lv = career_utils.has_badge(_id)
            if has:
                own_cunt += 1

        self.panel.temp_prog.lab_got.SetString('%d/%d' % (own_cunt, all_cunt))
        self.panel.temp_prog.prog.SetPercentage(int(own_cunt / float(all_cunt) * 100))