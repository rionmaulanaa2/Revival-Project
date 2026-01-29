# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gevent/live_event.py
from __future__ import absolute_import
from common.event.event_base import regist_event
EVENT_LIST = [
 'live_ready_event',
 'live_complete_event',
 'live_error_event',
 'live_report_stat_event',
 'live_get_vbr_list_event',
 'live_seek_complete_event',
 'live_list_receive_data_event',
 'receive_live_platform_channels_event',
 'notify_platform_live_list_update_event',
 'notify_platform_anchor_list_update_event',
 'live_danmu_msg_event',
 'notify_follow_anchor_change_event',
 'on_anchor_close_live_show_event',
 'on_write_storage_cb_event',
 'on_mic_permission_event',
 'receive_live_room_data_event',
 'live_url_change_event',
 'live_platform_inited_event',
 'live_vbr_change_event',
 'live_my_bet_info_ret']
regist_event(EVENT_LIST)