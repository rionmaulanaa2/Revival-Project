# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/parts/battleprepare/BattlePrepare.py
from __future__ import absolute_import
from __future__ import print_function
import six
import six_ex
from logic.gcommon.common_utils import parachute_utils
from logic.client.const import game_mode_const
from logic.gcommon.common_const import collision_const
from mobile.common.EntityManager import EntityManager
from mobile.common.EntityFactory import EntityFactory
from mobile.common.IdManager import IdManager
from logic.comsys.battle import BattleUtils
from logic.gutils import scene_utils
from common.utils import timer
from logic.gcommon import time_utility as tutil
import world
import math3d
import collision
import math
import game3d
import os
from common.cfg import confmgr
from common.framework import Functor
from logic.gcommon.common_const import battle_const
_HASH_Alpha = game3d.calc_string_hash('Alpha')
_HASH_Color_Bright = game3d.calc_string_hash('change_color_bright')
_HASH_Depth_Outline_Color = game3d.calc_string_hash('depth_outline_color')

class BattlePrepareBase(object):

    def __init__(self, parent):
        self.battle_prepare = parent
        self.process_event(True)

    def get_event_conf(self):
        return {}

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'on_player_parachute_stage_changed': self.on_player_parachute_stage_changed
           }
        econf.update(self.get_event_conf())
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def on_player_parachute_stage_changed(self, stage):
        if not global_data.cam_lplayer:
            return
        if stage == parachute_utils.STAGE_SORTIE_PREPARE:
            global_data.cam_lplayer.send_event('E_ON_CONTROL_TARGET_CHANGE', global_data.cam_lplayer.id, global_data.cam_lplayer.ev_g_foot_position())
            global_data.emgr.camera_inited_event.emit()

    def on_enter(self):
        pass

    def on_pre_load(self):
        pass

    def on_exit(self):
        self.process_event(False)


class BattleRangeMgr(object):

    def __init__(self):
        self._move_range_model_id = None
        self._model = None
        self._region_col_model = None
        self._limit_height_col = None
        self.set_trigger_timer = None
        self._update_range_related_data()
        self._register_events()
        return

    def _register_events(self):
        global_data.emgr.camera_lctarget_open_prez += self.on_open_prez

    def _unregister_events(self):
        global_data.emgr.camera_lctarget_open_prez -= self.on_open_prez

    def is_in_battle_boundary(self, px, py, pz, margin=0):
        move_range = self._range_data[0] if self._range_data else None
        if move_range is None:
            return False
        else:
            min_x = min(move_range[0][0], move_range[1][0])
            max_x = max(move_range[0][0], move_range[1][0])
            min_z = min(move_range[0][1], move_range[1][1])
            max_z = max(move_range[0][1], move_range[1][1])
            if px < min_x + margin or px > max_x - margin:
                return False
            if pz < min_z + margin or pz > max_z - margin:
                return False
            return True

    def _update_range_related_data(self):
        battle = global_data.battle
        if not battle:
            self._range_data = None
            return
        else:
            born_data = global_data.game_mode.get_born_data()
            move_range = born_data[str(battle.area_id)].get('move_range')
            move_height = born_data[str(battle.area_id)].get('move_height', 0.0)
            limit_height = born_data[str(battle.area_id)].get('limit_height')
            range_index = born_data[str(battle.area_id)].get('range_index')
            self._range_data = (
             move_range, move_height, limit_height, range_index)
            return

    def recreate_all_range_model(self):
        self.destroy_all_range_model()
        self.create_all_range_model()

    def create_all_range_model(self):
        battle = global_data.battle
        if not battle:
            return
        else:
            if self._move_range_model_id:
                return
            move_range = self._range_data[0] if self._range_data else None
            move_height = self._range_data[1] if self._range_data else 0.0
            limit_height = self._range_data[2] if self._range_data else None
            range_index = self._range_data[3] if self._range_data else None
            if range_index:
                self._region_col_model = self.create_special_range_model(range_index, move_range, move_height, limit_height, need_col=True)
            else:
                barrier_model_path = confmgr.get('script_gim_ref')['region_range_blue']
                self._region_col_model = self.create_range_model(barrier_model_path, move_range, move_height, limit_height, need_col=True)
            return

    def create_special_range_model(self, range_index, range_data, move_height, limit_height, need_col=False):
        if not range_data:
            return []
        else:
            range_sfx_data = global_data.game_mode.get_cfg_data('range_sfx_data')
            if not range_sfx_data:
                return []
            range_sfx_info = range_sfx_data.get(str(range_index))
            if not range_sfx_info:
                return []
            path = range_sfx_info.get('cSfxPath')
            rot = range_sfx_info.get('cRot')
            scale = range_sfx_info.get('cScale')
            col_path = range_sfx_info.get('cColPath')
            sfx_pos = range_sfx_info.get('cSfxPos')
            is_full_col = range_sfx_info.get('iFullCol')
            min_x = min(range_data[0][0], range_data[1][0])
            max_x = max(range_data[0][0], range_data[1][0])
            min_z = min(range_data[0][1], range_data[1][1])
            max_z = max(range_data[0][1], range_data[1][1])
            if sfx_pos:
                center = math3d.vector(*sfx_pos)
                center_x = center.x
                center_z = center.z
            else:
                center_x = (min_x + max_x) * 0.5
                center_z = (min_z + max_z) * 0.5
                center = math3d.vector(center_x, move_height, center_z)

            def on_range_model(model, sfx_pos=sfx_pos, rot=rot, scale=scale):
                model.world_scale = math3d.vector(*scale)
                model.rotation_matrix = math3d.euler_to_matrix(math3d.vector(math.pi * rot[0] / 180, math.pi * rot[1] / 180, math.pi * rot[2] / 180))
                if not sfx_pos:
                    model.world_position = model.world_position - model.center * model.world_scale * model.rotation_matrix
                model.set_rendergroup_and_priority(world.RENDER_GROUP_DECAL, 0)
                self._model = model

            self._move_range_model_id = global_data.model_mgr.create_model_in_scene(path, center, on_create_func=on_range_model)
            col_model = None
            if need_col:
                length, width, height = (max_x - min_x) * 0.5, (max_z - min_z) * 0.5, limit_height or 2000

                def create_col_cb(model, sfx_pos=sfx_pos, rot=rot, scale=scale, is_full_col=is_full_col):
                    model.visible = False
                    group = collision_const.TERRAIN_MASK if is_full_col else collision_const.REGION_BOUNDARY_SCENE_GROUP
                    if is_full_col:
                        mask = collision_const.TERRAIN_MASK if 1 else collision_const.REGION_BOUNDARY_SCENE_MASK
                        model.set_col_group_mask(group, mask)
                        model.active_collision = True
                        model.world_scale = math3d.vector(*scale)
                        model.rotation_matrix = math3d.euler_to_matrix(math3d.vector(math.pi * rot[0] / 180, math.pi * rot[1] / 180, math.pi * rot[2] / 180))
                        model.world_position = sfx_pos or model.world_position - model.center * model.world_scale * model.rotation_matrix

                col_model = global_data.model_mgr.create_model_in_scene(col_path, center, on_create_func=create_col_cb)
                trigger_pos = math3d.vector(center_x, height, center_z)
                trigger_size = math3d.vector(length, 5, width)
                self.add_limit_height_trigger(trigger_pos, trigger_size)
            return col_model

    def create_range_model(self, path, range_data, move_height, limit_height, need_col=False):
        if not range_data:
            return []
        else:
            min_x = min(range_data[0][0], range_data[1][0])
            max_x = max(range_data[0][0], range_data[1][0])
            min_z = min(range_data[0][1], range_data[1][1])
            max_z = max(range_data[0][1], range_data[1][1])
            center_x = (min_x + max_x) * 0.5
            center_z = (min_z + max_z) * 0.5
            center = math3d.vector(center_x, move_height, center_z)

            def on_range_model(model):
                scale_x = (max_x - min_x) / (model.bounding_box.x * 2)
                scale_z = (max_z - min_z) / (model.bounding_box.z * 2)
                model.world_scale = math3d.vector(scale_x, 10.0, scale_z)
                model.set_rendergroup_and_priority(world.RENDER_GROUP_DECAL, 0)
                model.rotation_matrix = math3d.euler_to_matrix(math3d.vector(0, 0, 0))
                self._model = model

            self._move_range_model_id = global_data.model_mgr.create_model_in_scene(path, center, on_create_func=on_range_model)
            col_model = None
            if need_col:
                center, length, width, height = (
                 (
                  center_x, move_height, center_z), (max_x - min_x) * 0.5, (max_z - min_z) * 0.5, limit_height or 2000)
                col_model = scene_utils.add_region_scene_collision_box(center, length, width, height)
                trigger_pos = math3d.vector(center_x, height, center_z)
                trigger_size = math3d.vector(length, 5, width)
                self.add_limit_height_trigger(trigger_pos, trigger_size)
            return col_model

    def add_limit_height_trigger(self, pos, size):
        _scn = world.get_active_scene()
        mask = collision_const.TERRAIN_MASK
        group = collision_const.REGION_SCENE_GROUP
        col = collision.col_object(collision.BOX, size, mask, group, 0, True)
        col.position = pos
        col.set_trigger(True)
        col.set_trigger_callback(Functor(self._trigger_cb))
        _scn.scene_col.add_object(col)
        self._limit_height_col = col

    def _trigger_cb(self, *args):
        if global_data.player and global_data.player.logic:
            character_col = global_data.player.logic.sd.ref_character
            if not character_col:
                mecha_id = global_data.player.logic.ev_g_ctrl_mecha()
                mecha = EntityManager.getentity(mecha_id)
                if mecha and mecha.logic:
                    character_col = mecha.logic.sd.ref_character
                if not character_col:
                    return
            trigger, col, is_in = args
            if character_col.cid == col.cid:
                self.clear_timer()
                if is_in:

                    def _show_tips():
                        global_data.game_mgr.show_tip(get_text_by_id(19926))

                    self.set_trigger_timer = global_data.game_mgr.get_logic_timer().register(func=_show_tips, mode=timer.CLOCK, interval=5)
                    _show_tips()

    def clear_timer(self):
        self.set_trigger_timer and global_data.game_mgr.get_logic_timer().unregister(self.set_trigger_timer)
        self.set_trigger_timer = None
        return

    def destroy_range_sfx(self):
        if self._move_range_model_id:
            global_data.model_mgr.remove_model_by_id(self._move_range_model_id)
        self._move_range_model_id = None
        self._model = None
        return

    def remove_col(self):
        if self._region_col_model:
            global_data.model_mgr.remove_model_by_id(self._region_col_model)
        self._region_col_model = None
        _scn = world.get_active_scene()
        if self._limit_height_col and self._limit_height_col.valid:
            _scn.scene_col.remove_object(self._limit_height_col)
        self._limit_height_col = None
        return

    def on_open_prez(self, enable):
        if self._model:
            if enable:
                self._model.all_materials.set_macro('DEPTH_OUTLINE', 'FALSE')
            else:
                self._model.all_materials.set_macro('DEPTH_OUTLINE', 'TRUE')
            self._model.all_materials.rebuild_tech()

    def destroy_all_range_model(self):
        self.destroy_range_sfx()
        self.remove_col()
        self.clear_timer()

    def destroy(self):
        self.destroy_all_range_model()
        self._unregister_events()


