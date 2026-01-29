# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/global_event/__init__.py
from __future__ import absolute_import
from common.event.event_base import regist_event
EVENT_LIST = [
 'resolution_changed',
 'resolution_changed_end',
 'avatar_finish_create_event_global']
regist_event(EVENT_LIST)