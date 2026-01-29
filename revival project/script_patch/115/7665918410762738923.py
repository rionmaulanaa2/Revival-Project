# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gutils/yet_another_observe_utils.py
from __future__ import absolute_import

def get_ob_target_id():
    scn = global_data.game_mgr.scene
    if scn:
        spart = scn.get_com('PartObserve')
        if spart:
            return spart.get_cur_observe_id()
    return None


def get_ob_target_unit():
    _id = get_ob_target_id()
    if _id is None:
        return
    else:
        from mobile.common.EntityManager import EntityManager
        ent = EntityManager.getentity(_id)
        if ent and ent.logic:
            return ent.logic
        return