class BattleRangeEXMgr(object):

    def __init__(self):
        self._move_range_model_id = None
        self._model = None
        self._region_col_model = None
        self._region_col_model_1 = None
        self._range_data = None
        self.rotate_y = 0
        self._update_range_related_data()
        return

    def _update_range_related_data(self):
        battle = global_data.battle
        if not battle:
            self._range_data = None
            return
        else:
            born_data = global_data.game_mode.get_born_data()
            center = born_data[str(battle.area_id)].get('center')
            radius = born_data[str(battle.area_id)].get('radius')
            height = born_data[str(battle.area_id)].get('height')
            range_index = born_data[str(battle.area_id)].get('range_index')
            self.rotate_y = born_data[str(battle.area_id)].get('rotate_y', 0)
            self._range_data = (
             center, radius, height, range_index)
            return

    def recreate_all_range_model(self):
        self.destroy_all_range_model()
        self.create_all_range_model()

    def create_all_range_model(self):
        battle = global_data.battle
        if not battle:
            return
        if self._move_range_model_id:
            return
        if not self._range_data:
            return
        center, radius, height = self._range_data
        barrier_model_path = confmgr.get('script_gim_ref')['region_range_blue']
        self._region_col_model, self._region_col_model_1 = self.create_range_model(barrier_model_path, center, radius, height, need_col=True)

    def create_range_model(self, path, center, radius, height, need_col=False):
        center = math3d.vector(center[0], height, center[1])
        length, width = radius

        def on_range_model(model):
            scale_x = length / model.bounding_box.x
            scale_z = width / model.bounding_box.z
            model.world_scale = math3d.vector(scale_x, 4.0, scale_z)
            model.set_rendergroup_and_priority(world.RENDER_GROUP_DECAL, 0)
            if self.rotate_y:
                model.rotate_y(self.rotate_y / 180.0 * math.pi)
            self._model = model

        self._move_range_model_id = global_data.model_mgr.create_model_in_scene(path, center, on_create_func=on_range_model)
        col_model = None
        col_model_1 = None
        if need_col:
            col_model, col_model_1 = scene_utils.add_region_scene_collision_box(center, length, width, rotate_y=self.rotate_y, cull=False)
        return (col_model, col_model_1)

    def destroy_range_sfx(self):
        if self._move_range_model_id:
            global_data.model_mgr.remove_model_by_id(self._move_range_model_id)
        self._move_range_model_id = None
        self._model = None
        return

    def remove_col(self):
        if self._region_col_model:
            global_data.model_mgr.remove_model_by_id(self._region_col_model)
        self._region_col_model = None
        if self._region_col_model_1:
            global_data.model_mgr.remove_model_by_id(self._region_col_model_1)
        self._region_col_model_1 = None
        return

    def destroy_all_range_model(self):
        self.destroy_range_sfx()
        self.remove_col()

    def destroy(self):
        self.destroy_all_range_model()


