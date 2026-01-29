# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/chat/QuickChatEmote.py
from __future__ import absolute_import
import six
from six.moves import range
from common.uisys.basepanel import BasePanel
import common.const.uiconst
from cocosui import cc, ccui, ccs
from logic.client.const import emote_const
from common.cfg import confmgr
from logic.comsys.archive.archive_manager import ArchiveManager
from logic.gutils.mall_utils import item_has_owned_by_item_no
from logic.gutils.item_utils import get_lobby_item_left_time
from logic.gcommon import time_utility as tutil
from logic.gcommon.item.item_const import DEFAULT_EMOTE_PACK
from logic.gutils.chat_utils import check_has_split_emote, filter_split_emote, get_all_split_emote
NUM_PER_PAGE = 16
NUM_PER_BIG_PAGE = 6
TURN_FACTOR = 0.1
from common.const import uiconst

class QuickChatEmote(BasePanel):
    DLG_ZORDER = common.const.uiconst.NORMAL_LAYER_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_CUSTOM
    PANEL_CONFIG_NAME = 'lobby/bp_chat/bp_chat_function'

    def on_init_panel(self, *args, **kargs):
        super(QuickChatEmote, self).on_init_panel()
        self.close_callback = None
        self._input_box = None
        self._send_btn = None
        self._battle_type = None
        self._history_msg_list = []
        self.cur_list_node = self.panel.list_emote
        self._emote_dict = confmgr.get('emote', 'emote')
        self._emote_list = confmgr.get('emote', 'emote_list')
        self._month_card_emotes = self._emote_list['riko_month_card']
        self.process_event(True)
        custom_emote = ArchiveManager().get_archive_data('custom_emote')
        self._my_custom_emote = custom_emote.get_field(str(global_data.player.uid))
        if self._my_custom_emote is None:
            self._my_custom_emote = [
             200, 203, 206]
        self._page_height = self.panel.list_emote.GetContentSize()[1]
        self._cur_tag = -1
        self._tag_index_dict = {}
        self._emote_num = 0
        self._page_num = 0
        self._cur_page = -1
        self._cur_upper_tag = -1

        @self.panel.nd_close.callback()
        def OnClick(*args):
            self.panel.SetTimeOut(0.001, self.close)

        self._tag_info = confmgr.get('chat_emoji', default={})
        self._all_emotes_info = confmgr.get('chat_all_emotes', default={})
        self.init_tag()
        for node in (self.panel.list_emote, self.panel.list_emote_big):
            node.addTouchEventListener(self._on_normal_touch)
            node.setInertiaScrollEnabled(False)

        self._pos_y = 0
        if not global_data.lobby_red_point_data:
            from logic.comsys.lobby.LobbyRedPointData import LobbyRedPointData
            LobbyRedPointData()
        return

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'refresh_item_red_point': self.update_rp,
           'on_lobby_bag_item_changed_event': self.on_remove_item
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def ui_vkb_custom_func(self):
        self.close()
        return True

    def update_rp(self):
        if not self._tag_index_dict:
            return
        else:
            for item_id, ui_index in six.iteritems(self._tag_index_dict):
                if item_id not in DEFAULT_EMOTE_PACK:
                    show_rp = self.get_rp_by_no(item_id)
                elif check_has_split_emote(item_id):
                    emote_list = get_all_split_emote(item_id)
                    show_rp = False
                    for emote in emote_list:
                        emote_item_id = self._all_emotes_info[str(emote)].get('iItemId', None)
                        if emote_item_id and self.get_rp_by_no(emote_item_id):
                            show_rp = True
                            break

                else:
                    show_rp = False
                self.panel.list_tab2.GetItem(ui_index).temp_reddot.setVisible(show_rp)

            return

    def is_multi_mode(self):
        from logic.gcommon.common_utils.battle_utils import get_play_type_by_battle_id
        from logic.gutils.mode_utils import get_sub_modes_by_play_type
        if self._battle_type:
            play_type = get_play_type_by_battle_id(self._battle_type)
            modes = get_sub_modes_by_play_type(play_type)
            return len(modes) > 1
        return False

    def init_upper_tag(self):
        list_tab = self.panel.list_tab
        tab_infos = [(860004, ), (81234, ), (19767, )]
        list_tab.SetInitCount(len(tab_infos))
        for idx, tab_info in enumerate(tab_infos):
            ui_item = list_tab.GetItem(idx)
            if ui_item:
                ui_item.btn_emote.SetText(tab_info[0])

                @ui_item.btn_emote.callback()
                def OnClick(btn, touch, idx=idx):
                    self.select_upper_tag(idx)

        self.select_upper_tag(0)

    def select_upper_tag(self, idx):
        if idx == 0:
            self.panel.list_tab2.setVisible(False)
            self.panel.list_emote.setVisible(False)
            self.panel.list_emote_big.setVisible(False)
            reply_text_list = confmgr.get('match_queue_quick_chat', 'content', default=[])
            reply_text_list = [ int(i) for i in reply_text_list ]
            reply_text_list = reply_text_list[3:] if self.is_multi_mode() else reply_text_list
            self.panel.list_reply.setVisible(True)
            self.update_list_reply(reply_text_list)
        elif idx == 2:
            self.panel.list_tab2.setVisible(False)
            self.panel.list_emote.setVisible(False)
            self.panel.list_emote_big.setVisible(False)
            self.panel.list_reply.setVisible(True)
            self.update_list_reply(self._history_msg_list)
        elif idx == 1:
            self.panel.nd_empty_record.setVisible(False)
            self.panel.list_reply.setVisible(False)
            self.panel.list_tab2.setVisible(True)
            self.panel.list_emote.setVisible(False)
            self.panel.list_emote_big.setVisible(False)
            self.select_tag(self._cur_tag, force_refresh=True)
        self._cur_upper_tag = idx
        for index in range(self.panel.list_tab.GetItemCount()):
            self.panel.list_tab.GetItem(index).btn_emote.SetSelect(index == self._cur_upper_tag)

    def update_list_reply(self, data_list):
        from logic.client.const.emote_const import EMOTE_TYPE, POPO_TYPE
        self.panel.list_reply.SetInitCount(len(data_list))
        import re
        pattern = re.compile('<emote=(\\d+),\\d{1,3}>')
        for i, data in enumerate(data_list):
            item = self.panel.list_reply.GetItem(i)
            if item:
                item.lab_content.SetString(data)
                sz = item.getContentSize()
                text_sz = item.lab_content.GetTextContentSize()
                item.SetContentSize(sz.width, text_sz.height + 20)
                item.lab_content.ReConfPosition()

                @item.callback()
                def OnClick(btn, touch, data=data):
                    is_big_emote = False
                    emote_no = None
                    if type(data) not in [int]:
                        ret = re.match(pattern, data)
                        if ret:
                            emote_no = int(ret.group(1))
                        if emote_no is not None:
                            is_normal_one = emote_no in self._emote_list[EMOTE_TYPE] or emote_no in self._emote_list[POPO_TYPE]
                            is_big_emote = not is_normal_one
                    if is_big_emote and self._send_btn:
                        self._send_btn.OnClick(None, do_not_check_msg=self._emote_dict.get(str(emote_no)))
                    elif self._input_box:
                        if type(data) in [int]:
                            self._input_box.set_text(get_text_by_id(data))
                        else:
                            self._input_box.set_text(str(data))
                    return

        self.panel.nd_empty_record.setVisible(len(data_list) <= 0)
        self.panel.list_reply.RefreshItemPos()

    def init_tag(self):
        list_tab = self.panel.list_tab2
        list_tab.SetInitCount(len(DEFAULT_EMOTE_PACK))
        index = -1
        self._tag_index_dict = {}
        for item_id, chat_info in six.iteritems(self._tag_info):
            item_id = int(item_id)
            if item_id in DEFAULT_EMOTE_PACK:
                index += 1
                self._tag_index_dict[item_id] = index
            elif check_has_split_emote(item_id):
                emote_list = get_all_split_emote(item_id)
                if emote_list:
                    index += 1
                    self._tag_index_dict[item_id] = index
                    ui_item = list_tab.AddTemplateItem()
                    show_rp = False
                    for emote in emote_list:
                        emote_item_id = self._all_emotes_info[str(emote)].get('iItemId', None)
                        if emote_item_id and self.get_rp_by_no(emote_item_id):
                            show_rp = True
                            break

                    ui_item.temp_reddot.setVisible(show_rp)
                else:
                    continue
            elif global_data.player.has_item_by_no(item_id):
                index += 1
                self._tag_index_dict[item_id] = index
                ui_item = list_tab.AddTemplateItem()
                show_rp = self.get_rp_by_no(item_id)
                ui_item.temp_reddot.setVisible(show_rp)
            else:
                continue
            tag_name = chat_info['iTxtId']
            tag_item = list_tab.GetItem(index)
            tag_item.btn_emote.SetText(tag_name)

            @tag_item.btn_emote.callback()
            def OnClick(btn, touch, tag=item_id):
                self.select_tag(tag)
                if tag not in DEFAULT_EMOTE_PACK:
                    if check_has_split_emote(tag):
                        _emote_list = get_all_split_emote(tag)
                        for _emote in _emote_list:
                            _emote_item_id = self._all_emotes_info[str(_emote)].get('iItemId', None)
                            if _emote_item_id and self.get_rp_by_no(_emote_item_id):
                                global_data.player.req_del_item_redpoint(_emote_item_id)

                    else:
                        show_new = self.get_rp_by_no(tag)
                        if show_new:
                            global_data.player.req_del_item_redpoint(tag)
                return

        self.select_tag(0)
        return

    def get_rp_by_no(self, tag):
        if global_data.lobby_red_point_data:
            return global_data.lobby_red_point_data.get_rp_by_no(tag)
        else:
            return False

    def select_tag(self, tag, force_refresh=False):
        if not force_refresh:
            if tag == self._cur_tag or str(tag) not in self._tag_info:
                return
        for item_id, chat_info in six.iteritems(self._tag_info):
            item_id = int(item_id)
            if item_id not in self._tag_index_dict:
                continue
            index = self._tag_index_dict[item_id]
            self.panel.list_tab2.GetItem(index).btn_emote.SetSelect(item_id == tag)

        self._cur_tag = tag
        cur_list_node = bool(self.cur_emote_is_big()) or self.panel.list_emote if 1 else self.panel.list_emote_big
        if cur_list_node != self.cur_list_node:
            self.cur_list_node.setVisible(False)
            cur_list_node.setVisible(True)
        self.cur_list_node = cur_list_node
        if force_refresh:
            cur_list_node.setVisible(True)
        self._page_height = self.cur_list_node.GetContentSize()[1]
        self._load_emotes()
        self._set_expire_time()

    def set_input_box(self, input_box, send_btn, battle_type):
        self._input_box = input_box
        self._send_btn = send_btn
        self._battle_type = battle_type

    def set_history_msg_list(self, msg_list):
        self._history_msg_list = msg_list

    def get_bg_height(self):
        pos = self.panel.img_bg.getPosition()
        return self.panel.img_bg.getContentSize().height + pos.y

    def set_close_callback(self, callback):
        self.close_callback = callback

    def on_finalize_panel(self):
        if self.close_callback:
            self.close_callback()
        ArchiveManager().get_archive_data('custom_emote').set_field(str(global_data.player.uid), self._my_custom_emote)
        self.process_event(False)
        self._history_msg_list = []
        super(QuickChatEmote, self).on_finalize_panel()

    def _on_normal_touch(self, widget, event):
        if event == ccui.WIDGET_TOUCHEVENTTYPE_BEGAN:
            self._pos_y = self.cur_list_node.GetContentOffset().y
        elif event in (ccui.WIDGET_TOUCHEVENTTYPE_ENDED, ccui.WIDGET_TOUCHEVENTTYPE_CANCELED):
            pos = self.cur_list_node.GetContentOffset()
            dy = self._pos_y - pos.y
            threshold = self._page_height * TURN_FACTOR
            if dy < -threshold:
                self._cur_page = min(self._cur_page + 1, self._page_num)
            elif dy > threshold:
                self._cur_page = max(self._cur_page - 1, 0)
            total_height = self.cur_list_node.GetInnerContainer().getContentSize().height
            view_height = self.cur_list_node.getContentSize().height
            ctrl_height = self.cur_list_node.GetCtrlSize().height
            offset_y = view_height - total_height + self._cur_page * ctrl_height
            offset_y = min(offset_y, 0)
            func = lambda : self.cur_list_node.SetContentOffsetInDuration(cc.Vec2(pos.x, offset_y), 0.2, False)
            self.panel.SetTimeOut(0.001, func, 100)
            self._refresh_list_num()

    def _load_emotes(self):
        import copy
        num_per_page = self.get_cur_num_per_page()
        cur_tag = self._cur_tag
        key = self.get_cur_emote_key()
        emote_list = self._emote_list[key] if cur_tag else self._my_custom_emote
        if check_has_split_emote(self._cur_tag):
            emote_list = filter_split_emote(emote_list)
        if key == 'riko':
            emote_list = copy.deepcopy(emote_list)
            emote_list.extend(self._month_card_emotes)
        self._emote_num = len(emote_list)
        self._page_num = self._emote_num // num_per_page
        if self._emote_num > self._page_num * num_per_page:
            self._page_num += 1
        self.cur_list_node.SetInitCount(self._page_num)
        self.panel.list_num.SetInitCount(self._page_num)
        for i in range(self._page_num):
            page_container = self.cur_list_node.GetItem(i)
            self._load_one_page(page_container.lv_emote, i, emote_list)
            self.cur_list_node._set_up_ctrl(page_container)

        self._cur_page = 0
        pos = self.cur_list_node.GetContentOffset()
        self.cur_list_node.ScrollToTop()
        self._refresh_list_num()

        @self.cur_list_node.callback()
        def OnScrolling(container):
            self._refresh_list_num()

    def get_cur_emote_key(self):
        return self._tag_info[str(self._cur_tag)]['cEmoteKey']

    def cur_emote_is_big(self):
        return self._tag_info[str(self._cur_tag)]['iIsBigEmote']

    def get_cur_num_per_page(self):
        if self.cur_emote_is_big():
            return NUM_PER_BIG_PAGE
        return NUM_PER_PAGE

    def _load_one_page(self, page_container, page_index, no_list):
        num_per_page = self.get_cur_num_per_page()
        begin_idx = page_index * num_per_page
        end_idx = min(begin_idx + num_per_page, len(no_list))
        no_list = no_list[begin_idx:end_idx]
        page_container.SetInitCount(len(no_list))
        for i, no in enumerate(no_list):
            item = page_container.GetItem(i)
            is_month_card_emot = no in self._month_card_emotes

            @item.callback()
            def OnClick(btn, touch, no=no, _is_month_card_emot=is_month_card_emot):
                if self.cur_emote_is_big() and self._send_btn:
                    if _is_month_card_emot and not global_data.player.has_yueka():
                        in_battle = not global_data.player or global_data.player.is_in_battle()
                        if True:
                            global_data.game_mgr.show_tip(get_text_by_id(82358))
                        return
                    self._send_btn.OnClick(None, do_not_check_msg=self._emote_dict.get(str(no)))
                elif self._input_box:
                    text = self._input_box.get_text()
                    text = text + '#' + str(no)
                    self._input_box.set_text(text)
                    if no in self._my_custom_emote:
                        self._my_custom_emote.remove(no)
                    self._my_custom_emote = [
                     no] + self._my_custom_emote
                    if len(self._my_custom_emote) > num_per_page:
                        self._my_custom_emote.pop()
                return

            s = self._emote_dict[str(no)]
            begin = s.find('=')
            end = s.find(',')
            filename = s[begin + 1:end] + '0000.png'
            item.img_item.SetSpriteFrame('', filename)
            if item.lab_name:
                item.lab_name.SetString(get_text_by_id(self._all_emotes_info.get(str(no), {}).get('iTxtId')))
            item.img_vip and item.img_vip.setVisible(is_month_card_emot)

    def _refresh_list_num(self):
        pos_y = self.cur_list_node.GetInnerContainer().getPositionY()
        cur_page = int(abs(pos_y) / self._page_height + 0.5)
        cur_page = min(cur_page, self._page_num - 1)
        for i in range(self._page_num):
            btn = self.panel.list_num.GetItem(i)
            if btn:
                btn = btn.btn_icon_choose
                btn and btn.SetSelect(i == cur_page)

    def _set_expire_time(self):
        self.panel.lab_time_available.setVisible(False)
        self.panel.lab_time_available.stopAllActions()
        if self._cur_tag in DEFAULT_EMOTE_PACK:
            return
        left_time = get_lobby_item_left_time(self._cur_tag)
        if left_time <= 0:
            return
        self.panel.lab_time_available.setVisible(True)
        delay = 1 if left_time < tutil.ONE_HOUR_SECONS else tutil.ONE_MINUTE_SECONDS
        text = tutil.get_readable_time_2(left_time)
        self.panel.lab_time_available.SetString(text + get_text_by_id(607217))
        self.panel.SetTimeOut(delay, self._set_expire_time)

    def on_remove_item(self):
        if self._cur_tag in DEFAULT_EMOTE_PACK:
            return
        if get_lobby_item_left_time(self._cur_tag) > 0:
            return
        self.init_tag()