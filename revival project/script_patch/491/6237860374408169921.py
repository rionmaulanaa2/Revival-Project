# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivityAnnivCalendar.py
from __future__ import absolute_import
import cc
from common.uisys.basepanel import BasePanel
from common.const.uiconst import NORMAL_LAYER_ZORDER, UI_VKB_CLOSE
from logic.comsys.activity.ActivityCalendarBase import ActivityCalendarBase
from logic.gutils.activity_utils import get_activity_open_time

class ActivityAnnivCalendar(BasePanel):
    DLG_ZORDER = NORMAL_LAYER_ZORDER
    UI_VKB_TYPE = UI_VKB_CLOSE
    NEED_HIDE_MAIN_UI = False
    PANEL_CONFIG_NAME = 'activity/activity_202201/anniversary_collection/anniversary_collection'
    UI_ACTION_EVENT = {'temp_btn_close.btn_back.OnClick': 'close'
       }

    def on_init_panel(self, *args, **kwargs):
        super(ActivityAnnivCalendar, self).on_init_panel(*args, **kwargs)
        self.calendar_widget = ActivityAnnivCalendarBase(self.panel)
        self.hide_main_ui()

    def on_finalize_panel(self):
        self.show_main_ui()


class ActivityAnnivCalendarBase(ActivityCalendarBase):
    ACTIVITY_ID = '20523'
    SHARE_TASK_ID = '1440542'
    ND_PREFIX = 'nd_item_%d'
    BTN_PREFIX = 'btn_list_%d'
    BTN_INFO_LIST = {1: {'activity_id': 20520},2: {'activity_id': 20517},3: {'activity_id': 20522},4: {'activity_id': 409},5: {'activity_id': 20519}}

    def __init__(self, panel, jump_cb=None, play_animation=True, accept_event=True):
        self.is_na = G_IS_NA_PROJECT or global_data.channel.is_steam_channel()
        super(ActivityAnnivCalendarBase, self).__init__(panel, jump_cb, play_animation, accept_event)
        start_str, end_str = get_activity_open_time(self.ACTIVITY_ID)
        if start_str and end_str:
            self.panel.lab_time.SetString(get_text_by_id(609202) + '{0}-{1}'.format(start_str, end_str))
        self.enable_share = True
        self.panel.btn_share_img.BindMethod('OnClick', self._share)
        self.panel.nd_cn.setVisible(not self.is_na)
        self.panel.nd_na.setVisible(self.is_na)
        if not self.is_na:
            self.panel.txt_tittle_art.SetDisplayFrameByPath('', 'gui/ui_res_2/txt_pic/text_pic_cn/activity_202201/txt_anniversary_cn.png')

    def init_btn_by_idx(self, idx):
        nd_name = self.ND_PREFIX % idx
        if self.is_na:
            nd_name += '_na'
        nd_item = getattr(self.panel, nd_name, None)
        if not nd_item:
            return
        else:
            btn_item = getattr(nd_item, self.BTN_PREFIX % idx, None)
            if not btn_item:
                return
            item_info = self.BTN_INFO_LIST[idx]
            btn_item.BindMethod('OnClick', lambda btn, touch, idx=idx: self.on_btn_item_clicked(btn, touch, idx))
            return (
             btn_item, item_info)

    def _refresh_share_btn(self, has_shared):
        self.panel.lab_share and self.panel.lab_share.setVisible(has_shared)
        self.panel.lab_share_first and self.panel.lab_share_first.setVisible(not has_shared)

    def _share(self, *args):
        from logic.comsys.share.ActivityAnnivCalendarShareCreator import ActivityAnnivShareCreator
        self.SHARE_CREATOR = ActivityAnnivShareCreator
        super(ActivityAnnivCalendarBase, self)._share()