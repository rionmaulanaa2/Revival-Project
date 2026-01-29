# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gevent/mecha_event.py
from __future__ import absolute_import
from common.event.event_base import regist_event
EVENT_LIST = [
 'observer_module_changed_event',
 'observer_attachment_changed_event',
 'observer_install_module_result_event',
 'observer_uninstall_module_result_event',
 'observer_install_attachment_result_event',
 'observer_bless_changed_event',
 'on_non_human_observer_fire_event',
 'update_mecha_module_plan_result_event',
 'on_lobby_mecha_changed',
 'mecha_control_main_ui_event',
 'mecha_switch_action',
 'on_init_mecha_ui',
 'reset_join_mecha_bgm',
 'on_init_state_change_ui',
 'mecha_init_event',
 'mecha_boarded_event',
 'mecha_leaved_event',
 'mecha_crashed_event']
regist_event(EVENT_LIST)