# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivityNewRole.py
from __future__ import absolute_import
from common.cfg import confmgr
from logic.comsys.activity.ActivityTemplate import ActivityBase
from common.cinematic.VideoPlayer import VideoPlayer
from logic.gutils.template_utils import init_price_view
from logic.client.const.mall_const import DARK_PRICE_COLOR
from logic.gutils.item_utils import get_lobby_item_name
from logic.gutils import jump_to_ui_utils
from logic.gcommon import time_utility as tutil
from logic.gutils.mall_utils import is_valid_goods
from logic.gcommon.common_utils.local_text import get_cur_text_lang, LANG_CN, LANG_ZHTW, LANG_EN, LANG_JA
import cc
from logic.gutils import advance_utils
money_icon_scale = 0.8

class ActivityNewRole(ActivityBase):
    VIDEO_PATH = None

    def on_init_panel(self):
        self.set_package_content()
        appear_anim = 'show'
        self.panel.runAction(cc.Sequence.create([
         cc.CallFunc.create(lambda : self.panel.nd_template.PlayAnimation(appear_anim)),
         cc.DelayTime.create(self.panel.nd_template.GetAnimationMaxRunTime(appear_anim)),
         cc.CallFunc.create(lambda : self.panel.nd_template.PlayAnimation('loop'))]))
        self.process_event(True)
        self._need_bg = False
        self.play_video()

    def on_finalize_panel(self):
        self.process_event(False)
        VideoPlayer().stop_video()

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'on_lobby_bag_item_changed_event': self.set_package_content
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def set_package_content(self):
        if self.VIDEO_PATH:
            advance_utils.set_new_role(self.panel.nd_template, self._activity_type, has_video=True)
        else:
            advance_utils.set_new_role(self.panel.nd_template, self._activity_type, has_video=False)

    def play_video(self):
        if self.VIDEO_PATH:
            VideoPlayer().play_video(self.VIDEO_PATH, None, {}, repeat_time=0, bg_play=True)
        return

    def refresh_panel(self):
        super(ActivityNewRole, self).refresh_panel()
        if self.VIDEO_PATH:
            VideoPlayer().play_video(self.VIDEO_PATH, None, {}, repeat_time=0, bg_play=True)
        return