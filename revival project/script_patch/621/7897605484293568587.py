# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gutils/mecha_skill_utils.py
from __future__ import absolute_import
from __future__ import print_function
import six
from logic.gutils.weapon_utils import get_weapon_conf, get_pve_weapon_conf
from common.cfg import confmgr
from logic.gcommon.common_const import weapon_const
from logic.gcommon.common_const import mecha_const
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gcommon.common_const.weapon_const import WP_LASER_SHOOTER, WP_MULTI_RAY_SHOOT, WP_MULTI_RAY_LASER_SHOOTER, WP_RAY_GRENADES_GUN
from decimal import Decimal
MIN_MECHA_HP_PERCENT = 40
MAX_MECHA_HP_PERCENT = 90
MIN_MECHA_FUEL_PERCENT = 40
MAX_MECHA_FUEL_PERCENT = 90
MIN_MECHA_SHIELD_PERCENT = 40
MAX_MECHA_SHIELD_PERCENT = 90
EXTREME_SPEED_WEAPON_KINDS = (
 WP_LASER_SHOOTER, WP_MULTI_RAY_SHOOT, WP_MULTI_RAY_LASER_SHOOTER, WP_RAY_GRENADES_GUN)

def get_mecha_speciality_desc_str(mecha_id):
    conf = confmgr.get('mecha_display', 'HangarConfig', 'Content')
    desc_conf = confmgr.get('mecha_display', 'HangarDescConf', 'Content')
    speciality_tag_list = conf[str(mecha_id)].get('desc_speciality')
    speciality_txt_list = []
    for tag in speciality_tag_list:
        tag_text_id = desc_conf.get(tag, {}).get('tag_name_text_id')
        speciality_txt_list.append(get_text_by_id(tag_text_id))

    return '/'.join(speciality_txt_list)


def get_lobby_mecha_hp_percent(mecha_id):
    mecha_conf = confmgr.get('mecha_conf', 'MechaConfig', 'Content')
    min_hp = 9999999
    max_hp = -1
    for _, mecha_info in six.iteritems(mecha_conf):
        mecha_type = mecha_info.get('mecha_type')
        if mecha_type == mecha_const.MECHA_TYPE_VEHICLE:
            continue
        cur_hp = mecha_info.get('health', 0)
        if cur_hp < min_hp:
            min_hp = cur_hp
        if cur_hp > max_hp:
            max_hp = cur_hp

    if max_hp == min_hp:
        return (MIN_MECHA_HP_PERCENT + MAX_MECHA_HP_PERCENT) / 2
    cur_mecha_info = mecha_conf.get(str(mecha_id))
    cur_mecha_hp = cur_mecha_info.get('health', 0)
    return 1.0 * (cur_mecha_hp - min_hp) / (max_hp - min_hp) * (MAX_MECHA_HP_PERCENT - MIN_MECHA_HP_PERCENT) + MIN_MECHA_HP_PERCENT


def get_lobby_mecha_fuel_percent(mecha_id):
    mecha_fuel_conf = confmgr.get('mecha_conf', 'FuelConfig', 'Content')
    min_fuel = 99999999
    max_fuel = -1
    for _, fuel_conf in six.iteritems(mecha_fuel_conf):
        cur_fuel = fuel_conf.get('max_fuel', 0)
        if cur_fuel < min_fuel:
            min_fuel = cur_fuel
        if cur_fuel > max_fuel:
            max_fuel = cur_fuel

    if max_fuel == min_fuel:
        return (MIN_MECHA_FUEL_PERCENT + MAX_MECHA_FUEL_PERCENT) / 2
    cur_mecha_info = mecha_fuel_conf.get(str(mecha_id))
    cur_mecha_fuel = cur_mecha_info.get('max_fuel', 0)
    return 1.0 * (cur_mecha_fuel - min_fuel) / (max_fuel - min_fuel) * (MAX_MECHA_FUEL_PERCENT - MIN_MECHA_FUEL_PERCENT) + MIN_MECHA_FUEL_PERCENT


