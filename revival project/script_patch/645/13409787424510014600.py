# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/pve/PVEMainUIWidgetUI/PVEDonateDebrisWidget.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
from logic.gutils.template_utils import WindowTopSingleSelectListHelper
from common.const.uiconst import NORMAL_LAYER_ZORDER_1, UI_VKB_CLOSE
from logic.gutils.role_head_utils import init_role_head, init_dan_info, init_privliege_badge
from common.const.property_const import U_ID, C_NAME, HEAD_FRAME, HEAD_PHOTO
from logic.gcommon.common_const.pve_const import PVE_STORY_DEBRIS_CACHE
from logic.gutils.item_utils import get_lobby_item_name, get_lobby_item_desc
from logic.gutils.task_utils import get_task_status_info
from logic.gutils.pve_lobby_utils import init_story_debris_item
from logic.gcommon.common_utils.ui_gameplay_utils import get_online_inf, get_online_inf_by_uid_simple
from logic.gcommon.const import PLAYER_INFO_BRIEF, PRIV_SHOW_BADGE, PRIV_SHOW_PURPLE_ID
from logic.gcommon.cdata.privilege_data import COLOR_NAME
from logic.comsys.message.FriendList import get_name_richtext
from .PVEDonateDebrisGiveWidget import PVEDonateDebrisGiveWidget
from common.cfg import confmgr
import six_ex
USE_MORE_LIST_COUNT = 3
DONATE_DEBRIS_TASK_ID = '1451983'
DEBRIS_GET_TAB_INDEX = 0
DEBRIS_GIVE_TAB_INDEX = 1

