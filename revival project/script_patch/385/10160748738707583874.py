# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComTrainCarriageCargoClient.py
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

class ComTrainCarriageCargoClient(UnitCom):
    BIND_EVENT = {'E_ADD_CARGO': 'add_cargo',
       'E_REMOVE_CARGO': 'remove_cargo',
       'G_CARGOS': 'get_cargos',
       'G_CARGO': 'get_cargo',
       'E_DO_CARGO_MOVE': 'do_cargo_move'
       }

    def __init__(self):
        super(ComTrainCarriageCargoClient, self).__init__()
        self._train_no = None
        self._carriage_idx = None
        self._cargos = {}
        return

    def init_from_dict(self, unit_obj, bdict):
        super(ComTrainCarriageCargoClient, self).init_from_dict(unit_obj, bdict)
        self._carriage_idx = bdict.get('carriage_idx')
        self._train_no = bdict.get('train_no')
        self._cargos = bdict.get('cargos', {})
        for cargo_id, cargo_rel_pos in six.iteritems(self._cargos):
            if isinstance(cargo_rel_pos, list):
                cargo_rel_pos = math3d.vector(*cargo_rel_pos)
            self._cargos[cargo_id] = cargo_rel_pos

    def add_cargo(self, cargo_eid, cargo_relative_pos):
        if isinstance(cargo_relative_pos, list):
            cargo_relative_pos = math3d.vector(*cargo_relative_pos)
        self._cargos[cargo_eid] = cargo_relative_pos

    def remove_cargo(self, cargo_eid):
        if cargo_eid not in self._cargos:
            log_error('[remove cargo] cargo is not on the train')
            return
        self._cargos.pop(cargo_eid)

    def get_cargos(self):
        return self._cargos

    def get_cargo(self, eid):
        return self._cargos.get(eid, None)

    def do_cargo_move(self, par_trans):
        for cargo_eid, cargo_rel_pos in six.iteritems(self._cargos):
            tmp_cargo_ent = self.battle.get_entity(cargo_eid)
            if tmp_cargo_ent and tmp_cargo_ent.logic:
                tmp_world_pos = self.relative_to_world(cargo_rel_pos, par_trans)
                tmp_cargo_ent.logic.send_event('E_POSITION', tmp_world_pos)

    def relative_to_world(self, rel_coor, par_trans):
        return rel_coor * par_trans

    def world_to_relative(self, world_coor, par_trans):
        par_trans.inverse()
        return world_coor * par_trans

    def destroy(self):
        super(ComTrainCarriageCargoClient, self).destroy()