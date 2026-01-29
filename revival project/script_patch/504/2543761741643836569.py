# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/pve/rank/PVESingleBaseRankWidget.py
from __future__ import absolute_import
import time
import six_ex
from common.utils.cocos_utils import ccp
from logic.gutils import locate_utils
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gutils import role_head_utils
from logic.gcommon.time_utility import get_readable_time
from logic.gutils.item_utils import get_mecha_name_by_id
from logic.gcommon.common_const.pve_rank_const import PVE_RANK_DATA_UID, PVE_RANK_DATA_PASS_TIME, PVE_RANK_DATA_RANK, PVE_RANK_DATA_MECHA_ID
from logic.comsys.battle.pve.rank.PVEBaseRankWidget import PVEBaseRankWidget

class PVESingleBaseRankWidget(PVEBaseRankWidget):
    RANK_PAGE_TYPE = None

    def __init__(self, rank_page_config, page_config=None):
        super(PVESingleBaseRankWidget, self).__init__(rank_page_config, page_config)

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
            self._my_rank_data = {'player_data': rank_data['player_data'],'player_rank': rank_data['player_rank']}
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
            uid = self._data_list[index]
            item = self.add_rank_item(uid, True, index)
            all_height += item.getContentSize().height
            index += 1

        self.list_rank.ScrollToTop()
        self._cur_show_index = index - 1
        self.on_show_empty_rank_list(data_count <= 0)

    def choose_default_uid(self):
        if self._choose_uid is None and self._data_list:
            data = self.get_rank_data_by_index(0)
            self._choose_uid = data[PVE_RANK_DATA_UID]
        return

    def get_rank_data_by_uid(self, uid):
        return self._data_dict.get(uid)

    def add_rank_item(self, uid, is_back_item, index=-1, bRefresh=True):
        data = self.get_rank_data_by_uid(uid)
        uid = data[PVE_RANK_DATA_UID]
        pass_time = data[PVE_RANK_DATA_PASS_TIME]
        rank = data[PVE_RANK_DATA_RANK]
        mecha_id = data[PVE_RANK_DATA_MECHA_ID]
        if is_back_item:
            item = self.list_rank.AddTemplateItem(bRefresh=bRefresh)
        else:
            item = self.list_rank.AddTemplateItem(0, bRefresh=bRefresh)
        item._uid = uid
        if self._choose_uid == uid:
            self.on_click_player_item(item, uid, data)
            self._choose_item.img_choose_frame.setVisible(True)
        else:
            item.img_choose_frame.setVisible(False)
        self.refresh_item(item, data)
        return item

    def refresh_item(self, item, data, is_mine=False):
        self.refresh_item_show(item, data, is_mine)
        uid = data[PVE_RANK_DATA_UID]

        @item.btn_info.unique_callback()
        def OnClick(btn, touch, _uid=uid):
            self._choose_pass_uid = _uid
            rank_key = self.get_cur_rank_key()
            self.show_player_pve_pass_ui(rank_key)

        @item.btn_choose.unique_callback()
        def OnClick(btn, touch, _data=data):
            self.on_click_player_item(item, uid, _data)

        if self._choose_uid == uid:
            self.on_click_player_item(item, uid, data)

    def refresh_item_show(self, item, data, is_mine=False):
        uid = data[PVE_RANK_DATA_UID]
        pass_time = data[PVE_RANK_DATA_PASS_TIME]
        rank = data[PVE_RANK_DATA_RANK]
        mecha_id = data[PVE_RANK_DATA_MECHA_ID]
        mecha_id = mecha_id if mecha_id != 0 else self.get_choosed_mecha_id()
        self.refresh_rank(item, pass_time, rank, is_mine)
        if pass_time > 0:
            pass_time_str = get_readable_time(pass_time) if 1 else '--'
            item.lab_time.SetString(pass_time_str)
            player_info = self._message_data.get_pve_rank_player_detail_inf(uid)
            return player_info or None
        else:
            name = player_info.get('char_name', '')
            item.lab_name_player.setString(name)
            item.lab_name_mecha.setString(get_mecha_name_by_id(mecha_id))
            role_head_utils.init_role_head(item.temp_head, player_info.get('head_frame', None), player_info.get('head_photo', None))
            self.add_player_simple_callback(item.temp_head, uid)
            return

    def refresh_my_data(self):
        if self._my_rank_data is None:
            return
        else:
            data = self._my_rank_data['player_data']
            panel = self.temp_mine
            panel.btn_info.setVisible(False)
            self.refresh_item_show(panel, data, True)

            @panel.btn_choose.unique_callback()
            def OnClick(btn, touch, _data=data):
                now = time.time()
                if now - self._last_scroll_time < self._last_scroll_interval:
                    return
                if self.is_scrolling:
                    return
                self.jump_to_rank_by_uid(global_data.player.uid, 0)

            return panel

    def jump_to_rank_by_uid(self, uid, cnt):
        if self.is_scrolling:
            return
        index = -1
        if self._data_list and uid in self._data_dict:
            index = self._data_list.index(uid)
        if index == -1:
            return
        list_node = self.list_rank
        if not list_node or not list_node.isValid():
            return
        show_uid = [ item._uid for item in list_node.GetAllItem() ]
        if not show_uid:
            return
        if uid in show_uid:
            uid_index = show_uid.index(uid)
            center_node = list_node.GetItem(uid_index)
            list_node.CenterWithNode(center_node)
            data = self._data_dict.get(uid)
            data and self.on_click_player_item(center_node, uid, data)
            return
        left_index = self._data_list.index(show_uid[0])
        right_index = self._data_list.index(show_uid[-1])
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
                self.jump_to_rank_by_uid(uid, cnt + 1)

        self.is_scrolling = True
        self.list_rank.DelayCall(0.001, scroll_callback)

    def filter_rank_list(self, rank_data):
        is_friend = self.is_friend_rank()
        if is_friend:
            return (rank_data['friend_rank_list'], rank_data['friend_rank_dict'])
        else:
            return (
             rank_data['rank_list'], rank_data['rank_dict'])

    def request_players_info(self, force=False):
        if not self._template_root or not self.list_rank or not global_data.player:
            return
        now = time.time()
        if not force and now - self._request_players_time < self._request_players_interval:
            return
        count = 0
        r_uid_list = []
        for i, uid in enumerate(self._data_list):
            if not self._message_data.has_player_inf(uid):
                r_uid_list.append(uid)
                count += 1
            if count > self._request_players_limit:
                break

        if force:
            self.list_rank.DeleteAllSubItem()
        if count > 0:
            self._request_players_time = now
            global_data.player.request_players_detail_inf(r_uid_list)
        elif force:
            self.on_players_detail_inf()

    def on_click_cur_player_item(self):
        if self._choose_data and self._choose_item:
            self.on_click_player_item(self._choose_item, self._choose_uid, self._choose_data)

    def on_click_player_item(self, item, uid, data):
        if not self._template_root or not item:
            return
        rank = data[PVE_RANK_DATA_RANK]
        data_obj = self.get_data_obj()
        info = [
         uid, data_obj]
        global_data.emgr.on_show_pve_rank_model.emit(info)
        self.show_rewards(rank)
        self.show_title(rank)
        if self._choose_item and self._choose_item.img_choose_frame and self._choose_item.isValid:
            self._choose_item.img_choose_frame.setVisible(False)
        self._choose_item = item
        self._choose_item.img_choose_frame and self._choose_item.img_choose_frame.setVisible(True)
        self._choose_uid = uid
        self._choose_data = data

    def reset_cur_choosed_info(self):
        self._choose_item = None
        self._choose_data = None
        self._choose_rank_key = None
        self._choose_uid = None
        return

    def show_player_pve_pass_ui(self, rank_key):
        uid = self._choose_pass_uid
        cur_rank_key = self.get_cur_rank_key()
        data_obj = self.get_data_obj()
        if not uid:
            return
        else:
            if rank_key != cur_rank_key:
                return
            req_uid_list, return_dict = self._message_data.get_pve_rank_pass_data(data_obj, [uid])
            pass_info = return_dict.get(uid, {})
            if not pass_info:
                return
            player_info = self._message_data.get_pve_rank_player_detail_inf(uid)
            if not player_info:
                return
            data = self.get_rank_data_by_uid(uid)
            if not data:
                return
            self._choose_pass_uid = None
            rank = data[PVE_RANK_DATA_RANK]
            ui = global_data.ui_mgr.show_ui('PVESinglePassDetailInfoUI', 'logic.comsys.battle.pve')
            if ui:
                ui.show_player_info(uid, self.RANK_PAGE_TYPE, rank_key, rank, pass_info, player_info)
            return