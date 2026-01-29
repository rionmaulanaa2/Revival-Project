# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivityWinter/ActivityWinterCupAdUI.py
import common.const.uiconst as ui_const
from common.uisys.basepanel import BasePanel

class ActivityWinterCupAdUI(BasePanel):
    PANEL_CONFIG_NAME = 'activity/activity_202312/winter_match/open_winter_match'
    DLG_ZORDER = ui_const.NORMAL_LAYER_ZORDER_1
    UI_VKB_TYPE = ui_const.UI_VKB_NO_EFFECT
    UI_ACTION_EVENT = {'btn_close.OnClick': 'on_close'
       }

    def on_init_panel(self, *args):
        self.panel.PlayAnimation('appear')

        @self.panel.btn_go.unique_callback()
        def OnClick(btn, touch):
            from logic.gutils import jump_to_ui_utils
            from logic.gcommon.common_const.activity_const import ACTIVITY_WINTER_CHAMP_LOGIN
            jump_to_ui_utils.jump_to_activity(ACTIVITY_WINTER_CHAMP_LOGIN)

    def on_close(self, *args):
        self.close()