# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComFlagBaseClient.py
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
import common.utils.timer as timer
import logic.vscene.parts.ctrl.GamePyHook as game_hook
import game
from logic.gcommon.common_const import battle_const
from logic.gcommon.common_const.building_const import FLAG_RECOVER_BY_DROPPING, FLAG_RECOVER_BY_PLANTING, FLAG_RECOVER_BY_TIME_UP, FLAG_RECOVER_REASION_TEXT

class ComFlagBaseClient(UnitCom):
    BIND_EVENT = {'E_COLLSION_LOADED': '_on_col_loaded'
       }
    SMALL_MAP_FLAG_BASE_BLUE = 2040
    SMALL_MAP_FLAG_BASE_RED = 2039

    def __init__(self):
        super(ComFlagBaseClient, self).__init__()
        self.faction_id = None
        self.sfx_id = None
        return

    def init_from_dict(self, unit_obj, bdict):
        super(ComFlagBaseClient, self).init_from_dict(unit_obj, bdict)
        self.faction_id = bdict.get('faction_id')
        self._on_flag_base_init_complete(self.unit_obj.id, self.ev_g_position())

    def _on_flag_base_init_complete(self, eid, pos):
        global_data.emgr.scene_del_client_mark.emit(eid)
        if self.faction_id == global_data.player.logic.ev_g_group_id():
            global_data.emgr.scene_add_client_mark.emit(eid, self.SMALL_MAP_FLAG_BASE_BLUE, pos)
        else:
            global_data.emgr.scene_add_client_mark.emit(eid, self.SMALL_MAP_FLAG_BASE_RED, pos)

    def destroy(self):
        global_data.emgr.scene_del_client_mark.emit(self.unit_obj.id)
        super(ComFlagBaseClient, self).destroy()

    def _on_col_loaded(self, *args):
        self.init_effect()

    def init_effect(self):
        pass