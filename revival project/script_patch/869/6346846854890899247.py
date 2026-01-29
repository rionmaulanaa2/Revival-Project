# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComParachuteDriverGhost.py
from __future__ import absolute_import
from ..UnitCom import UnitCom
import math3d
from logic.gcommon.time_utility import time
from logic.gcommon.common_utils.parachute_utils import STAGE_NONE, STAGE_FREE_DROP, STAGE_PARACHUTE_DROP, STAGE_PLANE, STAGE_LAND

class ComParachuteDriverGhost(UnitCom):
    BIND_EVENT = {'E_ACTION_PARA_TOWARD': '_on_action_toward',
       'E_ACTION_PARA_STOP': '_on_action_stop',
       'E_SORTIE': '_land',
       'E_LAND': '_land',
       'E_START_PARACHUTE': '_start_parachute_stage',
       'E_OPEN_PARACHUTE': '_on_open_parachute',
       'E_SYNC_LAUNCH_BOOST_MECHA_POSITION_OFFSET': 'on_sync_launch_boost_mecha_position_offset',
       'E_SYNC_LAUNCH_BOOST_MECHA_MOVE_DIR': 'on_sync_launch_boost_mecha_move_dir'
       }

    def __init__(self):
        super(ComParachuteDriverGhost, self).__init__(need_update=False)
        self.need_update = False
        self.sd.ref_mecha_target_position_offset = None
        self.sd.ref_mecha_move_dir = (0.0, 0.0)
        return

    def init_from_dict(self, unit_obj, bdict):
        stage = bdict.get('parachute_stage', STAGE_LAND)
        super(ComParachuteDriverGhost, self).init_from_dict(unit_obj, bdict)
        if stage == STAGE_PLANE:
            self._do_take_plane()

    def on_init_complete(self):
        pass

    def destroy(self):
        super(ComParachuteDriverGhost, self).destroy()

    def _on_action_toward(self, x, z):
        self.send_event('E_PARACHUTE_MOVE', math3d.vector(x, 0, z))

    def _on_action_stop(self):
        self.send_event('E_PARACHUTE_MOVE_STOP')

    def _land(self, *args):
        self.send_event('E_SYNC_MOVE_ITPL_STABLE_X', 0)
        self.send_event('E_SET_ENABLE_ITPL_LV', True)
        self.destroy_from_unit()

    def _start_parachute_stage(self, start_pos, *args):
        pos = math3d.vector(*start_pos)
        self._start_free_drop()
        if G_POS_CHANGE_MGR:
            self.notify_pos_change(pos, True)
        else:
            self.send_event('E_POSITION', pos)
        self.send_event('E_SYNC_CLEAR_RECEIVER_POS')

    def _start_free_drop(self):
        self.send_event('E_SYNC_MOVE_ITPL_STABLE_X', 5.0)
        self.send_event('E_SET_ENABLE_ITPL_LV', False)

    def _on_open_parachute(self):
        self._jetting = False
        self.send_event('E_EQUIP_PARACHUTE')

    def _do_take_plane(self):
        global_data.emgr.plane_add_passenger_event.emit(self.unit_obj.id)

    def on_sync_launch_boost_mecha_position_offset(self, x, z):
        self.sd.ref_mecha_target_position_offset = math3d.vector(x, 0.0, z)

    def on_sync_launch_boost_mecha_move_dir(self, x, z):
        self.sd.ref_mecha_move_dir = (
         x, z)