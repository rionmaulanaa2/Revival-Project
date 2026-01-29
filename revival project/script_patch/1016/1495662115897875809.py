# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/pve/PVEMainUIWidgetUI/PVEDonateDebrisGiveWidget.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
from logic.gutils.template_utils import WindowTopSingleSelectListHelper
from common.const.uiconst import NORMAL_LAYER_ZORDER_1, UI_VKB_CLOSE
from logic.gutils.role_head_utils import init_role_head, init_dan_info, init_privliege_badge
from common.const.property_const import C_NAME, HEAD_FRAME, HEAD_PHOTO
from logic.gutils.item_utils import get_lobby_item_name, get_lobby_item_desc
from logic.gutils.task_utils import get_task_status_info
from logic.gutils.pve_lobby_utils import init_story_debris_item
from logic.gcommon.common_utils.ui_gameplay_utils import get_online_inf, get_online_inf_by_uid_simple
from logic.gcommon.const import PLAYER_INFO_BRIEF, PRIV_SHOW_BADGE, PRIV_SHOW_PURPLE_ID
from logic.gcommon.cdata.privilege_data import COLOR_NAME
from logic.comsys.message.FriendList import get_name_richtext
from common.cfg import confmgr
import six_ex
import math
DONATE_DEBRIS_TASK_ID = '1451983'
DEBRIS_COUNT_PER_PAGE = 3
FRIEND_COUNT_PER_PAGE = 4

