# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/setting_ui/SettingWidget/HighLightSettingWidget.py
from __future__ import absolute_import
from six.moves import range
from .SettingWidgetBase import SettingWidgetBase
from logic.gcommon.common_const import ui_operation_const as uoc
from logic.comsys.video.video_record_utils import close_free_record, close_and_show_free_record_ui, MAX_SHARE_DAY_NUM

class HighLightSettingWidget(SettingWidgetBase):

    def on_exit_page(self, **kwargs):
        global_data.emgr.on_upload_file_day_nums_changed -= self._update_left_share_num
        super(HighLightSettingWidget, self).on_exit_page()
        self.save_setting()

    def save_setting(self):
        if not global_data.player:
            return
        need_save = False
        for idx in range(len(uoc.HIGH_LIGHT_DEF_SETTING)):
            if self._setting[idx] != self._init_setting[idx]:
                need_save = True
                global_data.player.write_setting_2(uoc.HIGH_LIGHT_DEF_KEYS[idx], self._setting[idx], True)

        if need_save:
            global_data.player.save_settings_to_file()

    def on_recover_default(self, **kwargs):
        self._setting = uoc.HIGH_LIGHT_DEF_SETTING
        high_light_enable = self._setting[0]
        high_light_times = self._setting[1]
        free_record_video = self._setting[2]
        self._set_high_light_enable(high_light_enable)
        self._set_free_record_enable(free_record_video)

    def __init__(self, panel, parent):
        super(HighLightSettingWidget, self).__init__(panel, parent)
        self._init_setting = uoc.HIGH_LIGHT_DEF_SETTING
        self._setting = uoc.HIGH_LIGHT_DEF_SETTING

    def on_init_panel(self, **kwargs):
        global_data.emgr.on_upload_file_day_nums_changed += self._update_left_share_num
        self._update_left_share_num()
        high_light_enable = global_data.player.get_setting_2(uoc.HIGH_LIGHT_KEY)
        high_light_times = uoc.HIGH_LIGHT_TIMES_DEF
        free_record_video = global_data.player.get_setting_2(uoc.FREE_RECORD_VIDEO_KEY)
        high_light_enable = True if high_light_enable else False
        free_record_video = True if free_record_video else False
        if high_light_enable and free_record_video:
            free_record_video = False
            global_data.player.write_setting_2(uoc.FREE_RECORD_VIDEO_KEY, True, True)
        self._set_high_light_enable(high_light_enable)
        self._set_free_record_enable(free_record_video)
        self._init_setting = [
         high_light_enable, high_light_times, free_record_video]
        self._setting = [high_light_enable, high_light_times, free_record_video]
        high_light_node = self.panel.nd_highlight_detail.choose_1
        free_node = self.panel.nd_highlight_detail.choose_2
        if global_data.achi_mgr.get_cur_user_archive_data('setting_red_point_high_light') is None:
            global_data.achi_mgr.set_cur_user_archive_data('setting_red_point_high_light', 1)

        @high_light_node.choose_1.btn.unique_callback()
        def OnClick(btn, touch):
            self._set_high_light_enable(True)
            self._set_free_record_enable(False)
            self._setting[0] = True
            if self._setting[2]:
                self._setting[2] = False
                close_free_record()

        @high_light_node.choose_2.btn.unique_callback()
        def OnClick(btn, touch):
            self._set_high_light_enable(False)
            self._setting[0] = False

        @free_node.choose_1.btn.unique_callback()
        def OnClick(btn, touch):
            self._set_high_light_enable(False)
            self._set_free_record_enable(True)
            self._setting[0] = False
            if not self._setting[2]:
                self._setting[2] = True
                close_and_show_free_record_ui()

        @free_node.choose_2.btn.unique_callback()
        def OnClick(btn, touch):
            self._set_free_record_enable(False)
            if self._setting[2]:
                self._setting[2] = False
                close_free_record()

        return

    def _set_high_light_enable(self, enable):
        high_light_node = self.panel.nd_highlight_detail.choose_1
        high_light_node.choose_1.choose.setVisible(enable)
        high_light_node.choose_2.choose.setVisible(not enable)

    def _set_free_record_enable(self, enable):
        free_node = self.panel.nd_highlight_detail.choose_2
        free_node.choose_1.choose.setVisible(enable)
        free_node.choose_2.choose.setVisible(not enable)

    def _update_left_share_num(self, *args):
        from logic.gcommon.const import FILE_SERVICE_FUNCTION_KEY_HIGHLIGHT_MOMENT
        day_uploaded_num = global_data.player or 0 if 1 else global_data.player.get_file_day_upload_num(FILE_SERVICE_FUNCTION_KEY_HIGHLIGHT_MOMENT)
        left_num = 0 if day_uploaded_num >= MAX_SHARE_DAY_NUM else MAX_SHARE_DAY_NUM - day_uploaded_num
        self.panel.lab_left_num.SetString(get_text_by_id(2323).format(left_num))