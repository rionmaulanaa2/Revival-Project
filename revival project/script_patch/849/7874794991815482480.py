# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/setting_ui/SettingWidget/MechaSensitivitySettingWidget.py
from __future__ import absolute_import
from six.moves import range
from logic.gcommon.common_const import ui_operation_const as uoc
from logic.gutils.pc_utils import adjust_setting_panel_pos_and_size
from .SettingWidgetBase import SettingWidgetBase
from logic.gutils.template_utils import init_radio_group, attach_radio_group_data, set_radio_group_item_select, init_checkbox_group, attach_checkbox_group_data, set_check_box_group_item_select
from logic.gutils.template_utils import init_setting_slider1
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gcommon.common_const.ui_operation_const import MECHA_SENS_TYPE_CUSTOM, MECHA_SENS_TYPE_PRESET_LOW, MECHA_SENS_TYPE_PRESET_MID, MECHA_SENS_TYPE_PRESET_HIGH
from logic.gutils import mecha_utils
from data.mecha_sens_open_scheme import check_scope_sensitivity_opened, check_scope_main_weapon_sensitivity_opened, check_scope_sub_weapon_sensitivity_opened, check_special_form_sensitivity_opened, check_special_form_main_weapon_sensitivity_opened, check_special_form_sub_weapon_sensitivity_opened
from common.cfg import confmgr
from logic.gutils.template_utils import set_slider_enable
from logic.gcommon.common_const.ui_operation_const import OPEN_CONDITION_NONE
SST_KEY_TO_CHECK_VALID_FUNC_MAP = {uoc.SST_SCR_SCOPE_MECHA_VAL_KEY: check_scope_sensitivity_opened,
   uoc.SST_GYROSCOPE_SCR_SCOPE_MECHA_VAL_KEY: check_scope_sensitivity_opened,
   uoc.SST_SCOPE_SAME_AS_NORMAL_KEY: (
                                    check_scope_main_weapon_sensitivity_opened, check_scope_sub_weapon_sensitivity_opened),
   uoc.SST_SCOPE_MAIN_WEAPON_STICK_SWITCH_MECHA_VAL_KEY: check_scope_main_weapon_sensitivity_opened,
   uoc.SST_SCOPE_MAIN_WEAPON_ROCKER_AS_SCREEN_KEY: check_scope_main_weapon_sensitivity_opened,
   uoc.SST_SCOPE_MAIN_WEAPON_STICK_MECHA_VAL_KEY: check_scope_main_weapon_sensitivity_opened,
   uoc.SST_SCOPE_SUB_WEAPON_STICK_SWITCH_MECHA_VAL_KEY: check_scope_sub_weapon_sensitivity_opened,
   uoc.SST_SCOPE_SUB_WEAPON_ROCKER_AS_SCREEN_KEY: check_scope_sub_weapon_sensitivity_opened,
   uoc.SST_SCOPE_SUB_WEAPON_STICK_MECHA_VAL_KEY: check_scope_sub_weapon_sensitivity_opened,
   uoc.SST_SCR_SPECIAL_FORM_MECHA_VAL_KEY: check_special_form_sensitivity_opened,
   uoc.SST_GYROSCOPE_SCR_SPECIAL_FORM_MECHA_VAL_KEY: check_special_form_sensitivity_opened,
   uoc.SST_SPECIAL_FORM_SAME_AS_NORMAL_KEY: (
                                           check_special_form_main_weapon_sensitivity_opened, check_special_form_sub_weapon_sensitivity_opened),
   uoc.SST_SPECIAL_FORM_MAIN_WEAPON_STICK_SWITCH_MECHA_VAL_KEY: check_special_form_main_weapon_sensitivity_opened,
   uoc.SST_SPECIAL_FORM_MAIN_WEAPON_ROCKER_AS_SCREEN_KEY: check_special_form_main_weapon_sensitivity_opened,
   uoc.SST_SPECIAL_FORM_MAIN_WEAPON_STICK_MECHA_VAL_KEY: check_special_form_main_weapon_sensitivity_opened,
   uoc.SST_SPECIAL_FORM_SUB_WEAPON_STICK_SWITCH_MECHA_VAL_KEY: check_special_form_sub_weapon_sensitivity_opened,
   uoc.SST_SPECIAL_FORM_SUB_WEAPON_ROCKER_AS_SCREEN_KEY: check_special_form_sub_weapon_sensitivity_opened,
   uoc.SST_SPECIAL_FORM_SUB_WEAPON_STICK_MECHA_VAL_KEY: check_special_form_sub_weapon_sensitivity_opened
   }

def _check_sst_key_valid(mecha_id, sst_key):
    if sst_key not in SST_KEY_TO_CHECK_VALID_FUNC_MAP:
        return True
    func = SST_KEY_TO_CHECK_VALID_FUNC_MAP[sst_key]
    if type(func) == tuple:
        for _func in func:
            if _func(mecha_id):
                return True

        return False
    return func(mecha_id)


