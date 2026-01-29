# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/setting_ui/SettingWidget/QualitySettingWidget.py
from __future__ import absolute_import
import six
from six.moves import range
from logic.gcommon.common_const import ui_operation_const as uoc
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.comsys.common_ui.NormalConfirmUI import SecondConfirmDlg2
from .SettingWidgetBase import SettingWidgetBase
import logic.gcommon.time_utility as time_utils
from logic.gutils.pc_utils import adjust_setting_panel_pos_and_size
from logic.gutils.pc_resolution_utils import get_current_resolution
from logic.client.const import pc_const
import logic.vscene.global_display_setting as gds
from common.platform.dctool import interface
display_setting = gds.GlobalDisplaySeting()
import game3d
QUALITY_PANEL_INFO = {'nd_full_screen': {'box_type': 'radio_box','uc_key': uoc.PC_FULL_SCREEN_KEY},'nd_pc_ui': {'box_type': 'radio_box','uc_key': uoc.PC_HOTKEY_HINT_DISPLAY_OPTION_KEY},'nd_quality': {'box_type': 'radio_box','uc_key': uoc.QUALITY_LEVEL_KEY},'nd_pve_quality': {'box_type': 'radio_box','uc_key': uoc.PVE_QUALITY_LEVEL_KEY},'nd_digit': {'box_type': 'radio_box','uc_key': uoc.QUALITY_RESOLUTION_KEY},'nd_digit_yuanchudao': {'box_type': 'radio_box','uc_key': uoc.QUALITY_RESOLUTION_KEY_KONGDAO},'nd_frame_rate': {'box_type': 'radio_box','uc_key': uoc.QUALITY_HIGH_FRAME_RATE_KEY},'nd_shadow': {'box_type': 'check_box','uc_key': uoc.QUALITY_SHADOWMAP_KEY},'nd_hdr': {'box_type': 'check_box','uc_key': uoc.QUALITY_HDR_KEY},'nd_sawtooth': {'box_type': 'radio_box','uc_key': uoc.QUALITY_MSAA_KEY},'nd_effects': {'box_type': 'radio_box','uc_key': uoc.QUALITY_MECHA_EFFECT_LEVEL_KEY},'nd_other_effects': {'box_type': 'radio_box','uc_key': uoc.QUALITY_OTHER_MECHA_EFFECT_LEVEL_KEY},'nd_dynamic_fuzzy': {'box_type': 'check_box','uc_key': uoc.QUALITY_RADIAL_BLUR_KEY},'nd_grass': {'box_type': 'radio_box','uc_key': uoc.QUALITY_MEADOW_KEY}}
SYNC_SERVER_SETTING_BLACK_SET = {
 uoc.PC_FULL_SCREEN_KEY}
QUALITY_LEVEL_RELAVANT_SUB = {
 'nd_digit',
 'nd_shadow',
 'nd_hdr',
 'nd_sawtooth',
 'nd_grass'}
QUALITY_LEVEL_RELAVANT = QUALITY_LEVEL_RELAVANT_SUB | set(('nd_quality', )) | set(('nd_pve_quality', ))
FPS_LEVEL_30 = 0
FPS_LEVEL_60 = 1
FPS_LEVEL_MAX = 2
FPS_LEVEL_90 = 3
FPS_LEVEL_45 = 4

def cal_ios_fps_level(level):
    import device_compatibility
    new_level = level
    if game3d.get_platform() == game3d.PLATFORM_IOS and device_compatibility.get_max_screen_refresh_rate() >= 120:
        if new_level == FPS_LEVEL_90:
            new_level = FPS_LEVEL_60
        elif new_level == FPS_LEVEL_45:
            new_level = FPS_LEVEL_30
    return new_level


