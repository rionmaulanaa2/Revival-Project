# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/setting_ui/SettingWidget/BusiniessLawSettingWidget.py
from __future__ import absolute_import
from six.moves import range
from logic.gcommon.common_utils.local_text import get_text_by_id
from .SettingWidgetBase import SettingWidgetBase

class BusiniessLawSettingWidget(SettingWidgetBase):

    def __init__(self, panel, parent):
        super(BusiniessLawSettingWidget, self).__init__(panel, parent)

    def on_init_panel(self, **kwargs):
        self.init_setting(self.panel)

    def on_exit_page(self, **kwargs):
        super(BusiniessLawSettingWidget, self).on_exit_page()

    def on_recover_default(self, **kwargs):
        pass

    def init_setting(self, page):
        self.list_items = [{'text_id': 2232,'announce_title': 2235,'announce_msg': 2236,'OnClick': self._show_announcement}, {'text_id': 2233,'announce_title': 2237,'announce_msg': 2238,'OnClick': self._show_announcement}, {'text_id': 2231,'OnClick': self._show_sdk_content}]
        count = len(self.list_items)
        tablist = self.panel.list_law
        tablist.DeleteAllSubItem()
        tablist.SetInitCount(count)
        for i in range(count):
            ui_item = tablist.GetItem(i)
            item_data = self.list_items[i]
            if not ui_item or not item_data:
                continue
            ui_item.lab_law_name.SetString(get_text_by_id(item_data.get('text_id')))

            @ui_item.btn_check.btn_common.unique_callback()
            def OnClick(btn, touch, item_info=item_data):
                call_back = item_info.get('OnClick')
                if call_back:
                    call_back(item_info)

    def _show_announcement(self, item_data):
        title_text_id, msg_id = item_data.get('announce_title'), item_data.get('announce_msg')
        ui = global_data.ui_mgr.show_ui('AnnouncementUI', 'logic.comsys.announcement')
        if ui:
            ui.show_content(title_text_id, get_text_by_id(msg_id))

    def _show_sdk_content(self, item_data):
        global_data.channel.show_compact_view()