# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/pve/rank/PVETeamBaseRankWidget.py
from __future__ import absolute_import
import time
import six_ex
import cc
from common.utils.cocos_utils import ccp
from logic.gutils import locate_utils
from logic.gutils import role_head_utils
from logic.gcommon.time_utility import get_readable_time
from logic.gutils.item_utils import get_mecha_name_by_id
from logic.gcommon.common_const.pve_rank_const import PVE_TEAM_RANK_DATA_UID_KEY, PVE_TEAM_RANK_DATA_PASS_TIME, PVE_TEAM_RANK_DATA_RANK, PVE_TEAM_RANK_DATA_MEMBERS, PVE_TEAM_RANK_MEMBER_UID, PVE_TEAM_RANK_MEMBER_MECHA_ID
from logic.comsys.battle.pve.rank.PVEBaseRankWidget import PVEBaseRankWidget

class PVETeamBaseRankWidget(PVEBaseRankWidget):
    RANK_PAGE_TYPE = None
    RANK_MINE_ITEM_BAR_BG = 'gui/ui_res_2/pve/rank/bar_pve_rank_mine_big.png'

    def __init__(self, rank_page_config, page_config=None):
        super(PVETeamBaseRankWidget, self).__init__(rank_page_config, page_config)

    def init_ui(self):
        super(PVETeamBaseRankWidget, self).init_ui()
        self._choose_pass_uid_key = None
        return

    def process_event(self, is_bind):
        if self._has_binded_event == is_bind:
            return
        emgr = global_data.emgr
        econf = {'message_on_players_detail_inf': self.on_players_detail_info_cb,
           'message_on_pve_rank_data': self.on_pve_rank_data,
           'message_on_mine_pve_rank_data': self.on_update_mine_pass_info,
           'message_pve_pass_info': self.on_pass_info_back,
           'on_change_pve_rank_page_config': self.on_choosed_config_refresh_ui
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)
        self._has_binded_event = is_bind

    def load_page_data(self):
        self.cur_rank_key = self.get_cur_rank_key()
        rank_data = self.get_cur_pve_rank_data()
        if rank_data:
            self._data_list, self._data_dict = self.filter_rank_list(rank_data)
            self._my_rank_data = self.filter_mine_first_rank(rank_data['mine_uid_keys'], self._data_dict)
            self._save_time = rank_data['save_time']
        else:
            self._data_list = []
            self._data_dict = None
            self._my_rank_data = None
            self._save_time = None
        return

    def refresh(self):
        self.choose_default_uid()
        self.list_rank.DeleteAllSubItem()
        data_count = len(self._data_list)
        sview_height = self.list_rank.getContentSize().height
        all_height = 0
        index = 0
        while all_height < sview_height + 200:
            if data_count - index <= 0:
                break
            uid_key = self._data_list[index]
            item = self.add_rank_item(uid_key, True, index)
            all_height += item.getContentSize().height
            index += 1

        self.list_rank.ScrollToTop()
        self._cur_show_index = index - 1
        self.on_show_empty_rank_list(data_count <= 0)

    def choose_default_uid(self):
        if self._choose_uid is None and self._data_list:
            default_idx = 0
            data = self.get_rank_data_by_index(default_idx)
            uid_key = data[PVE_TEAM_RANK_DATA_UID_KEY]
            members = data[PVE_TEAM_RANK_DATA_MEMBERS]
            self._choose_uid_key = uid_key
            first_uid = members[default_idx][PVE_TEAM_RANK_MEMBER_UID]
            self_in_mem = False
            for mem in members:
                uid = mem[PVE_TEAM_RANK_MEMBER_UID]
                if global_data.player.uid == uid:
                    self_in_mem = True
                    break

            self._choose_uid = global_data.player.uid if self_in_mem else first_uid
        return

    def get_rank_data_by_uid_key(self, uid_key):
        return self._data_dict.get(uid_key)

    def add_rank_item(self, uid_key, is_back_item, index=-1, bRefresh=True):
        data = self.get_rank_data_by_uid_key(uid_key)
        uid_key = data[PVE_TEAM_RANK_DATA_UID_KEY]
        rank = data[PVE_TEAM_RANK_DATA_RANK]
        if is_back_item:
            item = self.list_rank.AddTemplateItem(bRefresh=bRefresh)
        else:
            item = self.list_rank.AddTemplateItem(0, bRefresh=bRefresh)
        item._uid_key = uid_key
        self.refresh_item(item, data)
        return item

    def refresh_item(self, team_item, data, is_mine=False):
        self.refresh_item_show(team_item, data, is_mine)
        uid_key = data[PVE_TEAM_RANK_DATA_UID_KEY]
        members = data[PVE_TEAM_RANK_DATA_MEMBERS]

        @team_item.btn_choose.unique_callback()
        def OnClick(btn, touch, _data=data):
            if len(members) > 0:
                tar_uid = 0
                choose_idx = 0
                for idx, mem in enumerate(members):
                    uid = mem[PVE_TEAM_RANK_MEMBER_UID]
                    if global_data.player.uid == uid:
                        choose_idx = idx
                        break

                tar_uid = members[choose_idx][PVE_TEAM_RANK_MEMBER_UID]
                mem_item = team_item.list_team.GetItem(choose_idx)
                self.on_click_player_item(team_item, mem_item, tar_uid, _data)

        for index in range(len(members)):
            mem = members[index]
            uid = mem[PVE_TEAM_RANK_MEMBER_UID]
            mem_item = team_item.list_team.GetItem(index)
            rank_key = self.get_cur_rank_key()
            if not mem_item:
                continue

            @mem_item.btn_info.unique_callback()
            def OnClick(btn, touch, _uid_key=uid_key, _uid=uid):
                self._choose_pass_uid = _uid
                self._choose_pass_uid_key = _uid_key
                rank_key = self.get_cur_rank_key()
                self.show_player_pve_pass_ui(rank_key)

            @mem_item.unique_callback()
            def OnClick(btn, touch, _team_item=team_item, _mem_item=mem_item, _uid=uid, _data=data):
                self.on_click_player_item(_team_item, _mem_item, _uid, _data)

            if self._choose_uid_key == uid_key and self._choose_uid == uid:
                self.on_click_player_item(team_item, mem_item, uid, data)

    def refresh_item_show(self, item, data, is_mine=False):
        uid_key = data[PVE_TEAM_RANK_DATA_UID_KEY]
        pass_time = data[PVE_TEAM_RANK_DATA_PASS_TIME]
        rank = data[PVE_TEAM_RANK_DATA_RANK]
        members = data[PVE_TEAM_RANK_DATA_MEMBERS]
        self.refresh_rank(item, pass_time, rank, is_mine)
        if pass_time > 0:
            pass_time_str = get_readable_time(pass_time) if 1 else '--'
            item.lab_time.SetString(pass_time_str)

            def _check_data_all_done():
                for index in range(len(members)):
                    mem = members[index]
                    uid = mem[PVE_TEAM_RANK_MEMBER_UID]
                    player_info = self._message_data.get_pve_rank_player_detail_inf(uid)
                    if not player_info:
                        return False

                return True

            return _check_data_all_done() or None
        else:
            item.list_team.SetInitCount(len(members))
            for index in range(len(members)):
                mem = members[index]
                mem_item = item.list_team.GetItem(index)
                uid = mem[PVE_TEAM_RANK_MEMBER_UID]
                mecha_id = mem[PVE_TEAM_RANK_MEMBER_MECHA_ID]
                player_info = self._message_data.get_pve_rank_player_detail_inf(uid)
                name = player_info.get('char_name', '')
                mem_item.lab_name_player.setString(name)
                mem_item.lab_name_mecha.setString(get_mecha_name_by_id(mecha_id))
                role_head_utils.init_role_head(mem_item.temp_head, player_info.get('head_frame', None), player_info.get('head_photo', None))
                self.add_player_simple_callback(mem_item.temp_head, uid)

            return

    def refresh_my_data(self):
        empty_data = ['', -1, -1, [[global_data.player.uid, global_data.player.get_lobby_selected_mecha_id()]]]
        team_data = self._my_rank_data['team_data'] if self._my_rank_data else empty_data
        panel = self.temp_mine
        self.refresh_item_show(panel, team_data, True)
        members = team_data[PVE_TEAM_RANK_DATA_MEMBERS]
        for index in range(len(members)):
            mem_item = panel.list_team.GetItem(index)
            mem_item and mem_item.btn_info.setVisible(False)

        @panel.btn_choose.unique_callback()
        def OnClick(btn, touch, _team_data=team_data):
            now = time.time()
            if now - self._last_scroll_time < self._last_scroll_interval:
                return
            if self.is_scrolling:
                return
            uid_key = _team_data[PVE_TEAM_RANK_DATA_UID_KEY]
            self.jump_to_rank_by_uid(uid_key, global_data.player.uid, 0)

        return panel

    def jump_to_rank_by_uid(self, uid_key, tar_uid, cnt):
        if self.is_scrolling:
            return
        index = -1
        if self._data_list and uid_key in self._data_dict:
            index = self._data_list.index(uid_key)
        if index == -1:
            return
        list_node = self.list_rank
        if not list_node or not list_node.isValid():
            return
        show_uid_keys = [ item._uid_key for item in list_node.GetAllItem() ]
        if not show_uid_keys:
            return
        if uid_key in show_uid_keys:
            uid_index = show_uid_keys.index(uid_key)
            center_node = list_node.GetItem(uid_index)
            list_node.CenterWithNode(center_node)
            data = self._data_dict.get(uid_key)
            if data and center_node:
                choose_idx = 0
                members = data[PVE_TEAM_RANK_DATA_MEMBERS]
                for index in range(len(members)):
                    mem_info = members[index]
                    uid = mem_info[PVE_TEAM_RANK_MEMBER_UID]
                    if uid == tar_uid:
                        choose_idx = index
                        break

                mem_item = center_node.list_team.GetItem(choose_idx)
                self.on_click_player_item(center_node, mem_item, uid, data)
            return
        left_index = self._data_list.index(show_uid_keys[0])
        right_index = self._data_list.index(show_uid_keys[-1])
        delta = 0
        if index <= left_index:
            del_idx = abs(index - left_index)
            delta = del_idx * 100 if del_idx > 3 else 100
        elif index >= right_index:
            del_idx = abs(index - left_index)
            delta = del_idx * -100 if del_idx > 3 else -100
        from logic.gutils import mouse_scroll_utils
        from logic.gcommon.common_const import ui_operation_const as uoc
        mouse_scroll_utils.sview_scroll_by_mouse_wheel_dynamic(self, self.list_rank, delta, uoc.SST_MAIN_SETTING_DRAG_SCROLL_BAR)

        def scroll_callback():
            if self.is_scrolling == True:
                self.is_scrolling = False
                self.jump_to_rank_by_uid(uid_key, tar_uid, cnt + 1)

        self.is_scrolling = True
        self.list_rank.DelayCall(0.001, scroll_callback)

    def filter_rank_list(self, rank_data):
        is_friend = self.is_friend_rank()
        if is_friend:
            return (rank_data['friend_rank_list'], rank_data['friend_rank_dict'])
        else:
            return (
             rank_data['rank_list'], rank_data['rank_dict'])

    def filter_mine_first_rank(self, mine_uid_keys, data_dict):
        import copy
        if len(mine_uid_keys) < 1:
            return
        else:
            ldata = copy.deepcopy(data_dict[mine_uid_keys[0]])
            return {'team_data': ldata,'team_rank': ldata[0]}

    def request_players_info(self, force=False):
        if not self._template_root or not self.list_rank or not global_data.player:
            return
        now = time.time()
        if not force and now - self._request_players_time < self._request_players_interval:
            return
        count = 0
        r_uid_set = set([])
        for i, uid_key in enumerate(self._data_list):
            uids = [ int(s_uid) for s_uid in uid_key.split('_') ]
            for uid in uids:
                if not self._message_data.has_player_inf(uid):
                    r_uid_set.add(uid)
                    count += 1
                if count > self._request_players_limit:
                    break

        r_uid_list = list(r_uid_set)
        if force:
            self.list_rank.DeleteAllSubItem()
        if count > 0:
            self._request_players_time = now
            global_data.player.request_players_detail_inf(r_uid_list)
        elif force:
            self.on_players_detail_inf()

    def on_click_cur_player_item(self):
        if self._choose_data and self._choose_team_item and self._choose_mem_item:
            self.on_click_player_item(self._choose_team_item, self._choose_mem_item, self._choose_uid, self._choose_data)

    def on_click_player_item(self, team_item, mem_item, uid, data):
        if not self._template_root or not mem_item:
            return
        uid_key = data[PVE_TEAM_RANK_DATA_UID_KEY]
        rank = data[PVE_TEAM_RANK_DATA_RANK]
        data_obj = self.get_data_obj()
        info = [
         uid, data_obj, uid_key]
        global_data.emgr.on_show_pve_rank_model.emit(info)
        self.show_rewards(rank)
        self.show_title(rank)
        if self._choose_mem_item and not self._choose_mem_item.IsDestroyed() and self._choose_mem_item.vx_liuguang_orange:
            self._choose_mem_item.vx_liuguang_orange.setVisible(False)
            self._choose_mem_item.StopAnimation('loop')
            self._choose_mem_item.lab_name_player.SetColor('#SW')
        self._choose_uid = uid
        self._choose_uid_key = uid_key
        self._choose_data = data
        self._choose_mem_item = mem_item
        if self._choose_mem_item and not self._choose_mem_item.IsDestroyed() and self._choose_mem_item.lab_name_player:
            self._choose_mem_item.vx_liuguang_orange and self._choose_mem_item.vx_liuguang_orange.setVisible(True)
            self._choose_mem_item.PlayAnimation('loop')
            self._choose_mem_item.lab_name_player.SetColor('#SY')
        if self._choose_team_item and self._choose_team_item.img_choose_frame and not self._choose_team_item.IsDestroyed():
            self._choose_team_item.img_choose_frame.setVisible(False)
        self._choose_team_item = team_item
        self._choose_team_item.img_choose_frame and self._choose_team_item.img_choose_frame.setVisible(True)

    def reset_cur_choosed_info(self):
        self._choose_mem_item = None
        self._choose_team_item = None
        self._choose_data = None
        self._choose_rank_key = None
        self._choose_uid = None
        self._choose_uid_key = None
        return

    def show_player_pve_pass_ui(self, rank_key):
        uid = self._choose_pass_uid
        uid_key = self._choose_pass_uid_key
        cur_rank_key = self.get_cur_rank_key()
        data_obj = self.get_data_obj()
        if not uid or not uid_key:
            return
        else:
            if rank_key != cur_rank_key:
                return
            req_uid_list, return_dict = self._message_data.get_pve_team_rank_pass_data(data_obj, uid_key)
            pass_info = return_dict.get(uid, {})
            if not pass_info:
                print (
                 '===== no pass detail info: ', cur_rank_key, rank_key, uid_key, uid)
                return
            player_info = self._message_data.get_pve_rank_player_detail_inf(uid)
            if not player_info:
                print (
                 '===== no player detail info: ', cur_rank_key, rank_key, uid_key, uid)
                return
            data = self.get_rank_data_by_uid_key(uid_key)
            if not data:
                print (
                 '===== no rank info: ', cur_rank_key, rank_key, uid_key, uid)
                return
            self._choose_pass_uid = None
            self._choose_pass_uid_key = None
            rank = data[PVE_TEAM_RANK_DATA_RANK]
            ui = global_data.ui_mgr.show_ui('PVETeamPassDetailInfoUI', 'logic.comsys.battle.pve')
            if ui:
                ui.show_player_info(uid, self.RANK_PAGE_TYPE, rank_key, rank, pass_info, player_info)
            return