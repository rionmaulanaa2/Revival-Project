# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/rank/GlMainRank.py
from __future__ import absolute_import
import time
import common.const.uiconst
from common.uisys.basepanel import BasePanel
from logic.gcommon.common_const import rank_const
from logic.comsys.rank.GlRankContentWidget import GlRankContentWidget
from logic.comsys.common_ui.WindowCommonComponent import WindowCommonComponent
from logic.comsys.common_ui.WindowMediumBase import WindowMediumBase
MAX_COUNT = 200

class GlMainRank(WindowMediumBase):
    PANEL_CONFIG_NAME = 'activity/activity_202105/520/activity_520_leaderboard_detail'
    DLG_ZORDER = common.const.uiconst.NORMAL_LAYER_ZORDER
    UI_ACTION_EVENT = {}
    GLOBAL_EVENT = {'message_on_rank_data': 'refresh_rank_content'
       }
    OPEN_SOUND_NAME = 'leaderboard'
    TEMPLATE_NODE_NAME = 'content_bar'

    def set_title(self, title):
        self.panel.content_bar.lab_title.SetString(title)

    def on_init_panel(self, rank_type):
        super(GlMainRank, self).on_init_panel()
        self.cur_rank_type = rank_type
        self._message_data = global_data.message_data
        self._rank_version = None
        self._init_rank_widget()
        self.request_rank_data()
        return

    def _init_rank_widget(self):
        self.rank_content_widget = GlRankContentWidget(self.panel, self.panel.rank_list, self.check_sview_callback)

    def on_tab_selected(self, rank_index):
        if self.cur_rank_index == rank_index:
            return False
        self.cur_rank_index = rank_index
        self.request_rank_data()

    def request_rank_data(self):
        rank_data = self._message_data.get_rank_data(self.cur_rank_type)
        if rank_data and time.time() - rank_data['save_time'] < rank_const.RANK_DATA_CACHE_MAX_TIME:
            self.refresh_rank_content(self.cur_rank_type)
            self._rank_version = self._message_data.get_rank_version()
        else:
            self.rank_content_widget.clear_content()
            self._message_data.clean_rank_data(self.cur_rank_type)
            if global_data.player:
                self._rank_version = self._message_data.get_rank_version()
                global_data.player.request_rank_list(self.cur_rank_type, 0, rank_const.RANK_ONE_REQUEST_MAX_COUNT, True, True)

    def refresh_rank_content(self, rank_type):
        if self.cur_rank_type != rank_type:
            return
        if self.rank_content_widget:
            self.rank_content_widget.refresh_rank_content(self._message_data.get_rank_data(rank_type))

    def check_sview_callback(self, sview_index, msg_count):
        if sview_index == msg_count - 1 and self._message_data.is_need_request_rank_data(self.cur_rank_type) and msg_count < MAX_COUNT and global_data.player and self.cur_rank_type:
            cur_rank_version = self._message_data.get_rank_version()
            start_index = sview_index if self._rank_version == cur_rank_version else 0
            if sview_index + rank_const.RANK_ONE_REQUEST_MAX_COUNT > MAX_COUNT:
                end_index = MAX_COUNT if 1 else sview_index + rank_const.RANK_ONE_REQUEST_MAX_COUNT
                global_data.player.request_rank_list(self.cur_rank_type, start_index, end_index, False, True)
                self._rank_version = cur_rank_version

    def on_finalize_panel(self):
        self.destroy_widget('rank_content_widget')