# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/role/PlayerRoleInfoWidget.py
from __future__ import absolute_import
import time
import common.utilities
from logic.gcommon.cdata import privilege_data
from logic.gcommon.common_const import ui_operation_const
from logic.gutils import follow_utils
from logic.gutils import role_head_utils
from logic.gutils import template_utils
from logic.gutils.template_utils import set_sex_node_img, update_badge_node
from logic.comsys.share.ScreenFrameHelper import ScreenFrameHelper
from common.const.property_const import *
from .BattleInfoSubWidget import BattleInfoSubWidget
from .PlayerTabBaseWidget import PlayerTabBaseWidget
from .CollectInfoSubWidget import CollectInfoSubWidget
from logic.gcommon.item import lobby_item_type
from logic.gcommon.const import AVATAR_SEX_NONE, PRIV_SHOW_BADGE, PRIV_SHOW_PURPLE_ID, PRIVILEGE_LEVEL_TO_SETTING, PRIVILEGE_SETTING_TO_RED_POINT
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gcommon.common_const.battlepass_const import SEASON_CARD_TYPE
from logic.gcommon.cdata.privilege_data import COLOR_NAME
from common.utils import ui_path_utils

class PlayerRoleInfoWidget(PlayerTabBaseWidget):
    PANEL_CONFIG_NAME = 'role/i_role_base_detail_new'
    SEND_CD = 5.0
    MAX_SIGNATURE_LEN = 60

    def on_player_stat_inf(self, stat_inf):
        cur_season_id = global_data.player.get_battle_season()
        if cur_season_id in stat_inf:
            self._stat_inf = stat_inf[cur_season_id]
            self.refresh_person_battle_info()

    def on_refresh_player_detail_inf(self, player_inf):
        self._player_inf = player_inf
        self.refresh_person_info(player_inf)
        signature = player_inf.get('intro', '')
        self.init_person_signature(signature)

    def __init__(self, parent_panel):
        super(PlayerRoleInfoWidget, self).__init__(parent_panel)
        self._my_uid = global_data.player.uid
        self._cur_uid = None
        self.qrcode_sprite = None
        self.personal_info = {}
        self._stat_inf = {}
        self._player_inf = {}
        self._last_send_time = 0
        self._need_up_btns = {}
        self._init_ui_event()
        self.process_event(True)
        self._signature = ''
        self.panel.btn_share.setVisible(False)
        self._share_content = None
        self._screen_capture_helper = ScreenFrameHelper()
        self._init_widget()
        return

    def _init_widget(self):
        self._collect_info_widget = None
        self._battle_info_widget = None
        self._battle_info_widget = BattleInfoSubWidget(self, self.panel.temp_content)
        from logic.comsys.share.ShareTipsWidget import ShareTipsWidget
        self._share_tips_widget = ShareTipsWidget(self, self.panel, self.panel.btn_share)
        self._battle_info_widget.show()
        self.panel.temp_content.setVisible(True)
        self.panel.btn_group_battle.SetSelect(True)
        self.panel.btn_group_collect.SetSelect(False)
        return

    def _init_ui_event(self):

        @self.panel.unique_callback()
        def OnClick(*args):
            if self.panel.nd_more.IsVisible():
                self.panel.nd_more.setVisible(False)

        @self.panel.btn_set.unique_callback()
        def OnClick(*args):
            if not self._cur_uid:
                return
            is_vis = self.panel.nd_more.IsVisible()
            self.panel.nd_more.setVisible(not is_vis)

        @self.panel.btn_group_battle.unique_callback()
        def OnClick(*args):
            if self._battle_info_widget.is_visible():
                return
            self._battle_info_widget.show()
            if self._collect_info_widget:
                self._collect_info_widget.hide()
            self.panel.btn_group_battle.SetSelect(True)
            self.panel.btn_group_collect.SetSelect(False)

        @self.panel.btn_group_collect.unique_callback()
        def OnClick(*args):
            if self._collect_info_widget is None:
                _nd = global_data.uisystem.load_template_create('role/i_role_base_tab_collect', self.panel.nd_role_details)
                _nd.ReConfPosition()
                self._collect_info_widget = CollectInfoSubWidget(self, _nd)
                if self._player_inf:
                    self._collect_info_widget.refresh(self._player_inf)
                self._collect_info_widget.show()
            else:
                if self._collect_info_widget.is_visible():
                    return
                self._collect_info_widget.show()
            self._battle_info_widget.hide()
            self.panel.btn_group_battle.SetSelect(False)
            self.panel.btn_group_collect.SetSelect(True)
            return

        @self.panel.btn_share.callback()
        def OnClick(btn, touch):
            player_ui = global_data.ui_mgr.get_ui('PlayerInfoUI')
            if player_ui:
                if not player_ui.is_all_model_loaded():
                    return
            ui_names = [
             'LobbyFullScreenBgUI']
            player_ui = global_data.ui_mgr.get_ui('PlayerInfoUI')
            if player_ui:
                player_ui.panel.temp_btn_back.setVisible(False)

            def cb(*args):
                self.panel.btn_share.setVisible(True and global_data.is_share_show)
                if player_ui:
                    player_ui.panel.temp_btn_back.setVisible(True)

            if self._screen_capture_helper:
                self.panel.btn_share.setVisible(False)
                if not self._share_content:
                    self._share_content = self.generate_share_content()
                else:
                    self._share_content.update_collect_state(self._player_inf)
                self._screen_capture_helper.set_custom_share_content(self._share_content)
                self._screen_capture_helper.take_screen_shot(ui_names, self.panel, custom_cb=cb)

        @self.panel.btn_report.unique_callback()
        def OnClick(*args):
            if self._cur_uid and self._player_inf:
                ui = global_data.ui_mgr.show_ui('UserReportUI', 'logic.comsys.report')
                ui.report_users([{'uid': self._cur_uid,'name': self._player_inf.get('char_name')}])
                from logic.gcommon.common_const.log_const import REPORT_FROM_TYPE_INFO, REPORT_CLASS_NORMAL
                ui.set_report_class(REPORT_CLASS_NORMAL)
                if self._player_inf:
                    signature = self._player_inf.get('intro', '')
                    ui.set_extra_report_info('', signature, REPORT_FROM_TYPE_INFO)

        @self.panel.btn_id_copy.unique_callback()
        def OnClick(*args):
            self.set_text_to_clipboard(self.panel.nd_id.lab_id.getString())

        @self.panel.nd_role_info.nd_sign.btn_rename.unique_callback()
        def OnClick(*args):
            if not self._cur_uid:
                return
            from logic.comsys.message.ChangeName import ChangeMotto
            ChangeMotto(placeholder=get_text_by_id(10047), max_length=100, send_callback=self.on_edit_box_send_callback, init_text=self._signature)

        @self.panel.nd_head.unique_callback()
        def OnClick(*args):
            if not self._cur_uid or self._cur_uid != self._my_uid:
                return
            self.btn_change_head_func()

        @self.panel.btn_lobby.unique_callback()
        def OnClick(*args):
            player = global_data.player
            if not player:
                return
            if not self._cur_uid:
                return
            player.request_visit_player(self._cur_uid)

    def generate_share_content(self):
        from logic.comsys.share.RoleCollectShareCreator import RoleCollectShareCreator
        share_creator = RoleCollectShareCreator()
        share_creator.create()
        share_content = share_creator
        share_content.update_collect_state(self._player_inf)
        return share_content

    def destroy(self):
        self.process_event(False)
        self._need_up_btns = {}
        super(PlayerRoleInfoWidget, self).destroy()
        if self.qrcode_sprite:
            self.qrcode_sprite.removeFromParent()
            self.qrcode_sprite = None
        self.personal_info = {}
        for widget_name in ['_screen_capture_helper', '_collect_info_widget', '_battle_info_widget', '_share_content', '_share_tips_widget']:
            widget = getattr(self, widget_name, None)
            if widget:
                widget.destroy()
                setattr(self, widget_name, None)

        return

    def process_event(self, is_bind):
        if is_bind:
            global_data.emgr.on_follow_result += self._refresh_follow_info
            global_data.emgr.on_undo_follow_result += self._refresh_follow_info
            global_data.emgr.player_on_change_name += self.on_change_name
            global_data.emgr.player_on_change_sex += self.on_change_sex
            global_data.emgr.player_on_change_intro += self.on_change_intro
            global_data.emgr.message_on_player_role_head += self.on_change_role_head
            global_data.emgr.message_on_player_role_head_photo += self.on_change_role_head_photo
            global_data.emgr.refresh_item_red_point += self.refresh_setting_rp
            global_data.emgr.update_privilege_state += self.update_privilege_state
            global_data.emgr.privilege_level_upgrade += self.update_privilege_state
            global_data.emgr.update_setting_btn_red_point += self.refresh_setting_rp
        else:
            global_data.emgr.on_follow_result -= self._refresh_follow_info
            global_data.emgr.on_undo_follow_result -= self._refresh_follow_info
            global_data.emgr.player_on_change_name -= self.on_change_name
            global_data.emgr.player_on_change_sex -= self.on_change_sex
            global_data.emgr.player_on_change_intro -= self.on_change_intro
            global_data.emgr.message_on_player_role_head -= self.on_change_role_head
            global_data.emgr.message_on_player_role_head_photo -= self.on_change_role_head_photo
            global_data.emgr.refresh_item_red_point -= self.refresh_setting_rp
            global_data.emgr.update_privilege_state -= self.update_privilege_state
            global_data.emgr.privilege_level_upgrade -= self.update_privilege_state
            global_data.emgr.update_setting_btn_red_point -= self.refresh_setting_rp

    def refresh_person_info(self, player_inf):
        from logic.gcommon.common_const import rank_const
        self._cur_uid = player_inf[U_ID]
        self.panel.btn_lobby.setVisible(self._my_uid != self._cur_uid)
        self.panel.btn_set.setVisible(True)
        self._init_set_buttons()
        if self._cur_uid == self._my_uid:
            self.panel.btn_share.setVisible(True and global_data.is_share_show)
            self.panel.btn_report.setVisible(False)
            self.panel.nd_role_info.nd_sign.btn_rename.setVisible(True)
        else:
            self.panel.btn_share.setVisible(False)
            self.panel.btn_report.setVisible(True)
            self.panel.nd_role_info.nd_sign.btn_rename.setVisible(False)
        name = player_inf['char_name']
        self.panel.nd_name.lab_name.SetString(str(name))
        if G_IS_NA_USER:
            self.panel.nd_id.lab_id.SetString(str(player_inf.get('bind_uid', self._cur_uid)))
        else:
            show_uid = int(player_inf.get('bind_uid', self._cur_uid))
            show_uid -= global_data.uid_prefix
            self.panel.nd_id.lab_id.SetString(str(show_uid))
        role_head_utils.init_role_head_auto(self.panel.nd_head, self._cur_uid, 0, player_inf)
        self.refresh_setting_rp()
        self.update_privilege_state()
        battle_pass_type = player_inf.get('battlepass_types', '0')
        battle_pass_path = ui_path_utils.SEASON_PASS_LOW_1_PATH
        for bp_type in battle_pass_type:
            if str(bp_type) in SEASON_CARD_TYPE:
                battle_pass_path = ui_path_utils.SEASON_PASS_LOW_PATH
                break

        self.panel.nd_bp_level.img_bp.SetDisplayFrameByPath('', battle_pass_path)
        battle_pass_lv = player_inf.get('battlepass_lv', 1)
        self.panel.lab_bp_level.setString(str(battle_pass_lv))
        sex = player_inf.get('sex', AVATAR_SEX_NONE)
        set_sex_node_img(self.panel.nd_name.lab_name.nd_auto_fit.img_gender, sex)
        clan_info = player_inf.get('clan_info', {})
        if not clan_info:
            self.panel.nd_crew.setVisible(False)
        else:
            clan_id = clan_info.get('clan_id', -1)
            if clan_id <= 0:
                self.panel.nd_crew.setVisible(False)
            else:
                self.panel.nd_crew.setVisible(True)
                self.panel.nd_crew.lab_crew.SetString(str(clan_info.get('clan_name')))
                self.panel.nd_crew.lab_crew_level.SetString(str(clan_info.get('lv', 0)))
                update_badge_node(clan_info.get('badge', 0), self.panel.nd_crew.temp_crew_logo)

                @self.panel.nd_crew.btn_crew.unique_callback()
                def OnClick(btn, touch, c_id=clan_id):
                    from logic.gutils.jump_to_ui_utils import jump_to_clan_card
                    jump_to_clan_card(c_id)

        self.panel.lab_follow.SetString(follow_utils.format_popular_num(player_inf.get('fans_count', 0)))
        self.panel.lab_charm.SetString(str(player_inf.get('charm', 0)))
        if self._battle_info_widget:
            self._battle_info_widget.refresh(player_inf)
        if self._collect_info_widget:
            self._collect_info_widget.refresh(player_inf)
        rank_use_title_dict = player_inf.get('rank_use_title_dict', {})
        rank_info = rank_const.get_rank_use_title(rank_use_title_dict)
        rank_title = rank_const.get_rank_use_title_type(rank_use_title_dict)
        template_utils.init_rank_title(self.panel.temp_title, rank_title, rank_info)

    def _init_set_buttons(self):
        if self._cur_uid == self._my_uid:
            btn_info = [{'name': 80830,'click_func': self.btn_change_head_func}, {'name': 80732,'click_func': self.btn_change_head_frame_func}, {'name': 81300,'click_func': self.btn_rename_func}, {'name': 862000,'click_func': self.btn_set_sex_func}, {'name': 80690,'click_func': self.btn_modify_into}, {'name': 610196,'click_func': self.btn_privilege_setting}, {'name': 611444,'click_func': self.btn_user_verify_code}]
        else:
            btn_info = [{'name': self._update_btn_name,'click_func': self.btn_follow,'btn_name': 'btn_follow'}]
        self.panel.nd_more.list_button.SetInitCount(len(btn_info))
        for idx, info in enumerate(btn_info):
            btn_node = self.panel.nd_more.list_button.GetItem(idx)
            name = info.get('name')
            if isinstance(name, int):
                btn_node.btn_common.SetText(name)
            else:
                btn_name = info.get('btn_name')
                name(btn_node, btn_name)
            click_func = info.get('click_func')
            btn_node.btn_common.BindMethod('OnClick', click_func)

    def refresh_person_battle_info(self):
        likenum = self._stat_inf.get('likenum', 0)
        likenum_str = follow_utils.format_popular_num(likenum)
        self.panel.lab_like.SetString(likenum_str)

    def set_text_to_clipboard(self, text):
        import game3d
        game3d.set_clipboard_text(text)
        global_data.game_mgr.show_tip(get_text_by_id(10053))

    def init_person_signature(self, signature):
        from logic.gcommon.common_utils.local_text import get_text_by_id
        is_avatar = self._my_uid == self._cur_uid
        placeholder = get_text_by_id(10047) if is_avatar else get_text_by_id(10048)
        self.panel.lab_signature.SetString(signature or placeholder)
        self._signature = signature

    def on_edit_box_send_callback(self, msg):
        if not self.panel:
            return False
        else:
            from logic.gcommon.common_utils.text_utils import check_review_words
            if len(msg) > 60:
                global_data.game_mgr.show_tip(get_text_by_id(2185))
                return False
            flag, msg = check_review_words(msg)
            if not flag:
                global_data.player.notify_client_message((get_text_by_id(10045),))
                return False
            if msg is None or not self.check_can_send():
                return False
            self._last_send_time = time.time()
            if global_data.player:
                global_data.player.set_introduction(msg)
                return True
            return False

    def check_can_send(self):
        import math
        MIN_SEND_TIME = self.SEND_CD
        cur_time = time.time()
        pass_time = cur_time - self._last_send_time
        if pass_time < MIN_SEND_TIME:
            global_data.game_mgr.show_tip(get_text_by_id(10064, {'time': str(int(math.ceil(MIN_SEND_TIME - pass_time)))}))
            return False
        return True

    def _update_btn_name(self, btn_node, btn_name):
        self._need_up_btns[btn_name] = btn_node
        if btn_name == 'btn_follow':
            if global_data.player and global_data.player.has_follow_player(self._cur_uid):
                btn_node.btn_common.SetText(10343)
            else:
                btn_node.btn_common.SetText(10344)

    def update_privilege_state(self):
        if self._cur_uid != self._my_uid:
            player_data = global_data.message_data.get_player_simple_inf(self._cur_uid)
            if not player_data:
                return
        else:
            if not global_data.player:
                return
            player_data = global_data.player.get_privilege_data()
        role_head_utils.init_privilege_name_color_and_badge(self.panel.nd_name.lab_name, self.panel.nd_head, player_data)

    def on_change_role_head(self, update_list):
        if self._cur_uid in update_list:
            role_head_utils.set_role_head_frame(self.panel.nd_head, update_list[self._cur_uid])

    def on_change_role_head_photo(self, update_list):
        if self._cur_uid in update_list:
            role_head_utils.set_role_head_photo(self.panel.nd_head, update_list[self._cur_uid])

    def on_change_name(self, cname):
        if self._my_uid == self._cur_uid:
            if self.panel:
                self.panel.nd_name.lab_name.SetString(cname)

    def on_change_sex(self, sex):
        if self._my_uid == self._cur_uid and self.panel and self.panel.isValid():
            set_sex_node_img(self.panel.nd_name.lab_name.nd_auto_fit.img_gender, sex)

    def on_change_intro(self, intro):
        if self._my_uid == self._cur_uid and self.panel and self.panel.isValid():
            self.init_person_signature(intro)

    def refresh_friend_rank_content(self, rank_type):
        self.refresh_person_battle_info()

    def _refresh_follow_info(self, *args):
        btn_node = self._need_up_btns.get('btn_follow', None)
        if btn_node:
            self._update_btn_name(btn_node, 'btn_follow')
        return

    def refresh_setting_rp(self):
        from logic.gutils import red_point_utils
        is_mine = self._cur_uid == self._my_uid
        new_photo = global_data.lobby_red_point_data.get_rp_by_type(lobby_item_type.L_ITEM_TYPE_HEAD_PHOTO)
        new_frame = global_data.lobby_red_point_data.get_rp_by_type(lobby_item_type.L_ITEM_TYPE_HEAD_FRAME)
        new_priv_setting = red_point_utils.get_priv_setting_rp()
        red_point_utils.show_red_point_template(self.panel.img_red_dot, is_mine and (new_frame or new_photo or new_priv_setting))
        self.panel.img_red_dot.setVisible(is_mine and (new_frame or new_photo or new_priv_setting))
        if self.panel.nd_more.list_button.GetItem(0) is not None:
            red_point_utils.show_red_point_template(self.panel.nd_more.list_button.GetItem(0).img_red_dot, is_mine and new_photo)
        if self.panel.nd_more.list_button.GetItem(1) is not None:
            red_point_utils.show_red_point_template(self.panel.nd_more.list_button.GetItem(1).img_red_dot, is_mine and new_frame)
        if self.panel.nd_more.list_button.GetItem(5) is not None:
            red_point_utils.show_red_point_template(self.panel.nd_more.list_button.GetItem(5).img_red_dot, is_mine and new_priv_setting)
        return

    def btn_rename_func(self, *args):
        from logic.gcommon.item.item_const import ITEM_NO_RENAME_CARD
        if not global_data.player:
            return
        clan_ticket_num = global_data.player.get_item_money(ITEM_NO_RENAME_CARD)
        if clan_ticket_num <= 0:
            from logic.comsys.common_ui.NormalConfirmUI import SecondConfirmDlg2
            from logic.comsys.mall_ui.BuyConfirmUIInterface import groceries_buy_confirmUI
            from logic.client.const.mall_const import ROLE_CHANGE_NAME_CARD_GOODS_ID

            def call_back():
                groceries_buy_confirmUI(ROLE_CHANGE_NAME_CARD_GOODS_ID)

            SecondConfirmDlg2().confirm(content=10355, confirm_callback=call_back)
        else:
            global_data.ui_mgr.show_ui('ChangeName', 'logic.comsys.message')

    def btn_set_sex_func(self, *args):
        if global_data.player:
            sex = global_data.player.get_sex()
            ui = global_data.ui_mgr.show_ui('ChangeSexUI', 'logic.comsys.message')
            ui.set_original_sex(sex)

    def btn_modify_into(self, *args):
        from logic.comsys.message.ChangeName import ChangeMotto
        ChangeMotto(placeholder=get_text_by_id(10047), max_length=100, send_callback=self.on_edit_box_send_callback, init_text=self._signature)

    def btn_change_head_func(self, *args):
        ui = global_data.ui_mgr.show_ui('ChangeHeadUI', 'logic.comsys.role')
        ui.on_tab_selected(1)

    def btn_change_head_frame_func(self, *args):
        ui = global_data.ui_mgr.show_ui('ChangeHeadUI', 'logic.comsys.role')
        ui.on_tab_selected(0)

    def btn_copy_id_func(self, *args):
        self.set_text_to_clipboard(self.panel.nd_id.lab_id.getString())

    def btn_follow(self, *args):
        if global_data.player and not global_data.player.has_follow_player(self._cur_uid):
            global_data.player.try_follow(self._cur_uid)
        else:
            from logic.comsys.common_ui.NormalConfirmUI import SecondConfirmDlg2

            def click_unfollow():
                global_data.player and global_data.player.try_unfollow(self._cur_uid)

            if global_data.player and global_data.player.has_follow_player(self._cur_uid):
                SecondConfirmDlg2().confirm(content=get_text_by_id(10345), confirm_callback=click_unfollow)

    def btn_privilege_setting(self, *args):
        from logic.comsys.setting_ui.PrivilegeSettingUI import PrivilegeSettingUI
        PrivilegeSettingUI()

    def btn_user_verify_code(btn, *args):
        from logic.comsys.common_ui.UserVerifyCodeUI import UserVerifyCodeUI
        UserVerifyCodeUI()

    def init_qrcode(self):
        if self._cur_uid != self._my_uid:
            if self.qrcode_sprite:
                self.qrcode_sprite.setVisible(False)
            return
        if self.qrcode_sprite:
            self.qrcode_sprite.setVisible(True)
            return
        import game3d
        import os
        file_name = str(global_data.player.uid) + '_qrcode.png'
        file_path = game3d.get_doc_dir() + '/res_patch/' + file_name
        if os.path.exists(file_path):
            self.create_qrcode_pic(file_name)
        else:
            self.panel.SetTimeOut(0.001, self.make_qrcode_img)

    def make_qrcode_img(self):
        import game3d
        import os
        file_name = str(global_data.player.uid) + '_qrcode.png'
        file_path = 'res/' + file_name
        from patch.patch_path import get_download_target_path, get_abs_download_target_path
        dir_path = get_abs_download_target_path(file_path)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        file_path = dir_path + file_name
        common.utilities.make_qrcode(global_data.player.uid, file_path)
        self.create_qrcode_pic(file_name)

    def create_qrcode_pic(self, file_name):
        import cc
        self.qrcode_sprite = cc.Sprite.create(file_name)
        if not self.qrcode_sprite:
            return
        scale = float(110) / self.qrcode_sprite.getTextureRect().width
        self.qrcode_sprite.setScale(scale)
        self.panel.nd_code.addChild(self.qrcode_sprite, 1)
        self.qrcode_sprite.setAnchorPoint(cc.Vec2(0.5, 0.5))
        sz = self.qrcode_sprite.getParent().getContentSize()
        self.qrcode_sprite.setPosition(sz.width / 2.0, sz.height / 2.0)

    def is_num(self, text):
        try:
            int(text)
            return True
        except:
            return False

    def on_appear(self):
        super(PlayerRoleInfoWidget, self).on_appear()

    def on_disappear(self):
        super(PlayerRoleInfoWidget, self).on_disappear()

    def hide(self):
        super(PlayerRoleInfoWidget, self).hide()
        bg_ui = global_data.ui_mgr.get_ui('LobbyFullScreenBgUI')
        if bg_ui:
            bg_ui.hide_dec()

    def show(self):
        super(PlayerRoleInfoWidget, self).show()
        bg_ui = global_data.ui_mgr.get_ui('LobbyFullScreenBgUI')
        if bg_ui:
            bg_ui.show_dec()