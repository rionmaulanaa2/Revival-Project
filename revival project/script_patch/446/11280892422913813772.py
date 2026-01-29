# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/room/RoomListUINew.py
from __future__ import absolute_import
import six_ex
from common.const.uiconst import NORMAL_LAYER_ZORDER_2, UI_VKB_CLOSE
from logic.gcommon.common_utils.local_text import get_text_by_id
import logic.comsys.common_ui.InputBox as InputBox
from logic.comsys.room.RoomPasswordUI import RoomPasswordUI
from logic.gutils import role_head_utils
from logic.comsys.common_ui.WindowMediumBase import WindowMediumBase
from common.cfg import confmgr
import time
from logic.gutils.template_utils import update_badge_node
from logic.gcommon.const import ROOM_CREATE_MIN_PLAYER_LEVEL
from logic.comsys.room.RoomCreateUINew import RoomCreateUINew
from logic.gcommon import const
from logic.gcommon.common_const import spectate_const
from logic.gutils.observe_utils import goto_spectate_player, decode_global_spectate_brief_info, is_global_spectate_data_time_valid
from logic.gcommon import time_utility as t_util
from logic.gcommon.common_const import battle_const
from logic.gutils.custom_room_utils import RANDOM_MAP_TEXT_ID
from logic.gcommon.common_utils.battle_utils import get_mode_name
ROOM_MODE_BG_PIC = {90001: 'gui/ui_res_2/main/btn_mode_choose_tdm.png',
   90002: 'gui/ui_res_2/main/btn_mode_choose_suger.png',
   90003: 'gui/ui_res_2/main/btn_mode_choose_suger.png',
   90004: 'gui/ui_res_2/main/btn_mode_choose_gvg.png',
   90005: 'gui/ui_res_2/main/btn_mode_choose_suger.png',
   90006: 'gui/ui_res_2/main/btn_mode_choose_suger.png',
   90007: 'gui/ui_res_2/main/btn_mode_choose_tdm.png'
   }

