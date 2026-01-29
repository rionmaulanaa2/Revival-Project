# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gutils/monster_utils.py
from __future__ import absolute_import
from mobile.common.EntityManager import EntityManager

def check_monster_hit(hit_id, trigger_id):
    if global_data.cam_lplayer and global_data.cam_lplayer.id != trigger_id:
        return
    monster = EntityManager.getentity(hit_id)
    if not (monster and monster.logic and monster.__class__.__name__ == 'Monster'):
        return
    if global_data.game_mode.is_pve():
        global_data.emgr.pve_monster_hit.emit(hit_id)
        return
    ui = global_data.ui_mgr.get_ui('MonsterBloodUI')
    if ui:
        ui.show_monster_hp(hit_id)