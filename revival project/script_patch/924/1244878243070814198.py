# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/message/FriendEmpty.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
import common.const.uiconst
from common.const import uiconst

class FriendEmpty(BasePanel):
    PANEL_CONFIG_NAME = 'message/friend_empty'
    DLG_ZORDER = common.const.uiconst.NORMAL_LAYER_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT

    def on_init_panel(self, *args, **kargs):
        self.panel.PlayAnimation('appear')

    def on_finalize_panel(self):
        pass

    def set_visible(self, visible):
        self.panel.setVisible(visible)