class BattleSpawnMgr():
    spawn_appear_sfxs = ('effect/fx/scenes/common/sidou/xuebao_01.sfx', 'effect/fx/scenes/common/sidou/xuebao_red_01.sfx')
    spawn_disappear_sfxs = ('effect/fx/scenes/common/sidou/xuebao_02.sfx', 'effect/fx/scenes/common/sidou/xuebao_red_02.sfx')
    spawn_cd_sfx = 'effect/fx/niudan/xuebao/daojishi_01.sfx'

    def __init__(self):
        self._spawn_info = {}
        self._spawn_entity_id = {}
        self._spaw_appear_sfx_id = {}
        self._spaw_disappear_sfx_id = {}
        self._spaw_cd_sfx_id = {}
        self._item_model_ids = []
        self._item_model_col = []
        self._spawn_cd_check_timer = None
        self.process_event(True)
        return

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'scene_add_pickable_model_event': self.on_add_model,
           'scene_del_pickable_model_event': self.on_del_model,
           'scene_refresh_use_item_cd': self.on_refresh_use_item_cd,
           'scene_camera_switch_player_setted_event': self.on_camera_player_setted,
           'update_spawn_rebirth_data_event': self.on_update_spawn_rebirth_data
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def clear_spawn_cd_check_timer(self):
        self._spawn_cd_check_timer and global_data.game_mgr.get_logic_timer().unregister(self._spawn_cd_check_timer)
        self._spawn_cd_check_timer = None
        return

    def on_camera_player_setted(self, *args):
        self.refresh_sfx()
        self.on_update_spawn_rebirth_data()

    def refresh_sfx(self):
        for spawn_id, id in six.iteritems(self._spawn_entity_id):
            self.spawn_appear(spawn_id, id)

    def get_spawn_entity_id(self):
        return self._spawn_entity_id

    def init_spawn(self):
        battle = global_data.battle
        if not battle:
            return
        self._spawn_info = {}
        born_data = global_data.game_mode.get_born_data()
        born_spawn_data = global_data.game_mode.get_cfg_data('born_spawn_data')
        spawn_lst = born_data[str(battle.area_id)].get('spawn_lst', [])
        for spawn_id in spawn_lst:
            if str(spawn_id) in born_spawn_data:
                self._spawn_info[spawn_id] = born_spawn_data[str(spawn_id)]

        self.refresh_sfx()
        self.create_item_model()
        self.clear_spawn_cd_check_timer()
        self._spawn_cd_check_timer = global_data.game_mgr.get_logic_timer().register(func=self.update_spawn_cd_show, mode=timer.LOGIC, interval=3, times=-1)

    def on_refresh_use_item_cd(self):
        for entity_id in six.itervalues(self._spawn_entity_id):
            item_entity = EntityManager.getentity(entity_id)
            if item_entity and item_entity.logic:
                item_entity.logic.send_event('E_REFRESH_ITEM_CD')

    def on_add_model(self, model, ids, spawn_id):
        if spawn_id:
            self.spawn_appear(spawn_id, ids[0])

    def is_teammate(self, entity_id):
        if not entity_id:
            return True
        item_entity = EntityManager.getentity(entity_id)
        if item_entity and item_entity.logic:
            return item_entity.logic.ev_g_is_teammate_item()
        return True

    def spawn_appear(self, spawn_id, id):
        if spawn_id in self._spaw_disappear_sfx_id:
            global_data.sfx_mgr.remove_sfx_by_id(self._spaw_disappear_sfx_id[spawn_id])
            del self._spaw_disappear_sfx_id[spawn_id]
        if spawn_id in self._spaw_cd_sfx_id:
            global_data.sfx_mgr.remove_sfx_by_id(self._spaw_cd_sfx_id[spawn_id])
            del self._spaw_cd_sfx_id[spawn_id]
        if spawn_id in self._spawn_info:
            self._spawn_entity_id[spawn_id] = id
            if spawn_id in self._spaw_appear_sfx_id:
                global_data.sfx_mgr.remove_sfx_by_id(self._spaw_appear_sfx_id[spawn_id])
            x, y, z = self._spawn_info[spawn_id].get('pos')
            sfx_pos = math3d.vector(x, y, z)
            is_teammate = self.is_teammate(id)
            self._spaw_appear_sfx_id[spawn_id] = global_data.sfx_mgr.create_sfx_in_scene(self.spawn_appear_sfxs[0 if is_teammate else 1], sfx_pos)

    def on_del_model(self, model, spawn_id):
        self.spawn_disappear(spawn_id)

    def spawn_disappear(self, spawn_id):
        if spawn_id in self._spaw_appear_sfx_id:
            global_data.sfx_mgr.remove_sfx_by_id(self._spaw_appear_sfx_id[spawn_id])
            del self._spaw_appear_sfx_id[spawn_id]
        if spawn_id in self._spawn_info:
            if spawn_id in self._spaw_disappear_sfx_id:
                global_data.sfx_mgr.remove_sfx_by_id(self._spaw_disappear_sfx_id[spawn_id])
            x, y, z = self._spawn_info[spawn_id].get('pos')
            sfx_pos = math3d.vector(x, y, z)
            is_teammate = self.is_teammate(self._spawn_entity_id.get(spawn_id))
            self._spaw_disappear_sfx_id[spawn_id] = global_data.sfx_mgr.create_sfx_in_scene(self.spawn_disappear_sfxs[0 if is_teammate else 1], sfx_pos)
            if spawn_id in self._spawn_entity_id:
                del self._spawn_entity_id[spawn_id]

    def create_spwan_cd_sfx(self, spawn_id, faction_id, rebirth_ts):
        if spawn_id not in self._spawn_info:
            return
        if spawn_id in self._spaw_cd_sfx_id:
            global_data.sfx_mgr.remove_sfx_by_id(self._spaw_cd_sfx_id[spawn_id])
        x, y, z = self._spawn_info[spawn_id].get('pos')
        sfx_pos = math3d.vector(x, y, z)
        now = tutil.time()
        is_teammate = global_data.player.logic.ev_g_is_campmate(faction_id) if faction_id != 0 else True
        if is_teammate and now < rebirth_ts:
            cd = self._spawn_info[spawn_id].get('delay_time', 40)

            def call_back(sfx, cd=cd, rebirth_ts=rebirth_ts, *args):
                now = tutil.time()
                left_time = rebirth_ts - now
                pos = sfx.position
                sfx.position = math3d.vector(pos.x, pos.y + 20, pos.z)
                sfx.set_curtime_directly(sfx.life_span * 1.0 / cd * (cd - left_time))
                sfx.frame_rate = sfx.life_span * 1.0 / cd
                sfx.visible = self.check_spawn_cd_show(spawn_id)

            self._spaw_cd_sfx_id[spawn_id] = global_data.sfx_mgr.create_sfx_in_scene(self.spawn_cd_sfx, sfx_pos, on_create_func=call_back)

    def _get_battle_data(self):
        battle_data = None
        if global_data.death_battle_data:
            battle_data = global_data.death_battle_data
        elif global_data.ffa_battle_data:
            battle_data = global_data.ffa_battle_data
        elif global_data.zombieffa_battle_data:
            battle_data = global_data.zombieffa_battle_data
        elif global_data.gvg_battle_data:
            battle_data = global_data.gvg_battle_data
        return battle_data

    def on_update_spawn_rebirth_data(self, spwan_ids=None):
        battle_data = self._get_battle_data()
        if not battle_data:
            return
        else:
            if spwan_ids is None:
                spwan_ids = six_ex.keys(battle_data.spawn_rebirth_dict)
            for spawn_id in spwan_ids:
                faction_id, rebirth_ts = battle_data.get_spawn_rebirth_data(spawn_id)
                self.create_spwan_cd_sfx(spawn_id, faction_id, rebirth_ts)

            return

    def update_spawn_cd_show(self):
        for spawn_id, sfx_id in six.iteritems(self._spaw_cd_sfx_id):
            sfx = global_data.sfx_mgr.get_sfx_by_id(sfx_id)
            if sfx:
                sfx.visible = self.check_spawn_cd_show(spawn_id)

    def check_spawn_cd_show(self, spawn_id):
        born_idx = self._spawn_info[spawn_id].get('born_idx', -1)
        if not global_data.death_battle_data:
            return True
        if born_idx == -1:
            return True
        my_score, other_score = global_data.death_battle_data.get_group_score()
        show = True
        if not global_data.battle or not global_data.battle.settle_timestamp:
            return False
        if tutil.time() < global_data.battle.settle_timestamp - battle_const.PRE_SCORE_DIFF_MINUTES * tutil.ONE_MINUTE_SECONDS:
            if my_score > other_score - int(battle_const.PRE_SCORE_DIFF * global_data.battle.get_settle_point()):
                show = False
        elif my_score > other_score - int(battle_const.LATER_SCORE_DIFF * global_data.battle.get_settle_point()):
            show = False
        return show

    def create_item_model(self):
        if self._item_model_ids:
            return
        model_path = confmgr.get('script_gim_ref')['drug_path']
        for key, value in six.iteritems(self._spawn_info):
            x, y, z = value.get('pos')
            model_pos = math3d.vector(x, y, z)

            def create_model_cb(model):
                _scn = world.get_active_scene()
                if not _scn:
                    return
                mask = collision_const.GROUP_CHARACTER_INCLUDE
                group = collision_const.METAL_GROUP
                col = collision.col_object(collision.MESH, model, mask, group, 0, True)
                col.position = model.position
                _scn.scene_col.add_object(col)
                self._item_model_col.append(col)

            item_mode_id = global_data.model_mgr.create_model_in_scene(model_path, model_pos, on_create_func=create_model_cb)
            self._item_model_ids.append(item_mode_id)

    def destroy_item_model(self):
        for item_mode_id in self._item_model_ids:
            global_data.model_mgr.remove_model_by_id(item_mode_id)

        self._item_model_ids = []
        _scn = world.get_active_scene()
        for col in self._item_model_col:
            if col and col.valid:
                _scn.scene_col.remove_object(col)

        self._item_model_col = []

    def destroy_spaw_sfx(self):
        for sfx_id in six.itervalues(self._spaw_appear_sfx_id):
            global_data.sfx_mgr.remove_sfx_by_id(sfx_id)

        self._spaw_appear_sfx_id = {}
        for sfx_id in six.itervalues(self._spaw_disappear_sfx_id):
            global_data.sfx_mgr.remove_sfx_by_id(sfx_id)

        self._spaw_disappear_sfx_id = {}
        for sfx_id in six.itervalues(self._spaw_cd_sfx_id):
            global_data.sfx_mgr.remove_sfx_by_id(sfx_id)

        self._spaw_cd_sfx_id = {}

    def destroy(self):
        self.clear_spawn_cd_check_timer()
        self.destroy_item_model()
        self.destroy_spaw_sfx()
        self.process_event(False)


class BattleSfxMgr():

    def __init__(self):
        self._scene_sfx = []
        self._scene_model = []
        self._model_cols = []

    def init_scene_sfx(self):
        battle = global_data.battle
        if not battle:
            return
        if self._scene_sfx or self._scene_model:
            return
        born_cfg_data = global_data.game_mode.get_born_data()
        scene_sfxs = born_cfg_data[str(battle.area_id)].get('scene_sfx')
        if not scene_sfxs:
            return
        self.create_sfx(scene_sfxs)

    def create_sfx(self, scene_sfxs):
        scene_sfx_data = global_data.game_mode.get_cfg_data('scene_sfx_data')
        for sfx_index in scene_sfxs:
            sfx_data = scene_sfx_data.get(str(sfx_index))
            if not sfx_data:
                continue
            x, y, z = sfx_data.get('pos')
            position = math3d.vector(x, y, z)
            sfx_path = sfx_data.get('sfx_path')

            def create_sfx_cb(sfx, sfx_data=sfx_data):
                sx, sy, sz = sfx_data.get('scale')
                dx, dy, dz = sfx_data.get('rot')
                sfx.scale = math3d.vector(sx, sy, sz)
                sfx.rotation_matrix = math3d.euler_to_matrix(math3d.vector(math.pi * dx / 180, math.pi * dy / 180, math.pi * dz / 180))

            def create_model_cb(model, model_data=sfx_data):
                has_collision = model_data.get('has_collision', False)
                is_slope_collision = model_data.get('is_slope_collision', False)
                sx, sy, sz = model_data.get('scale')
                dx, dy, dz = model_data.get('rot')
                model.scale = math3d.vector(sx, sy, sz)
                model.rotation_matrix = math3d.euler_to_matrix(math3d.vector(math.pi * dx / 180, math.pi * dy / 180, math.pi * dz / 180))
                _scn = world.get_active_scene()
                if not _scn:
                    return
                if has_collision:
                    if is_slope_collision:
                        model.visible = False
                        model.set_col_group_mask(collision_const.SLOPE_GROUP, collision_const.SLOPE_GROUP)
                        model.active_collision = True
                    else:
                        mask = collision_const.TERRAIN_MASK
                        group = collision_const.TERRAIN_GROUP
                        col = collision.col_object(collision.MESH, model, mask, group, 0, True)
                        col.position = model.position
                        col.rotation_matrix = model.rotation_matrix
                        _scn.scene_col.add_object(col)
                        self._model_cols.append(col)

            if sfx_path.endswith('.sfx'):
                sfx_id = global_data.sfx_mgr.create_sfx_in_scene(sfx_path, position, on_create_func=create_sfx_cb)
                sfx_id and self._scene_sfx.append(sfx_id)
            else:
                model_id = global_data.model_mgr.create_model_in_scene(sfx_path, position, on_create_func=create_model_cb)
                model_id and self._scene_model.append(model_id)

    def destroy_scene_sfx_and_model(self):
        for sfx_id in self._scene_sfx:
            global_data.sfx_mgr.remove_sfx_by_id(sfx_id)

        self._scene_sfx = []
        for model_id in self._scene_model:
            global_data.model_mgr.remove_model_by_id(model_id)

        self._scene_model = []
        _scn = world.get_active_scene()
        for col in self._model_cols:
            _scn.scene_col.remove_object(col)

        self._model_cols = []

    def destroy(self):
        self.destroy_scene_sfx_and_model()


