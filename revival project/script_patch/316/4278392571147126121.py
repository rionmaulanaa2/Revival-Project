# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/proto/client/item_proto.py
from __future__ import absolute_import

def update_item_use_limit(synchronizer, item_id, cnt):
    synchronizer.send_event('E_REFRESH_ITEM_LIMIT', item_id, cnt)


def item_use_on(synchronizer, item_id, item_cd=None, item_limit=None):
    synchronizer.send_event('E_ITEMUSE_ON', item_id, item_cd, item_limit)


def item_set_cd(synchronizer, item_id, item_cd):
    synchronizer.send_event('E_SET_ITEM_CD', item_id, item_cd)


def item_use_try_res(synchronizer, item_id, ret):
    synchronizer.send_event('E_ITEMUSE_TRY_RET', item_id, ret)


def item_use_cancel(synchronizer, item_id):
    synchronizer.send_event('E_ITEMUSE_CANCEL_RES', item_id)


def ap_try_pick_up(synchronizer, item_position, player_position):
    import math3d
    p0 = item_position
    p1 = player_position
    synchronizer.send_event('E_TRY_PICK_UP', math3d.vector(*p0), math3d.vector(*p1))


def remove_child_item(synchronizer, item_eid):
    synchronizer.send_event('E_REMOVE_CHILD_ITEM', item_eid)


def throw_item(synchronizer, backpack_part, item_pos, mode):
    synchronizer.send_event('E_THROW_ITEM', backpack_part, item_pos)
    import logic.gcommon.const as g_const
    if mode == g_const.THROW_MODE_THROW:
        synchronizer.send_event('E_THROW_ITEM_SOUND')


def pick_up_others(synchronizer, item_list, need_play=False):
    for item_data in item_list:
        synchronizer.send_event('E_PICK_UP_OTHERS', item_data)

    if item_list:
        cur_weapon = synchronizer.ev_g_wpbar_cur_weapon()
        if cur_weapon and cur_weapon.get_bullet_num() <= 0:
            synchronizer.send_event('E_TRY_RELOAD')
    if need_play and synchronizer.ev_g_is_avatar():
        global_data.emgr.show_item_fly_to_bag_message_event.emit(item_list)


def pick_up_item_succ(synchronizer, item_eid, item_id=None, auto_use=False):
    synchronizer.send_event('E_PICK_UP_SUCC', item_eid, item_id, auto_use)


def mod_item_count(synchronizer, backpack_part, item_entity_id, count, is_throw=False):
    import logic.gcommon.const
    synchronizer.send_event('E_MOD_ITME_COUNT', backpack_part, item_entity_id, count)
    if is_throw:
        synchronizer.send_event('E_THROW_ITEM_SOUND')
    throw_item_data, throw_item_pos = synchronizer.ev_g_item_data(backpack_part, item_entity_id)
    if backpack_part == logic.gcommon.const.BACKPACK_PART_OTHERS and count > 0:
        cur_weapon = synchronizer.ev_g_wpbar_cur_weapon()
        if cur_weapon and cur_weapon.get_bullet_num() <= 0:
            synchronizer.send_event('E_TRY_RELOAD')


def equip_simu_weapon(synchronizer, item_data, put_pos):
    synchronizer.ev_g_on_equip_simu_weapon(item_data, put_pos)


def unequip_simu_weapon(synchronizer, put_pos):
    synchronizer.ev_g_on_unequip_simu_weapon(put_pos)


def pick_up_weapon(synchronizer, item_data, put_pos, switch=True):
    synchronizer.send_event('E_PICK_UP_WEAPON', item_data, put_pos, switch)


def pick_up_clothing(synchronizer, item_data, put_pos=None):
    synchronizer.send_event('E_PICK_UP_CLOTHING', item_data)
    if item_data['item_id'] >= 1651 and item_data['item_id'] <= 1662:
        return


def mod_pick_count(synchronizer, child_eid, count):
    synchronizer.send_event('E_PICKABLE_ITEM_COUNT', child_eid, count)


def clear_backpack(synchronizer):
    synchronizer.send_event('E_DO_CLEAR_BACKPACK')


def clear_weapon(synchronizer):
    synchronizer.send_event('E_DO_CLEAR_WEAPON')


def clear_clothing(synchronizer):
    synchronizer.send_event('E_DO_CLEAR_CLOTHING')


def clear_others(synchronizer):
    synchronizer.send_event('E_DO_CLEAR_OTHERS')


def clear_backpack_with_limited_list(synchronizer, limited_list):
    synchronizer.send_event('E_DO_CLEAR_BACKPACK_WITH_LIMITED_LIST', limited_list)


