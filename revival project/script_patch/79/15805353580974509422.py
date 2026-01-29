# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComMechaCollison.py
from __future__ import absolute_import
from ..UnitCom import UnitCom
from logic.gcommon.const import COLOR_MASK, COLOR_PART_MAP, BODY_COLOR, LEG_COLOR
from logic.gcommon.common_const import scene_const
from data.constant_break_data import data as constant_break_list
from common.cfg import confmgr
from logic.gcommon.const import NEOX_UNIT_SCALE
from mobile.common.EntityManager import EntityManager
from logic.gutils.scene_utils import SNOW_SCENE_BOX_MODEL_ENT_MAP, is_airwall_model, get_airwall_sfx, apply_ragdoll_explosion
from logic.gutils.dress_utils import get_mecha_model_hit_path, DEFAULT_CLOTHING_ID
from logic.gutils.model_collision_utils import ModelCollisionAgent
from common.utils.sfxmgr import CREATE_SRC_SIMPLE, CREATE_SRC_ONE
from logic.gutils.mecha_utils import do_hit_phantom
import logic.gcommon.common_const.animation_const as animation_const
import logic.gcommon.common_const.collision_const as collision_const
import collision
import math3d
import world
import weakref
import time
from math import ceil
MAX_TICK_TIME = 1
FOOTBALL_COL_SCALE_MINE = 1.0
FOOTBALL_COL_SCALE = 1.7
HIT_PHANTOM_INTERVAL = 1.0

