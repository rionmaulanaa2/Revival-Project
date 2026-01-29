# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/item/item_use_handler.py
from __future__ import absolute_import
import six
from logic.gcommon import time_utility as t_util
from logic.gcommon.common_const import battle_const
import logic.gcommon.item.item_utility as iutil
import logic.gcommon.common_utils.math3d_utils as mutil
import logic.gcommon.item.item_const as item_const
from data.mecha_conf import DEFAULT_MECHATRANS_ID
from mobile.common.IdManager import IdManager
from logic.gcommon.common_const import shop_const
from data.item_use_data import get_use_args
from logic.gcommon.common_const import attr_const
from data.buff_data import get_buff_human_replicate_to_mecha
from logic.gcommon.const import NEOX_UNIT_SCALE
from logic.server_const import ENTITY_TAG_PLAYER

def on_use_blood_packet(unit_obj, item_id, args):
    if unit_obj.ev_g_is_in_mecha():
        return on_use_mecha_drug(unit_obj, item_id, {'effect': args.get('mecha', 0),
           'ratio': args.get('mecha_ratio', 0),
           'item_eid': args.get('item_eid', None),
           'punish_func': args.get('punish_func', None),
           'punish_range': args.get('punish_range', None)
           })
    else:
        return on_use_drug(unit_obj, item_id, {'effect': args.get('human', 0)})
        return None


def on_use_drug(unit_obj, item_id, args):
    effect = args.get('effect', 0)
    cur_hp = unit_obj.ev_g_hp()
    if cur_hp <= 0:
        return
    bond_gift_add_factor = unit_obj.ev_g_add_attr(attr_const.HUMAN_ATTR_CURE_ITEM_ADD_FACTOR, 0)
    recover_signal = args.get('recover_signal', 30)
    if bond_gift_add_factor > 0:
        recover_signal += int(recover_signal * bond_gift_add_factor)
    unit_obj.send_event('E_RECOVER_SIGNAL', recover_signal)
    if bond_gift_add_factor > 0:
        effect += int(effect * bond_gift_add_factor)
    unit_obj.send_event('E_CURE', effect)
    unit_obj.send_event('E_RECORD_USE_DRUG')
    do_cure_sa_log(unit_obj, item_id, cur_hp)
    return True


def on_use_mecha_drug(unit_obj, item_id, args):
    mecha_id = unit_obj.ev_g_ctrl_mecha()
    if mecha_id is None:
        return False
    else:
        battle = unit_obj.get_battle()
        mecha = battle.get_entity(mecha_id)
        if mecha:
            lmecha = mecha.logic if 1 else None
            return lmecha or False
        effect = args.get('effect', 0)
        ratio = args.get('ratio', 0)
        if ratio > 0:
            max_hp = lmecha.ev_g_max_hp() or 0
            effect += max_hp * ratio
        item_eid = args.get('item_eid', None)
        item_entity = battle.get_entity(item_eid)
        unit_faction = unit_obj.get_owner().get_faction()
        if item_entity and item_entity.get_faction() == unit_faction:
            punish_func = args.get('punish_func', None)
            if punish_func:
                point = battle.get_group_points(unit_faction)
                other_point = battle.get_group_points(battle.get_another_group_id(unit_faction))
                point_range = args['punish_range']
                point_ratio = (point - other_point) * 1.0 / battle._settle_point
                punish_effect = 0
                if point_ratio < point_range[0][0]:
                    punish_effect = point_range[0][1]
                elif point_ratio > point_range[1][0]:
                    punish_effect = point_range[1][1]
                else:
                    punish_effect = punish_func(point_ratio)
                effect = effect * (1 - punish_effect / 100.0)
        cur_hp = lmecha.ev_g_hp()
        lmecha.send_event('E_CURE', effect)
        mecha_owner_id = mecha.get_owner()
        mecha_owner = battle.get_entity(mecha_owner_id)
        if mecha_owner and mecha_owner.logic:
            mecha_owner.logic.send_event('E_RECORD_USE_DRUG')
        do_cure_sa_log(unit_obj, item_id, cur_hp)
        return True


