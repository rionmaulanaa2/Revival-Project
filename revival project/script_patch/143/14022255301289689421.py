# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivitySummer/ActivitySummerCalendarMainUI.py
from __future__ import absolute_import
import cc
from common.uisys.basepanel import BasePanel
from common.const.uiconst import NORMAL_LAYER_ZORDER, UI_VKB_CLOSE
from logic.gcommon.common_utils.local_text import get_cur_text_lang, LANG_CN, LANG_ZHTW, LANG_EN, LANG_JA
from logic.comsys.activity.ActivityCalendarBase import ActivityCalendarBase

class ActivitySummerCalendarMainUI(BasePanel):
    DLG_ZORDER = NORMAL_LAYER_ZORDER
    UI_VKB_TYPE = UI_VKB_CLOSE
    NEED_HIDE_MAIN_UI = False
    PANEL_CONFIG_NAME = 'activity/activity_202107/calendar/activity_summer_calendar'
    UI_ACTION_EVENT = {'btn_close.OnClick': 'close'
       }

    def on_init_panel(self, *args, **kwargs):
        super(ActivitySummerCalendarMainUI, self).on_init_panel(*args, **kwargs)
        self.calendar_widget = ActivitySummerCalendarBase(self.panel, self.close)
        self.calendar_widget.adjust_title()
        self.hide_main_ui()
        global_data.display_agent.set_longtime_post_process_active('gaussian_blur', True)

    def on_finalize_panel(self):
        self.show_main_ui()
        global_data.display_agent.set_longtime_post_process_active('gaussian_blur', False)


class ActivitySummerCalendarBase(ActivityCalendarBase):
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
    BTN_INFO_LIST = {1: {'lottery_id': 24,'name_id': 609687,'date': '07.29-09.02'},2: {'activity_id': 10527,'name_id': 609684,'date': '07.29-08.12'},3: {'activity_id': 10329,'name_id': 609678,'date': '07.08-07.29','hide_tip_timestamp': 1627506000},4: {'activity_id': 10526,'name_id': 609682,'date': '07.22-08.12'},5: {'activity_id': 10525,'name_id': 609681,'date': '07.15-07.29'},6: {'activity_id': 10520,'name_id': 609676,'date': '07.08-07.21'},7: {'activity_id': 10530,'name_id': 609685,'date': '07.29-08.12'},8: {'activity_id': 10524,'name_id': 609680,'date': '07.15-07.29'},9: {'activity_id': 10534,'name_id': 609679,'date': '07.15-08.05','hide_tip_timestamp': 1628110800}}
    BTN_INFO_LIST_ALT = {5: {'activity_id': None,'name_id': 609677,'date': ''},9: {'activity_id': 10532,'name_id': 609683,'date': '07.22-08.05'}}

    def need_alt_btn(self):
        return G_IS_NA_PROJECT or global_data.is_pc_mode

    def play_show_animation(self):
        self.panel.img_bg.setVisible(True)
        self.panel.nd_content.setVisible(False)
        self.panel.vx.setVisible(False)
        self.panel.StopAnimation('loop')
        self.panel.StopAnimation('loop_02')
        self.panel.RecoverAnimationNodeState('loop')
        self.panel.RecoverAnimationNodeState('loop_02')
        self.panel.PlayAnimation('show')
        act = cc.Sequence.create([
         cc.DelayTime.create(1.7),
         cc.CallFunc.create(lambda : self.panel.PlayAnimation('loop')),
         cc.DelayTime.create(0.3),
         cc.CallFunc.create(lambda : self.panel.PlayAnimation('loop_02'))])
        self.panel.runAction(act)

    def init_btn_by_idx(self, idx):
        from logic.gutils.activity_utils import get_activity_state, get_lottery_state, ACTIVITY_STATE_OPENING
        from logic.gcommon.time_utility import get_server_time
        btn_item, item_info = super(ActivitySummerCalendarBase, self).init_btn_by_idx(idx)
        show_tip = self.get_item_state(idx) == ACTIVITY_STATE_OPENING
        if show_tip and item_info.get('hide_tip_timestamp', None):
            show_tip = get_server_time() <= item_info['hide_tip_timestamp']
        btn_item.img_tips.setVisible(show_tip)
        return

    def adjust_title(self):
        cur_lang = get_cur_text_lang()
        if cur_lang in self.TITLE_POS:
            pos = self.TITLE_POS[cur_lang]
            self.panel.txt_title.SetPosition(pos[0], pos[1])
            pos = self.TITLE_LIGHT_POS[cur_lang]
            self.panel.img_light_title.SetPosition(pos[0], pos[1])

    def on_btn_item_clicked(self, btn, touch, item_idx):
        if self.use_btn_info_alt and item_idx == 5:
            global_data.game_mgr.show_tip(get_text_by_id(609770))
            return
        super(ActivitySummerCalendarBase, self).on_btn_item_clicked(btn, touch, item_idx)