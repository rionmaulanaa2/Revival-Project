# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/Gulag/GulagSurvivalBattleMgr.py
from __future__ import absolute_import
import six
import six_ex
import math3d
import collision
import world
import game3d
from common.utils import timer
from common.cfg import confmgr
from common.framework import Singleton
from logic.gcommon.const import NEOX_UNIT_SCALE
from logic.gcommon.common_const.collision_const import GROUP_SHOOTUNIT, GROUP_CHARACTER_INCLUDE, GROUP_GRENADE, GROUP_CAMERA_COLL
from logic.gutils.scene_utils import add_region_scene_collision
from logic.gcommon import time_utility
from common.utils.timer import CLOCK
from mobile.common.EntityManager import EntityManager
AREA = 'area'
ARENA = 'arena_list'
AREA_COL_GROUP = GROUP_SHOOTUNIT | GROUP_CHARACTER_INCLUDE | GROUP_GRENADE | GROUP_CAMERA_COLL
INNER_COL_MODEL_PATH = confmgr.get('script_gim_ref', 'region_collision_box')
OUTER_COL_MODEL_PATH = confmgr.get('script_gim_ref', 'region_collision_box_no_cull')
INNER_SHOW_MODEL_PATH = 'effect/mesh/scenes/kongdao/gulage_box_40.gim'
OUTER_SHOW_MODEL_PATH = 'effect/mesh/scenes/kongdao/gulage_box_20.gim'
COL_THICKNESS = 25
COL_HEIGHT = 6000
SHOW_HEIGHT = 2000
VISIBLE_DIST = 600 * NEOX_UNIT_SCALE
INNER_SHOW_MODEL = 'inner_show_model'
OUTER_SHOW_MODEL = 'outer_show_model'
OUTER_COL = 'outer_col'
INNER_COL = 'inner_col'
READY_COL_MODEL_PATH = confmgr.get('script_gim_ref', 'ffa_zhunbei_col')
READY_MODEL_PATH = confmgr.get('script_gim_ref', 'ffa_zhunbei')

class GulagSurvivalBattleMgr(Singleton):
    ALIAS_NAME = 'gulag_sur_battle_mgr'

    def init(self):
        self.revive_game_area = {}
        self.revive_game_area_info = confmgr.get('game_mode/gulag/play_data', 'revive_game_area')
        self.revive_game_area_visible = {}
        self.timer_id = global_data.game_mgr.register_logic_timer(self.tick, interval=0.5, times=-1, mode=CLOCK)
        self.ready_col_model_id = []
        self.ready_model_id = []
        self.ready_model = []
        self.cam_player_gulag_enemy_eid = None
        self.gulag_enemy_see_through = False
        self.enemy_evt_registed = False
        return

    def set_cam_gulag_enemy(self, eid):
        old_enemy_entity = EntityManager.getentity(self.cam_player_gulag_enemy_eid)
        if old_enemy_entity and old_enemy_entity.logic:
            old_enemy_entity.logic.send_event('E_ENABLE_SEE_THROUGHT', False)
            if self.enemy_evt_registed:
                old_enemy_entity.logic.unregist_event('E_ON_CONTROL_TARGET_CHANGE', self.refresh_gulag_enemy_see_through)
        self.enemy_evt_registed = False
        self.cam_player_gulag_enemy_eid = eid
        self.gulag_enemy_see_through = False
        new_enemy_entity = EntityManager.getentity(eid)
        if new_enemy_entity and new_enemy_entity.logic:
            new_enemy_entity.logic.regist_event('E_ON_CONTROL_TARGET_CHANGE', self.refresh_gulag_enemy_see_through)
            self.enemy_evt_registed = True

    def enable_gulag_enemy_see_through(self, enable):
        self.gulag_enemy_see_through = enable
        if not self.enemy_evt_registed:
            new_enemy_entity = EntityManager.getentity(self.cam_player_gulag_enemy_eid)
            if new_enemy_entity and new_enemy_entity.logic:
                new_enemy_entity.logic.regist_event('E_ON_CONTROL_TARGET_CHANGE', self.refresh_gulag_enemy_see_through)
                self.enemy_evt_registed = True
        self.refresh_gulag_enemy_see_through()

    def refresh_gulag_enemy_see_through(self, *args):
        enemy_ent = EntityManager.getentity(self.cam_player_gulag_enemy_eid)
        if not enemy_ent or not enemy_ent.logic or not enemy_ent.logic.sd.ref_ctrl_target or not enemy_ent.logic.sd.ref_ctrl_target.logic:
            self.need_refresh_enemy_see_through = True
            return
        ret = enemy_ent.logic.sd.ref_ctrl_target.logic.send_event('E_ENABLE_SEE_THROUGHT', self.gulag_enemy_see_through)
        self.need_refresh_enemy_see_through = not bool(ret)

    def tick--- This code section failed: ---

  92       0  LOAD_FAST             0  'self'
           3  LOAD_ATTR             0  'check_revive_game_area_show'
           6  CALL_FUNCTION_0       0 
           9  POP_TOP          

  93      10  LOAD_GLOBAL           1  'getattr'
          13  LOAD_GLOBAL           1  'getattr'
          16  LOAD_GLOBAL           2  'False'
          19  CALL_FUNCTION_3       3 
          22  POP_JUMP_IF_FALSE    38  'to 38'

  94      25  LOAD_FAST             0  'self'
          28  LOAD_ATTR             3  'refresh_gulag_enemy_see_through'
          31  CALL_FUNCTION_0       0 
          34  POP_TOP          
          35  JUMP_FORWARD          0  'to 38'
        38_0  COME_FROM                '35'

