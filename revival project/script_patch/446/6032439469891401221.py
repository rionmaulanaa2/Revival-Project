# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/clan/ClanMemberList.py
from __future__ import absolute_import
import six_ex
from functools import cmp_to_key
import cc
import logic.gcommon.const as const
from logic.gutils import clan_utils
from logic.gutils import season_utils
from logic.gcommon.common_const import clan_const
from common.const.property_const import *
from logic.comsys.clan.ClanPageBase import ClanPageBase
from logic.gutils.InfiniteScrollHelper import InfiniteScrollHelper
from logic.gcommon.common_const import spectate_const as sp_const
from logic.gutils.observe_utils import goto_spectate_player, decode_global_spectate_brief_info, is_global_spectate_data_time_valid
from logic.gcommon import time_utility as t_util
from logic.gutils.online_state_utils import is_not_online

class ClanMemberList(ClanPageBase):

    def __init__(self, dlg):
        self.global_events = {'message_on_players_detail_inf': self.on_members_detail_inf,
           'clan_member_kick': self.on_kick_member,
           'clan_member_mod_info': self.on_members_info_update,
           'on_received_global_spectate_list': self._on_received_global_spectate_list,
           'on_received_global_spectate_brief_list': self._on_received_global_spectate_brief_list
           }
        super(ClanMemberList, self).__init__(dlg)

    def on_init_panel(self):
        super(ClanMemberList, self).on_init_panel()
        self._list_sview = None
        self._member_data_list = global_data.player.get_clan_member_list()
        self._sort_status = {}
        self._cur_sort = 4
        self._is_init_list = True
        self._cached_spectate_detail_info = {}
        self._requesting_watch_uid = None
        self._requesting_watch_time = None
        self.init_widget()
        if not global_data.player.is_members_info_finished():
            self._is_init_list = False
        else:
            self.resort_member_data()
        self.panel.PlayAnimation('show')
        self.request_members_status()
        return

    def on_finalize_panel(self):
        super(ClanMemberList, self).on_finalize_panel()
        self._cached_spectate_detail_info = None
        self._requesting_watch_uid = None
        if self._list_sview:
            self._list_sview.destroy()
            self._list_sview = None
        global_data.player and global_data.player.clear_global_spectate_cached()
        return

    def refresh_panel(self):
        super(ClanMemberList, self).refresh_panel()
        self.resort_member_data()

    def request_members_data(self):
        pass

    def request_members_status(self):
        uid_list = []
        member_data_list = global_data.player.get_clan_member_list()
        for info in member_data_list:
            uid_list.append(info['uid'])

        global_data.message_data.request_players_online_state(uid_list, immediately=True)
        self._request_spectate_brief_info()

    def request_players_detail_inf(self):
        if not self._list_sview:
            return
        refresh_list = self._list_sview.get_view_list()
        uid_list = [ info[1]['uid'] for info in refresh_list ]
        global_data.player.request_players_detail_inf(uid_list)

    def on_members_online_state(self):
        if not self._list_sview:
            return
        refresh_list = self._list_sview.get_view_list()
        for info in refresh_list:
            item_widget, data = info
            self.on_refresh_item_status(item_widget, data)

    def on_members_detail_inf(self, datas):
        if not self._is_init_list:
            self._is_init_list = True
            self.resort_member_data()

    def on_members_info_update(self, *args):
        self.refresh_exsit_list()

    def on_kick_member(self, uid):
        self.resort_member_data()

    def init_widget(self):
        self.init_sorted_header()

        @self.panel.btn_exit.unique_callback()
        def OnClick(btn, touch):
            from logic.comsys.common_ui.NormalConfirmUI import SecondConfirmDlg2
            member_data_list = global_data.player.get_clan_member_list()
            if len(member_data_list) == 1:
                content = get_text_local_content(800089)
            elif clan_utils.get_my_clan_info_by_field('title') == clan_const.COMMANDER:
                content = get_text_local_content(800090)
            else:
                content = get_text_local_content(800088)
            SecondConfirmDlg2().confirm(content=content, confirm_callback=lambda : global_data.player.request_quit_clan())

    def init_member_list(self):
        import common.utilities
        if self._list_sview:
            self._list_sview.destroy()
            self._list_sview = None
        self._list_sview = InfiniteScrollHelper(self.panel.rank_list, self.panel, up_limit=500, down_limit=500)
        self._list_sview.set_template_init_callback(self.on_init_list_item)
        self._list_sview.update_data_list(self._member_data_list)
        self._list_sview.update_scroll_view()
        self._list_sview.set_require_data_callback(self.request_members_data)

        def update_slider--- This code section failed: ---

 136       0  LOAD_DEREF            0  'self'
           3  LOAD_ATTR             0  '_list_sview'
           6  LOAD_ATTR             1  'get_slider_info'
           9  CALL_FUNCTION_0       0 
          12  STORE_FAST            0  'info'

 137      15  STORE_FAST            1  'scale'
          18  BINARY_SUBSCR    
          19  STORE_FAST            1  'scale'

 138      22  LOAD_DEREF            1  'common'
          25  LOAD_ATTR             2  'utilities'
          28  LOAD_ATTR             3  'lerp'
          31  LOAD_FAST             1  'scale'
          34  LOAD_CONST            2  0.5
          37  BINARY_MULTIPLY  
          38  LOAD_CONST            3  1.0
          41  LOAD_FAST             1  'scale'
          44  LOAD_CONST            2  0.5
          47  BINARY_MULTIPLY  
          48  BINARY_SUBTRACT  
          49  BINARY_SUBTRACT  
          50  BINARY_SUBTRACT  
          51  BINARY_SUBTRACT  
          52  BINARY_SUBSCR    
          53  LOAD_CONST            5  100.0
          56  BINARY_DIVIDE    
          57  CALL_FUNCTION_3       3 
          60  LOAD_CONST            5  100.0
          63  BINARY_MULTIPLY  
          64  STORE_FAST            2  'fixed_percent'

 139      67  LOAD_DEREF            0  'self'
          70  LOAD_ATTR             4  'panel'
          73  LOAD_ATTR             5  'img_slider'
          76  LOAD_ATTR             6  'SetContentSize'
          79  LOAD_CONST            6  4
          82  LOAD_CONST            7  '{}%'
          85  LOAD_ATTR             7  'format'
          88  LOAD_FAST             1  'scale'
          91  LOAD_CONST            8  100
          94  BINARY_MULTIPLY  
          95  CALL_FUNCTION_1       1 
          98  CALL_FUNCTION_2       2 
         101  POP_TOP          

 140     102  LOAD_DEREF            0  'self'
         105  LOAD_ATTR             4  'panel'
         108  LOAD_ATTR             5  'img_slider'
         111  LOAD_ATTR             8  'SetPosition'
         114  LOAD_CONST            9  '50%'
         117  LOAD_CONST            7  '{}%'
         120  LOAD_ATTR             7  'format'
         123  LOAD_FAST             2  'fixed_percent'
         126  CALL_FUNCTION_1       1 
         129  CALL_FUNCTION_2       2 
         132  POP_TOP          

