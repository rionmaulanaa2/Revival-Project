# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gevent/teammate_event.py
from __future__ import absolute_import
from common.event.event_base import regist_event
EVENT_LIST = [
 'teammate_control_target_change_event',
 'team_invite_count_down_event',
 'close_simple_inf_ui',
 'teammate_on_fire',
 'on_teammate_global_join_mecha',
 'on_teammate_global_leave_mecha',
 'on_teammate_global_add_emoji',
 'on_teammate_global_remove_emoji']
regist_event(EVENT_LIST)