class ComMechaCollison(UnitCom):
    BIND_COL_BONE_NAME = animation_const.BONE_BIPED_NAME
    BIND_EVENT = {'E_HUMAN_MODEL_LOADED': 'on_humman_model_load',
       'G_HUMAN_COL_ID': 'get_human_col_id',
       'G_HUMAN_COL': 'get_human_col',
       'G_HUMAN_BASE_COL_ID': 'get_human_base_col_id',
       'G_HUMAN_COL_INFO': 'get_human_col_info',
       'E_REFRESH_COL_CAMP': 'refresh_collision_camp',
       'E_DEATH': 'die',
       'G_MODEL_HIT_RAY': 'get_hit_by_ray_color',
       'G_SHOOT_PART': 'be_shoot_check',
       'G_HIT_MODEL': 'get_hit_model',
       'E_MARK_GROUPMATE': 'mark_groupmate',
       'E_ON_JOIN_MECHA': '_on_join_mecha',
       'E_ON_LEAVE_MECHA': '_on_leave_mecha',
       'E_MODIFY_MECHA_RELATIVE_COLS': 'on_modify_relative_col',
       'E_OX_BEGIN_RUSH': 'create_collision_timer',
       'E_OX_END_RUSH': 'clear_collision_timer',
       'E_SET_RUSH_COL_SIZE': 'set_rush_col_size',
       'E_RESET_RUSH_COL_SIZE': 'reset_rush_col_size',
       'E_DISABLE_SHOOT_COL': 'disable_col',
       'E_RESET_SHOOT_COL': 'reset_col_info',
       'E_REBIND_SHOOT_COL': 'rebind_col',
       'E_GM_RESCALE_TARGET': 'gm_rescale_mecha_model',
       'E_ACTIVE_BALL_DRIVER': '_active_ball_driver',
       'E_DISABLE_BALL_DRIVER': '_disable_ball_driver',
       'E_BEGIN_REFRESH_WHOLE_MODEL': 'on_begin_refresh_whole_model',
       'E_ADD_HANDY_SHIELD_COL': 'add_handy_shield_col',
       'E_REMOVE_HANDY_SHIELD_COL': 'remove_handy_shield_col',
       'E_SWITCH_MODEL': 'on_switch_model',
       'E_CHANGE_MECHA_COLLISION': 'on_change_collision'
       }
    ENABLE_RAGDOLL_EXPLODE = True

    def __init__(self):
        super(ComMechaCollison, self).__init__()
        self.col = None
        self.break_col = None
        self._football_col = None
        self.handy_shield_col = None
        self._hit_ref = None
        self.break_obj_list = []
        self.sd.ref_mecha_relative_cols = set()
        self._timer_id = None
        self._driver_id = None
        self.break_power = None
        self.break_dash_power = None
        self.collision_sfx = None
        self.collision_sfx_last_time = 0
        self.original_col_group = 0
        self.original_col_mask = 0
        self._load_mesh_task = None
        self._last_col_time = 0
        self._last_col_position = None
        self.model_col_agent = None
        self.default_rush_col_size = self.rush_col_size = [
         2.5, 3, 2.5]
        self.get_hit_model_path_func = None
        self.hit_phantom = {}
        return

    def init_from_dict(self, unit_obj, bdict):
        super(ComMechaCollison, self).init_from_dict(unit_obj, bdict)
        self._mecha_id = bdict.get('mecha_id', '8001')
        self._dead = bdict.get('hp', 0) == 0
        if not self._dead:
            self.need_update = True
        self.sd.ref_skip_model_ray_check = False
        self.collision_sfx = constant_break_list.get(1, {}).get('cResFx', None)
        phy_conf = confmgr.get('mecha_conf', 'PhysicConfig', 'Content', str(self._mecha_id), default={})
        self.break_power = phy_conf.get('break_power', None)
        self.break_dash_power = phy_conf.get('break_dash_power', None)
        pve_fix = global_data.game_mode.is_pve()
        self.shoot_collison_size = pve_fix or phy_conf.get('shoot_collison_size') if 1 else phy_conf.get('pve_shoot_col_size')
        self.shield_radius = phy_conf.get('shield_radius')
        self.shoot_col_pos_offset = None
        self.shield_col_pos_offset = None
        self.is_reycling = bdict.get('pre_standby', False)
        self._refresh_get_hit_model_path_func()
        self.handle_sunshine()
        self.rush_col_pos_offset = math3d.vector(0, 20, 0)
        self.model_col_agent = ModelCollisionAgent(self)
        return

    def on_init_complete(self):
        super(ComMechaCollison, self).on_init_complete()
        if self._mecha_id in collision_const.MECHA_IDLE_BIPED_BONE_LOCAL_POS_Y:
            y = collision_const.MECHA_IDLE_BIPED_BONE_LOCAL_POS_Y[self._mecha_id]
            if type(y) is tuple:
                y = y[0]
            self.rush_col_pos_offset = math3d.vector(0, y, 0)

    def handle_sunshine(self):
        if not global_data.use_sunshine:
            return
        p = global_data.sunshine_mecha_col_dict
        if not p:
            return
        m_id = p.get('mecha_id', 0)
        if str(m_id) == str(self._mecha_id):
            shoot_col_size = p.get('shoot_col_size', [0, 0])
            if shoot_col_size[0]:
                self.shoot_collison_size = shoot_col_size

    def _refresh_get_hit_model_path_func(self):
        if global_data.force_mecha_empty_model_path:
            self.get_hit_model_path_func = self.get_hit_model_path_in_editor
        else:
            self.get_hit_model_path_func = self.get_hit_model_path

    def get_human_col_id(self):
        ret = []
        for col in [self.col, self.handy_shield_col]:
            if col:
                ret.append(col.cid)

        return ret

    def get_human_col(self):
        ret = []
        for col in [self.col, self.handy_shield_col]:
            if col:
                ret.append(col)

        return ret

    def add_handy_shield_col(self, col):
        self.handy_shield_col = col

    def remove_handy_shield_col(self):
        self.handy_shield_col = None
        return

    def die(self, *args):
        self.remove_col()
        model = self.ev_g_model()
        apply_ragdoll_explosion(model, None)
        return

    def get_hit_model(self):
        return self._hit_ref()

    def mark_groupmate(self):
        if self.col:
            self.col.mask = collision_const.GROUP_SHOOTUNIT
            self.col.group = collision_const.GROUP_SHOOTUNIT
            self.model_col_agent.set_mask_and_group(self.col.mask, self.col.group)

    def tick(self, dt):
        if self.break_obj_list:
            global_data.emgr.scene_add_break_objs.emit(self.break_obj_list, True)
            self.break_obj_list = []
        if global_data.game_time - self._last_col_time > MAX_TICK_TIME:
            self.need_update = False

    def can_create_col(self):
        if self._dead:
            return False
        if not self.scene:
            return False
        if self.col:
            return False
        return True

    def create_shoot_collision(self, model, scl_xyz=1, mesh_model=None):
        if not self.can_create_col():
            return
        if not self.shoot_collison_size:
            return
        scale = self.unit_obj.get_battle()._ai_hit_box if self.sd.ref_is_robot else 1.0
        col_size = math3d.vector(*self.shoot_collison_size) * (0.5 * NEOX_UNIT_SCALE * scl_xyz * scale)
        self.col = collision.col_object(collision.BOX, col_size, 0, 0, 0)
        self.bind_shoot_collision(model)

    def bind_shoot_collision(self, model=None):
        if not model:
            model = self.ev_g_model()
        self.scene.scene_col.add_object(self.col)
        self.col.mask = collision_const.GROUP_GRENADE
        self.col.group = collision_const.GROUP_DYNAMIC_SHOOTUNIT | collision_const.GROUP_AUTO_AIM
        self.col.ignore_collision = True
        self.col.car_undrivable = True
        driver_id = self.sd.ref_driver_id
        if global_data.player.logic.ev_g_get_bind_mecha() == self.unit_obj.id:
            self.col.mask = self.col.mask & ~collision_const.GROUP_AUTO_AIM
            self.col.group = self.col.group & ~collision_const.GROUP_AUTO_AIM
        if driver_id and global_data.player.logic.ev_g_is_groupmate(driver_id):
            self.col.mask = self.col.mask & ~collision_const.GROUP_AUTO_AIM
            self.col.group = self.col.group & ~collision_const.GROUP_AUTO_AIM
        if driver_id and self.check_is_camp(global_data.player.logic.ev_g_camp_id()):
            self.col.mask = self.col.mask & ~collision_const.GROUP_AUTO_AIM
            self.col.group = self.col.group & ~collision_const.GROUP_AUTO_AIM
        self.model_col_agent.set_mask_and_group(self.col.mask, self.col.group)
        self.original_col_mask = self.col.mask
        self.original_col_group = self.col.group
        self.rush_col = collision.col_object(collision.BOX, math3d.vector(*self.rush_col_size) * NEOX_UNIT_SCALE)
        model.bind_col_obj(self.col, self.BIND_COL_BONE_NAME)
        if self.shoot_col_pos_offset:
            self.col.bone_matrix = math3d.matrix.make_translation(self.shoot_col_pos_offset.x, self.shoot_col_pos_offset.y, self.shoot_col_pos_offset.z)
        self._hit_ref = weakref.ref(model)
        self.add_shoot_event()
        global_data.emgr.scene_add_hit_mecha_event.emit(self.col.cid, self.unit_obj)
        self._create_football_collision(model)

    def add_shoot_event(self):
        global_data.emgr.scene_add_shoot_mecha_event.emit(self.col.cid, self.unit_obj)

    def remove_shoot_event(self):
        global_data.emgr.scene_remove_shoot_mecha_event.emit(self.col.cid)

    def refresh_collision_camp(self):
        if not self.col:
            return
        col_mask = collision_const.GROUP_GRENADE
        col_group = collision_const.GROUP_DYNAMIC_SHOOTUNIT | collision_const.GROUP_AUTO_AIM
        driver_id = self.ev_g_driver()
        if global_data.player.logic.ev_g_get_bind_mecha() == self.unit_obj.id:
            col_mask = col_mask & ~collision_const.GROUP_AUTO_AIM
            col_group = col_group & ~collision_const.GROUP_AUTO_AIM
        if driver_id and global_data.player.logic.ev_g_is_groupmate(driver_id):
            col_mask = col_mask & ~collision_const.GROUP_AUTO_AIM
            col_group = col_group & ~collision_const.GROUP_AUTO_AIM
        if driver_id and self.check_is_camp(global_data.player.logic.ev_g_camp_id()):
            col_mask = col_mask & ~collision_const.GROUP_AUTO_AIM
            col_group = col_group & ~collision_const.GROUP_AUTO_AIM
        self.col.mask = col_mask if self.col.mask else self.col.mask
        self.col.group = col_group if self.col.group else self.col.group
        self.model_col_agent.set_mask_and_group(self.col.mask, self.col.group)
        self.original_col_mask = col_mask
        self.original_col_group = col_group

    def _create_football_collision(self, model):
        if global_data.game_mode and global_data.game_mode.is_summer_environment():
            self._destroy_football_col()
            return self.shield_radius or None
        if global_data.player.logic.ev_g_get_bind_mecha() == self.unit_obj.id:
            scale = FOOTBALL_COL_SCALE_MINE if 1 else FOOTBALL_COL_SCALE
            self._football_col = collision.col_object(collision.SPHERE, math3d.vector(self.shield_radius * scale, 0, 0), 0, 0, 0)
            self._football_col.mask = collision_const.GROUP_FOOTBALL
            self._football_col.group = collision_const.GROUP_FOOTBALL
            self._football_col.ignore_collision = True
            model.bind_col_obj(self._football_col, self.BIND_COL_BONE_NAME)
            if self.shield_col_pos_offset:
                self._football_col.bone_matrix = math3d.matrix.make_translation(self.shield_col_pos_offset.x, self.shield_col_pos_offset.y, self.shield_col_pos_offset.z)

    def create_break_collision(self, model):
        if self._dead:
            return
        if not self.scene:
            return
        if self.break_col:
            return
        if not self.shoot_collison_size:
            return
        self.break_col = collision.col_object(collision.BOX, math3d.vector(self.shoot_collison_size[0] / 2 * NEOX_UNIT_SCALE, self.shoot_collison_size[1] / 2 * NEOX_UNIT_SCALE, self.shoot_collison_size[2] / 2 * NEOX_UNIT_SCALE), 0, 0, 1)
        self.scene.scene_col.add_object(self.col)
        self.break_col.mask = collision_const.GROUP_SHOOTUNIT
        self.break_col.group = collision_const.GROUP_BREAK
        driver_id = self.sd.ref_driver_id
        self.break_col.set_notify_contact(True)
        self.break_col.set_contact_callback(self.on_contact)
        self.break_col.kinematic = True
        self.break_col.is_unragdoll = True
        model.bind_col_obj(self.break_col, self.BIND_COL_BONE_NAME)
        if self.shoot_col_pos_offset:
            self.break_col.bone_matrix = math3d.matrix.make_translation(self.shoot_col_pos_offset.x, self.shoot_col_pos_offset.y, self.shoot_col_pos_offset.z)

    def on_contact(self, *args):
        is_dash = self.ev_g_is_dash()
        if is_dash:
            if not self.break_dash_power:
                return
        elif not self.break_power:
            return
        if is_dash:
            power = self.break_dash_power if 1 else self.break_power
            if len(args) == 3:
                cobj, point, normal = args
            else:
                my_obj, cobj, touch, hit_info = args
                if not touch:
                    return
                point = hit_info.position
                normal = hit_info.normal
            trigger_sfx = None
            trigger_enable_interval = False
            trigger_enable_normal_modify = False
            now = time.time()
            if now - self.collision_sfx_last_time > collision_const.COLLISION_SFX_INTERVAL:
                trigger_enable_interval = True
            model_col_name = getattr(cobj, 'model_col_name', None)
            sfx_duration = 0
            if trigger_enable_interval:
                if is_airwall_model(model_col_name):
                    trigger_sfx = get_airwall_sfx()
                    trigger_enable_normal_modify = True
                    sfx_duration = 3.0
                elif self.collision_sfx and cobj and cobj.group in (scene_const.COL_METAL, scene_const.COL_STONE):
                    trigger_sfx = self.collision_sfx
                else:
                    trigger_sfx = None
            if trigger_enable_interval and trigger_sfx:
                self.collision_sfx_last_time = now
                on_create_func = None
                if trigger_enable_normal_modify:

                    def create_cb(sfx):
                        if sfx and normal:
                            global_data.sfx_mgr.set_rotation_by_world_normal_ex(sfx, normal)

                    on_create_func = create_cb
                global_data.sfx_mgr.create_sfx_in_scene(trigger_sfx, point, duration=sfx_duration, int_check_type=CREATE_SRC_ONE, on_create_func=on_create_func)
            if model_col_name:
                break_type = collision_const.BREAK_TRIGGER_TYPE_MECHA_DASH if is_dash else collision_const.BREAK_TRIGGER_TYPE_MECHA_MOVE
                break_entity_id = SNOW_SCENE_BOX_MODEL_ENT_MAP.get(cobj.model_col_name, None)
                break_item_info = {'model_col_name': cobj.model_col_name,'point': point,
                   'normal': normal,
                   'power': power,
                   'break_type': break_type,
                   'break_entity_id': break_entity_id
                   }
                self.break_obj_list.append(break_item_info)
                self.need_update = self._need_update or True
                self._last_col_time = global_data.game_time
        return

    def get_hit_model_path(self, mecha_fashion_id):
        return get_mecha_model_hit_path(self._mecha_id, mecha_fashion_id)

    def get_hit_model_path_in_editor(self, mecha_fashion_id):
        if global_data.force_mecha_empty_model_path and self.ev_g_is_avatar():
            return global_data.force_mecha_empty_model_path.replace('empty', 'hit')
        else:
            return get_mecha_model_hit_path(self._mecha_id, mecha_fashion_id)

    def on_humman_model_load(self, model, *arg):
        if self.is_reycling:
            return
        self.create_shoot_collision(model)
        self.create_break_collision(model)
        if self.col:
            self.model_col_agent.set_mask_and_group(self.col.mask, self.col.group)
            mecha_fashion_id = self.ev_g_mecha_fashion_id()
            hit_path = self.get_hit_model_path_func(mecha_fashion_id)
            backup_hit_path = self.get_hit_model_path_func(DEFAULT_CLOTHING_ID)
            if self.sd.ref_second_model_dir:
                self.model_col_agent.load(self.ev_g_mecha_original_model(), hit_path, backup_hit_path)
                index = hit_path.rfind('/')
                hit_path = hit_path[:index] + '/' + self.sd.ref_second_model_dir + hit_path[index:]
                index = backup_hit_path.rfind('/')
                backup_hit_path = backup_hit_path[:index] + '/' + self.sd.ref_second_model_dir + backup_hit_path[index:]
                self.model_col_agent.load(self.ev_g_mecha_second_model(), hit_path, backup_hit_path)
            else:
                self.model_col_agent.load(model, hit_path, backup_hit_path)
            self.model_col_agent.set_cur_model(model)

    def remove_col(self, model=None):
        if model is None:
            model = self.ev_g_model()
        if self.col:
            if model:
                model.unbind_col_obj(self.col)
            self.remove_shoot_event()
            global_data.emgr.scene_remove_hit_mecha_event.emit(self.col.cid)
            self.scene.scene_col.remove_object(self.col)
            self.col = None
        if self.break_col:
            if model:
                model.unbind_col_obj(self.break_col)
            self.scene.scene_col.remove_object(self.break_col)
            self.break_col = None
        self._destroy_football_col()
        return

    def destroy(self):
        self.hit_phantom = {}
        self.get_hit_model_path_func = None
        self.remove_col()
        if self.model_col_agent:
            self.model_col_agent.destroy()
            self.model_col_agent = None
        self.clear_collision_timer()
        super(ComMechaCollison, self).destroy()
        return

    def get_hit_by_ray_color(self, begin, pdir):
        if not self._hit_ref:
            return None
        else:
            return self.model_col_agent.check_shoot_part(begin, pdir)

    def be_shoot_check(self, color):
        color = color & COLOR_MASK
        color = color if color in COLOR_PART_MAP else LEG_COLOR
        return COLOR_PART_MAP[color]

    def get_human_col_info(self):
        return (
         self.col.group, self.col.mask)

    def get_human_base_col_id(self):
        if self.col:
            return self.col.cid
        else:
            return None

    def _on_join_mecha(self):
        self.on_collision_set(True)
        self._driver_id = self.sd.ref_driver_id

    def _on_leave_mecha(self):
        if self.unit_obj.get_owner().is_share():
            return
        else:
            self.remove_col()
            self.on_collision_set(True)
            self._driver_id = None
            return

    def on_begin_refresh_whole_model(self):
        self._refresh_get_hit_model_path_func()
        self.model_col_agent.unload()
        self.remove_col()

    def on_collision_set(self, flag):
        pass

    def on_modify_relative_col(self, add, cid):
        if add:
            self.sd.ref_mecha_relative_cols.add(cid)
        else:
            cid in self.sd.ref_mecha_relative_cols and self.sd.ref_mecha_relative_cols.remove(cid)

    def disable_col(self):
        if not self.col:
            return
        self.original_col_group = self.col.group
        self.original_col_mask = self.col.mask
        self.col.group = 0
        self.col.mask = 0
        model = self.ev_g_model()
        if model:
            model.unbind_col_obj(self.col)
        self.remove_shoot_event()
        global_data.emgr.scene_remove_hit_mecha_event.emit(self.col.cid)

    def reset_col_info(self):
        if not self.col:
            return
        self.col.group = self.original_col_group
        self.col.mask = self.original_col_mask
        self.scene.scene_col.add_object(self.col)
        model = self.ev_g_model()
        if model:
            model.bind_col_obj(self.col, self.BIND_COL_BONE_NAME)
        self.add_shoot_event()
        global_data.emgr.scene_add_hit_mecha_event.emit(self.col.cid, self.unit_obj)

    def rebind_col(self, bone_name):
        if not self.col or not self.col.valid:
            return
        model = self.ev_g_model()
        if not model or not model.valid:
            return
        model.unbind_col_obj(self.col)
        model.bind_col_obj(self.col, bone_name)

    def collision_test(self):
        if not self.unit_obj.is_valid():
            return
        else:
            model = self.ev_g_model()
            if not model:
                return
            if self.col and self.col.valid:
                cur_col_pos = self.col.position
            else:
                cur_col_pos = model.position + self.rush_col_pos_offset
            self.rush_col.rotation_matrix = model.rotation_matrix

            def do_static_test(hitted_cobj=None):
                result = self.scene.scene_col.static_test(self.rush_col, -1, collision_const.GROUP_DYNAMIC_SHOOTUNIT, collision.INCLUDE_FILTER)
                if result:
                    for cobj in result:
                        if hitted_cobj is not None:
                            if cobj in hitted_cobj:
                                continue
                            hitted_cobj.add(cobj)
                        if cobj.cid in global_data.phantoms:
                            if cobj.cid not in self.hit_phantom or time.time() - self.hit_phantom[cobj.cid] > HIT_PHANTOM_INTERVAL:
                                unit = global_data.emgr.scene_find_unit_event.emit(cobj.cid)[0]
                                if unit:
                                    self.hit_phantom[cobj.cid] = time.time()
                                    do_hit_phantom(self, unit)
                                    continue
                        global_data.emgr.scene_mecha_collision_event.emit(cobj.cid, self.unit_obj.id, model.position, self._driver_id)

                result = self.scene.scene_col.static_test(self.rush_col, collision_const.GROUP_GRENADE, collision_const.GROUP_SHIELD, collision.INCLUDE_FILTER)
                if result:
                    for cobj in result:
                        if hitted_cobj is not None:
                            if cobj in hitted_cobj:
                                continue
                            hitted_cobj.add(cobj)
                        global_data.emgr.scene_field_shield_event.emit(cobj.cid, self.unit_obj.id, model.position, self._driver_id)

                return

            move_time = 1
            if self._last_col_position:
                self.rush_col.position = cur_col_pos
                do_static_test()
                move = cur_col_pos - self._last_col_position
                move_dist = move.length
                if move_dist > 0.1:
                    move_time = ceil(move_dist / (self.rush_col_size[2] * 2 * NEOX_UNIT_SCALE))
                    if move_time > 1:
                        move_dist /= move_time
                        move.normalize()
                hitted_cobj = set()
                for i in range(int(move_time)):
                    self.rush_col.position = cur_col_pos - move * i * move_dist
                    do_static_test(hitted_cobj)

            else:
                self.rush_col.position = cur_col_pos
                do_static_test()
            self._last_col_position = cur_col_pos
            return

    def create_collision_timer(self, *args):
        self.clear_collision_timer()
        self.hit_phantom = {}
        tm = global_data.game_mgr.get_logic_timer()
        self._timer_id = tm.register(func=self.collision_test, interval=1, times=-1)
        self._last_col_position = None
        self.collision_test()
        return

    def clear_collision_timer(self):
        if self._timer_id:
            tm = global_data.game_mgr.get_logic_timer()
            tm.unregister(self._timer_id)
            self._timer_id = None
        return

    def set_rush_col_size(self, size):
        if size == self.rush_col_size:
            return
        self.rush_col_size = size
        self.rush_col = collision.col_object(collision.BOX, math3d.vector(*self.rush_col_size) * NEOX_UNIT_SCALE)

    def reset_rush_col_size(self):
        self.set_rush_col_size(self.default_rush_col_size)

    def check_is_camp(self, target_camp_id):
        if target_camp_id is None:
            return False
        else:
            driver = EntityManager.getentity(self.sd.ref_driver_id)
            if not (driver and driver.logic):
                return False
            my_camp_id = driver.logic.ev_g_camp_id()
            return my_camp_id == target_camp_id

    def gm_rescale_mecha_model(self, scl_xyz):
        f_scl_xyz = float(scl_xyz)
        model = self.ev_g_model()
        if not model:
            return
        self.remove_col()
        self.create_shoot_collision(model, f_scl_xyz)

    def _active_ball_driver(self, *args):
        self._destroy_football_col()

    def _disable_ball_driver(self, *args):
        model = self.ev_g_model()
        if model:
            self._create_football_collision(model)

    def _destroy_football_col(self):
        if self._football_col:
            model = self.ev_g_model()
            if model:
                model.unbind_col_obj(self._football_col)
            self._football_col = None
        return

    def on_switch_model(self, model):
        old_model = self.ev_g_mecha_original_model() if self.sd.ref_using_second_model else self.ev_g_mecha_second_model()
        self.remove_col(old_model)
        self.create_shoot_collision(model)
        self.create_break_collision(model)
        if self.col:
            self.model_col_agent.set_cur_model(model)

    def on_change_collision(self, shield_col_info=None, shoot_col_info=None):
        model = self.ev_g_model()
        if not model:
            return
        else:
            mecha_conf = self.ev_g_mecha_config('PhysicConfig')
            pve_fix = global_data.game_mode.is_pve()
            self.shoot_collison_size = pve_fix or mecha_conf.get('shoot_collison_size') if 1 else mecha_conf.get('pve_shoot_col_size')
            self.shield_radius = mecha_conf['shield_radius']
            self.shield_col_pos_offset = None
            self.shoot_col_pos_offset = None
            if shield_col_info:
                self.shield_radius, self.shield_col_pos_offset = shield_col_info
            if shoot_col_info:
                self.shoot_collison_size, self.shoot_col_pos_offset = shoot_col_info
            self.remove_col(model)
            self.create_shoot_collision(model)
            self.create_break_collision(model)
            if self.col:
                self.model_col_agent.set_cur_model(model)
            return