def get_lobby_mecha_shield_percent(mecha_id):
    mecha_shield_conf = confmgr.get('mecha_conf', 'ShieldConfig', 'Content')
    min_shield = 99999999
    max_shield = -1
    for _, shield_conf in six.iteritems(mecha_shield_conf):
        cur_shield = shield_conf.get('max_shield', 0)
        if cur_shield < min_shield:
            min_shield = cur_shield
        if cur_shield > max_shield:
            max_shield = cur_shield

    if max_shield == min_shield:
        return (MIN_MECHA_SHIELD_PERCENT + MAX_MECHA_SHIELD_PERCENT) / 2
    cur_mecha_info = mecha_shield_conf.get(str(mecha_id))
    cur_mecha_shield = cur_mecha_info.get('max_shield', 0)
    return 1.0 * (cur_mecha_shield - min_shield) / (max_shield - min_shield) * (MAX_MECHA_SHIELD_PERCENT - MIN_MECHA_SHIELD_PERCENT) + MIN_MECHA_SHIELD_PERCENT


def get_mecha_weapon_speed_tag(weapon_id):
    grenade_conf = confmgr.get('grenade_config', str(weapon_id), default={})
    firearm_conf = confmgr.get('firearm_config', str(weapon_id), default={})
    wp_kind = firearm_conf.get('iKind', None)
    fly_speed = grenade_conf.get('fSpeed', None)
    if wp_kind in EXTREME_SPEED_WEAPON_KINDS and not fly_speed:
        return 'weapon_speed_lv_3'
    else:
        if not fly_speed:
            return 'weapon_speed_lv_3'
        min_speed, max_speed = get_all_mecha_weapon_speed_range()
        if min_speed == max_speed:
            return 'weapon_speed_lv_1'
        ratio = (fly_speed - min_speed) / (max_speed - min_speed)
        if ratio < 0.3:
            return 'weapon_speed_lv_0'
        if ratio < 0.6:
            return 'weapon_speed_lv_1'
        return 'weapon_speed_lv_2'
        return


def get_all_mecha_weapon_speed_range():
    min_speed = 9999999
    max_speed = -1
    weapon_conf = confmgr.get('grenade_config')
    mecha_conf = confmgr.get('mecha_conf', 'MechaConfig', 'Content')
    for mecha_id, mecha_info in six.iteritems(mecha_conf):
        mecha_type = mecha_info.get('mecha_type')
        if mecha_type == mecha_const.MECHA_TYPE_VEHICLE:
            continue
        guns = mecha_info.get('guns', [])
        for gun_id in guns:
            gun_conf = weapon_conf.get(str(gun_id), {})
            fly_speed = gun_conf.get('fSpeed', None)
            if not fly_speed:
                continue
            if fly_speed < min_speed:
                min_speed = fly_speed
            if fly_speed > max_speed:
                max_speed = fly_speed

    return (
     min_speed, max_speed)


def get_mecha_weapon_damage_tag(weapon_id):
    weapon_conf = confmgr.get('grenade_config', str(weapon_id), default={})
    dmg_type = weapon_conf.get('fDamage', None)
    if dmg_type is None:
        return 'damage_type_direct'
    else:
        if dmg_type == weapon_const.THROWABLE_DAMAGE_TARGET:
            return 'damage_type_direct'
        if dmg_type == weapon_const.THROWABLE_DAMAGE_COMMON:
            return 'damage_type_range'
        return
        return


def get_mecha_weapon_clip_size(weapon_id):
    weapon_conf = get_weapon_conf(weapon_id)
    show_ratio = weapon_conf.get('fShowRatio', 1)
    if show_ratio >= 0:
        return weapon_conf.get('iMagSize', 0) * show_ratio
    else:
        return weapon_conf.get('iMagSize', 0) / show_ratio * -1


def get_mecha_8002_main_weapon_clip_size(*args):
    skill_conf = confmgr.get('skill_conf', '800251', default={})
    max_mp = skill_conf.get('max_mp', None)
    inc_mp = skill_conf.get('cost_mp', None)
    if abs(inc_mp) < 1e-05:
        return 0
    else:
        return int(max_mp / inc_mp)


def get_mecha_weapon_shoot_rate(weapon_id):
    weapon_conf = get_weapon_conf(weapon_id)
    shoot_rate = weapon_conf.get('fCDTime', 1)
    if abs(shoot_rate) > 1e-05:
        cnt_per_sec = str(round(Decimal(1 / shoot_rate), 1))
    else:
        cnt_per_sec = 0
    return get_text_by_id(607564).format(cnt_per_sec)


def get_mecha_weapon_reload_time(weapon_id):
    weapon_conf = get_weapon_conf(weapon_id)
    reload_time = weapon_conf.get('fReloadTimeEmpty', 0)
    return '%.1f' % reload_time + get_text_by_id(18534)


