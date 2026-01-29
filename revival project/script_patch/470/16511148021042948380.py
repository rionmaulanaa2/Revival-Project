# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/live/LiveCompetitionPageWidget.py
from __future__ import absolute_import
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.comsys.live.LivePageWidgetBase import LivePageWidgetBase
from logic.gutils.observe_utils import LiveObserveUIHelper

class LiveCompetitionPageWidget(LivePageWidgetBase):

    def __init__(self, parent_panel, list_type):
        super(LiveCompetitionPageWidget, self).__init__(parent_panel, list_type)
        self._template_root = global_data.uisystem.load_template_create('live/i_observe_list', parent=parent_panel.temp_list)
        self._item_list_ui = self._template_root.item_list
        self._need_follow_status = False
        self._need_friend_status = False
        self._item_list_ui.SetTemplate('live/i_observe_list_item_match')

    def get_empty_content_text(self):
        return get_text_by_id(19519)

    def _init_live_observe_item(self, ui_item, list_type, item_data):
        LiveObserveUIHelper.init_live_observe_item_match(ui_item, list_type, item_data)