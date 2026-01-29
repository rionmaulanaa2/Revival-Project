# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/common/event/input_event.py
from __future__ import absolute_import
from common.event.event_base import regist_event
EVENT_LIST = [
 'hot_key_swtich_on_event',
 'hot_key_swtich_off_event',
 'hot_key_conf_refresh_event',
 'touch_pixel_rotate_camera_event',
 'touch_pixel_rotate_other_event',
 'textfield_eventtype_attach_with_ime_event',
 'textfield_eventtype_detach_with_ime_event']
regist_event(EVENT_LIST)