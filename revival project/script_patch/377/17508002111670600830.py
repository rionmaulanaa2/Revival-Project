# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivityChristmas/ActivityChristmasCalendarMainUI.py
from __future__ import absolute_import
import cc
from common.uisys.basepanel import BasePanel
from common.const.uiconst import NORMAL_LAYER_ZORDER, UI_VKB_CLOSE
from logic.gcommon.common_utils.local_text import get_cur_text_lang, LANG_CN, LANG_ZHTW, LANG_EN, LANG_JA
from logic.comsys.activity.ActivityCalendarBase import ActivityCalendarBase

class ActivityChristmasCalendarMainUI(BasePanel):
    DLG_ZORDER = NORMAL_LAYER_ZORDER
    UI_VKB_TYPE = UI_VKB_CLOSE
    NEED_HIDE_MAIN_UI = False
    PANEL_CONFIG_NAME = 'activity/activity_202112/christmas/calendar/activity_christmas_calendar'
    UI_ACTION_EVENT = {'btn_close.OnClick': 'close'
       }

    def on_init_panel(self, *args, **kwargs):
        super(ActivityChristmasCalendarMainUI, self).on_init_panel(*args, **kwargs)
        self.calendar_widget = ActivityChristmasCalendarBase(self.panel, self.close)
        self.hide_main_ui()
        global_data.display_agent.set_longtime_post_process_active('gaussian_blur', True)

    def on_finalize_panel(self):
        self.show_main_ui()
        global_data.display_agent.set_longtime_post_process_active('gaussian_blur', False)


class ActivityChristmasCalendarBase(ActivityCalendarBase):
    TITLE_POS = {LANG_CN: ('50%145', '50%266'),
       LANG_ZHTW: ('50%145', '50%266'),
       LANG_EN: ('50%16', '50%266'),
       LANG_JA: ('50%-12', '50%266')
       }
    TITLE_LIGHT_POS = {LANG_CN: ('50%-152', '50%-26'),
       LANG_ZHTW: ('50%-152', '50%-26'),
       LANG_EN: ('50%0', '50%-26'),
       LANG_JA: ('50%0', '50%-26')
       }
    ACTIVITY_ID = '20503'

    def play_show_animation(self):
        self.panel.StopAnimation('loop')
        self.panel.StopAnimation('loop_02')
        self.panel.RecoverAnimationNodeState('loop')
        self.panel.RecoverAnimationNodeState('loop_02')
        self.panel.PlayAnimation('show')
        self.panel.PlayAnimation('loop')
        act = cc.Sequence.create([
         cc.DelayTime.create(1.9),
         cc.CallFunc.create(lambda : self.panel.PlayAnimation('loop_02'))])
        self.panel.runAction(act)

    def init_btn_by_idx(self, idx):
        from logic.gutils.activity_utils import get_activity_state, get_lottery_state, ACTIVITY_STATE_OPENING
        from logic.gcommon.time_utility import get_server_time
        btn_item, item_info = super(ActivityChristmasCalendarBase, self).init_btn_by_idx(idx)