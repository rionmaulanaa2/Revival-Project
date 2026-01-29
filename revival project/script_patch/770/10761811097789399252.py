# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/KizunaAITeachingStepsUI.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
from common.const.uiconst import NORMAL_LAYER_ZORDER_2, UI_VKB_CLOSE

class KizunaAITeachingStepsUI(BasePanel):
    PANEL_CONFIG_NAME = 'activity/activity_202109/kizuna/new_player/i_activity_community_kizuna'
    DLG_ZORDER = NORMAL_LAYER_ZORDER_2
    UI_VKB_TYPE = UI_VKB_CLOSE
    UI_ACTION_EVENT = {'nd_close.OnClick': 'on_click_nd_close'
       }

    def on_init_panel(self):
        self.panel.PlayAnimation('appear')

    def on_click_nd_close(self, *args):
        self.close()