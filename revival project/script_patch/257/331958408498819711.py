# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivityMainPageTabWidget.py
from __future__ import absolute_import
import six_ex
import six
from logic.comsys.activity.ActivityPageTabWidget import ActivityPageTabWidget
from logic.gutils import activity_utils
from common.cfg import confmgr

class ActivityMainPageTabWidget(ActivityPageTabWidget):

    def __init__(self, parent, widget_type, select_cb=None, default_font_size=24, tab_init_cb=None):
        self.parent = parent
        self.panel = parent.panel
        self._request_activities = False
        self.widget_type = widget_type
        self._select_widget_cb = select_cb
        self._default_font_size = default_font_size
        self._tab_init_cb = tab_init_cb
        self.init_main_parameters()
        self.init_parameters()
        self.init_event()
        self.refresh_activity_list()

    def on_finalize_panel(self):
        super(ActivityMainPageTabWidget, self).on_finalize_panel()

    def init_main_parameters(self):
        self.tab_cfg = [
         {'tab_name_txt_id': 611324,'btn_pic': ['gui/ui_res_2/activity/activity_resource/icon_calendar_0.png',
                      'gui/ui_res_2/activity/activity_resource/icon_calendar_1.png',
                      'gui/ui_res_2/activity/activity_resource/icon_calendar_0.png']
            },
         {'tab_name_txt_id': 604023,'btn_pic': ['gui/ui_res_2/activity/activity_resource/icon_daily_0.png',
                      'gui/ui_res_2/activity/activity_resource/icon_daily_1.png',
                      'gui/ui_res_2/activity/activity_resource/icon_daily_0.png']
            },
         {'tab_name_txt_id': 604024,'btn_pic': ['gui/ui_res_2/activity/activity_resource/icon_special_0.png',
                      'gui/ui_res_2/activity/activity_resource/icon_special_1.png',
                      'gui/ui_res_2/activity/activity_resource/icon_special_0.png']
            },
         {'tab_name_txt_id': 606293,'btn_pic': ['gui/ui_res_2/activity/activity_resource/icon_cooperation_0.png',
                      'gui/ui_res_2/activity/activity_resource/icon_cooperation_1.png',
                      'gui/ui_res_2/activity/activity_resource/icon_cooperation_0.png']
            },
         {'tab_name_txt_id': 19518,'btn_pic': ['gui/ui_res_2/activity/activity_resource/icon_cooperation_0.png',
                      'gui/ui_res_2/activity/activity_resource/icon_cooperation_1.png',
                      'gui/ui_res_2/activity/activity_resource/icon_cooperation_0.png']
            }]
        self.cur_tab_id = 0
        self.tab_id_to_list_index = {}
        self.cur_tab = None
        self.activity_list_by_type = {}
        self.activity_to_tab = {}
        self.last_activity_list = []
        return

    def init_parameters(self):
        super(ActivityMainPageTabWidget, self).init_parameters()
        self.recover_page_widget()

    def refresh_activity_list(self):
        self.get_activity_list()
        self.init_main_page_tab()
        self.re_select_tab()

    def init_main_page_tab(self):
        tab_ids = six_ex.keys(self.activity_list_by_type)
        tab_ids.sort()
        tablist = self.panel.temp_tab_list.list_tab_1
        tablist.SetInitCount(len(tab_ids))
        for index, tab_id in enumerate(tab_ids):
            self.tab_id_to_list_index[tab_id] = index
            tab = tablist.GetItem(index)
            info = self.tab_cfg[tab_id]
            tab.btn_tab.SetText(info.get('tab_name_txt_id'))
            tab.btn_icon.SetFrames('', info.get('btn_pic'), False, None)

            @tab.btn_tab.unique_callback()
            def OnClick(btn, touch, cur_tab_id=tab_id):
                self.cur_tab_id = cur_tab_id
                self.recover_page_widget()
                self.init_parameters()
                self.init_page_tab()
                self.select_tab('')

        self._init_page_tab()
        return

    def recover_page_widget(self):
        if self._selected_widget:
            self._selected_widget.btn_tab.SetSelect(False)
            self._selected_widget.StopAnimation('continue')
            self._selected_widget.RecoverAnimationNodeState('continue')
        if self._cur_view_page_widget:
            last_selected_activity_type = self._cur_selected_activity_type
            last_panel = self._cur_view_page_widget.get_panel() if self._cur_view_page_widget else None
            self._cur_view_page_widget.set_show(False)
            self._cur_view_page_widget.on_finalize_panel()
            self._cur_view_page_widget = None
            self.check_is_nile_activity_finalized(last_selected_activity_type, last_panel)
        if self._cur_view_sub_page_widget:
            self._cur_view_sub_page_widget.set_show(False)
            self._cur_view_sub_page_widget.on_finalize_panel()
        return

    def get_activity_list(self):
        activity_list = activity_utils.get_ordered_activity_list(self.widget_type)
        if self.last_activity_list == activity_list:
            if self.cur_tab_id not in self.activity_list_by_type:
                self.cur_tab_id = 0
            self._activity_list = self.activity_list_by_type.get(self.cur_tab_id, [])
            if not self._activity_list:
                for tab_id, act_list in six.iteritems(self.activity_list_by_type):
                    if act_list:
                        self.cur_tab_id = tab_id
                        self._activity_list = act_list
                        break

            return
        self.last_activity_list = activity_list
        self.activity_list_by_type = {}
        self.activity_to_tab = {}
        for a_info in activity_list:
            if type(a_info) == list:
                activity_type = a_info[0]['activity_type']
                tab_id = activity_utils.get_activity_tab_id(activity_type)
                for info in a_info:
                    activity_type = info['activity_type']
                    self.activity_to_tab[activity_type] = tab_id

            else:
                activity_type = a_info['activity_type']
                tab_id = activity_utils.get_activity_tab_id(activity_type)
                self.activity_to_tab[activity_type] = tab_id
            if tab_id not in self.activity_list_by_type:
                self.activity_list_by_type[tab_id] = []
            self.activity_list_by_type[tab_id].append(a_info)

        if self.cur_tab_id not in self.activity_list_by_type:
            self.cur_tab_id = 0
        self._activity_list = self.activity_list_by_type.get(self.cur_tab_id, [])
        if not self._activity_list:
            for tab_id, act_list in six.iteritems(self.activity_list_by_type):
                if act_list:
                    self.cur_tab_id = tab_id
                    self._activity_list = act_list
                    break

    def try_select_tab(self, activity_type):
        self.select_tab(activity_type)

    def select_tab(self, activity_type, is_inner=False, is_init=False):
        if not activity_type or activity_type not in self.activity_to_tab:
            activity_type = self._default_activity_type
        if not activity_type:
            return
        tab_id = self.activity_to_tab[activity_type]
        index = self.tab_id_to_list_index.get(tab_id, 0)
        last_cur_tab_id = self.cur_tab_id
        self.cur_tab_id = tab_id
        if last_cur_tab_id != tab_id:
            self.init_page_tab()
        tablist = self.panel.temp_tab_list.list_tab_1
        if self.cur_tab:
            self.cur_tab.btn_tab.SetSelect(False)
            self.cur_tab.btn_icon.SetSelect(False)
        self.cur_tab = tablist.GetItem(index)
        self.cur_tab.btn_tab.SetSelect(True)
        self.cur_tab.btn_icon.SetSelect(True)
        self._select_tab(activity_type, is_inner, is_init)

    def refresh_red_point(self):
        if not self.panel or not self.panel.temp_tab_list:
            return
        mian_tablist = self.panel.temp_tab_list.list_tab_1
        tablist = self.panel.temp_tab_list.list_tab
        for tab_id, activity_list in six.iteritems(self.activity_list_by_type):
            index = self.tab_id_to_list_index.get(tab_id, 0)
            item = mian_tablist.GetItem(index)
            show_img_red = False
            for id, a_info in enumerate(activity_list):
                if type(a_info) == list:
                    activity_type = a_info[0]['activity_type']
                    cUiData = confmgr.get('c_activity_config', activity_type, 'cUiData', default={})
                    merge_activity = cUiData.get('merge_activity')
                    if merge_activity:
                        activity_type = activity_utils.switch_activity_type(activity_type)
                        tab_name_id = confmgr.get('c_activity_config', activity_type, 'cNameTextID', default='')
                        if tab_name_id:
                            count = 0
                            for sub_index, s_a_info in enumerate(a_info):
                                activity_type = s_a_info['activity_type']
                                tab_name_id = confmgr.get('c_activity_config', activity_type, 'cNameTextID', default='')
                                if tab_name_id:
                                    if activity_utils.is_activity_finished(activity_type) or activity_utils.lower_activity_level_limit(activity_type):
                                        continue
                                    count += activity_utils.get_redpoint_count_by_type(activity_type)

                        else:
                            if activity_utils.is_activity_finished(activity_type) or activity_utils.lower_activity_level_limit(activity_type):
                                continue
                            count = activity_utils.get_redpoint_count_by_type(activity_type)
                    else:
                        count = 0
                        for sub_index, s_a_info in enumerate(a_info):
                            activity_type = s_a_info['activity_type']
                            if activity_utils.is_activity_finished(activity_type) or activity_utils.lower_activity_level_limit(activity_type):
                                continue
                            count += activity_utils.get_redpoint_count_by_type(activity_type)

                else:
                    activity_type = a_info['activity_type']
                    count = activity_utils.get_redpoint_count_by_type(activity_type)
                if self.cur_tab_id == tab_id:
                    item_widget = tablist.GetItem(id)
                    item_widget.img_red.setVisible(count > 0)
                show_img_red = count > 0 or show_img_red

            item.img_red.setVisible(show_img_red)

        self._cur_view_sub_page_widget and self._cur_view_sub_page_widget.refresh_red_point()