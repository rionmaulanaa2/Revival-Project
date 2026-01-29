# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/video/VideoListSkip.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
from common.const.uiconst import DIALOG_LAYER_ZORDER, BG_ZORDER
from common.const import uiconst
import time
STATE_NONE = 0
STATE_SKIP = 1

class VideoListSkip(BasePanel):
    PANEL_CONFIG_NAME = 'lobby/video_skip'
    DLG_ZORDER = DIALOG_LAYER_ZORDER
    IS_FULLSCREEN = True
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    UI_ACTION_EVENT = {'btn_skip.OnClick': 'on_confirm',
       'nd_touch.OnClick': 'on_click_bg'
       }

    def on_init_panel(self, *args, **kwargs):
        self._start_time = time.time()
        self._stage = kwargs.get('stage', STATE_NONE)
        self._skip_time = kwargs.get('time', 5)
        self.skip_callback = kwargs.get('skip_cb', None)
        self.panel.btn_skip.setVisible(False)
        self.panel.lab_skip_time.setVisible(False)
        return

    def on_confirm(self, *args):
        if self.skip_callback:
            self.skip_callback()

    def on_cancel(self):
        self._stage = STATE_SKIP

    def on_click_bg(self, *args):
        if self._stage != STATE_NONE:
            return
        self.show_skip_btn()

    def show_skip_btn(self):
        self._stage = STATE_SKIP
        self.panel.btn_skip.setVisible(True)
        self.panel.lab_skip_time.setVisible(False)
        self.panel.nd_touch.setVisible(False)