class BattleReadyBoxMgr():
    COL_MODEL_PATH = confmgr.get('script_gim_ref')['ffa_zhunbei_col']
    MODEL_PATH = confmgr.get('script_gim_ref')['ffa_zhunbei']

    def __init__(self):
        self.ready_col = []
        self.ready_col_model = []
        self.ready_model_col = []
        self.ready_model = []
        self.del_col_timer = None
        self.delay_disappear_timer = None
        self.del_model_timer = None
        self.process_event(True)
        return

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'battle_change_prepare_timestamp': self.change_prepare_timestamp
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def change_prepare_timestamp(self):
        self.refresh_ready_box()

    def get_left_time(self):
        return BattleUtils.get_prepare_left_time(0)

    def refresh_ready_box(self):
        self.clear_ready_box()
        self.init_ready_box()

    def clear_ready_box(self):
        self.clear_timer()
        self.clear_col()
        self.clear_model()

    def init_ready_box(self):
        battle = global_data.battle
        if not battle:
            return
        revive_time = self.get_left_time()
        if global_data.game_mode.is_mode_type((game_mode_const.GAME_MODE_DUEL,)):
            print('TTTT BattleReadyBoxMgr revive_time:', revive_time)
        born_cfg_data = global_data.game_mode.get_born_data()
        born_data = born_cfg_data[str(battle.area_id)]
        born_pos = born_data.get('born_pos')
        readybox_scale = born_data.get('readybox_scale', [1, 1, 1])
        readybox_scale = math3d.vector(*readybox_scale)
        self.face_pos = math3d.vector(*born_data.get('map_center'))
        if revive_time > 0:
            if not self.ready_col_model:
                for pos in born_pos:
                    pos = math3d.vector(*pos)

                    def create_cb(model):
                        model.visible = False
                        model_pos = model.position
                        model.scale = readybox_scale
                        mask = collision_const.TERRAIN_MASK
                        group = collision_const.REGION_SCENE_GROUP
                        col = collision.col_object(collision.MESH, model, mask, group, 0, True)
                        col.position = model_pos
                        _scn = world.get_active_scene()
                        _scn.scene_col.add_object(col)
                        self.ready_col.append(col)
                        global_data.battle_ready_box_col_ids.add(col.cid)

                    col_model_id = global_data.model_mgr.create_model_in_scene(self.COL_MODEL_PATH, pos, on_create_func=create_cb)
                    self.ready_col_model.append(col_model_id)

            self.clear_col_timer()
            self.del_col_timer = global_data.game_mgr.get_logic_timer().register(func=self.open_box, mode=timer.CLOCK, interval=revive_time + 1, times=1)
            if not self.ready_model:
                for pos in born_pos:
                    pos = math3d.vector(*pos)
                    self.create_model(pos, readybox_scale)

    def create_model(self, model_pos, readybox_scale=None):

        def create_cb(model):
            model.anim_skip_update_enabled = False
            model_pos = model.position
            if readybox_scale:
                model.scale = readybox_scale
            model.play_animation('standby1')
            look_at_dir = model_pos - self.face_pos
            if look_at_dir.length > 1:
                look_at_yaw = look_at_dir.yaw
                mat = math3d.matrix.make_rotation_y(look_at_yaw + math.pi * 90 / 180)
                model.rotation_matrix = mat
            mask = collision_const.TERRAIN_MASK
            group = collision_const.REGION_SCENE_GROUP
            col = collision.col_object(collision.MESH, model, mask, group, 0, True)
            col.position = model_pos
            _scn = world.get_active_scene()
            _scn.scene_col.add_object(col)
            self.ready_model_col.append(col)
            global_data.battle_ready_box_col_ids.add(col.cid)

        model_id = global_data.model_mgr.create_model_in_scene(self.MODEL_PATH, model_pos, on_create_func=create_cb)
        self.ready_model.append(model_id)

    def clear_col_timer(self):
        self.del_col_timer and global_data.game_mgr.get_logic_timer().unregister(self.del_col_timer)
        self.del_col_timer = None
        return

    def clear_disappear_timer(self):
        self.delay_disappear_timer and global_data.game_mgr.get_logic_timer().unregister(self.delay_disappear_timer)
        self.delay_disappear_timer = None
        return

    def clear_del_model_timer(self):
        self.del_model_timer and global_data.game_mgr.get_logic_timer().unregister(self.del_model_timer)
        self.del_model_timer = None
        return

    def open_box(self):
        if global_data.game_mode.is_mode_type((game_mode_const.GAME_MODE_DUEL,)):
            print('TTTT open_box')
        if self.delay_disappear_timer:
            return
        self.clear_col()
        for model_id in self.ready_model:
            model = global_data.model_mgr.get_model_by_id(model_id)
            if model and model.valid:
                model.play_animation('descent')

        self.delay_disappear_timer = global_data.game_mgr.get_logic_timer().register(func=self.model_disappear, mode=timer.CLOCK, interval=5, times=1)

    def model_disappear(self):
        if self.del_model_timer:
            return
        for model_id in self.ready_model:
            model = global_data.model_mgr.get_model_by_id(model_id)
            if model and model.valid:
                model.play_animation('settledown')

        self.del_model_timer = global_data.game_mgr.get_logic_timer().register(func=self.clear_model, mode=timer.CLOCK, interval=2, times=1)

    def clear_col(self):
        for model_id in self.ready_col_model:
            global_data.model_mgr.remove_model_by_id(model_id)

        self.ready_col_model = []
        _scn = world.get_active_scene()
        for col in self.ready_col:
            _scn.scene_col.remove_object(col)

        self.ready_col = []
        global_data.battle_ready_box_col_ids.clear()

    def clear_model(self):
        for model_id in self.ready_model:
            global_data.model_mgr.remove_model_by_id(model_id)

        self.ready_model = []
        _scn = world.get_active_scene()
        for col in self.ready_model_col:
            _scn.scene_col.remove_object(col)

        self.ready_model_col = []
        self.clear_disappear_timer()
        self.clear_del_model_timer()

    def clear_timer(self):
        self.clear_col_timer()
        self.clear_disappear_timer()
        self.clear_del_model_timer()

    def destroy(self):
        self.clear_timer()
        self.clear_col()
        self.clear_model()
        self.process_event(False)


class BattleFlagMgr():

    def __init__(self):
        self._battle_flag_entity_id = []
        self._free_battle_flag_entity_id = [[], []]
        self.process_event(True)

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'add_battle_flag_event': self.add_battle_flag
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def init_battle_flag(self):
        battle = global_data.battle
        if not battle:
            return
        else:
            if self._battle_flag_entity_id:
                return
            born_cfg_data = global_data.game_mode.get_born_data()
            battle_flags = born_cfg_data[str(battle.area_id)].get('battle_flag')
            if not battle_flags:
                return
            battle_flag_info = battle.get_battle_flag()
            all_battle_flag = [[], []]
            for info in battle_flag_info:
                born_idx, battle_flag = info
                all_battle_flag[born_idx].append(battle_flag)

            for born_idx, tv_ids in enumerate(battle_flags):
                infos = all_battle_flag[born_idx]
                for i, tv_id in enumerate(tv_ids):
                    if i < len(infos):
                        self._add_entity(born_idx, tv_id, infos[i], True)
                    else:
                        self._add_entity(born_idx, tv_id, None, False)

            return

    def _add_entity(self, born_idx, tv_id, info, show):
        entity_id = IdManager.genid()
        television_sub_model_path = confmgr.get('script_gim_ref')['prepare_television_sub']
        entity_obj = EntityFactory.instance().create_entity('Television', entity_id)
        entity_obj.init_from_dict({'tv_id': tv_id,
           'is_client': True,'is_show': show,'show_info': info,'sub_model_pos_off': (0, -26, 0),'sub_model_path': television_sub_model_path,
           'sub_sfx_path': 'effect/fx/niudan/quanxi/quanxi_001.sfx',
           'model_transparent': 180.0 / 255.0,
           'rendergroup_and_priority': 10
           })
        entity_obj.on_add_to_battle(global_data.battle.id)
        self._battle_flag_entity_id.append(entity_id)
        if not show:
            self._free_battle_flag_entity_id[born_idx].append(entity_id)

    def add_battle_flag(self, info):
        born_idx, battle_flag = info
        if self._free_battle_flag_entity_id[born_idx]:
            entity_id = self._free_battle_flag_entity_id[born_idx].pop()
            entity_obj = EntityManager.getentity(entity_id)
            if entity_obj and entity_obj.logic:
                entity_obj.logic.send_event('E_UPDATE_TV_INFO', {'is_show': True,'show_info': battle_flag})

    def _remove_entity(self):
        for entity_id in self._battle_flag_entity_id:
            entity_obj = EntityManager.getentity(entity_id)
            if entity_obj:
                entity_obj.on_remove_from_battle()
                entity_obj.destroy()

        self._battle_flag_entity_id = []
        self._free_battle_flag_entity_id = [[], []]

    def destroy(self):
        self._remove_entity()
        self.process_event(False)


