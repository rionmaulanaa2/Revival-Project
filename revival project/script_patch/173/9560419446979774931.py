# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/common/event/account_event.py
from __future__ import absolute_import
from common.event.event_base import regist_event
EVENT_LIST = [
 'registed_account_updated_event',
 'request_sdk_login',
 'on_server_list_refresh_event',
 'on_used_name_updated_event',
 'on_random_name_updated_event',
 'account_request_create_usr',
 'character_choose_cancel',
 'character_choose_confirm',
 'character_walk_to_input_name',
 'character_inputing_name',
 'back_to_character_select',
 'language_select_event',
 'on_tw_agreement_change_event',
 'hide_main_login_btn_event',
 'should_login_channel_event',
 'on_delay_refreshed_event',
 'check_apply_postprocess']
regist_event(EVENT_LIST)