def get_mecha_skill_cost_fuel(skill_id):
    skill_conf = confmgr.get('skill_conf', str(skill_id))
    return skill_conf.get('cost_fuel', 0)


def get_mecha_skill_cost_fuel_per_time(skill_id):
    cost = get_mecha_skill_cost_fuel(skill_id)
    return get_text_by_id(607557).format(cost)


def get_mecha_skill_cost_fuel_per_second(skill_id):
    cost = get_mecha_skill_cost_fuel(skill_id)
    return get_text_by_id(607558).format(cost)


def get_mecha_skill_cd_time(skill_id):
    skill_conf = confmgr.get('skill_conf', str(skill_id), default={})
    max_mp = skill_conf.get('max_mp', None)
    inc_mp = skill_conf.get('inc_mp', None)
    if not max_mp or not inc_mp:
        cd_time = '0'
    else:
        cd_time = '%.1f' % (1.0 * max_mp / inc_mp)
    return cd_time + get_text_by_id(18534)


def get_mecha_8006_rush_duration(*args):
    conf = confmgr.get('c_buff_data', '340', default={})
    duration = conf.get('Duration', 0)
    return str(duration) + get_text_by_id(18534)


def get_mecha_8008_shield_duration(*args):
    skill_conf = confmgr.get('skill_conf', '800855', default={})
    ext_info = skill_conf.get('ext_info', {})
    building_no = ext_info.get('building_id', 6025)
    building_info = confmgr.get('c_building_res', str(building_no), default={})
    duration = building_info.get('LifeTime', 0)
    return str(duration) + get_text_by_id(18534)


def get_mecha_8008_shield_hp(*args):
    skill_conf = confmgr.get('skill_conf', '800855', default={})
    ext_info = skill_conf.get('ext_info', {})
    building_no = ext_info.get('building_id', 6025)
    building_info = confmgr.get('c_building_data', str(building_no), default={})
    return building_info.get('HpMax', 0)


def get_mecha_weapon_accu_time(weapon_id):
    accumulate_config = confmgr.get('accumulate_config', str(weapon_id), default={})
    accu_time = accumulate_config.get('fMaxCD', 0)
    return str(accu_time) + get_text_by_id(18534)


def get_mecha_8002_main_weapon_accu_speed(*args):
    skill_conf = confmgr.get('skill_conf', '800251', default={})
    inc_mp = skill_conf.get('inc_mp', None)
    cost_mp = skill_conf.get('cost_mp', None)
    if not inc_mp or not cost_mp:
        speed = '0'
    else:
        speed = '%.1f' % (inc_mp / cost_mp)
    return get_text_by_id(607559).format(speed)


def get_mecha_second_weapon_full_dmg(weapon_id):
    firearm_conf = confmgr.get('firearm_config', str(weapon_id), default={})
    gun_damage_conf = confmgr.get('c_gun_data', str(weapon_id), default={})
    pellets = firearm_conf.get('iPellets')
    if isinstance(pellets, dict):
        bullet_num = sum(pellets.get('bullets', []))
    elif isinstance(pellets, int):
        bullet_num = pellets
    else:
        bullet_num = 1
    base_dmg = gun_damage_conf.get('iBasePower', 0)
    dmg_factor = gun_damage_conf.get('fNonCharFactor', 0)
    return int(bullet_num * base_dmg * dmg_factor)


def get_mecha_8002_second_weapon_full_dmg(*args):
    skill_conf = confmgr.get('skill_conf', '800252', default={})
    ext_info = skill_conf.get('ext_info', {})
    continue_cnt = ext_info.get('continue_count', 3)
    other_dmg = skill_conf.get('other_damage', 0)
    return int(continue_cnt * int(other_dmg))


def get_mecha_8005_rocket_jump_full_dmg(*args):
    gun_damage_conf = confmgr.get('c_gun_data', '8205', default={})
    base_dmg = gun_damage_conf.get('iBasePower', 0)
    dmg_factor = gun_damage_conf.get('fNonCharFactor', 0)
    return int(base_dmg * dmg_factor)


def get_mecha_8004_rush_full_dmg(*args):
    dis = 0
    skill_conf = confmgr.get('skill_conf', '800451', default={})
    other_dmg = skill_conf.get('other_damage', '0')
    return eval(other_dmg)


