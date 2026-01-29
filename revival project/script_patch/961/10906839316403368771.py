# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/chat/ChatVoice.py
from __future__ import absolute_import
import time
from common.uisys.basepanel import BasePanel
import common.const.uiconst as uiconst
import common.utils.timer as timer
from logic.gutils import chat_utils
RECORED_MAX_TIME = 60.0

class ChatVoice(BasePanel):
    PANEL_CONFIG_NAME = 'chat/chat_voice'
    DLG_ZORDER = uiconst.DIALOG_LAYER_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    UI_TYPE = uiconst.UI_TYPE_CONFIRM

    def on_init_panel(self, *args, **kwargs):
        self.timeout_callback = None
        self.select = None
        self._voice_record_start = time.time()
        self._voice_record_timer = global_data.game_mgr.register_logic_timer(self.on_timer, interval=0.1, times=-1, mode=timer.CLOCK)
        self.progress = 0
        self.progress_delta = 1
        show_time = self.get_left_time()
        self.refresh_time(show_time)
        return

    def on_finalize_panel(self):
        if self._voice_record_timer:
            global_data.game_mgr.unregister_logic_timer(self._voice_record_timer)
            self._voice_record_timer = None
        return

    def set_timeout_callback(self, callback):
        self.timeout_callback = callback

    def set_select(self, select):
        if self.select != select:
            self.select = select
            self.refresh_ui()

    def get_select(self):
        return self.select

    def get_left_time(self):
        return int(RECORED_MAX_TIME - (time.time() - self._voice_record_start))

    def on_timer(self, *args):
        left_time = self.get_left_time()
        self.refresh_time(left_time)
        self.refresh_progress()
        if left_time <= 0:
            if self.timeout_callback:
                self.timeout_callback(self.select)
            self.close()

    def refresh_time(self, show_time):
        if show_time < 10:
            self.panel.img_mic.setVisible(False)
            self.panel.nd_num.setVisible(True)
            self.panel.nd_num.txt_num.setString(str(show_time))
        else:
            self.panel.img_mic.setVisible(True)
            self.panel.nd_num.setVisible(False)

    def refresh_progress(self):
        self.progress = self.progress + self.progress_delta
        self.panel.prog_record.setPercentage(self.progress * 10)
        if self.progress >= 10:
            self.progress_delta = -1
        if self.progress <= 0:
            self.progress_delta = 1

    def refresh_ui(self):
        if not self.panel:
            return
        if self.select == chat_utils.VOICE_STATUS_RECORD:
            self.panel.nd_slide.setVisible(False)
            self.panel.txt_slide.SetString(11087)
        else:
            self.panel.nd_slide.setVisible(True)
            if self.select == chat_utils.VOICE_STATUS_TRANSLATE:
                self.panel.btn_charge.SetSelect(True)
                self.panel.btn_cancel.SetSelect(False)
                self.panel.txt_slide.SetString(11106)
            else:
                self.panel.btn_charge.SetSelect(False)
                self.panel.btn_cancel.SetSelect(True)
                self.panel.txt_slide.SetString(11105)

    def on_drag_voice_btn(self, start_pos, end_pos):
        if not self.panel:
            return
        import logic.gcommon.const as g_const
        cur_select = chat_utils.VOICE_STATUS_RECORD
        nd_1_y = self.panel.nd_1.ConvertToWorldSpacePercentage(0, 100).y
        if end_pos.y > nd_1_y:
            cur_select = chat_utils.VOICE_STATUS_CANCEL
            if end_pos.x > start_pos.x + g_const.G_SOUND_TRANSLATE_RIGHT_MOVE_DIST:
                cur_select = chat_utils.VOICE_STATUS_TRANSLATE
        self.set_select(cur_select)