# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivityFairyland/ActivityFairylandCalendarMainUI.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
from common.const.uiconst import NORMAL_LAYER_ZORDER, UI_VKB_CLOSE
from logic.comsys.activity.ActivityCalendarBase import ActivityCalendarBase

class ActivityFairylandCalendarMainUI(BasePanel):
    DLG_ZORDER = NORMAL_LAYER_ZORDER
    UI_VKB_TYPE = UI_VKB_CLOSE
    NEED_HIDE_MAIN_UI = False
    PANEL_CONFIG_NAME = 'activity/activity_202108/15_calendar/activity_wonderland_calendar_b'
    UI_ACTION_EVENT = {'btn_close.OnClick': 'close'
       }

    def on_init_panel(self, *args, **kwargs):
        super(ActivityFairylandCalendarMainUI, self).on_init_panel(*args, **kwargs)
        self.calendar_widget = ActivityFairylandCalendarBase(self.panel, self.close)
        self.calendar_widget.adjust_title()
        self.hide_main_ui()
        global_data.display_agent.set_longtime_post_process_active('gaussian_blur', True)

    def on_finalize_panel(self):
        self.show_main_ui()
        global_data.display_agent.set_longtime_post_process_active('gaussian_blur', False)


class ActivityFairylandCalendarBase(ActivityCalendarBase):
    BTN_INFO_LIST = {1: {'lottery_id': 25},2: {'activity_id': 20007},3: {'activity_id': 10604},4: {'activity_id': 10605},5: {'activity_id': 10606},6: {'activity_id': 10607},7: {'activity_id': 20006},8: {'activity_id': 10533},9: {'activity_id': 10608},10: {'activity_id': 10609}}
    BTN_INFO_LIST_ALT = {2: {'activity_id': 20007,'pic_path': 'gui/ui_res_2/activity/activity_202108/wonderland/15_calendar/middle/img_yunque_01.png'}}

    def need_alt_btn(self):
        return not G_IS_NA_PROJECT and not global_data.channel.is_steam_channel()

    def play_show_animation(self):
        self.panel.StopAnimation('loop')
        self.panel.RecoverAnimationNodeState('loop')
        self.panel.PlayAnimation('show')
        self.panel.PlayAnimation('loop')

    def init_btn_by_idx(self, idx):
        from logic.gutils.activity_utils import ACTIVITY_STATE_OPENING, ACTIVITY_STATE_END
        btn_item, _ = super(ActivityFairylandCalendarBase, self).init_btn_by_idx(idx)
        btn_state = self.get_item_state(idx)
        btn_item.lab_name.SetColor(1520958 if btn_state == ACTIVITY_STATE_OPENING else 16247738)
        if btn_state == ACTIVITY_STATE_END:
            btn_item.lab_time.SetFontName('gui/fonts/fzdys.ttf')
        show_tip = btn_state == ACTIVITY_STATE_OPENING
        btn_item.img_tips.setVisible(show_tip)
        btn_item.img_bar.setVisible(btn_state != ACTIVITY_STATE_OPENING)
        btn_item.img_bar_in.setVisible(btn_state == ACTIVITY_STATE_OPENING)