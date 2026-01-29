# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/test/LogPanelUI.py
from __future__ import absolute_import
from six.moves import range
from common.uisys.basepanel import BasePanel
from common.const.uiconst import SCREEN_LOCKER_ZORDER
import time
from common.const import uiconst

class LogPanelUI(BasePanel):
    DLG_ZORDER = SCREEN_LOCKER_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    PANEL_CONFIG_NAME = 'test/log_panel'
    GLOBAL_EVENT = {'add_log_to_log_panel': 'add_log'
       }

    def on_init_panel(self):
        self.panel.sv_log.SetInitCount(20)
        self._log_list = []

    def refresh_log(self):
        count = self.panel.sv_log.GetItemCount()
        for i in range(count):
            index = count - i - 1
            ui_item = self.panel.sv_log.GetItem(index)
            if i < len(self._log_list):
                txt = self._log_list[0 - i - 1]
            else:
                txt = ''
            ui_item.txt.SetString(txt)
            ui_item.setOpacity(255)
            ui_item.txt.setOpacity(255)

    def add_log(self, txt, need_time_stamp=True):
        if need_time_stamp:
            import datetime
            t = datetime.datetime.now()
            time_stamp_str = str(t)
            txt = time_stamp_str[14:23] + ': ' + txt
        self._log_list.append(txt)
        if len(self._log_list) > 30:
            self._log_list.pop(0)
        self.refresh_log()