class PVEDonateDebrisWidget(BasePanel):
    PANEL_CONFIG_NAME = 'pve/fragments/open_pve_fragments_center'
    DLG_ZORDER = NORMAL_LAYER_ZORDER_1
    UI_VKB_TYPE = UI_VKB_CLOSE
    UI_ACTION_EVENT = {'nd_content.pnl_content.btn_close.OnClick': 'close'
       }

    def on_init_panel(self, default_tab_index=0, select_debris_id=None, *args, **kwargs):
        super(PVEDonateDebrisWidget, self).on_init_panel()
        self.init_params(default_tab_index, select_debris_id)
        self.init_ui()
        self.init_ui_event()
        self.process_events(True)

    def init_params(self, default_tab_index, select_debris_id):
        self._message_data = global_data.message_data
        self._default_tab_index = default_tab_index
        self._cur_select_tab_index = 0
        self._tab_btn_dict = {}
        self._tab_widgets = {}
        self._tab_list = [{'index': DEBRIS_GET_TAB_INDEX,'text': 1400071,'nd': self.panel.nd_get,'check_func': self._check_can_get,'init_func': self._init_nd_get,'check_redpoint_func': self._check_can_get_debris}, {'index': DEBRIS_GIVE_TAB_INDEX,'text': 1400053,'nd': self.panel.nd_give,'check_func': self._check_can_give,'init_func': self._init_nd_give}]
        self._is_check_get_sview = False
        self._cur_show_get_index = 0
        self._uid_to_item_dict = {}
        self._get_data = global_data.player.get_unreceived_story_debris_dict() if global_data.player else {}
        self._select_debris_id = select_debris_id
        self._give_widget = None
        self._is_check_friend_sview = False
        self._cur_show_friend_index = 0
        self._friend_id_to_item_dict = {}
        global_data.player and global_data.player.request_unreceived_story_debris()
        return

    def init_ui(self):
        self._list_details_get = self.panel.list_details_get
        self.panel.nd_get.setVisible(False)
        self.panel.nd_give.setVisible(False)
        self._init_bar()
        self._update_tab_red_point()
        self._update_task_label()

    def process_events(self, is_bind):
        emgr = global_data.emgr
        econf = {'on_get_pve_unreceived_story_debris_update': (
                                                       self.refresh_nd_get, self._update_tab_red_point),
           'on_receive_pve_story_debris_by_donator': (
                                                    self.on_receive_pve_story_debris_by_donator, self._update_tab_red_point),
           'on_receive_all_pve_story_debris': (
                                             self.refresh_nd_get, self._update_tab_red_point),
           'task_prog_changed': self.on_task_prog_changed,
           'message_on_player_simple_inf': self.message_on_player_simple_inf
           }
        emgr.bind_events(econf) if is_bind else emgr.unbind_events(econf)

    def init_ui_event(self):

        @self.panel.btn_get_all.unique_callback()
        def OnClick(btn, touch):
            if not global_data.player:
                return
            global_data.player.receive_all_donate_story_debris()

        @self.panel.nd_touch.unique_callback()
        def OnClick(btn, touch):
            self.panel.nd_friend.setVisible(False)
            self.panel.nd_touch.setVisible(False)

        @self.panel.btn_describe.callback()
        def OnClick(btn, touch):
            dlg = global_data.ui_mgr.show_ui('GameRuleDescUI', 'logic.comsys.common_ui')
            dlg.set_show_rule(1400057, 1400059)

        @self._list_details_get.unique_callback()
        def OnScrolling(sender):
            if self._is_check_get_sview is False:
                self._is_check_get_sview = True
                self._list_details_get.SetTimeOut(0.02, self._check_get_sview)

    def _init_bar(self):

        def _init_btn(node, data):
            node.btn_tab.SetText(get_text_by_id(data.get('text', '')))
            self._tab_btn_dict[data['index']] = node

        def _btn_click_cb(ui_item, data, index):
            self._cur_select_tab_index = index
            nd = data.get('nd')
            if self._tab_widgets.get(index) is None:
                self._tab_widgets[index] = nd
                init_func = data.get('init_func')
                init_func()
            check_func = data.get('check_func')
            if check_func:
                check_func()
            for _index in self._tab_widgets:
                widget = self._tab_widgets[_index]
                widget.setVisible(_index == index)

            return

        tab_list = self.panel.list_tab_left
        self._career_bar_wrapper = WindowTopSingleSelectListHelper()
        self._career_bar_wrapper.set_up_list(tab_list, self._tab_list, _init_btn, _btn_click_cb)
        self._career_bar_wrapper.set_node_click(tab_list.GetItem(self._default_tab_index))

    def _update_task_label(self):
        _, cur_prog, max_prog, _ = get_task_status_info(DONATE_DEBRIS_TASK_ID)
        self.panel.lab_tips.SetString(get_text_by_id(1400058).format(cur_prog, max_prog))

    def on_task_prog_changed(self, prog_changes):
        for change in prog_changes:
            if change.task_id == DONATE_DEBRIS_TASK_ID:
                self._update_task_label()
                return

    def _init_nd_get(self):
        self._refresh_nd_get_list()
        self._check_can_get()

    def refresh_nd_get(self):
        self._get_data = global_data.player.get_unreceived_story_debris_dict() if global_data.player else {}
        self._init_nd_get()
        self._check_can_get()

    def on_receive_pve_story_debris_by_donator(self, donater_id):
        donater_id = int(donater_id)
        self._get_data = global_data.player.get_unreceived_story_debris_dict() if global_data.player else {}
        get_item = self._uid_to_item_dict.get(donater_id)
        if get_item and get_item.isValid():
            self._list_details_get.DeleteItem(get_item)
        self._check_can_get()

    def _check_can_get(self):
        if len(self._get_data) == 0:
            self.panel.btn_get_all.setVisible(False)
            self.panel.nd_empty_get.setVisible(True)
        else:
            self.panel.btn_get_all.setVisible(True)
            self.panel.nd_empty_get.setVisible(False)

    def _refresh_nd_get_list(self):
        self._uid_to_item_dict = {}
        self._list_details_get.DeleteAllSubItem()
        show_data = self._get_nd_get_data()
        data_count = len(show_data)
        sview_height = self._list_details_get.getContentSize().height
        all_height = 0
        index = 0
        while all_height < sview_height + 100:
            if data_count - index <= 0:
                break
            data = show_data[index]
            get_item = self._add_get_list_item(data, True, index)
            all_height += get_item.getContentSize().height
            index += 1

        self._list_details_get.ScrollToTop()
        self._list_details_get._container._refreshItemPos()
        self._list_details_get._refreshItemPos()
        self._cur_show_get_index = index - 1

    def _check_get_sview(self):
        show_data = self._get_nd_get_data()
        self._cur_show_get_index = self._list_details_get.AutoAddAndRemoveItem(self._cur_show_get_index, show_data, len(show_data), self._add_get_list_item)
        self._is_check_get_sview = False

    def _get_nd_get_data(self):
        return list(self._get_data)

    def _add_get_list_item(self, donater_id, is_back_item, index=-1):
        if is_back_item:
            get_item = self._list_details_get.AddTemplateItem(bRefresh=True)
        else:
            get_item = self._list_details_get.AddTemplateItem(0, bRefresh=True)
        donater_id = int(donater_id)
        self._uid_to_item_dict[donater_id] = get_item
        self._init_friend_info(get_item, donater_id)
        self._init_debris_item(get_item, donater_id)

        @get_item.btn_get.callback()
        def OnClick(btn, touch):
            if not global_data.player:
                return
            global_data.player.request_receive_pve_story_debris_by_donator(donater_id)

        return get_item

    def _init_debris_item(self, get_item, donater_id):
        debris_info = self._get_data[str(donater_id)]
        list_item = get_item.list_item
        list_item_more = get_item.list_item_more
        list_item.DeleteAllSubItem()
        list_item_more.DeleteAllSubItem()
        if len(debris_info) > USE_MORE_LIST_COUNT:
            cur_list_item = list_item_more
            cur_list_item.setVisible(True)
            list_item.setVisible(False)
        else:
            cur_list_item = list_item
            cur_list_item.setVisible(True)
            list_item_more.setVisible(False)
        pve_story_debris_cache = global_data.achi_mgr.get_general_archive_data().get_field(PVE_STORY_DEBRIS_CACHE, [])
        for debris_id, count in six_ex.items(debris_info):
            debris_item = cur_list_item.AddTemplateItem()
            init_story_debris_item(debris_item, debris_id, count, False)
            debris_item.img_tag.setVisible(int(debris_id) not in pve_story_debris_cache)

    def _init_nd_give(self):
        self._give_widget = PVEDonateDebrisGiveWidget(self, self._select_debris_id)

    def _check_can_give(self):
        if self._give_widget:
            self._give_widget.check_can_give()

    def message_on_player_simple_inf(self, player_inf):
        if self._cur_select_tab_index != DEBRIS_GET_TAB_INDEX:
            return
        if not player_inf:
            return
        uid = player_inf.get(U_ID)
        get_item = self._uid_to_item_dict.get(uid)
        if get_item and not get_item.isValid():
            return
        get_data = self._get_data.get(str(uid))
        if not get_data:
            return
        if not get_item and get_data:
            get_item = self._add_get_list_item(uid, True)
        self._init_friend_info(get_item, uid)

    def _init_friend_info(self, item, uid):
        friend_info = self._message_data.get_player_inf(PLAYER_INFO_BRIEF, uid)
        if not friend_info:
            friend_info = {}
        init_role_head(item.temp_role, friend_info.get(HEAD_FRAME), friend_info.get(HEAD_PHOTO))
        lab_player_name = item.lab_player_name
        lab_player_name.SetString(friend_info.get(C_NAME, ''))
        lab_player_name.setVisible(True)
        init_dan_info(item.temp_tier, uid)
        priv_lv = friend_info.get('priv_lv', 0)
        priv_settings = friend_info.get('priv_settings', {})
        priv_purple_id = friend_info.get('priv_purple_id', False)
        init_privliege_badge(item.temp_role, priv_lv, priv_settings.get(PRIV_SHOW_BADGE, False))
        if priv_lv != 0:
            if lab_player_name and priv_purple_id and priv_settings.get(PRIV_SHOW_PURPLE_ID, False):
                priv_name_color = '%sFF' % hex(COLOR_NAME)
                lab_player_name.SetString(get_name_richtext(friend_info, priv_name_color))
        lab_state = item.lab_state
        if lab_state:
            text, color = get_online_inf_by_uid_simple(int(uid))
            lab_state.setString(text)
            lab_state.SetColor(color)

    def _update_tab_red_point(self, *args):
        for index, btn_tab in six_ex.items(self._tab_btn_dict):
            redpoint_check_func = self._tab_list[index].get('check_redpoint_func')
            if redpoint_check_func:
                btn_tab.temp_red.setVisible(redpoint_check_func())
            else:
                btn_tab.temp_red.setVisible(False)

    def _check_can_get_debris(self, *args):
        if not global_data.player:
            return False
        return bool(global_data.player.get_unreceived_story_debris_dict())

    def on_finalize_panel(self):
        self.process_events(False)
        if self._give_widget:
            self._give_widget.destroy()
            self._give_widget = None
        super(PVEDonateDebrisWidget, self).on_finalize_panel()
        return