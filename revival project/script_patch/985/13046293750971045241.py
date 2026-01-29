# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/com_field/ComFieldLogic.py
from __future__ import absolute_import
from logic.gcommon.component.UnitCom import UnitCom
import math3d
from common.cfg import confmgr
import common.utils.timer as timer
from logic.gcommon.const import NEOX_UNIT_SCALE
from mobile.common.EntityManager import EntityManager
CHEKC_INTERVAL = 0.1

class ComFieldLogic(UnitCom):
    BIND_EVENT = {'G_CREATOR_ID': 'get_creator_id'
       }

    def __init__(self):
        super(ComFieldLogic, self).__init__()

    def init_from_dict(self, unit_obj, bdict):
        super(ComFieldLogic, self).init_from_dict(unit_obj, bdict)
        self._create_id = bdict['creator_id']
        field_inf = confmgr.get('field_data', str(bdict['npc_id']))
        self._pos = math3d.vector(*bdict['position'])
        self._radius = bdict.get('range', 0)
        self._inside_robots = []
        self._timer = None
        if self._create_id == global_data.player.id:
            times = int(field_inf['fTime'] / CHEKC_INTERVAL)
            self._timer = global_data.game_mgr.register_logic_timer(self.check_tick, interval=CHEKC_INTERVAL, times=times, mode=timer.CLOCK)
        return

    def check_tick(self):
        robots = global_data.emgr.scene_explode_robot_event.emit(self._pos, self._radius)
        self._inside_robots = robots

    def get_creator_id(self):
        return self._create_id

    def destroy(self):
        global_data.game_mgr.unregister_logic_timer(self._timer)
        self._timer = None
        super(ComFieldLogic, self).destroy()
        return