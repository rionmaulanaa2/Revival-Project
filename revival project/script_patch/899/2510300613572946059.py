# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/live/LiveRecommendPageWidget.py
from __future__ import absolute_import
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gutils import observe_utils
from logic.comsys.live.LivePageWidgetBase import LivePageWidgetBase
from logic.gcommon.common_const import spectate_const as sp_const
import logic.gcommon.time_utility as tutil

class LiveRecommendPageWidget(LivePageWidgetBase):

    def __init__(self, parent_panel, list_type):
        super(LiveRecommendPageWidget, self).__init__(parent_panel, list_type)
        self._template_root = parent_panel.temp_list
        self._item_list_ui = self._template_root.item_list

    def get_empty_content_text(self):
        return get_text_by_id(19448)

    def get_youtube_data(self):
        start_ts = observe_utils.COMP_LIVE_START_TS
        end_ts = observe_utils.COMP_LIVE_END_TS
        if tutil.time() - start_ts >= 0 and tutil.time() - end_ts <= 0 and G_IS_NA_PROJECT:
            return [{'uid': global_data.player.uid,'role_name': 931000,'list_type': sp_const.SPECTATE_LIST_YOUTUBE}]
        return []