# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/GulagSurvivalBattle.py
from __future__ import absolute_import
import six
import math3d
import world
from logic.entities.SurvivalBattle import SurvivalBattle
from logic.gutils.scene_utils import add_region_scene_collision, add_region_scene_collision_box
from mobile.common.rpcdecorator import rpc_method, CLIENT_STUB
from mobile.common.RpcMethodArgs import Uuid, List, Str, Dict, Int, Float, Bool, Tuple
from logic.gcommon.common_const.battle_const import MAGIC_MONSTER_TIP, MAGIC_ACHIEVE, MAIN_NODE_COMMON_INFO

class GulagSurvivalBattle(SurvivalBattle):

    def init_from_dict(self, bdict):
        super(GulagSurvivalBattle, self).init_from_dict(bdict)
        self.gulag_canceled = bdict.get('is_gulag_canceled', False)

    def load_finish(self):
        super(GulagSurvivalBattle, self).load_finish()
        global_data.gulag_sur_battle_mgr.init_all_revive_game_area()

    def recruit_valid(self):
        return False

    @rpc_method(CLIENT_STUB, (Int('is_canceled'),))
    def gulag_force_cancel(self, is_canceled):
        self.gulag_canceled = is_canceled
        global_data.emgr.on_gulag_force_cancel.emit(is_canceled)
        if is_canceled:
            small_map = global_data.ui_mgr.get_ui('SmallMapUI')
            if small_map:
                small_map.on_update_can_revive(False, is_canceled=is_canceled)

    def update_gulag_cancel_state(self, state):
        self.gulag_canceled = state