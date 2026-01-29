# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/proto/client/crash_proto.py
from __future__ import absolute_import

def on_give_lin_spd(synchronizer, lst_vel_push, t, id_from):
    import math3d
    from mobile.common.EntityManager import EntityManager
    ve = EntityManager.getentity(id_from)
    if ve and ve.logic:
        pos = ve.logic.ev_g_position()
        synchronizer.send_event('E_HITED_SHOW_HURT_DIR', ve, pos)
    synchronizer.send_event('E_HIT_BY_FORCE', math3d.vector(*lst_vel_push), t)


def on_crash_id_changed(synchronizer, crash_id):
    synchronizer.send_event('E_CRASH_ID_CHANGED', crash_id)


def on_collision(synchronizer, a_id, b_id, lst_vel_diff, point):
    import math3d
    sfx_path = 'effect/fx/vehicle/huohua01.sfx'
    global_data.sfx_mgr.create_sfx_in_scene(sfx_path, math3d.vector(*point))