def on_use_mecha_shield_drug(unit_obj, item_id, args):
    mecha_id = unit_obj.ev_g_ctrl_mecha()
    if mecha_id is None:
        return False
    else:
        battle = unit_obj.get_battle()
        mecha = battle.get_entity(mecha_id)
        if mecha:
            lmecha = mecha.logic if 1 else None
            return lmecha or False
        effect = args.get('effect', 0)
        ratio = args.get('ratio', 0)
        if ratio > 0:
            max_shield = lmecha.ev_g_max_shield() or 0
            effect += max_shield * ratio
        pre_shield = lmecha.ev_g_shield()
        lmecha.send_event('E_ADD_SHIELD', effect)
        now_shield = lmecha.ev_g_shield()
        add = now_shield - pre_shield
        if add > 0:
            lmecha.send_event('E_EFFECT_EVENT', 'EVENT_PICK_SHIELD', {'effect': add})
        return True


def on_full_mecha_shield_drug(unit_obj, item_id, args):
    mecha_id = unit_obj.ev_g_ctrl_mecha()
    if mecha_id is None:
        return False
    else:
        battle = unit_obj.get_battle()
        mecha = battle.get_entity(mecha_id)
        if mecha:
            lmecha = mecha.logic if 1 else None
            return lmecha or False
        lmecha.send_event('E_FULL_SHIELD')
        lmecha.send_event('E_FULLHP')
        return True


def do_cure_sa_log(unit_obj, item_id, begin_hp):
    owner = unit_obj.get_owner()
    if not owner:
        return
    else:
        Get_Value = unit_obj.get_value
        pos = Get_Value('G_POSITION')
        position = (pos.x, pos.y, pos.z) if pos else None
        try_use_time = Get_Value('G_ITEMUSE_TRY_TIME') or 0
        mp_info = {'location': [
                      pos.x, pos.y, pos.z],
           'item_id': item_id,
           'itembeginhp': begin_hp,
           'position': position,
           'use_time': t_util.time() - try_use_time
           }
        owner.sa_log_game_medicine(mp_info)
        return


def on_add_human_buff(unit_obj, item_id, args):
    buff_id = args.get('buff_id', None)
    if buff_id is None:
        return False
    else:
        unit_obj.send_event('E_ADD_BUFF', buff_id)
        return True


def on_add_mecha_buff(unit_obj, item_id, args):
    buff_id = args.get('buff_id', None)
    need_on_mecha = args.get('need_on_mecha', True)
    if buff_id is None:
        return False
    else:
        mecha_id = unit_obj.ev_g_ctrl_mecha()
        if mecha_id is None and need_on_mecha:
            return False
        mecha = unit_obj.get_battle().get_entity(mecha_id)
        if not mecha or not mecha.logic or mecha.is_vehicle_mecha():
            mecha_id = unit_obj.ev_g_create_mecha()
            mecha = unit_obj.get_battle().get_entity(mecha_id)
            if not mecha or not mecha.logic:
                return False
        if item_id in ITEM_USE_SALOG_BEFORE:
            ITEM_USE_SALOG_BEFORE[item_id](unit_obj, mecha.logic, item_id, buff_id)
        mecha.logic.send_event('E_ADD_BUFF', buff_id)
        return True


def on_summon_attachable(unit_obj, item_id, args):
    battle = unit_obj.get_battle()
    point_3d = unit_obj.ev_g_position()
    point_tp = mutil.v3d_to_tp(point_3d)
    attachable_id = args.get('attach_id', None)
    if attachable_id is None:
        return False
    else:
        if iutil.is_attachable_item(attachable_id):
            fashion = unit_obj.ev_g_item_fashion(attachable_id)
            attachable = battle.create_attachable(attachable_id, point_tp, fashion=fashion)
            unit_obj.send_event('E_TRY_ATTACH', attachable.id)
            return True
        log_error('use an unvalid summon item, item_id=%d, summon_id=%d', item_id, attachable_id)
        return False
        return