class RoomListUINew(WindowMediumBase):
    PANEL_CONFIG_NAME = 'room/room_list_new'
    DLG_ZORDER = NORMAL_LAYER_ZORDER_2
    TEMPLATE_NODE_NAME = 'pnl_window'
    UI_VKB_TYPE = UI_VKB_CLOSE
    RECREATE_WHEN_RESOLUTION_CHANGE = True
    UI_ACTION_EVENT = {'btn_refresh.btn_major.OnClick': 'on_click_refresh_btn',
       'btn_create.btn_major.OnClick': 'on_click_create_room_btn',
       'btn_search.OnClick': 'on_click_search_btn',
       'btn_clean.OnClick': 'on_click_search_cancel_btn',
       'btn_tips.OnClick': 'on_click_tips_btn',
       'nd_bg.OnClick': 'on_click_nd_bg'
       }
    REFRESH_CD = 3
    ROOM_NUM_PER_PAGE = 10
    SEARCH_CD = 5

    def on_init_panel(self, *args, **kwargs):
        super(RoomListUINew, self).on_init_panel()
        self._cur_show_nd_report = None
        self.init_widget()
        self.init_event()
        self.room_list = []
        self.search_room_list = []
        self._search_sview_index = -1
        self.is_in_search_show = False
        self._can_refresh_room_list = True
        self.panel.DelayCall(0.3, self.requset_room_list)
        self._refresh_timestamp = None
        self._search_timestamp = 0
        self._uid2roomitem = {}
        self._requested_spectate_brief_info = False
        self._request_spectate_uid = None
        self._request_spectate_time = None
        return

    def requset_room_list(self):
        global_data.player.req_room_list()

    def on_finalize_panel(self):
        self._cur_show_nd_report = None
        if self._input_box:
            self._input_box.destroy()
            self._input_box = None
        global_data.emgr.on_received_global_spectate_brief_list -= self.on_received_global_spectate_brief_list
        global_data.emgr.on_received_global_spectate_list -= self.on_received_global_spectate_list
        return

    def init_widget(self):
        self.panel.lab_empty.setVisible(True)
        self.panel.list_room.setVisible(False)
        self.panel.list_room.DeleteAllSubItem()
        self.panel.list_room.SetInitCount(0)
        self.init_infinite_scroll()
        self._input_box = InputBox.InputBox(self.panel.input_search)
        self._input_box.set_rise_widget(self.panel)
        self.panel.btn_clean.setVisible(False)
        self.panel.pnl_window.SetEnableTouch(False)

    def init_event(self):
        global_data.emgr.on_received_global_spectate_brief_list += self.on_received_global_spectate_brief_list
        global_data.emgr.on_received_global_spectate_list += self.on_received_global_spectate_list

    def on_click_create_room_btn(self, *args):
        self.panel.btn_create.PlayAnimation('click')
        if global_data.player.get_lv() < ROOM_CREATE_MIN_PLAYER_LEVEL:
            global_data.game_mgr.show_tip(get_text_by_id(608165))
            return
        RoomCreateUINew(self.panel)

    def on_click_refresh_btn(self, *args):
        now = time.time()
        if self._refresh_timestamp is None:
            self._refresh_timestamp = now
            global_data.player.req_room_list()
        else:
            if now - self._refresh_timestamp < RoomListUINew.REFRESH_CD:
                global_data.game_mgr.show_tip(get_text_by_id(15815))
                return
            self._refresh_timestamp = now
            global_data.player.req_room_list()
        return

    def on_click_search_btn(self, *args):
        now = time.time()
        if now - self._search_timestamp < RoomListUINew.SEARCH_CD:
            global_data.game_mgr.show_tip(get_text_by_id(15815))
            return
        self._search_timestamp = now
        search_str = self._input_box.get_text()
        if search_str == '':
            global_data.game_mgr.show_tip(get_text_by_id(19317))
        else:
            global_data.player.req_search_room_list(search_str)
        self._input_box.set_text('')

    def on_search_room_list(self, room_list):
        self.panel.btn_clean.setVisible(True)
        self.is_in_search_show = True
        self.search_room_list = room_list
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

    def on_click_tips_btn(self, *args):
        from logic.comsys.common_ui.GameRuleDescUI import GameRuleDescUI
        dlg = GameRuleDescUI()
        dlg.set_show_rule(get_text_local_content(608157), get_text_local_content(608158))

    def find_room_id_in_room_list(self, room_id_str):
        room_search_res = []
        for room_data in self.room_list:
            cur_room_id = room_data.get('room_id', None)
            cur_room_id_str = str(cur_room_id)
            res = cur_room_id_str.find(room_id_str)
            if res != -1:
                room_search_res.append(room_data)

        return room_search_res

    def find_room_name_in_room_list(self, room_name_str):
        room_search_res = []
        for room_data in self.room_list:
            curr_room_name = str(room_data.get('name'))
            res = curr_room_name.find(room_name_str)
            if res != -1:
                room_search_res.append(room_data)

        return room_search_res

    def combine_room_list(self, room_list1, room_list2):
        combine_res = room_list1 + room_list2
        return [ dict(t_room_item) for t_room_item in set([ tuple(six_ex.items(room_item)) for room_item in combine_res ]) ]

    def switch_show_mode(self, is_search):
        self._room_sview.DeleteAllSubItem()
        if not is_search:
            self._sview_index = self.check_sview(self.room_list, self._sview_index)
        else:
            self._search_sview_index = self.check_sview(self.search_room_list, self._search_sview_index)

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

    def refresh_room_list_show(self, room_list):
        if len(room_list) <= 0:
            self.panel.list_room.setVisible(False)
            self.panel.lab_empty.setVisible(True)
            return
        self.panel.list_room.setVisible(True)
        self.panel.lab_empty.setVisible(False)
        index = 0
        room_num = len(room_list)
        while index < RoomListUINew.ROOM_NUM_PER_PAGE and index < room_num:
            curr_room = room_list[index]
            panel = self.add_room(curr_room)
            index += 1

        return index - 1

    def add_room(self, room_data, is_back_item=True, index=-1):
        if room_data is None:
            return
        else:
            if is_back_item:
                panel = self.panel.list_room.AddTemplateItem(bRefresh=True)
            else:
                panel = self.panel.list_room.AddTemplateItem(0, bRefresh=True)
            self.populate_room_ui_item(panel, room_data)
            creator_uid = room_data.get('creator', -1)
            self._uid2roomitem[creator_uid] = {'panel': panel,
               'is_battle': room_data.get('is_battle', True),
               'room_type': room_data.get('room_type', const.ROOM_TYPE_ORDINARY)
               }
            return panel

    def populate_room_ui_item(self, room_ui_item, room_data):
        if room_data is None:
            return
        else:
            room_id = room_data.get('room_id', None)
            is_battle = room_data.get('is_battle', True)
            is_week_compeition = room_data.get('is_week_competition', False)
            room_name = room_data.get('name', '')
            need_pwd = room_data.get('need_pwd', False)
            cur_player_cnt = int(room_data.get('cur_player_cnt', 0))
            max_player_cnt = int(room_data.get('max_player_cnt', 0))
            creator_name = room_data.get('creator_name', '')
            room_type = room_data.get('room_type', const.ROOM_TYPE_ORDINARY)
            room_mb = room_data.get('bin_mb')
            clan_name = room_data.get('clan_name', '')
            clan_lv = room_data.get('clan_lv', '')
            clan_badge = room_data.get('clan_badge', 0)
            if clan_badge == '':
                clan_badge = 0
            max_team_size = room_data.get('max_team_size', 1)
            team_size_bg_pic = self.get_team_size_info(max_team_size)
            battle_type = room_data.get('battle_type', None)
            mode_bg_pic = self.get_mode_bg_pic(battle_type)
            dan_info = room_data.get('dan_info', {})
            mode_name = get_mode_name(battle_type)
            born_idx = room_data.get('born_idx', -1)
            map_name = self.get_born_area_name(battle_type, born_idx)
            if map_name != '':
                room_ui_item.lab_mode.SetString(mode_name + '-' + map_name)
            else:
                room_ui_item.lab_mode.SetString(mode_name)
            room_ui_item.icon_rank.setVisible(is_week_compeition)
            if is_week_compeition:
                creator_name = get_text_by_id(860038)
                from logic.gcommon.cdata import dan_data
                dan_info = {'dan': dan_data.ALPHA,'lv': 1}
                from common.platform.dctool import interface
                if is_battle:
                    room_ui_item.btn_spectate.setVisible(True)
                    room_ui_item.btn_join.setVisible(False)
                else:
                    room_ui_item.btn_spectate.setVisible(False)
                    room_ui_item.btn_join.setVisible(True)
                global_data.player and global_data.player.request_global_spectate_brief_list(spectate_const.SPECTATE_LIST_COMPETITION)
            room_ui_item.lab_owner_name.SetString(creator_name)
            room_ui_item.lab_player_num.SetString(get_text_by_id(19313, (cur_player_cnt, max_player_cnt)))
            if is_battle:
                room_ui_item.lab_room_status.SetString(get_text_by_id(19314))
                room_ui_item.lab_room_status.SetColor('#BY')
            else:
                room_ui_item.lab_room_status.SetString(get_text_by_id(19315))
                room_ui_item.lab_room_status.SetColor('#BG')
            if team_size_bg_pic:
                room_ui_item.img_mode.SetDisplayFrameByPath('', team_size_bg_pic)
                room_ui_item.img_mode.setVisible(True)
            else:
                room_ui_item.img_mode.setVisible(False)
            room_ui_item.img_mode_bar.SetDisplayFrameByPath('', mode_bg_pic)
            room_ui_item.img_mode_bar.setVisible(True)
            room_ui_item.lab_room_num.SetString(get_text_by_id(862019).format(str(room_id)))
            room_ui_item.lab_name.SetString(str(room_name))
            room_ui_item.img_lock.setVisible(need_pwd)
            room_ui_item.img_inner.setVisible(global_data.player.get_room_type(battle_type) == 1)
            room_ui_item.img_room_bar_match.setVisible(False)
            room_ui_item.img_room_bar.setVisible(True)
            room_ui_item.img_match.setVisible(False)
            role_head_utils.init_role_head_auto(room_ui_item.temp_head, room_data.get('creator'), 0, None, head_frame=room_data.get('head_frame'), head_photo=room_data.get('head_photo'))
            if clan_name == '':
                room_ui_item.lab_crew.setVisible(False)
                room_ui_item.nd_crew.setVisible(False)
            else:
                room_ui_item.nd_crew.setVisible(True)
                room_ui_item.lab_crew.setVisible(True)
                room_ui_item.lab_crew.SetString(str(clan_name))
                room_ui_item.lab_crew_level.SetString(str(clan_lv))
                update_badge_node(int(clan_badge), room_ui_item.temp_crew_logo)
            role_head_utils.set_role_dan(room_ui_item.temp_tier, dan_info)
            room_ui_item.lab_name.SetColor(4138618)
            room_ui_item.lab_room_num.SetColor(4138618)
            room_ui_item.lab_owner_name.SetColor(4138618)
            room_ui_item.lab_crew.SetColor(4138618)
            room_ui_item.lab_player_num.SetColor(4138618)

            @room_ui_item.btn_join.btn_common.unique_callback()
            def OnClick(btn, *args):
                if battle_type is None:
                    global_data.game_mgr.show_tip(get_text_by_id(19331))
                    return
                else:
                    if is_battle:
                        global_data.game_mgr.show_tip(get_text_by_id(19324))
                        return

                    def request_pwd(password=''):
                        global_data.player.req_enter_room(room_id, battle_type, password)

                    if need_pwd:
                        RoomPasswordUI(None, confirm_cb=request_pwd, need_pwd=True, place_holder=get_text_by_id(19316))
                    else:
                        request_pwd()
                    return

            @room_ui_item.btn_spectate.btn_common.unique_callback()
            def OnClick(btn, *args):
                can_spectate = False
                list_info = global_data.player.get_global_specate_brief_info(spectate_const.SPECTATE_LIST_COMPETITION)
                if not list_info:
                    global_data.game_mgr.show_tip(get_text_by_id(19250))
                    global_data.player and global_data.player.request_global_spectate_brief_list(spectate_const.SPECTATE_LIST_COMPETITION)
                    return
                for brief_data in list_info:
                    item_data = decode_global_spectate_brief_info(brief_data)
                    if not item_data:
                        continue
                    can_spectate = is_global_spectate_data_time_valid(item_data)
                    if can_spectate:
                        from logic.comsys.live.LiveMainUI import LiveMainUI
                        LiveMainUI()
                        return

                global_data.game_mgr.show_tip(get_text_by_id(19250))
                global_data.player and global_data.player.request_global_spectate_brief_list(spectate_const.SPECTATE_LIST_COMPETITION)

            @room_ui_item.btn_report_entre.unique_callback()
            def OnClick(btn, touch, ui_item=room_ui_item):
                self.on_click_btn_entry(ui_item)

            @room_ui_item.temp_report.btn_report.unique_callback()
            def OnClick(btn, touch, data=room_data):
                self.on_click_btn_report(data)

            return

    def get_team_size_info(self, max_team_size):
        if max_team_size == 1:
            bg_pic = 'gui/ui_res_2/create_room/mode_1.png'
        elif max_team_size == 2:
            bg_pic = 'gui/ui_res_2/create_room/mode_2.png'
        elif max_team_size == 3:
            bg_pic = 'gui/ui_res_2/create_room/mode_4.png'
        else:
            bg_pic = None
        bg_pic = None
        return bg_pic

    def get_mode_bg_pic(self, battle_type):
        return ROOM_MODE_BG_PIC.get(int(battle_type), 'gui/ui_res_2/main/btn_mode_choose_tdm.png')

    def get_born_area_name(self, battle_type, born_idx):
        if battle_type is None:
            return ''
        else:
            battle_config = confmgr.get('battle_config')
            battle_info = battle_config.get(str(battle_type))
            if battle_info is None:
                return ''
            map_id = battle_info.get('iMapID', -1)
            if map_id == -1:
                return ''
            map_config = confmgr.get('map_config')
            map_info = map_config.get(str(map_id))
            if map_info is None:
                return ''
            born_list = map_info.get('bornList')
            if not born_list:
                return ''
            if born_idx == -1:
                return get_text_by_id(RANDOM_MAP_TEXT_ID)
            born_idx = born_idx if 0 <= born_idx <= len(born_list) - 1 else None
            if born_idx is None:
                return ''
            return get_text_by_id(born_list[born_idx])

    def get_needed_level(self, battle_type):
        if battle_type is None:
            return ''
        else:
            battle_config = confmgr.get('battle_config')
            battle_info = battle_config.get(str(battle_type))
            if battle_info is None:
                return ''
            needed_level = battle_info.get('iMinPlayerLevel', 0)
            return int(needed_level)

    def init_infinite_scroll(self):
        self._room_sview = self.panel.list_room
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
        if view_index is None or view_index < 0:
            return self.refresh_room_list_show(data_list)
        else:
            msg_count = len(data_list)
            new_view_index = self._room_sview.AutoAddAndRemoveItem_MulCol(view_index, data_list, msg_count, self.add_room, 700, 700)
            return new_view_index

    def on_received_global_spectate_brief_list(self, list_type):
        if list_type != spectate_const.SPECTATE_LIST_COMPETITION:
            return
        else:
            list_info = global_data.player.get_global_specate_brief_info(spectate_const.SPECTATE_LIST_COMPETITION)
            if list_info is None:
                return
            for brief_data in list_info:
                item_data = decode_global_spectate_brief_info(brief_data)
                if not item_data:
                    continue
                player_uid = int(item_data.get('uid', 0))
                if not player_uid:
                    continue
                room_item = self._uid2roomitem.get(player_uid, {})
                panel = room_item.get('panel', None)
                if panel and panel.isValid():
                    can_spectate = is_global_spectate_data_time_valid(item_data)
                    if item_data.get('competition_region', None):
                        can_spectate = False
                    panel.btn_spectate.setVisible(can_spectate)
                    panel.btn_join.setVisible(not can_spectate)

            return

    def on_room_spectate_obj(self, room_id, spectate_obj):
        self._request_spectate_uid = spectate_obj
        global_data.player.request_global_spectate_details(spectate_const.SPECTATE_LIST_COMPETITION, [spectate_obj])

    def on_received_global_spectate_list(self, list_type, list_info):
        if not global_data.player or list_type != spectate_const.SPECTATE_LIST_COMPETITION:
            return
        else:
            self._request_spectate_uid = None
            self._request_spectate_time = None
            return

    def on_click_btn_entry(self, room_ui_item):
        is_showing = room_ui_item.temp_report.isVisible()
        room_ui_item.temp_report.setVisible(not is_showing)
        self.panel.nd_bg.setVisible(not is_showing)
        self._cur_show_nd_report = room_ui_item.temp_report

    def on_click_btn_report(self, room_data):
        from logic.gutils import jump_to_ui_utils
        room_info = {'room_id': room_data.get('room_id'),
           'name': room_data.get('name', ''),
           'creator': room_data.get('creator', -1)
           }
        jump_to_ui_utils.jump_to_room_report(room_info)

    def on_click_nd_bg(self, *args):
        if self._cur_show_nd_report and self._cur_show_nd_report.isValid():
            self._cur_show_nd_report.setVisible(False)
            self.panel.nd_bg.setVisible(False)