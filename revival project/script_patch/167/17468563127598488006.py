# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/Rank/TeammatesRankWidget.py
from __future__ import absolute_import
import six
from common.const.uiconst import BASE_LAYER_ZORDER
from common.uisys.basepanel import BasePanel
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gcommon import time_utility
from logic.comsys.battle.Rank.RankTabBaseWidget import RankTabBaseWidget

class TeammatesRankWidget(RankTabBaseWidget):
    FULL_VIEW_ITEM_MAX_NUM = 6

    def __init__(self, panel, rise_panel):
        super(TeammatesRankWidget, self).__init__(panel)
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
        self._sview_index = 0
        self.rank_data = []
        self._is_check_sview = False

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
        self._sview_index = self.lview.AutoAddAndRemoveItem(self._sview_index, self.rank_data, len(self.rank_data), self.add_item_elem, 100, 100)
        self._is_check_sview = False

    def add_item_elem(self, data, is_back_item=True, index=-1):
        if is_back_item:
            item_widget = self.lview.AddTemplateItem(bRefresh=True)
        else:
            item_widget = self.lview.AddTemplateItem(0, bRefresh=True)
        data_index, key, kill_num, kill_mecha_num, killed, point = data
        name = ''
        item_widget.group_index = data_index
        if global_data.player and global_data.player.logic:
            if key == global_data.player.id:
                name = global_data.player.get_name()
            else:
                teanm_info = global_data.player.logic.ev_g_teammate_infos()
                if teanm_info:
                    name = teanm_info.get(key, {}).get('char_name', '')
        item_widget.lab_name.setString('%s' % name)
        item_widget.lab_kill_role.setString('%d' % kill_num)
        item_widget.lab_kill_mech.setString('%d' % kill_mecha_num)
        item_widget.lab_be_killed.setString('%d' % killed)
        item_widget.lab_point.setString(get_text_by_id(156).format(point))
        return item_widget

    def refresh_listview(self):
        count = self.lview.GetItemCount()
        if count <= 0:
            return
        first_index = self.lview.GetItem(0).group_index
        last_index = self.lview.GetItem(count - 1).group_index
        for id, data in enumerate(self.rank_data[first_index:last_index + 1]):
            index, key, kill_num, kill_mecha_num, killed, point = data
            name = ''
            if global_data.player and global_data.player.logic:
                if key == global_data.player.id:
                    name = global_data.player.get_name()
                else:
                    teanm_info = global_data.player.logic.ev_g_teammate_infos()
                    if teanm_info:
                        name = teanm_info.get(key, {}).get('char_name', '')
            self.lview.GetItem(id).lab_name.setString('%s' % name)
            self.lview.GetItem(id).lab_kill_role.setString('%d' % kill_num)
            self.lview.GetItem(id).lab_kill_mech.setString('%d' % kill_mecha_num)
            self.lview.GetItem(id).lab_be_killed.setString('%d' % killed)
            self.lview.GetItem(id).lab_point.setString(get_text_by_id(156).format(point))

    def request_data(self):
        bat = global_data.player.get_battle() or global_data.player.get_joining_battle()
        bat and bat.request_group_data()

    def set_group_data(self, group_data):
        self.rank_data = []
        index = 0
        for key, value in six.iteritems(group_data):
            kill_num, kill_mecha_num, killed, point = value
            self.rank_data.append((index, key, kill_num, kill_mecha_num, killed, point))
            index += 1

        if self.lview.GetItemCount() < self.FULL_VIEW_ITEM_MAX_NUM:
            self.init_item_list()
        else:
            self.refresh_listview()