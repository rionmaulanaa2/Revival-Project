# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/proto/client/parachute_proto.py
from __future__ import absolute_import
import math3d

def start_sortie(synchronizer, sortie_point, is_revive):
    if is_revive:
        synchronizer.send_event('E_LAND', math3d.vector(*sortie_point), False)
        synchronizer.send_event('E_SWITCH_LAST_GUN')
        global_data.emgr.player_revive_land.emit(synchronizer.unit_obj.id)
    else:
        synchronizer.send_event('E_SORTIE')


def start_parachute(synchronizer, start_pos, end_pos=None):
    synchronizer.send_event('E_START_PARACHUTE', start_pos, end_pos, False)


def open_parachute(synchronizer):
    synchronizer.send_event('E_OPEN_PARACHUTE')


def use_jet(synchronizer):
    synchronizer.send_event('E_USE_JET', False)


def stop_jet(synchronizer):
    synchronizer.send_event('E_STOP_JET', False)


def land(synchronizer, position):
    synchronizer.send_event('E_LAND', math3d.vector(*position))


def open_paragliding(synchronizer):
    synchronizer.send_event('E_EQUIP_PARACHUTE')


def close_paragliding(synchronizer):
    synchronizer.send_event('E_REMOVE_PARACHUTE')


def first_land(synchronizer):
    synchronizer.sd.ref_has_first_land = True