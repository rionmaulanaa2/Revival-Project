# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gevent/visit_event.py
from __future__ import absolute_import
from common.event.event_base import regist_event
EVENT_LIST = [
 'visit_player_add_teammate_event',
 'visit_player_del_teammate_event',
 'visit_player_teammate_info_update_event',
 'refresh_visit_player_info_event',
 'visit_place_change_event']
regist_event(EVENT_LIST)