class BattleBronBoxMgr():
    COL_MODEL_PATH = confmgr.get('script_gim_ref')['s5_col_model_path']

    def __init__(self):
        self.ready_col = []
        self.ready_col_model = []
        self.del_col_timer = None
        self.process_event(True)
        return

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'battle_change_prepare_timestamp': self.change_prepare_timestamp,
           'update_death_born_point': self.init_bron_box
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def change_prepare_timestamp(self):
        self.init_bron_box()

    def get_left_time(self):
        return BattleUtils.get_prepare_left_time(0)

    def get_player_group_id(self):
        if global_data.player and global_data.player.logic:
            return global_data.player.logic.ev_g_group_id()

    def init_bron_box(self):
        self.clear_timer()
        self.clear_model()
        self.clear_col()
        revive_time = self.get_left_time()
        need_create_model = revive_time > 0
        for group_id, born_data in six.iteritems(global_data.death_battle_data.born_data):
            _x, _y, _z, _r, _idx, _ = born_data.data
            position = math3d.vector(_x, _y, _z)
            is_group = self.get_player_group_id() == group_id

            def create_model_cb(model, range=_r, is_group=is_group):
                scale_x = range / model.bounding_box.x * 1.0
                scale_z = range / model.bounding_box.z * 1.0
                model.world_scale = math3d.vector(scale_x, 1.0, scale_z)
                if is_group:
                    color = (0.0, 0.22, 1.0)
                else:
                    color = (1.0, 0.0, 0.0)
                model.set_rendergroup_and_priority(world.RENDER_GROUP_DECAL, 0)
                model.all_materials.set_var(_HASH_Alpha, 'Alpha', (color[0], color[1], color[2], 1.0))
                model.all_materials.set_var(_HASH_Depth_Outline_Color, 'depth_outline_color', (color[0], color[1], color[2], 0.5))
                model_pos = model.position
                if need_create_model:
                    mask = collision_const.TERRAIN_MASK
                    group = collision_const.REGION_SCENE_GROUP
                    col = collision.col_object(collision.MESH, model, mask, group, 0, True)
                    col.position = model_pos
                    _scn = world.get_active_scene()
                    _scn.scene_col.add_object(col)
                    self.ready_col.append(col)

            col_model_id = global_data.model_mgr.create_model_in_scene(self.COL_MODEL_PATH, position, on_create_func=create_model_cb)
            self.ready_col_model.append(col_model_id)

        if need_create_model:
            self.del_col_timer = global_data.game_mgr.get_logic_timer().register(func=self.clear_col, mode=timer.CLOCK, interval=revive_time + 1, times=1)

    def clear_col_timer(self):
        self.del_col_timer and global_data.game_mgr.get_logic_timer().unregister(self.del_col_timer)
        self.del_col_timer = None
        return

    def clear_model(self):
        for model_id in self.ready_col_model:
            global_data.model_mgr.remove_model_by_id(model_id)

        self.ready_col_model = []

    def clear_col(self):
        _scn = world.get_active_scene()
        for col in self.ready_col:
            _scn.scene_col.remove_object(col)

        self.ready_col = []

    def clear_timer(self):
        self.clear_col_timer()

    def destroy(self):
        self.clear_timer()
        self.clear_model()
        self.clear_col()
        self.process_event(False)


class BattleAccMgr():

    def __init__(self):
        self.is_init = False
        self.acc_tri_dict = {}
        self.no_dir_acc_tri_dict = {}
        self.process_event(True)

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {}
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def init_battle_acc(self):
        battle = global_data.battle
        if not battle:
            return
        if self.is_init:
            return
        battle = global_data.battle
        if not battle:
            return
        from logic.gcommon.common_const.battle_const import BATTLE_SCENE_NORMAL
        scene_name = global_data.battle.get_scene_name()
        if scene_name == BATTLE_SCENE_NORMAL:
            from data.acc_trigger_data import data
            for idx, conf in enumerate(data):
                self.setup_acc_trigger(idx, conf)

            from data.no_dir_acc_trigger_data import data
            for idx, conf in enumerate(data):
                self.setup_no_dir_acc_trigger(idx, conf)

        born_cfg_data = global_data.game_mode.get_born_data()
        acc_index = born_cfg_data[str(battle.area_id)].get('acc_index')
        if not acc_index:
            return
        acc_triggers_data = global_data.game_mode.get_cfg_data('acc_triggers_data')
        for idx in acc_index:
            acc_data = acc_triggers_data.get(str(idx))
            if not acc_data:
                continue
            is_no_dir = acc_data.get('is_no_dir')
            if is_no_dir:
                self.setup_no_dir_acc_trigger(idx + 100, acc_data)
            else:
                self.setup_acc_trigger(idx + 100, acc_data)

        self.is_init = True

    def clear_acc_trigger(self):
        scene = global_data.game_mgr.scene
        if not scene:
            return
        scol = scene.scene_col
        for tri, _ in six.itervalues(self.acc_tri_dict):
            scol.remove_object(tri)

        for tri in six.itervalues(self.no_dir_acc_tri_dict):
            scol.remove_object(tri)

        self.acc_tri_dict = {}
        self.no_dir_acc_tri_dict = {}

    def setup_acc_trigger(self, idx, conf):
        rot = [ float(x) for x in conf['rot'].split(',') ]
        pos = math3d.vector(*[ float(x) for x in conf['pos'].split(',') ])
        bound_center = math3d.vector(*[ float(x) for x in conf['bound_center'].split(',') ])
        bound_half = math3d.vector(*[ float(x) for x in conf['bound_half'].split(',') ])
        scale = math3d.vector(*[ float(x) for x in conf['scale'].split(',') ])
        rot_mat = math3d.matrix()
        rot_mat.set_all(*rot)
        bound_half = bound_half * scale
        trigger = collision.col_object(collision.BOX, bound_half, 0, 0, 0)
        global_data.game_mgr.scene.scene_col.add_object(trigger)
        trigger.set_trigger(True)
        trigger.set_trigger_callback(Functor(self.acc_trigger_callback, idx))
        trigger.position = bound_center + pos
        trigger.rotation_matrix = rot_mat
        forward = rot_mat.forward
        acc_forward = math3d.vector(forward.x, 0, forward.z)
        acc_forward.normalize()
        self.acc_tri_dict[idx] = (trigger, acc_forward)

    def setup_no_dir_acc_trigger(self, idx, conf):
        rot = [ float(x) for x in conf['rot'].split(',') ]
        pos = math3d.vector(*[ float(x) for x in conf['pos'].split(',') ])
        bound_center = math3d.vector(*[ float(x) for x in conf['bound_center'].split(',') ])
        bound_half = math3d.vector(*[ float(x) for x in conf['bound_half'].split(',') ])
        scale = math3d.vector(*[ float(x) for x in conf['scale'].split(',') ])
        rot_mat = math3d.matrix()
        rot_mat.set_all(*rot)
        bound_half = bound_half * scale
        trigger = collision.col_object(collision.BOX, bound_half, 0, 0, 0)
        global_data.game_mgr.scene.scene_col.add_object(trigger)
        trigger.set_trigger(True)
        trigger.set_trigger_callback(Functor(self.no_dir_acc_trigger_callback, idx))
        trigger.position = bound_center + pos
        trigger.rotation_matrix = rot_mat
        self.no_dir_acc_tri_dict[idx] = trigger

    def no_dir_acc_trigger_callback(self, *args):
        idx, col_obj, tri_obj, is_in = args
        if tri_obj:
            user = global_data.emgr.scene_find_lift_user_event.emit(tri_obj.cid)
            if not user:
                return
            if not isinstance(user, list) or not user[0]:
                return
            user = user[0]
            if not (idx >= 0 and idx in self.no_dir_acc_tri_dict):
                return
            user.send_event('E_NO_DIR_ACC_TRIGGER_INFO', is_in, idx)

    def acc_trigger_callback(self, *args):
        idx, col_obj, tri_obj, is_in = args
        if tri_obj:
            user = global_data.emgr.scene_find_lift_user_event.emit(tri_obj.cid)
            if not user:
                return
            if not isinstance(user, list) or not user[0]:
                return
            user = user[0]
            if not (idx >= 0 and idx in self.acc_tri_dict):
                return
            tri_info = self.acc_tri_dict[idx]
            user.send_event('E_ACC_TRIGGER_INFO', is_in, tri_info[1] if is_in else None, idx)
        return

    def destroy(self):
        self.clear_acc_trigger()
        self.process_event(False)
        self.is_init = False


