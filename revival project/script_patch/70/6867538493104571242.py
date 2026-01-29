# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/login/LoginQueueUI.py
from __future__ import absolute_import
import cc
from common.uisys.basepanel import BasePanel
from common.const.uiconst import DIALOG_LAYER_ZORDER, UI_TYPE_CONFIRM, TOP_ZORDER
from logic.gcommon import time_utility as tutil
from common.const import uiconst

class LoginQueueUI(BasePanel):
    PANEL_CONFIG_NAME = 'login/wait_server'
    DLG_ZORDER = DIALOG_LAYER_ZORDER
    IS_FULLSCREEN = True
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    UI_TYPE = UI_TYPE_CONFIRM

    def on_init_panel(self, **kwargs):
        self.init_widget(**kwargs)

    def init_widget(self, **kwargs):
        from logic.gcommon.common_utils.local_text import get_text_by_id

        @self.panel.temp_second_confirm.temp_btn_1.btn_common_big.unique_callback()
        def OnClick(btn, touch):
            on_confirm = kwargs.get('on_confirm', None)
            self.close()
            if on_confirm:
                on_confirm()
            return

        content = kwargs.get('content', None)
        self.panel.lab_time.SetString(content)
        show_content = get_text_by_id(3115, {'time': '%s' % tutil.get_delta_time_str(0)})
        self.panel.lab_wait_time.SetString(show_content)
        self.panel.temp_second_confirm.temp_btn_1.btn_common_big.SetText(19002, None)
        self._tick_count = 0

        def tick():
            self._tick_count += 1
            show_content = get_text_by_id(3115, {'time': '%s' % tutil.get_delta_time_str(self._tick_count)})
            self.panel.lab_wait_time.SetString(show_content)

        seq_action = cc.Sequence.create([cc.DelayTime.create(1), cc.CallFunc.create(tick)])
        repeat_action = cc.RepeatForever.create(seq_action)
        self.panel.runAction(repeat_action)
        return