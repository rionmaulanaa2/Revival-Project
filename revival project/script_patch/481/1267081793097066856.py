# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gevent/koth_event.py
from __future__ import absolute_import
from common.event.event_base import regist_event
EVENT_LIST = [
 'update_koth_money_info_event',
 'update_koth_bullet_cd_info_event',
 'on_enter_king_camp_event',
 'on_leave_king_camp_event',
 'update_koth_praised_num_event']
regist_event(EVENT_LIST)