Parse error at or near `CALL_FUNCTION_3' instruction at offset 19

    def get_player_pos(self):
        cam_lplayer = global_data.cam_lplayer
        if cam_lplayer:
            control_target = cam_lplayer.ev_g_control_target()
            if control_target and control_target.logic:
                pos = control_target.logic.ev_g_model_position()
            else:
                pos = cam_lplayer.ev_g_model_position()
            if pos:
                return pos
        elif global_data.is_in_judge_camera:
            if global_data.game_mgr.scene:
                return global_data.game_mgr.scene.active_camera.world_position
        return global_data.sound_mgr.get_listener_pos()

    def on_enter_revive_game(self, game_detail):
        self.destroy_ready_box()
        fight_timestamp = game_detail['fight_timestamp']
        left_time = fight_timestamp - time_utility.time()
        if left_time <= 0:
            return
        game3d.delay_exec(left_time * 1000, self.destroy_ready_box)
        arena_no = game_detail['battlefield_no']
        arena_info = self.get_arena_info_with_arena_idx(arena_no)
        min_x, min_z, max_x, max_z, _ = arena_info['area_info']
        center = ((min_x + max_x) / 2, (min_z + max_z) / 2)
        for pos in arena_info['born_point']:
            self.create_ready_box(pos, center)

        for eid in game_detail.get('player_eids', []):
            if eid != global_data.cam_lplayer.id:
                self.cam_player_gulag_enemy_eid = eid
                break

    def get_arena_info_with_arena_idx(self, arena_idx):
        area_id, arena_idx = arena_idx.split('_')
        return self.revive_game_area_info[area_id][ARENA][int(arena_idx)]

    def create_ready_box(self, pos, center):

        def create_cb(model, flag=False):
            model.visible = flag
            model.set_col_group_mask(AREA_COL_GROUP, AREA_COL_GROUP)
            model.active_collision = True
            model.play_animation('standby1')
            up = math3d.vector(0, 1, 0)
            right = math3d.vector(pos[0] - center[0], 0, pos[2] - center[1])
            forward = up.cross(right)
            model.rotation_matrix = math3d.matrix.make_orient(forward, up)

        pos_vec = math3d.vector(*pos)
        self.ready_model_id.append(global_data.model_mgr.create_model_in_scene(READY_MODEL_PATH, pos_vec, on_create_func=lambda model: create_cb(model, True)))
        self.ready_col_model_id.append(global_data.model_mgr.create_model_in_scene(READY_COL_MODEL_PATH, pos_vec, on_create_func=create_cb))

    def destroy_ready_box(self):
        for model_id in self.ready_model_id:
            ready_model = global_data.model_mgr.get_model_by_id(model_id)
            if not ready_model or not ready_model.valid:
                global_data.model_mgr.remove_model_by_id(model_id)
            else:
                ready_model.play_animation('descent')
                game3d.delay_exec(3500, lambda m=ready_model: m and m.valid and m.play_animation('settledown'))
                game3d.delay_exec(4000, lambda mid=model_id: global_data.model_mgr.remove_model_by_id(mid))

        for model_id in self.ready_col_model_id:
            global_data.model_mgr.remove_model_by_id(model_id)

        self.ready_model_id = []
        self.ready_col_model_id = []

    def check_revive_game_area_show(self):
        player_pos = self.get_player_pos()
        p_x, p_z = player_pos.x, player_pos.z
        for area_id, area_info in six.iteritems(self.revive_game_area_info):
            if area_id not in self.revive_game_area_visible:
                self.revive_game_area_visible[area_id] = {AREA: {},ARENA: {}}
            min_x, min_z, max_x, max_z, height = area_info[AREA]
            area_visible = min_x - VISIBLE_DIST < p_x < max_x + VISIBLE_DIST and min_z - VISIBLE_DIST < p_z < max_z + VISIBLE_DIST
            arena_visible = area_visible and min_x < p_x < max_x and min_z < p_z < max_z
            outer_area_visible = area_visible and not arena_visible
            if self.revive_game_area_visible[area_id][AREA].get(OUTER_SHOW_MODEL, None) != outer_area_visible:
                self.revive_game_area_visible[area_id][AREA][OUTER_SHOW_MODEL] = outer_area_visible
                self.refresh_show_model_visible(outer_area_visible, area_id, OUTER_SHOW_MODEL)
            if self.revive_game_area_visible[area_id][AREA].get(INNER_SHOW_MODEL, None) != arena_visible:
                self.revive_game_area_visible[area_id][AREA][INNER_SHOW_MODEL] = arena_visible
                self.refresh_show_model_visible(arena_visible, area_id, INNER_SHOW_MODEL)
            in_arena = None
            if arena_visible:
                for arena_idx, arena_info in enumerate(area_info[ARENA]):
                    min_x, min_z, max_x, max_z, height = arena_info['area_info']
                    if min_x < p_x < max_x and min_z < p_z < max_z:
                        in_arena = arena_idx
                        break

            for arena_idx, arena_info in enumerate(area_info[ARENA]):
                if arena_idx not in self.revive_game_area_visible[area_id][ARENA]:
                    self.revive_game_area_visible[area_id][ARENA][arena_idx] = {INNER_SHOW_MODEL: None,OUTER_SHOW_MODEL: None}
                inner_show = in_arena == arena_idx
                outer_show = arena_visible and in_arena is None
                if self.revive_game_area_visible[area_id][ARENA][arena_idx].get(INNER_SHOW_MODEL) != inner_show:
                    self.revive_game_area_visible[area_id][ARENA][arena_idx][INNER_SHOW_MODEL] = inner_show
                    self.refresh_show_model_visible(inner_show, area_id, INNER_SHOW_MODEL, arena_idx)
                if self.revive_game_area_visible[area_id][ARENA][arena_idx].get(OUTER_SHOW_MODEL) != outer_show:
                    self.revive_game_area_visible[area_id][ARENA][arena_idx][OUTER_SHOW_MODEL] = outer_show
                    self.refresh_show_model_visible(outer_show, area_id, OUTER_SHOW_MODEL, arena_idx)

        return

    def init_all_revive_game_area(self):
        for area_id, area_info in six.iteritems(self.revive_game_area_info):
            self.revive_game_area[area_id] = {AREA: {},ARENA: []}
            self.init_revive_game_area(area_id, AREA, *area_info[AREA])
            for idx, arena_info in enumerate(area_info[ARENA]):
                min_x, min_z, max_x, max_z, height = arena_info['area_info']
                self.init_revive_game_area(area_id, ARENA, min_x, min_z, max_x, max_z, height, idx)

    def init_revive_game_area(self, area_id, kind, min_x, min_z, max_x, max_z, height, idx=0):
        if kind == AREA:
            area_dict = self.revive_game_area[area_id][kind]
        else:
            area_dict = {}
            self.revive_game_area[area_id][kind].append(area_dict)
        center = (
         (min_x + max_x) * 0.5, height, (min_z + max_z) * 0.5)
        area_dict[OUTER_COL + '_id'] = global_data.model_mgr.create_model_in_scene(OUTER_COL_MODEL_PATH, math3d.vector(*center), on_create_func=lambda model: self.on_revive_game_model_loaded(model, area_id, kind, idx, OUTER_COL))
        area_dict[INNER_COL + '_id'] = global_data.model_mgr.create_model_in_scene(INNER_COL_MODEL_PATH, math3d.vector(*center), on_create_func=lambda model: self.on_revive_game_model_loaded(model, area_id, kind, idx, INNER_COL))
        area_dict[INNER_SHOW_MODEL + '_id'] = global_data.model_mgr.create_model_in_scene(INNER_SHOW_MODEL_PATH, math3d.vector(*center), on_create_func=lambda model: self.on_revive_game_model_loaded(model, area_id, kind, idx, INNER_SHOW_MODEL))
        area_dict[OUTER_SHOW_MODEL + '_id'] = global_data.model_mgr.create_model_in_scene(OUTER_SHOW_MODEL_PATH, math3d.vector(*center), on_create_func=lambda model: self.on_revive_game_model_loaded(model, area_id, kind, idx, OUTER_SHOW_MODEL))

    def on_revive_game_model_loaded(self, model, area_id, kind, idx, model_type):
        if kind == AREA:
            min_x, min_z, max_x, max_z, height = self.revive_game_area_info[area_id][kind]
        else:
            min_x, min_z, max_x, max_z, height = self.revive_game_area_info[area_id][kind][idx]['area_info']
        if model_type in (INNER_COL, INNER_SHOW_MODEL):
            min_x += COL_THICKNESS
            min_z += COL_THICKNESS
            max_x -= COL_THICKNESS
            max_z -= COL_THICKNESS
        is_col = model_type in (INNER_COL, OUTER_COL)
        model.scale = math3d.vector((max_x - min_x) * 0.5 / model.bounding_box.x, (COL_HEIGHT if is_col else (max_x - min_x) * 0.5 + 500) / model.bounding_box.y, (max_z - min_z) * 0.5 / model.bounding_box.z)
        if is_col:
            model.set_col_group_mask(AREA_COL_GROUP, AREA_COL_GROUP)
            model.active_collision = True
        else:
            model.set_rendergroup_and_priority(world.RENDER_GROUP_DECAL, 0)
        if kind == AREA:
            self.revive_game_area[area_id][kind][model_type + '_id'] = None
            self.revive_game_area[area_id][kind][model_type] = model
            model.visible = self.revive_game_area_visible.get(area_id, {}).get(kind, {}).get(model_type, False)
        else:
            self.revive_game_area[area_id][kind][idx][model_type + '_id'] = None
            self.revive_game_area[area_id][kind][idx][model_type] = model
            model.visible = self.revive_game_area_visible.get(area_id, {}).get(kind, {}).get(idx, {}).get(model_type, False)
        return

    def refresh_show_model_visible(self, show_model, area_id, model_type, arena_idx=None):
        if area_id not in self.revive_game_area:
            return
        else:
            if arena_idx is None:
                area_model_dict = self.revive_game_area[area_id][AREA]
            elif arena_idx < len(self.revive_game_area[area_id][ARENA]):
                area_model_dict = self.revive_game_area[area_id][ARENA][arena_idx]
            else:
                return
            model = area_model_dict.get(model_type, None)
            if model and model.valid:
                model.visible = show_model
            return

    def clear_all(self):
        for area_id, area_info in six.iteritems(self.revive_game_area):
            area_model_dict = area_info[AREA]
            for model_type in (INNER_SHOW_MODEL, OUTER_SHOW_MODEL, OUTER_COL, INNER_COL):
                model = area_model_dict.get(model_type, None)
                if not model or not model.valid:
                    model_id = area_model_dict.get(model_type + '_id', None)
                    if model_id:
                        global_data.model_mgr.remove_model_by_id(model_id)
                else:
                    global_data.model_mgr.remove_model(model)

            for area_model_dict in area_info[ARENA]:
                for model_type in (INNER_SHOW_MODEL, OUTER_SHOW_MODEL, OUTER_COL, INNER_COL):
                    model = area_model_dict.get(model_type, None)
                    if not model or not model.valid:
                        model_id = area_model_dict.get(model_type + '_id', None)
                        if model_id:
                            global_data.model_mgr.remove_model_by_id(model_id)
                    else:
                        global_data.model_mgr.remove_model(model)

        self.revive_game_area = {}
        self.revive_game_area_visible = {}
        self.destroy_ready_box()
        return

    def on_finalize(self):
        self.clear_all()
        if self.timer_id:
            global_data.game_mgr.unregister_logic_timer(self.timer_id)
            self.timer_id = None
        return