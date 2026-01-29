# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/common/event/app_event.py
from __future__ import absolute_import
from .event_base import regist_event
EVENT_LIST = [
 'app_resume_event',
 'app_pause_event',
 'app_background_event',
 'app_exit_event',
 'app_lost_focus_event',
 'app_3d_touch_switch_event',
 'app_frame_rate_changed_event',
 'app_change_focus']
regist_event(EVENT_LIST)