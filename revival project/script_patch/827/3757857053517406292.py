# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/items_book_ui/BattleFlagWidget.py
from __future__ import absolute_import
import six_ex
import six
from functools import cmp_to_key
from logic.client.const import items_book_const
from common.cfg import confmgr
from logic.gutils import item_utils
from logic.comsys.items_book_ui.ItemsBookOwnBtnWidget import ItemsBookOwnBtnWidget
from logic.gutils import battle_flag_utils
from logic.gutils import career_utils
from logic.gutils import locate_utils
from logic.gcommon.item.item_const import DEFAULT_FLAG_FRAME
from logic.gutils.template_utils import set_ui_show_picture
from logic.comsys.role.BattleFlagChooseWidget import BattleFlagChooseWidget
from logic.comsys.role.BattleFlagBgChooseWidget import BattleFlagBgChooseWidget
from logic.gutils import role_head_utils
from logic.gcommon.common_utils.local_text import get_text_by_id
TAB_UI_BATTLE_FLAG = 2
TAB_TITLE = 3
FRAME_TEXT_ID = 860067
FRAME_TIPS_TXT_ID = 860130
TITLE_TEXT_ID = 10372
TITLE_TIPS_TXT_ID = 10373

class BattleFlagWidget(object):

    def __init__(self, parent, panel):
        self.page_index = items_book_const.BATTLEFLAG_ID
        self.parent = parent
        self.panel = panel
        self._own_widget = ItemsBookOwnBtnWidget(self.panel.btn_tick, self.on_click_own_btn)
        self.init_data()

    def init_data(self):
        self._tab_info = [{'cls': BattleFlagBgChooseWidget,'tab_name': FRAME_TEXT_ID,'tips': FRAME_TIPS_TXT_ID,'tab_id': TAB_UI_BATTLE_FLAG}]
        if locate_utils.is_open_location():
            from logic.comsys.role.BattleFlagLocationWidget import BattleFlagLocationWidget
            self._tab_info.append({'cls': BattleFlagLocationWidget,'tab_name': TITLE_TEXT_ID,'tips': TITLE_TIPS_TXT_ID,'tab_id': TAB_TITLE})
        self._cur_tab_id = 0
        self._jump_to_item_no = None
        self._cur_tab_widget = None
        self._cur_tab_btn = None
        self.last_battle_frame = None
        self.init_panel()
        self.init_event()
        return

    def init_event(self):
        self.process_event(True)

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'set_battle_flag_frame_event': self.refresh_flag_frame,
           'message_on_set_rank_title': self.refresh_rank_title,
           'message_on_player_role_head_photo': self.on_change_role_head_photo,
           'message_on_player_role_head': self.on_change_role_head_frame
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def init_panel(self):
        self.update_collect_count()
        self.refresh_rank_title()
        self.refresh_flag_frame(False)
        self.hide_medals_explain()
        tab_nd = self.panel.nd_change.temp_tab
        tab_lst = tab_nd.list_right
        tab_lst.SetInitCount(len(self._tab_info))

        @tab_lst.unique_callback()
        def OnCreateItem(lv, index, item_widget):
            self.cb_create_item(index, item_widget)

        all_items = tab_lst.GetAllItem()
        for index, widget in enumerate(all_items):
            if type(widget) in [dict, six.text_type, str]:
                continue
            self.cb_create_item(index, widget)

        @self.panel.nd_change.nd_touch.callback()
        def OnClick(btn, touch):
            self.refresh_flag_frame()

    def refresh_rank_title(self):
        battle_flag_utils.init_battle_flag_template_new(battle_flag_utils.get_battle_info_by_player(global_data.player), self.panel.temp_flag)

    def refresh_flag_frame(self, need_refresh_frame=True, battle_frame=None):
        if battle_frame or global_data.player:
            battle_frame = global_data.player.get_battle_flag_frame() if 1 else DEFAULT_FLAG_FRAME()
        self.panel.lab_frame_name.SetString(item_utils.get_lobby_item_name(battle_frame))
        if str(battle_frame) != str(self.last_battle_frame):
            if need_refresh_frame:
                self.panel.temp_flag.PlayAnimation('change')
            self.last_battle_frame = battle_frame
        need_refresh_frame and battle_flag_utils.refresh_battle_frame(battle_frame, self.panel.temp_flag.img_bar)
        need_refresh_frame and battle_flag_utils.refresh_battle_front_frame(battle_frame, self.panel.temp_flag.img_front)

    def hide_medals_explain(self):
        self.panel.list_explain.setVisible(False)

    def on_click_own_btn(self, *args):
        if self._cur_tab_widget:
            self._cur_tab_widget.cur_select_index = None
        self.update_show_on_condition()
        return

    def cb_create_item(self, index, tab_item):
        tab_info = self._tab_info[index]
        tab_item.btn.SetText(tab_info['tab_name'])

        @tab_item.btn.callback()
        def OnClick(btn, touch, index=index):
            self._cur_tab_id = index
            tab_info = self._tab_info[index]
            if self._cur_tab_widget:
                self._cur_tab_widget.destroy()
            temp_nd = self.panel.nd_change
            if self._cur_tab_id == 0:
                self._cur_tab_widget = tab_info['cls'](temp_nd, False)
                self.update_show_on_condition()
                self.panel.temp_prog.setVisible(True)
                self.panel.nd_choose.setVisible(True)
                self.panel.lab_prog.setVisible(True)
                self.panel.lab_collect.setVisible(True)
            else:
                self._cur_tab_widget = tab_info['cls'](temp_nd)
                self.panel.temp_prog.setVisible(False)
                self.panel.nd_choose.setVisible(False)
                self.panel.lab_prog.setVisible(False)
                self.panel.lab_collect.setVisible(False)
            temp_nd.nd_tips.SetString(get_text_by_id(tab_info.get('tips')))
            if self._cur_tab_btn:
                self._cur_tab_btn.SetSelect(False)
            self._cur_tab_btn = btn
            self._cur_tab_btn.SetSelect(True)

        if index == self._cur_tab_id:
            tab_item.btn.OnClick(tab_item.btn)
            if self._cur_tab_widget and self._jump_to_item_no is not None:
                if hasattr(self._cur_tab_widget, 'set_item_selected'):
                    self._cur_tab_widget.set_item_selected(self._jump_to_item_no)
                    self._jump_to_item_no = None
        return

    def get_battle_flag_collect_items(self):
        battle_flag_bg_config = confmgr.get('battle_flag_bg_config', default={})
        all_items = []
        owned_items = []
        for item_id, _ in six.iteritems(battle_flag_bg_config):
            if item_utils.can_open_show(item_id):
                all_items.append(item_id)
            is_owned = bool(global_data.player.get_item_by_no(int(item_id)))
            if is_owned:
                owned_items.append(item_id)

        def my_cmp(x, y):
            sort_key_x = item_utils.get_item_rare_degree(x)
            sort_key_y = item_utils.get_item_rare_degree(y)
            if sort_key_x == sort_key_y:
                return six_ex.compare(int(x), int(y))
            return six_ex.compare(sort_key_y, sort_key_x)

        def _owned_sort(item_id):
            if global_data.player.get_item_by_no(int(item_id)):
                return True
            return False

        all_items.sort(key=cmp_to_key(my_cmp))
        all_items.sort(key=_owned_sort, reverse=True)
        owned_items.sort(key=cmp_to_key(my_cmp))
        return (
         owned_items, all_items)

    def update_collect_count(self):
        own_list, all_list = self.get_battle_flag_collect_items()
        self.panel.temp_prog.lab_got.SetString('%d/%d' % (len(own_list), len(all_list)))
        self.panel.temp_prog.prog.SetPercentage(int(len(own_list) / float(len(all_list)) * 100))
        self.panel.lab_collect.SetString('%d/%d' % (len(own_list), len(all_list)))

    def update_show_on_condition(self):
        if self._cur_tab_id != 0:
            return
        owned_items, all_items = self.get_battle_flag_collect_items()
        info_list = []
        if self._own_widget.get_own_switch():
            info_list = owned_items
        else:
            info_list = all_items
        if self._cur_tab_widget:
            self._cur_tab_widget.init_item_list(info_list)

    def destroy(self):
        self.process_event(False)
        if self._cur_tab_widget:
            self._cur_tab_widget.destroy()
        self._cur_tab_widget = None
        return

    def on_change_role_head_photo(self, update_list):
        if global_data.player and global_data.player.uid in update_list:
            role_head_utils.set_role_head_photo(self.panel.temp_flag.temp_head, update_list[global_data.player.uid])

    def on_change_role_head_frame(self, update_list):
        if global_data.player and global_data.player.uid in update_list:
            role_head_utils.set_role_head_frame(self.panel.temp_flag.temp_head, update_list[global_data.player.uid])