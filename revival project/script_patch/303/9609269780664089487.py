# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/rank/CommonRankWidget.py
from __future__ import absolute_import
from logic.gcommon.common_const import rank_const
from common.uisys.BaseUIWidget import BaseUIWidget
from logic.gcommon import time_utility as tutil

class CommonRankWidget(BaseUIWidget):

    def __init__(self, parent, panel, rank_type, nd_title, nd_view_list, nd_self, *args, **kargs):
        self.rank_type = rank_type
        self.nd_title = nd_title
        self.nd_view_list = nd_view_list
        self.nd_self = nd_self
        self.sview_index = 0
        self.max_rank = 0
        self.is_check_sview = False
        self.sview_height = self.nd_view_list.getContentSize().height
        self.rank_data = global_data.message_data.get_rank_data(self.rank_type)
        self.rank_version = None
        self.global_events = {'message_on_rank_data': self.refresh_rank_content
           }
        super(CommonRankWidget, self).__init__(parent, panel)

        def scroll_callback(sender, eventType):
            if not self.is_check_sview:
                self.is_check_sview = True
                if self.panel:
                    self.panel.SetTimeOut(0.021, self.check_sview)

        self.nd_view_list.addEventListener(scroll_callback)
        return

    def destroy(self):
        super(CommonRankWidget, self).destroy()

    def init_title(self):
        pass

    def refresh_rank_content(self, rank_type, *args):
        if rank_type != self.rank_type:
            return
        self.rank_data = global_data.message_data.get_rank_data(self.rank_type)
        if not self.rank_data:
            return
        cur_rank_version = global_data.message_data.get_rank_version()
        if not self.rank_data or self.rank_version != cur_rank_version or tutil.time() - self.rank_data['save_time'] > rank_const.RANK_DATA_CACHE_MAX_TIME:
            global_data.message_data.clean_rank_data(self.rank_type)
            self.rank_version = global_data.message_data.get_rank_version()
            global_data.player.request_rank_list(self.rank_type, 0, rank_const.RANK_ONE_REQUEST_MAX_COUNT, True)
            return
        self.nd_view_list.DeleteAllSubItem()
        self.rank_list = self.rank_data.get('rank_list', [])
        msg_count = len(self.rank_list)
        self.sview_index = 0
        self.is_check_sview = False
        view_hight = 0
        index = 0
        while index < msg_count and view_hight < self.sview_height:
            data = self.rank_list[index]
            panel = self.add_rank_item(data)
            view_hight += panel.getContentSize().height
            index += 1

        self.sview_index = index - 1
        cur_rank_version = global_data.message_data.get_rank_version()
        self.rank_version = cur_rank_version

    def check_sview(self):
        msg_count = len(self.rank_list)
        self.sview_index = self.nd_view_list.AutoAddAndRemoveItem(self.sview_index, self.rank_list, msg_count, self.add_rank_item, 300, 300)
        self.is_check_sview = False
        if self.sview_index == msg_count - 1 and global_data.message_data.is_need_request_rank_data(self.rank_type):
            cur_rank_version = global_data.message_data.get_rank_version()
            start_index = self.sview_index if self.rank_version == cur_rank_version else 0
            global_data.player.request_rank_list(self.rank_type, start_index, start_index + rank_const.RANK_ONE_REQUEST_MAX_COUNT, True)

    def add_rank_item(self, data, is_back_item=True, index=-1):
        if is_back_item:
            panel = self.nd_view_list.AddTemplateItem(bRefresh=True)
        else:
            panel = self.nd_view_list.AddTemplateItem(0, bRefresh=True)
        is_self = False
        if str(global_data.player.uid) == str(data[0]):
            is_self = True
        self.update_rank_item(panel, data, is_self)
        return panel

    def update_rank_item(self, nd_item, data, is_self):
        pass