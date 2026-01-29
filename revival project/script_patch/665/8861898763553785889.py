# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/proto/client/mecha_proto.py
from __future__ import absolute_import
from mobile.common.EntityManager import EntityManager

def change_mecha_seat(synchronizer, ret, seat):
    pass


def change_passenger(synchronizer, passenger_id, seat):
    synchronizer.send_event('E_CHANGE_PASSENGER_SEAT', passenger_id, seat)
    synchronizer.send_event('E_CHANGE_PASSENGER', passenger_id, seat)


def join_mecha(synchronizer, mecha_id, mecha_type, seat_name, timestamp, is_share=False, fashion=None):
    synchronizer.send_event('E_ON_JOIN_MECHA_START', mecha_id, mecha_type, timestamp, is_share, fashion, seat_name)


def leave_mecha(synchronizer, off_point, timestamp, is_die, is_share=False):
    synchronizer.send_event('E_ON_LEAVE_MECHA_START', off_point, timestamp, is_die, is_share)


def destroy_mecha(synchronizer, is_revive):
    synchronizer.send_event('E_SET_RECHOOSE_MECHA', is_revive)


def add_passenger(synchronizer, pid, seat):
    synchronizer.send_event('E_ADD_PASSENGER', pid, seat)


def remove_passenger(synchronizer, pid):
    synchronizer.send_event('E_REMOVE_PASSENGER', pid)


def mecha_reduce_injure(synchronizer, arm_injure, leg_injure):
    synchronizer.send_event('E_REDUCE_MECHA_INJURE', arm_injure, leg_injure)


def mecha_injure(synchronizer, part, injure):
    synchronizer.send_event('E_MECHA_INJURE', part, injure)


def on_mecha_repair_energy(synchronizer, energy):
    synchronizer.send_event('E_MECHA_REPAIR_ENERGY', energy)


def recall_cd(synchronizer, cd_type, recall_cd, left_time, cd_rate):
    synchronizer.send_event('E_STATE_CHANGE_CD', cd_type, recall_cd, left_time)


def on_mecha_info_change(synchronizer, new_info):
    if 'hp' in new_info and 'max_hp' in new_info:
        synchronizer.send_event('E_MECHA_HP_CHANGE', new_info['hp'], new_info['max_hp'])
    elif 'cur_exp' in new_info:
        synchronizer.send_event('E_MECHA_EXP_CHANGE', new_info['cur_exp'])
        synchronizer.send_event('S_ATTR_SET', 'mecha_exp', new_info['cur_exp'])


def recall_ret(synchronizer, ret, err_code=None):
    synchronizer.send_event('E_RECALL_SUCESS', ret, err_code)


def notify_kill_mecha(synchronizer, mecha_type):
    return
    from common.cfg import confmgr
    from logic.gcommon.common_utils.local_text import get_text_by_id
    mecha_conf = confmgr.get('mecha_conf', 'MechaConfig', 'Content')
    mecha_conf = mecha_conf[str(mecha_type)]
    name_text_id = mecha_conf.get('name_text_id', None)
    if name_text_id is None:
        return
    else:
        global_data.emgr.battle_show_message_event.emit(get_text_by_id(18539, {'mechaname': get_text_by_id(name_text_id)}))
        return


def on_mecha_transfrom(synchronizer, mecha_pattern):
    synchronizer.send_event('E_CHANGE_PATTERN', mecha_pattern)


def on_mecha_transfrom_failed(synchronizer, mecha_pattern):
    pass


def execute(synchronizer, trigger_id):
    synchronizer.send_event('E_EXECUTE', trigger_id)


def mecha_upgrade(synchronizer, cur_exp):
    synchronizer.send_event('E_MECHA_UPGRADE', cur_exp)


def on_new_reinfrce_cards(synchronizer, new_cards):
    synchronizer.send_event('E_GEN_REINFORCE_CARD', new_cards)


def on_use_reinforce_card(synchronizer, card_id):
    synchronizer.send_event('E_USE_REINFORCE_CARD', card_id)


def on_reinforce_coin_change(synchronizer, new_coin):
    synchronizer.send_event('E_REINFORCE_COIN_CHANGE', new_coin)


