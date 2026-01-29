# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gutils/pet_utils.py
from __future__ import absolute_import
from common.cfg import confmgr
import six_ex

def get_pet_level(item_no):
    if not item_no:
        return 0
    else:
        base_item_no = confmgr.get('c_pet_info', str(item_no), 'base_skin', default=item_no)
        pet_item = global_data.player and global_data.player.get_item_by_no(int(base_item_no))
        if pet_item is None:
            return 0
        return pet_item.level


def get_skill_unlock_pet_level(skill_level):
    pet_exp_conf = confmgr.get('c_pet_exp', default={})
    for pet_level, conf in six_ex.items(pet_exp_conf):
        if conf.get('skill_level') == int(skill_level):
            return int(pet_level)

    return 0


def get_pet_skill_level(item_no):
    base_item_no = confmgr.get('c_pet_info', str(item_no), 'base_skin', default=item_no)
    pet_level = get_pet_level(base_item_no)
    pet_skill_level = confmgr.get('c_pet_exp', str(pet_level), 'skill_level', default=0)
    return pet_skill_level


def get_pet_max_skill_level(item_no):
    pet_conf = confmgr.get('c_pet_info', str(item_no), default={})
    pet_max_level = pet_conf.get('max_level', 0)
    pet_max_skill_level = confmgr.get('c_pet_exp', str(pet_max_level), 'skill_level', default=0)
    return pet_max_skill_level


def is_ss_pet(item_no):
    sub_skin_list = confmgr.get('c_pet_info', str(item_no), 'sub_skin', default=[]) or []
    if sub_skin_list:
        return True
    else:
        return False