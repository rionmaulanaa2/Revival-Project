# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gevent/lobby_player_event.py
from __future__ import absolute_import
from common.event.event_base import regist_event
EVENT_LIST = [
 'on_lobby_player_position_changed',
 'on_lobby_player_char_inited',
 'trigger_lobby_player_move',
 'trigger_lobby_player_move_stop',
 'trigger_lobby_player_set_yaw',
 'enable_lobby_player_free_cam',
 'reset_lobby_camera_from_free',
 'rotate_fixed_point_camera_event',
 'set_fixed_point_camera_event']
regist_event(EVENT_LIST)