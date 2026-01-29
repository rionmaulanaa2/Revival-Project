# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/common/event/pc_event.py
from __future__ import absolute_import
from common.event.event_base import regist_event
EVENT_LIST = [
 'pc_hotkey_hint_display_option_changed',
 'pc_hotkey_hint_switch_toggled',
 'pc_hotkey_binding_changed',
 'pc_hotkey_binding_bulk_updated',
 'pc_paste_text',
 'pc_hotkey_try_reload',
 'run_switch_state_changed_event']
regist_event(EVENT_LIST)