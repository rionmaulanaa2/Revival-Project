# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/com_parachute/ComParachuteState.py
from __future__ import absolute_import
from logic.gcommon.component.UnitCom import UnitCom
from logic.gcommon.common_utils.parachute_utils import STAGE_NONE, STAGE_ISLAND, STAGE_FREE_DROP, STAGE_PRE_PARACHUTE, STAGE_PARACHUTE_DROP, STAGE_PLANE, STAGE_LAND, STAGE_FLY_CARRIER, STAGE_MECHA_READY, STAGE_SUPER_JUMP, STAGE_LAUNCH_PREPARE, STAGE_SORTIE_PREPARE, STAGE_SORTIE_READY
from logic.gcommon.time_utility import time
from logic.gcommon.common_const import scene_const
from mobile.common.EntityManager import EntityManager
import math3d

class ComParachuteState(UnitCom):
    BIND_EVENT = {'G_PARACHUTE_STAGE': '_get_parachute_stage',
       'E_MECHA_BORDING': ('_stage_to_mecha_bording', -1),
       'E_READY': ('_stage_to_ready', -1),
       'E_PLANE': ('_stage_to_plane', -1),
       'E_SORTIE': ('_stage_to_land', -1),
       'E_LAND': ('_stage_to_land', -1),
       'G_IN_PARACHUTE_STAGE_IDLE': '_is_stage_idle',
       'G_PARACHUTING': '_is_parachuting',
       'E_OPEN_PARACHUTE': ('_stage_to_parachute', -1),
       'E_PREPARE_PARACHUTE': ('_stage_to_pre_parachute', -1),
       'E_START_PARACHUTE': ('_stage_to_free_drop', -1),
       'E_PREPARE_LAUNCH': ('_stage_to_launch', -1),
       'E_TO_AIRSHIP': ('_stage_to_fly_carrier', -1),
       'G_IN_CARRIER_OR_PLANE': 'is_in_carrier_or_plane',
       'G_IS_PARACHUTE_STAGE_LAND': 'is_parachute_stage_land',
       'G_IS_PARACHUTE_STAGE_FREE_DROP': 'is_parachute_free_drop',
       'G_IS_PARACHUTE_STAGE_PLANE': 'is_in_plane',
       'G_IS_PARACHUTE_BATTLE_LAND': 'is_in_battle_land',
       'G_IS_PARACHUTE_READY_BATTLE': 'is_in_ready_battle',
       'G_IS_PARACHUTE_PREPARE': 'is_preparing',
       'E_START_SUPER_JUMP': '_stage_to_super_jump',
       'G_IS_SUPER_JUMPING': 'is_super_jumping',
       'G_FORCE_OPEN_PARACHUTE_HEIGHT': 'get_force_open_parachute_height',
       'E_REVIVE': ('on_revive', -1),
       'G_LAUNCH_POS': 'get_launch_pos',
       'E_SET_LAUNCH_POS': 'set_launch_pos',
       'E_START_POSITION_CHECKER': 'on_start_position_checker'
       }

    def __init__(self):
        super(ComParachuteState, self).__init__()
        self._init_data()

    def _init_data(self):
        self._is_avatar = False
        self.sd.ref_parachute_stage = STAGE_NONE
        self._last_stage = STAGE_NONE
        self._super_jumping = False
        self._mecha_land_prepared = False
        self._launch_start_pos = None
        self._launch_end_pos = None
        self.enter_pre_parachute_timestamp = 0
        return

    @property
    def stage(self):
        return self.sd.ref_parachute_stage

    @stage.setter
    def stage(self, value):
        self._last_stage = self.sd.ref_parachute_stage
        self.sd.ref_parachute_stage = value

    def get_launch_pos(self):
        return (
         self._launch_start_pos, self._launch_end_pos)

    def set_launch_pos(self, start_pos, end_pos):
        if self.stage == STAGE_LAUNCH_PREPARE:
            return
        self._launch_start_pos = math3d.vector(*start_pos)
        self._launch_end_pos = math3d.vector(*end_pos)

    def get_force_open_parachute_height(self):
        return self._force_height

    def is_parachute_free_drop(self):
        return self.sd.ref_parachute_stage in (STAGE_FREE_DROP, STAGE_SUPER_JUMP, STAGE_LAUNCH_PREPARE)

    def is_in_battle_land(self):
        return self.sd.ref_parachute_stage == STAGE_LAND

    def is_in_ready_battle(self):
        return self.sd.ref_parachute_stage in (STAGE_SORTIE_PREPARE, STAGE_SORTIE_READY)

    def is_in_plane(self):
        return self.sd.ref_parachute_stage == STAGE_PLANE

    def is_super_jumping(self):
        return self._super_jumping

    def is_preparing(self):
        return self.sd.ref_parachute_stage in (STAGE_NONE, STAGE_MECHA_READY)

    def is_parachute_stage_land(self):
        return self.sd.ref_parachute_stage == STAGE_LAND

    def is_in_carrier_or_plane(self):
        return self.sd.ref_parachute_stage in (STAGE_FLY_CARRIER, STAGE_NONE, STAGE_MECHA_READY, STAGE_PLANE)

    def _is_parachuting(self):
        return self.sd.ref_parachute_stage == STAGE_PARACHUTE_DROP

    def init_from_dict(self, unit_obj, bdict):
        self._init_stage = bdict.get('parachute_stage', STAGE_LAND)
        if global_data.battle.is_in_island() and self._init_stage == STAGE_NONE:
            self._init_stage = STAGE_ISLAND
        self.sd.ref_parachute_stage = STAGE_LAND
        self._last_stage = bdict.get('last_fly_stage', STAGE_PLANE)
        launch_data = bdict.get('launch_data', [])
        if launch_data:
            self._launch_start_pos = math3d.vector(*launch_data[0])
            self._launch_end_pos = math3d.vector(*launch_data[1])
        super(ComParachuteState, self).init_from_dict(unit_obj, bdict)
        self.sd.ref_has_first_land = bdict.get('first_land', False)

    def on_init_complete(self):
        self._is_avatar = self.ev_g_is_avatar()
        if self._init_stage == STAGE_PLANE:
            self.send_event('E_PLANE')
        elif self._init_stage in (STAGE_FREE_DROP, STAGE_LAUNCH_PREPARE):
            sync = self._init_stage == STAGE_LAUNCH_PREPARE
            start_pos = self.ev_g_position()
            end_pos = self._launch_end_pos
            if not sync:
                self.stage = STAGE_PLANE
            self.send_event('E_START_PARACHUTE', (start_pos.x, start_pos.y, start_pos.z), (end_pos.x, end_pos.y, end_pos.z), sync)
        elif self._init_stage == STAGE_PARACHUTE_DROP:
            self.send_event('E_OPEN_PARACHUTE')
        else:
            self.stage = self._init_stage
            self._on_parachute_stage_changed()

    def _get_parachute_stage(self):
        return self.stage

    def _on_parachute_stage_changed(self):
        if self._is_avatar:
            if self._last_stage == STAGE_PARACHUTE_DROP or self.sd.ref_parachute_stage == STAGE_PARACHUTE_DROP:
                groupmate_eids = self.ev_g_groupmate()
                for eid in groupmate_eids:
                    if eid == global_data.player.id:
                        continue
                    groupmate = EntityManager.getentity(eid)
                    if groupmate and groupmate.logic:
                        groupmate.logic.send_event('E_REFRESH_MOVE_TICK_METHOD')

            if global_data.enable_parachute_view_range_optimize:
                if self.sd.ref_parachute_stage not in (STAGE_NONE, STAGE_MECHA_READY, STAGE_PLANE, STAGE_LAUNCH_PREPARE):
                    cur_scene = global_data.game_mgr.scene
                    if cur_scene:
                        scene_type = cur_scene.get_type()
                        if scene_type in (scene_const.SCENE_TRANING,):
                            cur_scene.modify_view_range_to_default()
        self.send_event('E_ENABLE_PARACHUTE_COM', self.sd.ref_parachute_stage in (STAGE_PARACHUTE_DROP, STAGE_FREE_DROP))
        self.send_event('E_PARACHUTE_STATUS_CHANGED', self.sd.ref_parachute_stage)

    def _stage_to_mecha_bording(self, *args):
        self.stage = STAGE_NONE
        self._on_parachute_stage_changed()

    def _stage_to_ready(self, *args):
        self.stage = STAGE_MECHA_READY
        self._on_parachute_stage_changed()

    def _stage_to_plane(self, *args):
        self.stage = STAGE_PLANE
        self._on_parachute_stage_changed()

    def _stage_to_land(self, *args):
        if self._is_avatar:
            if time() - self.enter_pre_parachute_timestamp < 2.0:
                from logic.gcommon.component.EventStop import ESTOP
                return ESTOP
        self._last_free_drop_timestamp = 0
        self.stage = STAGE_LAND
        self._super_jumping = False
        self._on_parachute_stage_changed()

    def _stage_to_launch(self, start_pos, end_pos, is_sync=True, *args):
        if self.stage == STAGE_LAUNCH_PREPARE:
            return
        self.stage = STAGE_LAUNCH_PREPARE
        self._launch_start_pos = math3d.vector(*start_pos)
        self._launch_end_pos = math3d.vector(*end_pos)
        self._on_parachute_stage_changed()
        if is_sync:
            self.send_event('E_CALL_SYNC_METHOD', 'start_launch', (start_pos, end_pos), True)

    def _stage_to_free_drop(self, start_pos=None, end_pos=None, is_sync=True, *args):
        from logic.gcommon.component.EventStop import ESTOP
        if self.stage != STAGE_PLANE and self.stage != STAGE_ISLAND:
            return ESTOP
        if is_sync:
            self.send_event('E_CALL_SYNC_METHOD', 'start_parachute', (start_pos, end_pos), True)
        self._stage_to_pre_parachute()
        if not self._is_avatar:
            groupmate_id_list = self.ev_g_groupmate()
            if groupmate_id_list and global_data.player and global_data.player.id in groupmate_id_list:
                global_data.emgr.groupmate_parachute_mecha_disappear.emit(self.unit_obj.id)
        self.send_event('E_SHOW_MODEL')

    def _stage_to_parachute(self, is_force=True, *args):
        self.on_start_position_checker()
        from logic.gcommon.component.EventStop import ESTOP
        if self.is_in_ready_battle():
            return ESTOP
        if self.sd.ref_parachute_stage == STAGE_PARACHUTE_DROP:
            return ESTOP
        self.stage = STAGE_PARACHUTE_DROP
        self.send_event('E_CALL_SYNC_METHOD', 'open_parachute', (), True)
        self._on_parachute_stage_changed()

    def _stage_to_pre_parachute(self):
        self.stage = STAGE_PRE_PARACHUTE
        self.enter_pre_parachute_timestamp = time()
        self._on_parachute_stage_changed()
        if self._is_avatar and self.ev_g_char_waiting() is None:
            self.send_event('E_TRY_ACTIVE_CHARACTER')
        return

    def _stage_to_parachute_none(self, *args):
        self.stage = STAGE_NONE
        self._on_parachute_stage_changed()

    def _stage_to_fly_carrier(self, *args):
        self.stage = STAGE_FLY_CARRIER
        self._on_parachute_stage_changed()

    def _is_stage_idle(self, *args):
        return self.sd.ref_parachute_stage in (STAGE_NONE, STAGE_ISLAND, STAGE_PLANE)

    def _stage_to_super_jump(self, *args):
        pass

    def on_revive(self, *args):
        bat = self.unit_obj.get_battle()
        if bat and bat.is_in_settle_celebrate_stage():
            pass
        else:
            self._init_data()

    def on_start_position_checker(self):
        if not self._is_avatar:
            return
        lavt = global_data.player.logic
        if lavt:
            com_checker = lavt.get_com('ComPositionChecker')
            if not com_checker:
                com_checker = lavt.add_com('ComPositionChecker', 'client')
                if com_checker:
                    com_checker.init_from_dict(lavt, {})