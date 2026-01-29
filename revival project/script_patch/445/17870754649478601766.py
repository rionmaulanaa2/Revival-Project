# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gutils/hitted_trk_utils.py
from __future__ import absolute_import
import six_ex
from common.cfg import confmgr
SCR_TRK_LV_1 = '1'
SCR_TRK_LV_2 = '2'
SCR_TRK_LV_3 = '3'
GUN_EF_LV_1 = 1
GUN_EF_LV_2 = 2
GUN_EF_LV_3 = 3

def get_gun_scr_lv(weapon_id, hit_parts, is_mecha, triger_is_mecha, by_screen_effect):
    from logic.gcommon import const
    from common.cfg import confmgr
    table_name = 'MechaFirearm' if is_mecha else 'HumanFirearm'
    gun_level = confmgr.get('firearm_config', str(weapon_id), default={}).get('iScreenLevel', GUN_EF_LV_1)
    is_headshot = 0
    if const.HIT_PART_HEAD in hit_parts:
        is_headshot = 1
    conf = confmgr.get('hitted_shake_conf', table_name, 'Content', default={})
    scr_effect_lv = conf.get(str(gun_level) + '_' + str(is_headshot), {}).get('ShakeLevel', SCR_TRK_LV_1)
    if not triger_is_mecha and is_mecha:
        scr_effect_lv = str(int(scr_effect_lv) - 1)
        if scr_effect_lv == '0' and by_screen_effect:
            scr_effect_lv = '1'
    return scr_effect_lv


def get_throwable_scr_lv(weapon_id, is_mecha, triger_is_mecha, by_screen_effect):
    from common.cfg import confmgr
    table_name = 'MechaThrow' if is_mecha else 'HumanThrow'
    throw_lv = confmgr.get('firearm_config', str(weapon_id), default={}).get('iScreenLevel', GUN_EF_LV_1)
    conf = confmgr.get('hitted_shake_conf', table_name, 'Content', default={})
    scr_effect_lv = conf.get(str(throw_lv), {}).get('ShakeLevel', SCR_TRK_LV_1)
    if not triger_is_mecha and is_mecha:
        scr_effect_lv = str(int(scr_effect_lv) - 1)
        if scr_effect_lv == '0' and by_screen_effect:
            scr_effect_lv = '1'
    return scr_effect_lv


def _get_other_damage_scr_lv(lentity, damage, is_mecha):
    from common.cfg import confmgr
    if not lentity:
        return
    else:
        max_hp = lentity.ev_g_max_hp()
        damage_percent = float(damage) / max_hp * 100.0
        table_name = 'MechaOther' if is_mecha else 'HumanOther'
        conf = confmgr.get('hitted_shake_conf', table_name, 'Content', default={})
        percent_list = sorted([ int(k) for k in six_ex.keys(conf) ])
        max_p = None
        for p in percent_list:
            if damage_percent <= p:
                break
            else:
                max_p = p

        scr_lv = conf.get(str(max_p), {}).get('ShakeLevel', None)
        return scr_lv


def get_show_dir(cur_pos, from_pos):
    import math
    if not from_pos or not cur_pos:
        return 'C_FRONT_HIT'
    vect = from_pos - cur_pos
    camera = global_data.game_mgr.scene.active_camera
    listener_look_at = camera.world_transformation.forward
    if listener_look_at.is_zero:
        return 'C_FRONT_HIT'
    import common.utilities
    cur_angle = common.utilities.vect2d_radian(listener_look_at, vect) * 180 / math.pi
    dic_table = {22.5: 'C_FRONT_HIT',
       67.5: 'C_FRONT_LEFT_HIT',
       112.5: 'C_POSITIVE_LEFT_HIT',
       157.5: 'C_REAR_LEFT_HIT',
       202.5: 'C_REAR_HIT',
       247.5: 'C_REAR_RIGHT_HIT',
       292.5: 'C_POSITIVE_RIGHT_HIT',
       337.5: 'C_FRONT_RIGHT_HIT',
       360.5: 'C_FRONT_HIT'
       }
    angles = sorted(six_ex.keys(dic_table))
    for ang in angles:
        if cur_angle <= ang:
            return dic_table[ang]

    return 'C_FRONT_HIT'