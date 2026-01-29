# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/room/RoomListUI.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
from common.const.uiconst import NORMAL_LAYER_ZORDER_2, UI_VKB_CLOSE
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.comsys.common_ui.WindowMediumBase import WindowMediumBase
ROOM_NUM_PER_PAGE = 10

class RoomListUI(WindowMediumBase):
    PANEL_CONFIG_NAME = 'room/room_list'
    DLG_ZORDER = NORMAL_LAYER_ZORDER_2
    TEMPLATE_NODE_NAME = 'pnl_window'
    UI_VKB_TYPE = UI_VKB_CLOSE
    UI_ACTION_EVENT = {'btn_refresh.OnClick': 'req_refresh_room_list',
       'btn_create.btn_major.OnClick': 'on_click_room_create',
       'btn_search.OnClick': 'on_click_search_btn',
       'btn_clean.OnClick': 'on_click_search_cancel_btn'
       }
    REFRESH_CD = 3

    def on_init_panel(self):
        super(RoomListUI, self).on_init_panel()
        import render
        global_data.display_agent.set_post_effect_active('gaussian_blur', True)
        self.room_list = []
        self.init_parameters()
        self.init_search_vars()
        self.init_infinite_scroll()
        self.init_event()
        self.init_widget()

    def init_parameters(self):
        self.is_can_refresh_room_list = True
        self.panel.lv_list.SetInitCount(0)

    def req_refresh_room_list(self, *args):
        if not self.is_can_refresh_room_list:
            return
        global_data.player.req_room_list()
        self.panel.img_cd.setVisible(True)
        self.panel.lab_cd.setVisible(True)
        self.panel.lab_cd.SetString(str(RoomListUI.REFRESH_CD))
        self.is_can_refresh_room_list = False

        def refresh_tick(passd_time):
            self.panel.lab_cd.SetString(str(int(RoomListUI.REFRESH_CD - passd_time)))

        def cb():
            self.panel.img_cd.setVisible(False)
            self.panel.lab_cd.setVisible(False)
            self.is_can_refresh_room_list = True

        self.panel.lab_cd.TimerAction(refresh_tick, RoomListUI.REFRESH_CD, callback=cb, interval=1.0)

    def init_event(self):
        self.panel.lv_list.setVisible(False)
        self.panel.lab_no_room.setVisible(True)
        self._room_sview.DeleteAllSubItem()
        global_data.player.req_room_list()

    def refresh_room_list(self, page, room_list):
        if page == 0:
            self.room_list = room_list
            self._room_sview.DeleteAllSubItem()
            self._sview_index = -1
            self.update_scroll_view()
            self.cur_max_page = 0
        else:
            self.room_list.extend(room_list)
        if len(room_list) != 0:
            self.cur_max_page = page

    def refresh_room_list_show(self, show_room_list):
        if len(show_room_list) <= 0:
            self.panel.lv_list.setVisible(False)
            self.panel.lab_no_room.setVisible(True)
            return
        self.panel.lv_list.setVisible(True)
        self.panel.lab_no_room.setVisible(False)
        data_count = len(show_room_list)
        index = 0
        while index < ROOM_NUM_PER_PAGE and index < data_count:
            data = show_room_list[index]
            panel = self.add_room_elem(data)
            index += 1

        return index - 1

    def get_team_mode_info(self, max_team_size):
        if max_team_size == 1:
            bg_pic = 'gui/ui_res_2/create_room/mode_1.png'
            text = get_text_by_id(19310)
        elif max_team_size == 2:
            bg_pic = 'gui/ui_res_2/create_room/mode_2.png'
            text = get_text_by_id(19311)
        else:
            bg_pic = 'gui/ui_res_2/create_room/mode_4.png'
            text = get_text_by_id(19312)
        return (bg_pic, text)

    def init_room_ui_item(self, ui_item, room_data):
        room_id = room_data.get('room_id', None)
        is_battle = room_data.get('is_battle', True)
        room_name = room_data.get('name', '')
        need_pwd = room_data.get('need_pwd', False)
        cur_player_cnt = int(room_data.get('cur_player_cnt', 0))
        max_player_cnt = int(room_data.get('max_player_cnt', 0))
        creator_name = room_data.get('creator_name', '')
        max_team_size = room_data.get('max_team_size', 1)
        battle_type = room_data.get('battle_type', None)
        bg_pic, mode_text = self.get_team_mode_info(max_team_size)
        ui_item.lab_mode.SetString(mode_text)
        ui_item.lab_leader_name.SetString(creator_name)
        ui_item.lab_player_no.SetString(get_text_by_id(19313, (cur_player_cnt, max_player_cnt)))
        if is_battle:
            ui_item.lab_room_status.SetString(get_text_by_id(19314))
        else:
            ui_item.lab_room_status.SetString(get_text_by_id(19315))
        ui_item.img_mode.SetDisplayFrameByPath('', bg_pic)
        ui_item.lab_room_no.SetString(str(room_id))
        ui_item.lab_room_name.SetString(str(room_name))
        ui_item.img_lock.setVisible(need_pwd)

        @ui_item.btn_join.btn_common.unique_callback()
        def OnClick(btn, *args):
            if battle_type is None:
                global_data.game_mgr.show_tip(get_text_by_id(19331))
                return
            else:
                if is_battle:
                    global_data.game_mgr.show_tip(get_text_by_id(19324))
                    return

                def request(password=''):
                    global_data.player.req_enter_room(room_id, battle_type, password)

                if need_pwd:
                    from logic.comsys.common_ui.NormalInputUI import NormalInputUI
                    NormalInputUI(None, confirm_cb=request, need_pwd=True, place_holder=get_text_by_id(19316))
                else:
                    request()
                return

        return

    def on_finalize_panel(self):
        if self._input_box:
            self._input_box.destroy()
            self._input_box = None
        import render
        return

    def init_widget(self):
        self.init_search_widget()
        self.panel.pnl_window.SetEnableTouch(False)

    def init_search_widget(self):
        import logic.comsys.common_ui.InputBox as InputBox
        self._input_box = InputBox.InputBox(self.panel.input_search)
        self._input_box.set_rise_widget(self.panel)
        self.panel.btn_clean.setVisible(False)

    def on_click_room_create(self, *args):
        self.panel.btn_create.PlayAnimation('click')
        from logic.comsys.room.RoomCreateUI import RoomCreateUI
        RoomCreateUI(self.panel)

    def on_click_search_btn(self, *args):
        room_no = self._input_box.get_text()
        if room_no == '':
            global_data.game_mgr.show_tip(get_text_by_id(19317))
        else:
            self.panel.btn_clean.setVisible(True)
            self.is_in_search_show = True
            res_room_list = self.find_room_id_in_room_list(room_no)
            self.search_room_list = res_room_list
            self._search_sview_index = -1
            self.switch_show_mode(is_search=True)

    def on_click_search_cancel_btn(self, *args):
        if self.is_in_search_show:
            self.panel.btn_clean.setVisible(False)
            self.is_in_search_show = False
            self._input_box.set_text('')
            self.search_room_list = []
            self._search_sview_index = -1
            self._sview_index = -1
            self.switch_show_mode(is_search=False)

    def find_room_id_in_room_list(self, room_id_str):
        room_search_res = []
        for room_data in self.room_list:
            cur_room_id = room_data.get('room_id', None)
            cur_room_id_str = str(cur_room_id)
            res = cur_room_id_str.find(room_id_str)
            if res != -1:
                room_search_res.append(room_data)

        return room_search_res

    def init_infinite_scroll(self):
        self._room_sview = self.panel.lv_list
        self._sview_index = -1
        self.cur_max_page = 0
        self._is_check_sview = False

        @self._room_sview.unique_callback()
        def OnScrolling(sender):
            if self._is_check_sview == False:
                self._is_check_sview = True
                self.SetTimeOut(0.2, self.update_scroll_view)

        @self._room_sview.unique_callback()
        def OnScrollBounceBottom(sv):
            if not self.is_in_search_show:
                msg_count = len(self.room_list)
                if self._sview_index == msg_count - 1:
                    global_data.player.req_room_list(self.cur_max_page + 1)

    def update_scroll_view(self):
        if not self.is_in_search_show:
            self._sview_index = self.check_sview(self.room_list, self._sview_index)
        else:
            self._search_sview_index = self.check_sview(self.search_room_list, self._search_sview_index)
        self._is_check_sview = False

    def check_sview(self, data_list, view_index):
        if view_index < 0:
            return self.refresh_room_list_show(data_list)
        msg_count = len(data_list)
        new_view_index = self._room_sview.AutoAddAndRemoveItem_MulCol(view_index, data_list, msg_count, self.add_room_elem, 700, 700)
        return new_view_index

    def add_room_elem(self, data, is_back_item=True, index=-1):
        if is_back_item:
            panel = self._room_sview.AddTemplateItem(bRefresh=True)
        else:
            panel = self._room_sview.AddTemplateItem(0, bRefresh=True)
        self.init_room_ui_item(panel, data)
        return panel

    def init_search_vars(self):
        self.search_room_list = []
        self._search_sview_index = -1
        self.is_in_search_show = False

    def switch_show_mode(self, is_search):
        self._room_sview.DeleteAllSubItem()
        if not is_search:
            self._sview_index = self.check_sview(self.room_list, self._sview_index)
        else:
            self._search_sview_index = self.check_sview(self.search_room_list, self._search_sview_index)