def get_mecha_8003_second_weapon_full_dmg(*args):
    dmg1 = get_mecha_second_weapon_full_dmg('800302')
    conf = confmgr.get('c_buff_data', '113')
    dmg2 = conf.get('ExtInfo', {}).get('damage', 0)
    return dmg1 + dmg2


def get_mecha_8009_rush_full_dmg(*args):
    weapon_list = [
     800904, 800905, 800906, 800908]
    skill_conf = confmgr.get('skill_conf', '800952', default={})
    lasting_time = int(skill_conf.get('ext_info', {}).get('lasting_time', 0))
    firearm_conf = confmgr.get('firearm_config', default={})
    total_dmg = 0
    for weapon_id in weapon_list:
        shoot_rate = firearm_conf.get(str(weapon_id), {}).get('fCDTime', -1)
        one_time_dmg = get_mecha_second_weapon_full_dmg(weapon_id)
        if abs(shoot_rate) > 1e-05:
            shoot_times = lasting_time / shoot_rate
        else:
            shoot_times = 0
        total_dmg += shoot_times * one_time_dmg

    return int(total_dmg)


def get_mecha_8012_bump_full_dmg(*args):
    skill_conf = confmgr.get('skill_conf', '801255', default={})
    buff_conf = confmgr.get('c_buff_data', '403', default={})
    ext_info = skill_conf.get('ext_info', {})
    other_damge_speed_factor = ext_info.get('other_damage_speed_factor', 50)
    max_speed = ext_info.get('max_speed', 20)
    buff_damage_factor = buff_conf.get('damage_factor', 1)
    return int(other_damge_speed_factor * max_speed * buff_damage_factor)


def get_mecha_8012_second_weapon_full_dmg(*args):
    skill_conf = confmgr.get('skill_conf', '801257', default={})
    max_mp = skill_conf.get('max_mp', 0)
    cost_mp = skill_conf.get('cost_mp', 1)
    cost_mp_pre = skill_conf.get('cost_mp_pre', 0)
    lasting_time = float(max_mp - cost_mp_pre) / cost_mp
    fire_cd = confmgr.get('firearm_config', '801203', 'fCDTime', default=0.1)
    gun_damage_conf = confmgr.get('c_gun_data', '801203', default={})
    one_damage = gun_damage_conf.get('iBasePower', 0) * gun_damage_conf.get('fNonCharFactor', 0)
    total_damage = (lasting_time / fire_cd + 1) * one_damage
    return int(total_damage)


def get_mecha_8013_second_weapon_full_dmg(*args):
    weapon_id_1 = 801304
    weapon_id_2 = 801305
    full_dmg = 0
    gun_damage_conf = confmgr.get('c_gun_data', str(weapon_id_1), default={})
    base_dmg = gun_damage_conf.get('iBasePower', 0)
    dmg_factor = gun_damage_conf.get('fNonCharFactor', 0)
    print(base_dmg, dmg_factor)
    full_dmg += base_dmg * dmg_factor
    gun_damage_conf = confmgr.get('c_gun_data', str(weapon_id_2), default={})
    base_dmg = gun_damage_conf.get('iBasePower', 0)
    dmg_factor = gun_damage_conf.get('fNonCharFactor', 0)
    print(base_dmg, dmg_factor)
    full_dmg += base_dmg * dmg_factor * 2
    return full_dmg * 3


def get_mecha_8014_second_weapon_full_dmg(*args):
    import math
    from logic.gcommon.cdata.mecha_status_config import MC_BLADE_SLASH
    from logic.gcommon.common_utils import status_utils
    data = status_utils.get_behavior_config('8014')
    behavior = data.get_behavior('8014')
    skill_conf = confmgr.get('skill_conf', '801451', default={})
    other_dmg = skill_conf.get('other_damage', [])
    other_dmg = eval(other_dmg)
    one_round_dmg = sum(other_dmg)
    lasting_time = confmgr.get('skill_conf', '801456', default={}).get('ext_info', {}).get('lasting_time', 0)
    MC_BLADE_SLASH_CONF = behavior.get(MC_BLADE_SLASH, {})
    slash_param_conf = MC_BLADE_SLASH_CONF.get('custom_param', {}).get('slash_param_list', [])
    one_round_time = 0
    for param in slash_param_conf:
        one_round_time += param.get('combo_time', 0)

    if abs(one_round_time) > 1e-05:
        round_cnt = math.ceil(lasting_time / one_round_time)
    else:
        round_cnt = 0
    return int(round_cnt * one_round_dmg)


