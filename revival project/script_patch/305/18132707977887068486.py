# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/setting_ui/SettingWidget/AdvancedSettingWidget.py
from __future__ import absolute_import
import six
import cc
from logic.comsys.accelerometer.AccInput import AccInput
from logic.gcommon.common_const.ui_operation_const import OPEN_CONDITION_NONE, OPEN_CONDITION_OPEN, OPEN_CONDITION_AIM_OPEN
from logic.gcommon.common_const import ui_operation_const as uoc
from .SettingWidgetBase import SettingWidgetBase
from logic.gutils.template_utils import init_radio_group, init_radio_group_new, attach_radio_group_data, set_radio_group_item_select, set_radio_group_item_select_new, set_radio_group_enable_state, init_checkbox_group, attach_checkbox_group_data, set_check_box_group_item_select, set_radio_group_enable_state_new
import game3d
from logic.gcommon.const import GEV_ONLY_FRIEND, GEV_ALL
from logic.gutils.setting_utils import SettingTips
FAQ_TITLE_ID = 2293

class AdvancedSettingWidget(SettingWidgetBase):

    def __init__(self, panel, parent):
        super(AdvancedSettingWidget, self).__init__(panel, parent)
        global_data.asw = panel
        self.mecha_expand_tip = None
        self.key_2_btn = {}
        self._has_changed_aim_color = False
        self._has_changed_down_color = False
        self._need_show_mecha_setting = False
        return

    def on_init_panel(self, **kwargs):
        self._init_members()
        self.init_panel(self.panel)

    def destroy(self):
        if self.mecha_expand_tip:
            self.mecha_expand_tip.destroy()
            self.mecha_expand_tip = None
        super(AdvancedSettingWidget, self).destroy()
        return

    def on_enter_page(self, **kwargs):
        super(AdvancedSettingWidget, self).on_enter_page()
        if self.mecha_expand_tip:
            self.mecha_expand_tip.check_show_tips()

    def on_exit_page(self, **kwargs):
        super(AdvancedSettingWidget, self).on_exit_page()
        if self._has_changed_aim_color:
            if global_data.player:
                global_data.player.save_settings_to_file()
            global_data.emgr.change_aim_color_event.emit()
        if self._has_changed_down_color:
            if global_data.player:
                global_data.player.save_settings_to_file()
            global_data.emgr.change_down_color_event.emit()

    def on_recover_default(self, **kwargs):
        if not global_data.player:
            return
        for key in uoc.ADVANCED_WEAPON_SETTINGS:
            global_data.player.write_setting_2(key, global_data.player.get_default_setting_2(key), True)

        page_keys = {uoc.LF_OPE_KEY: {'event': 'left_fire_ope_change_event'},uoc.GYROSCOPE_STATE_KEY: {'need_write': True,'need_upload': True},uoc.AIM_COLOR_VAL: {'need_write': True,'need_upload': True},uoc.DOWN_COLOR_VAL: {'need_write': True,'need_upload': True}}
        for set_key, set_conf in six.iteritems(page_keys):
            default_setting = global_data.player.get_default_setting(set_key)
            need_write = set_conf.get('need_write', False)
            need_upload = set_conf.get('need_upload', False)
            event = set_conf.get('event')
            if need_write:
                global_data.player.write_setting(set_key, default_setting, need_upload)
            if event:
                global_data.emgr.fireEvent(event, default_setting)

        if global_data.player:
            global_data.player.change_glide_effect_visibility(GEV_ALL, True)
        self._has_changed_aim_color = True
        self._has_changed_down_color = True
        self._refresh_panel(self.panel)

    def _init_members(self):
        self._sw_h_maps = {}

    def init_panel(self, page):
        self.key_2_btn = {uoc.AIM_HELPER_KEY_1: page.list_tab_weapon1.GetItem(0),
           uoc.ANTI_MECHA_WEAPON_FIRE_RELEASE_KEY: page.list_tab_weapon1.GetItem(1),
           uoc.SHOTGUN_WEAPON_FIRE_RELEASE_KEY: page.list_tab_weapon1.GetItem(2),
           uoc.SNIPER_RIFLE_FAST_AIM_AND_RELEASE_FIRE_KEY: page.list_tab_weapon1.GetItem(3),
           uoc.WEAPON_AIM_PRESS_TRIGGER_KEY: page.list_tab_weapon2.GetItem(0),
           uoc.MANUAL_WEAPON_RE_AUTO_AIM: page.list_tab_weapon2.GetItem(1),
           uoc.WEAPON_AIM_ROCKER_DRAG_ENABLE_KEY: page.list_tab_weapon2.GetItem(2),
           uoc.MANUAL_SNIPER_RIFLE_FAST_AIM_AND_FIRE_KEY: page.list_tab_weapon2.GetItem(3),
           uoc.AUTO_FAST_AIM_AND_FIRE_KEY: page.list_tab_weapon2.GetItem(4),
           uoc.ION_GUN_ACCUMULATE_AIM_CANCEL: page.list_tab_weapon2.GetItem(5)
           }
        nd_weapon_h_change = 0
        if global_data.is_pc_mode or global_data.deviceinfo.is_emulator():
            page.list_tab_weapon1.DeleteItem(self.key_2_btn[uoc.AIM_HELPER_KEY_1])
        if global_data.is_pc_mode:
            page.list_tab_weapon2.DeleteItem(self.key_2_btn[uoc.WEAPON_AIM_ROCKER_DRAG_ENABLE_KEY])
        _, ori_h = page.nd_weapon2.GetContentSize()
        _, h = page.list_tab_weapon2.GetContentSize()
        page.nd_weapon2.SetContentSize('100%', h)
        page.nd_weapon2.img_bg.SetContentSize('100%', '100%')
        nd_weapon_h_change += ori_h - h
        if global_data.is_pc_mode:
            page.nd_mecha_translucence.SetPosition(*page.nd_weapon3.GetPosition())
            page.nd_weapon3.setVisible(False)
            page.nd_weapon4.setVisible(False)
            nd_weapon_h_change += page.nd_weapon3.GetContentSize()[1]
            nd_weapon_h_change += page.nd_weapon4.GetContentSize()[1]
        w, h = page.GetContentSize()
        page.SetContentSize(w, h - nd_weapon_h_change)
        _, y = page.nd_weapon.GetPosition()
        page.nd_weapon.SetPosition('50%', y - nd_weapon_h_change)
        self._refresh_panel(page)

    def _refresh_panel(self, page):
        if not global_data.player:
            return
        if not (global_data.is_pc_mode or global_data.deviceinfo.is_emulator()):
            key = uoc.AIM_HELPER_KEY_1
            choose = self.key_2_btn[key]
            choose.setVisible(True)
            choose_1, choose_2 = init_radio_group_new(choose)
            attach_radio_group_data([choose_1, choose_2], [True, False])

            @choose_1.unique_callback()
            def OnSelect(btn, choose, trigger_event, key=key):
                if choose and trigger_event:
                    global_data.player.write_setting(key, True, True)
                    global_data.emgr.player_enable_aim_helper.emit(True)

            @choose_2.unique_callback()
            def OnSelect(btn, choose, trigger_event, key=key):
                if choose and trigger_event:
                    global_data.player.write_setting(key, False, True)
                    global_data.emgr.player_enable_aim_helper.emit(False)

            set_radio_group_item_select_new(choose.list_setting_item, global_data.player.get_setting(key), False)

            @choose.btn_ask.callback()
            def OnClick(btn, touch):
                self._on_question_click(FAQ_TITLE_ID, 609341, btn)

        key = uoc.ANTI_MECHA_WEAPON_FIRE_RELEASE_KEY
        choose = self.key_2_btn[key]
        choose_1, choose_2 = init_radio_group_new(choose)
        attach_radio_group_data([choose_1, choose_2], [False, True])

        @choose_1.unique_callback()
        def OnSelect(btn, choose, trigger_event, key=key):
            val = False
            if choose and trigger_event:
                global_data.player.write_setting_2(key, val, True)

        @choose_2.unique_callback()
        def OnSelect(btn, choose, trigger_event, key=key):
            val = True
            if choose and trigger_event:
                global_data.player.write_setting_2(key, val, True)

        set_radio_group_item_select_new(choose.list_setting_item, global_data.player.get_setting_2(key), False)

        @choose.btn_ask.callback()
        def OnClick(btn, touch):
            self._on_question_click(FAQ_TITLE_ID, 2288, btn)

        key = uoc.SHOTGUN_WEAPON_FIRE_RELEASE_KEY
        choose = self.key_2_btn[key]
        choose_1, choose_2 = init_radio_group_new(choose)
        attach_radio_group_data([choose_1, choose_2], [False, True])

        @choose_1.unique_callback()
        def OnSelect(btn, choose, trigger_event, key=key):
            if choose and trigger_event:
                global_data.player.write_setting_2(key, False, True)

        @choose_2.unique_callback()
        def OnSelect(btn, choose, trigger_event, key=key):
            if choose and trigger_event:
                global_data.player.write_setting_2(key, True, True)

        set_radio_group_item_select_new(choose.list_setting_item, global_data.player.get_setting_2(key), False)

        @choose.btn_ask.callback()
        def OnClick(btn, touch):
            self._on_question_click(FAQ_TITLE_ID, 2287, btn)

        key = uoc.SNIPER_RIFLE_FAST_AIM_AND_RELEASE_FIRE_KEY
        choose = self.key_2_btn[key]
        choose_1, choose_2 = init_radio_group_new(choose)
        attach_radio_group_data([choose_1, choose_2], [False, True])

        @choose_1.unique_callback()
        def OnSelect(btn, choose, trigger_event, key=key):
            val = False
            if choose and trigger_event:
                global_data.player.write_setting_2(key, val, True)

        @choose_2.unique_callback()
        def OnSelect(btn, choose, trigger_event, key=key):
            val = True
            if choose and trigger_event:
                global_data.player.write_setting_2(key, val, True)

        set_radio_group_item_select_new(choose.list_setting_item, global_data.player.get_setting_2(key), False)

        @choose.btn_ask.callback()
        def OnClick(btn, touch):
            self._on_question_click(FAQ_TITLE_ID, 906540, btn)

        key = uoc.WEAPON_AIM_PRESS_TRIGGER_KEY
        choose = self.key_2_btn[key]
        choose_1, choose_2 = init_radio_group_new(choose)
        attach_radio_group_data([choose_1, choose_2], [False, True])

        @choose_1.unique_callback()
        def OnSelect(btn, choose, trigger_event, key=key):
            val = False
            if choose and trigger_event:
                global_data.player.write_setting_2(key, val, True)
                global_data.emgr.weapon_aim_btn_trigger_changed.emit(val)

        @choose_2.unique_callback()
        def OnSelect(btn, choose, trigger_event, key=key):
            val = True
            if choose and trigger_event:
                global_data.player.write_setting_2(key, val, True)
                global_data.emgr.weapon_aim_btn_trigger_changed.emit(val)

        set_radio_group_item_select_new(choose.list_setting_item, global_data.player.get_setting_2(key), False)

        @choose.btn_ask.callback()
        def OnClick(btn, touch):
            self._on_question_click(FAQ_TITLE_ID, 2285, btn)

        key = uoc.MANUAL_WEAPON_RE_AUTO_AIM
        choose = self.key_2_btn[key]
        org_title_color = choose.lab_title.getColor()
        choose_1, choose_2 = init_radio_group_new(choose)
        attach_radio_group_data([choose_1, choose_2], [True, False])

        @choose_1.unique_callback()
        def OnSelect(btn, choose, trigger_event, key=key):
            val = True
            set_radio_group_enable_state(False, False, self.key_2_btn[uoc.MANUAL_SNIPER_RIFLE_FAST_AIM_AND_FIRE_KEY])
            if choose and trigger_event:
                global_data.player.write_setting_2(key, val, True)

        @choose_2.unique_callback()
        def OnSelect(btn, choose, trigger_event, key=key):
            val = False
            set_radio_group_enable_state(True, False, self.key_2_btn[uoc.MANUAL_SNIPER_RIFLE_FAST_AIM_AND_FIRE_KEY], org_title_color)
            if choose and trigger_event:
                global_data.player.write_setting_2(key, val, True)

        set_radio_group_item_select_new(choose.list_setting_item, global_data.player.get_setting_2(key), False)

        @choose.btn_ask.callback()
        def OnClick(btn, touch):
            self._on_question_click(FAQ_TITLE_ID, 2286, btn)

        if not global_data.is_pc_mode:
            key = uoc.WEAPON_AIM_ROCKER_DRAG_ENABLE_KEY
            choose = self.key_2_btn[key]
            choose.setVisible(True)
            choose_1, choose_2 = init_radio_group_new(choose)
            attach_radio_group_data([choose_1, choose_2], [True, False])

            @choose_1.unique_callback()
            def OnSelect(btn, choose, trigger_event, key=key):
                val = True
                if choose and trigger_event:
                    global_data.player.write_setting_2(key, val, True)
                    global_data.emgr.weapon_aim_rocker_draggable_changed.emit(val)

            @choose_2.unique_callback()
            def OnSelect(btn, choose, trigger_event, key=key):
                val = False
                if choose and trigger_event:
                    global_data.player.write_setting_2(key, val, True)
                    global_data.emgr.weapon_aim_rocker_draggable_changed.emit(val)

            set_radio_group_item_select_new(choose.list_setting_item, global_data.player.get_setting_2(key), False)

            @choose.btn_ask.callback()
            def OnClick(btn, touch):
                self._on_question_click(FAQ_TITLE_ID, 2284, btn)

        key = uoc.MANUAL_SNIPER_RIFLE_FAST_AIM_AND_FIRE_KEY
        choose = self.key_2_btn[key]
        choose_1, choose_2 = init_radio_group_new(choose)
        attach_radio_group_data([choose_1, choose_2], [True, False])

        @choose_1.unique_callback()
        def OnSelect(btn, choose, trigger_event, setting_key=key):
            val = True
            if choose and trigger_event:
                global_data.player.write_setting_2(setting_key, val, True)

        @choose_2.unique_callback()
        def OnSelect(btn, choose, trigger_event, setting_key=key):
            val = False
            if choose and trigger_event:
                global_data.player.write_setting_2(setting_key, val, True)

        re_auto_aim = global_data.player.get_setting_2(uoc.MANUAL_WEAPON_RE_AUTO_AIM)
        now_setting_val = False if re_auto_aim else global_data.player.get_setting_2(key)
        set_radio_group_enable_state(not re_auto_aim, now_setting_val, choose, org_title_color)
        if re_auto_aim:
            global_data.player.write_setting_2(key, False, True)

        @choose.btn_ask.callback()
        def OnClick(btn, touch):
            self._on_question_click(FAQ_TITLE_ID, 609343, btn)

        key = uoc.AUTO_FAST_AIM_AND_FIRE_KEY
        choose = self.key_2_btn[key]
        choose_1, choose_2 = init_radio_group_new(choose)
        attach_radio_group_data([choose_1, choose_2], [True, False])

        @choose_1.unique_callback()
        def OnSelect(btn, choose, trigger_event, key=key):
            val = True
            if choose and trigger_event:
                global_data.player.write_setting_2(key, val, True)

        @choose_2.unique_callback()
        def OnSelect(btn, choose, trigger_event, key=key):
            val = False
            if choose and trigger_event:
                global_data.player.write_setting_2(key, val, True)

        set_radio_group_item_select_new(choose.list_setting_item, global_data.player.get_setting_2(key), False)
        choose.btn_ask.setVisible(True)

        @choose.btn_ask.callback()
        def OnClick(btn, touch):
            self._on_question_click(FAQ_TITLE_ID, 609539, btn)

        key = uoc.ION_GUN_ACCUMULATE_AIM_CANCEL
        choose = self.key_2_btn[key]
        choose_1, choose_2 = init_radio_group_new(choose)
        attach_radio_group_data([choose_1, choose_2], [True, False])

        @choose_1.unique_callback()
        def OnSelect(btn, choose, trigger_event, key=key):
            val = True
            if choose and trigger_event:
                global_data.player.write_setting_2(key, val, True)
                global_data.emgr.ion_gun_accumulate_aim_cancel_event.emit()

        @choose_2.unique_callback()
        def OnSelect(btn, choose, trigger_event, key=key):
            val = False
            if choose and trigger_event:
                global_data.player.write_setting_2(key, val, True)
                global_data.emgr.ion_gun_accumulate_aim_cancel_event.emit()

        set_radio_group_item_select_new(choose.list_setting_item, global_data.player.get_setting_2(key), False)
        choose.btn_ask.setVisible(True)

        @choose.btn_ask.callback()
        def OnClick(btn, touch):
            self._on_question_click(2293, 2368, btn)

        if not global_data.is_pc_mode:
            choose = page.list_tab_weapon3.GetItem(0)
            choose_1, choose_2, choose_3 = init_radio_group_new(choose)
            second_choose = page.list_tab_weapon3.GetItem(1)
            sec_choose_1, sec_choose_2 = init_radio_group_new(second_choose)

            @choose_1.unique_callback()
            def OnSelect(btn, choose, trigger_event, second_choose=second_choose, sec_choose_1=sec_choose_1, sec_choose_2=sec_choose_2):
                second_choose.setVisible(True)
                if choose and trigger_event:
                    _, sub_sel = global_data.player.get_setting(uoc.LF_OPE_KEY)
                    global_data.emgr.left_fire_ope_change_event.emit([uoc.LEFT_FIRE_ALWAYS_OPEN, sub_sel])
                    sec_btn = sec_choose_1 if sub_sel == uoc.LF_ONLY_SHOT else sec_choose_2
                    sec_btn.btn_choose.OnClick(True, trigger_event=False)

            @choose_2.unique_callback()
            def OnSelect(btn, choose, trigger_event, second_choose=second_choose, sec_choose_1=sec_choose_1, sec_choose_2=sec_choose_2):
                second_choose.setVisible(True)
                if choose and trigger_event:
                    _, sub_sel = global_data.player.get_setting(uoc.LF_OPE_KEY)
                    global_data.emgr.left_fire_ope_change_event.emit([uoc.LEFT_FIRE_SHOW_WHEN_AIM, sub_sel])
                    sec_btn = sec_choose_1 if sub_sel == uoc.LF_ONLY_SHOT else sec_choose_2
                    sec_btn.btn_choose.OnClick(True, trigger_event=False)

            @choose_3.unique_callback()
            def OnSelect(btn, choose, trigger_event, second_choose=second_choose):
                second_choose.setVisible(False)
                if choose and trigger_event:
                    _, sub_sel = global_data.player.get_setting(uoc.LF_OPE_KEY)
                    global_data.emgr.left_fire_ope_change_event.emit([uoc.LEFT_FIRE_ALWAYS_CLOSE, sub_sel])

            @sec_choose_1.unique_callback()
            def OnSelect(btn, choose, trigger_event):
                if choose and trigger_event:
                    main_sel, _ = global_data.player.get_setting(uoc.LF_OPE_KEY)
                    global_data.emgr.left_fire_ope_change_event.emit([main_sel, uoc.LF_ONLY_SHOT])

            @sec_choose_2.unique_callback()
            def OnSelect(btn, choose, trigger_event):
                if choose and trigger_event:
                    main_sel, _ = global_data.player.get_setting(uoc.LF_OPE_KEY)
                    global_data.emgr.left_fire_ope_change_event.emit([main_sel, uoc.LF_SHOT_AND_MOVE])

            @second_choose.btn_ask.callback()
            def OnClick(btn, touch):
                self._on_question_click(FAQ_TITLE_ID, 82285, btn)

            if global_data.player:
                lf_setting = global_data.player.get_setting(uoc.LF_OPE_KEY)
                main_sel, sub_sel = lf_setting
                if main_sel == uoc.LEFT_FIRE_ALWAYS_OPEN:
                    choose_1.btn_choose.OnClick(True, trigger_event=False)
                elif main_sel == uoc.LEFT_FIRE_SHOW_WHEN_AIM:
                    choose_2.btn_choose.OnClick(True, trigger_event=False)
                else:
                    choose_3.btn_choose.OnClick(True, trigger_event=False)
                if sub_sel == uoc.LF_ONLY_SHOT:
                    sec_choose = sec_choose_1 if 1 else sec_choose_2
                    sec_choose.btn_choose.OnClick(True, trigger_event=False)
            choose = global_data.is_pc_mode or page.list_tab_weapon4.GetItem(0)
            choose_1, choose_2, choose_3 = init_radio_group_new(choose)
            sec_choose_1 = page.nd_weapon4.choose_1
            sec_choose_2 = page.nd_weapon4.choose_2
            init_checkbox_group((sec_choose_1, sec_choose_2))
            attach_radio_group_data([
             choose_1, choose_2, choose_3], [
             OPEN_CONDITION_OPEN, OPEN_CONDITION_AIM_OPEN, OPEN_CONDITION_NONE])
            attach_radio_group_data((sec_choose_1, sec_choose_2), ('xi', 'yi'))

            def check_gyro(choose=choose, sec_choose_1=sec_choose_1, sec_choose_2=sec_choose_2):
                gyr_open_state, x_reverse, y_reverse = global_data.player.get_setting(uoc.GYROSCOPE_STATE_KEY)
                set_radio_group_item_select_new(choose.list_setting_item, gyr_open_state, trigger_event=False)
                sec_choose_1.btn.OnClick(None, trigger_event=False, choose=bool(x_reverse))
                sec_choose_2.btn.OnClick(None, trigger_event=False, choose=bool(y_reverse))
                return

            @choose_1.unique_callback()
            def OnSelect(btn, choose, trigger_event, sec_choose_1=sec_choose_1, sec_choose_2=sec_choose_2):
                if choose:
                    sec_choose_1.setVisible(True)
                    sec_choose_2.setVisible(True)
                    if trigger_event:
                        AccInput().switch_acc_input_open_condition(OPEN_CONDITION_OPEN)
                        gyr_open_state, x_reverse, y_reverse = global_data.player.get_setting(uoc.GYROSCOPE_STATE_KEY)
                        global_data.player.write_setting(uoc.GYROSCOPE_STATE_KEY, [OPEN_CONDITION_OPEN, x_reverse, y_reverse], True)

            @choose_2.unique_callback()
            def OnSelect(btn, choose, trigger_event, sec_choose_1=sec_choose_1, sec_choose_2=sec_choose_2):
                if choose:
                    sec_choose_1.setVisible(True)
                    sec_choose_2.setVisible(True)
                    if trigger_event:
                        AccInput().switch_acc_input_open_condition(OPEN_CONDITION_AIM_OPEN)
                        _, x_reverse, y_reverse = global_data.player.get_setting(uoc.GYROSCOPE_STATE_KEY)
                        global_data.player.write_setting(uoc.GYROSCOPE_STATE_KEY, [OPEN_CONDITION_AIM_OPEN, x_reverse, y_reverse], True)

            @choose_3.unique_callback()
            def OnSelect(btn, choose, trigger_event, sec_choose_1=sec_choose_1, sec_choose_2=sec_choose_2):
                if choose:
                    sec_choose_1.setVisible(False)
                    sec_choose_2.setVisible(False)
                    if trigger_event:
                        AccInput().switch_acc_input_open_condition(OPEN_CONDITION_NONE)
                        _, x_reverse, y_reverse = global_data.player.get_setting(uoc.GYROSCOPE_STATE_KEY)
                        global_data.player.write_setting(uoc.GYROSCOPE_STATE_KEY, [OPEN_CONDITION_NONE, x_reverse, y_reverse], True)

            @sec_choose_1.unique_callback()
            def OnSelect(btn, choose, trigger_event):
                if trigger_event:
                    gyr_state, x_reverse, y_reverse = global_data.player.get_setting(uoc.GYROSCOPE_STATE_KEY)
                    global_data.player.write_setting(uoc.GYROSCOPE_STATE_KEY, [gyr_state, choose, y_reverse], True)
                    global_data.emgr.player_update_acc_sensitivity_event.emit()

            @sec_choose_2.unique_callback()
            def OnSelect(btn, choose, trigger_event):
                if trigger_event:
                    gyr_state, x_reverse, y_reverse = global_data.player.get_setting(uoc.GYROSCOPE_STATE_KEY)
                    global_data.player.write_setting(uoc.GYROSCOPE_STATE_KEY, [gyr_state, x_reverse, choose], True)
                    global_data.emgr.player_update_acc_sensitivity_event.emit()

            check_gyro()
        key = uoc.MECHA_JUMP_OPACITY_ENABLED_KEY
        choose = page.list_tab_translucence.GetItem(0)
        choose.setVisible(True)
        choose_1, choose_2 = init_radio_group_new(choose)
        attach_radio_group_data([choose_1, choose_2], [True, False])

        @choose_1.unique_callback()
        def OnSelect(btn, choose, trigger_event, key=key):
            if choose and trigger_event:
                global_data.player.write_setting_2(key, True, True)
                global_data.emgr.mecha_jump_opacity_enabled_changed.emit(True)

        @choose_2.unique_callback()
        def OnSelect(btn, choose, trigger_event, key=key):
            if choose and trigger_event:
                global_data.player.write_setting_2(key, False, True)
                global_data.emgr.mecha_jump_opacity_enabled_changed.emit(False)

        set_radio_group_item_select_new(choose.list_setting_item, global_data.player.get_setting_2(key), False)
        choose = page.list_tab_translucence.GetItem(1)
        choose.setVisible(True)
        choose_1, choose_2 = init_radio_group_new(choose)
        attach_radio_group_data([choose_1, choose_2], [True, False])

        @choose_1.unique_callback()
        def OnSelect(btn, choose, trigger_event, key=key):
            if choose and trigger_event:
                if global_data.player:
                    global_data.player.change_glide_effect_visibility(GEV_ONLY_FRIEND)

        @choose_2.unique_callback()
        def OnSelect(btn, choose, trigger_event, key=key):
            if choose and trigger_event:
                if global_data.player:
                    global_data.player.change_glide_effect_visibility(GEV_ALL)

        is_select = global_data.player.glide_effect_visibility == GEV_ONLY_FRIEND if global_data.player else False
        set_radio_group_item_select_new(choose.list_setting_item, is_select, False)
        self._refresh_aim_setting()
        self._refresh_down_settings()

    def _setup_common_choose(self, choose, key, faq_text_id, callback_func=None, flip=False, btn_question=None):
        init_radio_group(choose)
        choose_1 = choose.choose_1
        choose_2 = choose.choose_2
        attach_radio_group_data([choose_1, choose_2], [not flip, flip])

        @choose_1.unique_callback()
        def OnSelect(btn, choose, trigger_event, key=key):
            val = not flip
            if choose and trigger_event:
                global_data.player.write_setting_2(key, val, True)
                callable(callback_func) and callback_func(val)

        @choose_2.unique_callback()
        def OnSelect(btn, choose, trigger_event, key=key):
            val = flip
            if choose and trigger_event:
                global_data.player.write_setting_2(key, val, True)
                callable(callback_func) and callback_func(val)

        set_radio_group_item_select(choose, global_data.player.get_setting_2(key), False)
        if btn_question is None:
            btn_question = choose.lab_text.btn_question

        @btn_question.callback()
        def OnClick(btn, touch):
            self._on_question_click(FAQ_TITLE_ID, faq_text_id, btn)

        return

    def _setup_combine_choose(self, choose1, key1, faq_text_id1, choose2, key2, faq_text_id2, callback_func1=None, callback_func2=None, flip=False, btn_question1=None, btn_question2=None):

        def real_callback(flag):
            set_radio_group_enable_state_new(global_data.player.get_setting_2(key1), global_data.player.get_setting_2(key2), choose2)
            callback_func1 and callback_func1(flag)

        self._setup_common_choose(choose1, key1, faq_text_id1, real_callback, flip, btn_question1)
        self._setup_common_choose(choose2, key2, faq_text_id2, callback_func2, flip, btn_question2)
        set_radio_group_enable_state_new(global_data.player.get_setting_2(key1), global_data.player.get_setting_2(key2), choose2)

    def _on_question_click(self, title_id, content_id, btn=None):
        from logic.comsys.common_ui.GameRuleDescUI import GameRuleDescUI
        dlg = GameRuleDescUI()
        dlg.set_show_rule(title_id, content_id)
        if btn is not None:
            lpos = btn.getPosition()
            wpos = btn.getParent().convertToWorldSpace(lpos)
            lpos2 = dlg.panel.nd_game_describe.getParent().convertToNodeSpace(wpos)
            dlg.panel.nd_game_describe.setPosition(cc.Vec2(lpos2.x, lpos2.y + 200))
            dlg.panel.nd_game_describe.setAnchorPoint(cc.Vec2(1.0, 1.0))
        return

    def _refresh_aim_setting(self):
        aim_color_btns = [
         self.panel.nd_aim_color.nd_content.nd_color.btn_1,
         self.panel.nd_aim_color.nd_content.nd_color.btn_2,
         self.panel.nd_aim_color.nd_content.nd_color.btn_3,
         self.panel.nd_aim_color.nd_content.nd_color.btn_4,
         self.panel.nd_aim_color.nd_content.nd_color.btn_5,
         self.panel.nd_aim_color.nd_content.nd_color.btn_6]
        aim_color_list = uoc.AIM_COLOR_LIST
        cur_color_val = global_data.player.get_setting(uoc.AIM_COLOR_VAL)
        for idx, aim_color_btn in enumerate(aim_color_btns):
            aim_color_btn.img_color.SetColor(aim_color_list[idx])
            if abs(cur_color_val - aim_color_list[idx]) < 1:
                aim_color_btn.SetSelect(True)
            else:
                aim_color_btn.SetSelect(False)

            @aim_color_btn.callback()
            def OnClick(btn, touch, idx=idx):
                if not global_data.player:
                    return
                global_data.player.write_setting(uoc.AIM_COLOR_VAL, aim_color_list[idx])
                for _idx, aim_color_btn in enumerate(aim_color_btns):
                    if _idx == idx:
                        aim_color_btn.SetSelect(True)
                    else:
                        aim_color_btn.SetSelect(False)
                    self._update_aim_example(aim_color_list[idx])

                self._has_changed_aim_color = True

        self._update_aim_example(cur_color_val)

    def _update_aim_example(self, color):
        if color is not None:
            self.panel.nd_aim_color.nd_content.img_example.crosshair.SetColor(color)
            self.panel.nd_aim_color.nd_content.img_example.crosshair.setCascadeColorEnabled(True)
            self.panel.nd_icon_color.nd_content.img_example.crosshair.SetColor(color)
            self.panel.nd_icon_color.nd_content.img_example.crosshair.setCascadeColorEnabled(True)
        return

    def _refresh_down_settings(self):
        btn_ask = self.panel.nd_icon_color.nd_title_color.lab_color.nd_auto_fit.btn_question

        @btn_ask.callback()
        def OnClick(btn, touch):
            self._on_question_click(FAQ_TITLE_ID, 633877, btn)

        down_color_btns = [
         self.panel.nd_icon_color.nd_content.nd_color.btn_1,
         self.panel.nd_icon_color.nd_content.nd_color.btn_2,
         self.panel.nd_icon_color.nd_content.nd_color.btn_3,
         self.panel.nd_icon_color.nd_content.nd_color.btn_4,
         self.panel.nd_icon_color.nd_content.nd_color.btn_5,
         self.panel.nd_icon_color.nd_content.nd_color.btn_6]
        down_color_list = uoc.DOWN_COLOR_LIST if not G_IS_NA_PROJECT and not global_data.channel.get_app_channel() == 'steam' else uoc.DOWN_COLOR_LIST_SEA
        cur_color_val = global_data.player.get_setting(uoc.DOWN_COLOR_VAL)
        for idx, down_color_btn in enumerate(down_color_btns):
            down_color_btn.img_color.SetColor(down_color_list[idx])
            if abs(cur_color_val - down_color_list[idx]) < 1:
                down_color_btn.SetSelect(True)
            else:
                down_color_btn.SetSelect(False)

            @down_color_btn.callback()
            def OnClick(btn, touch, idx=idx):
                global_data.player.write_setting(uoc.DOWN_COLOR_VAL, down_color_list[idx])
                for _idx, down_color_btn in enumerate(down_color_btns):
                    if _idx == idx:
                        down_color_btn.SetSelect(True)
                    else:
                        down_color_btn.SetSelect(False)
                    self._update_down_example(down_color_list[idx])

                self._has_changed_down_color = True

        self._update_down_example(cur_color_val)

    def _update_down_example(self, color):
        if color is not None:
            self.panel.nd_icon_color.nd_content.img_example.crosshair_icon.SetColor(color)
            self.panel.nd_icon_color.nd_content.img_example.crosshair_icon.setCascadeColorEnabled(True)
        return

    def init_mecha_panel_arrow(self):
        self.mecha_expand_tip = SettingTips('setting_tips_mecha_expand', 'guide/i_guide_setting_mecha_expand', self.panel.nd_title_mecha, self.mecha_expand_tips_show_func, self.parent, self.panel)
        self.panel.icon_arrow.setFlippedY(True)

        @self.panel.btn_show.callback()
        def OnClick(btn, touch):
            self._need_show_mecha_setting = not self._need_show_mecha_setting
            self.parent.keep_unchanged_view_target(self.refresh_nd_tab_mecha_vis, offset=-250 if self._need_show_mecha_setting else 0)
            self.panel.icon_arrow.setFlippedY(not self._need_show_mecha_setting)

    def refresh_nd_tab_mecha_vis(self):
        self.panel.nd_tab_mecha.setVisible(self._need_show_mecha_setting)
        sz = self.panel.nd_tab_mecha.getContentSize()
        top_pos_y = sz.height
        last_pos_y = 0
        children = self.panel.nd_tab_mecha.GetChildren()
        redundancy = 15
        if children:
            last_one = children[-1]
            last_pos_y = last_one.getPosition().y - last_one.getAnchorPoint().y * last_one.getContentSize().height - redundancy
        w, h = self.panel.GetContentSize()
        h_change = top_pos_y - last_pos_y
        if not self._need_show_mecha_setting:
            self.panel.SetContentSize(w, h - h_change)
        else:
            self.panel.SetContentSize(w, h + h_change)
        children = self.panel.GetChildren()
        for child in children:
            _, y = child.GetPosition()
            if not self._need_show_mecha_setting:
                child.SetPosition('50%', y - h_change)
            else:
                child.SetPosition('50%', y + h_change)

    def mecha_expand_tips_show_func(self, guide_panel, time_check):

        @guide_panel.nd_touch.unique_callback()
        def OnClick(btn, touch):
            if time_check():
                guide_panel.setVisible(False)

        guide_panel.setVisible(True)
        inner_size = self.parent.panel.content_bar.page.GetInnerContentSize()
        scroll_dst_node = self.panel.nd_mecha
        lpos = scroll_dst_node.getPosition()
        wpos = scroll_dst_node.getParent().convertToWorldSpace(lpos)
        y = self.panel.convertToNodeSpace(wpos).y
        percent = min(int((inner_size.height - y) / inner_size.height * 100), 100)
        self.parent.panel.content_bar.page.jumpToPercentVertical(percent)
        target_nd = self.panel.nd_title_mecha
        import cc
        wpos = target_nd.ConvertToWorldSpace('50%', '50%')
        lpos = guide_panel.getParent().convertToNodeSpace(wpos)
        guide_panel.setPosition(lpos)
        width, height = target_nd.GetContentSize()
        guide_panel.SetContentSize(width, height)
        guide_panel.ChildResizeAndPosition()