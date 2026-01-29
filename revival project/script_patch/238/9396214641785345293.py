# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/setting_ui/SettingWidget/SensitivitySettingWidget.py
from __future__ import absolute_import
from logic.gcommon.common_const import ui_operation_const as uoc
from logic.gutils.pc_utils import adjust_setting_panel_pos_and_size
from .SettingWidgetBase import SettingWidgetBase
from logic.gutils import template_utils
from logic.gcommon.common_const.ui_operation_const import OPEN_CONDITION_NONE

class SensitivitySettingWidget(SettingWidgetBase):
    GYRO_SST_KEYS = [
     uoc.SST_GYROSCOPE_SCR_KEY, uoc.SST_GYROSCOPE_RD_KEY, uoc.SST_GYROSCOPE_2M_KEY, uoc.SST_GYROSCOPE_4M_KEY, uoc.SST_GYROSCOPE_6M_KEY]
    FREESIGHT_SST_KEYS = [uoc.SST_FS_ROCKER_KEY]
    THREED_TOUCH_KEYS = [uoc.ThreeD_TOUCH_PERCENT_KEY]

    def __init__(self, panel, parent):
        super(SensitivitySettingWidget, self).__init__(panel, parent)
        self.CAMERA_SST_KEYS_INST = [
         uoc.SST_SCR_KEY, uoc.SST_AIM_RD_KEY,
         uoc.SST_AIM_2M_KEY, uoc.SST_AIM_4M_KEY,
         uoc.SST_AIM_6M_KEY]
        if not global_data.is_pc_mode:
            self.CAMERA_SST_KEYS_INST.append(uoc.SST_FROCKER_KEY)
        self.CAMERA_SST_KEYS_NAME_ID = [2012, 2013,
         2014, 2015,
         2239]
        self.guide_node = None
        if not global_data.is_pc_mode:
            self.CAMERA_SST_KEYS_NAME_ID.append(2016)
        return

    def on_init_panel(self, **kwargs):
        self.init_sensitivity_setting(self.panel)
        adjust_setting_panel_pos_and_size(self.parent.panel.content_bar.page, self.parent, self.panel)

    def on_enter_page(self, **kwargs):
        super(SensitivitySettingWidget, self).on_enter_page()
        self.init_3d_touch_setting(self.panel)
        self.init_gyr_setting(self.panel)
        self._refresh_sync_server_btn_enable()

    def on_exit_page(self, **kwargs):
        super(SensitivitySettingWidget, self).on_exit_page()
        self.sync_sst_gui_data()
        if self.guide_node:
            self.guide_node.Destroy()
            self.guide_node = None
            if self.need_show_guide:
                setting_key, choose_nd, (read_guide_key, guide_text) = self.need_show_guide[0]
                global_data.achi_mgr.set_cur_user_archive_data(read_guide_key, 1)
        return

    def on_recover_default(self, **kwargs):
        self.recover_sensitivity_setting()
        self._refresh_sync_server_btn_enable()

    def _get_settings_available_on_pc(self):
        ret_set = set()
        for key in self.CAMERA_SST_KEYS_INST:
            ret_set.add(key)

        for key in self.FREESIGHT_SST_KEYS:
            ret_set.add(key)

        return ret_set

    def _get_out_of_sync_settings(self):
        ret_set = set()
        pc_settings = self._get_settings_available_on_pc()
        for setting_key in pc_settings:
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

    def _convert_percent_to_sst(self, percent):
        return self._convert_percent_to_value(percent, uoc.SST_RANGE)

    def _convert_sst_to_percent(self, sst):
        return self._convert_value_to_percent(sst, uoc.SST_RANGE)

    def _convert_percent_to_value(self, percent, range):
        from logic.gutils.template_utils import slider_convert_percent_to_value
        return slider_convert_percent_to_value(percent, range)

    def _convert_value_to_percent(self, value, range):
        from logic.gutils.template_utils import slider_convert_value_to_percent
        return slider_convert_value_to_percent(value, range)

    def on_set_slider_property(self, key, val, event_name=None):
        val = self._convert_percent_to_sst(val)
        cur_list = global_data.player.get_setting_2(key)
        cur_list[uoc.SST_IDX_BASE] = val
        self._refresh_sync_server_btn_enable()

    def on_select_nd_mobile_smooth_checkbox(self, node, choose_value, *args, **kwargs):
        setting_key = node._value
        trigger_event = kwargs.get('trigger_event', False)
        if trigger_event:
            global_data.player.write_setting_2(setting_key, str(choose_value), True)
            global_data.emgr.player_user_setting_changed_event.emit(setting_key, choose_value)

    def on_click_btn_detail(self, title, rule):
        from logic.comsys.common_ui.GameRuleDescUI import GameRuleDescUI
        dlg = GameRuleDescUI()
        dlg.set_show_rule(title, rule)

    def init_checkbox(self, page, check_box_group, setting_key, detail_info, guide_info=None):
        template_utils.init_checkbox_group(check_box_group)
        template_utils.attach_checkbox_group_data(check_box_group, [setting_key])
        choose_nd = check_box_group.choose_1
        choose_nd.BindMethod('OnSelect', self.on_select_nd_mobile_smooth_checkbox)
        choose_nd.btn_detail.BindMethod('OnClick', lambda btn, touch, info=detail_info: self.on_click_btn_detail(*info))
        sel = str(global_data.player.get_setting_2(setting_key)) == str(True)
        template_utils.set_check_box_group_item_select(check_box_group, setting_key, sel, trigger_event=False)
        if guide_info:
            read_guide_key, guide_text = guide_info
            if read_guide_key and not global_data.achi_mgr.get_cur_user_archive_data(read_guide_key):
                self.need_show_guide.append((setting_key, choose_nd, guide_info))

    def show_nd_mobile_smooth_guide(self, page):
        if not self.need_show_guide:
            if self.guide_node:
                self.guide_node.setVisible(False)
            return
        else:
            setting_key, choose_nd, (read_guide_key, guide_text) = self.need_show_guide[0]
            guide_anchor = choose_nd.nd_guide
            world_pos = guide_anchor.getParent().convertToWorldSpace(guide_anchor.getPosition())
            if self.guide_node:
                self.guide_node.Destroy()
                self.guide_node = None
            self.guide_node = template_utils.init_guide_temp(page, wpos=world_pos, text_id=guide_text, temp_path='common/i_guide_right_top_setting', adjust_pos_node_name='content', pos_consider_offset=False, delay_show_secs=0.233)

            @self.guide_node.block_click.unique_callback()
            def OnClick(btn, touch, rgk=read_guide_key):
                global_data.achi_mgr.set_cur_user_archive_data(rgk, 1)
                self.need_show_guide and self.need_show_guide.pop(0)
                self.show_nd_mobile_smooth_guide(page)

            return

    def init_sensitivity_setting(self, page):
        import math
        from logic.gutils.template_utils import init_setting_slider1
        lv_camera = page.lv_camera
        lv_rocker = page.lv_rocker
        lv_sight = page.lv_sight
        lv_camera.SetInitCount(len(self.CAMERA_SST_KEYS_NAME_ID))
        all_items = lv_camera.GetAllItem()
        for index, slider_widget in enumerate(all_items):

            def call_back(val, index=index):
                key = self.CAMERA_SST_KEYS_INST[index]
                self.on_set_slider_property(key, val)

            key = self.CAMERA_SST_KEYS_INST[index]
            setting = global_data.player.get_setting_2(key)
            base_value = setting[uoc.SST_IDX_BASE]
            if math.isnan(base_value) or math.isinf(base_value):
                default_value = global_data.player.get_default_setting(key)
                global_data.player.write_setting_2(key, default_value, True)
                base_value = default_value[uoc.SST_IDX_BASE]
            percent = self._convert_sst_to_percent(base_value)
            slider_widget.slider.setPercent(percent)
            init_setting_slider1(slider_widget, get_text_local_content(self.CAMERA_SST_KEYS_NAME_ID[index]), call_back, val_scale=uoc.SST_PERCENT_SCALE)

        self.need_show_guide = []
        self.init_checkbox(page, page.nd_mobile_smooth.choose, uoc.SST_AUTO_HELP_KEY, (2293,
                                                                                       609097), ('read_sst_auto_help_guide_201021',
                                                                                                 609098))
        self.init_checkbox(page, page.nd_adapt_mag.choose, uoc.SST_ADAPT_MAGNIFICATION, (2293,
                                                                                         606331))
        lv = global_data.player.get_lv()
        if self.need_show_guide and not global_data.is_pc_mode and lv >= 5:
            self.show_nd_mobile_smooth_guide(page)
        rocker_name_list = [
         get_text_local_content(2012), get_text_local_content(2013),
         get_text_local_content(2014), get_text_local_content(2015),
         get_text_local_content(2239)]
        lv_rocker.SetInitCount(len(rocker_name_list))
        all_items = lv_rocker.GetAllItem()
        for index, slider_widget in enumerate(all_items):
            key = self.GYRO_SST_KEYS[index]
            setting = global_data.player.get_setting_2(key)
            base_value = setting[uoc.SST_IDX_BASE]
            percent = self._convert_sst_to_percent(base_value)
            slider_widget.slider.setPercent(percent)
            init_setting_slider1(slider_widget, rocker_name_list[index], val_scale=uoc.SST_PERCENT_SCALE)

        sight_name_list = [
         get_text_local_content(2017)]
        lv_sight.SetInitCount(len(sight_name_list))
        all_items = lv_sight.GetAllItem()
        for index, slider_widget in enumerate(all_items):

            def sight_call_back(val, index=index):
                key = self.FREESIGHT_SST_KEYS[index]
                self.on_set_slider_property(key, val)

            key = self.FREESIGHT_SST_KEYS[index]
            setting = global_data.player.get_setting_2(key)
            base_value = setting[uoc.SST_IDX_BASE]
            percent = self._convert_sst_to_percent(base_value)
            slider_widget.slider.setPercent(percent)
            init_setting_slider1(slider_widget, sight_name_list[index], sight_call_back, val_scale=uoc.SST_PERCENT_SCALE)

        self.init_3d_touch_setting(page)
        self.init_gyr_setting(page)

    def init_3d_touch_setting(self, page):
        from logic.gutils.template_utils import init_setting_slider1
        lv_3dtouch = page.lv_3dtouch
        touch_name_list = [get_text_local_content(2018)]
        lv_3dtouch.SetInitCount(len(touch_name_list))
        all_items = lv_3dtouch.GetAllItem()
        for index, slider_widget in enumerate(all_items):

            def sight_call_back(val, index=index):
                pass

            key = self.THREED_TOUCH_KEYS[index]
            val = global_data.player.get_setting_2(key)
            percent = self._convert_value_to_percent(val, uoc.ThreeD_TOUCH_RANGE)
            slider_widget.slider.setPercent(percent)
            init_setting_slider1(slider_widget, touch_name_list[index], sight_call_back)

    def init_gyr_setting(self, page):
        from logic.gutils.template_utils import set_slider_enable
        rocker_name_list = [
         get_text_local_content(2012), get_text_local_content(2013),
         get_text_local_content(2014), get_text_local_content(2015),
         get_text_local_content(2239)]
        gyr_open_state, _, _ = global_data.player.get_setting(uoc.GYROSCOPE_STATE_KEY)
        gyr_state = gyr_open_state != OPEN_CONDITION_NONE
        lv_rocker = page.lv_rocker
        lv_rocker.SetInitCount(len(rocker_name_list))
        all_items = lv_rocker.GetAllItem()
        for index, slider_widget in enumerate(all_items):
            set_slider_enable(slider_widget, rocker_name_list[index], gyr_state, val_scale=uoc.SST_PERCENT_SCALE)

    def recover_3d_touch_setting(self):
        page = self.panel
        lv_3dtouch = page.lv_3dtouch

        def _reverse_helper(container, store_keys):
            all_items = container.GetAllItem()
            for index, slider_widget in enumerate(all_items):
                val = global_data.player.get_default_setting_2(store_keys[index])
                perc = self._convert_value_to_percent(val, uoc.ThreeD_TOUCH_RANGE)
                slider_widget.slider.setPercent(perc)
                slider_widget.slider.OnPercentageChanged(slider_widget.slider)

        _reverse_helper(lv_3dtouch, self.THREED_TOUCH_KEYS)

    def sync_3d_touch_setting(self):
        lv_3dtouch = self.panel.lv_3dtouch
        slider_widget = lv_3dtouch.GetItem(0)
        percent = slider_widget.slider.getPercent()
        val = self._convert_percent_to_value(percent, uoc.ThreeD_TOUCH_RANGE)
        global_data.emgr.threed_touch_pressure_change_event.emit(val)

    def recover_sensitivity_setting(self):
        page = self.panel
        lv_camera = page.lv_camera
        lv_rocker = page.lv_rocker
        lv_sight = page.lv_sight
        is_enable = global_data.player.get_default_setting_2(uoc.SST_AUTO_HELP_KEY)
        global_data.player.write_setting_2(uoc.SST_AUTO_HELP_KEY, is_enable, True)
        is_enable = str(is_enable) == 'True'
        global_data.emgr.player_user_setting_changed_event.emit(uoc.SST_AUTO_HELP_KEY, is_enable)
        template_utils.set_check_box_group_item_select(page.nd_mobile_smooth.choose, uoc.SST_AUTO_HELP_KEY, is_enable, trigger_event=False)
        is_enable = global_data.player.get_default_setting_2(uoc.SST_ADAPT_MAGNIFICATION)
        global_data.player.write_setting_2(uoc.SST_ADAPT_MAGNIFICATION, is_enable, True)
        is_enable = str(is_enable) == 'True'
        global_data.emgr.player_user_setting_changed_event.emit(uoc.SST_ADAPT_MAGNIFICATION, is_enable)
        template_utils.set_check_box_group_item_select(page.nd_adapt_mag.choose, uoc.SST_ADAPT_MAGNIFICATION, is_enable, trigger_event=False)

        def _reverse_helper(container, store_keys):
            all_items = container.GetAllItem()
            for index, slider_widget in enumerate(all_items):
                setting = global_data.player.get_default_setting_2(store_keys[index])
                base_mul = setting[uoc.SST_IDX_BASE]
                perc = self._convert_sst_to_percent(base_mul)
                slider_widget.slider.setPercent(perc)
                slider_widget.slider.OnPercentageChanged(slider_widget.slider)

        def _reverse_data_helper(store_keys):
            import copy
            for index, key in enumerate(store_keys):
                setting = global_data.player.get_default_setting_2(key)
                global_data.player.write_setting_2(key, copy.deepcopy(setting), sync_to_server=False if global_data.is_pc_mode else True)

        _reverse_helper(lv_camera, self.CAMERA_SST_KEYS_INST)
        _reverse_helper(lv_rocker, self.GYRO_SST_KEYS)
        _reverse_helper(lv_sight, self.FREESIGHT_SST_KEYS)
        self.recover_3d_touch_setting()
        _reverse_data_helper(self.CAMERA_SST_KEYS_INST)
        _reverse_data_helper(self.GYRO_SST_KEYS)
        _reverse_data_helper(self.FREESIGHT_SST_KEYS)
        self._refresh_sync_server_btn_enable()

    def sync_sst_gui_data(self):
        lv_rocker = self.panel.lv_rocker
        self.sync_slider_data_to_mem_helper(lv_rocker, self.GYRO_SST_KEYS)
        global_data.emgr.player_update_acc_sensitivity_event.emit()
        camera_sst_event_list = []
        lv_camera = self.panel.lv_camera
        self.sync_slider_data_to_mem_helper(lv_camera, self.CAMERA_SST_KEYS_INST, camera_sst_event_list)
        sight_camera_sst_event_list = ['sst_free_sight_changed_event']
        lv_sight = self.panel.lv_sight
        self.sync_slider_data_to_mem_helper(lv_sight, self.FREESIGHT_SST_KEYS, sight_camera_sst_event_list)
        self.sync_3d_touch_setting()

    def sync_slider_data_to_mem_helper(self, slider_container, keys, events=[]):
        if not global_data.player:
            return
        for idx, slider_widget in enumerate(slider_container.GetAllItem()):
            percent = slider_widget.slider.getPercent()
            sst = self._convert_percent_to_sst(percent)
            if idx < len(keys):
                cur_list = global_data.player.get_setting_2(keys[idx])
                cur_list[uoc.SST_IDX_BASE] = sst
                global_data.player.write_setting_2(keys[idx], cur_list, sync_to_server=False if global_data.is_pc_mode else True)
                if not events:
                    ev = 'sst_common_changed_event'
                    global_data.emgr.fireEvent(ev, keys[idx], cur_list)
                if idx < len(events):
                    ev = events[idx]
                    global_data.emgr.fireEvent(ev, cur_list)

        self._refresh_sync_server_btn_enable()