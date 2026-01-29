# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/Activity202201/ActivitySpringFestivalCalendarMainUI.py
from __future__ import absolute_import
import time
import cc
from common.cfg import confmgr
from common.uisys.basepanel import BasePanel
from common.const.uiconst import NORMAL_LAYER_ZORDER, UI_VKB_CLOSE
from logic.gcommon.common_utils.local_text import get_cur_text_lang, LANG_CN, LANG_ZHTW, LANG_EN, LANG_JA
from logic.comsys.activity.ActivityCalendarBase import ActivityCalendarBase

class ActivitySpringFestivalCalendarMainUI(BasePanel):
    DLG_ZORDER = NORMAL_LAYER_ZORDER
    UI_VKB_TYPE = UI_VKB_CLOSE
    NEED_HIDE_MAIN_UI = False
    PANEL_CONFIG_NAME = 'activity/activity_202201/spring_calendar/activity_spring_calendar'
    UI_ACTION_EVENT = {'btn_close.OnClick': 'close'
       }

    def on_init_panel(self, *args, **kwargs):
        super(ActivitySpringFestivalCalendarMainUI, self).on_init_panel(*args, **kwargs)
        self.calendar_widget = ActivitySpringFestivalCalendarBase(self.panel, self.close)
        self.panel.btn_question.setVisible(False)
        self.hide_main_ui()
        global_data.display_agent.set_longtime_post_process_active('gaussian_blur', True)

    def on_finalize_panel(self):
        self.show_main_ui()
        global_data.display_agent.set_longtime_post_process_active('gaussian_blur', False)


class ActivitySpringFestivalCalendarBase(ActivityCalendarBase):
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
    ACTIVITY_ID = '20602'
    IMG_TAG_OPEN = 'img_tag_open%d'
    IMG_TAG_OVER = 'img_tag_over%d'

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
        btn_item = getattr(self.panel, self.BTN_PREFIX % idx, None)
        if not btn_item:
            return
        else:
            item_info = self.BTN_INFO_LIST[idx]
            name_id = item_info.get('name_id', None)
            activity_id = item_info.get('activity_id', None)
            activity_start_time = item_info.get('activity_start_time', None)
            if not name_id and activity_id:
                name_id = confmgr.get('c_activity_config', activity_id, 'cNameTextID', None)
            lab_name = btn_item.lab_name
            if hasattr(self.panel, self.LAB_NAME % idx):
                lab_name = getattr(self.panel, self.LAB_NAME % idx)
            name_id is not None and lab_name.SetString(name_id)
            date_text = item_info.get('date', None)
            lab_time = btn_item.lab_time
            if hasattr(self.panel, self.LAB_TIME % idx):
                lab_time = getattr(self.panel, self.LAB_TIME % idx)
            date_text is not None and lab_time.SetString(date_text)
            btn_state = self.get_item_state(idx)
            self.init_btn_state_by_idx_new(idx, btn_item, btn_state, activity_start_time)
            alt_pic = item_info.get('pic_path', None)
            img_item = getattr(btn_item, 'img_item', None)
            img_item and alt_pic and img_item.SetDisplayFrameByPath('', alt_pic)
            btn_item.BindMethod('OnClick', lambda btn, touch, idx=idx: self.on_btn_item_clicked(btn, touch, idx))
            return (
             btn_item, item_info)

    def init_btn_state_by_idx_new(self, idx, btn, state, activity_start_time):
        from logic.gutils.activity_utils import ACTIVITY_STATE_END, ACTIVITY_STATE_OPENING, ACTIVITY_STATE_NOT_OPEN
        from logic.gcommon.time_utility import get_delta_days, get_server_time
        lab_time = btn.lab_time
        if hasattr(self.panel, self.LAB_TIME % idx):
            lab_time = getattr(self.panel, self.LAB_TIME % idx)
        img_tag_open = None
        if hasattr(self.panel, self.IMG_TAG_OPEN % idx):
            img_tag_open = getattr(self.panel, self.IMG_TAG_OPEN % idx)
        img_tag_over = None
        if hasattr(self.panel, self.IMG_TAG_OVER % idx):
            img_tag_over = getattr(self.panel, self.IMG_TAG_OVER % idx)
        if state == ACTIVITY_STATE_END:
            lab_time.SetString(601214)
            if img_tag_open is not None:
                img_tag_open.setVisible(False)
            if img_tag_over is not None:
                img_tag_over.setVisible(True)
        elif state == ACTIVITY_STATE_OPENING:
            if img_tag_open is not None:
                img_tag_open.setVisible(True)
            if img_tag_over is not None:
                img_tag_over.setVisible(False)
        elif state == ACTIVITY_STATE_NOT_OPEN:
            if img_tag_open is not None:
                img_tag_open.setVisible(False)
            if img_tag_over is not None:
                img_tag_over.setVisible(False)
            if activity_start_time is not None:
                from logic.gcommon.common_utils.local_text import get_text_by_id
                delta_days = get_delta_days(activity_start_time, get_server_time())
                lab_time.SetString(get_text_by_id(81352).format(delta_days))
        return