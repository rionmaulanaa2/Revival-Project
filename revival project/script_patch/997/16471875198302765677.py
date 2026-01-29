# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/setting_ui/PrivilegeSettingUI.py
from __future__ import absolute_import
from six.moves import range
from common.const.uiconst import DIALOG_LAYER_ZORDER
from logic.comsys.common_ui.WindowMediumBase import WindowMediumBase
from logic.comsys.setting_ui.SettingWidget.BaseSettingWidget import FAQ_TITLE_ID
from logic.gcommon.const import PRIVILEGE_SETTING_TO_RED_POINT, PRIVILEGE_LEVEL_TO_SETTING, PRIV_SETTING_KEYS, PRIV_SHOW_BADGE, PRIV_SHOW_PURPLE_ID, PRIV_SHOW_COLORFUL_FONT, PRIV_SHARE_MECHA_FASHION, PRIV_RED_PACKET, PRIV_SHARE_LOBBY_MECHA_FASHION
import cc
from logic.gutils.dress_utils import default_shadow_path
FAQ_PRIVILIGE_TITLE = 2293

class PrivilegeSettingUI(WindowMediumBase):
    PANEL_CONFIG_NAME = 'setting/i_setting_window_specialset'
    DLG_ZORDER = DIALOG_LAYER_ZORDER
    UI_ACTION_EVENT = {'nd_window.btn_close.OnClick': 'on_click_close_btn'
       }

    def on_init_panel(self):
        super(PrivilegeSettingUI, self).on_init_panel()
        self.panel.nd_window.lab_title.SetString(get_text_by_id(610196))
        self.init_paramater()
        self.init_privilege_setting()

    def init_paramater(self):
        self.key_btn = {PRIV_SHOW_BADGE: self.panel.list_tab_choose1.GetItem(0),
           PRIV_SHOW_COLORFUL_FONT: self.panel.list_tab_choose1.GetItem(1),
           PRIV_SHOW_PURPLE_ID: self.panel.list_tab_choose2.GetItem(0),
           PRIV_SHARE_MECHA_FASHION: self.panel.list_tab_choose2.GetItem(1),
           PRIV_RED_PACKET: self.panel.list_tab_choose3.GetItem(0),
           PRIV_SHARE_LOBBY_MECHA_FASHION: self.panel.list_tab_choose3.GetItem(1)
           }

    def init_privilege_setting(self):
        if not global_data.player:
            return
        priv_data = global_data.player.get_privilege_data()
        priv_lv = priv_data['priv_lv']
        uid = str(global_data.player.uid)
        priv_badge_setting_name = PRIV_SHOW_BADGE + uid
        btn_privilege_badge = self.key_btn[PRIV_SHOW_BADGE]
        btn_privilege_badge.text.SetString(610237)
        if priv_lv <= 0:
            btn_privilege_badge.img_lock.setVisible(True)
            btn_privilege_badge.choose.setVisible(False)
            btn_privilege_badge.btn.SetEnable(False)
            btn_privilege_badge.img_new.setVisible(False)
        else:
            btn_privilege_badge.img_lock.setVisible(False)
            btn_privilege_badge.choose.setVisible(global_data.achi_mgr.get_cur_user_archive_data(priv_badge_setting_name, default=False))

        @btn_privilege_badge.btn_ask.unique_callback()
        def OnClick(*args):
            self._on_question_click(FAQ_PRIVILIGE_TITLE, 610241)

        @btn_privilege_badge.btn.unique_callback()
        def OnClick(*args):
            is_enable = global_data.achi_mgr.get_cur_user_archive_data(priv_badge_setting_name, default=False)
            is_enable = not is_enable
            btn_privilege_badge.choose.setVisible(is_enable)
            btn_privilege_badge.img_new.setVisible(False)
            global_data.achi_mgr.set_cur_user_archive_data(priv_badge_setting_name, is_enable)
            global_data.player.update_privilege_setting(PRIV_SHOW_BADGE, is_enable)
            global_data.emgr.update_privilege_state.emit()

        priv_id_setting_name = PRIV_SHOW_PURPLE_ID + uid
        btn_privilege_id = self.key_btn[PRIV_SHOW_PURPLE_ID]
        purple_id_state = priv_data['priv_purple_id']
        btn_privilege_id.text.SetString(610238)
        if not purple_id_state:
            btn_privilege_id.img_lock.setVisible(True)
            btn_privilege_id.choose.setVisible(False)
            btn_privilege_id.btn.SetEnable(False)
            btn_privilege_id.img_new.setVisible(False)
        else:
            btn_privilege_id.img_lock.setVisible(False)
            btn_privilege_id.img_new.setVisible(False)
            btn_privilege_id.choose.setVisible(global_data.achi_mgr.get_cur_user_archive_data(priv_id_setting_name, default=False))

        @btn_privilege_id.btn_ask.unique_callback()
        def OnClick(*args):
            self._on_question_click(FAQ_PRIVILIGE_TITLE, 610242)

        @btn_privilege_id.btn.unique_callback()
        def OnClick(*args):
            is_enable = global_data.achi_mgr.get_cur_user_archive_data(priv_id_setting_name, default=False)
            is_enable = not is_enable
            btn_privilege_id.choose.setVisible(is_enable)
            btn_privilege_id.img_new.setVisible(False)
            global_data.achi_mgr.set_cur_user_archive_data(priv_id_setting_name, is_enable)
            global_data.player.update_privilege_setting(PRIV_SHOW_PURPLE_ID, is_enable)
            global_data.emgr.update_privilege_state.emit()

        priv_text_setting_name = PRIV_SHOW_COLORFUL_FONT + uid
        btn_privilege_text = self.key_btn[PRIV_SHOW_COLORFUL_FONT]
        colorful_font_state = priv_data['priv_colorful_font']
        btn_privilege_text.text.SetString(610239)
        if not colorful_font_state:
            btn_privilege_text.img_lock.setVisible(True)
            btn_privilege_text.choose.setVisible(False)
            btn_privilege_text.btn.SetEnable(False)
            btn_privilege_text.img_new.setVisible(False)
        else:
            btn_privilege_text.img_lock.setVisible(False)
            btn_privilege_text.img_new.setVisible(False)
            btn_privilege_text.choose.setVisible(global_data.achi_mgr.get_cur_user_archive_data(priv_text_setting_name, default=False))

        @btn_privilege_text.btn_ask.unique_callback()
        def OnClick(*args):
            self._on_question_click(FAQ_PRIVILIGE_TITLE, 610243)

        @btn_privilege_text.btn.unique_callback()
        def OnClick(*args):
            is_enable = global_data.achi_mgr.get_cur_user_archive_data(priv_text_setting_name, default=False)
            is_enable = not is_enable
            btn_privilege_text.choose.setVisible(is_enable)
            btn_privilege_text.img_new.setVisible(False)
            global_data.achi_mgr.set_cur_user_archive_data(priv_text_setting_name, is_enable)
            global_data.player.update_privilege_setting(PRIV_SHOW_COLORFUL_FONT, is_enable)
            global_data.emgr.update_privilege_state.emit()

        priv_share_mecha_fashion_setting_name = PRIV_SHARE_MECHA_FASHION + uid
        btn_priv_share = self.key_btn[PRIV_SHARE_MECHA_FASHION]
        priv_share_mecha_fashion = priv_data['priv_share_mecha_fashion']
        if not priv_share_mecha_fashion:
            btn_priv_share.img_lock.setVisible(True)
            btn_priv_share.choose.setVisible(False)
            btn_priv_share.btn.SetEnable(False)
            btn_priv_share.img_new.setVisible(False)
        else:
            btn_priv_share.img_lock.setVisible(False)
            btn_priv_share.img_new.setVisible(False)
            btn_priv_share.choose.setVisible(global_data.achi_mgr.get_cur_user_archive_data(priv_share_mecha_fashion_setting_name, default=False))

        @btn_priv_share.btn_ask.unique_callback()
        def OnClick(*args):
            self._on_question_click(FAQ_PRIVILIGE_TITLE, 611589)

        @btn_priv_share.btn.unique_callback()
        def OnClick(*args):
            is_enable = global_data.achi_mgr.get_cur_user_archive_data(priv_share_mecha_fashion_setting_name, default=False)
            is_enable = not is_enable
            btn_priv_share.choose.setVisible(is_enable)
            btn_priv_share.img_new.setVisible(False)
            global_data.achi_mgr.set_cur_user_archive_data(priv_share_mecha_fashion_setting_name, is_enable)
            global_data.player.update_privilege_setting(PRIV_SHARE_MECHA_FASHION, is_enable)
            global_data.emgr.update_privilege_state.emit()

        priv_share_lobby_mecha_fashion_setting_name = PRIV_SHARE_LOBBY_MECHA_FASHION + uid
        btn_prive_share_lobby = self.key_btn[PRIV_SHARE_LOBBY_MECHA_FASHION]
        if not priv_share_mecha_fashion:
            btn_prive_share_lobby.img_lock.setVisible(True)
            btn_prive_share_lobby.choose.setVisible(False)
            btn_prive_share_lobby.btn.SetEnable(False)
            btn_prive_share_lobby.img_new.setVisible(False)
        else:
            btn_prive_share_lobby.img_lock.setVisible(False)
            btn_prive_share_lobby.img_new.setVisible(False)
            btn_prive_share_lobby.choose.setVisible(global_data.achi_mgr.get_cur_user_archive_data(priv_share_lobby_mecha_fashion_setting_name, default=False))

        @btn_prive_share_lobby.btn_ask.unique_callback()
        def OnClick(*args):
            self._on_question_click(FAQ_PRIVILIGE_TITLE, 860318)

        @btn_prive_share_lobby.btn.unique_callback()
        def OnClick(*args):
            is_enable = global_data.achi_mgr.get_cur_user_archive_data(priv_share_lobby_mecha_fashion_setting_name, default=False)
            is_enable = not is_enable
            btn_prive_share_lobby.choose.setVisible(is_enable)
            btn_prive_share_lobby.img_new.setVisible(False)
            global_data.achi_mgr.set_cur_user_archive_data(priv_share_lobby_mecha_fashion_setting_name, is_enable)
            global_data.player.update_privilege_setting(PRIV_SHARE_LOBBY_MECHA_FASHION, is_enable)
            global_data.emgr.update_privilege_state.emit()

        priv_red_packet_setting_name = PRIV_RED_PACKET + uid
        btn_priv_red_packet = self.key_btn[PRIV_RED_PACKET]
        priv_red_packet = priv_data['priv_red_packet']
        if not priv_red_packet:
            btn_priv_red_packet.img_lock.setVisible(True)
            btn_priv_red_packet.choose.setVisible(False)
            btn_priv_red_packet.btn.SetEnable(False)
            btn_priv_red_packet.img_new.setVisible(False)
        else:
            btn_priv_red_packet.img_lock.setVisible(False)
            btn_priv_red_packet.img_new.setVisible(False)
            btn_priv_red_packet.choose.setVisible(global_data.achi_mgr.get_cur_user_archive_data(priv_red_packet_setting_name, default=False))

        @btn_priv_red_packet.btn_ask.unique_callback()
        def OnClick(*args):
            self._on_question_click(FAQ_PRIVILIGE_TITLE, 634756)

        @btn_priv_red_packet.btn.unique_callback()
        def OnClick(*args):
            is_enable = global_data.achi_mgr.get_cur_user_archive_data(priv_red_packet_setting_name, default=False)
            is_enable = not is_enable
            btn_priv_red_packet.choose.setVisible(is_enable)
            btn_priv_red_packet.img_new.setVisible(False)
            global_data.achi_mgr.set_cur_user_archive_data(priv_red_packet_setting_name, is_enable)
            global_data.player.update_privilege_setting(PRIV_RED_PACKET, is_enable)
            global_data.emgr.update_privilege_state.emit()

        self.refresh_red_point(priv_lv)

    def refresh_red_point(self, priv_lv):
        for i in range(1, priv_lv + 1):
            priv_settings = PRIVILEGE_LEVEL_TO_SETTING.get(i, [])
            if priv_settings:
                for setting in priv_settings:
                    btn_setting = self.key_btn[setting]
                    red_point_name = PRIVILEGE_SETTING_TO_RED_POINT[setting] + str(global_data.player.uid)
                    state = global_data.achi_mgr.get_cur_user_archive_data(red_point_name, default=-1)
                    if state == -1 or state == 1:
                        btn_setting.img_new.setVisible(False)
                    elif state == 0:
                        btn_setting.img_new.setVisible(True)
                        global_data.achi_mgr.set_cur_user_archive_data(red_point_name, 1)

        global_data.emgr.update_setting_btn_red_point.emit()

    def on_click_close_btn(self, touch, btn):
        self.close()

    def _on_question_click(self, title_id, content_id, btn=None):
        from logic.comsys.common_ui.GameRuleDescUI import GameRuleDescUI
        dlg = GameRuleDescUI()
        dlg.set_show_rule(title_id, content_id)
        if btn:
            lpos = btn.getPosition()
            wpos = btn.getParent().convertToWorldSpace(lpos)
            lpos2 = dlg.panel.nd_game_describe.getParent().convertToNodeSpace(wpos)
            dlg.panel.nd_game_describe.setPosition(cc.Vec2(lpos2.x, lpos2.y + 200))
            dlg.panel.nd_game_describe.setAnchorPoint(cc.Vec2(1.0, 1.0))