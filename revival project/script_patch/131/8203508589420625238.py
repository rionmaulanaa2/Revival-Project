# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/share/PersonInfoShareCreator.py
from __future__ import absolute_import
from logic.gutils.share_utils import init_share_person_info
from logic.comsys.share.ShareTemplateBase import ShareTemplateBase, async_disable_wrapper
from logic.gcommon.common_const import statistics_const as sconst

class PersonInfoShareCreator(ShareTemplateBase):
    KIND = 'PERSONAL_SHARE'

    @async_disable_wrapper
    def create(self, parent=None, tmpl=None):
        super(PersonInfoShareCreator, self).create(parent)

    def refresh_player_stat_inf(self, battle_mode_str, battle_data):
        self.panel.pnl_content.lab_title.setString(battle_mode_str)
        win_cnt, total_cnt, top10_cnt, kill_cnt, dead_cnt = battle_data
        self.panel.nd_statistics_2.lab_num.setString(str(win_cnt))
        if total_cnt == 0:
            text = '0%'
        else:
            text = '%.2f' % (win_cnt * 100.0 / total_cnt) + '%'
        self.panel.nd_statistics_3.lab_num.setString(str(text))
        self.panel.nd_statistics_1.lab_num.setString(str(total_cnt))
        self.panel.nd_statistics_4.lab_num.setString(str(top10_cnt))
        self.panel.nd_statistics_5.lab_num.setString(str(kill_cnt))
        if dead_cnt == 0:
            text = '-'
        else:
            text = '%.2f' % (kill_cnt / float(dead_cnt))
        self.panel.nd_statistics_6.lab_num.setString(text)