def on_summon_mecha(unit_obj, item_id, args):
    battle = unit_obj.get_battle()
    position = args.get('position')
    if position and type(position) in (list, tuple) and len(position) == 3:
        import math3d
        point_3d = math3d.vector(*position)
    else:
        point_3d = unit_obj.ev_g_position()
    mecha_id = args.get('mecha_id', None)
    if mecha_id is None:
        return False
    else:
        if iutil.is_mecha(mecha_id):
            from logic.gcommon.common_const import mecha_const
            mecha_data = {'auto_join': True,
               'trans_pattern': mecha_const.MECHA_PATTERN_NORMAL,
               'shapeshift': mecha_const.VEHICLE_STATE_HUMAN,
               'human_yaw': unit_obj.ev_g_yaw() or 0,
               'mecha_fashion': unit_obj.ev_g_item_fashion(mecha_id)
               }
            if not mecha_data['mecha_fashion']:
                mecha_data['mecha_fashion'] = unit_obj.ev_g_item_fashion(DEFAULT_MECHATRANS_ID)
            mecha_obj = battle.create_mecha(mecha_id, point_3d, unit_obj.get_owner().id, mecha_data)
            if mecha_obj and unit_obj.get_owner():
                mecha_obj.set_faction(unit_obj.get_owner().get_faction())
            return True
        log_error('use an unvalid summon item, item_id=%d, summon_id=%d', item_id, mecha_id)
        return False
        return


def on_use_reset_mecha_item(unit_obj, item_id, args):
    if not unit_obj.ev_g_is_created_mecha():
        return False
    if unit_obj.ev_g_is_in_mecha():
        return False
    unit_obj.send_event('E_RESET_MECHA')
    battle = unit_obj.get_battle()
    owner = unit_obj.get_owner()
    if battle and owner:
        report_dict = {'event_type': battle_const.FIGHT_EVENT_RESET_MECHA,'char_name': owner.get_name()
           }
        battle.notify_battle_report(report_dict)
    return True


def on_use_reset_mecha_item_in_exercise(unit_obj, item_id, args):
    if not unit_obj.ev_g_is_created_mecha():
        return False
    if unit_obj.ev_g_is_in_mecha():
        return False
    unit_obj.send_event('E_RESET_MECHA')
    battle = unit_obj.get_battle()
    owner = unit_obj.get_owner()
    if battle and owner:
        report_dict = {'event_type': battle_const.FIGHT_EVENT_RESET_MECHA,'char_name': owner.get_name()
           }
        battle.notify_battle_report(report_dict)
    item_data = {'item_id': item_id,'entity_id': IdManager.genid(),'count': 1}
    unit_obj.ev_g_give_other_item(item_data)
    return True


def on_use_neutral_shop_candy(unit_obj, item_id, args):
    battle = unit_obj.get_battle()
    if not battle:
        return False
    else:
        buff_data = args.get('buff_data', {})
        if not buff_data:
            return False
        need_buff_len = len(buff_data)
        buff_add_result = []
        ctrl_mecha = unit_obj.ev_g_ctrl_mecha_obj()
        created_mecha = battle.get_entity(unit_obj.ev_g_create_mecha())
        mecha_objs = []
        if ctrl_mecha:
            mecha_objs.append(ctrl_mecha)
            if created_mecha and created_mecha.id != ctrl_mecha.id:
                mecha_objs.append(created_mecha)
        elif created_mecha:
            mecha_objs.append(created_mecha)
        for item_no in shop_const.NEUTRAL_SHOP_CANDY_ITEM_NO_SET:
            if item_no == item_id:
                continue
            other_add_buff_data = get_use_args(item_no).get('buff_data', {})
            for other_buff_id in six.iterkeys(other_add_buff_data):
                if other_buff_id and type(other_buff_id) is int:
                    unit_obj.send_event('E_DEL_BUFF_BY_ID', other_buff_id)
                    for mecha in mecha_objs:
                        buff_human_replicate_to_mecha = get_buff_human_replicate_to_mecha(other_buff_id)
                        if mecha and mecha.logic and buff_human_replicate_to_mecha is not None:
                            mecha_buff_id = buff_human_replicate_to_mecha.get('add_mecha_buff_id')
                            mecha.logic.send_event('E_DEL_BUFF_BY_ID', mecha_buff_id)

        for b_id, b_data in six.iteritems(buff_data):
            unit_obj.send_event('E_ADD_BUFF', b_id, b_data, buff_ret=buff_add_result, source_info='use_%s' % item_id)

        if hasattr(battle, 'update_neutral_shop_item_use_record'):
            battle.update_neutral_shop_item_use_record(unit_obj.id, item_id)
        return len(buff_add_result) == need_buff_len


