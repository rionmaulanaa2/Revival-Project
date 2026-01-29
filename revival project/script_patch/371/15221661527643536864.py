# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/chat/DanmuChatWidget.py
from __future__ import absolute_import
from six.moves import range
from common.uisys.basepanel import BasePanel
import logic.comsys.common_ui.InputBox as InputBox
from logic.gutils import chat_utils
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gcommon.common_utils import text_utils
import time
STATE_DEAD = 3
quick_text_map = {STATE_DEAD: [ str(qid) for qid in range(19140, 19150) ]}

class DanmuChatWidget(object):
    SEND_CD = 4.0

    def init(self, panel, *args, **kargs):
        self.panel = panel
        self._is_chat_open = False
        self._last_send_time = 0
        self._enable_danmu = True
        self.enable_danmu_switch(True)
        self.is_in_send_cd = False
        self._send_group_message_either = False
        self.end_send_cd()
        self.init_botom()
        self.process_event(True)
        self.chat_close()
        self.enable_diy_text_input(True)
        self.init_click_event()

    def set_send_group_message_either(self, enable):
        self._send_group_message_either = enable

    def send_group_message_either(self):
        if not self._send_group_message_either:
            return False
        if not global_data.cam_lplayer:
            return False
        if not (global_data.player and global_data.player.logic):
            return False
        self_unit = global_data.player.logic
        if not global_data.cam_lplayer.ev_g_is_groupmate(self_unit.id, False):
            return False
        return True

    def init_click_event(self):

        @self.panel.bg_layer.callback()
        def OnBegin(btn, touch):
            self.on_bg_layer_begin(btn, touch)

        @self.panel.btn_confirm.callback()
        def OnClick(btn, touch):
            self.on_edit_box_send_callback()

    def process_event(self, is_bind):
        emgr = global_data.emgr
        event_infos = {}
        if is_bind:
            emgr.bind_events(event_infos)
        else:
            emgr.unbind_events(event_infos)

    def enable_diy_text_input(self, enable):
        self.panel.nd_diy.setVisible(enable)
        if enable:
            self.panel.lv_chat_list.SetContentSize(*self.panel.nd_lv_chat_min_size.GetContentSize())
        else:
            self.panel.lv_chat_list.SetContentSize(*self.panel.nd_lv_chat_max_size.GetContentSize())

    def enable_danmu_switch(self, enable):
        self._enable_danmu_switch = enable

    def on_danmu_input_chat_ui(self, *args):
        if not self.panel.nd_send.isVisible():
            self.chat_open()
        else:
            self.chat_close()

    def init_botom(self):
        nd_bottom = self.panel.nd_diy
        self._input_box = InputBox.InputBox(nd_bottom.input_box, max_length=20, placeholder=get_text_by_id(15816), send_callback=self.on_edit_box_send_callback, input_callback=self.on_edit_box_changed_callback)
        self._input_box.set_rise_widget(self.panel)
        self.panel.lab_title.SetString(get_text_by_id(80236))

    def on_edit_box_changed_callback(self, text):
        if text.endswith('\n') or text.endswith('\r'):
            text = text.rstrip('\n')
            text = text.rstrip('\r')
            self._input_box.set_text(text)
            self._input_box.detachWithIME()

    def check_can_send(self):
        import math
        MIN_SEND_TIME = self.SEND_CD
        cur_time = time.time()
        pass_time = cur_time - self._last_send_time
        from logic.gcommon.common_const import ui_operation_const as uoc
        if global_data.player and global_data.player.get_setting_2(uoc.BLOCK_ALL_MSG_KEY):
            return False
        if pass_time < MIN_SEND_TIME:
            global_data.game_mgr.show_tip(get_text_by_id(11008, {'time': str(int(math.ceil(MIN_SEND_TIME - pass_time)))}))
            return False
        return True

    def on_edit_box_send_callback(self, *args):
        msg = self._input_box.get_text()
        if not msg:
            return
        check_code, flag, msg = text_utils.check_review_words_chat(msg)
        if flag != text_utils.CHECK_WORDS_PASS:
            global_data.player.notify_client_message((get_text_by_id(11009),))
            if self.send_group_message_either():
                global_data.player.sa_log_forbidden_msg('danmu_chat', msg, check_code, hint=3, input_type='shortcut')
            else:
                global_data.player.sa_log_forbidden_msg('danmu_chat', msg, check_code, hint=2, input_type='text')
            return
        if not self.check_can_send():
            return
        if not global_data.player or not global_data.player.logic:
            return
        self._last_send_time = time.time()
        if self._enable_danmu_switch:
            if self.send_group_message_either():
                global_data.player.logic.send_event('E_SEND_BATTLE_GROUP_MSG', {'text': msg})
            else:
                global_data.player.logic.send_event('E_SEND_BS_MSG', msg)
                global_data.emgr.on_recv_danmu_msg.emit(msg, 1)
        self.on_into_chat_send_cd()
        self._input_box.set_text('')
        self.chat_close()

    def clean_input_box_msg(self, r_msg):
        msg = self._input_box.get_text()
        if r_msg == msg:
            self._input_box.set_text('')

    def chat_open(self):
        self.panel.nd_send.setVisible(True)
        self.panel.pnl_chat_list.setVisible(True)
        self.panel.bg_layer.setVisible(True)
        self.update_cur_show_quick_list()

    def update_cur_show_quick_list(self):
        self.update_cur_quick_list(STATE_DEAD)

    def chat_close(self):
        self.panel.nd_send.setVisible(False)
        self.panel.pnl_chat_list.setVisible(False)
        self.panel.bg_layer.setVisible(False)

    def update_cur_quick_list(self, state):
        from logic.client.const.game_mode_const import GAME_MODE_PVES
        if global_data.game_mode.is_mode_type(GAME_MODE_PVES):
            state += 100
        info_list = chat_utils.get_quick_notice_list(state)
        self.panel.lv_chat_list.SetInitCount(len(info_list))
        allItem = self.panel.lv_chat_list.GetAllItem()
        for idx, ui_item in enumerate(allItem):
            if idx < len(info_list):
                info = info_list[idx]
                self.init_quick_item(ui_item, info)

    def init_quick_item(self, ui_item, info):
        q_text_id = info.get('cQText')
        q_voice = info.get('cQVoice')
        ui_item.lab_content.SetString(get_text_by_id(q_text_id))

        @ui_item.btn_chat.unique_callback()
        def OnClick(btn, touch):
            if not self.check_can_send():
                return
            self._last_send_time = time.time()
            if self._enable_danmu_switch:
                msg = get_text_by_id(q_text_id)
                if self.send_group_message_either():
                    global_data.player.logic.send_event('E_SEND_BATTLE_GROUP_MSG', {'text': msg}, True)
                else:
                    global_data.player.logic.send_event('E_SEND_BS_MSG', msg)
                    global_data.emgr.on_recv_danmu_msg.emit(msg, 1)
            self.on_into_chat_send_cd()
            self.chat_close()

    def destroy(self):
        if self._input_box:
            self._input_box.destroy()
            self._input_box = None
        self.process_event(False)
        return

    def on_bg_layer_begin(self, btn, touch):
        if self.panel.btn_send.IsPointIn(touch.getLocation()):
            return
        self.chat_close()

    def on_into_chat_send_cd(self):
        self.is_in_send_cd = True
        self.panel.SetTimeOut(self.SEND_CD, self.end_send_cd, tag=180426)

    def end_send_cd(self):
        self.is_in_send_cd = False