def get_mecha_8015_second_weapon_full_dmg(*args):
    return get_mecha_second_weapon_full_dmg('801502') * 2


def get_mecha_8016_second_weapon_full_dmg(*args):
    try:
        skill_conf = confmgr.get('skill_conf', '801651', default={})
        other_dmg = skill_conf.get('other_damage', 0)
        other_dmg = eval(other_dmg)
        first_other_damage = skill_conf.get('ext_info', {}).get('first_other_damage', 0)
        max_hit_duration = skill_conf.get('ext_info', {}).get('max_hit_duration', 0)
        hit_interval = skill_conf.get('ext_info', {}).get('hit_interval', 1)
        if abs(hit_interval) > 1e-05:
            hit_times = int(max_hit_duration / hit_interval) - 1
        else:
            hit_times = 0
        return other_dmg * hit_times + first_other_damage
    except:
        return 0


def get_mecha_8016_dash_cd_time(*args):
    from logic.gcommon.cdata.mecha_status_config import MC_FLIGHT_BOOST
    from logic.gcommon.common_utils import status_utils
    data = status_utils.get_behavior_config('8016')
    behavior = data.get_behavior('8016')
    MC_FLIGHT_BOOST_CONF = behavior.get(MC_FLIGHT_BOOST, {})
    action_cd = MC_FLIGHT_BOOST_CONF.get('custom_param', {}).get('action_cd', 1)
    return action_cd


def get_mecha_8028_fairy_second_weapon_full_dmg(*args):
    skill_conf = confmgr.get('skill_conf', '802857', default={})
    ext_info = skill_conf.get('ext_info', {})
    dmg_decay = ext_info.get('dmg_decay', [])
    full_dmg = 0
    gun_damage_conf = confmgr.get('c_gun_data', str(802805), default={})
    base_dmg = gun_damage_conf.get('iBasePower', 0)
    dmg_factor = gun_damage_conf.get('fNonCharFactor', 0)
    one_dmg = base_dmg * dmg_factor
    for idx, decay in enumerate(dmg_decay):
        if idx == 0:
            continue
        full_dmg += one_dmg * (1.0 + decay)

    return full_dmg


def get_pve_mecha_weapon_clip_size(weapon_id):
    weapon_conf = get_pve_weapon_conf(weapon_id)
    show_ratio = weapon_conf.get('fShowRatio', 1)
    if show_ratio >= 0:
        return weapon_conf.get('iMagSize', 0) * show_ratio
    else:
        return weapon_conf.get('iMagSize', 0) / show_ratio * -1


def get_pve_mecha_8002_main_weapon_clip_size(*args):
    skill_conf = confmgr.get('pve/diff/skill_conf', '800251', default={})
    if not skill_conf:
        skill_conf = confmgr.get('skill_conf', '800251')
    max_mp = skill_conf.get('max_mp', None)
    inc_mp = skill_conf.get('cost_mp', None)
    if abs(inc_mp) < 1e-05:
        return 0
    else:
        return int(max_mp / inc_mp)


def get_pve_mecha_skill_cd_time(skill_id):
    skill_conf = confmgr.get('pve/diff/skill_conf', str(skill_id), default={})
    if not skill_conf:
        skill_conf = confmgr.get('skill_conf', str(skill_id))
    max_mp = skill_conf.get('max_mp', None)
    inc_mp = skill_conf.get('inc_mp', None)
    if not max_mp or not inc_mp:
        cd_time = '0'
    else:
        cd_time = '%.1f' % (1.0 * max_mp / inc_mp)
    return cd_time


def get_pve_mecha_8006_rush_duration(*args):
    conf = confmgr.get('pve/diff/c_buff_data', '340', default={})
    if not conf:
        conf = confmgr.get('c_buff_data', '340', default={})
    duration = conf.get('Duration', 0)
    return str(duration) + get_text_by_id(18534)


def get_pve_mecha_skill_cost_fuel(skill_id):
    skill_conf = confmgr.get('pve/diff/skill_conf', str(skill_id))
    if not skill_conf:
        skill_conf = confmgr.get('skill_conf', str(skill_id))
    return skill_conf.get('cost_fuel', 0)


def get_pve_mecha_skill_cost_fuel_per_time(skill_id):
    cost = get_pve_mecha_skill_cost_fuel(skill_id)
    return get_text_by_id(607557).format(cost)