class ControlBattlePrepare(BattlePrepareBase):

    def __init__(self, parent):
        super(ControlBattlePrepare, self).__init__(parent)
        self.init_mgr()

    def init_mgr(self):
        from logic.comsys.battle.Death.DeathBattleDoorCol import DeathBattleDoorCol
        DeathBattleDoorCol()
        self.range_mgr = BattleRangeMgr()
        self.sfx_mgr = BattleSfxMgr()
        self.spawn_mgr = BattleSpawnMgr()
        self.battle_flag_mgr = BattleFlagMgr()

    def on_player_parachute_stage_changed(self, stage):
        if stage in (parachute_utils.STAGE_SORTIE_PREPARE, parachute_utils.STAGE_LAND):
            self.range_mgr and self.range_mgr.create_all_range_model()
            self.sfx_mgr and self.sfx_mgr.init_scene_sfx()
            self.spawn_mgr and self.spawn_mgr.init_spawn()
            self.battle_flag_mgr and self.battle_flag_mgr.init_battle_flag()

    def on_exit(self):
        super(ControlBattlePrepare, self).on_exit()
        global_data.death_battle_door_col.finalize()
        self.range_mgr and self.range_mgr.destroy()
        self.range_mgr = None
        self.sfx_mgr and self.sfx_mgr.destroy()
        self.sfx_mgr = None
        self.spawn_mgr and self.spawn_mgr.destroy()
        self.spawn_mgr = None
        self.battle_flag_mgr and self.battle_flag_mgr.destroy()
        self.battle_flag_mgr = None
        return

    def is_in_battle_boundary(self, px, py, pz, margin=0):
        if self.range_mgr:
            return self.range_mgr.is_in_battle_boundary(px, py, pz, margin)
        return False


class KothBattlePrepare(BattlePrepareBase):

    def __init__(self, parent):
        super(KothBattlePrepare, self).__init__(parent)
        self._col_obj = []

    def on_player_parachute_stage_changed(self, stage):
        if not global_data.cam_lplayer:
            return
        self.remove_col()
        if stage == parachute_utils.STAGE_SORTIE_PREPARE:
            self.create_col()

    def create_col(self):
        self.remove_col()
        cfg = global_data.game_mode.get_cfg_data('play_data')
        my_camp_id = global_data.king_battle_data.my_camp_id
        center = cfg.get('camp0%d_base_center' % my_camp_id)
        length = cfg.get('camp0%d_base_length' % my_camp_id)
        width = cfg.get('camp0%d_base_width' % my_camp_id)
        self._col_obj = scene_utils.add_region_scene_collision(center, length, width)

    def remove_col(self):
        if not self._col_obj:
            return
        _scn = world.get_active_scene()
        for col in self._col_obj:
            if col and col.valid:
                _scn.scene_col.remove_object(col)

        self._col_obj = []

    def on_exit(self):
        super(KothBattlePrepare, self).on_exit()
        self.remove_col()


class DeathBattlePrepare(BattlePrepareBase):

    def __init__(self, parent):
        super(DeathBattlePrepare, self).__init__(parent)
        self.init_mgr()

    def init_mgr(self):
        from logic.comsys.battle.Death.DeathBattleDoorCol import DeathBattleDoorCol
        DeathBattleDoorCol()
        self.range_mgr = BattleRangeMgr()
        self.sfx_mgr = BattleSfxMgr()
        self.spawn_mgr = BattleSpawnMgr()
        self.battle_flag_mgr = BattleFlagMgr()
        self.acc_mgr = BattleAccMgr()

    def on_player_parachute_stage_changed(self, stage):
        if stage in (parachute_utils.STAGE_SORTIE_PREPARE, parachute_utils.STAGE_LAND):
            self.range_mgr and self.range_mgr.create_all_range_model()
            self.sfx_mgr and self.sfx_mgr.init_scene_sfx()
            self.spawn_mgr and self.spawn_mgr.init_spawn()
            self.battle_flag_mgr and self.battle_flag_mgr.init_battle_flag()
            self.acc_mgr and self.acc_mgr.init_battle_acc()

    def on_exit(self):
        super(DeathBattlePrepare, self).on_exit()
        global_data.death_battle_door_col and global_data.death_battle_door_col.finalize()
        self.range_mgr and self.range_mgr.destroy()
        self.range_mgr = None
        self.sfx_mgr and self.sfx_mgr.destroy()
        self.sfx_mgr = None
        self.spawn_mgr and self.spawn_mgr.destroy()
        self.spawn_mgr = None
        self.battle_flag_mgr and self.battle_flag_mgr.destroy()
        self.battle_flag_mgr = None
        self.acc_mgr and self.acc_mgr.destroy()
        self.acc_mgr = None
        return

    def is_in_battle_boundary(self, px, py, pz, margin=0):
        if self.range_mgr:
            return self.range_mgr.is_in_battle_boundary(px, py, pz, margin)
        return False


class BattleDuelRangeMgr(object):

    def __init__(self):
        self._move_range_model_id = None
        self._model = None
        self._region_col_models = []
        self._update_range_related_data()
        self._register_events()
        return

    def _register_events(self):
        global_data.emgr.camera_lctarget_open_prez += self.on_open_prez

    def _unregister_events(self):
        global_data.emgr.camera_lctarget_open_prez -= self.on_open_prez

    def is_in_battle_boundary(self, px, py, pz, margin=0):
        move_range = self._range_data[0] if self._range_data else None
        if move_range is None:
            return False
        else:
            min_x = min(move_range[0][0], move_range[1][0])
            max_x = max(move_range[0][0], move_range[1][0])
            min_z = min(move_range[0][1], move_range[1][1])
            max_z = max(move_range[0][1], move_range[1][1])
            if px < min_x + margin or px > max_x - margin:
                return False
            if pz < min_z + margin or pz > max_z - margin:
                return False
            return True

    def _update_range_related_data(self):
        battle = global_data.battle
        if not battle:
            self._range_data = None
            return
        else:
            born_data = global_data.game_mode.get_cfg_data('born_data')
            move_range = born_data[str(battle.area_id)].get('move_range')
            move_height = born_data[str(battle.area_id)].get('move_height', 0.0)
            limit_height = born_data[str(battle.area_id)].get('limit_height')
            range_rot = born_data[str(battle.area_id)].get('range_rot')
            self._range_data = (
             move_range, move_height, limit_height, range_rot)
            return

    def recreate_all_range_model(self):
        self.destroy_all_range_model()
        self.create_all_range_model()

    def create_all_range_model(self):
        battle = global_data.battle
        if not battle:
            return
        else:
            if self._move_range_model_id:
                return
            move_range = self._range_data[0] if self._range_data else None
            move_height = self._range_data[1] if self._range_data else 0.0
            limit_height = self._range_data[2] if self._range_data else None
            range_rot = self._range_data[3] if self._range_data else None
            barrier_model_path = confmgr.get('script_gim_ref')['region_range_blue']
            self._region_col_models = self.create_range_model(barrier_model_path, move_range, move_height, limit_height, range_rot, need_col=True)
            return

    def create_range_model(self, path, range_data, move_height, limit_height, range_rot, need_col=False):
        if not range_data:
            return []
        else:
            range1_x, range1_z = range_data[0]
            range2_x, range2_z = range_data[1]
            center_x = (range1_x + range2_x) * 0.5
            center_z = (range1_z + range2_z) * 0.5
            length = abs(range1_x - range2_x)
            width = abs(range1_z - range2_z)
            center = math3d.vector(center_x, move_height, center_z)
            rot_mat = None
            if range_rot:
                dx, dy, dz = range_rot
                rot_mat = math3d.euler_to_matrix(math3d.vector(math.pi * dx / 180, math.pi * dy / 180, math.pi * dz / 180))
                revert_rot_mat = math3d.euler_to_matrix(math3d.vector(math.pi * (180 - dx) / 180, math.pi * (180 - dy) / 180, math.pi * (180 - dz) / 180))
                new_range1 = center + math3d.vector(range_data[0][0] - center_x, move_height, range_data[0][1] - center_z) * revert_rot_mat
                new_range2 = center + math3d.vector(range_data[1][0] - center_x, move_height, range_data[1][1] - center_z) * revert_rot_mat
                length = abs(new_range1.x - new_range2.x)
                width = abs(new_range1.z - new_range2.z)

            def on_range_model(model, length=length, width=width, rot_mat=rot_mat):
                scale_x = length / (model.bounding_box.x * 2)
                scale_z = width / (model.bounding_box.z * 2)
                model.world_scale = math3d.vector(scale_x, 4.0, scale_z)
                model.set_rendergroup_and_priority(world.RENDER_GROUP_DECAL, 0)
                if rot_mat:
                    model.rotation_matrix = rot_mat
                self._model = model

            self._move_range_model_id = global_data.model_mgr.create_model_in_scene(path, center, on_create_func=on_range_model)
            col_models = []
            if need_col:
                center, length, width, height = (
                 (
                  center_x, move_height, center_z), length * 0.5, width * 0.5, limit_height or 2000)
                col_models = scene_utils.add_region_scene_collision(center, length, width, height, rot_mat)
            return col_models

    def destroy_range_sfx(self):
        if self._move_range_model_id:
            global_data.model_mgr.remove_model_by_id(self._move_range_model_id)
        self._move_range_model_id = None
        self._model = None
        return

    def remove_col(self):
        _scn = world.get_active_scene()
        for col_model in self._region_col_models:
            if col_model and col_model.valid:
                _scn.scene_col.remove_object(col_model)

        self._region_col_models = []

    def on_open_prez(self, enable):
        if self._model:
            if enable:
                self._model.all_materials.set_macro('DEPTH_OUTLINE', 'FALSE')
            else:
                self._model.all_materials.set_macro('DEPTH_OUTLINE', 'TRUE')
            self._model.all_materials.rebuild_tech()

    def destroy_all_range_model(self):
        self.destroy_range_sfx()
        self.remove_col()

    def destroy(self):
        self.destroy_all_range_model()
        self._unregister_events()