def on_use_back_home_item(unit_obj, item_id, args):
    item_data = {'item_id': item_id,'entity_id': IdManager.genid(),'count': 1}
    unit_obj.ev_g_give_other_item(item_data)
    battle = unit_obj.get_battle()
    if not battle:
        return False
    if hasattr(battle, 'start_suicide'):
        battle.start_suicide(unit_obj.get_owner())
    return True


def on_use_dogtag(unit_obj, item_id, args):
    buff_data = args.get('buff_data', {})
    if not buff_data:
        return False
    soul_id = args.get('soul_id')
    if not soul_id:
        return
    for buff_id, data in six.iteritems(buff_data):
        d = {'soul_id': soul_id,'replicate_data': {'soul_id': soul_id}}
        d.update(data)
        unit_obj.send_event('E_ADD_BUFF', buff_id, d)


def on_summon_building(unit_obj, item_id, args):
    try:
        position = args.get('position')
        if not isinstance(position, (list, tuple)) or len(position) != 3:
            return
        rot = args.get('rot')
        if not isinstance(rot, (list, tuple)) or len(rot) != 4:
            return
        data = {}
        data.update(args)
        data['owner'] = unit_obj.id
        building_no = args['building_no']
        battle = unit_obj.get_battle()
        battle.create_building(building_no, position, data)
        return True
    except Exception as e:
        log_error('summon building, item_id: %s, args: %s, error: %s', item_id, args, str(e))
        return False


def on_use_empty(unit_obj, item_id, args):
    return True


def on_use_outside_items(unit_obj, item_id, args):
    unit_obj.get_owner().cost_game_item(item_id, 1)
    return True


def on_use_concert_light_stick_item(unit_obj, item_id, args):
    weapon_pos = args['weapon_pos']
    weapon_id = args['weapon_id']
    unit_obj.send_event('E_INIT_EQUIPMENT', {'weapon_dict': {weapon_pos: weapon_id}})
    unit_obj.send_event('E_SWITCHING', weapon_pos)


def on_use_rewardorder_item(unit_obj, item_id, args):
    battle = unit_obj.get_battle()
    owner = unit_obj.get_owner()
    if not battle or not owner:
        return False
    if not battle.can_use_rewardorder(owner):
        return False
    battle.add_hunter_state(owner)
    return True


def on_use_live_salvo(unit_obj, item_id, args):
    range = int(args.get('range', 10))
    battle = unit_obj.get_battle()
    pos = unit_obj.ev_g_position()
    entity_ids = battle.get_circle_entity_ids(range * NEOX_UNIT_SCALE, pos.x, pos.y, pos.z, ENTITY_TAG_PLAYER)
    for entity_id in entity_ids:
        ent = battle.get_entity(entity_id)
        if entity_id == battle._king or entity_id == battle._defier:
            continue
        if ent and ent.logic:
            ent.logic.send_event('E_CALL_SYNC_METHOD', 'do_live_dance', (), True, True, True)

    if unit_obj.get_owner():
        pack_msg = pack_text(610622, {'player_name': unit_obj.get_owner().get_name()})
        for soul_id in battle.get_all_soul_iterids():
            soul = battle.get_soul(soul_id)
            if soul and soul.logic:
                soul.logic.send_event('E_CALL_SYNC_METHOD', 'on_bs_pack_msg', (pack_msg, 0), True, True, False)


