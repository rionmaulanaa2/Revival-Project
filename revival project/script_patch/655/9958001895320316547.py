# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/message/BPChat.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
import cc
from common.const.property_const import *
RICHTEXT_CONTENT_EDGE = 10
RICHTEXT_BOTTOM_TRIANGLE_WIDTH = 13
from logic.gcommon.common_utils.local_text import get_text_by_id, get_server_text
from logic.comsys.chat.MainChat import check_show_msg
from .SimpleChat import SimpleChat

class BPChat(SimpleChat):
    MIN_SEND_TIME = 2

    def __init__(self, panel, rise_panel, battle_type):
        from logic.gcommon.common_const.chat_const import CHAT_MATCH_QUEUE
        self.history_send_msg_list = []
        super(BPChat, self).__init__(CHAT_MATCH_QUEUE, panel, rise_panel)
        self.init_touch_event()
        self.battle_type = battle_type
        self.is_in_touch = False
        self._unread_msg_count = 0
        self._is_msg_lock = False

        @self.panel.bar_chat.btn_chat.callback()
        def OnClick(*args):
            ui = global_data.ui_mgr.show_ui('QuickChatEmote', 'logic.comsys.chat')
            self._chat_emote_ui = ui
            ui.set_input_box(self._input_box, panel.btn_send.btn_common, self.battle_type)
            ui.set_history_msg_list(self.history_send_msg_list)
            ui.init_upper_tag()

        self.panel.btn_top.setVisible(False)

        @self.panel.btn_top.callback()
        def OnClick(*args):
            self.refresh_channel_show(self._cur_msg_data)
            self._unread_msg_count = 0
            self._is_msg_lock = False
            self.panel.btn_top.setVisible(False)

    def init_touch_event(self):
        self.is_in_touch = False
        self._lv_chat.addTouchEventListener(self._on_normal_touch)

    def _on_normal_touch(self, widget, event):
        import ccui
        if event == ccui.WIDGET_TOUCHEVENTTYPE_BEGAN:
            self.is_in_touch = True
        elif event == ccui.WIDGET_TOUCHEVENTTYPE_ENDED:
            self.is_in_touch = False
        elif event == ccui.WIDGET_TOUCHEVENTTYPE_CANCELED:
            self.is_in_touch = False

    def init_touch(self):
        self._is_check_sview = False

        def scroll_callback(sender, eventType):
            if not self.is_in_touch:
                return
            if self._is_check_sview == False:
                self._is_check_sview = True
                self.panel.SetTimeOut(0.021, self.check_sview)
            in_height = sender.getInnerContainerSize().height
            out_height = sender.getContentSize().height
            if in_height != out_height:
                posy = sender.getInnerContainer().getPositionY()
                if posy > 0:
                    self._is_msg_lock = False
                    self._unread_msg_count = 0
                    self.panel.btn_top.setVisible(False)
                elif posy < 0:
                    self._is_msg_lock = True

        self._lv_chat.addEventListener(scroll_callback)

    def on_add_channel_msg(self, index_move, channel, data):
        if self._channel_index == channel:
            self._cur_msg_data.append(data)
            in_height = self._lv_chat.getInnerContainerSize().height
            out_height = self._lv_chat.getContentSize().height
            if self._is_msg_lock and in_height != out_height:
                if 'sender_info' in data and 'notify_type' not in data['sender_info'] and self._my_uid == data['sender_info'].get(U_ID, 0):
                    self.refresh_channel_show(self._cur_msg_data)
                    self._unread_msg_count = 0
                    self._is_msg_lock = False
                    self.panel.btn_top.setVisible(False)
                else:
                    self._unread_msg_count += 1
                    if self._unread_msg_count <= 99:
                        msg_inf = get_text_by_id(11002, (self._unread_msg_count,))
                    else:
                        msg_inf = get_text_by_id(11003)
                    self.panel.btn_top.SetText(msg_inf)
                    self.panel.btn_top.setVisible(True)
            else:
                self.add_msg(data, is_new=True)
                self._lv_chat._container._refreshItemPos()
                self._lv_chat._refreshItemPos()
                self._lv_chat.jumpToBottom()
            self._sview_data_index += index_move

    def init_channel(self):
        self.refresh_channel_show([])

    def load_template_format(self):
        self.chat_temp = global_data.uisystem.load_template('lobby/bp_chat/bp_chat_item')

    def release_template_format(self):
        global_data.uisystem.unload_template('lobby/bp_chat/bp_chat_item')

    def add_msg(self, data, is_back_item=True, index=-1, is_new=False):
        sender_info = data.get('sender_info', '')
        if sender_info:
            from logic.gutils.chat_utils import has_extra_msg
            msg = data.get('msg', None)
            if msg:
                data['msg'] = check_show_msg(msg)
            panel = self.add_text_msg(data, is_back_item)
        else:
            panel = None
        return panel

    def add_text_msg(self, data, is_back_item=True):
        conf = self.chat_temp
        anchor_x = 1.0
        align = 0
        scale = 1
        is_left = False
        chat_ui_item, msg_pos, size, rt_width, time_msg_offset = self.make_chat_message(data, conf, is_back_item, anchor_x, align, is_left)
        self.adjust_chat_panel(chat_ui_item, msg_pos, scale, rt_width, size, time_msg_offset)
        return chat_ui_item

    def make_chat_message(self, data, conf, is_back_item, anchor_x, align, is_left):
        from logic.gcommon.common_const import rank_const
        if is_back_item:
            chat_ui_item = self._lv_chat.AddItem(conf, bRefresh=True)
        else:
            chat_ui_item = self._lv_chat.AddItem(conf, 0, bRefresh=True)
        chat = chat_ui_item
        name = '<color=0XFECD40FF>%s</color>' % data['sender_info'][C_NAME]
        chat_item_no = data['sender_info'].get('chat_background', 0)
        sender_info = data['sender_info']
        uid = sender_info.get(U_ID, 0)
        is_my_message = self._my_uid == uid
        from logic.gutils.role_head_utils import set_role_head_frame, set_role_head_photo, get_head_photo_res_path
        head_data = global_data.message_data.get_role_head_info(uid)
        info_dict = sender_info or {}
        frame_no = head_data.get(HEAD_FRAME) or info_dict.get(HEAD_FRAME)
        photo_no = head_data.get(HEAD_PHOTO) or info_dict.get(HEAD_PHOTO)
        head_icon = get_head_photo_res_path(photo_no)
        chat.icon_head.SetDisplayFrameByPath('', head_icon)
        msg = data['msg']
        content = chat.lab_msg
        content.SetString('%s:%s' % (name, msg))
        content.formatText()
        size = content.getTextContentSize()
        content_width = self.get_max_line_width(content.getLineWidths())
        time_msg_offset = 0
        pos = content.getPosition()
        msg_pos = {'x': pos.x,'y': pos.y}
        return (
         chat_ui_item, msg_pos, size, content_width, time_msg_offset)

    def adjust_chat_panel(self, chat_ui_item, msg_pos, scale, rt_width, size, time_msg_offset):
        chat = chat_ui_item
        pnl_size = chat.getContentSize()
        img_item = None
        if getattr(chat, 'img_item'):
            img_item = chat.img_item
        elif getattr(chat, 'temp_bar'):
            img_item = chat.temp_bar.chat_bar
            img_item = chat.temp_bar
        if img_item:
            img_item_pos = img_item.getPosition()
            img_item_size = img_item.getContentSize()
            x_diff = img_item_pos.x - msg_pos['x']
            richtext_bottom_width = x_diff * scale + rt_width + RICHTEXT_CONTENT_EDGE + RICHTEXT_BOTTOM_TRIANGLE_WIDTH
            richtext_bottom_height = img_item_pos.y - msg_pos['y'] + size.height + RICHTEXT_CONTENT_EDGE
            img_item.setContentSize(cc.Size(richtext_bottom_width, richtext_bottom_height))
            bottom_height = pnl_size.height - img_item_size.height + richtext_bottom_height + RICHTEXT_CONTENT_EDGE
            img_item.ChildResizeAndPosition()
        else:
            bottom_height = pnl_size.height - msg_pos['y'] + size.height + RICHTEXT_CONTENT_EDGE
        if bottom_height < pnl_size.height:
            bottom_height = pnl_size.height
        chat.setContentSize(cc.Size(pnl_size.width, bottom_height))
        chat_ui_item.setContentSize(cc.Size(pnl_size.width, bottom_height))
        offset = bottom_height - pnl_size.height
        for child in chat.getChildren():
            pos = child.getPosition()
            child.setPosition(cc.Vec2(pos.x, pos.y + offset))

        chat.SetPosition('50%', '50%')
        if time_msg_offset != 0:
            chat.setContentSize(cc.Size(pnl_size.width, bottom_height + time_msg_offset))
            chat_ui_item.setContentSize(cc.Size(pnl_size.width, bottom_height + time_msg_offset))
        return

    def on_send_success(self, msg):
        self.history_send_msg_list.append(msg)

    def init_quick_emote(self):
        pass

    def destroy(self):
        super(BPChat, self).destroy()
        global_data.ui_mgr.close_ui('QuickChatEmote')