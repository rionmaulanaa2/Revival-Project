# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/chat/JudgeDanmuWidget.py
from __future__ import absolute_import
from logic.comsys.common_ui.InputBox import InputBox
from logic.gcommon.common_utils import text_utils
from logic.gcommon.common_utils.local_text import get_text_by_id
import time
import math

class JudgeDanmuWidget(object):
    SEND_CD = 5.0

    def __init__(self, nd_danmu):
        self.panel = nd_danmu
        self.last_send_time = 0
        self.init_buttons()
        self.init_input_box()

    def destroy(self):
        pass

    def init_input_box(self):
        self.input_box = InputBox(self.panel.input_box, max_length=20, placeholder=get_text_by_id(15816), send_callback=self.on_edit_box_send_callback, input_callback=self.on_edit_box_changed_callback)

    def init_buttons(self):

        @self.panel.btn_send.unique_callback()
        def OnClick(*args):
            self.on_click_btn_send()

        @self.panel.bg_layer.unique_callback()
        def OnClick(*args):
            self.on_click_bg_layer()

        @self.panel.btn_confirm.unique_callback()
        def OnClick(*args):
            self.on_click_btn_confirm()

    def on_click_btn_send(self, *args):
        cur_visible = self.panel.nd_input.isVisible()
        self.panel.nd_input.setVisible(not cur_visible)

    def on_click_bg_layer(self, *args):
        self.panel.nd_input.setVisible(False)

    def on_click_btn_confirm(self, *args):
        self.on_edit_box_send_callback()

    def on_edit_box_send_callback(self, *args):
        from logic.gutils.judge_utils import is_ob
        player = global_data.player
        if not player:
            return
        if not is_ob():
            return
        msg = self.input_box.get_text()
        if not msg:
            return
        cur_time = time.time()
        delta_time = cur_time - self.last_send_time
        if delta_time < self.SEND_CD:
            global_data.game_mgr.show_tip(get_text_by_id(11008, {'time': int(self.SEND_CD - delta_time)}))
            return
        self.last_send_time = cur_time
        check_code, flag, msg = text_utils.check_review_words_chat(msg)
        if flag != text_utils.CHECK_WORDS_PASS:
            global_data.player.notify_client_message((get_text_by_id(11009),))
            return
        color_msg = '#SR {} {} #n'.format(get_text_by_id(19214), msg)
        player.call_server_method('ob_send_battle_message', (color_msg,))
        self.input_box.set_text('')

    def on_edit_box_changed_callback(self, text):
        if text.endswith('\n') or text.endswith('\r'):
            text = text.rstrip('\n')
            text = text.rstrip('\r')
            self.input_box.set_text(text)
            self.input_box.detachWithIME()