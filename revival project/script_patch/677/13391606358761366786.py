# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/common/cfg/confmgr.py
from __future__ import absolute_import
from __future__ import print_function
import six
from six.moves import range
from . import jsonconf
from common.utils.time_utils import get_time as now
import taggeddict
confs = {}
check_time = 0
LRU_TIME = 10
LRU_CHECK_TIME = 15
cur_conf_is_pve = False
pve_conf_set = set([
 'item',
 'box_res',
 'c_buff_data',
 'skill_conf',
 'monster_data',
 'firearm_config',
 'firearm_component',
 'grenade_config',
 'firearm_res_config',
 'firearm_res_mapping',
 'gun_attachment_attr',
 'grenade_res_config',
 'special_bullet_config',
 'field_data',
 'accumulate_config',
 'gun_harm_config',
 'shoot_rocker_config',
 'move_force_config',
 'c_gun_data',
 'firearm_aim_args',
 'fire_adsorb_args',
 'fire_aim_style',
 'gun_heat',
 'limited_bullet_weapon_config',
 'bless_data',
 'bless_element_data',
 'talent_cost_data',
 'talent_data',
 'talent_effect_data',
 'pve_loading_tips',
 'pve_level_conf',
 'pve_monster_sound',
 'item_use',
 'mecha_init_data',
 'story_data',
 'story_role_data',
 'story_text_data',
 'mecha_breakthrough_data',
 'mecha_upgrade_data',
 'mecha_upgrade_effect_data',
 'mecha_debris_data',
 'mecha_upgrade_cost_data',
 'pve_shop_data',
 'story_debris_chapter_data',
 'story_debris_clue_data',
 'story_debris_data',
 'monster_level_data',
 'pve_suggest_conf',
 'element_text_data',
 'c_pve_wp_shiny_sfx_map'])
pve_diff_set = {
 'c_gun_data',
 'firearm_config',
 'gun_harm_config',
 'skill_conf',
 'grenade_res_config',
 'firearm_res_config',
 'firearm_res_mapping',
 'hit_hint'}

def change_to_pve(is_pve):
    global confs
    global cur_conf_is_pve
    if cur_conf_is_pve ^ is_pve:
        cur_conf_is_pve = is_pve
        for ctype in pve_diff_set:
            confs.pop(ctype, None)
            init(ctype)

    return


def init(ctype, raw=False):
    if ctype in confs:
        return
    confs[ctype] = jsonconf.get_conf_data(ctype, raw)
    if ctype in pve_conf_set:
        confs[ctype].update(jsonconf.get_pve_conf_data(ctype, raw))
    if cur_conf_is_pve:
        diff = jsonconf.get_pve_diff_conf_data(ctype, False)
        confs[ctype].update(diff)


def refresh(ctype, raw=False):
    confs[ctype] = jsonconf.get_conf_data(ctype, raw)
    if ctype in pve_conf_set:
        confs[ctype].update(jsonconf.get_pve_conf_data(ctype, raw))


def preload(ctype):
    init(ctype)


def unload(ctype):
    if ctype in confs:
        del confs[ctype]


def exit():
    global confs
    confs = {}


def get(ctype, *args, **kargs):
    init(ctype)
    ret = confs[ctype]
    ret.last_use_time = global_data.game_time
    for arg in args:
        ret = ret.get(arg)
        if ret is None:
            return kargs.get('default')

    return ret


def get_raw(ctype, *args, **kargs):
    init(ctype)
    ret = confs[ctype]
    ret.last_use_time = global_data.game_time
    for arg in args:
        ret = ret.get(arg)
        if ret is None:
            return kargs.get('default')

    return ret


def get_in_lut(ctype, *args, **kargs):
    try:
        init(ctype)
        ret = confs[ctype]
        ret.last_use_time = global_data.game_time
        if args:
            real_table = ret[args[0]]
            return get(real_table, *args, **kargs)
        raise ValueError('Args must not be empty when using look-up-table')
    except KeyError:
        ret = kargs.get('default')

    return ret


def set(ctype, new_value, *args):
    import trigger
    import copy
    try:
        init(ctype)
        taggeddict.unlock_tagged_dict()
        ret = confs[ctype]
        for x in range(len(args) - 1):
            ret = ret[args[x]]

        ret[args[-1]] = copy.deepcopy(new_value)
        taggeddict.lock_tagged_dict()
    except:
        pass

    import game3d
    game3d.delay_exec(1, lambda : trigger.run(trigger.CONF_DIRTY, ctype, *args))


def check():
    global check_time
    if not global_data.enable_pop_lru_conf:
        return
    curt = global_data.game_time
    if curt - check_time > LRU_CHECK_TIME:
        check_time = curt
        dels = []
        for k, v in six.iteritems(confs):
            if curt - v.last_use_time > LRU_TIME:
                del v
                dels.append(k)

        print('Pop useless conf count: %s ...' % len(dels))
        for k in dels:
            del confs[k]


def copy(conf):
    t = type(conf)
    if t == dict or t == taggeddict.taggeddict:
        ret = {}
        for k, v in six.iteritems(conf):
            ret[k] = copy(v)

        return ret
    else:
        if t == list:
            ret = []
            for v in conf:
                ret.append(copy(v))

            return ret
        return conf


def enable_taggeddict(value):
    print('enable_taggeddict in confmgr...', value)
    jsonconf.USE_TAGGEDDICT = value