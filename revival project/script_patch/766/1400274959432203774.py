# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/rank/FriendHelpRankWidget.py
from __future__ import absolute_import
from logic.comsys.rank.CommonRankWidget import CommonRankWidget
from logic.gcommon.common_const import rank_const
import time

class FriendHelpRankWidget(CommonRankWidget):
    RANK_COUNT = 10

    def __init__(self, parent, panel):
        super(FriendHelpRankWidget, self).__init__(parent, panel, rank_const.RANK_TYPE_FRIEND_HELP, parent.nd_tittle, parent.list_rank, parent.nd_tittle)

    def update_rank_item(self, nd_item, data, is_self):
        rank = data[-1]
        nd_itm = nd_item.nd_itm
        nd_itm.lab_rank.SetString(str(data[-1] + 1))
        nd_itm.lab_name.SetString(str(data[1]))
        nd_itm.lab_number.SetString(str(data[2]))
        if is_self:
            nd_itm.lab_rank.SetColor('#SR')
            nd_itm.lab_name.SetColor('#SR')
            nd_itm.lab_number.SetColor('#SR')
        if rank == 0:
            nd_itm.bar_1st.setVisible(True)
            nd_itm.bar_other_rank.setVisible(False)
        else:
            nd_itm.bar_1st.setVisible(False)
            nd_itm.bar_other_rank.setVisible(True)
        if 5 <= rank <= 10:
            nd_itm.bar_other_rank.SetDisplayFrameByPath('', '/gui/ui_res_2/activity/activity_201907/21.png')

    def refresh_rank_content(self, rank_type, *args):
        if rank_type != self.rank_type:
            return
        self.rank_data = global_data.message_data.get_rank_data(self.rank_type)
        if not self.rank_data or time.time() - self.rank_data['save_time'] > rank_const.RANK_DATA_CACHE_MAX_TIME:
            global_data.message_data.clean_rank_data(self.rank_type)
            global_data.player.request_friendhelp_rank(self.RANK_COUNT)
            return
        self.nd_view_list.DeleteAllSubItem()
        self.rank_list = self.rank_data.get('rank_list', [])
        msg_count = len(self.rank_list)
        self.sview_index = 0
        self.is_check_sview = False
        view_hight = 0
        index = 0
        while index < msg_count and view_hight < self.sview_height + 100:
            data = self.rank_list[index]
            panel = self.add_rank_item(data)
            view_hight += panel.getContentSize().height
            index += 1

        self.sview_index = index - 1