class ExerciseBattlePrepare(BattlePrepareBase):

    def __init__(self, parent):
        super(ExerciseBattlePrepare, self).__init__(parent)
        range_conf = confmgr.get('game_mode/exercise/c_map_exercise_conf')['Barrier']['Content']['main']
        self.min_x = range_conf['barrier_range_lb'][0]
        self.min_z = range_conf['barrier_range_lb'][2]
        self.max_x = range_conf['barrier_range_rt'][0]
        self.max_z = range_conf['barrier_range_rt'][2]
        self.init_mgr()

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'update_battle_stage': self.on_update_battle_stage,
           'on_player_parachute_stage_changed': self.on_player_parachute_stage_changed,
           'on_player_inited_event': self.on_player_inited_event
           }
        econf.update(self.get_event_conf())
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def on_player_inited_event(self, lplayer):
        bat = global_data.battle
        if bat:
            king, defier, _, _ = bat.get_battle_data()
            if king == lplayer.id:
                bat.refresh_mvp_tv()
            if lplayer.id in (king, defier) and global_data.cam_lplayer and global_data.cam_lplayer.id in (king, defier):
                bat.refresh_outline()

    def on_update_battle_stage(self):
        pass

    def init_mgr(self):
        self.duel_range_mgr = BattleDuelRangeMgr()
        self.duel_sfx_mgr = BattleSfxMgr()

    def on_player_parachute_stage_changed(self, stage):
        if stage in (parachute_utils.STAGE_SORTIE_PREPARE, parachute_utils.STAGE_LAND):
            self.duel_range_mgr and self.duel_range_mgr.create_all_range_model()
            self.duel_sfx_mgr and self.duel_sfx_mgr.init_scene_sfx()
            self.on_update_battle_stage()

    def is_in_battle_boundary(self, px, py, pz, margin=0):
        if px < self.min_x + margin or px > self.max_x - margin:
            return False
        if pz < self.min_z + margin or pz > self.max_z - margin:
            return False
        return True

    def on_exit(self):
        super(ExerciseBattlePrepare, self).on_exit()
        self.duel_range_mgr and self.duel_range_mgr.destroy()
        self.duel_range_mgr = None
        self.duel_sfx_mgr and self.duel_sfx_mgr.destroy()
        self.duel_sfx_mgr = None
        return


class FFABattlePrepare(BattlePrepareBase):

    def __init__(self, parent):
        super(FFABattlePrepare, self).__init__(parent)
        self.init_mgr()

    def init_mgr(self):
        self.range_mgr = BattleRangeMgr()
        self.spawn_mgr = BattleSpawnMgr()
        self.ready_box_mgr = BattleReadyBoxMgr()

    def on_player_parachute_stage_changed(self, stage):
        if stage in (parachute_utils.STAGE_SORTIE_PREPARE, parachute_utils.STAGE_LAND):
            self.range_mgr and self.range_mgr.create_all_range_model()
            self.spawn_mgr and self.spawn_mgr.init_spawn()
            self.ready_box_mgr and self.ready_box_mgr.init_ready_box()

    def on_exit(self):
        super(FFABattlePrepare, self).on_exit()
        self.range_mgr and self.range_mgr.destroy()
        self.range_mgr = None
        self.spawn_mgr and self.spawn_mgr.destroy()
        self.spawn_mgr = None
        self.ready_box_mgr and self.ready_box_mgr.destroy()
        self.ready_box_mgr = None
        return


class GVGBattlePrepare(BattlePrepareBase):

    def __init__(self, parent):
        super(GVGBattlePrepare, self).__init__(parent)
        self.init_mgr()

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'on_player_parachute_stage_changed': self.on_player_parachute_stage_changed,
           'duel_round_interval_event': self.on_round_play_interval
           }
        econf.update(self.get_event_conf())
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def on_round_play_interval(self):
        self.ready_box_mgr and self.ready_box_mgr.init_ready_box()

    def init_mgr(self):
        self.range_mgr = BattleRangeMgr()
        self.ready_box_mgr = BattleReadyBoxMgr()

    def on_player_parachute_stage_changed(self, stage):
        if stage in (parachute_utils.STAGE_SORTIE_PREPARE, parachute_utils.STAGE_LAND):
            self.range_mgr and self.range_mgr.create_all_range_model()
            self.ready_box_mgr and self.ready_box_mgr.init_ready_box()

    def on_exit(self):
        super(GVGBattlePrepare, self).on_exit()
        self.range_mgr and self.range_mgr.destroy()
        self.range_mgr = None
        self.ready_box_mgr and self.ready_box_mgr.destroy()
        self.ready_box_mgr = None
        return


class ImproviseBattleRangeMgr(BattleRangeMgr):

    def _register_events(self):
        super(ImproviseBattleRangeMgr, self)._register_events()
        global_data.emgr.battle_new_round += self._on_battle_new_round
        global_data.emgr.improvise_battle_data_initted += self._on_improvise_battle_data_initted

    def _unregister_events(self):
        global_data.emgr.battle_new_round -= self._on_battle_new_round
        global_data.emgr.improvise_battle_data_initted -= self._on_improvise_battle_data_initted
        super(ImproviseBattleRangeMgr, self)._unregister_events()

    def _update_range_related_data(self):
        self._range_data = None
        battle = global_data.battle
        if not battle:
            return
        else:
            if not global_data.improvise_battle_data:
                return
            born_data = global_data.game_mode.get_born_data()
            from logic.gcommon.common_const.battle_const import ROUND_TYPE_MECHA
            range_index = born_data[str(battle.area_id)].get('range_index')
            if global_data.improvise_battle_data.get_round_type() == ROUND_TYPE_MECHA:
                move_range = born_data[str(battle.area_id)].get('move_range_mecha')
                move_height = born_data[str(battle.area_id)].get('move_height_mecha', 0.0)
                limit_height = born_data[str(battle.area_id)].get('limit_height_mecha')
            else:
                move_range = born_data[str(battle.area_id)].get('move_range')
                move_height = born_data[str(battle.area_id)].get('move_height', 0.0)
                limit_height = born_data[str(battle.area_id)].get('limit_height')
            self._range_data = (move_range, move_height, limit_height, range_index)
            return

    def _on_battle_new_round(self, prev, now, mode):
        if mode != game_mode_const.GAME_MODE_IMPROVISE:
            return
        self._update_range_related_data()
        self.recreate_all_range_model()

    def _on_improvise_battle_data_initted(self):
        self._update_range_related_data()
        self.recreate_all_range_model()


class ImproviseBattlePrepare(BattlePrepareBase):

    def __init__(self, parent):
        super(ImproviseBattlePrepare, self).__init__(parent)
        self.init_mgr()

    def init_mgr(self):
        self.range_mgr = ImproviseBattleRangeMgr()

    def on_player_parachute_stage_changed(self, stage):
        if stage in (parachute_utils.STAGE_SORTIE_PREPARE, parachute_utils.STAGE_LAND):
            self.range_mgr and self.range_mgr.create_all_range_model()

    def on_exit(self):
        self.range_mgr and self.range_mgr.destroy()
        self.range_mgr = None
        super(ImproviseBattlePrepare, self).on_exit()
        return

    def is_in_battle_boundary(self, px, py, pz, margin=0):
        if self.range_mgr:
            return self.range_mgr.is_in_battle_boundary(px, py, pz, margin)
        return False


class HumanDeathBattlePrepare(BattlePrepareBase):

    def __init__(self, parent):
        super(HumanDeathBattlePrepare, self).__init__(parent)
        self.init_mgr()

    def init_mgr(self):
        self.range_mgr = BattleRangeMgr()
        self.acc_mgr = BattleAccMgr()

    def on_player_parachute_stage_changed(self, stage):
        if stage in (parachute_utils.STAGE_SORTIE_PREPARE, parachute_utils.STAGE_LAND):
            self.range_mgr and self.range_mgr.create_all_range_model()
            self.acc_mgr and self.acc_mgr.init_battle_acc()

    def on_exit(self):
        super(HumanDeathBattlePrepare, self).on_exit()
        self.range_mgr and self.range_mgr.destroy()
        self.range_mgr = None
        self.acc_mgr and self.acc_mgr.destroy()
        self.acc_mgr = None
        return

    def is_in_battle_boundary(self, px, py, pz, margin=0):
        if self.range_mgr:
            return self.range_mgr.is_in_battle_boundary(px, py, pz, margin)
        return False


