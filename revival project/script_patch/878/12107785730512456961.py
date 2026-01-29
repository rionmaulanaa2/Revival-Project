# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/proto/client/assistant_proto.py
from __future__ import absolute_import

def on_asst_status(synchronizer, status):
    synchronizer.send_event('E_SET_ASSISTANT_STATUS', status)


def on_asst_pos(synchronizer, pos_idx):
    synchronizer.send_event('E_ASSIATANT_POS_IDX_CHANGE', pos_idx)


def on_asst_action(synchronizer, iid, pos):
    import math3d
    if pos:
        pos = math3d.vector(*pos)
    else:
        pos = None

    def callback(event):
        if event:
            synchronizer.send_event('E_ASSISTANT_ACTION', event)

    synchronizer.ev_g_assistant_action_list(callback, iid, pos)
    return