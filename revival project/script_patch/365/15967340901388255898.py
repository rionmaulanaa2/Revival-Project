# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/proto/client/common_proto.py
from __future__ import absolute_import
import logic.gcommon.common_utils.bcast_utils as bcast_utils
import six

def nearby_session_mic(synchronizer, state):
    synchronizer.send_event('E_NEARBY_SESSION_MIC_STATE', state)


def nearby_voice_info(synchronizer, nearby_streamid, nearby_eid):
    synchronizer.send_event('E_NEARBY_VOICE_INFO', nearby_streamid, nearby_eid)


def bcast_evt(synchronizer, event_name, args=(), kwargs=None, offline_monitor=None, offline_id=None, offline_ename=None):
    event_name = bcast_utils.idx_2_event_name(event_name)
    if offline_monitor is not None:
        synchronizer.send_event('E_BCAST_OFFLINE_MONITOR', offline_monitor, offline_id, offline_ename)
    if not synchronizer.ev_g_death() or event_name == 'E_REVIVE':
        if kwargs and type(kwargs) is dict:
            synchronizer.send_event(event_name, *args, **kwargs)
        else:
            synchronizer.send_event(event_name, *args)
    return