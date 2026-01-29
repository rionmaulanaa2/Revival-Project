# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gutils/reinforce_card_utils.py
from __future__ import absolute_import
from common.cfg import confmgr

def get_card_effect_config(card_id):
    module_config = confmgr.get('mecha_reinforce_card', 'ModuleConfig', 'Content')
    skill_effect_config = confmgr.get('mecha_reinforce_card', 'SkillEffectConfig', 'Content')
    buff_effect_config = confmgr.get('mecha_reinforce_card', 'BuffEffectConfig', 'Content')
    weapon_effect_config = confmgr.get('mecha_reinforce_card', 'WeaponEffectConfig', 'Content')
    effect_config = module_config.get(str(card_id), {})
    skill_effects = effect_config.get('skill_effects', [])
    buff_effects = effect_config.get('buff_effects', [])
    weapon_effects = effect_config.get('weapon_effects', [])
    card_effect_config = {}
    for effect_id in skill_effects:
        effect_config = skill_effect_config.get(str(effect_id), {})
        if 'cfunc' in effect_config:
            card_effect_config[effect_config.get('cfunc')] = effect_config

    for effect_id in buff_effects:
        effect_config = buff_effect_config.get(str(effect_id), {})
        if 'cfunc' in effect_config:
            card_effect_config[effect_config.get('cfunc')] = effect_config

    for effect_id in weapon_effects:
        effect_config = weapon_effect_config.get(str(effect_id), {})
        if 'cfunc' in effect_config:
            card_effect_config[effect_config.get('cfunc')] = effect_config

    return card_effect_config


def get_card_item_no(card_id):
    module_config = confmgr.get('mecha_reinforce_card', 'ModuleConfig', 'Content')
    card_conf = module_config.get(str(card_id), {})
    return card_conf.get('item_no', None)