# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/map/FightTalkUI.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
from common.const.uiconst import SCALE_PLATE_ZORDER
from logic.gcommon.const import NEOX_UNIT_SCALE
from common.const import uiconst
from logic.gcommon.common_utils import text_utils
from logic.gcommon import time_utility
import math
import cc
STATE_NORMAL = 1
STATE_SPEAK = 2
STATE_WAIT_MSG = 3
STATE_SEND_MSG = 4
END_TIME = 20
SEND_CD = 20

class FightTalkUI(BasePanel):
    PANEL_CONFIG_NAME = 'observe/fight_speak_generate_btn'
    DLG_ZORDER = SCALE_PLATE_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    UI_ACTION_EVENT = {'btn_battle_cancel.OnClick': 'on_cancel_btn_click',
       'btn_battle_finish.OnClick': 'on_end_btn_click'
       }

    def on_init_panel(self, player=None):
        self.init_event()
        self.init_parameter()
        self.init_record_timer()
        self.regist_main_ui()

    def init_parameter(self):
        self._state = STATE_NORMAL
        self._send_cd = SEND_CD
        self._last_send_time = 0
        self._wait_timer = None
        return

    def on_finalize_panel(self):
        self.unregist_main_ui()
        self.unbind_event(global_data.player)
        self.panel.lab_count.StopTimerAction()
        global_data.voice_mgr.stop_recording(False)
        if self._wait_timer:
            global_data.game_mgr.unregister_logic_timer(self._wait_timer)
        self._wait_timer = None
        return

    def init_event(self):
        self.bind_event(global_data.player)

    def on_cancel_btn_click(self, btn, touch):
        self.close()

    def init_record_timer(self):
        self._state = STATE_SPEAK
        self.panel.lab_voice.SetString(83157)
        global_data.voice_mgr.start_recording(self.on_voice_msg_send)

        def timer_end():
            self._state = STATE_WAIT_MSG
            self.end_record_voice_callback()

        def update_time(pass_time):
            if not self.panel:
                return
            left_second = int(END_TIME - pass_time)
            self.panel.lab_count.SetString('{}s'.format(left_second))
            self.panel.prog_battle_speak_1.SetPercentage(float(left_second) / END_TIME * 100.0)

        update_time(0)
        self.panel.lab_count.StopTimerAction()
        self.panel.lab_count.TimerAction(update_time, END_TIME, callback=timer_end, interval=1.0)

    def on_end_btn_click(self, btn, touch):
        if self._state == STATE_SPEAK:
            self._state = STATE_WAIT_MSG
            self._wait_timer = global_data.game_mgr.register_logic_timer(self.time_out, interval=5, times=1, mode=2)
            self.end_record_voice_callback()
        elif self._state == STATE_WAIT_MSG:
            global_data.game_mgr.show_tip(11115)
        elif self._state == STATE_SEND_MSG:
            self.send_msg()

    def end_record_voice_callback(self, is_cancel=False):
        global_data.voice_mgr.set_send_callback(self.on_voice_msg_send)
        global_data.voice_mgr.stop_recording(not is_cancel)
        self.panel.lab_count.StopTimerAction()
        self.panel.lab_count.setVisible(False)
        self.panel.lab_voice.SetString(11115)
        self.panel.btn_battle_finish.SetText(80137)
        self.panel.prog_battle_speak_2.setVisible(False)

    def on_voice_msg_send(self, voice_text, voice_data, finish=True):
        if not self.panel:
            return
        else:
            self._state = STATE_SEND_MSG
            self._voice_data = voice_data
            self._voice_text = voice_text
            self.set_voice_text(voice_text)
            if self._wait_timer:
                global_data.game_mgr.unregister_logic_timer(self._wait_timer)
                self._wait_timer = None
            return

    def set_voice_text(self, voice_text):
        self.panel.lab_voice.setVisible(False)
        self.panel.list_describe.setVisible(True)
        item = self.panel.list_describe.GetItem(0)
        item.lab_speak_generate.SetString(voice_text)
        size_text = item.lab_speak_generate.getContentSize()
        item.lab_speak_generate.formatText()
        sz = item.lab_speak_generate.GetTextContentSize()
        old_sz = item.getContentSize()
        item.setContentSize(cc.Size(old_sz.width, sz.height + 20))
        item.RecursionReConfPosition()
        old_inner_size = self.panel.list_describe.GetInnerContentSize()
        self.panel.list_describe.SetInnerContentSize(old_inner_size.width, sz.height)
        self.panel.list_describe.GetContainer()._refreshItemPos()
        self.panel.list_describe._refreshItemPos()

    def time_out(self):
        if not self.panel:
            return
        self.set_voice_text('')
        self._state = STATE_SEND_MSG

    def send_msg(self):
        if self._state != STATE_SEND_MSG:
            return
        if not global_data.player or not global_data.player.logic:
            return
        item = self.panel.list_describe.GetItem(0)
        msg = item.lab_speak_generate.GetString()
        check_code, flag, msg = text_utils.check_review_words_chat(msg)
        if flag != text_utils.CHECK_WORDS_PASS:
            global_data.player.notify_client_message((get_text_by_id(11009),))
            global_data.player.sa_log_forbidden_msg('fight_chat', msg, check_code, hint=3, input_type='shortcut')
            return
        if not self.check_can_send():
            return
        self._last_send_time = time_utility.time()
        global_data.player.logic.send_event('E_SEND_BATTLE_GROUP_MSG', {'text': msg,'is_self_send': True})
        self.close()

    def check_can_send(self):
        MIN_SEND_TIME = self._send_cd
        cur_time = time_utility.time()
        pass_time = cur_time - self._last_send_time
        from logic.gcommon.common_const import ui_operation_const as uoc
        if global_data.player and global_data.player.get_setting_2(uoc.BLOCK_ALL_MSG_KEY):
            return False
        if pass_time < MIN_SEND_TIME:
            global_data.game_mgr.show_tip(get_text_by_id(11008, {'time': str(int(math.ceil(MIN_SEND_TIME - pass_time)))}))
            return False
        return True

    def do_hide_panel(self):
        super(FightTalkUI, self).do_hide_panel()

    def do_show_panel(self):
        super(FightTalkUI, self).do_show_panel()

    def bind_event(self, target):
        pass

    def unbind_event(self, target):
        pass