# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/setting_ui/SettingWidget/BaseSettingWidget.py
from __future__ import absolute_import
from __future__ import print_function
import six
from six.moves import range
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gutils.pc_utils import adjust_setting_panel_pos_and_size
from logic.gcommon.common_const import ui_operation_const as uoc
from logic.gutils.template_utils import init_radio_group_new, init_checkbox_group, attach_radio_group_data, set_radio_group_item_select_new, attach_checkbox_group_data, set_check_box_group_item_select, set_radio_group_enable_state
import cc
from logic.gutils import template_utils
from common.cfg import confmgr
from common.framework import Functor
from .SettingWidgetBase import SettingWidgetBase
import logic.gcommon.time_utility as time_utils
from cocosui import cc, ccui, ccs
from logic.gutils import red_point_utils
from logic.comsys.common_ui.NormalConfirmUI import SecondConfirmDlg2
INTRODUCE_2D_INJURE_ID = 5
INTRODUCE_3D_INJURE_ID = 6
FAQ_TITLE_ID = 2293

class BaseSettingWidget(SettingWidgetBase):

    def __init__(self, panel, parent):
        super(BaseSettingWidget, self).__init__(panel, parent)

    def on_init_panel(self, **kwargs):
        self.guide_setting_visable_sound = None
        self.visable_sound_limit = None
        self.init_panel(self.panel)
        adjust_setting_panel_pos_and_size(self.parent.panel.content_bar.page, self.parent, self.panel)
        self.process_events(is_bind=True)
        return

    def on_enter_page(self, **kwargs):
        super(BaseSettingWidget, self).on_enter_page()

    def on_exit_page(self, **kwargs):
        super(BaseSettingWidget, self).on_exit_page()
        self.sync_setting_data()

    def on_recover_default(self, **kwargs):
        self.recover_base_settings()

    def destroy(self):
        self.process_events(is_bind=False)
        if self.guide_setting_visable_sound and self.guide_setting_visable_sound.isValid():
            self.guide_setting_visable_sound.Destroy()
        self.guide_setting_visable_sound = None
        super(BaseSettingWidget, self).destroy()
        return

    def process_events(self, is_bind):
        emgr = global_data.emgr
        econf = {'quick_shortcut_order_change': self.on_quick_shortcut_order_change,
           'update_underage_sub_setting': self.update_underage_sub_setting
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def on_click_shake_option(self, key, *args):
        setting_key = uoc.CONF_SHAKE_KEY_PATTERN % key
        new_value = not global_data.player.get_setting(setting_key)
        global_data.player.write_setting(setting_key, new_value, True)

    def get_shake_option_setting_val(self, key):
        return bool(global_data.player.get_setting(uoc.CONF_SHAKE_KEY_PATTERN % key))

    def init_phone_shaking_group(self, page):
        temp_mech_destroy_shake = page.nd_tab_fight.choose_1
        temp_injure_shake = page.nd_tab_fight.choose_2
        init_checkbox_group((temp_mech_destroy_shake, temp_injure_shake))
        attach_checkbox_group_data((temp_mech_destroy_shake, temp_injure_shake), [uoc.CONF_SHAKE_MECHA_DESTROY, uoc.CONF_SHAKE_INJURE])

        @temp_mech_destroy_shake.unique_callback()
        def OnSelect(btn, choose_value, trigger_event):
            if trigger_event:
                self.on_click_shake_option(uoc.CONF_SHAKE_MECHA_DESTROY)

        @temp_injure_shake.unique_callback()
        def OnSelect(btn, choose_value, trigger_event):
            if trigger_event:
                self.on_click_shake_option(uoc.CONF_SHAKE_INJURE)

        temp_mech_destroy_shake.btn.OnClick(None, trigger_event=False, choose=self.get_shake_option_setting_val(uoc.CONF_SHAKE_MECHA_DESTROY))
        temp_injure_shake.btn.OnClick(None, trigger_event=False, choose=self.get_shake_option_setting_val(uoc.CONF_SHAKE_INJURE))
        return

    def init_panel(self, page):
        self.key_2_btn = {uoc.AUTO_OPEN_DOOR: page.list_tab_function1.GetItem(0),
           uoc.AUTO_PICK_KEY: page.list_tab_function1.GetItem(1),
           uoc.WEAPON_PICK_DIRECTLY_REPLACE_KEY: page.list_tab_function1.GetItem(2),
           uoc.AUTO_CLIMB: page.list_tab_function1.GetItem(3),
           uoc.ROCKER_DASH: page.list_tab_function1.GetItem(4),
           uoc.FREE_SIGHT_KEY: page.list_tab_function1.GetItem(5),
           uoc.ITEM_SHORT_CUT: page.list_tab_function1.GetItem(6),
           uoc.WEAPON_BAR_SKIN_SHOW_KEY: page.list_tab_function1.GetItem(7),
           uoc.DOUBLE_CLICK_MARK_KEY: page.list_tab_function1.GetItem(8),
           uoc.MATCH_SUCC_VIBRATE_KEY: page.list_tab_function1.GetItem(9),
           uoc.BIT_MODE: page.list_tab_function1.GetItem(10),
           uoc.SEASON_LEVEL_UP_REMINDER_KEY: page.list_tab_function1.GetItem(11),
           uoc.DANMU_SHOW_DEFAULT_HEAD: page.list_tab_function1.GetItem(12),
           uoc.AUTO_SHOW_PLANE_BIG_MAP: page.list_tab_function2.GetItem(0),
           uoc.SMALL_MAP_ROTATE: page.list_tab_function2.GetItem(1),
           uoc.TEAMMATE_DANMU: page.list_tab_function2.GetItem(2),
           uoc.PVE_RADAR_MAP_TYPE: page.list_tab_function2.GetItem(3),
           uoc.CHANGE_MECHA_SKIN_IN_BATTLE: page.list_tab_function2.GetItem(4),
           uoc.PVE_MECHA_RADAR: page.list_tab_function2.GetItem(5),
           uoc.UNDERAGE_MODE_KEY: page.list_tab_function2.GetItem(6),
           uoc.SOUND_VISIBLE_3D_KEY: page.list_tab_fight.GetItem(0),
           uoc.SOUND_VISIBLE_IN_MAP_KEY: page.list_tab_fight.GetItem(1),
           uoc.INJURE_VISIBLE_3D_KEY: page.list_tab_fight.GetItem(2),
           'shake': page.list_tab_fight.GetItem(0),
           uoc.SOUND_TIP_CD: page.list_tab_fight.GetItem(4)
           }
        h_change = 0
        if global_data.is_pc_mode:
            page.list_tab_function1.RecycleItem(self.key_2_btn[uoc.FREE_SIGHT_KEY])
            page.list_tab_function1.RecycleItem(self.key_2_btn[uoc.ROCKER_DASH])
            page.nd_tab_fight.choose_1.setVisible(False)
            page.nd_tab_fight.choose_2.setVisible(False)
            page.nd_tab_fight.lab_title.setVisible(False)
        _, ori_h = page.nd_function1.GetContentSize()
        _, h = page.list_tab_function1.GetContentSize()
        page.nd_function1.SetContentSize('100%', h)
        page.nd_function1.img_bg.SetContentSize('100%', '100%')
        h_change += ori_h - h
        _, y = page.nd_function1.GetPosition()
        page.nd_function1.SetPosition('50%', y - h_change / 2)
        _, y = page.nd_function2.GetPosition()
        page.nd_function2.SetPosition('50%', y + h_change)
        _, y = page.nd_fight.GetPosition()
        page.nd_fight.SetPosition('50%', y + h_change)
        self._refresh_panel(page)

    def _refresh_panel(self, page):
        if not global_data.player:
            return
        self._refresh_nd_function1_widget()
        self._refresh_nd_function2_widget()
        self._refresh_nd_fight_widget(page)
        self._refresh_nd_shortcut_widget()

    def _refresh_nd_function1_widget(self):
        choose = self.key_2_btn[uoc.AUTO_OPEN_DOOR]
        choose_1, choose_2 = init_radio_group_new(choose)

        @choose_1.unique_callback()
        def OnSelect(btn, choose, trigger_event):
            if choose and trigger_event:
                global_data.player and global_data.player.write_setting(uoc.AUTO_OPEN_DOOR, True, True)
                global_data.emgr.player_enable_auto_open_door.emit(True)

        @choose_2.unique_callback()
        def OnSelect(btn, choose, trigger_event):
            if choose and trigger_event:
                global_data.player and global_data.player.write_setting(uoc.AUTO_OPEN_DOOR, False, True)
                global_data.emgr.player_enable_auto_open_door.emit(False)

        if global_data.player.get_setting(uoc.AUTO_OPEN_DOOR):
            choose_1.btn_choose.OnClick(None, False)
        else:
            choose_2.btn_choose.OnClick(None, False)
        choose = self.key_2_btn[uoc.AUTO_PICK_KEY]
        choose_1, choose_2 = init_radio_group_new(choose)

        @choose_1.unique_callback()
        def OnSelect(btn, choose, trigger_event):
            if choose and trigger_event:
                global_data.player and global_data.player.write_setting(uoc.AUTO_PICK_KEY, True, True)
                global_data.emgr.player_enable_auto_pick_event.emit(True)

        @choose_2.unique_callback()
        def OnSelect(btn, choose, trigger_event):
            if choose and trigger_event:
                global_data.player and global_data.player.write_setting(uoc.AUTO_PICK_KEY, False, True)
                global_data.emgr.player_enable_auto_pick_event.emit(False)

        if global_data.player.get_setting(uoc.AUTO_PICK_KEY):
            choose_1.btn_choose.OnClick(None, False)
        else:
            choose_2.btn_choose.OnClick(None, False)
        choose = self.key_2_btn[uoc.WEAPON_PICK_DIRECTLY_REPLACE_KEY]
        choose_1, choose_2 = init_radio_group_new(choose)

        @choose_1.unique_callback()
        def OnSelect(btn, choose, trigger_event):
            if choose and trigger_event:
                global_data.player and global_data.player.write_setting(uoc.WEAPON_PICK_DIRECTLY_REPLACE_KEY, True, True)
                global_data.emgr.player_user_setting_changed_event.emit(uoc.WEAPON_PICK_DIRECTLY_REPLACE_KEY, True)

        @choose_2.unique_callback()
        def OnSelect(btn, choose, trigger_event):
            if choose and trigger_event:
                global_data.player and global_data.player.write_setting(uoc.WEAPON_PICK_DIRECTLY_REPLACE_KEY, False, True)
                global_data.emgr.player_user_setting_changed_event.emit(uoc.WEAPON_PICK_DIRECTLY_REPLACE_KEY, False)

        if global_data.player.get_setting(uoc.WEAPON_PICK_DIRECTLY_REPLACE_KEY):
            choose_1.btn_choose.OnClick(None, False)
        else:
            choose_2.btn_choose.OnClick(None, False)
        choose = self.key_2_btn[uoc.AUTO_CLIMB]
        choose_1, choose_2 = init_radio_group_new(choose)

        @choose_1.unique_callback()
        def OnSelect(btn, choose, trigger_event):
            if choose and trigger_event:
                global_data.player and global_data.player.write_setting(uoc.AUTO_CLIMB, True, True)
                global_data.emgr.player_enable_auto_climb.emit(True)

        @choose_2.unique_callback()
        def OnSelect(btn, choose, trigger_event):
            if choose and trigger_event:
                global_data.player and global_data.player.write_setting(uoc.AUTO_CLIMB, False, True)
                global_data.emgr.player_enable_auto_climb.emit(False)

        if global_data.player.get_setting(uoc.AUTO_CLIMB):
            choose_1.btn_choose.OnClick(None, False)
        else:
            choose_2.btn_choose.OnClick(None, False)

        @choose.btn_ask.callback()
        def OnClick(btn, touch):
            self._on_question_click(FAQ_TITLE_ID, 605011, btn)

        if not global_data.is_pc_mode:
            choose = self.key_2_btn[uoc.ROCKER_DASH]
            choose_1, choose_2 = init_radio_group_new(choose)

            @choose_1.unique_callback()
            def OnSelect(btn, choose, trigger_event):
                if choose and trigger_event:
                    global_data.player and global_data.player.write_setting(uoc.ROCKER_DASH, False, True)
                    global_data.emgr.player_enable_rocker_dash.emit(False)

            @choose_2.unique_callback()
            def OnSelect(btn, choose, trigger_event):
                if choose and trigger_event:
                    global_data.player and global_data.player.write_setting(uoc.ROCKER_DASH, True, True)
                    global_data.emgr.player_enable_rocker_dash.emit(True)

            if global_data.player.get_setting(uoc.ROCKER_DASH):
                choose_2.btn_choose.OnClick(None, False)
            else:
                choose_1.btn_choose.OnClick(None, False)
        if not global_data.is_pc_mode:
            choose = self.key_2_btn[uoc.FREE_SIGHT_KEY]
            choose_1, choose_2 = init_radio_group_new(choose)
            attach_radio_group_data([choose_1, choose_2], [uoc.FS_ONLY_ROCKER, uoc.FS_ROCKER_AND_SWITCH])

            @choose_1.unique_callback()
            def OnSelect(btn, choose, trigger_event):
                if choose and trigger_event:
                    global_data.emgr.free_sight_ope_change_event.emit(uoc.FS_ONLY_ROCKER)

            @choose_2.unique_callback()
            def OnSelect(btn, choose, trigger_event):
                if choose and trigger_event:
                    global_data.emgr.free_sight_ope_change_event.emit(uoc.FS_ROCKER_AND_SWITCH)

            set_radio_group_item_select_new(choose.list_setting_item, global_data.player.get_setting(uoc.FREE_SIGHT_KEY), False)
        choose = self.key_2_btn[uoc.ITEM_SHORT_CUT]
        choose_1, choose_2 = init_radio_group_new(choose)

        @choose_1.unique_callback()
        def OnSelect(btn, choose, trigger_event):
            if choose and trigger_event:
                global_data.player and global_data.player.write_setting_2(uoc.ITEM_SHORT_CUT, True, True)
                global_data.cam_lplayer and global_data.cam_lplayer.send_event('E_SHORT_CUT_REFRESH_STATE')

        @choose_2.unique_callback()
        def OnSelect(btn, choose, trigger_event):
            if choose and trigger_event:
                global_data.player and global_data.player.write_setting_2(uoc.ITEM_SHORT_CUT, False, True)

        if global_data.player.get_setting_2(uoc.ITEM_SHORT_CUT):
            choose_1.btn_choose.OnClick(None, False)
        else:
            choose_2.btn_choose.OnClick(None, False)

        @choose.btn_ask.callback()
        def OnClick(btn, touch):
            self._on_question_click(FAQ_TITLE_ID, 2329, btn)

        choose = self.key_2_btn[uoc.WEAPON_BAR_SKIN_SHOW_KEY]
        choose_1, choose_2 = init_radio_group_new(choose)

        @choose_1.unique_callback()
        def OnSelect(btn, choose, trigger_event):
            if choose and trigger_event:
                global_data.player and global_data.player.write_setting_2(uoc.WEAPON_BAR_SKIN_SHOW_KEY, True, True)
                global_data.emgr.weapon_skin_ope_change_event.emit()

        @choose_2.unique_callback()
        def OnSelect(btn, choose, trigger_event):
            if choose and trigger_event:
                global_data.player and global_data.player.write_setting_2(uoc.WEAPON_BAR_SKIN_SHOW_KEY, False, True)
                global_data.emgr.weapon_skin_ope_change_event.emit()

        if global_data.player.get_setting_2(uoc.WEAPON_BAR_SKIN_SHOW_KEY):
            choose_1.btn_choose.OnClick(None, False)
        else:
            choose_2.btn_choose.OnClick(None, False)
        choose = self.key_2_btn[uoc.DOUBLE_CLICK_MARK_KEY]
        choose_1, choose_2 = init_radio_group_new(choose)

        @choose_1.unique_callback()
        def OnSelect(btn, choose, trigger_event):
            if choose and trigger_event:
                global_data.player and global_data.player.write_setting_2(uoc.DOUBLE_CLICK_MARK_KEY, True, True)
                global_data.emgr.double_click_mark_change_event.emit()

        @choose_2.unique_callback()
        def OnSelect(btn, choose, trigger_event):
            if choose and trigger_event:
                global_data.player and global_data.player.write_setting_2(uoc.DOUBLE_CLICK_MARK_KEY, False, True)
                global_data.emgr.double_click_mark_change_event.emit()

        if global_data.player.get_setting_2(uoc.DOUBLE_CLICK_MARK_KEY):
            choose_1.btn_choose.OnClick(None, False)
        else:
            choose_2.btn_choose.OnClick(None, False)
        choose = self.key_2_btn[uoc.MATCH_SUCC_VIBRATE_KEY]
        choose_1, choose_2 = init_radio_group_new(choose)

        @choose_1.unique_callback()
        def OnSelect(btn, choose, trigger_event):
            if choose and trigger_event:
                global_data.player and global_data.player.write_setting_2(uoc.MATCH_SUCC_VIBRATE_KEY, True, True)

        @choose_2.unique_callback()
        def OnSelect(btn, choose, trigger_event):
            if choose and trigger_event:
                global_data.player and global_data.player.write_setting_2(uoc.MATCH_SUCC_VIBRATE_KEY, False, True)

        if global_data.player.get_setting_2(uoc.MATCH_SUCC_VIBRATE_KEY):
            choose_1.btn_choose.OnClick(None, False)
        else:
            choose_2.btn_choose.OnClick(None, False)
        choose = self.key_2_btn[uoc.BIT_MODE]
        choose_1, choose_2 = init_radio_group_new(choose)

        @choose_1.unique_callback()
        def OnSelect(btn, choose, trigger_event):
            if choose and trigger_event:
                if not (G_CLIENT_TRUNK or global_data.is_32bit_system()):
                    return

                def cb():
                    if global_data.player:
                        global_data.player.write_setting_2(uoc.BIT_MODE, '32bit', False)
                        global_data.achi_mgr.save_custom_bit_mode('32bit')
                        global_data.game_mgr.try_restart_app()

                def cancel_cb():
                    self._refresh_panel(self.panel)

                SecondConfirmDlg2(parent=self.panel).confirm(content=get_text_by_id(2359), confirm_callback=lambda : cb(), cancel_callback=lambda : cancel_cb())

        @choose_2.unique_callback()
        def OnSelect(btn, choose, trigger_event):
            if choose and trigger_event:
                if not (G_CLIENT_TRUNK or global_data.is_32bit_system()):
                    return

                def cb():
                    if global_data.player:
                        global_data.player.write_setting_2(uoc.BIT_MODE, '64bit', False)
                        global_data.achi_mgr.save_custom_bit_mode('64bit')
                        global_data.game_mgr.try_restart_app()

                def cancel_cb():
                    self._refresh_panel(self.panel)

                SecondConfirmDlg2(parent=self.panel).confirm(content=get_text_by_id(2358), confirm_callback=lambda : cb(), cancel_callback=lambda : cancel_cb())

        if global_data.is_32bit_system():
            if global_data.achi_mgr.get_custom_bit_mode() == '64bit':
                choose_2.btn_choose.OnClick(None, False)
            else:
                choose_1.btn_choose.OnClick(None, False)
        else:
            choose_2.btn_choose.OnClick(None, False)
            choose_1.btn_choose.SetEnable(False)
            choose_2.btn_choose.SetEnable(False)
            try:
                set_radio_group_enable_state(False, False, choose)
            except Exception as e:
                print('set_radio_group_enable_state failed for:%s' % e)

        choose = self.key_2_btn[uoc.SEASON_LEVEL_UP_REMINDER_KEY]
        choose_1, choose_2 = init_radio_group_new(choose)

        @choose_1.unique_callback()
        def OnSelect(btn, choose, trigger_event):
            if choose and trigger_event:
                global_data.player and global_data.player.write_setting_2(uoc.SEASON_LEVEL_UP_REMINDER_KEY, True, True)

        @choose_2.unique_callback()
        def OnSelect(btn, choose, trigger_event):
            if choose and trigger_event:
                global_data.player and global_data.player.write_setting_2(uoc.SEASON_LEVEL_UP_REMINDER_KEY, False, True)

        if global_data.player.get_setting_2(uoc.SEASON_LEVEL_UP_REMINDER_KEY):
            choose_1.btn_choose.OnClick(None, False)
        else:
            choose_2.btn_choose.OnClick(None, False)
        choose = self.key_2_btn[uoc.DANMU_SHOW_DEFAULT_HEAD]
        choose_1, choose_2 = init_radio_group_new(choose)

        @choose_1.unique_callback()
        def OnSelect(btn, choose, trigger_event):
            if choose and trigger_event and global_data.player:
                global_data.player.write_setting_2(uoc.DANMU_SHOW_DEFAULT_HEAD, True, True)

        @choose_2.unique_callback()
        def OnSelect(btn, choose, trigger_event):
            if choose and trigger_event and global_data.player:
                global_data.player.write_setting_2(uoc.DANMU_SHOW_DEFAULT_HEAD, False, True)

        enable_left = global_data.player.get_setting_2(uoc.DANMU_SHOW_DEFAULT_HEAD)
        if enable_left:
            choose_1.btn_choose.OnClick(None, False)
        else:
            choose_2.btn_choose.OnClick(None, False)
        if global_data.player.is_in_battle():
            set_radio_group_enable_state(False, enable_left, choose)
        else:
            set_radio_group_enable_state(True, enable_left, choose)

        @choose.btn_ask.callback()
        def OnClick(btn, touch):
            self._on_question_click(FAQ_TITLE_ID, 83594, btn)

        return

    def _refresh_nd_function2_widget(self):
        choose = self.key_2_btn[uoc.AUTO_SHOW_PLANE_BIG_MAP]
        choose_1, choose_2 = init_radio_group_new(choose)

        @choose_1.unique_callback()
        def OnSelect(btn, choose, trigger_event):
            if choose and trigger_event:
                global_data.player and global_data.player.write_setting(uoc.AUTO_SHOW_PLANE_BIG_MAP, True, True)

        @choose_2.unique_callback()
        def OnSelect(btn, choose, trigger_event):
            if choose and trigger_event:
                global_data.player and global_data.player.write_setting(uoc.AUTO_SHOW_PLANE_BIG_MAP, False, True)

        if global_data.player.get_setting(uoc.AUTO_SHOW_PLANE_BIG_MAP):
            choose_1.btn_choose.OnClick(None, False)
        else:
            choose_2.btn_choose.OnClick(None, False)
        choose = self.key_2_btn[uoc.SMALL_MAP_ROTATE]
        choose_1, choose_2 = init_radio_group_new(choose)

        def update_small_map_view_range():
            from logic.client.const import game_mode_const
            if not global_data.game_mode.is_mode_type((game_mode_const.GAME_MODE_DEATH, game_mode_const.GAME_MODE_FLAG, game_mode_const.GAME_MODE_CROWN, game_mode_const.GAME_MODE_RANDOM_DEATH, game_mode_const.GAME_MODE_MUTIOCCUPY)):
                return
            if global_data.battle:
                global_data.game_mgr.scene.get_com('PartMap').show_small_map_ui()

        @choose_1.unique_callback()
        def OnSelect(btn, choose, trigger_event):
            if choose and trigger_event:
                global_data.player and global_data.player.write_setting(uoc.SMALL_MAP_ROTATE, True, True)
                update_small_map_view_range()
                uoc.SMALL_MAP_ROTATE_ENABLE = True

        @choose_2.unique_callback()
        def OnSelect(btn, choose, trigger_event):
            if choose and trigger_event:
                global_data.player and global_data.player.write_setting(uoc.SMALL_MAP_ROTATE, False, True)
                update_small_map_view_range()
                uoc.SMALL_MAP_ROTATE_ENABLE = False

        if global_data.player.get_setting(uoc.SMALL_MAP_ROTATE):
            choose_1.btn_choose.OnClick(None, False)
            uoc.SMALL_MAP_ROTATE_ENABLE = True
        else:
            choose_2.btn_choose.OnClick(None, False)
            uoc.SMALL_MAP_ROTATE_ENABLE = False

        @choose.btn_ask.callback()
        def OnClick(btn, touch):
            self._on_question_click(FAQ_TITLE_ID, 2321, btn)

        choose = self.key_2_btn[uoc.TEAMMATE_DANMU]
        choose_1, choose_2 = init_radio_group_new(choose)

        @choose_1.unique_callback()
        def OnSelect(btn, choose, trigger_event):
            if choose and trigger_event:
                global_data.player and global_data.player.write_setting_2(uoc.TEAMMATE_DANMU, True, True)
                uoc.TEAMMATE_DANMU_ENABLE = True

        @choose_2.unique_callback()
        def OnSelect(btn, choose, trigger_event):
            if choose and trigger_event:
                global_data.player and global_data.player.write_setting_2(uoc.TEAMMATE_DANMU, False, True)
                uoc.TEAMMATE_DANMU_ENABLE = False

        if global_data.player.get_setting_2(uoc.TEAMMATE_DANMU):
            choose_1.btn_choose.OnClick(None, False)
        else:
            choose_2.btn_choose.OnClick(None, False)
        choose = self.key_2_btn[uoc.PVE_RADAR_MAP_TYPE]
        choose_1, choose_2 = init_radio_group_new(choose)

        @choose_1.unique_callback()
        def OnSelect(btn, choose, trigger_event):
            if choose and trigger_event:
                global_data.player and global_data.player.write_setting(uoc.PVE_RADAR_MAP_TYPE, True, True)
                uoc.PVE_RADAR_MAP_TYPE_ENABLE = True
                ui = global_data.ui_mgr.get_ui('PVERadarMapUI')
                ui and ui.set_map_type(1)

        @choose_2.unique_callback()
        def OnSelect(btn, choose, trigger_event):
            if choose and trigger_event:
                global_data.player and global_data.player.write_setting(uoc.PVE_RADAR_MAP_TYPE, False, True)
                uoc.PVE_RADAR_MAP_TYPE_ENABLE = False
                ui = global_data.ui_mgr.get_ui('PVERadarMapUI')
                ui and ui.set_map_type(2)

        ret = global_data.player.get_setting(uoc.PVE_RADAR_MAP_TYPE)
        if ret is None:
            ret = True
        if ret:
            choose_1.btn_choose.OnClick(None, False)
            uoc.PVE_RADAR_MAP_TYPE_ENABLE = True
        else:
            choose_2.btn_choose.OnClick(None, False)
            uoc.PVE_RADAR_MAP_TYPE_ENABLE = False
        choose = self.key_2_btn[uoc.CHANGE_MECHA_SKIN_IN_BATTLE]
        choose_1, choose_2 = init_radio_group_new(choose)

        @choose_1.unique_callback()
        def OnSelect(btn, choose, trigger_event):
            if choose and trigger_event:
                global_data.player and global_data.player.write_setting_2(uoc.CHANGE_MECHA_SKIN_IN_BATTLE, True, True)

        @choose_2.unique_callback()
        def OnSelect(btn, choose, trigger_event):
            if choose and trigger_event:
                global_data.player and global_data.player.write_setting_2(uoc.CHANGE_MECHA_SKIN_IN_BATTLE, False, True)

        if global_data.player.get_setting_2(uoc.CHANGE_MECHA_SKIN_IN_BATTLE):
            choose_1.btn_choose.OnClick(None, False)
        else:
            choose_2.btn_choose.OnClick(None, False)
        choose = self.key_2_btn[uoc.PVE_MECHA_RADAR]
        choose_1, choose_2, choose_3 = init_radio_group_new(choose)

        @choose_1.unique_callback()
        def OnSelect(btn, choose, trigger_event):
            if choose and trigger_event:
                global_data.player and global_data.player.write_setting_2(uoc.PVE_MECHA_RADAR, uoc.PVE_MECHA_RADAR_NONE, True)

        @choose_2.unique_callback()
        def OnSelect(btn, choose, trigger_event):
            if choose and trigger_event:
                global_data.player and global_data.player.write_setting_2(uoc.PVE_MECHA_RADAR, uoc.PVE_MECHA_RADAR_2D, True)

        @choose_3.unique_callback()
        def OnSelect(btn, choose, trigger_event):
            if choose and trigger_event:
                global_data.player and global_data.player.write_setting_2(uoc.PVE_MECHA_RADAR, uoc.PVE_MECHA_RADAR_3D, True)

        @choose.btn_ask.callback()
        def OnClick(btn, touch):
            self._on_question_click(FAQ_TITLE_ID, 2389, btn)

        setting = global_data.player.get_setting_2(uoc.PVE_MECHA_RADAR)
        if setting == uoc.PVE_MECHA_RADAR_NONE:
            choose_1.btn_choose.OnClick(None, False)
        elif setting == uoc.PVE_MECHA_RADAR_2D:
            choose_2.btn_choose.OnClick(None, False)
        elif setting == uoc.PVE_MECHA_RADAR_3D:
            choose_3.btn_choose.OnClick(None, False)
        from logic.comsys.setting_ui.UnderageHelper import underage_comfirm_callback

        def on_underage_select_cb(pwd):

            def underage_cancel_cb():
                global_data.player.write_setting_2(uoc.TEAM_ONLY_FRIEND_KEY, False, True)
                global_data.player and global_data.player.write_setting(uoc.UNDERAGE_MODE_KEY, '', True)
                global_data.emgr.player_underage_mode_changed_event.emit()
                self.update_underage_sub_setting(uoc.UNDERAGE_MODE_KEY, '')

            def underage_confirm_cb():
                global_data.player and global_data.player.write_setting_2(uoc.UNDERAGE_MODE_KEY, str(pwd), True)
                global_data.emgr.player_underage_mode_changed_event.emit()
                self.update_underage_sub_setting(uoc.UNDERAGE_MODE_KEY, pwd)

            if pwd:
                from logic.comsys.setting_ui.UnderageSettingUI import UnderageSettingUI
                age_ui = UnderageSettingUI()
                age_ui.set_callback(underage_confirm_cb, underage_cancel_cb)
            elif pwd == '':
                underage_cancel_cb()

        choose = self.panel.list_tab_function2.GetItem(6)
        choose_1, choose_2 = init_radio_group_new(choose)

        @choose_1.unique_callback()
        def OnSelect(btn, choose, trigger_event):
            if choose and trigger_event:
                self.update_underage_sub_setting(uoc.UNDERAGE_MODE_KEY, '')
                has_pwd = global_data.player and global_data.player.get_setting_2(uoc.UNDERAGE_MODE_KEY)
                if has_pwd:
                    return

                def cancel_cb():
                    self._refresh_panel(self.panel)

                SecondConfirmDlg2(parent=self.panel).confirm(content=get_text_by_id(635248), confirm_callback=lambda : underage_comfirm_callback(on_underage_select_cb), cancel_callback=lambda : cancel_cb())

        @choose_2.unique_callback()
        def OnSelect(btn, choose, trigger_event):
            if choose and trigger_event:
                self.update_underage_sub_setting(uoc.UNDERAGE_MODE_KEY, None)
                if global_data.player and global_data.player.get_setting_2(uoc.UNDERAGE_MODE_KEY):
                    underage_comfirm_callback(on_underage_select_cb)
            return

        @choose.btn_ask.callback()
        def OnClick(btn, touch):
            self._on_question_click(FAQ_TITLE_ID, 635247, btn)

        underage_pwd = global_data.player.get_setting_2(uoc.UNDERAGE_MODE_KEY)
        if type(underage_pwd) in [bool]:
            underage_pwd = ''
            global_data.player.write_setting_2(uoc.UNDERAGE_MODE_KEY, str(underage_pwd), True)
        if underage_pwd:
            choose_1.btn_choose.OnClick(None, False)
        else:
            choose_2.btn_choose.OnClick(None, False)
        return

    def _refresh_nd_fight_widget(self, page):
        choose = self.key_2_btn[uoc.SOUND_VISIBLE_3D_KEY]
        choose_1, choose_2 = init_radio_group_new(choose)

        @choose_1.unique_callback()
        def OnSelect(btn, choose, trigger_event):
            if choose and trigger_event:
                global_data.player and global_data.player.write_setting(uoc.SOUND_VISIBLE_3D_KEY, False, True)
                global_data.emgr.player_open_sound_visible3d.emit(True)

        @choose_2.unique_callback()
        def OnSelect(btn, choose, trigger_event):
            if choose and trigger_event:
                global_data.player and global_data.player.write_setting(uoc.SOUND_VISIBLE_3D_KEY, True, True)
                global_data.emgr.player_open_sound_visible3d.emit(False)

        if not global_data.player.get_setting(uoc.SOUND_VISIBLE_3D_KEY):
            choose_1.btn_choose.OnClick(None, False)
        else:
            choose_2.btn_choose.OnClick(None, False)

        @choose.btn_ask.callback()
        def OnClick(btn, touch):
            from logic.comsys.lobby.PlayIntroduceUI import PlayIntroduceUI
            PlayIntroduceUI(self.panel, INTRODUCE_3D_INJURE_ID)

        choose = self.key_2_btn[uoc.SOUND_VISIBLE_IN_MAP_KEY]
        choose_1, choose_2 = init_radio_group_new(choose)

        @choose_1.unique_callback()
        def OnSelect(btn, choose, trigger_event):
            if choose and trigger_event:
                global_data.player and global_data.player.write_setting(uoc.SOUND_VISIBLE_IN_MAP_KEY, True, True)
                global_data.emgr.player_open_sound_visible_in_map.emit(True)

        @choose_2.unique_callback()
        def OnSelect(btn, choose, trigger_event):
            if choose and trigger_event:
                global_data.player and global_data.player.write_setting(uoc.SOUND_VISIBLE_IN_MAP_KEY, False, True)
                global_data.emgr.player_open_sound_visible_in_map.emit(False)

        if global_data.player.get_setting(uoc.SOUND_VISIBLE_IN_MAP_KEY):
            choose_1.btn_choose.OnClick(None, False)
        else:
            choose_2.btn_choose.OnClick(None, False)

        @choose.btn_ask.callback()
        def OnClick(btn, touch):
            self._on_question_click(FAQ_TITLE_ID, 2325, btn)

        choose = self.key_2_btn[uoc.INJURE_VISIBLE_3D_KEY]
        choose_1, choose_2 = init_radio_group_new(choose)

        @choose_1.unique_callback()
        def OnSelect(btn, choose, trigger_event):
            if choose and trigger_event:
                global_data.player and global_data.player.write_setting(uoc.INJURE_VISIBLE_3D_KEY, False, True)
                global_data.emgr.player_open_injure_visible3d.emit(True)

        @choose_2.unique_callback()
        def OnSelect(btn, choose, trigger_event):
            if choose and trigger_event:
                global_data.player and global_data.player.write_setting(uoc.INJURE_VISIBLE_3D_KEY, True, True)
                global_data.emgr.player_open_injure_visible3d.emit(False)

        if not global_data.player.get_setting(uoc.INJURE_VISIBLE_3D_KEY):
            choose_1.btn_choose.OnClick(None, False)
        else:
            choose_2.btn_choose.OnClick(None, False)

        @choose.btn_ask.callback()
        def OnClick(btn, touch):
            from logic.comsys.lobby.PlayIntroduceUI import PlayIntroduceUI
            PlayIntroduceUI(self.panel, INTRODUCE_2D_INJURE_ID)

        if not global_data.is_pc_mode:
            self.init_phone_shaking_group(page)
        choose = self.key_2_btn[uoc.SOUND_TIP_CD]
        choose_1, choose_2 = init_radio_group_new(choose)

        @choose_1.unique_callback()
        def OnSelect(btn, choose, trigger_event):
            if choose and trigger_event:
                global_data.player and global_data.player.write_setting(uoc.SOUND_TIP_CD, True, True)
                global_data.emgr.player_open_sound_tip_cd.emit(True)

        @choose_2.unique_callback()
        def OnSelect(btn, choose, trigger_event):
            if choose and trigger_event:
                global_data.player and global_data.player.write_setting(uoc.SOUND_TIP_CD, False, True)
                global_data.emgr.player_open_sound_tip_cd.emit(False)

        if global_data.player.get_setting(uoc.SOUND_TIP_CD):
            choose_1.btn_choose.OnClick(None, False)
        else:
            choose_2.btn_choose.OnClick(None, False)
        return

    def init_one_list_choose(self, ui_list_item, index, key, select_cb=None):
        choose = ui_list_item.GetItem(index)
        choose_1, choose_2 = init_radio_group_new(choose)

        @choose_1.unique_callback()
        def OnSelect(btn, choose, trigger_event):
            if choose and trigger_event:
                global_data.player and global_data.player.write_setting_2(key, True, True)
                select_cb and select_cb(key, True)

        @choose_2.unique_callback()
        def OnSelect(btn, choose, trigger_event):
            if choose and trigger_event:
                global_data.player and global_data.player.write_setting_2(key, False, True)
                select_cb and select_cb(key, False)

        if global_data.player.get_setting_2(key):
            choose_1.btn_choose.OnClick(None, False)
        else:
            choose_2.btn_choose.OnClick(None, False)
        return

    def _refresh_nd_shortcut_widget(self):
        if global_data.player:
            shortcut_order = global_data.player.get_setting_2(uoc.SHORTCUT_ORDER) if 1 else list(range(7))
            shortcut_order = shortcut_order or list(range(7))
        shortcut_lst = self.panel.nd_shortcut.img_bg.lv_chat_list
        shortcut_lst.SetInitCount(len(shortcut_order))
        quick_chat_conf = confmgr.get('team_quick_chat', '0')
        for idx, shortcut_id in enumerate(shortcut_order):
            item = shortcut_lst.GetItem(idx)
            shortcut_conf = quick_chat_conf.get(str(shortcut_id))
            item.lab_content.SetString(shortcut_conf['text_id'], args={'second': 'n'})

        @self.panel.nd_shortcut.btn_common.unique_callback()
        def OnClick(*args):
            global_data.ui_mgr.show_ui('QuickChatSettingUI', 'logic.comsys.setting_ui')

        @self.panel.nd_shortcut.auto_pick_title.title.auto_fit.btn_question.unique_callback()
        def OnClick(btn, touch):
            dlg = global_data.ui_mgr.show_ui('GameRuleDescUI', 'logic.comsys.common_ui')
            dlg.set_show_rule(2293, 860180)

    def on_quick_shortcut_order_change(self):
        self._refresh_nd_shortcut_widget()

    def recover_base_settings(self):
        if not global_data.player:
            return
        base_page_keys = {uoc.AUTO_OPEN_DOOR: {'need_write': True,'need_upload': True},uoc.AUTO_PICK_KEY: {'need_write': True,'need_upload': True,'event': 'player_enable_auto_pick_event'},uoc.WEAPON_PICK_DIRECTLY_REPLACE_KEY: {'need_write': True,'need_upload': True},uoc.AUTO_CLIMB: {'need_write': True,'need_upload': True,'event': 'player_enable_auto_climb'},uoc.ROCKER_DASH: {'need_write': True,'need_upload': True,'event': 'player_enable_rocker_dash'},uoc.FREE_SIGHT_KEY: {'event': 'free_sight_ope_change_event'},uoc.ITEM_SHORT_CUT: {'need_write': True,'need_upload': True},uoc.WEAPON_BAR_SKIN_SHOW_KEY: {'need_write': True,'need_upload': True},uoc.DOUBLE_CLICK_MARK_KEY: {'need_write': True,'need_upload': False},uoc.MATCH_SUCC_VIBRATE_KEY: {'need_write': True,'need_upload': False},uoc.BIT_MODE: {'need_write': True,'need_upload': False},uoc.SEASON_LEVEL_UP_REMINDER_KEY: {'need_write': True,'need_upload': False},uoc.DANMU_SHOW_DEFAULT_HEAD: {'need_write': True,'need_upload': True},uoc.AUTO_SHOW_PLANE_BIG_MAP: {'need_write': True,'need_upload': True},uoc.SMALL_MAP_ROTATE: {'need_write': True,'need_upload': True},uoc.TEAMMATE_DANMU: {'need_write': True,'need_upload': True},uoc.PVE_RADAR_MAP_TYPE: {'need_write': True,'need_upload': True},uoc.CHANGE_MECHA_SKIN_IN_BATTLE: {'need_write': True,'need_upload': True},uoc.SOUND_VISIBLE_3D_KEY: {'need_write': True,'need_upload': True,'event': 'player_open_sound_visible3d'},uoc.SOUND_VISIBLE_IN_MAP_KEY: {'need_write': True,'need_upload': True,'event': 'player_open_sound_visible_in_map'},uoc.INJURE_VISIBLE_3D_KEY: {'need_write': True,'need_upload': True,'event': 'player_open_injure_visible3d'},uoc.SOUND_TIP_CD: {'need_write': True,'need_upload': True,'event': 'player_open_sound_tip_cd'},uoc.AIM_HELPER_KEY_1: {'need_write': True,'need_upload': True,'event': 'player_enable_aim_helper'},uoc.PC_FULL_SCREEN_KEY: {'need_write': True,'need_upload': True},uoc.CONF_SHAKE_KEY_PATTERN % uoc.CONF_SHAKE_MECHA_DESTROY: {'need_write': True,'need_upload': True},uoc.CONF_SHAKE_KEY_PATTERN % uoc.CONF_SHAKE_INJURE: {'need_write': True,'need_upload': True}}
        for set_key, set_conf in six.iteritems(base_page_keys):
            default_setting = global_data.player.get_default_setting(set_key)
            need_write = set_conf.get('need_write', False)
            need_upload = set_conf.get('need_upload', False)
            event = set_conf.get('event')
            if need_write:
                global_data.player.write_setting(set_key, default_setting, need_upload)
            if event:
                global_data.emgr.fireEvent(event, default_setting)

        global_data.player.write_setting_2(uoc.SHORTCUT_ORDER, list(range(7)), sync_to_server=True)
        global_data.emgr.quick_shortcut_order_change.emit()
        ui = global_data.ui_mgr.get_ui('PVERadarMapUI')
        ui and ui.set_map_type(1)
        global_data.player.write_setting_2(uoc.PVE_MECHA_RADAR, uoc.PVE_MECHA_RADAR_3D, True)
        self._refresh_panel(self.panel)

    def sync_setting_data(self):
        if global_data.player:
            global_data.player.save_settings_to_file()

    def show_setting_widget_sound(self):
        if global_data.achi_mgr.get_cur_user_archive_data('setting_red_point'):
            inner_size = self.parent.panel.content_bar.page.GetInnerContentSize()
            scroll_dst_node = self.panel.sound_and_injure.tips_anchor
            wpos = scroll_dst_node.getParent().convertToWorldSpace(scroll_dst_node.getPosition())
            y = self.panel.sound_and_injure.getParent().convertToNodeSpace(wpos).y
            offset = -160
            percent = int((inner_size.height - y + offset) / inner_size.height * 100)
            self.parent.panel.content_bar.page.jumpToPercentVertical(percent)
            self.show_guide_setting_visable_sound()
            global_data.achi_mgr.set_cur_user_archive_data('setting_red_point', 0)

    def show_guide_setting_visable_sound(self):
        panel = self.guide_setting_visable_sound
        if panel is None:
            panel = global_data.uisystem.load_template_create('guide/i_guide_setting_visable_sound', parent=self.parent.panel)
            self.guide_setting_visable_sound = panel

            @panel.unique_callback()
            def OnClick(btn, touch):
                if time_utils.time() - self.visable_sound_limit > 1:
                    self.guide_setting_visable_sound.setVisible(False)

        panel.setVisible(True)
        panel.temp_tips.lab_tips.SetString(get_text_local_content(2225))
        import cc
        wpos = self.panel.sound_and_injure.tips_anchor.ConvertToWorldSpace('50%', '50%')
        lpos = panel.nd_content.getParent().convertToNodeSpace(wpos)
        panel.nd_content.setPosition(lpos)
        self.visable_sound_limit = time_utils.time()
        return

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

    def update_underage_sub_setting(self, key, value):
        if not (self.panel and self.panel.isValid()):
            return
        else:
            if key == uoc.UNDERAGE_MODE_KEY:
                choose = self.panel.list_tab_function2.GetItem(6)
                choose_1, choose_2 = init_radio_group_new(choose)
                if global_data.player.get_setting_2(key):
                    choose_1.btn_choose.OnClick(None, False)
                else:
                    choose_2.btn_choose.OnClick(None, False)
            return

    def jump_to_underage_mode(self):
        nd = self.key_2_btn.get(uoc.UNDERAGE_MODE_KEY)
        center_wpos = nd.ConvertToWorldSpacePercentage(50, 50)
        scroll_pos = self.parent.panel.content_bar.page.GetInnerContainer().convertToNodeSpace(center_wpos)
        self.parent.panel.content_bar.page.CenterWithPos(scroll_pos.x, scroll_pos.y)