# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/proto/client/explosive_robot_proto.py
from __future__ import absolute_import

def on_explosive_robot_lock_target(synchronizer, target_id):
    if target_id is not None:
        from mobile.common.EntityManager import EntityManager
        lock_target = EntityManager.getentity(target_id)
        if lock_target and lock_target.logic:
            synchronizer.send_event('E_EXPLOSIVE_ROBOT_LOCK_TARGET', lock_target.logic)
            return
    synchronizer.send_event('E_EXPLOSIVE_ROBOT_LOCK_TARGET', None)
    return


def on_explosive_robot_swoop(synchronizer, target_id):
    if target_id is not None:
        from mobile.common.EntityManager import EntityManager
        target = EntityManager.getentity(target_id)
        if target and target.logic:
            synchronizer.send_event('E_EXPLOSIVE_ROBOT_SWOOP', target.logic)
    return


def on_explosive_robot_boom(synchronizer, is_time_out):
    synchronizer.send_event('E_EXPLOSIVE_ROBOT_TIMEOUT', is_time_out)


def on_tvmissile_boom(synchronizer):
    synchronizer.send_event('E_TV_MISSILE_EXPLODE_FROM_SERVER')