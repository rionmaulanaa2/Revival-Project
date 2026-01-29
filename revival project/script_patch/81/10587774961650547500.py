# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivityPinganjing/ActivityPinganjingCalendarMainUI.py
from __future__ import absolute_import
import time
import cc
from common.cfg import confmgr
from common.uisys.basepanel import BasePanel
from common.const.uiconst import NORMAL_LAYER_ZORDER, UI_VKB_CLOSE
from logic.gcommon.common_utils.local_text import get_cur_text_lang, LANG_CN, LANG_ZHTW, LANG_EN, LANG_JA
from logic.comsys.activity.ActivityCalendarBase import ActivityCalendarBase, ACTIVITY_STATE_END, ACTIVITY_STATE_OPENING, ACTIVITY_STATE_NOT_OPEN

class ActivityPinganjingCalendarMainUI(ActivityCalendarBase):
    ACTIVITY_ID = '21183'

    def init_panel(self):
        super(ActivityPinganjingCalendarMainUI, self).init_panel()

    def need_alt_btn(self):
        return G_IS_NA_PROJECT

    def play_show_animation(self):
        super(ActivityPinganjingCalendarMainUI, self).play_show_animation()
        self.panel.PlayAnimation('loop')
        temp_head = self.panel.temp_head
        if temp_head:
            temp_head.PlayAnimation('show_head')

    def on_btn_item_clicked(self, btn, touch, idx):
        super(ActivityPinganjingCalendarMainUI, self).on_btn_item_clicked(btn, touch, idx)

    def init_btn_by_idx(self, idx):
        super(ActivityPinganjingCalendarMainUI, self).init_btn_by_idx(idx)
        btn_item = getattr(self.panel, self.BTN_PREFIX % idx, None)
        if not btn_item:
            return
        else:
            item_info = self.BTN_INFO_LIST[idx]
            alt_pic = item_info.get('pic_path', None)
            img_item = getattr(self.panel, 'img_item%d' % idx, None)
            img_item and alt_pic and img_item.SetDisplayFrameByPath('', alt_pic)
            return

    def init_btn_state_by_idx(self, idx, btn, state):
        show = True
        tag_open = getattr(self.panel, 'img_tag_open%d' % idx)
        tag_open and tag_open.setVisible(show and state == ACTIVITY_STATE_OPENING)
        tag_over = getattr(self.panel, 'img_tag_over%d' % idx)
        tag_over and tag_over.setVisible(show and state == ACTIVITY_STATE_END)