def on_use_magic_box_item(unit_obj, item_id, args):
    user_args = get_use_args(item_id)
    buff_ids = user_args.get('buffs', [])
    for buff_id in buff_ids:
        unit_obj.send_event('E_ADD_BUFF', buff_id)

    remove_histroy_magic_items_effect(unit_obj, item_id)
    return True


def on_use_magic_endurance_drug(unit_obj, item_id, args):
    mecha_obj = unit_obj.ev_g_ctrl_mecha_obj()
    if not mecha_obj or mecha_obj.is_vehicle_mecha():
        mecha_id = unit_obj.ev_g_create_mecha()
        mecha_obj = unit_obj.get_battle().get_entity(mecha_id)
    if mecha_obj and mecha_obj.logic:
        user_args = get_use_args(item_id)
        buff_ids = user_args.get('buffs', [])
        for buff_id in buff_ids:
            mecha_obj.logic.send_event('E_ADD_BUFF', buff_id)

    remove_histroy_magic_items_effect(unit_obj, item_id)
    return True


def on_summon_tvmissile_launcher(unit_obj, item_id, args):
    if not unit_obj:
        return
    battle = unit_obj.get_battle()
    if not battle:
        return
    point_3d = unit_obj.ev_g_position()
    if not point_3d:
        log_error('on_summon_tvmissile_launcher error, battle: %s, unit_obj: %s', battle.id, unit_obj.id)
        return
    launcher_id = args.get('launcher_id', 0)
    max_hp = args.get('max_hp', 0)
    bind_guns = args.get('bind_guns', [])
    launcher_data = {'pos': (
             point_3d.x, point_3d.y, point_3d.z),
       'max_hp': max_hp,
       'bind_guns': bind_guns,
       'human_yaw': unit_obj.ev_g_yaw() or 0
       }
    battle.create_tvmissile_launcher(launcher_id, launcher_data)
    return True


def on_use_crystal_stone(unit_obj, item_id, args):
    unit_obj.send_event('E_ON_ADD_CRYSTAL_STONE', 1)
    return True


def on_add_buff_cure_sa_log(unit_obj, lmecha, item_id, buff_id):
    cur_hp = lmecha.ev_g_hp()
    do_cure_sa_log(unit_obj, item_id, cur_hp)


ITEM_USE_SALOG_BEFORE = {item_const.ITEM_NO_MECHABATTERY: on_add_buff_cure_sa_log,
   item_const.ITEM_NO_MECHA_SLOW_DRUG: on_add_buff_cure_sa_log
   }

def remove_histroy_magic_items_effect(unit_obj, item_id):
    battle = unit_obj.get_battle()
    if not battle:
        return False
    ctrl_mecha = unit_obj.ev_g_ctrl_mecha_obj()
    created_mecha = battle.get_entity(unit_obj.ev_g_create_mecha())
    mecha_objs = []
    if ctrl_mecha:
        mecha_objs.append(ctrl_mecha)
        if created_mecha and created_mecha.id != ctrl_mecha.id:
            mecha_objs.append(created_mecha)
    elif created_mecha:
        mecha_objs.append(created_mecha)
    magic_items = battle.get_magic_items()
    for item_no in magic_items:
        if item_no == item_id:
            continue
        other_add_buff_list = get_use_args(item_no).get('buffs', [])
        for other_buff_id in other_add_buff_list:
            if other_buff_id and type(other_buff_id) is int:
                unit_obj.send_event('E_DEL_BUFF_BY_ID', other_buff_id)
                for mecha in mecha_objs:
                    buff_human_replicate_to_mecha = get_buff_human_replicate_to_mecha(other_buff_id)
                    if buff_human_replicate_to_mecha:
                        mecha_buff_id = buff_human_replicate_to_mecha.get('add_mecha_buff_id')
                    else:
                        mecha_buff_id = other_buff_id
                    if mecha and mecha.logic:
                        mecha.logic.send_event('E_DEL_BUFF_BY_ID', mecha_buff_id)