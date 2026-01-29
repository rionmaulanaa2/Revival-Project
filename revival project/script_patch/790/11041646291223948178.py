# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivitySubPage.py
from __future__ import absolute_import
from logic.gutils import activity_utils
from common.cfg import confmgr
from .ActivityTemplate import ActivityBase
from logic.gcommon.item import item_const as iconst

class ActivitySubPage(ActivityBase):

    def __init__(self, dlg, activity_type):
        super(ActivitySubPage, self).__init__(dlg, activity_type)
        self.init_parameters()
        self.init_event()

    def on_finalize_panel(self):
        self.process_event(False)

    def init_parameters(self):
        self._page_list = []
        self._select_callback = None
        return

    def init_event(self):
        self.process_event(True)

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {}
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def set_select_callback(self, callback):
        self._select_callback = callback

    def select_tab(self, activity_type, is_init=False):
        if self._select_callback:
            self._select_callback(activity_type, is_init)
        tablist = self.panel.pnl_list_tab
        if not tablist:
            return
        activity_list = self._page_list
        all_items = tablist.GetAllItem()
        for index, item_widget in enumerate(all_items):
            a_type = activity_list[index]['activity_type']
            if a_type == activity_type:
                item_widget.btn_top.SetSelect(True)
            else:
                item_widget.btn_top.SetSelect(False)

    def show_page_list(self, page_list, sel_activity_type=None):
        self._page_list = page_list
        tablist = self.panel.pnl_list_tab
        if not tablist:
            return
        else:
            count = len(self._page_list)
            tablist.DeleteAllSubItem()
            tablist.SetInitCount(count)
            do_click = None
            for index, a_info in enumerate(self._page_list):
                item_widget = tablist.GetItem(index)
                activity_type = a_info['activity_type']
                tab_name_id = confmgr.get('c_activity_config', activity_type, 'cNameTextID', default='')

                @item_widget.btn_top.callback()
                def OnClick(btn, touch, activity_type=activity_type, is_init=False):
                    self.select_tab(activity_type, is_init=is_init)

                if sel_activity_type == activity_type:
                    do_click = OnClick
                if tab_name_id:
                    if item_widget.lab:
                        item_widget.lab.SetString(int(tab_name_id))
                    else:
                        item_widget.btn_top.SetText(int(tab_name_id))
                item_widget.setVisible(bool(tab_name_id))

            do_click and do_click(None, None, is_init=True)
            tablist.RefreshItemPos(is_cal_visible=True)
            return

    def refresh_red_point(self):
        tablist = self.panel.pnl_list_tab
        if not tablist:
            return
        for index, a_info in enumerate(self._page_list):
            item_widget = tablist.GetItem(index)
            activity_type = a_info['activity_type']
            count = activity_utils.get_redpoint_count_by_type(activity_type)
            item_widget.img_red.setVisible(count > 0)

    def on_init_panel(self):
        pass

    def refresh_bow_cnt(self):
        if not global_data.player:
            return
        bow_cnt = global_data.player.get_item_num_by_no(iconst.ITEM_NO_MILA_BOW)
        if self.panel.lab_num:
            self.panel.lab_num.SetString(str(bow_cnt))