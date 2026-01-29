# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gevent/artcheck_event.py
from __future__ import absolute_import
from common.event.event_base import regist_event
EVENT_LIST = [
 'change_artcheck_model_display_item',
 'change_artcheck_model_display_anim',
 'add_pendant_by_add_mesh',
 'add_pendant_by_bind',
 'delete_pendant_from_add_mesh',
 'delete_pendant_from_bind',
 'enable_character_outline',
 'disable_character_outline',
 'change_camera_focus_and_distance',
 'add_sfx',
 'delete_sfx',
 'change_artcheck_display_camera_state']
regist_event(EVENT_LIST)