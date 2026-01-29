# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/common/event/login_event.py
from __future__ import absolute_import
from common.event.event_base import regist_event
EVENT_LIST = [
 'login_scene_prepared_signal',
 'on_request_login_event',
 'on_login_success_event',
 'on_login_failed_event',
 'check_first_choosing_svr_event',
 'on_login_sdk_success_event',
 'guest_login_state_changed',
 'on_login_enter_lobby',
 'on_new_user_setting']
regist_event(EVENT_LIST)