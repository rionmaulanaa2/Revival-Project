# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/Rank/GroupsRankWidget.py
from __future__ import absolute_import
from common.const.uiconst import BASE_LAYER_ZORDER
from common.uisys.basepanel import BasePanel
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gcommon import time_utility
from logic.comsys.battle.Rank.RankTabBaseWidget import RankTabBaseWidget
RNAK_ICON = {1: 'gui/ui_res_2/battle/point_mode/icon_1st.png',2: 'gui/ui_res_2/battle/point_mode/icon_2nd.png',
   3: 'gui/ui_res_2/battle/point_mode/icon_3rd.png'
   }

class GroupsRankWidget(RankTabBaseWidget):
    FULL_VIEW_ITEM_MAX_NUM = 6
    REQUEST_MAX_NUM = 20

    def __init__(self, panel, rise_panel):
        super(GroupsRankWidget, self).__init__(panel)
        self.rise_panel = rise_panel
        self.init_parameters()
        self.init_event()
        self.lview = self.panel.list_rank

        @self.lview.unique_callback()
        def OnScrolling(sender):
            if self._is_check_sview == False:
                self._is_check_sview = True
                self.panel.SetTimeOut(0.2, self.check_sview)

        self.lview.DeleteAllSubItem()
        self.lview_height = self.lview.getContentSize().height

    def init_parameters(self):
        self._request_tag = self.REQUEST_MAX_NUM / 2 - 1
        self._sview_index = 0
        self.rank_data = []
        self._is_check_sview = False
        self._own_rank_data = []
        self._rank_num = 0

    def init_event(self):
        pass

    def init_item_list(self):
        self.lview.DeleteAllSubItem()
        data_count = len(self.rank_data)
        self._sview_index = 0
        all_height = 0
        index = 0
        vert_indent = self.lview.GetVertIndent()
        while all_height < self.lview_height + 100 and index < data_count:
            data = self.rank_data[index]
            item_widget = self.add_item_elem(data)
            all_height += item_widget.getContentSize().height + vert_indent
            index += 1

        self._sview_index = index - 1

    def check_sview(self):
        self._sview_index = self.lview.AutoAddAndRemoveItem(self._sview_index, self.rank_data, len(self.rank_data), self.add_item_elem, 300, 300)
        self._is_check_sview = False
        self.panel.temp_myself.setVisible(not self.is_my_rank_visible())

    def is_my_rank_visible(self):
        count = self.lview.GetItemCount()
        if count <= 0:
            return True
        my_rank = self._own_rank_data[0]
        first_index = self.lview.GetItem(0).group_index
        last_index = self.lview.GetItem(count - 1).group_index
        f_rank = self.rank_data[first_index][1]
        l_rank = self.rank_data[last_index][1]
        if my_rank >= f_rank and my_rank <= l_rank:
            node = self.lview.GetItem(my_rank - first_index)
            return node and self.lview.IsNodeVisible(node)
        return False

    def add_item_elem(self, data, is_back_item=True, index=-1):
        if is_back_item:
            item_widget = self.lview.AddTemplateItem(bRefresh=True)
        else:
            item_widget = self.lview.AddTemplateItem(0, bRefresh=True)
        rank_index, rank, rankdata = data
        teamname, kill_num, kill_mecha_num, killed, point = rankdata
        item_widget.group_index = rank_index
        item_widget.rank.setString(get_text_by_id(19409).format(**{'rank': rank}))
        item_widget.lab_team_name.setString(teamname)
        item_widget.lab_kd.setString('/'.join([str(kill_num), str(kill_mecha_num), str(killed)]))
        item_widget.lab_point.setString(get_text_by_id(156).format(point))
        if (rank_index + 1) % self.REQUEST_MAX_NUM == self.REQUEST_MAX_NUM / 2:
            self._request_tag = rank_index
        item_widget.bar_my.setVisible(self._own_rank_data[0] == rank)
        self.show_star(item_widget, rank)
        return item_widget

    def refresh_listview(self):
        count = self.lview.GetItemCount()
        if count <= 0:
            return
        first_index = self.lview.GetItem(0).group_index
        last_index = self.lview.GetItem(count - 1).group_index
        for id, data in enumerate(self.rank_data[first_index:last_index + 1]):
            index, rank, rankdata = data
            teamname, kill_num, kill_mecha_num, killed, point = rankdata
            self.lview.GetItem(id).rank.setString(get_text_by_id(19409).format(**{'rank': rank}))
            self.lview.GetItem(id).lab_team_name.setString(teamname)
            self.lview.GetItem(id).lab_kd.setString('/'.join([str(kill_num), str(kill_mecha_num), str(killed)]))
            self.lview.GetItem(id).lab_point.setString(get_text_by_id(156).format(point))
            self.lview.GetItem(id).bar_my.setVisible(self._own_rank_data[0] == rank)
            self.show_star(self.lview.GetItem(id), rank)

    def on_show_lstview(self, *args, **kargs):
        self.panel.PlayAnimation('show')
        self.refresh_listview()

    def on_hide_lstview(self, *args, **kargs):
        self.panel.PlayAnimation('disappear')

    def request_data(self):
        start_rank = self._request_tag + 1 - self.REQUEST_MAX_NUM + 1
        end_rank = max(self._request_tag + 1 + self.REQUEST_MAX_NUM, self._rank_num)
        bat = global_data.player.get_battle() or global_data.player.get_joining_battle()
        bat and bat.request_rank(start_rank, end_rank)

    def set_group_data(self, data):
        start_rank, rank_len, rank_data, group_data = data
        self._rank_num = rank_len
        self._own_rank_data = group_data
        self.set_own_rank()
        for i, data in enumerate(rank_data):
            rank = start_rank + i
            index = rank - 1
            if len(self.rank_data) >= rank:
                self.rank_data[index] = (
                 index, rank, data)
            else:
                self.rank_data.append((index, rank, data))

        if self.lview.GetItemCount() < self.FULL_VIEW_ITEM_MAX_NUM:
            self.init_item_list()
        else:
            self.refresh_listview()
        self.panel.temp_myself.setVisible(not self.is_my_rank_visible())

    def set_own_rank(self):
        rank, kill_num, kill_mecha_num, killed, point = self._own_rank_data
        self.panel.temp_myself.rank.setString(''.join([get_text_by_id(19409).format(**{'rank': rank}), '(', get_text_by_id(19410), ')']))
        self.panel.temp_myself.lab_team_name.setString(global_data.player.get_name())
        self.panel.temp_myself.lab_kd.setString('/'.join([str(kill_num), str(kill_mecha_num), str(killed)]))
        self.panel.temp_myself.lab_point.setString(get_text_by_id(156).format(point))
        self.show_star(self.panel.temp_myself, rank)

    def show_star(self, node, rank):
        star_icon = RNAK_ICON.get(rank, '')
        if star_icon:
            node.star.setVisible(True)
            node.star.SetDisplayFrameByPath('', star_icon)
        else:
            node.star.setVisible(False)