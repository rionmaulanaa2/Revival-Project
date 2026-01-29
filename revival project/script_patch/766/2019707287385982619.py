# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/chat/ChatRecord.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
import time
import common.const.uiconst
from cocosui import cc, ccui, ccs
from common.const.property_const import *
from common.cfg import confmgr
import common.utils.timer as timer
import time
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gutils import chat_utils
RECORD_MAX_TIME = 60.0
from common.const import uiconst

class ChatRecord(BasePanel):
    DLG_ZORDER = common.const.uiconst.DIALOG_LAYER_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    PANEL_CONFIG_NAME = 'chat/voice_record'
    UI_TYPE = common.const.uiconst.UI_TYPE_CONFIRM

    def on_init_panel(self, *args, **kargs):
        self.panel.PlayAnimation('voice_record')
        self.timeout_callback = None
        self.touch_in_btn_area = True
        self.select = None
        self._start_time = time.time()
        self._timer = global_data.game_mgr.register_logic_timer(self.on_timer, interval=1, times=-1, mode=timer.CLOCK)
        show_time = int(RECORD_MAX_TIME - (time.time() - self._start_time))
        self.refresh_time(show_time)
        return

    def on_finalize_panel(self):
        if self._timer:
            global_data.game_mgr.unregister_logic_timer(self._timer)
            self._timer = None
        return

    def set_timeout_callback(self, callback):
        self.timeout_callback = callback

    def set_select(self, select):
        if self.select != select:
            self.select = select
            self.show_record()

    def get_select(self):
        return self.select

    def show_record(self):
        if not self.panel:
            return
        show_record = self.select == chat_utils.VOICE_STATUS_RECORD
        show_cancel = not show_record
        self.panel.img_voice.setVisible(show_record)
        self.panel.img_bowen1_right.setVisible(show_record)
        self.panel.img_bowen1_left.setVisible(show_record)
        self.panel.img_bowen2_right.setVisible(show_record)
        self.panel.img_bowen2_left.setVisible(show_record)
        self.panel.img_bowen3_right.setVisible(show_record)
        self.panel.img_bowen3_left.setVisible(show_record)
        self.panel.img_cancel.setVisible(show_cancel)
        if show_record:
            self.panel.lab_tips.SetString(get_text_by_id(2134))
        else:
            self.panel.lab_tips.SetString(get_text_by_id(2135))

    def on_timer(self, *args):
        show_time = int(RECORD_MAX_TIME - (time.time() - self._start_time))
        self.refresh_time(show_time)
        if show_time <= 0:
            if self.timeout_callback:
                self.timeout_callback()
            self.close()

    def refresh_time(self, show_time):
        if show_time <= 10:
            self.panel.lab_time.setVisible(True)
            self.panel.lab_time.SetString(get_text_by_id(2136).format(show_time))
        else:
            self.panel.lab_time.setVisible(False)

    def on_drag_voice_btn(self, start_pos, end_pos):
        import logic.gcommon.const as g_const
        r_spr = (end_pos.x - start_pos.x) ** 2 + (end_pos.y - start_pos.y) ** 2
        cur_select = chat_utils.VOICE_STATUS_RECORD
        touch_in_btn_area = r_spr <= g_const.G_SOUND_RECORD_RADIUS_SPR
        if not touch_in_btn_area:
            cur_select = chat_utils.VOICE_STATUS_CANCEL
        self.set_select(cur_select)