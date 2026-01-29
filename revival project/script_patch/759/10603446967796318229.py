# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/MechaTrans.py
from __future__ import absolute_import
from mobile.common.EntityManager import Dynamic
from .NPC import NPC
from ext_package.ext_decorator import mecha_trans_unit_use_default_skin

@Dynamic
class MechaTrans(NPC):

    @mecha_trans_unit_use_default_skin
    def init_from_dict(self, bdict):
        super(MechaTrans, self).init_from_dict(bdict)

    def is_share(self):
        return False

    def on_add_to_battle(self, battle_id):
        from mobile.common.EntityManager import EntityManager
        from logic.gcommon.common_const import mecha_const
        bdata = self._data
        super(MechaTrans, self).on_add_to_battle(battle_id)
        trans_pattern = bdata.get('trans_pattern')
        is_mecha_vehicle = trans_pattern == mecha_const.MECHA_TYPE_VEHICLE
        if bdata:
            driver_id = bdata.get('driver_id')
            passenger_info = bdata.get('passenger_dict')
            driver = None
            if driver_id:
                driver = EntityManager.getentity(driver_id)
            target = self
            if driver:
                driver.logic.send_event('E_SET_CONTROL_TARGET', target)
            myid = global_data.player.id
            if myid == driver_id:
                global_data.mecha = target
                target.logic.send_event('E_ENABLE_SYNC', True)
                target.logic.send_event('E_CONTROL_MECHA_TWO', True, True)
            elif global_data.player and global_data.player.logic and driver_id and driver_id == global_data.player.logic.ev_g_spectate_target_id():
                target.logic.send_event('E_OBSERVE_CONTROL_MECHA_TWO')
        return