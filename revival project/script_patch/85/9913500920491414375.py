# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComTrainCargoClient.py
from __future__ import absolute_import
import six
from logic.gcommon.component.UnitCom import UnitCom
from logic.gcommon.const import NEOX_UNIT_SCALE
import world
import collision
import math3d
import game3d
from common.cfg import confmgr
import logic.gcommon.cdata.status_config as status_config
import weakref
from logic.gcommon.common_const.collision_const import GROUP_SHOOTUNIT
import logic.gcommon.common_utils.bcast_utils as bcast
from logic.gcommon.trk.TrkManager import TrkManager
from logic.gcommon.common_const import collision_const
from logic.gcommon.common_const import battle_const
import common.utils.timer as timer

class ComTrainCargoClient(UnitCom):
    BIND_EVENT = {'E_ADD_CARGO': 'add_cargo',
       'E_REMOVE_CARGO': 'remove_cargo',
       'G_CARGOS': 'get_cargos',
       'G_CARGO': 'get_cargo'
       }

    def __init__(self):
        super(ComTrainCargoClient, self).__init__()
        self._train_no = None
        self._cargos = {}
        return

    def init_from_dict(self, unit_obj, bdict):
        super(ComTrainCargoClient, self).init_from_dict(unit_obj, bdict)
        self._train_no = bdict.get('train_no')
        self._cargos = bdict.get('cargos', {})
        self.init_carriage_cargos()

    def add_cargo(self, cargo_eid, cargo_relative_pos, carriage_id):
        self._cargos[cargo_eid] = (
         cargo_relative_pos, carriage_id)
        tmp_carriage = self.battle.get_entity(carriage_id)
        if not tmp_carriage or not tmp_carriage.logic:
            return
        tmp_carriage.logic.send_event('E_ADD_CARGO', cargo_eid, cargo_relative_pos)

    def remove_cargo(self, cargo_eid):
        if cargo_eid not in self._cargos:
            log_error('[remove cargo] cargo is not on the train')
            return
        carriage_id = self._cargos[cargo_eid][1]
        self._cargos.pop(cargo_eid)
        tmp_carriage = self.battle.get_entity(carriage_id)
        if not tmp_carriage or not tmp_carriage.logic:
            return
        tmp_carriage.logic.send_event('E_REMOVE_CARGO', cargo_eid)

    def init_carriage_cargos(self):
        for cargo_id, cargo_info in six.iteritems(self._cargos):
            rel_pos = cargo_info[0]
            carriage_id = cargo_info[1]
            self.add_cargo(cargo_id, rel_pos, carriage_id)

    def get_cargos(self):
        return self._cargos

    def get_cargo(self, eid):
        return self._cargos.get(eid, None)

    def destroy(self):
        super(ComTrainCargoClient, self).destroy()