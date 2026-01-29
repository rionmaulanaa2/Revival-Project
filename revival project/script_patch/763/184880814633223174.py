# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/com_pet/ComPetSynchronizer.py
from logic.gcommon.component.UnitCom import UnitCom
from logic.gcommon.component.client.ComClientSynchronizer import ComClientSynchronizer

class ComPetSynchronizer(ComClientSynchronizer):

    def init_from_dict(self, unit_obj, bdict):
        super(ComClientSynchronizer, self).init_from_dict(unit_obj, bdict)
        self.sd.ref_sync_method = self.do_sync_method
        battle = self.battle
        aoi_id = battle.get_entity_aoi_id(unit_obj.id) if battle else None
        if aoi_id is not None and aoi_id > 0:
            self._sync_id = aoi_id
        else:
            self._sync_id = str(unit_obj.id)
        self._sync_method = battle.sync_logic_entity if battle else None
        self._sync_method_misty = battle.sync_logic_entity_misty if battle else None
        self.enable(True)
        return

    def call_sync_method(self, method_name, parameters, immediate=False, include_self=False, broadcast=True, exclude=(), merge=None):
        if not self.ev_g_is_my_pet():
            return
        if self.battle:
            super(ComPetSynchronizer, self).call_sync_method(method_name, parameters, immediate, include_self, broadcast, exclude, merge)
        elif global_data.player:
            global_data.player.sync_visit_pet_event(parameters)