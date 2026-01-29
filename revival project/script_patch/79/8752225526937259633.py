# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivityAIConcert/ActivityAIConcertCalendarMainUI.py
from __future__ import absolute_import
import cc
from common.cfg import confmgr
from common.uisys.basepanel import BasePanel
from common.const.uiconst import NORMAL_LAYER_ZORDER, UI_VKB_CLOSE
from logic.gcommon.common_utils.local_text import get_cur_text_lang, LANG_CN, LANG_ZHTW, LANG_EN, LANG_JA
from logic.comsys.activity.ActivityCalendarBase import ActivityCalendarBase, ACTIVITY_STATE_OPENING, ACTIVITY_STATE_NOT_OPEN, ACTIVITY_STATE_END
from logic.gcommon.time_utility import get_server_time

class ActivityAIConcertCalendarMainUI(BasePanel):
    DLG_ZORDER = NORMAL_LAYER_ZORDER
    UI_VKB_TYPE = UI_VKB_CLOSE
    NEED_HIDE_MAIN_UI = False
    PANEL_CONFIG_NAME = 'activity/activity_202109/kizuna/calendar/activity_kizuna_calendar'
    UI_ACTION_EVENT = {'btn_close.OnClick': 'close'
       }

    def on_init_panel(self, *args, **kwargs):
        super(ActivityAIConcertCalendarMainUI, self).on_init_panel(*args, **kwargs)
        self.calendar_widget = ActivityAIConcertCalendarBase(self.panel)
        self.hide_main_ui()
        global_data.display_agent.set_longtime_post_process_active('gaussian_blur', True)

    def on_finalize_panel(self):
        self.show_main_ui()
        global_data.display_agent.set_longtime_post_process_active('gaussian_blur', False)


class ActivityAIConcertCalendarBase(ActivityCalendarBase):
    ACTIVITY_ID = '20218'

    def need_alt_btn(self):
        return global_data.is_pc_mode or G_IS_NA_PROJECT

    def init_btn_by_idx(self, idx):
        super(ActivityAIConcertCalendarBase, self).init_btn_by_idx(idx)
        if idx == 1:
            lab_time = getattr(self.panel, 'lab_time1')
            lab_time and lab_time.SetString(610024 if get_server_time() < 1634400000 else 610025)
        item_info = self.BTN_INFO_LIST[idx]
        alt_pic = item_info.get('pic_path', None)
        img_item = getattr(self.panel, 'img_item%d' % idx, None)
        img_item and alt_pic and img_item.SetDisplayFrameByPath('', alt_pic)
        return

    def play_show_animation(self):
        self.panel.StopAnimation('loop')
        self.panel.StopAnimation('loop_02')
        self.panel.StopAnimation('loop_line')
        self.panel.RecoverAnimationNodeState('loop')
        self.panel.RecoverAnimationNodeState('loop_02')
        self.panel.RecoverAnimationNodeState('loop_line')
        self.panel.runAction(cc.Sequence.create([
         cc.CallFunc.create(lambda : self.panel.PlayAnimation('show')),
         cc.CallFunc.create(lambda : self.panel.PlayAnimation('loop_line')),
         cc.DelayTime.create(1.3),
         cc.CallFunc.create(lambda : self.panel.PlayAnimation('loop')),
         cc.DelayTime.create(0.7),
         cc.CallFunc.create(lambda : self.panel.PlayAnimation('loop_02'))]))

    def init_btn_state_by_idx(self, idx, btn, state):
        getattr(self.panel, 'img_tag_open%d' % idx).setVisible(state == ACTIVITY_STATE_OPENING)
        getattr(self.panel, 'img_tag_over%d' % idx).setVisible(state == ACTIVITY_STATE_END)

    def on_btn_item_clicked(self, btn, touch, idx):
        if idx == 1:
            cur_time = get_server_time()
            time_zone = [1634384100, 1634387700, 1634470500, 1634474100]
            text_id = time_zone[0] < cur_time < time_zone[1] or (610075 if time_zone[2] < cur_time < time_zone[3] else 10063)
            global_data.game_mgr.show_tip(get_text_by_id(text_id))
        else:
            super(ActivityAIConcertCalendarBase, self).on_btn_item_clicked(btn, touch, idx)