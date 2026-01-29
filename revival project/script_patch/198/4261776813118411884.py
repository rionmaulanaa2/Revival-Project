# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/proto/client/throwable_proto.py
from __future__ import absolute_import
import six

def throw_explosive_item(synchronizer, item_info):
    entity_id = None
    if synchronizer.is_unit_obj_type('LMecha') or synchronizer.is_unit_obj_type('LMechaTrans'):
        entity_id = synchronizer.sd.ref_driver_id
    elif synchronizer.is_unit_obj_type('LAvatar'):
        entity_id = synchronizer.unit_obj.id
    entity_id and global_data.emgr.teammate_on_fire.emit(entity_id)
    if not global_data.battle_idx or item_info.get('call_sync_id', None) != global_data.battle_idx:
        synchronizer.send_event('E_THROW_EXPLOSIVE_ITEM', item_info)
    return


def attach_explosive_item(synchronizer, item_info):
    synchronizer.send_event('E_ATTACH_EXPLOSIVE', item_info)


def detach_explosive_item(synchronizer, uniq_key):
    synchronizer.send_event('E_DETACH_EXPLOSIVE', uniq_key)


def on_ask_explosive_aff(synchronizer, item_eid, ipos, aff_radius):
    if ipos is None:
        return
    else:
        from math3d import vector
        ret = {}
        ipos = vector(*ipos)
        for eid, lentity in six.iteritems(global_data.war_lrobots):
            epos = lentity.ev_g_position()
            if not (epos and (ipos - epos).length < aff_radius):
                continue
            ret[eid] = (
             epos.x, epos.y, epos.z)

        if ret:
            synchronizer.call_sync_method('on_answer_explosive_aff', (item_eid, ret), True)
        return


def on_set_missile_lock_target(synchronizer, id_target):
    synchronizer.send_event('E_SET_MISSILE_LOCK_TARGET', id_target)


def on_bird_explosive_cure(synchronizer, cure_self_hp, cure_groupmate_ratio, cure_groupmate_range):
    synchronizer.send_event('E_SHOW_BIRD_CURE_EFFECT')


def on_throwable_stage_change(synchronizer, unique_key, stage, *args):
    global_data.emgr.scene_throw_item_stage_changed.emit(unique_key, stage, *args)


def on_trackmissile_boom(synchronizer, ret):
    synchronizer.send_event('E_TRACK_MISSILE_EXPLODE', ret)