class ArmRaceBattlePrepare(BattlePrepareBase):

    def __init__(self, parent):
        super(ArmRaceBattlePrepare, self).__init__(parent)
        self.init_mgr()

    def init_mgr(self):
        self.range_mgr = BattleRangeMgr()
        self.spawn_mgr = BattleSpawnMgr()

    def on_player_parachute_stage_changed(self, stage):
        if stage in (parachute_utils.STAGE_SORTIE_PREPARE, parachute_utils.STAGE_LAND):
            self.range_mgr and self.range_mgr.create_all_range_model()
            self.spawn_mgr and self.spawn_mgr.init_spawn()

    def on_exit(self):
        super(ArmRaceBattlePrepare, self).on_exit()
        self.range_mgr and self.range_mgr.destroy()
        self.range_mgr = None
        self.spawn_mgr and self.spawn_mgr.destroy()
        self.spawn_mgr = None
        return


class ConcertBattlePrepare(BattlePrepareBase):

    def __init__(self, parent):
        super(ConcertBattlePrepare, self).__init__(parent)
        self.init_mgr()
        self.on_update_battle_stage()

    def on_enter(self):
        pass

    def init_mgr(self):
        self.sfx_mgr = BattleSfxMgr()

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'update_battle_stage': self.on_update_battle_stage,
           'on_player_parachute_stage_changed': self.on_player_parachute_stage_changed,
           'on_player_inited_event': self.on_player_inited_event
           }
        econf.update(self.get_event_conf())
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def on_player_parachute_stage_changed(self, stage):
        if stage in (parachute_utils.STAGE_SORTIE_PREPARE, parachute_utils.STAGE_LAND):
            self.on_update_battle_stage()

    def on_player_inited_event(self, lplayer):
        bat = global_data.battle
        if bat:
            king, defier, _, _ = bat.get_battle_data()
            if king == lplayer.id:
                bat.refresh_mvp_tv()
            if lplayer.id in (king, defier) and global_data.cam_lplayer and global_data.cam_lplayer.id in (king, defier):
                bat.refresh_outline()

    def on_update_battle_stage(self):
        bat = global_data.battle
        if not bat:
            return
        is_duel_stage = bat.is_duel_stage()
        if is_duel_stage:
            self.sfx_mgr and self.sfx_mgr.init_scene_sfx()
        else:
            self.sfx_mgr and self.sfx_mgr.destroy_scene_sfx_and_model()

    def on_exit(self):
        super(ConcertBattlePrepare, self).on_exit()
        self.sfx_mgr and self.sfx_mgr.destroy()
        self.sfx_mgr = None
        return

    def is_in_battle_boundary(self, px, py, pz, margin=0):
        return False


class ADCrystalBattleSpawnMgr(BattleSpawnMgr):

    def init_spawn(self):
        battle = global_data.battle
        if not battle:
            return
        self._spawn_info = {}
        born_data = global_data.game_mode.get_born_data()
        born_spawn_data = global_data.game_mode.get_cfg_data('born_spawn_data')
        spawn_lst = born_data[str(battle.area_id)].get('spawn_lst', [])
        for spawn_child_lst in spawn_lst:
            for spawn_id in spawn_child_lst:
                if str(spawn_id) in born_spawn_data:
                    self._spawn_info[spawn_id] = born_spawn_data[str(spawn_id)]

        self.refresh_sfx()
        self.create_item_model()
        self.clear_spawn_cd_check_timer()
        self._spawn_cd_check_timer = global_data.game_mgr.get_logic_timer().register(func=self.update_spawn_cd_show, mode=timer.LOGIC, interval=3, times=-1)


class ADCrystalBattlePrepare(BattlePrepareBase):

    def __init__(self, parent):
        super(ADCrystalBattlePrepare, self).__init__(parent)
        self.init_mgr()

    def init_mgr(self):
        from logic.comsys.battle.Death.DeathBattleDoorCol import DeathBattleDoorCol
        DeathBattleDoorCol()
        self.range_mgr = BattleRangeMgr()
        self.sfx_mgr = BattleSfxMgr()
        self.spawn_mgr = ADCrystalBattleSpawnMgr()
        self.battle_flag_mgr = BattleFlagMgr()
        self.acc_mgr = BattleAccMgr()

    def on_player_parachute_stage_changed(self, stage):
        if stage in (parachute_utils.STAGE_SORTIE_PREPARE, parachute_utils.STAGE_LAND):
            self.range_mgr and self.range_mgr.create_all_range_model()
            self.sfx_mgr and self.sfx_mgr.init_scene_sfx()
            self.spawn_mgr and self.spawn_mgr.init_spawn()
            self.battle_flag_mgr and self.battle_flag_mgr.init_battle_flag()
            self.acc_mgr and self.acc_mgr.init_battle_acc()

    def on_exit(self):
        super(ADCrystalBattlePrepare, self).on_exit()
        global_data.death_battle_door_col and global_data.death_battle_door_col.finalize()
        self.range_mgr and self.range_mgr.destroy()
        self.range_mgr = None
        self.sfx_mgr and self.sfx_mgr.destroy()
        self.sfx_mgr = None
        self.spawn_mgr and self.spawn_mgr.destroy()
        self.spawn_mgr = None
        self.battle_flag_mgr and self.battle_flag_mgr.destroy()
        self.battle_flag_mgr = None
        self.acc_mgr and self.acc_mgr.destroy()
        self.acc_mgr = None
        return

    def is_in_battle_boundary(self, px, py, pz, margin=0):
        if self.range_mgr:
            return self.range_mgr.is_in_battle_boundary(px, py, pz, margin)
        return False


class SnatchEggBattlePrepare(BattlePrepareBase):

    def __init__(self, parent):
        super(SnatchEggBattlePrepare, self).__init__(parent)
        self.init_mgr()

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'on_player_parachute_stage_changed': self.on_player_parachute_stage_changed,
           'snatchegg_round_interval_event': self.on_round_play_interval
           }
        econf.update(self.get_event_conf())
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def init_mgr(self):
        self.range_mgr = BattleRangeMgr()
        self.sfx_mgr = BattleSfxMgr()
        self.spawn_mgr = BattleSpawnMgr()
        self.ready_box_mgr = BattleReadyBoxMgr()

    def on_player_parachute_stage_changed(self, stage):
        if stage in (parachute_utils.STAGE_SORTIE_PREPARE, parachute_utils.STAGE_LAND):
            self.range_mgr and self.range_mgr.create_all_range_model()
            self.sfx_mgr and self.sfx_mgr.init_scene_sfx()
            self.spawn_mgr and self.spawn_mgr.init_spawn()
            self.ready_box_mgr and self.ready_box_mgr.init_ready_box()

    def on_round_play_interval(self):
        self.ready_box_mgr and self.ready_box_mgr.init_ready_box()

    def on_exit(self):
        super(SnatchEggBattlePrepare, self).on_exit()
        self.range_mgr and self.range_mgr.destroy()
        self.range_mgr = None
        self.sfx_mgr and self.sfx_mgr.destroy()
        self.sfx_mgr = None
        self.spawn_mgr and self.spawn_mgr.destroy()
        self.spawn_mgr = None
        self.ready_box_mgr and self.ready_box_mgr.destroy()
        self.ready_box_mgr = None
        return

    def is_in_battle_boundary(self, px, py, pz, margin=0):
        if self.range_mgr:
            return self.range_mgr.is_in_battle_boundary(px, py, pz, margin)
        return True


class GooseBearBattlePrepare(BattlePrepareBase):

    def __init__(self, parent):
        super(GooseBearBattlePrepare, self).__init__(parent)
        self.init_mgr()

    def init_mgr(self):
        self.ready_box_mgr = BattleReadyBoxMgr()

    def on_player_parachute_stage_changed(self, stage):
        if stage in (parachute_utils.STAGE_SORTIE_PREPARE, parachute_utils.STAGE_LAND):
            self.ready_box_mgr and self.ready_box_mgr.init_ready_box()

    def on_exit(self):
        super(GooseBearBattlePrepare, self).on_exit()
        self.ready_box_mgr and self.ready_box_mgr.destroy()
        self.ready_box_mgr = None
        return


class AssaultBattlePrepare(DeathBattlePrepare):

    def init_mgr(self):
        from logic.comsys.battle.Death.DeathBattleDoorCol import DeathBattleDoorCol
        DeathBattleDoorCol()
        self.range_mgr = BattleRangeMgr()
        self.sfx_mgr = BattleSfxMgr()
        self.spawn_mgr = BattleSpawnMgr()
        self.acc_mgr = BattleAccMgr()
        self.battle_flag_mgr = None
        return