def pick_up_mecha_battery(synchronizer, battery_eid):
    synchronizer.send_event('E_PICK_UP_MECHA_BATTERY', battery_eid)


def paradrop_set_pickable(synchronizer, is_pickable):
    synchronizer.send_event('E_SET_PICKABLE', is_pickable)


def install_mecha_module_result(synchronizer, result, slot_pos, card_id, item_id):
    synchronizer.send_event('E_MECHA_INSTALL_MODULE_RESULT', result, slot_pos, card_id, item_id)


def uninstall_mecha_module_result(synchronizer, result, slot_pos, card_id, clear_item=True):
    synchronizer.send_event('E_MECHA_UNINSTALL_MODULE_RESULT', result, slot_pos, card_id, clear_item)


def mecha_module_drop_on_die(synchronizer, item_ids, left_modules):
    synchronizer.send_event('E_MECHA_MODULE_DROP_ON_DIE', item_ids)
    synchronizer.send_event('E_REFRESH_MECHA_MODULE', left_modules.get('module_installed', {}))


def on_star_point_update(synchronizer, driver_lv, star_point):
    synchronizer.send_event('E_PLAYER_LEVEL_UP', driver_lv, star_point)
    synchronizer.send_event('S_ATTR_SET', 'driver_level', driver_lv)
    synchronizer.send_event('S_ATTR_SET', 'star_point', star_point)


def nightmare_box_start_awake(synchronizer, level=0):
    synchronizer.send_event('E_START_AWAKE', level)


def nightmare_box_on_awake(synchronizer):
    synchronizer.send_event('E_SET_AWAKE')


def nightmare_monster_on_killed(synchronizer, monster_pos):
    synchronizer.send_event('E_ON_MONSTER_KILLED', monster_pos)


def on_set_drug_shortcut(synchronizer, item_id):
    synchronizer.send_event('E_SET_SHOW_SHORTCUT', item_id, False)


def mecha_module_effect_activate(synchronizer, card_id, buff_params):
    synchronizer.send_event('E_MECHA_MODULE_EFFECT_ACTIVATE', card_id, buff_params)


def mecha_module_effect_deactivate(synchronizer, card_id):
    synchronizer.send_event('E_MECHA_MODULE_EFFECT_DEACTIVATE', card_id)


def open_rogue_box_success(synchronizer, box_id, gift_list):
    synchronizer.send_event('E_OPEN_ROGUE_BOX_SUCCESS', box_id, gift_list)


def choose_rogue_gift_result(synchronizer, result, gift_id):
    synchronizer.send_event('E_CHOOSE_ROGUE_GIFT_RESULT', result, gift_id)


def clear_rogue_gifts(synchronizer):
    synchronizer.send_event('E_CLEAR_ROGUE_GIFTS')


def cancel_holding_rogue_box(synchronizer, box_id):
    synchronizer.send_event('E_CANCEL_HOLDING_ROGUE_BOX', box_id)


def update_elasticity_use_cd(synchronizer, elasticity_use_cd):
    synchronizer.send_event('E_SET_ELASTICITY_USE_CD', elasticity_use_cd)


def on_meow_coin_update(synchronizer, bag_num, mail_total_time, mail_total_num):
    synchronizer.send_event('E_ON_MEOW_COIN_UPDATE', bag_num, mail_total_time, mail_total_num)


def mail_meow_coin_result(synchronizer, error_code, mail_num, bag_num, mail_total_time, m_t_num, m_id):
    synchronizer.send_event('E_ON_MAIL_MEOW_COIN_RESULT', error_code, mail_num, bag_num, mail_total_time, m_t_num, m_id)


def do_live_dance(synchronizer):
    synchronizer.send_event('E_PLAY_LIVE_CONCERT_DANCE')


def clear_item_use_status(synchronizer):
    synchronizer.send_event('E_CLEAR_ITEM_USE_STATUS')


def on_carry_bullet_merged(synchronizer, transfer_num, put_pos):
    synchronizer.send_event('E_ON_CARRY_BULLET_MERGED', transfer_num, put_pos)


def on_magic_coin_cnt_change(synchronizer, coin_cnt):
    synchronizer.send_event('E_UPDATE_MAGIC_COIN_CNT', coin_cnt)


def on_magic_exchange_times_change(synchronizer, times):
    synchronizer.send_event('E_UPDATE_MAGIC_EXCHANGE_TIMES', times)


def clear_module_data(synchronizer):
    synchronizer.send_event('E_MECHA_CLEAR_MODULE_DATA')