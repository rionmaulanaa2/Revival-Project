# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/live/LivePageWidgetBase.py
from __future__ import absolute_import
import six
from six.moves import range
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gutils.observe_utils import LiveObserveUIHelper, goto_spectate_player, decode_global_spectate_brief_info, is_global_spectate_data_time_valid, is_none
from logic.gcommon.common_const import spectate_const as sp_const
from logic.entities.avatarmembers.impUserSetting import deserialize_setting_2_val
from logic.gcommon.common_const.ui_operation_const import ENABLE_BE_SPECTATED_DEFAULT

class LivePageWidgetBase(object):
    LIST_SHOW_MIN_NUM = 6
    DECODE_NUM_PER_CHECK = 20

    def __init__(self, parent_panel, list_type):
        self._parent_panel = parent_panel
        self._list_type = list_type
        self._item_list_ui = None
        self._uid_2_ui_item = {}
        self._uid_to_name_dict = {}
        self._template_root = None
        self.init_event()
        self._all_brief_info_list = global_data.player.get_global_specate_brief_info(self._list_type)
        self._is_check_sview = False
        self._detail_info_dict = {}
        self._cur_show_index = -1
        self._valid_brief_info_list = []
        self._all_brief_info_index = 0
        self._need_follow_status = True
        self._need_friend_status = True
        self._other_list_type = None
        self._other_brief_info_list = []
        self._inserted_other_info_list = False
        self._valid_other_brief_info_list = []
        self._cur_show_data = []
        return

    def on_finalize_panel(self):
        self.process_event(False)
        self._uid_2_ui_item = {}
        self._uid_to_name_dict = {}
        self._item_list_ui = None
        self._template_root = None
        self._detail_info_dict = None
        self._cur_show_index = -1
        self._cur_show_data = []
        self._other_brief_info_list = []
        self._valid_other_brief_info_list = []
        return

    def set_other_spectate_type(self, other_list_type):
        self._other_list_type = other_list_type
        other_brief_info_list = global_data.player.get_global_specate_brief_info(self._other_list_type)
        self._other_brief_info_list = other_brief_info_list

    def get_other_spectate_type(self):
        return self._other_list_type

    def init_parameters(self):
        pass

    def get_spectate_type(self):
        return self._list_type

    def init_event(self):
        self.process_event(True)

    def init_panel(self):
        self._item_list_ui.setVisible(False)

        def scroll_callback(sender, eventType):
            if self._is_check_sview is False:
                self._is_check_sview = True
                self._item_list_ui.SetTimeOut(0.001, self.check_sview)

        self._item_list_ui.addEventListener(scroll_callback)

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'on_follow_result': self.on_follow_result,
           'on_undo_follow_result': self.on_undo_follow_result,
           'message_refresh_friends': self.message_refresh_friends,
           'on_loading_spectate': self.on_loading_spectate,
           'on_cancel_loading_spectate': self.cancel_loading_and_refresh
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def refresh_content_with_brief(self, refresh_ui=False):
        self._item_list_ui.DeleteAllSubItem()
        self._request_detail_index = 0
        self._valid_brief_info_list = []
        self._all_brief_info_index = 0
        self._detail_info_dict = {}
        self._uid_2_ui_item = {}
        self._inserted_other_info_list = False
        self._valid_other_brief_info_list = []
        self._cur_show_data = []
        show_data = self.get_show_brief_data()
        other_show_data = self.get_other_show_brief_data()
        youtube_data = self.get_youtube_data()
        self._cur_show_data = youtube_data + other_show_data + show_data
        self._cur_show_data = self.filter_cur_show_data()
        if refresh_ui:
            self._refresh_panel()
        if not self._cur_show_data:
            return
        index = 0
        data_count = len(self._cur_show_data)
        for i in range(LivePageWidgetBase.LIST_SHOW_MIN_NUM):
            if i >= data_count:
                break
            data = self._cur_show_data[i]
            ui_item = self.add_list_item(data, True)
            ui_item.setLocalZOrder(data_count - i)
            index += 1

        self._item_list_ui.ScrollToTop()
        self._item_list_ui._container._refreshItemPos()
        self._item_list_ui._refreshItemPos()
        self._cur_show_index = index - 1
        self._check_request_detail_data()

    def get_youtube_data(self):
        return []

    def refresh_content_with_details(self, list_type, list_info, refresh_ui=False):
        for item_data in list_info:
            player_uid = int(item_data.get('uid', 0))
            ui_item = self._uid_2_ui_item.get(player_uid)
            if not ui_item:
                continue
            if not self.check_can_be_spectated(item_data):
                continue
            item_data['list_type'] = list_type
            self._detail_info_dict[player_uid] = item_data
            if not ui_item.isValid():
                del self._uid_2_ui_item[player_uid]
                del self._detail_info_dict[player_uid]
                continue
            item_data['recommend_key'] = global_data.player.get_global_spectate_recommend_key(player_uid)
            self.refresh_list_item(ui_item, item_data, with_detail=True)

        if refresh_ui:
            self._refresh_panel()

    def check_sview(self):
        show_data = self._cur_show_data
        self._cur_show_index = self._item_list_ui.AutoAddAndRemoveItem_MulCol(self._cur_show_index, show_data, len(show_data), self.add_list_item, 300, 400, ignore_height_check=True)
        self._is_check_sview = False
        self._check_request_detail_data()
        if self._cur_show_index >= len(show_data) / 2:
            self._decode_spectate_brief_info()

    def _check_request_detail_data(self):
        ui_item_count = self._item_list_ui.GetItemCount()
        request_uids = {}
        for i in range(ui_item_count):
            ui_item = self._item_list_ui.GetItem(i)
            uid = ui_item.uid
            list_type = ui_item.list_type
            if uid in self._detail_info_dict:
                continue
            request_uids.setdefault(list_type, [])
            request_uids[list_type].append(uid)

        if request_uids and global_data.player:
            for list_type in six.iterkeys(request_uids):
                global_data.player.request_global_spectate_details(list_type, request_uids[list_type])

    def add_list_item(self, brief_data, is_back_item, index=-1):
        if is_back_item:
            panel = self._item_list_ui.AddTemplateItem(bRefresh=True)
        else:
            panel = self._item_list_ui.AddTemplateItem(0, bRefresh=True)
        if not brief_data:
            return
        player_uid = int(brief_data.get('uid', 0))
        if not player_uid:
            return
        if player_uid in self._detail_info_dict:
            item_data = self._detail_info_dict[player_uid]
            self.refresh_list_item(panel, item_data, with_detail=True)
        else:
            item_data = brief_data
            item_data['recommend_key'] = global_data.player.get_global_spectate_recommend_key(player_uid)
            self.refresh_list_item(panel, item_data, with_detail=False)
        return panel

    def refresh_list_item(self, ui_item, item_data, with_detail=False):
        player_uid = int(item_data.get('uid', 0))
        role_name = item_data.get('role_name')
        recommend_key = item_data.get('recommend_key')
        list_type = item_data.get('list_type', self._list_type)
        setattr(ui_item, 'uid', player_uid)
        setattr(ui_item, 'recommend_key', recommend_key)
        setattr(ui_item, 'has_details', with_detail)
        setattr(ui_item, 'list_type', list_type)
        self._init_live_observe_item(ui_item, list_type, item_data)
        self._uid_2_ui_item[player_uid] = ui_item
        self._uid_to_name_dict[player_uid] = role_name

    def _init_live_observe_item(self, ui_item, list_type, item_data):
        LiveObserveUIHelper.init_live_observe_item(ui_item, list_type, item_data)

    def get_show_brief_data(self):
        if not self._valid_brief_info_list:
            self._decode_spectate_brief_info()
        return self._valid_brief_info_list

    def get_other_show_brief_data(self):
        if not self._inserted_other_info_list:
            self._valid_other_brief_info_list = self._decode_spectate_brief_info_for_list(self._other_brief_info_list, self._other_list_type)
            self._inserted_other_info_list = True
        return self._valid_other_brief_info_list

    def _decode_spectate_brief_info(self):
        if self._all_brief_info_index >= len(self._all_brief_info_list):
            return
        else:
            for i in range(self._all_brief_info_index, self._all_brief_info_index + LivePageWidgetBase.DECODE_NUM_PER_CHECK):
                self._all_brief_info_index = i
                if i >= len(self._all_brief_info_list):
                    break
                brief_data = self._all_brief_info_list[i]
                brief_data = decode_global_spectate_brief_info(brief_data)
                if not brief_data:
                    continue
                if not is_global_spectate_data_time_valid(brief_data):
                    continue
                if not is_none(brief_data.get('competition_region', None)) and self._list_type != sp_const.SPECTATE_LIST_COMPETITION:
                    continue
                self._valid_brief_info_list.append(brief_data)

            if self._all_brief_info_index < len(self._all_brief_info_list):
                self._all_brief_info_index += 1
            return

    def _decode_spectate_brief_info_for_list(self, info_list, list_type):
        _valid_brief_info_list = []
        for i in range(LivePageWidgetBase.DECODE_NUM_PER_CHECK):
            if i >= len(info_list):
                break
            brief_data = info_list[i]
            brief_data = decode_global_spectate_brief_info(brief_data)
            if not brief_data:
                continue
            if not is_global_spectate_data_time_valid(brief_data):
                continue
            if not is_none(brief_data.get('competition_region', None)) and list_type != sp_const.SPECTATE_LIST_COMPETITION:
                continue
            brief_data_copy = dict(brief_data)
            brief_data_copy['list_type'] = list_type
            _valid_brief_info_list.append(brief_data_copy)

        return _valid_brief_info_list

    def message_refresh_friends(self):
        if not self._need_friend_status:
            return
        for uid, ui_item in six.iteritems(self._uid_2_ui_item):
            if not ui_item or not ui_item.isValid():
                continue
            LiveObserveUIHelper.refresh_friend_status(ui_item, uid)

    def on_follow_result(self, uid):
        if not self._need_follow_status:
            return
        self._refresh_follow_status(uid)

    def on_undo_follow_result(self, uid):
        if not self._need_follow_status:
            return
        self._refresh_follow_status(uid)

    def _refresh_follow_status(self, uid):
        if not self._need_follow_status:
            return
        else:
            ui_item = self._uid_2_ui_item.get(uid)
            if not ui_item or not ui_item.isValid():
                return
            name = self._uid_to_name_dict.get(uid, None)
            if ui_item:
                LiveObserveUIHelper.refresh_follow_status(ui_item, uid, name)
            if global_data.player and global_data.player.has_follow_player(uid):
                if name and self._item_list_ui.isVisible():
                    global_data.game_mgr.show_tip(get_text_by_id(10336).format(name))
            return

    def get_empty_content_text(self):
        pass

    def get_real_content_size(self):
        return len(self._valid_brief_info_list) + len(self._valid_other_brief_info_list) + len(self.get_youtube_data())

    def _refresh_panel(self):
        if self.get_real_content_size() > 0:
            if self._item_list_ui.isVisible():
                self._template_root.PlayAnimation('show')
            cur_item_count = self._item_list_ui.GetItemCount()
            for i in range(cur_item_count):
                ui_item = self._item_list_ui.GetItem(i)
                if ui_item and ui_item.isVisible():
                    ui_item.PlayAnimation('show')

    def show_panel(self):
        self._item_list_ui.setVisible(True)
        self._refresh_panel()

    def hide_panel(self):
        self._item_list_ui.setVisible(False)
        self._template_root.StopAnimation('show')
        self._template_root.vx.setVisible(False)
        cur_item_count = self._item_list_ui.GetItemCount()
        for i in range(cur_item_count):
            ui_item = self._item_list_ui.GetItem(i)
            ui_item.StopAnimation('show')

        self.cancel_loading_spectate()

    def on_loading_spectate(self, item_data):
        if not self._item_list_ui.isVisible():
            return
        self._template_root.PlayAnimation('show_loading')
        self._template_root.PlayAnimation('loading')

        def update_loading(pass_time):
            percent = int(pass_time / sp_const.CLIENT_LOADING_SPECTATE_TIME * 100)
            percent = 100 if percent > 100 else percent
            self._template_root.prog_loading.SetPercent(percent)
            str_percent = '{}%'.format(percent)
            self._template_root.lab_loading.SetString(str_percent)
            self._template_root.nd_pro_ani.SetPosition(str_percent, '100%')

        def finish_loading():
            if global_data.player and item_data:
                player_uid = int(item_data.get('uid', 0))
                spectate_type = item_data.get('list_type', self._list_type)
                if global_data.player.get_member_clan_info(player_uid):
                    spectate_type = sp_const.SPECTATE_LIST_CLAN
                item_data['spectate_type'] = spectate_type
                goto_spectate_player(item_data)

        self._template_root.TimerAction(update_loading, sp_const.CLIENT_LOADING_SPECTATE_TIME, finish_loading)
        if global_data.player:
            goto_spectate_player(item_data, ask_for_caching=True)

    def cancel_loading_spectate(self):
        self._template_root.nd_loading.setVisible(False)
        self._template_root.StopAnimation('show_loading')
        self._template_root.StopAnimation('loading')
        self._template_root.StopTimerAction()

    def cancel_loading_and_refresh(self):
        self.cancel_loading_spectate()
        self._refresh_panel()

    def check_can_be_spectated(self, item_data):
        setting_val = item_data.get('enable_be_spectated')
        if setting_val is None:
            enable_be_spectated = ENABLE_BE_SPECTATED_DEFAULT
        elif isinstance(setting_val, bool):
            enable_be_spectated = setting_val
        elif setting_val == 'True':
            enable_be_spectated = True
        elif setting_val == 'False':
            enable_be_spectated = False
        else:
            try:
                enable_be_spectated = deserialize_setting_2_val(setting_val)
            except:
                enable_be_spectated = ENABLE_BE_SPECTATED_DEFAULT

        return enable_be_spectated

    def filter_cur_show_data(self):
        new_show_data = []
        for data in self._cur_show_data:
            if self.check_can_be_spectated(data):
                new_show_data.append(data)

        return new_show_data