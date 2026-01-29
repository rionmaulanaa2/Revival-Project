# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComHpBreakable.py
from __future__ import absolute_import
from __future__ import print_function
import time
from ..UnitCom import UnitCom
import math3d
import C_file
import collision
import render
import game3d
import weakref
import world
from logic.gutils.scene_utils import is_break_obj, get_break_info_by_full_name, get_model_check_name, enable_dynamic_physics
from logic.gcommon.common_const import collision_const
from logic.gcommon.common_const import battle_const
from data.constant_break_data import data as constant_break_list
from logic.gcommon.const import NEOX_UNIT_SCALE
from logic.gcommon.common_const.collision_const import TERRAIN_GROUP, TERRAIN_MASK
from common.utils.sfxmgr import CREATE_SRC_SIMPLE
from common.cfg import confmgr
_HASH_TexLightmap = game3d.calc_string_hash('tex_lightmap')
_HASH_FrameTimeBreak = game3d.calc_string_hash('FrameTimeBreak')
_HASH_FrameTimeShine = game3d.calc_string_hash('FrameTimeShine')

class ComHpBreakable(UnitCom):
    SHAKE_RANGE = 5 * NEOX_UNIT_SCALE
    SFX_SCALE_FACTOR = 0.8

    def __init__(self):
        super(ComHpBreakable, self).__init__()
        self.break_id = None
        self.is_damaged = False
        self.is_touched = False
        self.break_model_task = None
        self.broken_model_task = None
        self.break_model = None
        self.broken_model = None
        self.custom_col_group = None
        self.hp = 0
        self.break_info = None
        self.hit_sfx = None
        self.hit_sfx_last_time = 0
        self.break_sfxes = None
        self.broken_sfxes = None
        self.break_type = None
        self.hp_max = 0
        self.hp_damaged = 0
        self.is_emissive = False
        self.has_break_res = False
        self.ex_model_task_done = 0
        return

    def init_from_dict(self, unit_obj, bdict):
        super(ComHpBreakable, self).init_from_dict(unit_obj, bdict)
        EVENT_LIST = {'E_INIT_HP_MODEL': '_init_hp_model',
           'G_BREAK_ID': '_get_break_id',
           'G_HP_MODEL': '_get_hp_model',
           'G_HP': '_get_hp',
           'E_HEALTH_HP_CHANGE': '_on_hp_change',
           'G_COLLISION_INFO': '_get_collision_info',
           'G_CHECK_SHOOT_INFO': '_check_shoot_info',
           'E_RECORD_HP_BREAK_HIT_ITEM': '_record_lst_hit_item'
           }
        self._bind_event(EVENT_LIST)
        self.break_id = bdict.get('break_id', None)
        self.break_info = get_break_info_by_full_name(self.break_id)
        self.break_type = self.break_info.get('iBreakType', 0)
        self.hit_sfx = self.break_info.get('cResFx', None)
        self.break_sfxes = self.break_info.get('cBreakFx', None)
        self.broken_sfxes = self.break_info.get('cBrokenFx', None)
        self.hp = bdict.get('hp', 0)
        self._lst_hit_item = 0
        hp_range = self.break_info.get('arrBreakBlood', (0, 0))
        if len(hp_range) >= 2:
            self.hp_max, self.hp_damaged = hp_range
        self.is_emissive = self.break_info.get('iHaveLumines', None)
        self.has_break_res = self.break_info.get('iBreakRes', None)
        self.scene.add_breakable_hp_obj_unit_obj(self.break_id, weakref.ref(self.unit_obj))
        self.orig_pos = None
        trans_info = bdict.get('trans_info', None)
        if trans_info:
            self.orig_pos = math3d.vector(*trans_info[12:15])
        return

    def _get_break_id(self):
        return self.break_id

    def _get_hp_model(self):
        return self._get_scn_model(self.break_id)

    def _get_hp(self):
        return self.hp

    def _get_cur_model(self):
        if not self.has_break_res:
            return self._get_hp_model()
        if self.hp > self.hp_damaged:
            return self._get_hp_model()
        return self.broken_model

    def _auto_scale_model(self, old_model, new_model):
        if not (old_model and new_model):
            return
        ratio = old_model.bounding_radius_w / new_model.bounding_radius_w
        scale = math3d.vector(ratio, ratio, ratio)
        if scale.x < 0 or scale.y < 0 or scale.z < 0:
            log_error('Scale of breakable model should not be negative, please check model:', old_model)
            scale = math3d.vector(abs(scale.x), abs(scale.y), abs(scale.z))
        new_model.scale = scale

    def _init_hp_model(self, trans_info):
        if not self.break_id:
            return
        else:
            model = self._get_hp_model()
            if model:
                if trans_info:
                    idx = 12
                    pos = math3d.vector(*trans_info[idx:idx + 3])
                else:
                    pos = math3d.vector(0, 0, 0)
                self.custom_col_group = model.get_col_group()
            scn = world.get_active_scene()
            if scn:
                mat = math3d.matrix()
                mat.set_all(trans_info)
                if self.has_break_res:
                    if self.hp > 0 and self.break_type in (collision_const.BREAK_OBJ_TYPE_HP_STATIC,):
                        break_model_pre = collision_const.BREAK_MODEL_PREFIX
                        if global_data.battle and global_data.battle.get_scene_name() == battle_const.BATTLE_SCENE_KONGDAO:
                            break_model_pre = collision_const.KONGDAO_BREAK_MODEL_PREFIX
                        break_model_path = collision_const.BREAK_MODEL_PATTERN % (break_model_pre, self.break_info.get('name', ''))
                        mpos = math3d.vector(*trans_info[12:15])
                        if self.break_model_task:
                            self.break_model_task.cancel()
                            self.break_model_task = None
                        self.break_model_task = world.create_model_async(break_model_path, self._on_create_model, (mpos, False, 1))
                    else:
                        self.ex_model_task_done += 1
                    broken_model_path = collision_const.BROKEN_MODEL_PATTERN % (collision_const.BROKEN_MODEL_PREFIX, self.break_info.get('name', ''))
                    if self.broken_model_task:
                        self.broken_model_task.cancel()
                        self.broken_model_task = None
                    self.broken_model_task = world.create_model_async(broken_model_path, self._on_create_model, (self.orig_pos, True, 2))
            return

    def _on_create_model(self, model, uinfo, current_task):
        self.ex_model_task_done += 1
        scn = world.get_active_scene()
        if not (scn and scn.valid):
            return
        else:
            if not (model and model.valid):
                print('ComHpModel No model existed....failed.')
                return
            scn.add_object(model)
            mpos, hit_ground, model_type = uinfo
            if model_type == 1:
                self.break_model = model
                if not (global_data.game_mode and global_data.game_mode.is_pve()):
                    self.break_model.all_materials.set_macro('LIGHT_MAP_ENABLE', 'FALSE')
                else:
                    self.break_model.all_materials.set_macro('LIGHT_MAP_ENABLE', 'TRUE')
                self.break_model.all_materials.rebuild_tech()
            elif model_type == 2:
                self.broken_model = model
                self.broken_model.all_materials.set_macro('LIGHT_MAP_ENABLE', 'FALSE')
                self.broken_model.all_materials.rebuild_tech()
            model.visible = False
            model.world_position = mpos
            check_name = get_model_check_name(self.break_id)
            model.set_attr('orig_break_id', check_name)
            if hit_ground:
                ground_pos = self.get_ground_pos_y(model.world_position)
                model.world_position = ground_pos
            if self.break_type == collision_const.BREAK_OBJ_TYPE_HP_STATIC:
                model.all_materials.set_macro('VERTEX_ANIMATION', 'FALSE')
                model.all_materials.rebuild_tech()
            if self.ex_model_task_done == 2:
                self._on_hp_change(self.hp, None, True)
            return

    def _get_scn_model(self, break_id):
        scn = world.get_active_scene()
        if not scn:
            return None
        else:
            model = scn.get_model(break_id)
            return model

    def _get_collision_info(self):
        custom_box = self.break_info.get('cSize', None)
        model = self._get_hp_model()
        if model:
            return {'need_update': True,
               'scale': 1.01,
               'non_explosion_dis': False,
               'custom_box': custom_box
               }
        else:
            return {}
            return

    def _check_shoot_info(self, begin, pdir, hit_pos=None):
        return 0

    def _on_hp_change(self, hp, mod, is_init=False):
        self.hp = hp
        if self.hp < self.hp_max:
            if not self.is_touched:
                self.is_touched = True
                if self.is_emissive:
                    m = self._get_cur_model()
                    self.enable_dynamic_emissive(m, True)
            if self.has_break_res and not is_init:
                if self.break_type == collision_const.BREAK_OBJ_TYPE_HP_STATIC and not self.is_damaged:
                    now = time.time()
                    if now - self.hit_sfx_last_time > 1.0:
                        self.hit_sfx_last_time = now
                        cur_model = self._get_cur_model()
                        if cur_model and cur_model.valid and self.hit_sfx:
                            global_data.sfx_mgr.create_sfx_in_scene(self.hit_sfx, cur_model.world_position, on_create_func=self.sfx_create_cb, int_check_type=CREATE_SRC_SIMPLE)
        if hp <= self.hp_damaged and not self.is_damaged:
            self.on_hp_damaged(hp, is_init)
            self.is_damaged = True
        if hp <= 0:
            self.on_hp_destroyed(hp, is_init)

    def on_hp_destroyed(self, hp, is_init=False):
        if not self.has_break_res:
            return
        if self.broken_model and self.broken_model.valid:
            if self.break_type == collision_const.BREAK_OBJ_TYPE_HP_STATIC:
                self.show_static_model(self.broken_model)
            else:
                if not is_init and self.broken_sfxes:
                    pos = self.broken_model.world_position
                    for broken_sfx in self.broken_sfxes:
                        if 'shake' in broken_sfx:
                            if global_data.player:
                                player_pos = global_data.player.logic.ev_g_position()
                                if player_pos:
                                    pos = player_pos
                        global_data.sfx_mgr.create_sfx_in_scene(broken_sfx, pos, on_create_func=self.sfx_create_cb, int_check_type=CREATE_SRC_SIMPLE)

                self.broken_model.visible = False
                self.broken_model.active_collision = False
                self.broken_model.cast_shadow = False
                self.broken_model.destroy()
        old_model = self._get_hp_model()
        if old_model:
            old_model.destroy()
        else:
            scn = world.get_active_scene()
            if scn:
                scn.hide_async_model(self.break_id)

    def get_ground_pos_y(self, pos, offset=0):
        scn = world.get_active_scene()
        start = math3d.vector(pos.x, pos.y + 3 * NEOX_UNIT_SCALE, pos.z)
        end = math3d.vector(pos.x, pos.y - 15 * NEOX_UNIT_SCALE, pos.z)
        result = scn.scene_col.hit_by_ray(start, end, 0, TERRAIN_GROUP, TERRAIN_MASK, collision.EQUAL_FILTER, False)
        if result[0]:
            hit_pos = result[1]
            cobj = result[5]
            height = hit_pos.y + offset
            return math3d.vector(pos.x, height, pos.z)
        return pos

    def sfx_create_cb(self, sfx):
        sfx.scale = math3d.vector(self.SFX_SCALE_FACTOR, self.SFX_SCALE_FACTOR, self.SFX_SCALE_FACTOR)

    def on_hp_damaged(self, hp, is_init=False):
        if not self.has_break_res:
            return
        if self.broken_model and self.broken_model.valid:
            if self.orig_pos:
                ground_pos = self.get_ground_pos_y(self.orig_pos)
                self.broken_model.world_position = ground_pos
                self.show_static_model(self.broken_model)
        if is_init:
            old_model = self._get_hp_model()
            if self.break_type != collision_const.BREAK_OBJ_TYPE_HP_STATIC:
                if self.broken_model and self.broken_model.valid:
                    self.show_static_model(self.broken_model)
                    if old_model:
                        self.broken_model.world_transformation = old_model.world_transformation
                    col_id = self.broken_model.get_col_id()
                    if self.scene:
                        self.scene.add_breakable_hp_obj_cid(self.break_id, col_id)
            if old_model:
                old_model.visible = False
                old_model.destroy()
            else:
                scn = world.get_active_scene()
                if scn:
                    scn.hide_async_model(self.break_id)
        else:
            old_model = self._get_hp_model()
            if old_model:
                if self.broken_model and self.broken_model.valid:
                    self.broken_model.world_transformation = old_model.world_transformation
                old_model.visible = False
            if self.broken_model and self.broken_model.valid:
                self.broken_model.visible = True
                self.broken_model.cast_shadow = True
                if self.break_sfxes:
                    for break_sfx in self.break_sfxes:
                        pos = self.broken_model.world_position
                        if 'shake' in break_sfx:
                            player_pos = global_data.player.logic.ev_g_position()
                            if player_pos:
                                pos = player_pos
                            mpos = self.broken_model.world_position
                            if (math3d.vector(pos.x, 0, pos.z) - math3d.vector(mpos.x, 0, mpos.z)).length < self.SHAKE_RANGE:
                                global_data.sfx_mgr.create_sfx_in_scene(break_sfx, pos, on_create_func=self.sfx_create_cb, int_check_type=CREATE_SRC_SIMPLE)
                        else:
                            global_data.sfx_mgr.create_sfx_in_scene(break_sfx, pos, on_create_func=self.sfx_create_cb, int_check_type=CREATE_SRC_SIMPLE)

                if self.break_type == collision_const.BREAK_OBJ_TYPE_HP_STATIC:
                    self.show_static_model(self.broken_model)
                    self.show_dynamic_model(self.break_model)
                elif self.break_type == collision_const.BREAK_OBJ_TYPE_HP_BOX:
                    self.show_static_model(self.broken_model)
                elif self.break_type == collision_const.BREAK_OBJ_TYPE_HP_DYNAMIC:
                    self.show_dynamic_model(self.broken_model)

    def show_dynamic_model(self, model):
        if not (model and model.valid):
            return
        else:
            orig_model = self._get_hp_model()
            self._auto_scale_model(orig_model, model)
            if orig_model and orig_model.valid:
                orig_model.destroy()
            model.visible = True
            model.cast_shadow = True
            model.set_attr('first_touched', '1')
            enable_dynamic_physics(model)
            if self.break_type == collision_const.BREAK_OBJ_TYPE_HP_DYNAMIC:
                mask = (collision_const.GROUP_CHARACTER_INCLUDE | collision_const.GROUP_GRENADE) & ~collision_const.GROUP_CAMERA_COLL
                group = collision_const.GROUP_CHARACTER_INCLUDE | collision_const.GROUP_DYNAMIC_SHOOTUNIT
            else:
                mask = (collision_const.GROUP_CHARACTER_EXCLUDE | collision_const.GROUP_GRENADE) & ~collision_const.GROUP_CAMERA_COLL
                group = collision_const.GROUP_CHARACTER_EXCLUDE | collision_const.GROUP_DYNAMIC_SHOOTUNIT
            model.set_mask_and_group(mask, group)
            self.scene.add_breakable_hp_obj_unit_obj(model.name, weakref.ref(self.unit_obj))
            impulse_power = None
            if self._lst_hit_item:
                break_conf = confmgr.get('break_data', str(self._lst_hit_item), default={})
                impulse_power = break_conf.get('cBreakPower', None)
            break_item_info = {'model_col_name': model.name,'point': model.world_position,
               'normal': math3d.vector(0, 1, 0),
               'power': impulse_power,
               'break_type': collision_const.BREAK_TRIGGER_TYPE_WEAPON,
               'no_scale': True
               }
            if not (global_data.game_mode and global_data.game_mode.is_pve()):
                break_item_info.update({'use_orig_scale': True})
            global_data.emgr.scene_add_break_objs.emit([break_item_info], True)
            return

    def show_static_model(self, model):
        if not (model and model.valid):
            return
        model.visible = True
        model.cast_shadow = True
        model.active_collision = True
        model.set_attr('first_touched', '1')

    def destroy(self):
        if self.break_model and self.break_model.valid:
            self.break_model.destroy()
        self.break_model = None
        if self.broken_model and self.broken_model.valid:
            self.broken_model.destroy()
        self.broken_model = None
        self.ex_model_task_done = 0
        return

    def enable_dynamic_emissive(self, m, flag):
        if not (m and m.valid):
            return
        if flag:
            m.all_materials.set_macro('DYNAMIC_EMISSIVE_ENABLE', 'TRUE')
            m.all_materials.rebuild_tech()
            now = render.get_frametime() / 1000.0
            m.all_materials.set_var(_HASH_FrameTimeBreak, 'FrameTimeBreak', now)
            m.all_materials.set_var(_HASH_FrameTimeShine, 'FrameTimeShine', 4.0)
        else:
            m.all_materials.set_macro('DYNAMIC_EMISSIVE_ENABLE', 'FALSE')
            m.all_materials.rebuild_tech()

    def _record_lst_hit_item(self, hit_item):
        if hit_item:
            self._lst_hit_item = hit_item