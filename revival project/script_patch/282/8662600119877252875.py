# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/proto/client/vehicle_proto.py
from __future__ import absolute_import

def set_seat_controller(synchronizer, player_id):
    synchronizer.send_event('E_SET_SEAT_CONTROLLER', player_id)


def vehicle_syn_transform(synchronizer, vid, trans_info):
    from mobile.common.EntityManager import EntityManager
    target = EntityManager.getentity(vid)
    if not target or not target.logic:
        return
    target.logic.send_event('E_VEHICLE_SYNC_RC_TRANSFORM', trans_info)


def join_vehicle(synchronizer, vehicle_id, driver, passenger):
    synchronizer.send_event('E_ON_JOIN_VEHICLE', vehicle_id, driver, passenger)


def change_seat(synchronizer, vehicle_id, seat_name):
    synchronizer.send_event('E_ON_CHANGE_SEAT', vehicle_id, seat_name)


def change_vehicle_data(synchronizer, vehicle_info):
    from logic.gcommon.common_const import vehicle_const
    if 'errcode' not in vehicle_info:
        synchronizer.send_event('E_ON_CHANGE_VEHICLE_DATA', vehicle_info)
        return
    errcode = vehicle_info['errcode']
    if errcode == vehicle_const.CH_SUCCESS:
        synchronizer.send_event('E_ON_CHANGE_VEHICLE_DATA', vehicle_info)
    else:
        emsg = {vehicle_const.CH_ERR_CHANGE_DRIVE_WHEN_NO_STOP: '\xe8\xbd\xbd\xe5\x85\xb7\xe5\x81\x9c\xe6\xad\xa2\xe5\x90\x8e\xe6\x89\x8d\xe8\x83\xbd\xe5\x88\x87\xe6\x8d\xa2\xe5\x8f\xb8\xe6\x9c\xba'}
        synchronizer.send_event('E_SHOW_MESSAGE', emsg.get(errcode, str(errcode)))


def vehicle_collision(synchronizer, vehicle_info):
    from mobile.common.EntityManager import EntityManager
    vid = vehicle_info['vid']
    vnpc = EntityManager.getentity(vid)
    vnpc.logic.send_event('E_SIMULATE_PHYSICS', vehicle_info)


def leave_vehicle(synchronizer, vehicle_info):
    synchronizer.send_event('E_ON_LEAVE_VEHICLE', vehicle_info)


def on_vehicle_hp_change(synchronizer, hp, part):
    synchronizer.send_event('S_HP', hp, part)


def on_vehicle_gas_mod(synchronizer, gas):
    synchronizer.send_event('S_VEHICLE_GAS', gas)


def on_vehicle_data_change(synchronizer, data):
    synchronizer.send_event('E_VEHICLE_DATA_CHANGE', data)


def set_phys_ctrl_enable(synchronizer, vid, enable, new_player_id, lin_spd, agl_spd):
    import math3d
    v3d_lin_spd = math3d.vector(*lin_spd)
    v3d_agl_spd = math3d.vector(*agl_spd)
    from mobile.common.EntityManager import EntityManager
    vnpc = EntityManager.getentity(vid)
    if not vnpc:
        return
    lvcl = vnpc.logic
    lvcl.send_event('E_VEHICLE_ENABLE_PHYSX', enable, new_player_id, v3d_lin_spd, v3d_agl_spd)


def airship_status(synchronizer, status, start_timestamp=None, speed=None, acc=None, start_point=None, end_point=None, orientation=None):
    synchronizer.send_event('E_AIRSHIP_STATUS', status, start_timestamp, speed, acc, start_point, end_point, orientation)


def on_low_freq_position(synchronizer, vehicle_pos):
    if not vehicle_pos or type(vehicle_pos) not in (tuple, list) or len(vehicle_pos) != 3:
        return
    from logic.gcommon.cdata import status_config
    in_vehicle = synchronizer.ev_g_in_mecha()
    on_driving = synchronizer.ev_g_is_in_any_state((status_config.ST_MECHA_DRIVER, status_config.ST_MECHA_PASSENGER))
    if not in_vehicle and on_driving:
        import math3d
        if G_POS_CHANGE_MGR:
            synchronizer.notify_pos_change(math3d.vector(*vehicle_pos))
        else:
            synchronizer.send_event('E_POSITION', math3d.vector(*vehicle_pos))


def vehicle_syn_water(synchronizer, vid, in_water, water_height):
    from mobile.common.EntityManager import EntityManager
    target = EntityManager.getentity(vid)
    if not target or not target.logic:
        return
    target.logic.send_event('E_VEHICLE_SYNC_WATER', in_water, water_height)


def vehicle_broadcast(synchronizer, vid, event_name, args):
    from mobile.common.EntityManager import EntityManager
    target = EntityManager.getentity(vid)
    if not target:
        return
    target.logic.send_event(event_name, *args)


def set_leave_point(synchronizer, leave_point):
    synchronizer.send_event('E_SET_LEAVE_POINT', leave_point)


def vehicle_horn(synchronizer, vid):
    from mobile.common.EntityManager import EntityManager
    target = EntityManager.getentity(vid)
    if not target:
        return
    target.logic.send_event('E_VEHICLE_HORN_SOUND')


def vehicle_sync_lin(synchronizer, vid, t, lin_pos, lin_vel, lin_acc):
    from mobile.common.EntityManager import EntityManager
    target = EntityManager.getentity(vid)
    if not target:
        return
    target.logic.send_event('E_VEHICLE_SYNC_LIN', t, lin_pos, lin_vel, lin_acc)


def vehicle_sync_agl(synchronizer, vid, t, agl_v3d, agl_vel, agl_acc):
    from mobile.common.EntityManager import EntityManager
    target = EntityManager.getentity(vid)
    if not target:
        return
    target.logic.send_event('E_VEHICLE_SYNC_AGL', t, agl_v3d, agl_vel, agl_acc)


def vehicle_sync_rb(synchronizer, vid, t, lin_pos, lin_agl, lin_vel, rb_id):
    from mobile.common.EntityManager import EntityManager
    target = EntityManager.getentity(vid)
    if not target:
        return
    target.logic.send_event('E_VEHICLE_SYNC_RB', t, lin_pos, lin_agl, lin_vel, rb_id)