class QualitySettingWidget(SettingWidgetBase):

    def __init__(self, panel, parent):
        super(QualitySettingWidget, self).__init__(panel, parent)

    def on_init_panel(self, **kwargs):
        self.nd_guide_frame_rate = None
        self.init_quality_level(self.panel)
        self.show_frame_rate_limit = None
        from logic.gutils import device_utils
        if device_utils.check_vivo_device():
            hide_list = [
             self.panel.nd_digit_yuanchudao]
        else:
            hide_list = []
        if not global_data.is_pc_mode:
            hide_list.append(self.panel.nd_full_screen)
        elif global_data.is_android_pc:
            hide_list.append(self.panel.nd_full_screen)
        adjust_setting_panel_pos_and_size(self.parent.panel.content_bar.page, self.parent, self.panel, hide_list=hide_list)
        return

    def destroy(self):
        self.nd_guide_frame_rate = None
        return

    def on_enter_page(self, **kwargs):
        super(QualitySettingWidget, self).on_enter_page()
        self.show_setting_widget_frame_rate()
        self._refresh_sync_server_btn_enable()

    def on_exit_page(self, **kwargs):
        super(QualitySettingWidget, self).on_exit_page()
        self.sync_setting_data()

    def _get_settings_available_on_pc(self):
        ret_set = set()
        if not self.panel:
            return ret_set
        else:
            for node_name in QUALITY_PANEL_INFO:
                node = getattr(self.panel, node_name)
                if not node or not node.isVisible():
                    continue
                panel_info = QUALITY_PANEL_INFO[node_name]
                uc_key = panel_info.get('uc_key', None)
                if not uc_key:
                    continue
                ret_set.add(uc_key)

            return ret_set

    def _get_out_of_sync_settings(self):
        ret_set = set()
        pc_settings = self._get_settings_available_on_pc()
        for setting_key in pc_settings:
            if setting_key in SYNC_SERVER_SETTING_BLACK_SET:
                continue
            if global_data.player and global_data.player.is_setting_out_of_sync_2(setting_key):
                ret_set.add(setting_key)

        return ret_set

    def should_btn_sync_server_enabled(self):
        if not global_data.is_pc_mode:
            return False
        out_of_sync_settings = self._get_out_of_sync_settings()
        return bool(out_of_sync_settings)

    def on_sync_to_server(self, **kwargs):
        out_of_sync_settings = self._get_out_of_sync_settings()
        if not out_of_sync_settings:
            return
        for setting_key in out_of_sync_settings:
            global_data.player.sync_setting_to_server_2(setting_key)

        self._refresh_sync_server_btn_enable()

    def on_recover_default(self, **kwargs):
        self.recover_quality_level()
        self.recover_pve_quality_level()
        self.graph_styly_reset()
        self.redirect_scale_reset()
        archive_data = global_data.achi_mgr.get_general_archive_data()
        if archive_data:
            archive_data.del_field(uoc.PC_FULL_SCREEN_KEY)
        default_val = self._get_default_setting(global_data.player, uoc.QUALITY_HIGH_FRAME_RATE_KEY)
        self._write_setting(global_data.player, uoc.QUALITY_HIGH_FRAME_RATE_KEY, default_val, False)
        display_setting.reset_frame_rate()
        if global_data.pc_ctrl_mgr:
            global_data.pc_ctrl_mgr.set_hotkey_hint_display_option(pc_const.PC_HOTKEY_HINT_DISPLAY_OPTION_VAL_DEFAULT, True)
        self.sync_setting_data()
        page = self.panel
        self.refresh_all_btn(page, exclude=QUALITY_LEVEL_RELAVANT - {'nd_digit'})
        self._refresh_sync_server_btn_enable()
        if global_data.pc_ctrl_mgr:
            default_pc_fullscreen_val = uoc.LOCAL_SETTING_CONF.get(uoc.PC_FULL_SCREEN_KEY, False)
            archive_data = global_data.achi_mgr.get_general_archive_data()
            pc_fullscreen_val = archive_data.get_field(uoc.PC_FULL_SCREEN_KEY, default=default_pc_fullscreen_val)
            global_data.pc_ctrl_mgr.request_fullscreen(pc_fullscreen_val, req_from_setting_ui=True, persistent=False)

    def recover_quality_level(self):
        page = self.panel
        panel_quality = getattr(page, 'nd_quality')
        choose = panel_quality.choose
        level = global_data.game_mgr.gds.get_default_quality()
        self.on_set_quality_level(page, choose, True, level)
        self.refresh_all_btn(page, only_include=('nd_quality', ), default_reset_level=level)

    def recover_pve_quality_level(self):
        page = self.panel
        panel_quality = getattr(page, 'nd_pve_quality')
        choose = panel_quality.choose
        level = global_data.game_mgr.gds.get_default_quality()
        self.on_set_quality_level(page, choose, True, level, True)
        self.refresh_all_btn(page, only_include=('nd_pve_quality', ), default_reset_level=level)

    def sync_setting_data(self):
        if global_data.player:
            global_data.player.save_settings_to_file()

    def on_set_quality_level(self, page, choose, trigger_event, level, is_pve=False):
        import logic.vscene.global_display_setting as gds
        import device_compatibility
        display_setting = gds.GlobalDisplaySeting()
        if not choose:
            return
        if is_pve:
            old_quality = display_setting.get_pve_quality()
        else:
            old_quality = display_setting.get_quality()
        if old_quality != level:
            global_data.game_mgr.show_tip(get_text_by_id(2230))
            perf_flag = device_compatibility.get_device_perf_flag()
            if perf_flag in (device_compatibility.PERF_FLAG_ANDROID_LOW, device_compatibility.PERF_FLAG_IOS_LOW) and level > old_quality:

                def cancel_callback():
                    self.refresh_all_btn(page)

                def confirm_callback():
                    if is_pve:
                        display_setting.set_pve_quality(level)
                        self._write_setting(global_data.player, uoc.PVE_QUALITY_LEVEL_KEY, level, False)
                    else:
                        display_setting.set_quality(level)
                        self._write_setting(global_data.player, uoc.QUALITY_LEVEL_KEY, level, False)
                    if trigger_event:
                        self.refresh_all_btn(page, only_include=QUALITY_LEVEL_RELAVANT_SUB, default_reset_level=level)

                SecondConfirmDlg2(parent=self.panel).confirm(content=get_text_by_id(2324), confirm_callback=confirm_callback, cancel_callback=cancel_callback, click_blank_close=False)
            else:
                if is_pve:
                    display_setting.set_pve_quality(level)
                    self._write_setting(global_data.player, uoc.PVE_QUALITY_LEVEL_KEY, level, False)
                else:
                    display_setting.set_quality(level)
                    self._write_setting(global_data.player, uoc.QUALITY_LEVEL_KEY, level, False)
                if trigger_event:
                    self.refresh_all_btn(page, only_include=QUALITY_LEVEL_RELAVANT_SUB, default_reset_level=level)

    def do_enable_fps_level(self, page, level):
        import logic.vscene.global_display_setting as gds
        display_setting = gds.GlobalDisplaySeting()
        self._write_setting(global_data.player, uoc.QUALITY_HIGH_FRAME_RATE_KEY, level, False)
        display_setting.reset_frame_rate()
        if level not in [FPS_LEVEL_60, FPS_LEVEL_30, FPS_LEVEL_45] and (display_setting.get_quality() > 0 or display_setting.get_pve_quality() > 0) and not global_data.is_pc_mode:
            display_setting.set_quality(0)
            display_setting.set_pve_quality(0)
            self._write_setting(global_data.player, uoc.QUALITY_LEVEL_KEY, 0, False)
            self._write_setting(global_data.player, uoc.PVE_QUALITY_LEVEL_KEY, 0, False)
            self.refresh_all_btn(page, only_include=QUALITY_LEVEL_RELAVANT)

    def refresh_all_btn(self, page, exclude=(), only_include=(), default_reset_level=-1):
        from logic.gutils.template_utils import set_radio_group_item_select, set_check_box_group_item_select
        import logic.vscene.global_display_setting as gds
        if default_reset_level != -1:
            if global_data.is_pc_mode:
                for uc_key, level_info in six.iteritems(gds.USER_PC_CUSTOM_DEFAULT_SETTINGS):
                    self._write_setting(global_data.player, uc_key, level_info[default_reset_level], True)

            else:
                for uc_key, level_info in six.iteritems(gds.USER_CUSTOM_DEFAULT_SETTINGS):
                    self._write_setting(global_data.player, uc_key, level_info[default_reset_level], True)

            global_data.player.save_settings_to_file()
        for panel_name, info in six.iteritems(QUALITY_PANEL_INFO):
            if only_include and panel_name not in only_include:
                continue
            if panel_name in exclude:
                continue
            panel = getattr(page, panel_name)
            if not panel:
                continue
            choose = panel.choose
            box_type = info.get('box_type', None)
            uc_key = info.get('uc_key', None)
            if uc_key == uoc.PC_FULL_SCREEN_KEY:
                if not global_data.pc_ctrl_mgr:
                    setting_val = False
                else:
                    setting_val = global_data.pc_ctrl_mgr.is_fullscreen()
            elif uc_key == uoc.PC_HOTKEY_HINT_DISPLAY_OPTION_KEY:
                if not global_data.pc_ctrl_mgr:
                    setting_val = pc_const.PC_HOTKEY_HINT_DISPLAY_OPTION_VAL_DEFAULT
                else:
                    setting_val = global_data.pc_ctrl_mgr.get_hotkey_hint_display_option()
            elif uc_key == uoc.QUALITY_MEADOW_KEY:
                setting_val = global_data.gsetting.get_meadow_quality()
            else:
                setting_val = self._get_setting(global_data.player, uc_key)
                if uc_key == uoc.QUALITY_HIGH_FRAME_RATE_KEY:
                    setting_val = cal_ios_fps_level(setting_val)
            if choose:
                if box_type == 'radio_box':
                    set_radio_group_item_select(choose, setting_val, False)
                elif box_type == 'check_box':
                    set_check_box_group_item_select(choose, uc_key, setting_val == 1, trigger_event=False)

        return

    def init_quality_level(self, page):
        from logic.gutils.template_utils import init_radio_group, init_checkbox_group, set_radio_group_item_select, attach_radio_group_data, attach_checkbox_group_data, set_check_box_group_item_select
        panel_full_screen = getattr(page, 'nd_full_screen')
        choose = panel_full_screen.choose
        init_radio_group(choose)
        attach_radio_group_data([choose.choose_1, choose.choose_2], [
         True, False])

        @choose.choose_1.callback()
        def OnSelect(btn, choose, trigger_event):
            if trigger_event and choose:
                if global_data.pc_ctrl_mgr:
                    if global_data.pc_ctrl_mgr.request_fullscreen(True, req_from_setting_ui=True):
                        archive_data = global_data.achi_mgr.get_general_archive_data()
                        archive_data.set_field(uoc.PC_FULL_SCREEN_KEY, True)

        @choose.choose_2.callback()
        def OnSelect(btn, choose, trigger_event):
            if trigger_event and choose:
                if global_data.pc_ctrl_mgr:
                    if global_data.pc_ctrl_mgr.request_fullscreen(False, req_from_setting_ui=True):
                        archive_data = global_data.achi_mgr.get_general_archive_data()
                        archive_data.set_field(uoc.PC_FULL_SCREEN_KEY, False)

        panel_pc_hotkey_hint = getattr(page, 'nd_pc_ui')
        choose = panel_pc_hotkey_hint.choose
        init_radio_group(choose)
        attach_radio_group_data([choose.choose_1, choose.choose_3], [
         pc_const.PC_HOTKEY_HINT_DIPLAY_OPTION_VAL_HIDE, pc_const.PC_HOTKEY_HINT_DISPLAY_OPTION_VAL_TEXT])

        def on_selected(option_val):
            if global_data.pc_ctrl_mgr:
                global_data.pc_ctrl_mgr.set_hotkey_hint_display_option(option_val, True)
                self._refresh_sync_server_btn_enable()

        @choose.choose_1.callback()
        def OnSelect(btn, choose, trigger_event):
            if trigger_event and choose:
                on_selected(pc_const.PC_HOTKEY_HINT_DIPLAY_OPTION_VAL_HIDE)

        @choose.choose_3.callback()
        def OnSelect(btn, choose, trigger_event):
            if trigger_event and choose:
                on_selected(pc_const.PC_HOTKEY_HINT_DISPLAY_OPTION_VAL_TEXT)

        import device_compatibility
        panel_quality = getattr(page, 'nd_quality')
        choose = panel_quality.choose
        init_radio_group(choose)
        attach_radio_group_data([choose.choose_1, choose.choose_2, choose.choose_3, choose.choose_4], [
         0, 1, 2, 3])
        if global_data.is_pc_mode:
            choose_1_text_id = 19713
        else:
            choose_1_text_id = 80804
        choose.choose_1.text.SetString(choose_1_text_id)

        def on_notice_battery_warning(choose, trigger_event, callback, tips=81034, args=()):
            if not choose:
                return

            def confirm_callback():
                if global_data.player:
                    if callback:
                        callback(*args)

            def cancel_callback():
                self.refresh_all_btn(page)

            if trigger_event and choose:
                SecondConfirmDlg2(parent=self.panel).confirm(content=get_text_by_id(tips), confirm_callback=confirm_callback, cancel_callback=cancel_callback)

        def on_notice_high_quality_fps_warning(choose, trigger_event, level, is_pve=False):
            if not choose:
                return

            def confirm_callback():
                self.on_set_quality_level(page, choose, trigger_event, level, is_pve)
                if level > 0 and display_setting.quality_value('HIGH_FRAME_RATE') not in [FPS_LEVEL_60, FPS_LEVEL_30, FPS_LEVEL_45] and not global_data.is_pc_mode:
                    self.do_enable_fps_level(page, FPS_LEVEL_60)
                    self.refresh_all_btn(page)
                if trigger_event and choose:
                    self.check_frame_rate_red_point()

            if level > 0 and display_setting.quality_value('HIGH_FRAME_RATE') not in [FPS_LEVEL_60, FPS_LEVEL_30, FPS_LEVEL_45] and not global_data.is_pc_mode:

                def cancel_callback():
                    self.refresh_all_btn(page)

                SecondConfirmDlg2(parent=self.panel).confirm(content=get_text_by_id(609404), confirm_callback=confirm_callback, cancel_callback=cancel_callback, click_blank_close=False)
            else:
                confirm_callback()

        def on_notice_high_quality_warning(choose, trigger_event, level, is_pve=False):
            if not choose:
                return

            def confirm_callback():
                on_notice_high_quality_fps_warning(choose, trigger_event, level, is_pve)
                if trigger_event and choose:
                    self.check_frame_rate_red_point()

            perf_flag = device_compatibility.get_device_perf_flag()
            if perf_flag in (device_compatibility.PERF_FLAG_ANDROID_LOW, device_compatibility.PERF_FLAG_IOS_LOW):
                confirm_callback()
            else:
                default_level = global_data.game_mgr.gds.get_default_quality()
                if is_pve:
                    old_quality = global_data.game_mgr.gds.get_pve_quality()
                else:
                    old_quality = global_data.game_mgr.gds.get_quality()
                if level <= default_level or level <= old_quality or global_data.is_pc_mode:
                    confirm_callback()
                    return

                def cancel_callback():
                    self.refresh_all_btn(page)

                SecondConfirmDlg2(parent=self.panel).confirm(content=get_text_by_id(218), confirm_callback=confirm_callback, cancel_callback=cancel_callback, click_blank_close=False)

        @choose.choose_1.callback()
        def OnSelect(btn, choose, trigger_event):
            self.on_set_quality_level(page, choose, trigger_event, 0)

        @choose.choose_2.callback()
        def OnSelect(btn, choose, trigger_event):
            on_notice_high_quality_warning(choose, trigger_event, 1)

        @choose.choose_3.callback()
        def OnSelect(btn, choose, trigger_event):
            on_notice_high_quality_warning(choose, trigger_event, 2)

        @choose.choose_4.callback()
        def OnSelect(btn, choose, trigger_event):
            on_notice_high_quality_warning(choose, trigger_event, 3)

        panel_pve_quality = getattr(page, 'nd_pve_quality')
        choose = panel_pve_quality.choose
        init_radio_group(choose)
        attach_radio_group_data([choose.choose_1, choose.choose_2, choose.choose_3, choose.choose_4], [
         0, 1, 2, 3])
        if global_data.is_pc_mode:
            choose_1_text_id = 19713
        else:
            choose_1_text_id = 80804
        choose.choose_1.text.SetString(choose_1_text_id)

        @choose.choose_1.callback()
        def OnSelect(btn, choose, trigger_event):
            self.on_set_quality_level(page, choose, trigger_event, 0, True)

        @choose.choose_2.callback()
        def OnSelect(btn, choose, trigger_event):
            on_notice_high_quality_warning(choose, trigger_event, 1, True)

        @choose.choose_3.callback()
        def OnSelect(btn, choose, trigger_event):
            on_notice_high_quality_warning(choose, trigger_event, 2, True)

        @choose.choose_4.callback()
        def OnSelect(btn, choose, trigger_event):
            on_notice_high_quality_warning(choose, trigger_event, 3, True)

        def set_resolution(name, key):
            panel_digit = getattr(page, name)
            choose = panel_digit.choose
            init_radio_group(choose)
            attach_radio_group_data([choose.choose_1, choose.choose_2, choose.choose_3, choose.choose_4], [
             0, 1, 2, 3])

            @choose.choose_1.callback()
            def OnSelect(btn, choose, trigger_event):
                if choose:
                    self._write_setting(global_data.player, key, 0, True)
                    if key == uoc.QUALITY_RESOLUTION_KEY:
                        display_setting.set_detail_setting_resolution(0)

            @choose.choose_2.callback()
            def OnSelect(btn, choose, trigger_event):
                if choose:
                    self._write_setting(global_data.player, key, 1, True)
                    if key == uoc.QUALITY_RESOLUTION_KEY:
                        display_setting.set_detail_setting_resolution(1)

            @choose.choose_3.callback()
            def OnSelect(btn, choose, trigger_event):
                if choose:
                    self._write_setting(global_data.player, key, 2, True)
                    if key == uoc.QUALITY_RESOLUTION_KEY:
                        display_setting.set_detail_setting_resolution(2)

            @choose.choose_4.callback()
            def OnSelect(btn, choose, trigger_event):
                if choose:
                    self._write_setting(global_data.player, key, 3, True)
                    if key == uoc.QUALITY_RESOLUTION_KEY:
                        display_setting.set_detail_setting_resolution(3)

        set_resolution('nd_digit', uoc.QUALITY_RESOLUTION_KEY)
        set_resolution('nd_digit_yuanchudao', uoc.QUALITY_RESOLUTION_KEY_KONGDAO)
        self.init_redirect_scale()
        panel_frame_rate = getattr(page, 'nd_frame_rate')
        panel_frame_rate.setVisible(True)
        choose = panel_frame_rate.choose
        init_radio_group(choose)
        is_ios_high_fps = False
        if global_data.enable_high_fps and game3d.get_platform() == game3d.PLATFORM_IOS and device_compatibility.get_max_screen_refresh_rate() >= 120:
            is_ios_high_fps = True
        if is_ios_high_fps:
            attach_radio_group_data([choose.choose_1, choose.choose_2, choose.choose_3], [
             FPS_LEVEL_30, FPS_LEVEL_60, FPS_LEVEL_MAX, FPS_LEVEL_MAX, FPS_LEVEL_MAX])
        else:
            attach_radio_group_data([choose.choose_1, choose.choose_2, choose.choose_3, choose.choose_4, choose.choose_5], [
             FPS_LEVEL_30, FPS_LEVEL_45, FPS_LEVEL_60, FPS_LEVEL_90, FPS_LEVEL_MAX])

        def do_select_high_fps(toggle, trigger_event, level):
            if device_compatibility.can_use_high_fps():
                if global_data.is_pc_mode:
                    self.do_enable_fps_level(page, level)
                else:
                    on_notice_battery_warning(toggle, trigger_event, self.do_enable_fps_level, 609403, (page, level))
            elif toggle:
                from logic.comsys.common_ui.NormalConfirmUI import NormalConfirmUI2
                NormalConfirmUI2().init_widget(content=get_text_by_id(81391))
                self.refresh_all_btn(page)

        @choose.choose_1.callback()
        def OnSelect(btn, choose, trigger_event):
            self.do_enable_fps_level(page, FPS_LEVEL_30)

        @choose.choose_2.callback()
        def OnSelect(btn, toggle, trigger_event):
            if game3d.get_platform() == game3d.PLATFORM_IOS:
                if not global_data.feature_mgr.is_fix_ios_framerate():
                    if trigger_event:
                        global_data.game_mgr.show_tip(get_text_by_id(2343))
                        self.refresh_all_btn(page)
                        return
                    return
            if is_ios_high_fps:
                self.do_enable_fps_level(page, FPS_LEVEL_60)
            else:
                self.do_enable_fps_level(page, FPS_LEVEL_45)

        @choose.choose_3.callback()
        def OnSelect(btn, toggle, trigger_event):
            if is_ios_high_fps:
                do_select_high_fps(toggle, trigger_event, FPS_LEVEL_MAX)
            else:
                self.do_enable_fps_level(page, FPS_LEVEL_60)

        @choose.choose_4.callback()
        def OnSelect(btn, toggle, trigger_event):
            do_select_high_fps(toggle, trigger_event, FPS_LEVEL_90)

        @choose.choose_5.callback()
        def OnSelect(btn, toggle, trigger_event):
            do_select_high_fps(toggle, trigger_event, FPS_LEVEL_MAX)

        if global_data.enable_high_fps:
            if global_data.is_pc_mode and not global_data.is_android_pc:
                choose.choose_4.setVisible(True)
                choose.choose_5.setVisible(True)
                choose.choose_5.btn.text.SetString(860061)
            else:
                max_fresh_rate = device_compatibility.get_max_screen_refresh_rate()
                if is_ios_high_fps:
                    choose.choose_4.setVisible(False)
                    choose.choose_5.setVisible(False)
                    choose.choose_2.btn.text.SetString(860055)
                    choose.choose_3.btn.text.SetString(860057)
                else:
                    choose.choose_4.setVisible(max_fresh_rate >= 90)
                    choose.choose_5.setVisible(max_fresh_rate >= 120)
                    if max_fresh_rate > 120:
                        text_id = 860061 if 1 else 860057
                        choose.choose_5.btn.text.SetString(text_id)
                    panel_quality = getattr(page, 'nd_grass')
                    is_snow_res = global_data.game_mode and global_data.game_mode.is_snow_res()
                    panel_quality.setVisible(global_data.enable_meadow and not is_snow_res)
                    choose = panel_quality.choose
                    init_radio_group(choose)
                    attach_radio_group_data([choose.choose_1, choose.choose_2, choose.choose_3, choose.choose_4], [
                     0, 1, 2, 3])

                    def set_meadow_quality_level(level, trigger_event):
                        global_data.game_mgr.gds.set_meadow_quality(level)

                    @choose.choose_1.callback()
                    def OnSelect(btn, choose, trigger_event):
                        if choose:
                            set_meadow_quality_level(0, trigger_event)

                    @choose.choose_2.callback()
                    def OnSelect(btn, choose, trigger_event):
                        if choose:
                            set_meadow_quality_level(1, trigger_event)

                    @choose.choose_3.callback()
                    def OnSelect(btn, choose, trigger_event):
                        if choose:
                            set_meadow_quality_level(2, trigger_event)

                    @choose.choose_4.callback()
                    def OnSelect(btn, choose, trigger_event):
                        if choose:
                            set_meadow_quality_level(3, trigger_event)

                    panel_shadow = getattr(page, 'nd_shadow')
                    choose = panel_shadow.choose
                    init_checkbox_group(choose)
                    attach_checkbox_group_data(choose, (uoc.QUALITY_SHADOWMAP_KEY,))

                    @choose.choose_1_1.callback()
                    def OnSelect(btn, choose, trigger_event):
                        if trigger_event:
                            if choose:

                                def cb():
                                    if global_data.player:
                                        self._write_setting(global_data.player, uoc.QUALITY_SHADOWMAP_KEY, 1, True)
                                        if game3d.get_platform() != game3d.PLATFORM_IOS:
                                            SecondConfirmDlg2(parent=self.panel).confirm(content=get_text_by_id(81466), confirm_callback=lambda : global_data.game_mgr.try_restart_app())

                                if not global_data.is_pc_mode:
                                    on_notice_battery_warning(choose, trigger_event, cb)
                                else:
                                    cb()
                            else:
                                self._write_setting(global_data.player, uoc.QUALITY_SHADOWMAP_KEY, 0, True)

                    panel_hdr = getattr(page, 'nd_hdr')
                    choose = panel_hdr.choose
                    init_checkbox_group(choose)
                    attach_checkbox_group_data(choose, (uoc.QUALITY_HDR_KEY,))

                    @choose.choose_1_1.callback()
                    def OnSelect(btn, choose, trigger_event):
                        if trigger_event:

                            def on_changed_hdr():
                                import logic.vscene.global_display_setting as gds
                                display_setting = gds.GlobalDisplaySeting()
                                if display_setting:
                                    display_setting.refresh_hdr()

                            if choose:
                                self._write_setting(global_data.player, uoc.QUALITY_HDR_KEY, 1, True)
                                on_changed_hdr()
                            else:
                                self._write_setting(global_data.player, uoc.QUALITY_HDR_KEY, 0, True)
                                on_changed_hdr()

                    if not device_compatibility.can_use_hdr():
                        set_check_box_group_item_select(choose, uoc.QUALITY_HDR_KEY, False, trigger_event=False)
                    if global_data.is_ue_model:
                        panel_graphics_style = getattr(page, 'nd_graphics_style')
                        self.init_graph_styly(panel_graphics_style)
                    panel_sawtooth = getattr(page, 'nd_sawtooth')
                    choose = panel_sawtooth.choose
                    init_radio_group(choose)
                    attach_radio_group_data([choose.choose_1, choose.choose_2, choose.choose_3], [0, 1, 2])
                    device_compatibility.can_use_msaa() or choose.choose_2.setVisible(False)
                    choose.choose_3.setVisible(False)
                    if global_data.player:
                        self._write_setting(global_data.player, uoc.QUALITY_MSAA_KEY, 0, True)

        @choose.choose_1.callback()
        def OnSelect(btn, choose, trigger_event):
            if choose:
                display_setting.set_detail_setting_msaa(0)
                self._write_setting(global_data.player, uoc.QUALITY_MSAA_KEY, 0, True)

        @choose.choose_2.callback()
        def OnSelect(btn, choose, trigger_event):
            if choose and device_compatibility.can_use_msaa():
                display_setting.set_detail_setting_msaa(1)
                self._write_setting(global_data.player, uoc.QUALITY_MSAA_KEY, 1, True)

        @choose.choose_3.callback()
        def OnSelect(btn, choose, trigger_event):
            if choose and device_compatibility.can_use_msaa():

                def onSetMsaa2():
                    display_setting.set_detail_setting_msaa(2)
                    if global_data.player:
                        self._write_setting(global_data.player, uoc.QUALITY_MSAA_KEY, 2, True)

                if not global_data.is_pc_mode:
                    on_notice_battery_warning(choose, trigger_event, onSetMsaa2)
                else:
                    onSetMsaa2()

        page.nd_effects.setVisible(True)
        page.nd_other_effects.setVisible(True)
        panel_quality = getattr(page, 'nd_effects')
        choose = panel_quality.choose
        init_radio_group(choose)
        attach_radio_group_data([
         choose.choose_1, choose.choose_2, choose.choose_3, choose.choose_4], [
         uoc.MECHA_EFFECT_LEVEL_LOW, uoc.MECHA_EFFECT_LEVEL_MEDIUM, uoc.MECHA_EFFECT_LEVEL_HIGH, uoc.MECHA_EFFECT_LEVEL_ULTRA])

        @choose.choose_1.callback()
        def OnSelect(btn, choose, trigger_event):
            if choose:
                self._write_setting(global_data.player, uoc.QUALITY_MECHA_EFFECT_LEVEL_KEY, uoc.MECHA_EFFECT_LEVEL_LOW, True)
                global_data.emgr.set_mecha_effect_level.emit(uoc.MECHA_EFFECT_LEVEL_LOW, True)

        @choose.choose_2.callback()
        def OnSelect(btn, choose, trigger_event):
            if choose:
                self._write_setting(global_data.player, uoc.QUALITY_MECHA_EFFECT_LEVEL_KEY, uoc.MECHA_EFFECT_LEVEL_MEDIUM, True)
                global_data.emgr.set_mecha_effect_level.emit(uoc.MECHA_EFFECT_LEVEL_MEDIUM, True)

        @choose.choose_3.callback()
        def OnSelect(btn, choose, trigger_event):
            if choose:
                self._write_setting(global_data.player, uoc.QUALITY_MECHA_EFFECT_LEVEL_KEY, uoc.MECHA_EFFECT_LEVEL_HIGH, True)
                global_data.emgr.set_mecha_effect_level.emit(uoc.MECHA_EFFECT_LEVEL_HIGH, True)

        @choose.choose_4.callback()
        def OnSelect(btn, choose, trigger_event):
            if choose:
                self._write_setting(global_data.player, uoc.QUALITY_MECHA_EFFECT_LEVEL_KEY, uoc.MECHA_EFFECT_LEVEL_ULTRA, True)
                global_data.emgr.set_mecha_effect_level.emit(uoc.MECHA_EFFECT_LEVEL_ULTRA, True)

        panel_quality = getattr(page, 'nd_other_effects')
        choose = panel_quality.choose
        init_radio_group(choose)
        attach_radio_group_data([
         choose.choose_1, choose.choose_2, choose.choose_3, choose.choose_4], [
         uoc.MECHA_EFFECT_LEVEL_LOW, uoc.MECHA_EFFECT_LEVEL_MEDIUM, uoc.MECHA_EFFECT_LEVEL_HIGH,
         uoc.MECHA_EFFECT_LEVEL_ULTRA])

        @choose.choose_1.callback()
        def OnSelect(btn, choose, trigger_event):
            if choose:
                self._write_setting(global_data.player, uoc.QUALITY_OTHER_MECHA_EFFECT_LEVEL_KEY, uoc.MECHA_EFFECT_LEVEL_LOW, True)
                global_data.emgr.set_mecha_effect_level.emit(uoc.MECHA_EFFECT_LEVEL_LOW, False)

        @choose.choose_2.callback()
        def OnSelect(btn, choose, trigger_event):
            if choose:
                self._write_setting(global_data.player, uoc.QUALITY_OTHER_MECHA_EFFECT_LEVEL_KEY, uoc.MECHA_EFFECT_LEVEL_MEDIUM, True)
                global_data.emgr.set_mecha_effect_level.emit(uoc.MECHA_EFFECT_LEVEL_MEDIUM, False)

        @choose.choose_3.callback()
        def OnSelect(btn, choose, trigger_event):
            if choose:
                self._write_setting(global_data.player, uoc.QUALITY_OTHER_MECHA_EFFECT_LEVEL_KEY, uoc.MECHA_EFFECT_LEVEL_HIGH, True)
                global_data.emgr.set_mecha_effect_level.emit(uoc.MECHA_EFFECT_LEVEL_HIGH, False)

        @choose.choose_4.callback()
        def OnSelect(btn, choose, trigger_event):
            if choose:
                self._write_setting(global_data.player, uoc.QUALITY_OTHER_MECHA_EFFECT_LEVEL_KEY, uoc.MECHA_EFFECT_LEVEL_ULTRA, True)
                global_data.emgr.set_mecha_effect_level.emit(uoc.MECHA_EFFECT_LEVEL_ULTRA, False)

        nd_dynamic_fuzzy = getattr(page, 'nd_dynamic_fuzzy')
        choose = nd_dynamic_fuzzy.choose
        init_checkbox_group(choose)
        attach_checkbox_group_data(choose, (uoc.QUALITY_RADIAL_BLUR_KEY,))

        @choose.choose_1.callback()
        def OnSelect(btn, choose, trigger_event):
            if trigger_event:
                self._write_setting(global_data.player, uoc.QUALITY_RADIAL_BLUR_KEY, 1 if choose else 0, True)
                global_data.display_agent.set_radial_blur_active(choose)

        self.refresh_all_btn(page)

    def set_redirect_scale_level(self, level, is_refresh_slider=False, is_write=False):
        panel_render = getattr(self.panel, 'nd_render')
        nd_pic = panel_render.choose.nd_pic
        redirect_scale = uoc.PC_REDIRECT_RANGE[level]
        if is_write:
            global_data.player.write_setting(uoc.PC_REDIRECT_SCALE, level, True)
        nd_pic.lab_small.SetString(get_text_by_id(2331).format(str(redirect_scale)))
        if is_refresh_slider:
            percent = level * 100.0 / (len(uoc.PC_REDIRECT_RANGE) - 1)
            nd_pic.slider.setPercent(percent)

    def redirect_scale_reset(self):
        if global_data.is_pc_mode:
            redirect_scale_level = global_data.player.get_default_setting(uoc.PC_REDIRECT_SCALE)
            self.set_redirect_scale_level(redirect_scale_level, False, True)

    def init_redirect_scale(self):
        if global_data.is_pc_mode:
            panel_render = getattr(self.panel, 'nd_render')
            nd_pic = panel_render.choose.nd_pic
            level_count = len(uoc.PC_REDIRECT_RANGE)
            level_step = 100.0 / (level_count - 1)
            if not nd_pic:
                return

            @nd_pic.slider.unique_callback()
            def OnPercentageChanged(ctrl, slider):
                val = slider.getPercent()
                cur_level = int(val / level_step)
                if cur_level >= level_count:
                    cur_level = level_count - 1
                self.set_redirect_scale_level(cur_level, False, True)
                redirect_scale = uoc.PC_REDIRECT_RANGE[cur_level]
                global_data.display_agent.set_redirect_scale(redirect_scale)

            @nd_pic.minute.callback()
            def OnClick(*args):
                level = global_data.player.get_setting(uoc.PC_REDIRECT_SCALE)
                level -= 1
                if level < 0:
                    level = 0
                self.set_redirect_scale_level(level, True, True)
                redirect_scale = uoc.PC_REDIRECT_RANGE[level]
                global_data.display_agent.set_redirect_scale(redirect_scale)

            @nd_pic.plus.callback()
            def OnClick(*args):
                level = global_data.player.get_setting(uoc.PC_REDIRECT_SCALE)
                level += 1
                if level >= level_count:
                    level = level_count - 1
                self.set_redirect_scale_level(level, True, True)
                redirect_scale = uoc.PC_REDIRECT_RANGE[level]
                global_data.display_agent.set_redirect_scale(redirect_scale)

            level = global_data.player.get_setting(uoc.PC_REDIRECT_SCALE)
            self.set_redirect_scale_level(level, True, False)

    def show_setting_widget_frame_rate(self):
        if global_data.achi_mgr.get_cur_user_archive_data('setting_red_point_frame_rate'):
            inner_size = self.panel.getContentSize()
            _, y = self.panel.nd_frame_rate.GetPosition()
            percent = int((inner_size.height - y) / inner_size.height * 100)
            self.parent.panel.content_bar.page.jumpToPercentVertical(percent)
            self.show_guide_setting_frame_rate()
            global_data.achi_mgr.set_cur_user_archive_data('setting_red_point_frame_rate', 0)

    def show_guide_setting_frame_rate(self):
        page = self.panel
        if not page:
            return
        else:
            anchor_node = page.nd_rate_tips
            panel = self.nd_guide_frame_rate
            if panel is None:
                self.nd_guide_frame_rate = global_data.uisystem.load_template_create('guide/i_guide_setting_rate', parent=self.parent.panel)

                @self.nd_guide_frame_rate.unique_callback()
                def OnClick(btn, touch):
                    if time_utils.time() - self.show_frame_rate_limit > 1:
                        self.nd_guide_frame_rate.setVisible(False)

            self.nd_guide_frame_rate.setVisible(True)
            self.nd_guide_frame_rate.temp_tips.lab_tips.SetString(get_text_local_content(81394))
            wpos = anchor_node.getParent().convertToWorldSpace(anchor_node.getPosition())
            lpos = self.nd_guide_frame_rate.nd_content.getParent().convertToNodeSpace(wpos)
            import cc
            lpos.add(cc.Vec2(0.0, 10.0))
            self.nd_guide_frame_rate.nd_content.setPosition(lpos)
            self.show_frame_rate_limit = time_utils.time()
            return

    def check_frame_rate_red_point(self):
        from logic.gutils.activity_utils import check_update_frame_rate_red_point
        check_update_frame_rate_red_point()
        self.show_setting_widget_frame_rate()

    def _write_setting(self, avatar, key, contact, upload):
        if global_data.is_pc_mode:
            upload = False
        ret = avatar.write_setting_2(key, contact, sync_to_server=upload)
        if global_data.is_pc_mode:
            self._refresh_sync_server_btn_enable()
        return ret

    def _get_setting(self, avatar, key):
        return avatar.get_setting_2(key)

    def _get_default_setting(self, avatar, key):
        return avatar.get_default_setting_2(key)

    def add_graph_item(self, item, index):

        @item.btn.callback()
        def OnClick(*args):
            if item == self.last_choose_item or not global_data.player:
                return
            else:
                item.btn.choose.setVisible(True)
                global_data.gsetting.set_graphics_style(index)
                if self.last_choose_item != None:
                    self.last_choose_item.btn.choose.setVisible(False)
                self.last_choose_item = item
                return

        if global_data.player and global_data.gsetting.get_graphics_style() == index:
            OnClick()

    def init_graph_styly(self, panel_graphics_style):
        self.panel_graphics_style = panel_graphics_style
        graphics_style_count = 5
        self.last_choose_item = None
        list_graphics_style = panel_graphics_style.choose.list_graphics_style
        list_graphics_style.SetInitCount(graphics_style_count)
        for index in range(graphics_style_count):
            item = list_graphics_style.GetItem(index)
            self.add_graph_item(item, index)

        return

    def graph_styly_reset(self):
        if not global_data.is_ue_model:
            return
        else:
            if self.last_choose_item != None:
                self.last_choose_item.btn.choose.setVisible(False)
            default_type_index = uoc.SETTING_CONF[uoc.GRAPHICS_STYLE_TYPE]
            global_data.gsetting.set_graphics_style(default_type_index)
            list_graphics_style = self.panel_graphics_style.choose.list_graphics_style
            item = list_graphics_style.GetItem(default_type_index)
            item.btn.choose.setVisible(True)
            self.last_choose_item = item
            return