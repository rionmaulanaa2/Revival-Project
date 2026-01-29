# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/message/ChannelSettingUI.py
from __future__ import absolute_import
import common.utilities
from common.const.property_const import *
from logic.comsys.common_ui.WindowSmallBase import WindowSmallBase
from common.platform import channel_const
from common.const.uiconst import NORMAL_LAYER_ZORDER
import logic.gcommon.const as const
from logic.gcommon.common_const import friend_const
from logic.gcommon.common_utils.local_text import get_text_by_id
from cocosui import cc, ccui, ccs

class ChannelSettingUI(WindowSmallBase):
    PANEL_CONFIG_NAME = 'friend/platform_set'
    TEMPLATE_NODE_NAME = 'temp_bg'
    DLG_ZORDER = NORMAL_LAYER_ZORDER

    def on_init_panel(self, *args, **kargs):
        super(ChannelSettingUI, self).on_init_panel(*args, **kargs)
        self._line_enable_init = global_data.player.is_social_enable(friend_const.SOCIAL_ID_TYPE_LINEGAME)
        self._line_enable = self._line_enable_init
        check_line = self.panel.check_line
        visible = global_data.channel.is_bind_linegame()
        check_line.setVisible(visible)
        enable = []

        @check_line.callback()
        def OnClick(*args):
            self._line_enable = not self._line_enable
            check_line.checkbox.SetSelect(self._line_enable)

        check_line.checkbox.SetSelect(self._line_enable)

    def on_finalize_panel(self):
        if self._line_enable_init != self._line_enable and global_data.player:
            if self._line_enable:
                global_data.player.request_enable_social(friend_const.SOCIAL_ID_TYPE_LINEGAME)
            else:
                global_data.player.request_disable_social(friend_const.SOCIAL_ID_TYPE_LINEGAME)