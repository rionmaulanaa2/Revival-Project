# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/com_field/ComChainFieldLogic.py
from __future__ import absolute_import
from logic.gcommon.component.UnitCom import UnitCom
import math3d
import world
from common.cfg import confmgr
from logic.gcommon.const import NEOX_UNIT_SCALE
from mobile.common.EntityManager import EntityManager
import logic.gcommon.common_utils.bcast_utils as bcast
CHEKC_INTERVAL = 0.1

class ComChainFieldLogic(UnitCom):
    BIND_EVENT = {'E_LOCK_CHAIN_TARGET_8015': '_on_lock_chain_target'
       }

    def init_from_dict(self, unit_obj, bdict):
        super(ComChainFieldLogic, self).init_from_dict(unit_obj, bdict)
        self._create_id = bdict['creator_id']
        field_inf = confmgr.get('field_data', str(bdict['npc_id']))
        self._pos = math3d.vector(*bdict['position'])
        self._radius = bdict.get('range', 0)
        self._in_radius = field_inf['cCustomParam'].get('in_radius', 0)
        self._catapult_sfx_path = field_inf['cCustomParam'].get('catapult_sfx_path')
        self._ignore_targets = bdict.get('ignore_targets', [])
        self._chain_tid = bdict.get('chain_tid')

    def on_init_complete(self):
        if self._create_id == global_data.player.id:
            self.start_check_unit()

    def start_check_unit(self):
        entity = EntityManager.getentity(self._create_id)
        if not (entity and entity.logic):
            return
        pos = self._pos
        if self._chain_tid:
            pos = self._pos + math3d.vector(0, 3 * NEOX_UNIT_SCALE, 0)
        unit_datas = global_data.emgr.scene_get_nearest_enemy_mecha_unit.emit(entity.logic, pos, self._radius, self._in_radius, monster_too=global_data.game_mode.is_pve())
        if unit_datas and unit_datas[0]:
            unit_data = unit_datas[0][1]
            for data in unit_data:
                if not data:
                    continue
                lock_target_id = data[0].id
                if lock_target_id in self._ignore_targets:
                    continue
                self.send_event('E_FIELD_LOCK_TARGET', lock_target_id, self._pos, self._catapult_sfx_path, self._chain_tid)
                self.send_event('E_CALL_SYNC_METHOD', 'upload_field_target', ([lock_target_id],), True)
                self.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', [bcast.E_LOCK_CHAIN_TARGET_8015, (lock_target_id,)], True)
                break

    def _on_lock_chain_target(self, lock_target_id):
        self.send_event('E_FIELD_LOCK_TARGET', lock_target_id, self._pos, self._catapult_sfx_path, self._chain_tid)