def get_pve_mecha_skill_cost_fuel_per_second(skill_id):
    cost = get_pve_mecha_skill_cost_fuel(skill_id)
    return get_text_by_id(607558).format(cost)


def get_pve_mecha_main_dmg--- This code section failed: ---

 638       0  LOAD_GLOBAL           0  'type'
           3  LOAD_FAST             0  'data'
           6  CALL_FUNCTION_1       1 
           9  LOAD_GLOBAL           1  'list'
          12  COMPARE_OP            2  '=='
          15  POP_JUMP_IF_FALSE    39  'to 39'

 640      18  POP_JUMP_IF_FALSE     1  'to 1'
          21  BINARY_SUBSCR    
          22  STORE_FAST            1  'mecha_id'

 642      25  STORE_FAST            2  'main_atk_ratio_index'
          28  BINARY_SUBSCR    
          29  LOAD_CONST            2  1
          32  BINARY_SUBTRACT  
          33  STORE_FAST            2  'main_atk_ratio_index'
          36  JUMP_FORWARD         12  'to 51'

 645      39  LOAD_FAST             0  'data'
          42  STORE_FAST            1  'mecha_id'

 646      45  LOAD_CONST            1  ''
          48  STORE_FAST            2  'main_atk_ratio_index'
        51_0  COME_FROM                '36'

 647      51  LOAD_GLOBAL           2  'confmgr'
          54  LOAD_ATTR             3  'get'
          57  LOAD_CONST            3  'mecha_init_data'
          60  LOAD_GLOBAL           4  'str'
          63  LOAD_FAST             1  'mecha_id'
          66  CALL_FUNCTION_1       1 
          69  LOAD_CONST            4  'default'
          72  BUILD_MAP_0           0 
          75  CALL_FUNCTION_258   258 
          78  STORE_FAST            3  'mecha_init_data'

 648      81  LOAD_FAST             3  'mecha_init_data'
          84  LOAD_ATTR             3  'get'
          87  LOAD_CONST            5  'main_atk_ratio'
          90  LOAD_CONST            2  1
          93  BUILD_LIST_1          1 
          96  CALL_FUNCTION_2       2 
          99  STORE_FAST            4  'main_atk_ratio_list'

 649     102  LOAD_FAST             4  'main_atk_ratio_list'
         105  LOAD_FAST             2  'main_atk_ratio_index'
         108  BINARY_SUBSCR    
         109  STORE_FAST            5  'main_atk_ratio'

 650     112  LOAD_CONST            6  '{}%'
         115  LOAD_ATTR             5  'format'
         118  LOAD_GLOBAL           6  'int'
         121  LOAD_FAST             5  'main_atk_ratio'
         124  LOAD_CONST            7  100
         127  BINARY_MULTIPLY  
         128  CALL_FUNCTION_1       1 
         131  CALL_FUNCTION_1       1 
         134  STORE_FAST            6  'main_atk_ratio_str'

 651     137  LOAD_FAST             3  'mecha_init_data'
         140  LOAD_ATTR             3  'get'
         143  LOAD_CONST            8  'atk'
         146  LOAD_CONST            1  ''
         149  CALL_FUNCTION_2       2 
         152  STORE_FAST            7  'base_atk'

 652     155  LOAD_GLOBAL           7  'global_data'
         158  LOAD_ATTR             8  'player'
         161  POP_JUMP_IF_FALSE   182  'to 182'
         164  LOAD_GLOBAL           7  'global_data'
         167  LOAD_ATTR             8  'player'
         170  LOAD_ATTR             9  'get_mecha_level_by_id'
         173  LOAD_FAST             1  'mecha_id'
         176  CALL_FUNCTION_1       1 
         179  JUMP_FORWARD          3  'to 185'
         182  LOAD_CONST            1  ''
       185_0  COME_FROM                '179'
         185  STORE_FAST            8  'mecha_level'

 653     188  LOAD_FAST             3  'mecha_init_data'
         191  LOAD_ATTR             3  'get'
         194  LOAD_CONST            9  'up_atk'
         197  LOAD_CONST            1  ''
         200  CALL_FUNCTION_2       2 
         203  LOAD_FAST             8  'mecha_level'
         206  BINARY_MULTIPLY  
         207  STORE_FAST            9  'add_atk'

 654     210  LOAD_GLOBAL          10  'get_text_by_id'
         213  LOAD_CONST           10  433
         216  CALL_FUNCTION_1       1 
         219  LOAD_ATTR             5  'format'
         222  LOAD_GLOBAL           6  'int'
         225  LOAD_FAST             7  'base_atk'
         228  LOAD_FAST             9  'add_atk'
         231  BINARY_ADD       
         232  LOAD_FAST             5  'main_atk_ratio'
         235  BINARY_MULTIPLY  
         236  CALL_FUNCTION_1       1 
         239  LOAD_FAST             6  'main_atk_ratio_str'
         242  CALL_FUNCTION_2       2 
         245  RETURN_VALUE     
          -1  RETURN_LAST      