class PVEDonateDebrisGiveWidget(object):

    def __init__(self, parent, select_debris_id):
        self.parent = parent
        self.panel = parent.panel
        self.init_params(select_debris_id)
        self.init_ui()
        self.init_ui_event()
        self.process_events(True)

    def init_params(self, select_debris_id):
        self._message_data = global_data.message_data
        self._chapter_conf = confmgr.get('pve_level_conf', 'ChapterConf', 'Content')
        self._init_clue_dict()
        self._init_debris_dict()
        self._select_give_debris_id = select_debris_id or 0
        self._cur_select_give_debris = 0
        self._cur_select_give_item = None
        self._cur_select_give_dict = {}
        self._cur_debris_info_list = None
        self._cur_select_chapter = 0
        self._cur_select_clue = 0
        self._cur_debris_page = 1
        self._max_debris_page = 0
        self._has_init_chapter_option_list = False
        self._has_init_clue_option_list = False
        self._is_check_friend_sview = False
        self._cur_show_friend_index = 0
        self._cur_friend_page = 1
        self._max_friend_page = 0
        global_data.message_data.request_player_online_state(immediately=True)
        global_data.message_data.request_wish_debris_info()
        return

    def _init_clue_dict(self):
        chapter_debris_conf = confmgr.get('story_debris_chapter_data')
        self._clue_conf = confmgr.get('story_debris_clue_data')
        self._clue_dict = {}
        for chapter_id, chapter_data in six_ex.items(chapter_debris_conf):
            clue_data = [
             0]
            clue_data += chapter_data.get('clue')
            self._clue_dict[int(chapter_id)] = clue_data
            if not self._clue_dict.get(0):
                self._clue_dict[0] = []
            self._clue_dict[0] += clue_data

        self._clue_dict[0] = list(set(self._clue_dict[0]))
        self._clue_dict[0].sort()

    def _init_debris_dict(self):
        story_debris_data = confmgr.get('story_debris_data', default={})
        self._debris_dict = {}
        self._debris_id_list = []
        for debris_id, debris_data in six_ex.items(story_debris_data):
            chapter_id = int(debris_data.get('chapter'))
            clue_id = int(debris_data.get('clue'))
            if not self._debris_dict.get(chapter_id):
                self._debris_dict[chapter_id] = {}
                self._debris_dict[chapter_id][0] = []
            if not self._debris_dict[chapter_id].get(clue_id):
                self._debris_dict[chapter_id][clue_id] = []
            self._debris_dict[chapter_id][clue_id].append(debris_id)
            self._debris_dict[chapter_id][0].append(debris_id)
            if not self._debris_dict.get(0):
                self._debris_dict[0] = {}
                self._debris_dict[0][0] = []
            if not self._debris_dict[0].get(clue_id):
                self._debris_dict[0][clue_id] = []
            self._debris_dict[0][clue_id].append(debris_id)
            self._debris_dict[0][0].append(debris_id)

        def sort_function(debris_id):
            debris_data = story_debris_data.get(debris_id)
            chapter = debris_data.get('chapter')
            clue = debris_data.get('clue')
            return (
             chapter, clue, debris_id)

        self._debris_id_list.sort(key=lambda x: sort_function(x))
        for clue_info in six_ex.values(self._debris_dict):
            for debris_id_list in six_ex.values(clue_info):
                debris_id_list.sort(key=lambda x: sort_function(x))

    def init_ui(self):
        self._list_details_give = self.panel.list_details_give
        self._list_friend = self.panel.list_friend_item
        self._refresh_nd_give()
        self._init_chapter_choose()
        self._init_clue_choose()

    def process_events(self, is_bind):
        emgr = global_data.emgr
        econf = {'on_donate_story_debris_succ': self._refresh_nd_give,
           'on_receive_pve_story_debris_by_donator': self._refresh_nd_give,
           'on_receive_all_pve_story_debris': self._refresh_nd_give,
           'message_refresh_friends': self._init_nd_friend,
           'message_friend_state': self._refresh_friend_state,
           'message_on_player_wish_derbis_info': self._refresh_friend_state
           }
        emgr.bind_events(econf) if is_bind else emgr.unbind_events(econf)

    def init_ui_event(self):
        nd_page_main = self.panel.nd_page_main

        @nd_page_main.btn_page_up.unique_callback()
        def OnClick(*args):
            if self._cur_debris_page >= self._max_debris_page:
                return
            else:
                self._cur_debris_page += 1
                self._update_debris_list()
                self.panel.nd_friend.setVisible(False)
                self.panel.nd_touch.setVisible(False)
                self._cur_select_give_item = None
                return

        @nd_page_main.btn_page_down.unique_callback()
        def OnClick(*args):
            if self._cur_debris_page <= 1:
                return
            else:
                self._cur_debris_page -= 1
                self._update_debris_list()
                self.panel.nd_friend.setVisible(False)
                self.panel.nd_touch.setVisible(False)
                self._cur_select_give_item = None
                return

        nd_page_friend = self.panel.nd_page_friend

        @nd_page_friend.btn_page_up.unique_callback()
        def OnClick(*args):
            if self._cur_friend_page >= self._max_friend_page:
                return
            self._cur_friend_page += 1
            self._update_friend_list()

        @nd_page_friend.btn_page_down.unique_callback()
        def OnClick(*args):
            if self._cur_friend_page <= 1:
                return
            self._cur_friend_page -= 1
            self._update_friend_list()

        @self._list_friend.unique_callback()
        def OnScrolling(sender):
            if self._is_check_friend_sview is False:
                self._is_check_friend_sview = True
                self._list_friend.SetTimeOut(0.02, self._check_friend_sview)

    def _init_chapter_choose(self):
        btn_choose = self.panel.temp_title_choose_chapter
        lab_title = btn_choose.lab_title_rank
        lab_title.SetString(get_text_by_id(1400074))
        temp_choose = self.panel.temp_choose_chapter

        def update_arrow():
            is_visible = temp_choose.isVisible()
            btn_choose.icon_arrow.setRotation(180 if is_visible else 0)

        @btn_choose.callback()
        def OnClick(*args):
            if not self._has_init_chapter_option_list:
                self._init_chapter_option_list()
                self._has_init_chapter_option_list = True
            temp_choose.setVisible(not temp_choose.isVisible())
            update_arrow()

        @temp_choose.nd_close.callback()
        def OnClick(*args):
            temp_choose.setVisible(False)
            update_arrow()

    def _init_chapter_option_list(self):
        btn_choose = self.panel.temp_title_choose_chapter
        lab_title = btn_choose.lab_title_rank
        temp_choose = self.panel.temp_choose_chapter

        def on_create_callback(_, chapter, item):
            if item:
                if chapter == 0:
                    chapter = 0
                    chapter_str = get_text_by_id(1400074)
                else:
                    chapter_conf = self._chapter_conf.get(str(chapter), {})
                    chapter_str = get_text_by_id(chapter_conf.get('title_text'))
                button = item.button
                button.SetText(chapter_str)

                @button.callback()
                def OnClick(btn, touch):
                    self._cur_select_chapter = int(chapter)
                    lab_title.SetString(chapter_str)
                    temp_choose.setVisible(False)
                    btn_choose.icon_arrow.setRotation(0)
                    self._has_init_clue_option_list = False
                    self._refresh_clue_option_list()
                    self._cur_select_clue = 0
                    self.panel.temp_title_choose_group.lab_title_rank.SetString(get_text_by_id(1400075))
                    self._cur_debris_page = 1
                    self._refresh_nd_give()

        conf = confmgr.get('pve_level_conf', 'ChapterConf', 'Content')
        option_list = temp_choose.option_list
        option_list.BindMethod('OnCreateItem', on_create_callback)
        option_list.DeleteAllSubItem()
        option_list.SetInitCount(len(conf) + 1)

    def _init_clue_choose(self):
        btn_choose = self.panel.temp_title_choose_group
        lab_title = btn_choose.lab_title_rank
        lab_title.SetString(get_text_by_id(1400075))
        temp_choose = self.panel.temp_choose_group

        def update_arrow():
            is_visible = temp_choose.isVisible()
            btn_choose.icon_arrow.setRotation(180 if is_visible else 0)

        @btn_choose.callback()
        def OnClick(*args):
            if not self._has_init_clue_option_list:
                self._refresh_clue_option_list()
                self._has_init_clue_option_list = True
            temp_choose.setVisible(not temp_choose.isVisible())
            update_arrow()

        @temp_choose.nd_close.callback()
        def OnClick(*args):
            temp_choose.setVisible(False)
            update_arrow()

    def _refresh_clue_option_list(self):
        btn_choose = self.panel.temp_title_choose_group
        lab_title = btn_choose.lab_title_rank
        temp_choose = self.panel.temp_choose_group

        def on_create_callback(_, index, item):
            if item:
                if index == 0:
                    clue_id = 0
                    clue_str = get_text_by_id(1400075)
                else:
                    if index == 1:
                        item.setVisible(False)
                        return
                    index -= 1
                    clue_id = self._clue_dict[self._cur_select_chapter][index]
                    clue_conf = self._clue_conf.get(str(clue_id), {})
                    clue_str = get_text_by_id(clue_conf.get('name_id'))
                button = item.button
                button.SetText(clue_str)

                @button.callback()
                def OnClick(btn, touch):
                    self._cur_select_clue = int(clue_id)
                    lab_title.SetString(clue_str)
                    temp_choose.setVisible(False)
                    btn_choose.icon_arrow.setRotation(0)
                    self._cur_debris_page = 1
                    self._refresh_nd_give()

        option_list = temp_choose.option_list
        option_list.BindMethod('OnCreateItem', on_create_callback)
        option_list.DeleteAllSubItem()
        option_list.SetInitCount(len(self._clue_dict[self._cur_select_chapter]) + 1)

    def _update_debris_page(self):
        self._max_debris_page = int(math.ceil(float(len(self._cur_debris_info_list)) / DEBRIS_COUNT_PER_PAGE))
        if self._cur_debris_page > self._max_debris_page:
            self._cur_debris_page = self._max_debris_page
        self.panel.nd_page_main.setVisible(self._max_debris_page > 0)
        self.panel.nd_page_main.lab_page.setString('{}/{}'.format(self._cur_debris_page, self._max_debris_page))

    def _refresh_nd_give(self, *args):
        self._update_debris_list()
        self.check_can_give()

    def _init_default_debris_page(self):
        if self._select_give_debris_id:
            for index, debris_info in enumerate(self._cur_debris_info_list):
                debris_id, count = debris_info
                if debris_id == self._select_give_debris_id:
                    self._cur_debris_page = index // DEBRIS_COUNT_PER_PAGE + 1
                    return

    def check_can_give(self):
        if len(self._cur_debris_info_list) == 0:
            self.panel.nd_empty_give.setVisible(True)
        else:
            self.panel.nd_empty_give.setVisible(False)
        self.panel.nd_page_main.setVisible(len(self._cur_debris_info_list) > 0)
        has_can_give_debris = False
        for debris_id in self._debris_dict.get(0, {}).get(0, {}):
            debris_id = int(debris_id)
            count = global_data.player.get_item_num_by_no(debris_id) if global_data.player else 0
            if count > 1:
                has_can_give_debris = True

        self.panel.temp_title_choose_chapter.setVisible(has_can_give_debris)
        self.panel.temp_title_choose_group.setVisible(has_can_give_debris)

    def _update_debris_list(self):
        self._list_details_give.DeleteAllSubItem()
        self._cur_debris_info_list = self._get_cur_select_debris_id_list()
        if not self._cur_debris_info_list:
            return
        self._init_default_debris_page()
        self._update_debris_page()
        cur_index = DEBRIS_COUNT_PER_PAGE * (self._cur_debris_page - 1)
        for i in range(DEBRIS_COUNT_PER_PAGE):
            index = cur_index + i
            if len(self._cur_debris_info_list) > index:
                give_item = self._list_details_give.AddTemplateItem()
                self._init_give_list_item(give_item, self._cur_debris_info_list[index])

    def _get_cur_select_debris_id_list(self):
        debris_info_list = []
        debris_id_list = self._debris_dict.get(self._cur_select_chapter, {}).get(self._cur_select_clue, {})
        for debris_id in debris_id_list:
            debris_id = int(debris_id)
            count = global_data.player.get_item_num_by_no(debris_id) if global_data.player else 0
            if count > 1:
                debris_info_list.append((debris_id, count - 1))

        return debris_info_list

    def _init_give_list_item(self, give_item, debris_info):
        debris_id, count = debris_info
        debris_item = give_item.temp_item
        init_story_debris_item(debris_item, debris_id, count, False)
        give_item.lab_name.setString(get_lobby_item_name(debris_id))
        give_item.lab_details.setString(get_lobby_item_desc(debris_id))
        btn_choose = give_item.btn_choose
        btn_choose.EnableCustomState(True)
        if self._select_give_debris_id == debris_id:
            self._select_give_debris_id = 0
            btn_choose.SetSelect(True)
        else:
            btn_choose.SetSelect(False)

        def on_select_player_head():
            self._cur_select_give_debris = debris_id
            self._cur_select_give_item = give_item
            self._init_nd_friend()

        btn_add = give_item.btn_add
        temp_role = give_item.temp_role
        cur_select_friend = self._cur_select_give_dict.get(debris_id)
        if cur_select_friend:
            self._init_friend_info(give_item, cur_select_friend)
            temp_role.setVisible(True)
            btn_add.setVisible(False)
        else:
            temp_role.setVisible(False)
            btn_add.setVisible(True)

        @btn_add.callback()
        def OnClick(btn, touch):
            on_select_player_head()

        @temp_role.callback()
        def OnClick(btn, touch):
            on_select_player_head()

        @give_item.btn_give.callback()
        def OnClick(btn, touch):
            if not global_data.player:
                return
            else:
                acceptor_uid = self._cur_select_give_dict.get(debris_id)
                if not acceptor_uid:
                    on_select_player_head()
                    return
                self._cur_select_give_dict[debris_id] = 0
                if self._cur_select_give_item and self._cur_select_give_item.isValid():
                    self._cur_select_give_item.lab_player_name.setString('')
                    self._cur_select_give_item.temp_role.setVisible(False)
                    self._cur_select_give_item.btn_add.setVisible(True)
                self._cur_select_give_item = None
                global_data.player.donate_story_debris(debris_id, acceptor_uid)
                return

        return give_item

    def on_donate_story_debris_succ(self, *args):
        self._refresh_nd_give()

    def _update_friend_page(self):
        self._max_friend_page = int(math.ceil(float(len(self._cur_friend_info_list)) / FRIEND_COUNT_PER_PAGE))
        self.panel.nd_page_friend.setVisible(self._max_friend_page > 0)
        self.panel.nd_page_friend.lab_page.setString('{}/{}'.format(self._cur_friend_page, self._max_friend_page))

    def _init_nd_friend(self):
        global_data.message_data.request_player_online_state(immediately=True)
        global_data.message_data.request_wish_debris_info()
        self._update_friend_list()
        self.panel.nd_friend.setVisible(True)
        self.panel.nd_touch.setVisible(True)

    def _refresh_friend_state(self):
        self._update_friend_list()

    def _update_friend_list(self):
        self._list_friend.DeleteAllSubItem()
        self._cur_friend_info_list = self._get_cur_friend_id_list()
        cur_index = FRIEND_COUNT_PER_PAGE * (self._cur_friend_page - 1)
        for i in range(FRIEND_COUNT_PER_PAGE):
            index = cur_index + i
            if len(self._cur_friend_info_list) > index:
                friend_item = self._list_friend.AddTemplateItem()
                self._init_friend_list_item(friend_item, self._cur_friend_info_list[index])

        self.panel.nd_empty_friend.setVisible(len(self._cur_friend_info_list) == 0)
        self._update_friend_page()

    def _get_cur_friend_id_list(self):

        def sort_function(friend_id):
            friend_id = int(friend_id)
            online_state = self._message_data.get_player_online_state_by_uid(friend_id)
            time_delta = self._message_data.get_player_offline_time_delta(friend_id)
            return (
             -online_state, time_delta)

        friend_list = list(self._message_data.get_friends())
        friend_list.sort(key=lambda x: sort_function(x))
        return friend_list

    def _init_friend_list_item(self, friend_item, friend_id):
        self._update_friend_wish_state(friend_item, friend_id)
        friend_item.frame_choose.setVisible(self._cur_select_give_dict.get(self._cur_select_give_debris) == friend_id)

        def select_give_friend():
            if not self._cur_select_give_item or not self._cur_select_give_item.isValid():
                return
            self.panel.nd_friend.setVisible(False)
            self.panel.nd_touch.setVisible(False)
            self._cur_select_give_dict[self._cur_select_give_debris] = friend_id
            self._cur_select_give_debris = 0
            self._init_friend_info(self._cur_select_give_item, friend_id)
            self._cur_select_give_item.temp_role.setVisible(True)
            self._cur_select_give_item.btn_add.setVisible(False)

        @friend_item.temp_role.callback()
        def OnClick(btn, touch):
            select_give_friend()

        @friend_item.btn_bg.callback()
        def OnClick(btn, touch):
            select_give_friend()

        return friend_item

    def _update_friend_wish_state(self, friend_item, friend_id):
        friend_data = self._init_friend_info(friend_item, friend_id)
        wish_debris_id = friend_data.get('pve_wished_debris_id')
        debris_item = friend_item.temp_item
        if wish_debris_id:
            debris_item.setVisible(True)
            init_story_debris_item(debris_item, wish_debris_id, 1, False)
            friend_item.lab_wish_name.setString(get_text_by_id(1400060).format(get_lobby_item_name(wish_debris_id)))
        else:
            debris_item.setVisible(False)
            friend_item.lab_wish_name.setString('')

    def _init_friend_info(self, item, uid):
        if not item or not item.isValid():
            return
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
        return friend_info

    def destroy(self):
        self.process_events(False)