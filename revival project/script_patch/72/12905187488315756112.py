# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/message/RecruitList.py
from __future__ import absolute_import
import six
import six_ex
from common.const.property_const import U_ID, C_NAME
from logic.gutils.role_head_utils import PlayerInfoManager, set_gray, set_role_dan
from cocosui import cc
from logic.gcommon.common_utils import ui_gameplay_utils as ui_utils
import logic.gcommon.const as const
from logic.gcommon.common_const.battle_const import DEFAULT_INVITE_TID
from logic.gutils.online_state_utils import is_not_online

class RecruitList(object):

    def __init__(self, main_panel):
        self._message_data = global_data.message_data
        self.panel = global_data.uisystem.load_template_create('friend/i_friend_invite_3', parent=main_panel)
        self.player_info_manager = PlayerInfoManager()
        self._recruits = None
        self._cur_show_index = -1
        self._is_check_sview = False
        self._cur_tab_index = 0
        self.uid_to_btn_dict = {}
        self._player_simple_inf_pos_y = self.panel.nd_friends.getContentSize().height
        self.init_panel()
        global_data.emgr.team_invite_count_down_event += self.update_invite_count_down
        return

    def update_invite_count_down(self, count_down_dict):
        for uid, seconds in six.iteritems(count_down_dict):
            button = self.uid_to_btn_dict.get(uid, None)
            if button and button.isValid():
                if seconds <= 0:
                    button.SetEnable(True)
                    button.icon_team.setVisible(True)
                    button.lab_time.setVisible(False)
                    continue
                button.lab_time.SetString('{}s'.format(seconds))
                if not button.lab_time.isVisible():
                    button.SetEnable(False)
                    button.icon_team.setVisible(False)
                    button.lab_time.setVisible(True)

        return

    def init_panel(self):
        self.panel.nd_info.nd_desc.setString(get_text_by_id(10308))
        self.panel.nd_friends.nd_desc.setString(get_text_by_id(10309))
        list_friends = self.panel.nd_friends.nd_content.list_friends
        list_friends.DeleteAllSubItem()
        self._recruits = list_friends
        self.refresh_recruits()

        def scroll_callback(sender, eventType):
            if self._is_check_sview is False:
                self._is_check_sview = True
                self._recruits.SetTimeOut(0.001, self.check_sview)

        self._recruits.addEventListener(scroll_callback)
        uid = global_data.player.uid
        self.panel.nd_info.nd_content.lab_invite_code.SetStringWithChildRefresh(get_text_by_id(10314).format(uid))
        btn_copy = self.panel.nd_info.nd_content.lab_invite_code.btn_copy

        @btn_copy.callback()
        def OnClick(*args):
            import game3d
            game3d.set_clipboard_text(str(global_data.player.uid))
            global_data.game_mgr.show_tip(get_text_by_id(10053))

    def get_show_data(self):
        data = global_data.player._recruit_info
        if data:
            return six_ex.values(data)
        return []

    def refresh_recruits(self):
        show_data = self.get_show_data()
        data_count = len(show_data)
        sview_height = self._recruits.getContentSize().height
        all_height = 0
        index = 0
        while all_height < sview_height + 200:
            if data_count - index <= 0:
                break
            data = show_data[index]
            chat_pnl = self.add_list_item(data, True)
            all_height += chat_pnl.getContentSize().height
            index += 1

        self._recruits.ScrollToTop()
        self._recruits._container._refreshItemPos()
        self._recruits._refreshItemPos()
        self._cur_show_index = index - 1

    def check_sview(self):
        show_data = self.get_show_data()
        self._cur_show_index = self._recruits.AutoAddAndRemoveItem(self._cur_show_index, show_data, len(show_data), self.add_list_item, 300, 400)
        self._is_check_sview = False

    def add_list_item(self, data, is_back_item, index=-1):
        if is_back_item:
            panel = self._recruits.AddTemplateItem(bRefresh=True)
        else:
            panel = self._recruits.AddTemplateItem(0, bRefresh=True)
        self.refresh_list_item(panel, data)
        self.uid_to_btn_dict[data[U_ID]] = panel.btn_team
        return panel

    def refresh_list_item(self, panel, data):
        uid = data[U_ID]
        panel.btn_item.SetEnableCascadeOpacityRecursion(True)
        setattr(panel, 'panel_type', 'item')
        setattr(panel, 'data', data)
        name = data.get(C_NAME, '')
        panel.btn_item.lab_name.setString(name)
        self.player_info_manager.add_head_item_auto(panel.btn_item.temp_head, uid, 0, data)
        set_role_dan(panel.temp_tier, data.get('dan_info', {}))
        is_friend = self._message_data.is_friend(uid)
        self.set_online_state(panel, uid, is_friend)
        panel.btn_item.red_dot_1.setVisible(False)
        if data['recruit']:
            panel.btn_item.img_invite_me.setVisible(True)
        else:
            panel.btn_item.img_invite_me.setVisible(False)
        if not is_friend:

            @panel.btn_follow.callback()
            def OnClick(btn, touch):
                global_data.player.req_add_friend(data[U_ID])
                global_data.message_data.del_recommend_friend(data[U_ID])
                btn.setVisible(False)
                btn.SetShowEnable(True)

            panel.btn_follow.setVisible(True)
            panel.btn_follow.SetSwallowTouch(False)
        else:
            panel.btn_follow.setVisible(False)

        @panel.temp_head.callback()
        def OnClick(*args):
            pos_x, pos_y = panel.GetPosition()
            world_pos = panel.ConvertToWorldSpace(pos_x, pos_y)
            size = panel.getContentSize()
            show_pos_x = world_pos.x + size.width
            ui = global_data.ui_mgr.show_ui('PlayerSimpleInf', 'logic.comsys.message')
            ui.refresh_by_uid(int(data[U_ID]))
            ui.set_position(cc.Vec2(show_pos_x, self._player_simple_inf_pos_y))

        panel.temp_head.SetSwallowTouch(False)

    def set_online_state(self, panel, uid, is_friend):
        player = global_data.player
        state = player._recruit_info_state.get(int(uid), 0)
        text_id, color = ui_utils.get_online_inf(state)
        panel.lab_status.setString(get_text_by_id(text_id))
        panel.lab_status.SetColor(color)
        if is_not_online(state):
            set_gray(panel.btn_item.temp_head, True)
            panel.btn_team.setVisible(False)
        else:
            set_gray(panel.btn_item.temp_head, False)
            panel.btn_team.setVisible(False)
            if is_friend:
                if state == const.STATE_SINGLE:

                    @panel.btn_team.callback()
                    def OnClick(*args):
                        battle_tid = global_data.player.get_battle_tid()
                        if battle_tid is None:
                            battle_tid = DEFAULT_INVITE_TID
                        team_info = global_data.player.get_team_info() or {}
                        auto_flag = team_info.get('auto_match', global_data.player.get_self_auto_match())
                        from logic.gcommon.common_const.log_const import TEAM_MODE_FRIEND
                        global_data.player.invite_frd(uid, battle_tid, auto_flag, TEAM_MODE_FRIEND)
                        return

                    panel.btn_team.setVisible(True)
                    panel.btn_team.SetSwallowTouch(False)
        return not is_not_online(state)

    def show_panel(self):
        self.panel.setVisible(True)

    def hide_panel(self):
        self.panel.setVisible(False)

    def destroy(self):
        self.player_info_manager.destroy()
        self.player_info_manager = None
        self.uid_to_btn_dict.clear()
        return