def on_heat_change(synchronizer, new_heat, heat_state):
    synchronizer.send_event('E_SET_HEAT', new_heat, heat_state)


def hit_flag_value(synchronizer, flag_id, new_value):
    synchronizer.send_event('E_HIT_FLAG_VALUE', flag_id, new_value)


def immobilize_value(synchronizer, new_value):
    synchronizer.send_event('E_IMMOBILIZE_VALUE', new_value)


def select_random_mecha(synchronizer, mecha_no):
    synchronizer.send_event('E_SELECT_RANDOM_MECHA', mecha_no)


def notify_create_mecha(synchronizer, mecha_no):
    if mecha_no:
        mecha_img_path = 'gui/ui_res_2/battle/notice/%s_mecha.png' % str(mecha_no)
        msg = '<img="%s">[%s] %s [%s]' % (mecha_img_path, synchronizer.ev_g_char_name(), get_text_by_id(18220), get_text_by_id(210000 + mecha_no))
        global_data.emgr.battle_show_message_event.emit(str(msg))


def on_flight_state_changed(synchronizer, state):
    synchronizer.send_event('E_SET_SERVER_FLIGHT_STATE', state)


def notify_fuel_exhausted(synchronizer):
    if hasattr(global_data, 'no_cd') and global_data.no_cd:
        return
    synchronizer.send_event('E_FUEL_EXHAUSTED')


def notify_skill_fuel_exhausted(synchronizer, skill_id):
    if hasattr(global_data, 'no_cd') and global_data.no_cd:
        return
    synchronizer.send_event('E_SKILL_FUEL_EXHAUSTED', skill_id)


def trio_transform(synchronizer, state):
    synchronizer.send_event('E_TRIO_TRANS_STATE', state)


def trio_dash(synchronizer, is_firepower, total_time=0, finish_timestamp=0):
    synchronizer.send_event('E_ENTER_FIREPOWER', is_firepower, total_time, finish_timestamp)


def trans_create_mecha_to_share(synchronizer):
    synchronizer.send_event('E_TRANS_CREATE_MECHA_TO_SHARE')


def wind_dragon_shield(synchronizer, *args):
    synchronizer.send_event('E_ENABLE_ABSORB_SHIELD', *args)


def rechoose_mecha_module_plan(synchronizer, mecha_id, new_module_plan):
    synchronizer.send_event('E_RECHOOSE_MECHA_MODULE_PLAN', mecha_id, new_module_plan)


def set_vehicle_owner(synchronizer, owner_id):
    synchronizer.send_event('E_SET_MOVE_CONTROLLER', owner_id)


def on_switch_defend(synchronizer, defend_state, ret):
    synchronizer.send_event('E_SWITCH_DEFEND', defend_state, ret)


def on_try_switch_defend(synchronizer, defend_state):
    synchronizer.send_event('E_TRY_SWITCH_DEFEND', defend_state)


def on_carry_shield_hp(synchronizer, hp):
    synchronizer.send_event('E_HANDY_SHIELD_HP', hp)


def on_light_cake_energy_change(synchronizer, energy):
    synchronizer.send_event('E_LIGHT_CAKE_ENERGY_CHANGE', energy)


def on_carry_shield_max_hp_change(synchronizer, max_hp):
    synchronizer.send_event('E_MAX_SHIELD_HP_CHANGE', max_hp)


def enhance_8021_second_weapon(synchronizer, enhance_timestamp):
    synchronizer.send_event('E_ENHANCE_8021_SEC_WP', enhance_timestamp)


def on_switch_8023_weapon_form(synchronizer, weapon_form):
    synchronizer.send_event('E_8023_SWITCH_WEAPON_FORM', weapon_form)


def on_switch_8023_visiblity(synchronizer, is_invisible, left_invisible_time=0):
    synchronizer.send_event('E_8023_SWITCH_VISIBLE', is_invisible, left_invisible_time)


def enable_8023_powerful_snipe(synchronizer, enable):
    synchronizer.send_event('E_8023_POWERFUL_SNIPE', enable)


def on_change_car_mode(synchronizer, mode):
    synchronizer.send_event('E_SWITCH_CAR_MODE', mode)


def priv_enjoy_free_cnt_change(synchronizer, cnt):
    synchronizer.send_event('E_PRIV_ENJOY_FREE_CNT_CHANGE', cnt)


