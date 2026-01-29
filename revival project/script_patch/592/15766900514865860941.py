# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/message/ConcertChat.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
import math
import time
from common.uisys.uielment.CCRichText import CCRichText
from cocosui import cc, ccui, ccs
from common.const.property_const import *
import common.const.uiconst
import common.utilities
import logic.comsys.common_ui.InputBox as InputBox
import game3d
import re
from logic.gcommon.common_utils.local_text import get_text_by_id
import logic.gcommon.const as const
from common.utils.cocos_utils import ccc3FromHex, ccp, CCRect, CCSizeZero, ccc4FromHex, ccc4aFromHex
import common.utilities
import logic.gutils.template_utils
from logic.gutils.role_head_utils import PlayerInfoManager
from logic.gcommon.common_const import chat_const
from logic.gcommon.common_utils import text_utils
from logic.gutils import role_head_utils
from logic.comsys.chat import chat_link
from bson.objectid import ObjectId
from mobile.common.EntityManager import EntityManager
from common.cfg import confmgr
RICHTEXT_CONTENT_EDGE = 10
RICHTEXT_BOTTOM_TRIANGLE_WIDTH = 13
from logic.gcommon.common_utils.local_text import get_text_by_id, get_server_text
from logic.comsys.chat.MainChat import check_show_msg

