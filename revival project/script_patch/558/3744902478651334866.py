# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gutils/online_state_utils.py
from __future__ import absolute_import
import six
import logic.gcommon.const as const
from common.const.property_const import C_NAME, U_ID, U_LV, ROLE_ID, HEAD_FRAME, HEAD_PHOTO

def is_not_online(state):
    return state in (const.STATE_OFFLINE, const.STATE_INVISIBLE)


def get_friend_online_count(friends):
    count = 0
    friend_online_state = global_data.message_data.get_player_online_state()
    if isinstance(friends, dict):
        for friend_id in six.iterkeys(friends):
            state = int(friend_online_state.get(int(friend_id), const.STATE_OFFLINE))
            if not is_not_online(state):
                count += 1

    elif isinstance(friends, list) or isinstance(friends, tuple):
        for friend in friends:
            state = int(friend_online_state.get(int(friend[U_ID]), 0))
            if not is_not_online(state):
                count += 1

    return count