Parse error at or near `POP_JUMP_IF_FALSE' instruction at offset 18


def get_pve_mecha_sec_dmg(mecha_id):
    mecha_init_data = confmgr.get('mecha_init_data', str(mecha_id), default={})
    sec_atk_ratio = mecha_init_data.get('sec_ratio', {}).get('atk', 1)
    sec_atk_ratio = float(sec_atk_ratio)
    sec_atk_ratio_str = '{}%'.format(int(sec_atk_ratio * 100))
    base_atk = mecha_init_data.get('atk', 0)
    mecha_level = global_data.player.get_mecha_level_by_id(mecha_id) if global_data.player else 0
    add_atk = mecha_init_data.get('up_atk', 0) * mecha_level
    return get_text_by_id(433).format(int((base_atk + add_atk) * sec_atk_ratio), sec_atk_ratio_str)


def get_pve_mecha_sec_shield(mecha_id):
    mecha_init_data = confmgr.get('mecha_init_data', str(mecha_id), default={})
    sec_shield_ratio = mecha_init_data.get('sec_ratio', {}).get('shield', 1)
    sec_shield_ratio = float(sec_shield_ratio)
    sec_shield_ratio_str = '{}%'.format(int(sec_shield_ratio * 100))
    base_shield = mecha_init_data.get('shield', 0)
    mecha_level = global_data.player.get_mecha_level_by_id(mecha_id) if global_data.player else 0
    add_shield = mecha_init_data.get('up_shield', 0) * mecha_level
    return get_text_by_id(434).format(int((base_shield + add_shield) * sec_shield_ratio), sec_shield_ratio_str)


def get_pve_mecha_tactic_dmg(mecha_id):
    mecha_init_data = confmgr.get('mecha_init_data', str(mecha_id), default={})
    tactic_atk_ratio = mecha_init_data.get('tactic_ratio', {}).get('atk', 1)
    tactic_atk_ratio = float(tactic_atk_ratio)
    tactic_atk_ratio_str = '{}%'.format(int(tactic_atk_ratio * 100))
    base_atk = mecha_init_data.get('atk', 0)
    mecha_level = global_data.player.get_mecha_level_by_id(mecha_id) if global_data.player else 0
    add_atk = mecha_init_data.get('up_atk', 0) * mecha_level
    return get_text_by_id(433).format(int((base_atk + add_atk) * tactic_atk_ratio), tactic_atk_ratio_str)


def get_pve_mecha_tactic_shield(mecha_id):
    mecha_init_data = confmgr.get('mecha_init_data', str(mecha_id), default={})
    tactic_shield_ratio = mecha_init_data.get('tactic_ratio', {}).get('shield', 1)
    tactic_shield_ratio = float(tactic_shield_ratio)
    tactic_shield_ratio_str = '{}%'.format(int(tactic_shield_ratio * 100))
    base_shield = mecha_init_data.get('shield', 0)
    mecha_level = global_data.player.get_mecha_level_by_id(mecha_id) if global_data.player else 0
    add_shield = mecha_init_data.get('up_shield', 0) * mecha_level
    return get_text_by_id(434).format(int((base_shield + add_shield) * tactic_shield_ratio), tactic_shield_ratio_str)


def get_custom_clip_size(custom_val):
    if not custom_val:
        return 0
    return str(custom_val)


def get_custom_shoot_rate(custom_val):
    if not custom_val:
        return 0
    return get_text_by_id(607564).format(custom_val)


def get_custom_reload_time(custom_val):
    if not custom_val:
        return 0
    return str(custom_val) + get_text_by_id(18534)


def get_custom_cd_time(custom_val):
    if not custom_val:
        return 0
    return str(custom_val) + get_text_by_id(18534)


def get_custom_full_damage(custom_val):
    if not custom_val:
        return 0
    return custom_val