# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/role/ChangeChatFrameWidget.py
from __future__ import absolute_import
import six
from six.moves import range
from common.uisys.basepanel import BasePanel
import common.const.uiconst as ui_const
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gcommon.item import item_const as iconst
from logic.gutils import role_head_utils
from logic.comsys.battle.Death.TabBaseWidget import TabBaseWidget
from common.cfg import confmgr
import cc
from logic.gcommon.item import lobby_item_type
from logic.gutils import item_utils
from logic.gcommon import time_utility
from logic.gutils import template_utils, chat_utils

class ChangeChatFrameWidget(TabBaseWidget):

    def __init__(self, panel, rise_panel):
        super(ChangeChatFrameWidget, self).__init__(panel)
        self.rise_panel = rise_panel
        self.lview = panel.list_frame
        self.init_parameters()
        self._init_all_chat_items()
        self.init_event()

    def init_chat_items(self):
        item_confs = confmgr.get('chat_head', default={})
        ignore_key = '__doc__'
        self._all_chat_items = []
        for item_no, one_config in six.iteritems(item_confs):
            if item_no == ignore_key:
                continue
            if one_config.get('iSkip', 0) == 1:
                continue
            if not chat_utils.is_chat_background_in_available_time(item_no):
                continue
            item_conf = confmgr.get('lobby_item', str(item_no))
            if item_conf:
                self._all_chat_items.append(int(item_no))

    def init_parameters(self):
        self.init_chat_items()
        chat_item = global_data.player.get_chat_frame_item()
        self.using_chat_item = self.check_using_chat_item(chat_item)
        self.choose_index = None
        self.number_to_index = {}
        self.index_to_number = {}
        self.init_own_chat_items()
        return

    def init_own_chat_items(self):
        chat_item_list = global_data.player.get_view_item_list(iconst.INV_VIEW_CHAT_ITEM)
        self.own_chat_items = set([ item.get_item_no() for item in chat_item_list ])
        if self.using_chat_item:
            self.own_chat_items.add(self.using_chat_item)

    def init_event(self):
        init_index = self.number_to_index.get(self.using_chat_item, 0)
        self.on_click_chat_item(init_index)
        global_data.emgr.message_on_player_chat_background_item += self.on_change_chat_background_item
        global_data.emgr.message_on_add_chat_item += self.on_message_on_add_chat_item

    def refresh(self):
        self.init_own_chat_items()
        self._init_all_chat_items()

    def on_finalize_panel(self):
        global_data.emgr.message_on_player_chat_background_item -= self.on_change_chat_background_item
        global_data.emgr.message_on_add_chat_item -= self.on_message_on_add_chat_item

    def on_message_on_add_chat_item(self, item_no):
        self.init_chat_items()
        self.refresh()
        index = self.number_to_index.get(item_no, 0)
        item = self.lview.GetItem(index)
        self._update_one_chat_items(item, index)
        if self.using_chat_item == item_no:
            self.on_click_chat_item(index)

    def _init_all_chat_items(self):
        self.number_to_index = {}
        self.index_to_number = {}
        init_num = self.lview.GetItemCount()
        index = 0
        for item_no in self._all_chat_items:
            item = None
            if index < init_num:
                item = self.lview.GetItem(index)
            else:
                item = self.lview.AddTemplateItem(bRefresh=False)
            self.number_to_index[item_no] = index
            self.index_to_number[index] = item_no
            self._update_one_chat_items(item, index)

            @item.callback()
            def OnClick(btn, touch, click_index=index):
                self.on_click_chat_item(click_index)

            index += 1

        if self.using_chat_item:
            using_index = self.number_to_index[self.using_chat_item]
            self.lview.GetItem(using_index).nd_using.setVisible(True)
        while index < init_num:
            init_num -= 1
            self.lview.DeleteItemIndex(init_num, False)

        self.lview.GetContainer()._refreshItemPos()
        self.lview._refreshItemPos()
        return

    def update_one_chat_item_pic(self, item_bar, item_no):
        res_path = item_utils.get_lobby_chat_item_pic_by_item_no(item_no)
        item_bar.SetDisplayFrameByPath('', res_path)
        img_list = item_bar.GetChildren()
        for index in range(1, 5):
            res_path = item_utils.get_lobby_chat_item_pic_by_item_no(item_no, index)
            one_img = img_list[index - 1]
            if res_path:
                one_img.SetDisplayFrameByPath('', res_path)
            if res_path:
                is_visible = True if 1 else False
                one_img.setVisible(is_visible)

    def _update_one_chat_items(self, ui_item, index):
        item_no = self.index_to_number[index]
        self.update_one_chat_item_pic(ui_item.temp_bar.chat_bar, item_no)
        text = ''
        total_remain_time = 0
        if item_no in self.own_chat_items:
            ui_item.nd_lock.setVisible(False)
            chat_item = global_data.player.get_item_by_no(item_no)
            total_remain_time = int(chat_item.get_expire_time() - time_utility.get_server_time())
        else:
            ui_item.nd_lock.setVisible(True)
        if self.choose_index is not None:
            is_visible = self.choose_index == index
            ui_item.nd_choose.setVisible(is_visible)
        else:
            ui_item.nd_choose.setVisible(False)
        is_visible = self.using_chat_item == item_no
        ui_item.nd_using.setVisible(is_visible)
        if total_remain_time > 0:
            template_utils.show_remain_time_countdown(ui_item.lab_date, ui_item.lab_date, total_remain_time)
        else:
            ui_item.lab_date.setVisible(True)
            ui_item.lab_date.SetString('')
        return

    def on_change_chat_background_item(self, item_no):
        if not self.lview:
            return
        else:
            if self.using_chat_item:
                index = self.number_to_index.get(self.using_chat_item)
                if index is not None:
                    ui_item = self.lview.GetItem(index)
                    ui_item.nd_using.setVisible(False)
            self.using_chat_item = self.check_using_chat_item(item_no)
            index = self.number_to_index.get(self.using_chat_item, None)
            if index is not None:
                ui_item = self.lview.GetItem(index)
                ui_item.nd_using.setVisible(True)
            self.set_equip_btn_state()
            return

    def on_click_chat_item(self, index):
        if self.choose_index is not None:
            last_item = self.lview.GetItem(self.choose_index)
            last_item.nd_choose.setVisible(False)
        self.choose_index = index
        item_no = self.index_to_number.get(index, None)
        if item_no is None:
            return
        else:
            item = self.lview.GetItem(index)
            item.nd_choose.setVisible(True)
            name = global_data.player.get_name()
            self.rise_panel.temp_chat_frame_now.lab_name.SetString(name)
            dan_info = global_data.player.get_dan_info()
            role_head_utils.set_role_dan(self.rise_panel.temp_chat_frame_now.temp_tier, dan_info)
            item_conf = confmgr.get('lobby_item', str(item_no))
            nameIDs = item_conf.get('name_id')
            if nameIDs:
                self.rise_panel.lab_frame_name.SetString(nameIDs[0])
            descIDs = item_conf.get('desc_id')
            if descIDs:
                self.rise_panel.lab_frame_desc.SetString(descIDs[0])
                self.rise_panel.lab_frame_desc.setVisible(True)
            else:
                self.rise_panel.lab_frame_desc.setVisible(False)
            self.update_one_chat_item_pic(self.rise_panel.temp_chat_frame_now.temp_bar.chat_bar, item_no)
            self.set_equip_btn_state()
            self.rise_panel.temp_chat_frame_now.lab_name.SetString(name)
            self.rise_panel.temp_chat_frame_now.lab_msg.SetString(608084)
            unlock_desc = item_utils.get_item_access(item_no)
            is_visible = True if unlock_desc else False
            self.rise_panel.btn_go.setVisible(is_visible)
            if unlock_desc:
                self.rise_panel.btn_go.lab_go.SetString(unlock_desc)

                @self.rise_panel.btn_go.callback()
                def OnClick(btn, touch, go_item_no=item_no):
                    item_utils.jump_to_ui(go_item_no)

            return

    def set_equip_btn_state(self):
        item_no = self.index_to_number.get(self.choose_index)
        btn = self.panel.btn_change
        btn.setVisible(True)
        self.rise_panel.nd_confirm.nd_lock.setVisible(False)
        if item_no == self.using_chat_item:
            btn.btn_common.SetText(2219)
            btn.btn_common.SetEnable(False)
        elif item_no in self.own_chat_items:
            btn.btn_common.SetText(2220)
            btn.btn_common.SetEnable(True)

            @btn.btn_common.callback()
            def OnClick(btn, touch, item_no=item_no):
                global_data.player.req_set_chat_background(item_no)

        else:
            btn.btn_common.SetText(2220)
            btn.btn_common.SetEnable(False)

    def check_using_chat_item(self, item_no):
        if item_no not in self._all_chat_items:
            return 0
        return item_no

    def select_item_by_item_no(self, item_no):
        if item_no not in self.number_to_index:
            return
        index = self.number_to_index[item_no]
        self.on_click_chat_item(index)