Parse error at or near `STORE_FAST' instruction at offset 15

        self._list_sview.set_scroll_callback(update_slider)
        update_slider()
        my_data = global_data.player.get_member_data(global_data.player.uid)
        if my_data:
            self.on_init_list_item(self.panel.rank_player, my_data)
        else:
            self.panel.rank_player.setVisible(False)
        return

    def refresh_exsit_list(self):
        if not self._list_sview:
            return
        refresh_list = self._list_sview.get_view_list()
        for info in refresh_list:
            item_widget, data = info
            self.on_refresh_item_info(item_widget, data)
            self.on_refresh_item_status(item_widget, data)

        my_data = global_data.player.get_member_data(global_data.player.uid)
        if my_data:
            self.on_init_list_item(self.panel.rank_player, my_data)

    def on_refresh_item_status(self, item_widget, data):
        from logic.comsys.effect import ui_effect
        from logic.gcommon.common_utils import ui_gameplay_utils as ui_utils
        cur_state = data.get(ONLINE_STATE, -1)
        cur_state = cur_state if cur_state != None else -1
        cur_state = int(cur_state)
        uid = data['uid']
        if cur_state < 0:
            return
        else:
            if is_not_online(cur_state):
                ui_effect.set_gray(item_widget.temp_head.img_head, True)
            else:
                ui_effect.set_gray(item_widget.temp_head.img_head, False)
            text, color = ui_utils.get_online_inf_by_uid(uid, state=cur_state)
            item_widget.lab_content4.setString(text)
            item_widget.lab_content4.SetColor(color)
            if cur_state != const.STATE_BATTLE_FIGHT:
                item_widget.btn_watch.setVisible(False)
            return

    def on_refresh_item_info(self, item_widget, data):
        from logic.gutils import season_utils
        from logic.gcommon.cdata import dan_data
        from logic.gutils import role_head_utils
        path = clan_utils.get_clan_title_icon(data.get('title', clan_const.MASS))
        if path:
            item_widget.icon_title.SetDisplayFrameByPath('', path)
            item_widget.icon_title.setVisible(True)
        else:
            item_widget.icon_title.setVisible(False)
        item_widget.lab_title.SetString(clan_utils.get_clan_title_text(data.get('title', clan_const.MASS)))
        dan_info = data.get('dan_info', {})
        dan_inf = dan_info.get(dan_data.DAN_SURVIVAL, {})
        role_head_utils.set_role_dan(item_widget.temp_tier, dan_info)
        item_widget.lab_content1.SetString(season_utils.get_dan_lv_name(dan_inf.get('dan', dan_data.BROZE), lv=dan_inf.get('lv', dan_data.get_lv_num(dan_data.BROZE))))
        item_widget.lab_content2.SetString('{}'.format(data.get('week_point', 0)))
        item_widget.lab_content3.SetString('{}'.format(data.get('fashion_value', 0)))

    def on_init_list_item(self, item_widget, data):
        from logic.gutils import role_head_utils
        from logic.comsys.message import PlayerSimpleInf
        role_head_utils.init_role_head(item_widget.temp_head, data.get(HEAD_FRAME, None), data.get(HEAD_PHOTO, None))
        item_widget.lab_name.SetString(data.get(C_NAME, ''))
        self.on_refresh_item_info(item_widget, data)
        self.on_refresh_item_status(item_widget, data)

        def callback(touch):
            if global_data.player.uid == data['uid']:
                return
            ui = global_data.ui_mgr.show_ui('PlayerSimpleInf', 'logic.comsys.message')
            ui.set_extra_btns([PlayerSimpleInf.BTN_TYPE_MOD_CLAN_TITLE, PlayerSimpleInf.BTN_TYPE_CLAN_KICK])
            ui.refresh_by_uid(data['uid'])
            ui.set_position(touch.getLocation(), anchor_point=cc.Vec2(0.5, 0.5))

        @item_widget.unique_callback()
        def OnClick(btn, touch):
            callback(touch)

        @item_widget.temp_head.unique_callback()
        def OnClick(btn, touch):
            callback(touch)

        @item_widget.btn_watch.unique_callback()
        def OnClick(btn, touch):
            if not global_data.player:
                return
            member_uid = data['uid']
            self._requesting_watch_uid = member_uid
            self._requesting_watch_time = t_util.get_server_time()
            spectate_info = self._cached_spectate_detail_info.get(member_uid)
            if spectate_info:
                spectate_info['spectate_type'] = sp_const.SPECTATE_LIST_CLAN
                goto_spectate_player(spectate_info)
            else:
                global_data.player.request_global_spectate_details(sp_const.SPECTATE_LIST_CLAN, [member_uid])

        return

    def set_btn_sort_flag(self, btn, up_sort):
        if up_sort:
            btn.icon_arrow.setScaleY(-1)
        else:
            btn.icon_arrow.setScaleY(1)

    def resort_member_data(self):
        from logic.gcommon.cdata import dan_data
        self._member_data_list = global_data.player.get_clan_member_list()
        index_to_field = {0: 'title',1: 'dan_info',2: 'week_point',3: 'fashion_value',4: ONLINE_STATE}
        prior_list = [
         0, 1, 2, 3, 4]
        prior_list.remove(self._cur_sort)
        prior_list.insert(0, self._cur_sort)
        status_info = self._sort_status

        def cmp_func(a, b):
            for index in prior_list:
                field = index_to_field[index]
                a_val = a.get(field, 0)
                b_val = b.get(field, 0)
                a_val = a_val if a_val != None else 0
                b_val = b_val if b_val != None else 0
                if field == 'dan_info':
                    a_inf = a.get(field, {}).get(dan_data.DAN_SURVIVAL, {})
                    b_inf = b.get(field, {}).get(dan_data.DAN_SURVIVAL, {})
                    ret = season_utils.dan_compare(a_inf.get('dan', 1), a_inf.get('lv', 1), a_inf.get('star', 0), a_inf.get('league_point', 0), b_inf.get('dan', 1), b_inf.get('lv', 1), b_inf.get('star', 0), b_inf.get('league_point', 0))
                    if ret != 0:
                        if status_info[index]['up_sort']:
                            return ret
                        return -ret
                elif field == 'title':
                    ret = six_ex.compare(a.get('title', clan_const.MASS), b.get('title', clan_const.MASS))
                    if ret != 0:
                        if status_info[index]['up_sort']:
                            return -ret
                        return ret
                elif field == ONLINE_STATE and is_not_online(int(a_val)) and is_not_online(int(b_val)):
                    a_delta = int(global_data.message_data.get_player_offline_time_delta(a.get('uid')))
                    b_delta = int(global_data.message_data.get_player_offline_time_delta(b.get('uid')))
                    ret = six_ex.compare(b_delta, a_delta)
                    if ret != 0:
                        if status_info[index]['up_sort']:
                            return ret
                        return -ret
                else:
                    a_val = int(a_val)
                    b_val = int(b_val)
                    if a_val != b_val:
                        if status_info[index]['up_sort']:
                            return six_ex.compare(a_val, b_val)
                        else:
                            return six_ex.compare(b_val, a_val)

            return six_ex.compare(0, 1)

        self._member_data_list = sorted(self._member_data_list, key=cmp_to_key(cmp_func), reverse=False)
        self.init_member_list()
        self.refresh_sorted_header()

    def refresh_sorted_header(self):
        btn_list = [
         'btn_title', 'btn_grade', 'btn_score', 'btn_fashion_score', 'btn_status']
        for i, btn_name in enumerate(btn_list):
            btn_tab = getattr(self.panel.rank_title, btn_name)
            if i == self._cur_sort:
                btn_tab.icon_arrow.setVisible(True)
                btn_tab.SetSelect(True)
            else:
                btn_tab.icon_arrow.setVisible(False)
                btn_tab.SetSelect(False)

    def init_sorted_header(self):
        btn_list = [
         'btn_title', 'btn_grade', 'btn_score', 'btn_fashion_score', 'btn_status']
        for i, btn_name in enumerate(btn_list):
            btn_tab = getattr(self.panel.rank_title, btn_name)
            btn_tab.SetTextColor(color1='#SW', color2='#SB', color3='#SW')
            status_info = {'btn': btn_tab,'index': i,'up_sort': False}
            self._sort_status[i] = status_info
            self.set_btn_sort_flag(btn_tab, status_info['up_sort'])

            @btn_tab.unique_callback()
            def OnClick(btn, touch, status_info=status_info):
                self.set_btn_sort_flag(btn, status_info['up_sort'])
                self._cur_sort = status_info['index']
                self.resort_member_data()

    def _on_received_global_spectate_brief_list(self, list_type):
        if not self._list_sview:
            return
        else:
            if list_type != sp_const.SPECTATE_LIST_CLAN:
                return
            list_info = global_data.player.get_global_specate_brief_info(sp_const.SPECTATE_LIST_CLAN)
            if not list_info:
                return
            refresh_list = self._list_sview.get_view_list()
            uid_to_btn_dict = {}
            for info in refresh_list:
                item_widget, data = info
                uid = int(data.get('uid'))
                uid_to_btn_dict[uid] = item_widget

            for brief_data in list_info:
                item_data = decode_global_spectate_brief_info(brief_data)
                if not item_data:
                    continue
                player_uid = int(item_data.get('uid', 0))
                if not player_uid:
                    continue
                item_widget = uid_to_btn_dict.get(player_uid, None)
                if not item_widget:
                    continue
                if is_global_spectate_data_time_valid(item_data):
                    item_widget.btn_watch.setVisible(True)
                else:
                    item_widget.btn_watch.setVisible(False)

            return

    def _on_received_global_spectate_list(self, list_type, list_info):
        if not global_data.player or list_type != sp_const.SPECTATE_LIST_CLAN:
            return
        else:
            if not self._list_sview:
                return
            for item_data in list_info:
                player_uid = int(item_data.get('uid', 0))
                if player_uid > 0:
                    self._cached_spectate_detail_info[player_uid] = item_data

            if self._requesting_watch_uid and self._requesting_watch_time and t_util.get_server_time() - self._requesting_watch_time <= 1:
                item_data = self._cached_spectate_detail_info.get(self._requesting_watch_uid)
                if item_data:
                    item_data['spectate_type'] = sp_const.SPECTATE_LIST_CLAN
                    goto_spectate_player(item_data)
                else:
                    global_data.game_mgr.show_tip(get_text_by_id(19459), True)
                    refresh_list = self._list_sview.get_view_list()
                    for info in refresh_list:
                        item_widget, data = info
                        uid = data.get('uid')
                        if uid == self._requesting_watch_uid:
                            item_widget.btn_watch.setVisible(False)
                            break

            self._requesting_watch_uid = None
            self._requesting_watch_time = None
            return

    def _request_spectate_brief_info(self):
        if not global_data.player:
            return
        members_online_state = global_data.message_data.get_player_online_state()
        member_data_list = global_data.player.get_clan_member_list()
        if not members_online_state or not member_data_list:
            return
        request_spectate_brief_uids = []
        for info in member_data_list:
            uid = int(info.get('uid', 0))
            state = int(members_online_state.get(uid, 0))
            if state != const.STATE_BATTLE_FIGHT:
                continue
            request_spectate_brief_uids.append(uid)

        if request_spectate_brief_uids:
            global_data.player and global_data.player.request_global_spectate_brief_list(sp_const.SPECTATE_LIST_CLAN, request_spectate_brief_uids)