class ConcertChat(object):

    def __init__(self, main_panel):
        self._message_data = global_data.message_data
        self.main_panel = main_panel
        self.panel = main_panel.panel.chat_content
        from logic.gcommon.common_const.chat_const import CHAT_BATTLE_WORLD
        self._channel_index = CHAT_BATTLE_WORLD
        self._my_uid = global_data.player.uid
        self._last_send_time = time.time()
        self._player_info_manager = PlayerInfoManager()
        self._chat_emote_ui = None
        self._sview_data_index = 0
        self._cur_msg_data = []
        self._lv_chat = self.panel.lv_chat
        self._lv_chat.DeleteAllSubItem()
        self.reload_all_template_format()
        self.init_channel()
        self.init_touch()
        self.init_input()
        self.save_nd_chat_pos_y = self.main_panel.panel.GetPosition()[1]
        global_data.emgr.chat_add_channel_msg += self.on_add_channel_msg
        return

    def init_channel(self):
        self._lv_chat.DeleteAllSubItem()
        self._lv_chat.setVisible(True)
        self._cur_msg_data = self._message_data.get_channel_msg(self._channel_index)
        data_count = len(self._cur_msg_data)
        sview_height = self._lv_chat.getContentSize().height
        all_height = 0
        index = 0
        while all_height < sview_height + 200:
            if data_count - index <= 0:
                break
            data = self._cur_msg_data[data_count - index - 1]
            chat_pnl = self.add_msg(data, False)
            if chat_pnl is None:
                del self._cur_msg_data[data_count - index - 1]
                data_count -= 1
                continue
            all_height += chat_pnl.getContentSize().height
            index += 1

        self._lv_chat._container._refreshItemPos()
        self._lv_chat._refreshItemPos()
        self._lv_chat.ScrollToBottom()
        self._sview_data_index = len(self._cur_msg_data) - 1
        return

    def init_touch(self):
        self._is_check_sview = False

        def scroll_callback(sender, eventType):
            if self._is_check_sview == False:
                self._is_check_sview = True
                self._lv_chat.SetTimeOut(0.021, self.check_sview)

        self._lv_chat.addEventListener(scroll_callback)

    def init_input(self):
        panel = self.panel
        input_box = panel.input_box

        def max_input_cb(length, max_length):
            global_data.game_mgr.show_tip(get_text_by_id(19150, {'num': max_length}))

        def send_cb(*args, **kwargs):
            panel.btn_send.btn_common.OnClick(None)
            return

        self._input_box = InputBox.InputBox(input_box, max_input_cb=max_input_cb, send_callback=send_cb, detach_after_enter=False)
        self._input_box.set_rise_widget(self.main_panel)

        @panel.btn_emote.callback()
        def OnClick(*args):
            ui = global_data.ui_mgr.show_ui('ChatEmote', 'logic.comsys.chat')
            self._chat_emote_ui = ui
            ui.set_input_box(self._input_box, panel.btn_send.btn_common)
            ui.set_close_callback(self.panel_recover)
            panel_bot_pos = self.panel.img_bg.ConvertToWorldSpacePercentage(100, 100)
            height_offset = ui.get_bg_height() - panel_bot_pos.y + 5
            if height_offset < 0:
                height_offset = 0
            self.panel_up_move(height_offset)

        @panel.btn_send.btn_common.callback()
        def OnClick(*args, **kargs):
            cur_time = time.time()
            if cur_time - self._last_send_time < 0.5:
                return
            if global_data.player.get_lv() < chat_const.SEND_WORLD_MSG_MIN_LV:
                global_data.player.notify_client_message((get_text_by_id(11063).format(lv=chat_const.SEND_WORLD_MSG_MIN_LV),))
                return
            from logic.gcommon.common_const import ui_operation_const as uoc
            if global_data.player and global_data.player.get_setting_2(uoc.BLOCK_ALL_MSG_KEY):
                return
            pass_time = cur_time - self._last_send_time
            MIN_SEND_TIME = 5
            if pass_time < MIN_SEND_TIME:
                global_data.game_mgr.show_tip(get_text_by_id(11008, {'time': str(int(math.ceil(MIN_SEND_TIME - pass_time)))}))
                return
            self._last_send_time = cur_time
            do_not_check_msg = kargs.get('do_not_check_msg')
            msg = do_not_check_msg or self._input_box.get_text()
            self.send_msg(self._channel_index, msg, do_not_check_msg, from_input_box=True)

    def send_msg(self, channel, msg, do_not_check_msg=False, from_input_box=False):
        if msg == '':
            global_data.player.notify_client_message((get_text_by_id(11055),))
            return
        if channel == chat_const.CHAT_WORLD and global_data.player.get_lv() < chat_const.SEND_WORLD_MSG_MIN_LV:
            global_data.player.notify_client_message((get_text_by_id(11063).format(lv=chat_const.SEND_WORLD_MSG_MIN_LV),))
            return
        from logic.gcommon.common_const import ui_operation_const as uoc
        if global_data.player and global_data.player.get_setting_2(uoc.BLOCK_ALL_MSG_KEY):
            return
        if do_not_check_msg:
            check_code = 0
            check_result = text_utils.CHECK_WORDS_PASS
        else:
            check_code, check_result, msg = text_utils.check_review_words_chat(msg)
            if check_result == text_utils.CHECK_WORDS_NO_PASS:
                global_data.player.notify_client_message((get_text_by_id(11009),))
                global_data.player.sa_log_forbidden_msg(channel, msg, check_code)
                return
        if from_input_box:
            self._input_box.set_text('')
        if check_result == text_utils.CHECK_WORDS_PASS:
            global_data.player.send_msg(channel, msg, code=check_code)
        elif check_result == text_utils.CHECK_WORDS_ONLY_SELF:
            self._message_data.add_only_self_msg(channel, msg)
            global_data.player.sa_log_forbidden_msg(channel, msg, check_code)

    def on_add_channel_msg(self, index_move, channel, data):
        if self._channel_index == channel:
            self.add_msg(data)
            self._lv_chat._container._refreshItemPos()
            self._lv_chat._refreshItemPos()
            self._lv_chat.jumpToBottom()
            self._sview_data_index += index_move
            self.check_msg_dammu_content(data)

    def add_msg(self, data, is_back_item=True, index=-1, is_new=False):
        sender_info = data.get('sender_info', '')
        if sender_info:
            from logic.gutils.chat_utils import has_extra_msg
            is_extra_as_normal = self.is_this_extra_msg_show_as_text(data)
            msg = data.get('msg', None)
            if msg:
                if is_extra_as_normal:
                    msg = unpack_text(msg)
                data['msg'] = check_show_msg(msg)
            if has_extra_msg(data) and not is_extra_as_normal:
                panel = self.add_extra_msg(data, is_back_item, is_new)
            else:
                panel = self.add_text_msg(data, is_back_item)
        else:
            panel = None
        return panel

    def add_extra_msg(self, data, is_back_item=True, is_new=False):
        content, size, content_width, hide_bar = self._add_extra_msg(data)
        panel = content
        if panel:
            if is_back_item:
                self._lv_chat.AddControl(panel, bRefresh=True)
            else:
                self._lv_chat.AddControl(panel, index=0, bRefresh=True)
        return panel

    def add_text_msg(self, data, is_back_item=True):
        if self._my_uid == data['sender_info'].get(U_ID, 0):
            conf = self.chat_me_temp
            anchor_x = 1.0
            align = 0
            scale = 1
            is_left = False
        else:
            conf = self.chat_other_temp
            anchor_x = 0.0
            align = 0
            scale = -1
            is_left = True
        chat_ui_item, msg_pos, size, rt_width, time_msg_offset = self.make_chat_message(data, conf, is_back_item, anchor_x, align, is_left)
        self.adjust_chat_panel(chat_ui_item, msg_pos, scale, rt_width, size, time_msg_offset)
        chat_ui_item.temp_chat.temp_head.SetSwallowTouch(False)
        return chat_ui_item

    def make_chat_message(self, data, conf, is_back_item, anchor_x, align, is_left):
        from logic.gcommon.common_const import rank_const
        if is_back_item:
            chat_ui_item = self._lv_chat.AddItem(conf, bRefresh=True)
        else:
            chat_ui_item = self._lv_chat.AddItem(conf, 0, bRefresh=True)
        chat = chat_ui_item.temp_chat
        time_rt_msg, time_msg_offset = self.add_time_msg(chat, data)
        chat.lab_name.SetString(data['sender_info'][C_NAME])
        chat_item_no = data['sender_info'].get('chat_background', 0)
        sender_info = data['sender_info']
        uid = sender_info.get(U_ID, 0)
        is_my_message = self._my_uid == uid
        self._player_info_manager.add_head_item_auto(chat.temp_head, uid, 0, sender_info)
        from logic.gutils.chat_utils import has_extra_msg
        if not has_extra_msg(data) or self.is_this_extra_msg_show_as_text(data):
            msg = get_server_text(data['msg'])
            content = chat.lab_msg
            content.SetString(msg)
            content.formatText()
            size = content.getTextContentSize()
            content_width = self.get_max_line_width(content.getLineWidths())
        else:
            content, size, content_width, hide_bar = self._add_extra_msg(data, is_left)
            if size is None:
                size = chat.getContentSize()
                content_width = size.width
            if hide_bar:
                chat.temp_bar.setVisible(False)
        pos = content.getPosition()
        msg_pos = {'x': pos.x,'y': pos.y}
        return (
         chat_ui_item, msg_pos, size, content_width, time_msg_offset)

    def add_time_msg(self, chat, data):
        time_msg_offset = 0
        time_rt_msg = None
        if data.get('is_show_time', False) and data.get('time', 0):
            pnl_size = chat.getContentSize()
            time_str = '#SC%s</color>' % common.utilities.get_time_str_chat(data['time'])
            time_rt_msg = CCRichText.Create(time_str, 18, cc.Size(pnl_size.width, 0))
            time_rt_msg.setAnchorPoint(cc.Vec2(0.5, 1.0))
            time_rt_msg.setHorizontalAlign(1)
            time_rt_msg.formatText()
            chat.AddChild(None, time_rt_msg)
            time_msg_offset = time_rt_msg.getVirtualRendererSize().height
            time_rt_msg.SetPosition(pnl_size.width * 0.5, pnl_size.height + time_msg_offset)
        return (
         time_rt_msg, time_msg_offset)

    def adjust_chat_panel(self, chat_ui_item, msg_pos, scale, rt_width, size, time_msg_offset):
        chat = chat_ui_item.temp_chat
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

    def get_max_line_width(self, line_widths):
        max_width = None
        for width in line_widths:
            if not max_width:
                max_width = width
            elif max_width < width:
                max_width = width

        return max_width

    def reload_all_template_format(self):
        self.release_template_format()
        self.load_template_format()

    def load_template_format(self):
        self.chat_me_temp = global_data.uisystem.load_template('battle/i_fight_live_chat_anniversary')
        self.chat_other_temp = global_data.uisystem.load_template('battle/i_fight_live_chat_other')
        self.chat_sys_temp = global_data.uisystem.load_template('friend/chat_sys_item')

    def release_template_format(self):
        global_data.uisystem.unload_template('battle/i_fight_live_chat_anniversary')
        global_data.uisystem.unload_template('battle/i_fight_live_chat_other')
        global_data.uisystem.unload_template('friend/chat_sys_item')

    def check_sview(self):
        msg_count = len(self._cur_msg_data)
        self._sview_data_index = self._lv_chat.AutoAddAndRemoveItem_chat(self._sview_data_index, self._cur_msg_data, msg_count, self.add_msg, 300, 400)
        self._is_check_sview = False

    def panel_up_move(self, height):
        x, _ = self.main_panel.panel.GetPosition()
        self.main_panel.panel.SetPosition(x, self.save_nd_chat_pos_y + height)

    def panel_recover(self):
        x, _ = self.main_panel.panel.GetPosition()
        self.main_panel.panel.SetPosition(x, self.save_nd_chat_pos_y)
        self._chat_emote_ui = None
        return

    def hide_inputbox(self):
        if self._input_box:
            self._input_box.hide()

    def is_this_extra_msg_show_as_text(self, data):
        extra_msg_type = data.get('extra', {}).get('type', None)
        return extra_msg_type in [chat_const.MSG_TYPE_CONCERT_BULLET]

    def _add_extra_msg(self, data, is_me=False):
        msg_func_dict = {chat_const.MSG_TYPE_CONCERT_FIREWORK: self._make_firework_msg
           }
        extra_msg_type = data['extra'].get('type', None)
        if extra_msg_type in msg_func_dict:
            deal_func = msg_func_dict[extra_msg_type]
            return deal_func(data, is_me)
        else:
            return (
             None, None, None, False)
            return

    def _make_firework_msg(self, data, is_left):
        extra = data['extra']
        entity_id = extra.get('entity_id')
        firework_id = extra.get('firework_id', None)
        fireworks_data = confmgr.get('ai_concert_conf', 'FireworkSetting', 'Content', str(firework_id), default={})
        if fireworks_data.get('trigger_chat_msg') == 2:
            if not EntityManager.getentity(ObjectId(entity_id)):
                return (None, None, None, False)
        content = global_data.uisystem.load_template_create('battle/i_chat_firework')
        name = extra.get('player_name', '')
        from logic.gutils.template_utils import get_item_quality
        from logic.gutils.item_utils import get_item_pic_by_item_no
        from logic.gcommon.item.item_const import EPIC_PURPLE
        trigger_chat_msg = fireworks_data.get('trigger_chat_msg')
        txt_id = 82900 if trigger_chat_msg == 1 else 82840
        txt = get_text_by_id(txt_id, {'playername': name,'itemtype': firework_id})
        content.lab_kind_name.SetString(txt)
        content.nd_mech.img_skin.SetDisplayFrameByPath('', get_item_pic_by_item_no(firework_id))
        anim = 'show_high' if get_item_quality(firework_id) >= EPIC_PURPLE else 'show'
        content.PlayAnimation(anim)
        size = content.getContentSize()
        content_width = size.width
        return (
         content, size, content_width, False)

    def destroy(self):
        if self._chat_emote_ui:
            global_data.ui_mgr.close_ui('ChatEmote')
            self._chat_emote_ui = None
        if self._input_box:
            self._input_box.destroy()
            self._input_box = None
        self._lv_chat.DeleteAllSubItem()
        global_data.emgr.chat_add_channel_msg -= self.on_add_channel_msg
        self.release_template_format()
        return

    def check_msg_dammu_content(self, data):
        from logic.gutils.chat_utils import has_extra_msg
        if has_extra_msg(data):
            extra_msg_type = data['extra'].get('type', None)
            if extra_msg_type == chat_const.MSG_TYPE_CONCERT_FIREWORK:
                extra = data['extra']
                entity_id = extra.get('entity_id')
                name = extra.get('player_name', '')
                firework_id = extra.get('firework_id', None)
                fireworks_data = confmgr.get('ai_concert_conf', 'FireworkSetting', 'Content', str(firework_id), default={})
                danmu_text_id = fireworks_data.get('danmu_msg')
                if fireworks_data.get('trigger_chat_msg') == 2:
                    return
                if danmu_text_id:
                    dammu_txt = get_text_by_id(danmu_text_id, {'playername': name,'itemtype': firework_id})
                    global_data.emgr.on_recv_danmu_msg.emit(dammu_txt)
                    return
            elif extra_msg_type == chat_const.MSG_TYPE_CONCERT_BULLET:
                extra = data['extra']
                bullet_tid = extra.get('text', 0)
                if self._my_uid == data['sender_info'].get(U_ID, 0):
                    name = data['sender_info'][C_NAME]
                    text = name + ':' + get_text_by_id(bullet_tid)

                    def custom_func(item, danmu):
                        item.lab_player_name.SetString(text)
                        item.lab_player_name.formatText()
                        size = item.lab_player_name.getTextContentSize()
                        return size

                    global_data.emgr.on_recv_danmu_msg.emit(text, priority=0, head_pic=None, template='activity/activity_202212/music_lottery/i_music_lottery_barrage', custom_item_func=custom_func)
                else:
                    prefix = '<align=1>#SW<img="gui/ui_res_2/activity/activity_202109/kizuna/ai_dacall/chat/img_firework.png", scale=0.5>#n%s</align>'
                    global_data.emgr.on_recv_danmu_msg.emit(prefix % get_server_text(data['msg']))
        else:
            prefix = '<align=1>#SW<img="gui/ui_res_2/activity/activity_202109/kizuna/ai_dacall/chat/img_firework.png", scale=0.5>#n%s</align>'
            global_data.emgr.on_recv_danmu_msg.emit(prefix % get_server_text(data['msg']))
        return