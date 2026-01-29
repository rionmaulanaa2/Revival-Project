# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComTrainCarriageClient.py
from __future__ import absolute_import
from logic.gcommon.component.UnitCom import UnitCom
from logic.gcommon.const import NEOX_UNIT_SCALE
import world
import collision
import math3d
import game3d
import logic.gcommon.cdata.status_config as status_config
import weakref
from logic.gcommon.common_const.collision_const import GROUP_SHOOTUNIT
import logic.gcommon.common_utils.bcast_utils as bcast
from logic.gcommon import time_utility as tutil
from logic.gcommon.common_const import battle_const
from logic.client.const import game_mode_const
from logic.vscene.parts.gamemode.GMDecorator import execute_by_mode

class ComTrainCarriageClient(UnitCom):
    SMALL_MAP_TRAIN_ID = 2034
    BIND_EVENT = {'E_CHANGE_CARRIAGE_STATE': '_on_change_carriage_state',
       'E_RECREAT_MARK': 'create_train_mark',
       'E_COLLSION_LOADED': '_on_col_loaded'
       }

    def __init__(self):
        super(ComTrainCarriageClient, self).__init__()
        self._carriage_idx = None
        self._train_state = None
        return

    def _on_col_loaded(self, *args):
        if self._carriage_idx == 1:
            self.create_train_mark()

    def init_from_dict(self, unit_obj, bdict):
        super(ComTrainCarriageClient, self).init_from_dict(unit_obj, bdict)
        self._carriage_idx = bdict.get('carriage_idx')
        self._train_state = bdict.get('client_state', battle_const.KD_TRAIN_START_SPEED_REDUCE)
        if self._carriage_idx == 1:
            global_data.carry_mgr.add_train_id(self.unit_obj.id)
            self.create_train_mark()
        global_data.carry_mgr.add_train_carriage_id(self.unit_obj.id)

    def _on_change_carriage_state(self, state):
        self._train_state = state
        if self._carriage_idx == 1:
            global_data.emgr.on_train_station_changed.emit(state, self.ev_g_position())

    @execute_by_mode(False, (game_mode_const.GAME_MODE_TRAIN,))
    def create_train_mark(self):
        tmp_pos = self.ev_g_position()
        global_data.emgr.scene_del_client_mark.emit(self.unit_obj.id)
        global_data.emgr.scene_add_client_mark.emit(self.unit_obj.id, self.SMALL_MAP_TRAIN_ID, tmp_pos)

    def destroy(self):
        super(ComTrainCarriageClient, self).destroy()