class MechaSensitivitySettingWidget(SettingWidgetBase):
    SCREEN_SENS_KEYS = (
     uoc.SST_SCR_MECHA_VAL_KEY,
     uoc.SST_GYROSCOPE_SCR_MECHA_VAL_KEY)
    WEAPON_SENS_SWITCH_KEYS = (
     uoc.SST_MAIN_WEAPON_STICK_SWITCH_MECHA_VAL_KEY,
     uoc.SST_SUB_WEAPON_STICK_SWITCH_MECHA_VAL_KEY)
    WEAPON_AS_SCREEN_SENS_KEYS = (
     uoc.SST_MAIN_WEAPON_ROCKER_AS_SCREEN_KEY,
     uoc.SST_SUB_WEAPON_ROCKER_AS_SCREEN_KEY)
    WEAPON_SENS_KEYS = (
     uoc.SST_MAIN_WEAPON_STICK_MECHA_VAL_KEY,
     uoc.SST_SUB_WEAPON_STICK_MECHA_VAL_KEY)
    SCOPE_SCREEN_SENS_KEYS = (
     uoc.SST_SCR_SCOPE_MECHA_VAL_KEY,
     uoc.SST_GYROSCOPE_SCR_SCOPE_MECHA_VAL_KEY)
    SCOPE_WEAPON_SENS_SWITCH_KEYS = (
     uoc.SST_SCOPE_MAIN_WEAPON_STICK_SWITCH_MECHA_VAL_KEY,
     uoc.SST_SCOPE_SUB_WEAPON_STICK_SWITCH_MECHA_VAL_KEY)
    SCOPE_WEAPON_AS_SCREEN_SENS_KEYS = (
     uoc.SST_SCOPE_MAIN_WEAPON_ROCKER_AS_SCREEN_KEY,
     uoc.SST_SCOPE_SUB_WEAPON_ROCKER_AS_SCREEN_KEY)
    SCOPE_WEAPON_SENS_KEYS = (
     uoc.SST_SCOPE_MAIN_WEAPON_STICK_MECHA_VAL_KEY,
     uoc.SST_SCOPE_SUB_WEAPON_STICK_MECHA_VAL_KEY)
    SPECIAL_FORM_SCREEN_SENS_KEYS = (
     uoc.SST_SCR_SPECIAL_FORM_MECHA_VAL_KEY,
     uoc.SST_GYROSCOPE_SCR_SPECIAL_FORM_MECHA_VAL_KEY)
    SPECIAL_FORM_WEAPON_SENS_SWITCH_KEYS = (
     uoc.SST_SPECIAL_FORM_MAIN_WEAPON_STICK_SWITCH_MECHA_VAL_KEY,
     uoc.SST_SPECIAL_FORM_SUB_WEAPON_STICK_SWITCH_MECHA_VAL_KEY)
    SPECIAL_FORM_WEAPON_AS_SCREEN_SENS_KEYS = (
     uoc.SST_SPECIAL_FORM_MAIN_WEAPON_ROCKER_AS_SCREEN_KEY,
     uoc.SST_SPECIAL_FORM_SUB_WEAPON_ROCKER_AS_SCREEN_KEY)
    SPECIAL_FORM_WEAPON_SENS_KEYS = (
     uoc.SST_SPECIAL_FORM_MAIN_WEAPON_STICK_MECHA_VAL_KEY,
     uoc.SST_SPECIAL_FORM_SUB_WEAPON_STICK_MECHA_VAL_KEY)
    PLATFORM_EXCLUSIVE_CONF = {uoc.SST_GYROSCOPE_SCR_MECHA_VAL_KEY: ('mobile', ),
       uoc.SST_GYROSCOPE_SCR_SCOPE_MECHA_VAL_KEY: ('mobile', ),
       uoc.SST_GYROSCOPE_SCR_SPECIAL_FORM_MECHA_VAL_KEY: ('mobile', )
       }
    NAME_MAP = {uoc.SST_SCR_MECHA_VAL_KEY: 2248,
       uoc.SST_GYROSCOPE_SCR_MECHA_VAL_KEY: 2249,
       uoc.SST_SCR_SCOPE_MECHA_VAL_KEY: 2248,
       uoc.SST_GYROSCOPE_SCR_SCOPE_MECHA_VAL_KEY: 2249,
       uoc.SST_SCR_SPECIAL_FORM_MECHA_VAL_KEY: 2248,
       uoc.SST_GYROSCOPE_SCR_SPECIAL_FORM_MECHA_VAL_KEY: 2249,
       uoc.SST_MAIN_WEAPON_STICK_MECHA_VAL_KEY: 2250,
       uoc.SST_SUB_WEAPON_STICK_MECHA_VAL_KEY: 2251,
       uoc.SST_SCOPE_MAIN_WEAPON_STICK_MECHA_VAL_KEY: 2250,
       uoc.SST_SCOPE_SUB_WEAPON_STICK_MECHA_VAL_KEY: 2251,
       uoc.SST_SPECIAL_FORM_MAIN_WEAPON_STICK_MECHA_VAL_KEY: 2250,
       uoc.SST_SPECIAL_FORM_SUB_WEAPON_STICK_MECHA_VAL_KEY: 2251
       }

    def __init__(self, panel, parent):
        super(MechaSensitivitySettingWidget, self).__init__(panel, parent)

    def on_init_panel(self, **kwargs):
        self.guide_setting_as_rocker = None
        self.visable_as_rocker_limit = 0
        self._init_members()
        self._init_panel(self.panel)
        return

    def destroy(self):
        if self.guide_setting_as_rocker and self.guide_setting_as_rocker.isValid():
            self.guide_setting_as_rocker.Destroy()
        self.guide_setting_as_rocker = None
        super(MechaSensitivitySettingWidget, self).destroy()
        return

    def on_enter_page(self, **kwargs):
        super(MechaSensitivitySettingWidget, self).on_enter_page()
        self._refresh_apply_all_btn()
        not global_data.is_pc_mode and self._refresh_all_gyroscope_setting(self.panel)
        shoot_stick_switch_val = mecha_utils.get_mecha_sens_setting_val(self._cur_mecha_id, uoc.SST_SHOOT_STICK_SWITCH_MECHA_VAL_KEY)
        if shoot_stick_switch_val:
            main_weapon_stick_switch_val = mecha_utils.get_mecha_sens_setting_val(self._cur_mecha_id, uoc.SST_MAIN_WEAPON_STICK_SWITCH_MECHA_VAL_KEY)
        else:
            main_weapon_stick_switch_val, sub_weapon_stick_switch_val = False, False
        if main_weapon_stick_switch_val:
            self.check_show_guide_setting_as_rocker()

    def on_exit_page(self, **kwargs):
        super(MechaSensitivitySettingWidget, self).on_exit_page()

    def on_recover_default(self, **kwargs):

        def ok():
            self._restore_all_mechas()

        from logic.comsys.common_ui.NormalConfirmUI import SecondConfirmDlg2
        SecondConfirmDlg2().confirm(content=get_text_by_id(2252), confirm_callback=ok)

    def on_apply_all(self, **kwargs):

        def ok():
            self._apply_presets_to_all()

        from logic.comsys.common_ui.NormalConfirmUI import SecondConfirmDlg2
        SecondConfirmDlg2().confirm(content=get_text_by_id(2247), confirm_callback=ok)

    def _init_members(self):
        if global_data.player:
            open_info = global_data.player.read_mecha_open_info() if 1 else {}
            self._mecha_ids_readonly = open_info.get('opened_order', [])
            init_mecha_id = None
            if global_data.player and global_data.player.logic:
                init_mecha_id = global_data.player.logic.ev_g_get_bind_mecha_type()
            init_mecha_id = init_mecha_id or (self._mecha_ids_readonly[0] if self._mecha_ids_readonly else 8001)
        self._cur_mecha_id = init_mecha_id
        self._mecha_to_grid_node = {}
        self._init_panel_size = self.panel.GetContentSize()
        self._apply_all_dirty = True
        self.SCREEN_SENS_KEYS_INST = self._filter_plat_val_keys(self.SCREEN_SENS_KEYS)
        self.SCOPE_SCREEN_SENS_KEYS_INST = self._filter_plat_val_keys(self.SCOPE_SCREEN_SENS_KEYS)
        self.SPECIAL_FORM_SCREEN_SENS_KEYS_INST = self._filter_plat_val_keys(self.SPECIAL_FORM_SCREEN_SENS_KEYS)
        return

    def _filter_plat_val_keys(self, in_keys):
        out_keys = []
        for val_key in in_keys:
            if val_key in self.PLATFORM_EXCLUSIVE_CONF:
                plats = self.PLATFORM_EXCLUSIVE_CONF[val_key]
                if global_data.is_pc_mode and 'pc' not in plats:
                    continue
                if not global_data.is_pc_mode and 'mobile' not in plats:
                    continue
            out_keys.append(val_key)

        return out_keys

    def _init_panel(self, page):

        @page.btn_mech.unique_callback()
        def OnClick(btn, touch):
            self._set_mecha_drop_list_visible(not self._is_mecha_drop_list_visible())

        cnt = len(self._mecha_ids_readonly)
        page.list_mech_list.SetInitCount(cnt)
        for i in range(cnt):
            mecha_id = self._mecha_ids_readonly[i]
            item = page.list_mech_list.GetItem(i)
            self._mecha_to_grid_node[mecha_id] = item
            self._refresh_mecha_grid_basics(item.lab_mech_name, item.mach_head, mecha_id)
            self._refresh_mecha_grid_custom(item, mecha_id)

            @item.btn_shose_mech.unique_callback()
            def OnClick(btn, touch, mecha_id=mecha_id):
                self._select_mecha(mecha_id)
                self._set_mecha_drop_list_visible(False)

            self._update_lab_node(item.lab_mech_name, item.btn_shose_mech.GetSelect())

            def cb(btn_state, item=item):
                from common.uisys.uielment.CCButton import STATE_SELECTED
                selected = btn_state == STATE_SELECTED
                self._update_lab_node(item.lab_mech_name, selected)

            item.btn_shose_mech.set_state_changed_cb(cb)

        page.nd_hide_mecha_list_static.setVisible(False)

        @page.nd_hide_mecha_list_static.unique_callback()
        def OnClick(btn, touch):
            self._set_mecha_drop_list_visible(False)

        self._init_refresh_preset_area()
        self._select_mecha(self._cur_mecha_id, duplicate_check=False)

    @classmethod
    def _update_lab_node(cls, lab_node, selected):
        if not lab_node:
            return
        from common.uisys.uielment.CCButton import STATE_SELECTED
        if selected:
            lab_node.SetColor('#SW')
        else:
            lab_node.SetColor(4865186)

    @classmethod
    def _refresh_mecha_grid_basics(cls, lab_node, img_node, mecha_id):
        mecha_pic_path = 'gui/ui_res_2/mall/10100%s_2.png' % mecha_id
        img_node.SetDisplayFrameByPath('', mecha_pic_path)
        from logic.gutils import item_utils
        mecha_name_id = item_utils.get_mecha_name_by_id(mecha_id)
        lab_node.SetString(mecha_name_id)

    @classmethod
    def _refresh_mecha_grid_custom(cls, node, mecha_id):
        if not node.isValid():
            return
        custom = cls.is_mecha_sens_custom(mecha_id)
        node.img_bg_change.setVisible(custom)
        node.img_mark.setVisible(custom)
        node.img_bg.setVisible(not custom)

    @classmethod
    def is_mecha_sens_custom(cls, mecha_id):
        return cls._get_mecha_sens_setting_type(mecha_id) == MECHA_SENS_TYPE_CUSTOM

    def _select_mecha(self, mecha_id, duplicate_check=True):
        change = self._cur_mecha_id != mecha_id
        self._cur_mecha_id = mecha_id
        if not duplicate_check or change:
            self._refresh_cur_mecha(mecha_id)
            self._refresh_preset_area()
            self._refresh_sens_settings()

    def _get_mecha_grid(self, mecha_id):
        return self._mecha_to_grid_node.get(mecha_id, None)

    def _refresh_cur_mecha_custom_mark(self):
        item = self._get_mecha_grid(self._cur_mecha_id)
        if not item:
            return
        self._refresh_mecha_grid_custom(item, self._cur_mecha_id)

    def _refresh_all_mecha_custom_mark(self):
        for mecha_id in self._mecha_ids_readonly:
            item = self._get_mecha_grid(mecha_id)
            if not item:
                continue
            self._refresh_mecha_grid_custom(item, mecha_id)

    def _refresh_cur_mecha(self, mecha_id):
        self._refresh_mecha_grid_basics(self.panel.lab_name, self.panel.imd_head, mecha_id)

    def _set_mecha_drop_list_visible(self, vis):
        if vis:
            self.panel.img_arrow.SetFlippedY(False)
            self.panel.nd_mecha_list_static.setVisible(True)
            self.panel.nd_hide_mecha_list_static.setVisible(True)
        else:
            self.panel.img_arrow.SetFlippedY(True)
            self.panel.nd_mecha_list_static.setVisible(False)
            self.panel.nd_hide_mecha_list_static.setVisible(False)

    def _is_mecha_drop_list_visible(self):
        return self.panel.nd_mecha_list_static.isVisible()

    def _refresh_preset_area(self):
        return self._refresh_preset_area_core(self._cur_mecha_id)

    def _refresh_preset_area_core(self, mecha_id):
        sens_setting_type = self._get_mecha_sens_setting_type(mecha_id)
        if not self.panel:
            return
        choose = self.panel.nd_quick_set_static.choose
        set_radio_group_item_select(choose, sens_setting_type, False)

    @classmethod
    def _get_mecha_sens_setting_type(cls, mecha_id):
        return mecha_utils.get_mecha_sens_setting_type(mecha_id)

    def _init_refresh_preset_area(self):
        choose = self.panel.nd_quick_set_static.choose
        init_radio_group(choose)
        attach_radio_group_data([choose.choose_1, choose.choose_2, choose.choose_3, choose.choose_4], [MECHA_SENS_TYPE_PRESET_LOW, MECHA_SENS_TYPE_PRESET_MID, MECHA_SENS_TYPE_PRESET_HIGH, MECHA_SENS_TYPE_CUSTOM])

        @choose.choose_1.unique_callback()
        def OnSelect(btn, choose, trigger_event):
            if choose and trigger_event:
                mecha_utils.set_mecha_sens_setting_type(self._cur_mecha_id, MECHA_SENS_TYPE_PRESET_LOW)
                self._refresh_cur_mecha_custom_mark()
                self._refresh_sens_settings(check_adjustment=False)
                self._set_apply_all_dirty(True)

        @choose.choose_2.unique_callback()
        def OnSelect(btn, choose, trigger_event):
            if choose and trigger_event:
                mecha_utils.set_mecha_sens_setting_type(self._cur_mecha_id, MECHA_SENS_TYPE_PRESET_MID)
                self._refresh_cur_mecha_custom_mark()
                self._refresh_sens_settings(check_adjustment=False)
                self._set_apply_all_dirty(True)

        @choose.choose_3.unique_callback()
        def OnSelect(btn, choose, trigger_event):
            if choose and trigger_event:
                mecha_utils.set_mecha_sens_setting_type(self._cur_mecha_id, MECHA_SENS_TYPE_PRESET_HIGH)
                self._refresh_cur_mecha_custom_mark()
                self._refresh_sens_settings(check_adjustment=False)
                self._set_apply_all_dirty(True)

        @choose.choose_4.unique_callback()
        def OnSelect(btn, choose, trigger_event):
            if choose and trigger_event:
                mecha_utils.set_mecha_sens_setting_type(self._cur_mecha_id, MECHA_SENS_TYPE_CUSTOM)
                self._refresh_cur_mecha_custom_mark()
                self._refresh_sens_settings(check_adjustment=False)
                self._set_apply_all_dirty(True)

    def _refresh_sens_settings(self, check_adjustment=True):
        return self._refresh_sens_settings_core(self.panel, self._cur_mecha_id, check_adjustment)

    @classmethod
    def has_sp_sens(cls, mecha_id):
        d = {8007: 2244,
           8023: 2244
           }
        text_id = 2244
        if mecha_id in d:
            text_id = d[mecha_id]
        return (mecha_id in d, text_id)

    def get_name_text(self, val_key):
        return get_text_by_id(self.NAME_MAP.get(val_key, 2248))

    def _refresh_all_gyroscope_setting(self, page):
        gyroscope_open_state, _, _ = global_data.player.get_setting(uoc.GYROSCOPE_STATE_KEY)
        gyroscope_open_state = gyroscope_open_state != OPEN_CONDITION_NONE
        self._refresh_gyroscope_enabled(page.nd_cam.lv_camera, self.SCREEN_SENS_KEYS_INST, uoc.SST_GYROSCOPE_SCR_MECHA_VAL_KEY, force_open_state=gyroscope_open_state)
        self._refresh_gyroscope_enabled(page.nd_special.lv_camera, self.SCOPE_SCREEN_SENS_KEYS_INST, uoc.SST_GYROSCOPE_SCR_SCOPE_MECHA_VAL_KEY, force_open_state=gyroscope_open_state)
        self._refresh_gyroscope_enabled(page.nd_special2.lv_camera, self.SPECIAL_FORM_SCREEN_SENS_KEYS_INST, uoc.SST_GYROSCOPE_SCR_SPECIAL_FORM_MECHA_VAL_KEY, force_open_state=gyroscope_open_state)

    def _refresh_gyroscope_enabled(self, nd_list, screen_sens_keys_inst, target_key, force_open_state=None):
        if force_open_state is None:
            gyroscope_open_state, _, _ = global_data.player.get_setting(uoc.GYROSCOPE_STATE_KEY)
            gyroscope_open_state = gyroscope_open_state != OPEN_CONDITION_NONE
        else:
            gyroscope_open_state = force_open_state
        for index, slider_widget in enumerate(nd_list.GetAllItem()):
            val_key = screen_sens_keys_inst[index]
            if val_key == target_key:
                set_slider_enable(slider_widget, self.get_name_text(target_key), gyroscope_open_state, val_scale=uoc.SST_PERCENT_SCALE)

        return

    def _update_mecha_camera_sensitivity_option_appearance(self, mecha_id, nd_list, option_keys, gyroscope_key):
        nd_list.SetInitCount(len(option_keys))
        for index, val_key in enumerate(option_keys):
            slider_widget = nd_list.GetItem(index)
            val = mecha_utils.get_mecha_sens_setting_val(mecha_id, val_key)
            percent = self._convert_sst_to_percent(val)
            slider_widget.slider.setPercent(percent)

            def slide_cb(new_percent, sens_key=val_key):
                new_value = self._convert_percent_to_sst(new_percent)
                mecha_utils.set_mecha_sens_setting_val_direct(mecha_id, sens_key, new_value)
                if self._cur_mecha_id == mecha_id:
                    self._refresh_preset_area()
                    self._refresh_sens_settings(check_adjustment=False)
                    self._refresh_cur_mecha_custom_mark()
                    self._set_apply_all_dirty(True)

            init_setting_slider1(slider_widget, self.get_name_text(val_key), slide_cb, val_scale=uoc.SST_PERCENT_SCALE)

        gyroscope_key in option_keys and self._refresh_gyroscope_enabled(nd_list, option_keys, gyroscope_key)

    def _register_checkbox_callbacks(self, mecha_id, nd_checkbox, sens_key, force_sens_value=None, text_id=None, extra_fix_true_key=None):
        text_id and nd_checkbox.text.SetString(text_id)
        nd_checkbox_list = [nd_checkbox]
        init_checkbox_group(nd_checkbox_list)
        attach_checkbox_group_data(nd_checkbox_list, [sens_key])

        @nd_checkbox.unique_callback()
        def OnSelect(btn, choose_value, trigger_event):
            if trigger_event:
                if extra_fix_true_key and choose_value:
                    mecha_utils.set_mecha_sens_setting_val_direct(mecha_id, extra_fix_true_key, True)
                mecha_utils.set_mecha_sens_setting_val_direct(mecha_id, sens_key, choose_value)
                if self._cur_mecha_id == mecha_id:
                    self._refresh_sens_settings(check_adjustment=False)
                    self._refresh_cur_mecha_custom_mark()
                    self._set_apply_all_dirty(True)

        sens_value = mecha_utils.get_mecha_sens_setting_val(mecha_id, sens_key) if force_sens_value is None else force_sens_value
        set_check_box_group_item_select(nd_checkbox_list, sens_key, sens_value, trigger_event=False)
        return

    def _register_slider_callbacks(self, mecha_id, nd_slider, sens_key):
        sens_value = mecha_utils.get_mecha_sens_setting_val(mecha_id, sens_key)
        percent = self._convert_sst_to_percent(sens_value)
        nd_slider.slider.setPercent(percent)

        def slide_callback(new_percent):
            new_value = self._convert_percent_to_sst(new_percent)
            mecha_utils.set_mecha_sens_setting_val_direct(mecha_id, sens_key, new_value)
            if self._cur_mecha_id == mecha_id:
                self._refresh_preset_area()
                self._refresh_sens_settings(check_adjustment=False)
                self._refresh_cur_mecha_custom_mark()
                self._set_apply_all_dirty(True)

        init_setting_slider1(nd_slider, self.get_name_text(sens_key), slide_callback, val_scale=uoc.SST_PERCENT_SCALE)

    @staticmethod
    def _block_weapon_sensitivity_slider(nd_weapon, flag):
        nd_weapon.list_slider.nd_auto_fit.SetSwallowTouch(flag)
        nd_weapon.img_bg_slider.setVisible(flag)

    def _disable_weapon_sensitivity_setting(self, mecha_id, nd_weapon, sens_key, text_id):
        nd_weapon.list_check.SetInitCount(1)
        nd_rocker = nd_weapon.list_check.GetItem(0)
        self._register_checkbox_callbacks(mecha_id, nd_rocker, sens_key, force_sens_value=False, text_id=text_id)
        nd_rocker.btn.SetEnable(False)
        nd_weapon.list_slider.SetInitCount(1)
        self._block_weapon_sensitivity_slider(nd_weapon, True)

    def _update_weapon_sensitivity_setting(self, mecha_id, switch_on, as_screen, nd_weapon, sens_switch_key, as_screen_screen_key, sens_value_key, switch_text_id, extra_fix_true_key=None):
        nd_weapon.list_check.SetInitCount(1)
        nd_weapon.list_check.SetInitCount(2 if switch_on else 1)
        nd_rocker = nd_weapon.list_check.GetItem(0)
        nd_rocker.btn.SetEnable(True)
        self._register_checkbox_callbacks(mecha_id, nd_rocker, sens_switch_key, text_id=switch_text_id, extra_fix_true_key=extra_fix_true_key)
        if switch_on:
            nd_as_screen = nd_weapon.list_check.GetItem(1)
            self._register_checkbox_callbacks(mecha_id, nd_as_screen, as_screen_screen_key)
        nd_weapon.list_slider.SetInitCount(1)
        nd_slider = nd_weapon.list_slider.GetItem(0)
        self._register_slider_callbacks(mecha_id, nd_slider, sens_value_key)
        self._block_weapon_sensitivity_slider(nd_weapon, not switch_on or as_screen)

    def _update_mecha_weapon_sensitivity_option_appearance(self, mecha_id, nd, weapon_sensitivity_switch_keys, same_as_screen_keys, weapon_sensitivity_keys, main_opened, sub_opened, same_as_normal_key=None, total_switch_key=None):
        nd_main_weapon, nd_sub_weapon = nd.temp_weapon_1, nd.temp_weapon_2
        if main_opened and sub_opened:
            nd_main_weapon.setVisible(True)
            nd_sub_weapon.setVisible(True)
        else:
            nd_sub_weapon.setVisible(False)
            if sub_opened:
                nd_sub_weapon = nd_main_weapon
        main_switch_key, sub_switch_key = weapon_sensitivity_switch_keys
        if same_as_normal_key is not None:
            same_as_normal = mecha_utils.get_mecha_sens_setting_val(mecha_id, same_as_normal_key)
            self._register_checkbox_callbacks(mecha_id, nd.temp_check, same_as_normal_key, same_as_normal)
            if same_as_normal:
                self._disable_weapon_sensitivity_setting(mecha_id, nd.temp_weapon_1, main_switch_key, 609344)
                self._disable_weapon_sensitivity_setting(mecha_id, nd.temp_weapon_2, sub_switch_key, 609345)
                return
        main_as_screen_key, sub_as_screen_key = same_as_screen_keys
        main_sens_value_key, sub_sens_value_key = weapon_sensitivity_keys
        if total_switch_key is not None:
            if mecha_utils.get_mecha_sens_setting_val(mecha_id, total_switch_key):
                main_switch_on = mecha_utils.get_mecha_sens_setting_val(mecha_id, main_switch_key)
                if main_switch_on is None:
                    main_switch_on = True
                sub_switch_on = mecha_utils.get_mecha_sens_setting_val(mecha_id, sub_switch_key)
                if sub_switch_on is None:
                    sub_switch_on = True
                main_as_screen = mecha_utils.get_mecha_sens_setting_val(mecha_id, main_as_screen_key)
                sub_as_screen = mecha_utils.get_mecha_sens_setting_val(mecha_id, sub_as_screen_key)
            else:
                main_switch_on, sub_switch_on = False, False
                main_as_screen, sub_as_screen = False, False
                mecha_utils.set_mecha_sens_setting_val_direct(mecha_id, main_switch_key, False)
                mecha_utils.set_mecha_sens_setting_val_direct(mecha_id, sub_switch_key, False)
        else:
            main_switch_on = mecha_utils.get_mecha_sens_setting_val(mecha_id, main_switch_key)
            if main_switch_on is None:
                main_switch_on = True
            sub_switch_on = mecha_utils.get_mecha_sens_setting_val(mecha_id, sub_switch_key)
            if sub_switch_on is None:
                sub_switch_on = True
            main_as_screen = mecha_utils.get_mecha_sens_setting_val(mecha_id, main_as_screen_key)
            sub_as_screen = mecha_utils.get_mecha_sens_setting_val(mecha_id, sub_as_screen_key)
        if main_opened:
            self._update_weapon_sensitivity_setting(mecha_id, main_switch_on, main_as_screen, nd_main_weapon, main_switch_key, main_as_screen_key, main_sens_value_key, 609344, extra_fix_true_key=total_switch_key)
        rocker_btn = confmgr.get('mecha_conf', 'ActionConfig', 'Content', str(mecha_id), 'rocker_btn', default=[])
        if 'action4' in rocker_btn and sub_opened:
            self._update_weapon_sensitivity_setting(mecha_id, sub_switch_on, sub_as_screen, nd_sub_weapon, sub_switch_key, sub_as_screen_key, sub_sens_value_key, 609345, extra_fix_true_key=total_switch_key)
        else:
            nd_sub_weapon.setVisible(False)
        return

    def _refresh_sens_settings_core(self, page, mecha_id, check_adjustment=True):
        if not page:
            return
        self._update_mecha_camera_sensitivity_option_appearance(mecha_id, page.nd_cam.lv_camera, self.SCREEN_SENS_KEYS_INST, uoc.SST_GYROSCOPE_SCR_MECHA_VAL_KEY)
        self._update_mecha_weapon_sensitivity_option_appearance(mecha_id, page.nd_mobile_joystick, self.WEAPON_SENS_SWITCH_KEYS, self.WEAPON_AS_SCREEN_SENS_KEYS, self.WEAPON_SENS_KEYS, True, True, total_switch_key=uoc.SST_SHOOT_STICK_SWITCH_MECHA_VAL_KEY)
        hide_list = []
        if check_scope_sensitivity_opened(mecha_id):
            page.nd_special.setVisible(True)
            self._update_mecha_camera_sensitivity_option_appearance(mecha_id, page.nd_special.lv_camera, self.SCOPE_SCREEN_SENS_KEYS_INST, uoc.SST_GYROSCOPE_SCR_SCOPE_MECHA_VAL_KEY)
        else:
            page.nd_special.setVisible(False)
        main_opened, sub_opened = check_scope_main_weapon_sensitivity_opened(mecha_id), check_scope_sub_weapon_sensitivity_opened(mecha_id)
        if main_opened or sub_opened:
            page.nd_mobile_deformation_joystick.setVisible(True)
            self._update_mecha_weapon_sensitivity_option_appearance(mecha_id, page.nd_mobile_deformation_joystick, self.SCOPE_WEAPON_SENS_SWITCH_KEYS, self.SCOPE_WEAPON_AS_SCREEN_SENS_KEYS, self.SCOPE_WEAPON_SENS_KEYS, main_opened, sub_opened, same_as_normal_key=uoc.SST_SCOPE_SAME_AS_NORMAL_KEY)
        else:
            page.nd_mobile_deformation_joystick.setVisible(False)
            hide_list.append(page.nd_mobile_deformation_joystick)
        if check_special_form_sensitivity_opened(mecha_id):
            page.nd_special2.setVisible(True)
            self._update_mecha_camera_sensitivity_option_appearance(mecha_id, page.nd_special2.lv_camera, self.SPECIAL_FORM_SCREEN_SENS_KEYS_INST, uoc.SST_GYROSCOPE_SCR_SPECIAL_FORM_MECHA_VAL_KEY)
        else:
            page.nd_special2.setVisible(False)
        main_opened, sub_opened = check_special_form_main_weapon_sensitivity_opened(mecha_id), check_special_form_sub_weapon_sensitivity_opened(mecha_id)
        if main_opened or sub_opened:
            page.nd_mobile_deformation_joystick2.setVisible(True)
            self._update_mecha_weapon_sensitivity_option_appearance(mecha_id, page.nd_mobile_deformation_joystick2, self.SPECIAL_FORM_WEAPON_SENS_SWITCH_KEYS, self.SPECIAL_FORM_WEAPON_AS_SCREEN_SENS_KEYS, self.SPECIAL_FORM_WEAPON_SENS_KEYS, main_opened, sub_opened, same_as_normal_key=uoc.SST_SPECIAL_FORM_SAME_AS_NORMAL_KEY)
        else:
            page.nd_mobile_deformation_joystick2.setVisible(False)
            hide_list.append(page.nd_mobile_deformation_joystick2)
        if check_adjustment:
            adjust_setting_panel_pos_and_size(self.parent.panel.content_bar.page, self.parent, self.panel, total_size=self._init_panel_size, hide_list=hide_list)

    def _convert_percent_to_sst(self, percent):
        return self._convert_percent_to_value(percent, uoc.SST_RANGE)

    def _convert_sst_to_percent(self, sst):
        return self._convert_value_to_percent(sst, uoc.SST_RANGE)

    def _convert_percent_to_value(self, percent, range):
        from logic.gutils.template_utils import slider_convert_percent_to_value
        return slider_convert_percent_to_value(percent, range, clamp=True)

    def _convert_value_to_percent(self, value, range):
        from logic.gutils.template_utils import slider_convert_value_to_percent
        return slider_convert_value_to_percent(value, range, clamp=True)

    def _get_all_sens_val_keys(self):
        ret_set = set()
        lsts = [
         self.SCREEN_SENS_KEYS_INST, self.SCOPE_SCREEN_SENS_KEYS_INST, self.SPECIAL_FORM_SCREEN_SENS_KEYS_INST]
        if not global_data.is_pc_mode:
            lsts.append(self.WEAPON_SENS_KEYS)
            lsts.append(self.SCOPE_WEAPON_SENS_KEYS)
            lsts.append(self.SPECIAL_FORM_WEAPON_SENS_KEYS)
        for lst in lsts:
            for key in lst:
                ret_set.add(key)

        if not global_data.is_pc_mode:
            ret_set.add(uoc.SST_SHOOT_STICK_SWITCH_MECHA_VAL_KEY)
            ret_set.add(uoc.SST_MAIN_WEAPON_STICK_SWITCH_MECHA_VAL_KEY)
            ret_set.add(uoc.SST_SUB_WEAPON_STICK_SWITCH_MECHA_VAL_KEY)
            ret_set.add(uoc.SST_SCOPE_MAIN_WEAPON_STICK_SWITCH_MECHA_VAL_KEY)
            ret_set.add(uoc.SST_SCOPE_SUB_WEAPON_STICK_SWITCH_MECHA_VAL_KEY)
            ret_set.add(uoc.SST_SPECIAL_FORM_MAIN_WEAPON_STICK_SWITCH_MECHA_VAL_KEY)
            ret_set.add(uoc.SST_SPECIAL_FORM_SUB_WEAPON_STICK_SWITCH_MECHA_VAL_KEY)
        return ret_set

    def _apply_presets_to_all(self):
        if not self._cur_mecha_id:
            return
        target_mecha_id = self._cur_mecha_id
        ordered_sync_sens_val_keys = list(uoc.MECHA_SENS_PRESET_VAL_KEYS)
        target_vals = [ mecha_utils.get_mecha_sens_setting_val(target_mecha_id, val_key) for val_key in ordered_sync_sens_val_keys ]
        for mecha_id in self._mecha_ids_readonly:
            for i, val_key in enumerate(ordered_sync_sens_val_keys):
                if not _check_sst_key_valid(self._cur_mecha_id, val_key) or not _check_sst_key_valid(mecha_id, val_key):
                    continue
                target_val = target_vals[i]
                mecha_utils.set_mecha_sens_setting_val_direct(mecha_id, val_key, target_val)

        self._refresh_preset_area()
        self._refresh_sens_settings(check_adjustment=False)
        self._refresh_all_mecha_custom_mark()
        self._set_apply_all_dirty(False)

    def _restore_all_mechas(self):
        val_key_set = self._get_all_sens_val_keys()
        for mecha_id in self._mecha_ids_readonly:
            for key in val_key_set:
                if _check_sst_key_valid(mecha_id, key):
                    mecha_utils.restore_mecha_sens_settings(mecha_id, key)

        self._refresh_preset_area()
        self._refresh_sens_settings(check_adjustment=False)
        self._refresh_all_mecha_custom_mark()

    def _set_apply_all_dirty(self, dirty):
        prev_val = self._apply_all_dirty
        self._apply_all_dirty = dirty
        if prev_val != dirty:
            self._refresh_apply_all_btn()

    def _refresh_apply_all_btn(self):
        self._set_big_func_btn_enabled('btn_apply_all', self._apply_all_dirty)

    def check_show_guide_setting_as_rocker(self):
        if global_data.achi_mgr.get_cur_user_archive_data('setting_sst_as_rocker'):
            return
        else:
            import logic.gcommon.time_utility as time_utils
            panel = self.guide_setting_as_rocker
            if not (panel and panel.isValid()):
                self.guide_setting_as_rocker = None
                panel = self.guide_setting_as_rocker
            page = self.panel
            parent = page.nd_mobile_joystick.temp_weapon_1.list_check.GetItem(1)
            if panel is None:
                if parent:
                    panel = global_data.uisystem.load_template_create('common/i_common_tips_riko_frame', parent=parent)
                    panel.SetPosition('50%69', '50%')
                    panel.PlayAnimation('loop')
                    panel.lab_tips.setVisible(True)
                    self.guide_setting_as_rocker = panel

                @panel.nd_touch.unique_callback()
                def OnClick(btn, touch):
                    if time_utils.time() - self.visable_as_rocker_limit > 1:
                        if self.guide_setting_as_rocker:
                            self.guide_setting_as_rocker.setVisible(False)
                        global_data.achi_mgr.set_cur_user_archive_data('setting_sst_as_rocker', 1)

            panel.setVisible(True)
            panel.lab_tips.SetString(get_text_local_content(2334))
            self.parent.panel.content_bar.page.jumpToPercentVertical(100)
            self.visable_as_rocker_limit = time_utils.time()
            return