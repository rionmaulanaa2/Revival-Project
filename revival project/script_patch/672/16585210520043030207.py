# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/lottery/LuckScore/LuckScoreWeekRankWidget.py
from logic.comsys.lottery.LuckScore.LuckScoreRankBaseWidget import LuckScoreRankBaseWidget
from logic.gcommon.common_const import rank_const
from logic.gcommon.common_const.luck_score_const import LUCK_SCORE_WEEK_TYPE
from logic.gutils.mall_utils import check_lucky_score_rank_week_likes_red_point

class LuckScoreWeekRankWidget(LuckScoreRankBaseWidget):

    def init_parameters(self):
        super(LuckScoreWeekRankWidget, self).init_parameters()
        self.rank_type = rank_const.RANK_TYPE_LUCK_WEEK.format(self.item_no)
        self.luck_type = LUCK_SCORE_WEEK_TYPE
        self.my_luck_dict = global_data.player.get_my_week_luck_dict(self.item_no) if global_data.player else {}
        self.luck_data_index = 4

    def check_red_point(self):
        return check_lucky_score_rank_week_likes_red_point(self.lottery_id)