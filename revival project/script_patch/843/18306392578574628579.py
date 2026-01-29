# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/setting_ui/SettingWidget/OperationSettingWidget.py
from __future__ import absolute_import
from six.moves import zip
from logic.gcommon.common_const import ui_operation_const as uoc
from .SettingWidgetBase import SettingWidgetBase
from logic.gutils.template_utils import init_setting_slider1, slider_convert_percent_to_value, slider_convert_value_to_percent

class OperationSettingWidget(SettingWidgetBase):
    THREED_TOUCH_KEYS = [
     uoc.ThreeD_TOUCH_PERCENT_KEY]

    def __init__(self, panel, parent):
        super(OperationSettingWidget, self).__init__(panel, parent)

    def on_init_panel(self, **kwargs):
        self.init_operation_setting(self.panel)

    def on_exit_page(self, **kwargs):
        super(OperationSettingWidget, self).on_exit_page()
        self.parent.panel.nd_layout_custom.setVisible(False)
        self.sync_3d_touch_setting()
        self.sync_setting_data()

    def on_enter_page(self, **kwargs):
        super(OperationSettingWidget, self).on_enter_page()
        self.parent.panel.nd_layout_custom.setVisible(True)
        self.init_3d_touch_setting(self.panel)

    def on_recover_default(self, **kwargs):
        self.recover_ope_setting()
        self.recover_3d_touch_setting()

    def sync_setting_data(self):
        if global_data.player:
            global_data.player.save_settings_to_file()

    def init_operation_setting(self, page):
        from logic.gutils.template_utils import init_radio_group, attach_radio_group_data, set_radio_group_item_select
        init_radio_group(page)
        opt_list = [uoc.FIXED_FIREROCKER, uoc.MOVABLE_FIREROCKER, uoc.ALL_FIX_ROCKER]
        attach_radio_group_data([page.pnl_1, page.pnl_2, page.pnl_3], opt_list)
        check_box_keys = [uoc.WEAPON_ROCKER_DISABLE_DRAG_KEY, uoc.ThreeD_TOUCH_TOGGLE_KEY, uoc.WEAPON_ROCKER_DISABLE_DRAG_KEY]
        associated_check_box_dict = {1: page.pnl_3.check_box,3: page.pnl_1.check_box}
        check_box_events = ['weapon_rocker_draggable_change_event', 'threed_touch_change_event', 'weapon_rocker_draggable_change_event']
        operation_list = [1, 2, 3]
        page.pnl_1.RecordAnimationNodeState('show_1_1')
        page.pnl_1.RecordAnimationNodeState('show_1')
        page.pnl_2.RecordAnimationNodeState('show_2_1')
        page.pnl_2.RecordAnimationNodeState('show_2')
        page.pnl_3.RecordAnimationNodeState('show_3_1')
        page.pnl_3.RecordAnimationNodeState('show_3')
        page.pnl_1.check_box.setVisible(False)
        page.pnl_3.check_box.setVisible(False)
        cur_pnl = [None]
        for operation_index in operation_list:
            pnl = getattr(page, 'pnl_{0}'.format(operation_index))
            if not pnl:
                continue
            check_box = pnl.check_box
            if check_box:

                @check_box.btn.unique_callback()
                def OnClick(btn, touch, trigger_event=True, index=operation_index, check_box=check_box, pnl=pnl):
                    if not global_data.player:
                        return
                    store_key = check_box_keys[index - 1]
                    if store_key == uoc.ThreeD_TOUCH_TOGGLE_KEY:
                        is_can_open = self.check_can_open_3d_touch()
                    else:
                        is_can_open = True
                    if not is_can_open:
                        global_data.game_mgr.show_tip(get_text_local_content(2019))
                        return
                    choose = not check_box.choose.isVisible()
                    check_box.choose.setVisible(choose)
                    if index in associated_check_box_dict:
                        ass_check_box = associated_check_box_dict[index]
                        ass_check_box.choose.setVisible(choose)
                    check_box_ani = 'show_{}_1'.format(index)
                    pnl_ani = 'show_{}'.format(index)
                    if pnl.choose.isVisible():
                        if choose:
                            pnl.StopAnimation(pnl_ani)
                            pnl.RecoverAnimationNodeState(pnl_ani)
                            pnl.PlayAnimation(check_box_ani)
                        else:
                            pnl.StopAnimation(check_box_ani)
                            pnl.RecoverAnimationNodeState(check_box_ani)
                            pnl.PlayAnimation(pnl_ani)
                    event = check_box_events[index - 1]
                    if global_data.player:
                        global_data.player.write_setting(store_key, choose)
                    global_data.emgr.fireEvent(event, choose)

                store_key = check_box_keys[operation_index - 1]
                is_open = bool(global_data.player and global_data.player.get_setting(store_key))
                if store_key == uoc.ThreeD_TOUCH_TOGGLE_KEY:
                    is_can_open = self.check_can_open_3d_touch()
                    check_box.choose.setVisible(is_open and is_can_open)
                else:
                    check_box.choose.setVisible(is_open)
                self.update_3d_touch_show()

            @pnl.unique_callback()
            def OnSelect(btn, choose, trigger_event, check_box=check_box, index=operation_index, pnl=pnl, cur_pnl=cur_pnl):
                btn.bg.SetSelect(choose)
                cur_pnl[0] = pnl
                check_box_ani = 'show_{}_1'.format(index)
                pnl_ani = 'show_{}'.format(index)
                if choose:
                    pnl.PlayAnimation(pnl_ani)
                else:
                    pnl.StopAnimation(pnl_ani)
                    pnl.StopAnimation(check_box_ani)
                    pnl.RecoverAnimationNodeState(pnl_ani)
                    pnl.RecoverAnimationNodeState(check_box_ani)
                if trigger_event:
                    global_data.emgr.firerocker_ope_change_event.emit(opt_list[index - 1])
                self.update_3d_touch_show()

        set_radio_group_item_select(page, global_data.player.get_setting(uoc.FIREROCKER_OPE_KEY), False)
        return

    def check_can_open_3d_touch(self):
        from common.platform.device_info import DeviceInfo
        device_info = DeviceInfo.get_instance()
        return device_info.is_open_3d_touch()

    def recover_ope_setting(self):
        page = self.panel
        from logic.gutils.template_utils import set_radio_group_item_select
        set_radio_group_item_select(page, global_data.player.get_default_setting(uoc.FIREROCKER_OPE_KEY), True)
        check_box_keys = [uoc.ONE_SHOT_SETTING_KEY, uoc.ThreeD_TOUCH_TOGGLE_KEY, uoc.ONE_SHOT_SETTING_KEY]
        check_boxs = [page.pnl_1.check_box, page.pnl_2.check_box, page.pnl_3.check_box]
        for check_box, key in zip(check_boxs, check_box_keys):
            is_open = global_data.player.get_default_setting(key)
            if check_box:
                if is_open != check_box.choose.isVisible():
                    check_box.btn.OnClick(None, True)

        return

    def init_3d_touch_setting(self, page):
        from logic.gutils.template_utils import init_setting_slider1, slider_convert_value_to_percent
        touch_name_list = [
         get_text_local_content(2018)]
        all_items = [self.panel.pnl_2.btn.temp_3dtouch]
        for index, slider_widget in enumerate(all_items):

            def sight_call_back(val, index=index):
                pass

            key = self.THREED_TOUCH_KEYS[index]
            val = global_data.player.get_setting(key)
            percent = slider_convert_value_to_percent(val, uoc.ThreeD_TOUCH_RANGE)
            slider_widget.slider.setPercent(percent)
            init_setting_slider1(slider_widget, touch_name_list[index], sight_call_back)

    def recover_3d_touch_setting(self):
        from logic.gutils.template_utils import slider_convert_value_to_percent
        page = self.panel
        all_items = [self.panel.pnl_2.btn.temp_3dtouch]
        for index, slider_widget in enumerate(all_items):
            val = global_data.player.get_default_setting(self.THREED_TOUCH_KEYS[index])
            perc = slider_convert_value_to_percent(val, uoc.ThreeD_TOUCH_RANGE)
            slider_widget.slider.setPercent(perc)
            slider_widget.slider.OnPercentageChanged(slider_widget.slider)

    def sync_3d_touch_setting(self):
        from logic.gutils.template_utils import slider_convert_percent_to_value
        slider_widget = self.panel.pnl_2.btn.temp_3dtouch
        percent = slider_widget.slider.getPercent()
        val = slider_convert_percent_to_value(percent, uoc.ThreeD_TOUCH_RANGE)
        global_data.emgr.threed_touch_pressure_change_event.emit(val)

    def update_3d_touch_show(self):
        is_open = global_data.player.get_setting(uoc.ThreeD_TOUCH_TOGGLE_KEY)
        self.panel.pnl_2.btn.temp_3dtouch.setVisible(is_open)