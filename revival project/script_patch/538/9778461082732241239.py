# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/setting_ui/SettingWidget/PrivacySettingWidget.py
from __future__ import absolute_import
from __future__ import print_function
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gutils.pc_utils import adjust_setting_panel_pos_and_size
from logic.gcommon.common_const import ui_operation_const as uoc
from logic.gutils.template_utils import init_radio_group_new, set_radio_group_enable_state
from .SettingWidgetBase import SettingWidgetBase
from six.moves import range
import six
import cc
FAQ_TITLE_ID = 2293

class PrivacySettingWidget(SettingWidgetBase):

    def __init__(self, panel, parent):
        super(PrivacySettingWidget, self).__init__(panel, parent)

    def on_init_panel(self, **kwargs):
        self.init_panel(self.panel)
        adjust_setting_panel_pos_and_size(self.parent.panel.content_bar.page, self.parent, self.panel)
        self.process_events(is_bind=True)

    def on_exit_page(self, **kwargs):
        super(PrivacySettingWidget, self).on_exit_page()
        self.parent.panel.nd_layout_privacy.setVisible(False)
        self.parent.panel.page.SetContentSize(923, 471)
        self.sync_setting_data()

    def on_enter_page(self, **kwargs):
        super(PrivacySettingWidget, self).on_enter_page()
        self.parent.panel.nd_layout_privacy.setVisible(True)
        if self.parent.panel.list_btn_privacy.GetItemCount() > 0:
            self.parent.panel.page.SetContentSize(923, 405)

    def on_resolution_changed(self):
        if self.parent.panel.list_btn_privacy.GetItemCount() > 0:
            self.parent.panel.page.SetContentSize(923, 405)

    def on_recover_default(self, **kwargs):
        self.recover_base_settings()

    def destroy(self):
        self.process_events(is_bind=False)
        super(PrivacySettingWidget, self).destroy()

    def process_events(self, is_bind):
        emgr = global_data.emgr
        econf = {'update_setting_btn_red_point': self.update_privilege_setting_red_point,
           'invisible_times_change_event': self.on_invisible_times_change,
           'invisibel_state_change_event': self.on_invisibel_state_change,
           'update_underage_sub_setting': self.update_underage_sub_setting
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def init_panel(self, page):
        self._refresh_panel(page)

    def _refresh_panel(self, page):
        if not global_data.player:
            return
        else:
            choose = page.list_tab_privacy.GetItem(0)
            choose_1, choose_2 = init_radio_group_new(choose)

            @choose_1.unique_callback()
            def OnSelect(btn, choose, trigger_event):
                if choose and trigger_event:
                    global_data.player and global_data.player.write_setting_2(uoc.REVEAL_HISTORY_RECORD_KEY, True, True)

            @choose_2.unique_callback()
            def OnSelect(btn, choose, trigger_event):
                if choose and trigger_event:
                    global_data.player and global_data.player.write_setting_2(uoc.REVEAL_HISTORY_RECORD_KEY, False, True)

            if global_data.player.get_setting_2(uoc.REVEAL_HISTORY_RECORD_KEY):
                choose_1.btn_choose.OnClick(None, False)
            else:
                choose_2.btn_choose.OnClick(None, False)
            choose = page.list_tab_privacy.GetItem(1)
            choose_1, choose_2 = init_radio_group_new(choose)
            self.init_one_list_choose(self.panel.list_tab_privacy, 1, uoc.MALL_RECOMMEND)

            @choose.btn_ask.callback()
            def OnClick(btn, touch):
                self._on_question_click(FAQ_TITLE_ID, 860198, btn)

            choose = page.list_tab_privacy.GetItem(3)
            choose_1, choose_2 = init_radio_group_new(choose)

            @choose_1.unique_callback()
            def OnSelect(btn, choose, trigger_event):
                if choose and trigger_event:
                    global_data.player and global_data.player.write_setting_2(uoc.SS_SKIN_BATTLE_MSG_SHOW, True, True)

            @choose_2.unique_callback()
            def OnSelect(btn, choose, trigger_event):
                if choose and trigger_event:
                    global_data.player and global_data.player.write_setting_2(uoc.SS_SKIN_BATTLE_MSG_SHOW, False, True)

            if global_data.player.get_setting_2(uoc.SS_SKIN_BATTLE_MSG_SHOW):
                choose_1.btn_choose.OnClick(None, False)
            else:
                choose_2.btn_choose.OnClick(None, False)

            @choose.btn_ask.callback()
            def OnClick(btn, touch):
                self._on_question_click(FAQ_TITLE_ID, 610869, btn)

            choose = page.list_tab_privacy.GetItem(4)
            choose_1, choose_2 = init_radio_group_new(choose)

            @choose_1.unique_callback()
            def OnSelect(btn, choose, trigger_event):
                if choose and trigger_event:
                    global_data.player and global_data.player.write_setting_2(uoc.REVEAL_INTIMACY_RELATION_KEY, False, True)

            @choose_2.unique_callback()
            def OnSelect(btn, choose, trigger_event):
                if choose and trigger_event:
                    global_data.player and global_data.player.write_setting_2(uoc.REVEAL_INTIMACY_RELATION_KEY, True, True)

            if global_data.player.get_setting_2(uoc.REVEAL_INTIMACY_RELATION_KEY):
                choose_2.btn_choose.OnClick(None, False)
            else:
                choose_1.btn_choose.OnClick(None, False)
            choose = page.list_tab_privacy.GetItem(5)
            self.init_one_list_choose(self.panel.list_tab_privacy, 5, uoc.SHIELD_STRANGER_MSG_KEY)

            @choose.btn_ask.unique_callback()
            def OnClick(btn, touch):
                self._on_question_click(FAQ_TITLE_ID, 2349, btn)

            choose = page.list_tab_privacy.GetItem(6)
            choose_1, choose_2 = init_radio_group_new(choose)

            @choose_1.unique_callback()
            def OnSelect(btn, choose, trigger_event):
                if choose and trigger_event:
                    global_data.player and global_data.player.write_setting_2(uoc.ENABLE_BE_SPECTATED_KEY, True, True)

            @choose_2.unique_callback()
            def OnSelect(btn, choose, trigger_event):
                if choose and trigger_event:
                    global_data.player and global_data.player.write_setting_2(uoc.ENABLE_BE_SPECTATED_KEY, False, True)

            if global_data.player.get_setting_2(uoc.ENABLE_BE_SPECTATED_KEY):
                choose_1.btn_choose.OnClick(None, False)
            else:
                choose_2.btn_choose.OnClick(None, False)
            choose = page.list_tab_privacy.GetItem(7)
            choose_1, choose_2 = init_radio_group_new(choose)

            @choose_1.unique_callback()
            def OnSelect(btn, choose, trigger_event):
                if choose and trigger_event:
                    global_data.player and global_data.player.set_enable_invisible(True)

            @choose_2.unique_callback()
            def OnSelect(btn, choose, trigger_event):
                if choose and trigger_event:
                    global_data.player and global_data.player.set_enable_invisible(False)

            if global_data.player.is_invisible():
                choose_1.btn_choose.OnClick(None, False)
            else:
                choose_2.btn_choose.OnClick(None, False)
            left_invisible_times = global_data.player.get_left_invisible_times()
            choose.lab_times.SetString(get_text_by_id(2351).format(prog=left_invisible_times))
            choose.lab_times.setVisible(True)

            @choose.btn_ask.unique_callback()
            def OnClick(btn, touch):
                self._on_question_click(FAQ_TITLE_ID, 2350, btn)

            privilege_setting = page.temp_privacy
            privilege_setting.lab_title.SetString(get_text_by_id(610214))

            @privilege_setting.btn_set.unique_callback()
            def OnClick(btn, touch):
                from logic.comsys.setting_ui.PrivilegeSettingUI import PrivilegeSettingUI
                PrivilegeSettingUI()

            self.update_privilege_setting_red_point()
            choose = page.list_tab_privacy.GetItem(8)
            org_title_color = choose.lab_title.getColor()
            choose_1, choose_2 = init_radio_group_new(choose)

            @choose_1.unique_callback()
            def OnSelect(btn, choose, trigger_event):
                if choose and trigger_event:
                    choose_bind = page.list_tab_privacy.GetItem(9)
                    set_radio_group_enable_state(True, False, choose_bind, org_title_color)
                    global_data.player and global_data.player.write_setting_2(uoc.BLOCK_STRANGER_VISIT, False, True)

            @choose_2.unique_callback()
            def OnSelect(btn, choose, trigger_event):
                if choose and trigger_event and global_data.player:
                    choose_bind = page.list_tab_privacy.GetItem(9)
                    enable_left = global_data.player.get_setting_2(uoc.ENABLE_STRANGER_LEFT_MSG)
                    set_radio_group_enable_state(False, enable_left, choose_bind)
                    global_data.player.write_setting_2(uoc.BLOCK_STRANGER_VISIT, True, True)

            block_stranger_visit = global_data.player.get_setting_2(uoc.BLOCK_STRANGER_VISIT)
            if not block_stranger_visit:
                choose_1.btn_choose.OnClick(None, False)
            else:
                choose_2.btn_choose.OnClick(None, False)
            choose = page.list_tab_privacy.GetItem(9)
            choose_1, choose_2 = init_radio_group_new(choose)

            @choose_1.unique_callback()
            def OnSelect(btn, choose, trigger_event):
                if choose and trigger_event:
                    global_data.player and global_data.player.write_setting_2(uoc.ENABLE_STRANGER_LEFT_MSG, True, True)

            @choose_2.unique_callback()
            def OnSelect(btn, choose, trigger_event):
                if choose and trigger_event:
                    global_data.player and global_data.player.write_setting_2(uoc.ENABLE_STRANGER_LEFT_MSG, False, True)

            enable_stranger_left_msg = global_data.player.get_setting_2(uoc.ENABLE_STRANGER_LEFT_MSG)
            if enable_stranger_left_msg:
                choose_1.btn_choose.OnClick(None, False)
            else:
                choose_2.btn_choose.OnClick(None, False)
            if not block_stranger_visit:
                set_radio_group_enable_state(True, enable_stranger_left_msg, choose, org_title_color)
            else:
                set_radio_group_enable_state(False, False, choose)
            choose = page.list_tab_privacy.GetItem(10)
            choose_1, choose_2 = init_radio_group_new(choose)

            @choose_1.unique_callback()
            def OnSelect(btn, choose, trigger_event):
                if choose and trigger_event:
                    global_data.player and global_data.player.write_setting_2(uoc.ENABLE_REWARD_FRIEND_REPORT, True, True)

            @choose_2.unique_callback()
            def OnSelect(btn, choose, trigger_event):
                if choose and trigger_event:
                    global_data.player and global_data.player.write_setting_2(uoc.ENABLE_REWARD_FRIEND_REPORT, False, True)

            if global_data.player.get_setting_2(uoc.ENABLE_REWARD_FRIEND_REPORT):
                choose_1.btn_choose.OnClick(None, False)
            else:
                choose_2.btn_choose.OnClick(None, False)

            @choose.btn_ask.unique_callback()
            def OnClick(btn, touch):
                self._on_question_click(FAQ_TITLE_ID, 633748, btn)

            choose = page.list_tab_privacy.GetItem(11)
            choose_1, choose_2 = init_radio_group_new(choose)

            @choose_1.unique_callback()
            def OnSelect(btn, choose, trigger_event):
                if choose and trigger_event:
                    global_data.player and global_data.player.write_setting_2(uoc.ENABLE_STRANGER_ADD_FRIEND, True, True)

            @choose_2.unique_callback()
            def OnSelect(btn, choose, trigger_event):
                if choose and trigger_event:
                    global_data.player and global_data.player.write_setting_2(uoc.ENABLE_STRANGER_ADD_FRIEND, False, True)

            if global_data.player.get_setting_2(uoc.ENABLE_STRANGER_ADD_FRIEND):
                choose_1.btn_choose.OnClick(None, False)
            else:
                choose_2.btn_choose.OnClick(None, False)
            self.init_one_list_choose(self.panel.list_tab_privacy, 12, uoc.REVEAL_MECHA_MEMORY_RECORD_KEY)
            self.init_one_list_choose(self.panel.list_tab_privacy, 13, uoc.BLOCK_ALL_MSG_KEY)
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

    def recover_base_settings(self):
        if not global_data.player:
            return
        base_page_keys = {uoc.REVEAL_HISTORY_RECORD_KEY: {'need_write': True,'need_upload': True},uoc.MALL_RECOMMEND: {'need_write': True,'need_upload': True},uoc.SS_SKIN_BATTLE_MSG_SHOW: {'need_write': True,'need_upload': True},uoc.REVEAL_INTIMACY_RELATION_KEY: {'need_write': True,'need_upload': True},uoc.SHIELD_STRANGER_MSG_KEY: {'need_write': True,'need_upload': True},uoc.ENABLE_BE_SPECTATED_KEY: {'need_write': True,'need_upload': True},uoc.BLOCK_STRANGER_VISIT: {'need_write': True,'need_upload': True},uoc.ENABLE_STRANGER_LEFT_MSG: {'need_write': True,'need_upload': True},uoc.ENABLE_REWARD_FRIEND_REPORT: {'need_write': True,'need_upload': True},uoc.ENABLE_STRANGER_ADD_FRIEND: {'need_write': True,'need_upload': True},uoc.REVEAL_MECHA_MEMORY_RECORD_KEY: {'need_write': True,'need_upload': True},uoc.BLOCK_ALL_MSG_KEY: {'need_write': True,'need_upload': True}}
        for set_key, set_conf in six.iteritems(base_page_keys):
            default_setting = global_data.player.get_default_setting(set_key)
            need_write = set_conf.get('need_write', False)
            need_upload = set_conf.get('need_upload', False)
            event = set_conf.get('event')
            if need_write:
                global_data.player.write_setting(set_key, default_setting, need_upload)
            if event:
                global_data.emgr.fireEvent(event, default_setting)

        self._refresh_panel(self.panel)

    def sync_setting_data(self):
        if global_data.player:
            global_data.player.save_settings_to_file()

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

    def update_privilege_setting_red_point(self):
        from logic.gutils.red_point_utils import get_priv_setting_rp
        new_setting = get_priv_setting_rp()
        self.panel.temp_privacy.img_new.setVisible(new_setting)

    def on_invisible_times_change(self, new_times):
        nd_invisible = self.panel.list_tab_privacy.GetItem(7)
        if not nd_invisible:
            return
        nd_invisible.lab_times.SetString(get_text_by_id(2351).format(prog=new_times))

    def on_invisibel_state_change(self, enable):
        nd_invisible = self.panel.list_tab_privacy.GetItem(7)
        if not nd_invisible:
            return
        else:
            radio_list = nd_invisible.list_setting_item.GetAllItem()
            if enable:
                radio_list[0] and radio_list[0].btn_choose.OnClick(None, False)
            else:
                len(radio_list) > 1 and radio_list[1] and radio_list[1].btn_choose.OnClick(None, False)
            return

    def update_underage_sub_setting(self, key, value):
        if not (self.panel and self.panel.isValid()):
            return
        if key == uoc.MALL_RECOMMEND:
            self.init_one_list_choose(self.panel.list_tab_privacy, 1, uoc.MALL_RECOMMEND)
        elif key == uoc.SHIELD_STRANGER_MSG_KEY:
            self.init_one_list_choose(self.panel.list_tab_privacy, 5, uoc.SHIELD_STRANGER_MSG_KEY)