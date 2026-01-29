# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/message/FansList.py
from __future__ import absolute_import
from common.const.property_const import U_ID, C_NAME
from logic.gutils.role_head_utils import PlayerInfoManager, set_gray, set_role_dan
from cocosui import cc
import logic.gcommon.const as const
from logic.gcommon.common_utils import ui_gameplay_utils as ui_utils
from logic.gutils import role_head_utils
from logic.gutils import follow_utils
import logic.gcommon.time_utility as tutil
from logic.gcommon.cdata import dan_data
from logic.gutils import season_utils

class FansList(object):

    def __init__(self, main_panel):
        self.main_panel = main_panel
        self.panel = global_data.uisystem.load_template_create('friend/i_fans_list', parent=main_panel.nd_content)
        self.player_info_manager = PlayerInfoManager()
        self._fans = None
        self._cur_show_index = -1
        self._is_check_sview = False
        self._uid_to_panel_dict = {}
        self._fans_player_infos = global_data.player.get_fans_system_player_info(const.FANS_SYSTEM_INFO_TYPE_FANS)
        self._uid_to_name_dict = {}
        self._cur_page_index = 1
        self._last_request_time = None
        self._player_simple_inf_pos_y = self.main_panel.getContentSize().height
        self.init_panel()
        self.init_event()
        return

    def init_event(self):
        self.process_event(True)

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'on_received_fans_system_player_info': self.update_fans_player_info,
           'on_follow_result': self.on_follow_result,
           'on_undo_follow_result': self.on_undo_follow_result,
           'message_refresh_friends': self.message_refresh_friends
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def update_fans_player_info(self, info_type, page_index):
        if info_type != const.FANS_SYSTEM_INFO_TYPE_FANS:
            return
        self._cur_page_index = page_index
        old_show_data = len(self.get_show_data())
        if self._fans.GetItemCount() == 0:
            self._uid_to_panel_dict = {}
            self._uid_to_name_dict = {}
            self.refresh_fans()

    def on_follow_result(self, uid):
        panel = self._uid_to_panel_dict.get(uid)
        if panel:
            name = self._uid_to_name_dict.get(uid, None)
            if name:
                if self.panel.isVisible():
                    global_data.game_mgr.show_tip(get_text_by_id(10336).format(name))
                follow_utils.refresh_follow_status(panel, uid, name)
        return

    def on_undo_follow_result(self, uid):
        panel = self._uid_to_panel_dict.get(uid)
        name = self._uid_to_name_dict.get(uid, None)
        if panel:
            follow_utils.refresh_follow_status(panel, uid, name)
        return

    def message_refresh_friends(self):
        for index, player_info in enumerate(self._fans_player_infos):
            uid = player_info.get('uid')
            panel = self._uid_to_panel_dict.get(uid)
            if panel:
                follow_utils.refresh_friend_status(panel, uid)

    def init_panel(self):
        list_fans = self.panel.temp_list
        list_fans.DeleteAllSubItem()
        self._fans = list_fans
        self.refresh_fans()

        def scroll_callback(sender, eventType):
            if self._is_check_sview is False:
                self._is_check_sview = True
                self._fans.SetTimeOut(0.001, self.check_sview)

        self._fans.addEventListener(scroll_callback)

    def get_show_data(self):
        return self._fans_player_infos

    def check_and_hide_content(self):
        show_data = self.get_show_data()
        if not show_data:
            self.main_panel.nd_empty.lab_empty.setString(get_text_by_id(10339))
            self.main_panel.nd_empty.setVisible(True)
            self.main_panel.temp_search.setVisible(False)
            self.main_panel.nd_content.setVisible(False)
            return True
        return False

    def refresh_fans(self):
        show_data = self.get_show_data()
        if self.check_and_hide_content():
            return
        self.main_panel.nd_content.setVisible(True)
        self.main_panel.nd_empty.setVisible(False)
        self.main_panel.temp_search.setVisible(True)
        data_count = len(show_data)
        sview_height = self._fans.getContentSize().height
        all_height = 0
        index = 0
        while all_height < sview_height + 300:
            if data_count - index <= 0:
                break
            data = show_data[index]
            chat_pnl = self.add_list_item(data, True)
            all_height += chat_pnl.getContentSize().height
            index += 1

        self._fans.ScrollToTop()
        self._fans._container._refreshItemPos()
        self._fans._refreshItemPos()
        self._cur_show_index = index - 1

    def check_sview(self):
        show_data = self.get_show_data()
        self._cur_show_index = self._fans.AutoAddAndRemoveItem_MulCol(self._cur_show_index, show_data, len(show_data), self.add_list_item, 300, 400, ignore_height_check=True)
        self._is_check_sview = False
        if self._cur_show_index + 1 >= len(show_data):
            self._request_more_data()

    def _request_more_data(self):
        if self._last_request_time and tutil.get_time() - self._last_request_time < 2:
            return
        cur_show_count = len(self.get_show_data())
        request_page_index = self._cur_page_index
        if cur_show_count >= self._cur_page_index * const.FANS_SYSTEM_PLAYER_INFO_PAGE_SIZE:
            request_page_index = self._cur_page_index + 1
        global_data.player.request_fans_system_player_info(const.FANS_SYSTEM_INFO_TYPE_FANS, request_page_index)
        self._last_request_time = tutil.get_time()

    def add_list_item(self, data, is_back_item, index=-1):
        if is_back_item:
            panel = self._fans.AddTemplateItem(bRefresh=True)
        else:
            panel = self._fans.AddTemplateItem(0, bRefresh=True)
        self.refresh_list_item(panel, data)
        self._uid_to_panel_dict[data[U_ID]] = panel
        return panel

    def refresh_list_item(self, panel, data):
        uid = data[U_ID]
        setattr(panel, 'panel_type', 'item')
        setattr(panel, 'data', data)
        name = data.get(C_NAME, '')
        self._uid_to_name_dict[uid] = name
        panel.lab_name.setString(name)
        self.player_info_manager.add_head_item_auto(panel.temp_head, uid, 0, data)
        dan_info = data.get('dan_info', {})
        dan_inf = dan_info.get(dan_data.DAN_SURVIVAL, {})
        set_role_dan(panel.temp_tier, dan_info)
        panel.lab_dan_name.SetString(season_utils.get_dan_lv_name(dan_inf.get('dan', dan_data.BROZE), lv=dan_inf.get('lv', dan_data.get_lv_num(dan_data.BROZE))))
        follow_utils.refresh_fans_count(panel, uid, data.get('fans_count', 0))
        follow_utils.refresh_friend_status(panel, uid)
        online_state = data.get('st', const.STATE_OFFLINE)
        follow_utils.refresh_observe_status(panel, uid, online_state)
        follow_utils.refresh_follow_status(panel, uid, name)

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

    def show_panel(self):
        if self.check_and_hide_content():
            global_data.player.request_fans_system_player_info(const.FANS_SYSTEM_INFO_TYPE_FANS, self._cur_page_index)
            return
        self.main_panel.nd_content.setVisible(True)
        self.main_panel.nd_empty.setVisible(False)
        self.main_panel.temp_search.setVisible(True)
        self.panel.setVisible(True)

    def hide_panel(self):
        self.panel.setVisible(False)

    def destroy(self):
        self.player_info_manager.destroy()
        self.player_info_manager = None
        self._uid_to_panel_dict.clear()
        self._uid_to_name_dict.clear()
        self._fans_player_infos = []
        self._cur_page_index = 1
        self._last_request_time = None
        self.process_event(False)
        return

    def get_friend_list(self):
        return self._fans