def on_8026_shield_change(synchronizer, shield_state):
    synchronizer.send_event('E_8026_SHIELD_CHANGE', shield_state)


def shiled_absorbed_damage(synchronizer, absorbed_damage):
    synchronizer.send_event('E_SHILED_ABSORBED_DAMAGE', absorbed_damage)


def on_8028_energy_change(synchronizer, old_cnt, new_cnt):
    synchronizer.send_event('E_8028_ENERGY_CHANGE', old_cnt, new_cnt)


def on_8028_form_change(synchronizer, form):
    synchronizer.send_event('E_8028_FORM_CHANGE', form)


def on_phantom_start_destroy(synchronizer):
    synchronizer.send_event('E_8029_PHANTOM_START_DESTROY')


def set_phantom_pos(synchronizer, posx, posy, posz):
    synchronizer.send_event('E_SET_PHANTOM_POS', (posx, posy, posz))


def join_tvml_ret(synchronizer, tvml_eid):
    synchronizer.send_event('E_START_CONTROL_TV_MISSILE_LAUNCHER', tvml_eid)


def leave_tvml_ret(synchronizer, off_point):
    synchronizer.send_event('E_STOP_CONTROL_TV_MISSILE_LAUNCHER', off_point)


def tvml_add_player(synchronizer, player_id):
    synchronizer.send_event('E_ADD_CONTROLLER', player_id)


def tvml_remove_player(synchronizer, player_id, off_point):
    synchronizer.send_event('E_REMOVE_CONTROLLER', player_id, off_point)


def on_8031_skill_restore(synchronizer):
    synchronizer.send_event('E_SHOW_DASH_CURE_SFX')


def on_mecha_execute(synchronizer, target_eid):
    synchronizer.send_event('E_DO_EXECUTE_APPEARANCE', target_eid)
    executed_entity = global_data.battle.get_entity(target_eid)
    if executed_entity and executed_entity.logic:
        executed_entity.logic.send_event('E_BE_EXECUTED', synchronizer.unit_obj.id)


def on_8032_stab_mecha(synchronizer, attack_eid, target_eid, state):
    from logic.client.const.game_mode_const import GAME_MODE_EXERCISE
    if not global_data.battle:
        return
    else:
        if global_data.game_mode and global_data.game_mode.is_mode_type(GAME_MODE_EXERCISE):
            return
        followed_entity = global_data.battle.get_entity(attack_eid)
        follower_entity = global_data.battle.get_entity(target_eid)
        if followed_entity and followed_entity.logic and follower_entity and follower_entity.logic:
            if state == True:
                followed_entity.logic.send_event('E_FOLLOW_MECHA', target_eid, attack_eid)
                follower_entity.logic.send_event('E_FOLLOW_MECHA', target_eid, attack_eid)
            else:
                followed_entity.logic.send_event('E_FOLLOW_MECHA', None, None)
                follower_entity.logic.send_event('E_FOLLOW_MECHA', None, None)
            followed_entity.logic.send_event('E_ENABLE_FOLLOW', state)
            follower_entity.logic.send_event('E_ENABLE_FOLLOW', state)
        return


def update_ik_solver_enable_dict(synchronizer, enable_dict):
    for key, value in enable_dict.items():
        enable_dict[key] = tuple(value)

    synchronizer.send_event('E_ENABLE_MECHA_FOOT_IK_BY_MAP', enable_dict, False)


def on_8033_scan(synchronizer, mecha_eids):
    global_data.emgr.mecha_8033_scan.emit(mecha_eids)


def on_8013_force_full_shoot(synchronizer, cnt):
    synchronizer.send_event('E_8013_FORCE_FULL_SHOOT', cnt)


def on_custom_8013_accumulate_levels_and_max_time(synchronizer, levels, max_time, pos_list):
    synchronizer.send_event('E_SET_WEAPON_ACCUMULATE_LEVEL', levels, max_time, pos_list)


def on_hit_8023_phantom(synchronizer, phantom_id, is_destroy):
    phantom_unit = global_data.battle.get_entity(phantom_id)
    if phantom_unit and phantom_unit.logic:
        global_data.emgr.player_make_damage_event.emit(phantom_unit.logic, None)
    return