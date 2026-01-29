# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivityRedCliff/ActivityRedCliffCalendarMainUI.py
from __future__ import absolute_import
import time
import cc
from common.cfg import confmgr
from common.uisys.basepanel import BasePanel
from common.const.uiconst import NORMAL_LAYER_ZORDER, UI_VKB_CLOSE
from logic.gcommon.common_utils.local_text import get_cur_text_lang, LANG_CN, LANG_ZHTW, LANG_EN, LANG_JA
from logic.comsys.activity.ActivityCalendarBase import ActivityCalendarBase

class ActivityRedCliffCalendarMainUI(BasePanel):
    DLG_ZORDER = NORMAL_LAYER_ZORDER
    UI_VKB_TYPE = UI_VKB_CLOSE
    NEED_HIDE_MAIN_UI = False
    PANEL_CONFIG_NAME = 'activity/activity_202203/red_cliff/calendar/open_red_cliff_calendar'
    UI_ACTION_EVENT = {'btn_close.OnClick': 'close'
       }

    def on_init_panel(self, *args, **kwargs):
        super(ActivityRedCliffCalendarMainUI, self).on_init_panel(*args, **kwargs)
        self.calendar_widget = ActivityRedCliffCalendarBase(self.panel)
        self.hide_main_ui()

    def on_finalize_panel(self):
        self.show_main_ui()


class ActivityRedCliffCalendarBase(ActivityCalendarBase):
    ACTIVITY_ID = '20701'

    def init_panel(self):
        super(ActivityRedCliffCalendarBase, self).init_panel()
        if self.need_alt_btn():
            self.panel.img_item7.SetDisplayFrameByPath('', 'gui/ui_res_2/activity/activity_202203/red_cliff/calendar/item7/img_red_cliff_calendar_item7_2.png')

    def need_alt_btn(self):
        return G_IS_NA_PROJECT or global_data.channel.is_steam_channel()

    def play_show_animation(self):
        super(ActivityRedCliffCalendarBase, self).play_show_animation()
        self.panel.PlayAnimation('loop')
        self.panel.img_item6.PlayAnimation('show_head')