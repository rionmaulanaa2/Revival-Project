# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/item/client_item_pick_check_handler.py
from __future__ import absolute_import

def check_pick_mecha_shield_drug(unit_obj, item_id, args):
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
            enable_overfull = lmecha.ev_g_is_enable_overfull()
            if enable_overfull:
                check_full = False
            if not check_full or not lmecha.ev_g_full_shield():
                shield_limit = args.get('limit', None)
                return shield_limit or True
            cur_shield = lmecha.ev_g_shield()
            if cur_shield < shield_limit:
                return True
        return False


def check_pick_pve_ice_crystal(unit_obj, item_id, args):
    max_cnt = args.get('max_cnt', 20)
    if unit_obj.ev_g_pve_ice() < max_cnt:
        return True
    return False