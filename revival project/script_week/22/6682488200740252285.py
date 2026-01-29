# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/SurvivalBattle.py
from __future__ import absolute_import
from logic.entities.Battle import Battle
from mobile.common.rpcdecorator import rpc_method, CLIENT_STUB
from mobile.common.RpcMethodArgs import Uuid, List, Str, Dict, Int, Float, Bool, Tuple
from mobile.common.EntityManager import EntityManager
from logic.gutils.EntityPool import EntityPool
from mobile.common.IdManager import IdManager
from ext_package.ext_decorator import ext_get_nb_mecha_info, ext_get_nb_role_info
from logic.gutils import gravity_mode_utils, judge_utils
from logic.gcommon.const import NEOX_UNIT_SCALE
import six

class SurvivalBattle(Battle):

    def init_from_dict(self, bdict):
        self.aero_gravity_open = False
        self.aero_gravity_center = (95, 38, -12559)
        self.aero_gravity_radius = 200 * NEOX_UNIT_SCALE
        self.aerospace_gravity_reconnect(bdict)
        super(SurvivalBattle, self).init_from_dict(bdict)
        self.area_id = bdict.get('area_id')
        self._top_nb_role_info = bdict.get('top_nb_role_info', [])
        self._top_nb_mecha_info = bdict.get('top_nb_mecha_info', [])
        self._next_island_refresh_ts = bdict.get('next_island_refresh_ts', 0)
        self.cargos = bdict.get('cargos', [])
        self.aero_gravity_reconnect_data = {}
        self.custom_faction_members = {}
        self.faction_danmu_controller = self.create_faction_danmu_controller()

    def destroy(self, clear_cache=True):
        super(SurvivalBattle, self).destroy(clear_cache)
        self.destroy_faction_danmu_controller()

    def aerospace_gravity_reconnect(self, bdict):
        self.aero_gravity_open = bdict.get('aero_gravity_open', False)
        self.aero_gravity_center = bdict.get('aero_gravity_center')
        self.aero_gravity_radius = bdict.get('aero_gravity_radius')

    def load_finish(self):
        super(SurvivalBattle, self).load_finish()
        self.reconnect_handle_aerospace_gravity()

    def reconnect_handle_aerospace_gravity(self):
        if self.aero_gravity_open:
            if global_data.gravity_sur_battle_mgr:
                global_data.gravity_sur_battle_mgr.set_region_param(gravity_mode_utils.AERO_LESS_GRAVITY, [(self.aero_gravity_center, self.aero_gravity_radius, 1)])
            global_data.emgr.init_gravity_region.emit(gravity_mode_utils.AERO_LESS_GRAVITY)

    def init_battle_scene(self, scene_data):
        from logic.gcommon.common_utils import parachute_utils
        parachute_stage = self._save_init_bdict.get('parachute_stage', None)
        preload_cockpit = parachute_utils.is_need_prepload_cockpit(parachute_stage)
        scene_data.update({'preload_cockpit': preload_cockpit})
        super(SurvivalBattle, self).init_battle_scene(scene_data)
        return

    @rpc_method(CLIENT_STUB, (Dict('stage_dict'),))
    def prepare_stage(self, stage_dict):
        prepare_num = stage_dict.get('prepare_num', 0)
        player_num = stage_dict.get('fighter_num', 0)
        prepare_timestamp = stage_dict.get('prepare_timestamp', 0)
        flight_dict = stage_dict.get('flight_dict', {})
        self.update_prepare_num((prepare_num, player_num))
        self.flight_dict = flight_dict
        import logic.gcommon.time_utility as tutil
        self.prepare_timestamp = prepare_timestamp
        self._save_init_bdict['prepare_timestamp'] = prepare_timestamp
        self.on_battle_status_changed(Battle.BATTLE_STATUS_PREPARE)
        global_data.emgr.battle_change_prepare_timestamp.emit()
        self.init_top_nb_info(stage_dict)

    def init_top_nb_info(self, stage_dict):
        self._next_island_refresh_ts = stage_dict.get('next_island_refresh_ts', 0)
        self._top_nb_role_info = stage_dict.get('top_nb_role_info', [])
        self._top_nb_mecha_info = stage_dict.get('top_nb_mecha_info', [])

    @ext_get_nb_role_info
    def get_top_nb_role_info(self):
        return self._top_nb_role_info

    @ext_get_nb_mecha_info
    def get_top_nb_mecha_info(self):
        return self._top_nb_mecha_info

    def get_next_island_refresh_ts(self):
        return self._next_island_refresh_ts

    @rpc_method(CLIENT_STUB, (List('top_nb_mecha_info'), List('top_nb_role_info'), Float('next_refresh_time')))
    def on_island_nb_fasion_update(self, top_nb_mecha_info, top_nb_role_info, next_refresh_time):
        self._top_nb_mecha_info = top_nb_mecha_info
        self._top_nb_role_info = top_nb_role_info
        self._next_island_refresh_ts = next_refresh_time
        global_data.emgr.island_top_skin_change.emit()

    @rpc_method(CLIENT_STUB, (List('cargos'),))
    def update_cargos(self, cargos):
        self.cargos = cargos

    def get_cargos(self):
        str_cargos = []
        for cargo in self.cargos:
            str_cargos.append(str(cargo))

        return str_cargos

    def create_entity(self, entity_type, entity_id, entity_aoi_id, entity_dict):
        if self.is_battle_prepare_stage():
            island_set_id = entity_dict.get('island_set_id')
            if island_set_id is not None and global_data.player and global_data.player.logic:
                if global_data.player.logic.ev_g_island_set_id() != island_set_id:
                    return
            if entity_type in ('Item', 'House', 'Building', 'Motorcycle'):
                return
        entity = EntityManager.getentity(entity_id)
        if entity is None:
            entity = EntityPool.create_entity(entity_type, entity_id)
            entity.init_from_dict(entity_dict)
            self.add_entity_imp(entity_id, entity_aoi_id)
        else:
            entity.update_from_dict(entity_dict)
            self.update_entity_imp(entity_id, entity_aoi_id)
        return entity

    def logic_entity(self, sync_id, method_name, parameters):
        try:
            entity_id = self._entity_aoi_id_dict.get(sync_id, None) or IdManager.str2id(sync_id)
            entity = EntityManager.getentity(entity_id)
        except:
            entity = None

        if entity is None:
            if not self.is_battle_prepare_stage():
                from logic.gcommon.component.proto.client import methods
                log_name = methods.get(method_name, method_name)
                self.logger.error('Cannot sync non-existed entity to battle, sync_id, %s %s %s', sync_id, log_name, parameters)
            return
        else:
            if entity.logic is None:
                return
            entity.logic.send_event('E_DO_SYNC_METHOD', method_name, parameters)
            return

    @rpc_method(CLIENT_STUB, (Tuple('region_pos'), Float('region_r'), Int('region_level')))
    def init_aerospace_less_gravity_region(self, region_pos, region_r, region_level):
        if global_data.gravity_sur_battle_mgr:
            global_data.gravity_sur_battle_mgr.set_region_param(gravity_mode_utils.AERO_LESS_GRAVITY, [(region_pos, region_r, region_level)])
        global_data.emgr.init_gravity_region.emit(gravity_mode_utils.AERO_LESS_GRAVITY)

    @rpc_method(CLIENT_STUB, (Int('region_level'),))
    def remove_aerospace_gravity_region(self, region_level):
        self.remove_aerospace_gravity_region_by_type(gravity_mode_utils.AERO_LESS_GRAVITY)

    def remove_aerospace_gravity_region_by_type(self, type):
        if global_data.gravity_sur_battle_mgr:
            global_data.gravity_sur_battle_mgr.set_region_param(gravity_mode_utils.AERO_LESS_GRAVITY)
        global_data.emgr.remove_gravity_region.emit(gravity_mode_utils.AERO_LESS_GRAVITY)

    @rpc_method(CLIENT_STUB, (Dict('sync_data'),))
    def sync_custom_faction_members(self, sync_data):
        self.custom_faction_members = sync_data
        self.init_faction_member_mark()

    def init_faction_member_mark(self):
        player = global_data.player
        if not player or not player.logic:
            return
        my_faction = player.logic.ev_g_camp_id()
        entity_ids = list(self.custom_faction_members.get(my_faction, {}).keys())
        if not self.is_battle_fight_stage() or judge_utils.is_ob():
            return
        ui = global_data.ui_mgr.get_ui('EntityHeadMarkUI')
        if ui:
            ui.update_entity_ids(entity_ids)
            return
        from logic.comsys.battle.Hunting.EntityHeadMarkUI import EntityHeadMarkUI
        from logic.gcommon.common_const.battle_const import MAP_COL_BLUE, MAP_COL_GREEN, MAP_COL_RED, MAP_COL_YELLOW
        ui = EntityHeadMarkUI()
        ui and ui.set_color_info(MAP_COL_GREEN)
        ui and ui.update_entity_ids(entity_ids)

    def get_custom_faction_members(self, faction_id):
        return self.custom_faction_members.get(faction_id, {})

    def get_custom_faction_members_ids(self, faction_id):
        return list(self.get_custom_faction_members(faction_id).keys())

    def get_enemy_faction_members(self, my_faction_id):
        all_enemies = {}
        for faction_id, members in six.iteritems(self.custom_faction_members):
            if faction_id == my_faction_id:
                continue
            all_enemies.update(members)

        return all_enemies

    def create_faction_danmu_controller(self):
        if not self.is_custom_faction_room:
            return None
        else:
            from logic.comsys.battle.FactionDanmuController import FactionDanmuController
            return FactionDanmuController()

    def destroy_faction_danmu_controller(self):
        if self.faction_danmu_controller:
            self.faction_danmu_controller.destroy()