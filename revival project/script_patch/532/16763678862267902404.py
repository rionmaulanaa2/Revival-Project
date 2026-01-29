# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/common/event/keyboard_event.py
from __future__ import absolute_import
from .event_base import regist_event
EVENT_LIST = [
 'kb_on_vkb_event',
 'kb_on_will_vkb_event']
regist_event(EVENT_LIST)