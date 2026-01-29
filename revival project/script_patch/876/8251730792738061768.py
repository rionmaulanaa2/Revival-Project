# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/common_ui/MouseLockerUI.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
from common.const.uiconst import SCREEN_LOCKER_ZORDER, UI_TYPE_NO_RELEASE
from common.const import uiconst

class MouseLockerUI(BasePanel):
    PANEL_CONFIG_NAME = 'common/screen_locker'
    DLG_ZORDER = SCREEN_LOCKER_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    UI_TYPE = UI_TYPE_NO_RELEASE

    def on_init_panel(self, is_auto_unlocker=False, auto_unlocker_time=10):
        self._lock_timer = None
        if is_auto_unlocker:
            self._lock_timer = self.panel.SetTimeOut(auto_unlocker_time, self.close)
        if global_data.is_inner_server and not global_data.is_pc_mode:
            pass
        return

    def reset_lock_time(self, auto_unlocker_time=10):
        if self._lock_timer:
            self.panel.stopAction(self._lock_timer)
        self._lock_timer = self.panel.SetTimeOut(auto_unlocker_time, self.close)