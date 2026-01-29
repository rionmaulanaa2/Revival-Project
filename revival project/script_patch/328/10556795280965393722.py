# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivityPreviewPageTabWidget.py
from __future__ import absolute_import
from logic.comsys.activity.ActivityPageTabWidget import ActivityPageTabWidget
from logic.gutils import activity_utils
from logic.gcommon.common_utils.local_text import get_text_by_id
from common.cfg import confmgr
from logic.gcommon import time_utility as tutil

class ActivityPreviewPageTabWidget(ActivityPageTabWidget):

    def get_activity_list(self):
        activity_list_not_preview = activity_utils.get_ordered_activity_list(self.widget_type, with_redpoint=False)
        activity_list_preview = activity_utils.get_preview_activity_list(self.widget_type)
        self._activity_list = activity_list_not_preview + activity_list_preview

    def on_click_btn_tab_with_folder(self, activity_type, a_info):
        if activity_utils.is_preview_activity(activity_type):
            tab_name_id = confmgr.get('c_activity_config', activity_type, 'cNameTextID', default='')
            act_name = get_text_by_id(tab_name_id)
            global_data.game_mgr.show_tip(get_text_by_id(608413).format(activity_name=act_name))
            return
        super(ActivityPreviewPageTabWidget, self).on_click_btn_tab_with_folder(activity_type, a_info)

    def on_click_btn_tab_without_folder(self, activity_type, a_info):
        if activity_utils.is_preview_activity(activity_type):
            tab_name_id = confmgr.get('c_activity_config', activity_type, 'cNameTextID', default='')
            act_name = get_text_by_id(tab_name_id)
            global_data.game_mgr.show_tip(get_text_by_id(608413).format(activity_name=act_name))
            return
        super(ActivityPreviewPageTabWidget, self).on_click_btn_tab_without_folder(activity_type, a_info)

    def on_init_widget(self, item_widget, a_info):
        super(ActivityPreviewPageTabWidget, self).on_init_widget(item_widget, a_info)
        if type(a_info) == list:
            activity_type = a_info[0]['activity_type']
        else:
            activity_type = a_info['activity_type']
        if activity_utils.is_preview_activity(activity_type):
            item_widget.btn_tab.lab_time.setVisible(True)
            conf = confmgr.get('c_activity_config', activity_type)
            start_time = conf.get('cBeginTime', 0)
            end_time = conf.get('cEndTime', 0)
            start_str = ''
            end_str = ''
            if start_time:
                start_str = tutil.get_date_str('%m.%d', start_time)
            if end_time:
                end_str = tutil.get_date_str('%m.%d', end_time)
            item_widget.btn_tab.lab_time.SetString('{0}-{1}'.format(start_str, end_str))
        else:
            item_widget.btn_tab.lab_time.setVisible(False)