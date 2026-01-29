# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/item/item_check_handler.py
from __future__ import absolute_import
import logic.gcommon.time_utility as t_util
import logic.gcommon.common_const.mecha_const as mconst
from logic.gutils.server_region import is_china_server

def check_use_blood_packet(unit_obj, item_id, args, auto_use=False):
    if unit_obj.ev_g_is_in_mecha():
        return check_use_mecha_drug(unit_obj, item_id, args, auto_use)
    else:
        return check_use_drug(unit_obj, item_id, args, auto_use)


def check_use_drug(unit_obj, item_id, args, auto_use=False):
    mecha_obj = unit_obj.ev_g_ctrl_mecha_obj()
    if mecha_obj and not mecha_obj.is_vehicle_mecha():
        unit_obj.get_owner().show_msg(pack_text(19055))
        return False
    else:
        check_full = args.get('full', False)
        if not check_full or not unit_obj.ev_g_full_hp():
            hp_limit = args.get('limit', None)
            if not hp_limit:
                return True
            cur_hp = unit_obj.ev_g_hp()
            if cur_hp < hp_limit:
                return True
        if not auto_use:
            unit_obj.get_owner().show_msg(pack_text(18019))
        return False


def check_use_mecha_drug(unit_obj, item_id, args, auto_use=False):
    mecha_id = unit_obj.ev_g_ctrl_mecha()
    if mecha_id is None:
        return False
    else:
        mecha = unit_obj.get_battle().get_entity(mecha_id)
        if mecha:
            lmecha = mecha.logic if 1 else None
            if not lmecha:
                return False
            check_full = args.get('full', False)
            if not check_full or not lmecha.ev_g_full_hp():
                hp_limit = args.get('limit', None)
                return hp_limit or True
            cur_hp = lmecha.ev_g_hp()
            if cur_hp < hp_limit:
                return True
        return False


def check_use_mecha_shield_drug(unit_obj, item_id, args, auto_use=False):
    mecha_id = unit_obj.ev_g_ctrl_mecha()
    if mecha_id is None:
        return False
    else:
        mecha = unit_obj.get_battle().get_entity(mecha_id)
        if mecha:
            lmecha = mecha.logic if 1 else None
            if not lmecha:
                return False
            check_full = args.get('full', False)
            if not check_full or not lmecha.ev_g_full_shield():
                shield_limit = args.get('limit', None)
                return shield_limit or True
            cur_shield = lmecha.ev_g_shield()
            if cur_shield < shield_limit:
                return True
        return False


def check_use_charger(unit_obj, item_id, args, auto_use=False):
    recall_cd_type = unit_obj.ev_g_recall_cd_type()
    if recall_cd_type == mconst.RECALL_CD_TYPE_NORMAL:
        unit_obj.get_owner().show_msg(pack_text(18196))
        return False
    if recall_cd_type == mconst.RECOVER_CD_TYPE_DISABLE:
        unit_obj.get_owner().show_msg(pack_text(80538))
        return False
    next_recall_time = unit_obj.ev_g_next_recall_time()
    if not next_recall_time:
        unit_obj.get_owner().show_msg(pack_text(18196))
        return False
    now = t_util.time()
    if now >= next_recall_time:
        unit_obj.get_owner().show_msg(pack_text(18224))
        return False
    return True


def check_use_summon_item(unit_obj, item_id, args, auto_use=False):
    vid = unit_obj.ev_g_get_cur_vehicle()
    if vid:
        return False
    in_mecha = unit_obj.ev_g_is_in_mecha()
    if in_mecha:
        return False
    return True


def check_use_battery(unit_obj, item_id, args, auto_use=False):
    if not unit_obj.ev_g_is_in_mecha():
        return False
    mecha_obj = unit_obj.ev_g_ctrl_mecha_obj()
    if not mecha_obj:
        return False
    if mecha_obj.is_vehicle_mecha():
        return False
    return True


def check_called_mecha(unit_obj, item_id, args, auto_use=False):
    mecha_obj = unit_obj.ev_g_ctrl_mecha_obj()
    if not mecha_obj or mecha_obj.is_vehicle_mecha():
        mecha_id = unit_obj.ev_g_create_mecha()
        mecha_obj = unit_obj.get_battle().get_entity(mecha_id)
    if not mecha_obj or not mecha_obj.logic:
        return False
    recall_cd_type = unit_obj.ev_g_recall_cd_type()
    if recall_cd_type == mconst.RECOVER_CD_TYPE_DISABLE:
        return False
    if recall_cd_type == mconst.RECALL_CD_TYPE_DIE and unit_obj.ev_g_next_recall_left_time() > 0:
        return False
    return True


def check_use_reset_mecha_item(unit_obj, item_id, args, auto_use=False):
    if not unit_obj.ev_g_is_created_mecha():
        return False
    if unit_obj.ev_g_is_in_mecha():
        return False
    battle = unit_obj.get_battle()
    if not battle or battle.is_battle_finish():
        return False
    if not unit_obj.ev_g_is_call_mecha_valid():
        unit_obj.get_owner().show_msg(pack_text(17024))
        return False
    return True


def check_use_reset_mecha_item_in_exercise(unit_obj, item_id, args, auto_use=False):
    if not unit_obj.ev_g_is_created_mecha():
        return False
    if unit_obj.ev_g_is_in_mecha():
        return False
    if not unit_obj.ev_g_is_call_mecha_valid():
        unit_obj.get_owner().show_msg(pack_text(17024))
        return False
    return True


def check_use_back_home(unit_obj, item_id, args, auto_use=False):
    is_in_mecha = unit_obj.ev_g_is_in_mecha()
    last_is_in_mecha = unit_obj.ev_g_last_is_in_mecha()
    if last_is_in_mecha is None:
        unit_obj.send_event('E_SET_LAST_IS_IN_MECHA', is_in_mecha)
        return True
    else:
        if last_is_in_mecha and not is_in_mecha:
            return False
        return True
        return


def check_use_outside_items(unit_obj, item_id, args, auto_use=False):
    check_item_no = args.get('item_no')
    wp = unit_obj.ev_g_wpbar_cur_weapon()
    if wp and int(wp.get_id()) == check_item_no:
        return False
    return True


def check_use_rewardorder_item(unit_obj, item_id, args, auto_use=False):
    battle = unit_obj.get_battle()
    owner = unit_obj.get_owner()
    if not battle or not owner:
        return False
    if not battle.can_use_rewardorder(owner):
        return False
    return True


def check_not_in_water(unit_obj, item_id, args, auto_use=False):
    from logic.gcommon.common_const.water_const import WATER_NONE
    return unit_obj.sd.ref_water_status == WATER_NONE