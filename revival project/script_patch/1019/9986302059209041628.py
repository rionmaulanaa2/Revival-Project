# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComParadropBallCollision.py
from __future__ import absolute_import
import time
import game3d
import math3d
import collision
import world
import math
from .ComObjCollision import ComObjCollision
from logic.gcommon.common_const.sync_const import SENDER_MODE_BALL_CTRL
from common.cfg import confmgr
from logic.gcommon.common_const.collision_const import GROUP_CAN_SHOOT, GROUP_MECHA_BALL, GROUP_GRENADE, GROUP_AUTO_AIM, GROUP_FOOTBALL, GROUP_DYNAMIC_SHOOTUNIT
SCALE = 5
RADIUS = 3.16 * SCALE
SYNC_DELTA_TIME = 0.5
COMPRESSED_TIME = 0.5
FORCE_SCALE = 0.5
DISABLE_PHYSICS_DIST = 5475600
COMPRESSED_TIME_0 = COMPRESSED_TIME / 2.0
FACTOR_A = FORCE_SCALE / COMPRESSED_TIME_0
FACTOR_B = FORCE_SCALE / (COMPRESSED_TIME_0 - COMPRESSED_TIME)
CONST_B = -0.5 * FACTOR_B
FORCE_FACTOR_AGENT = 150
FORCE_FACTOR_SLAVE = 75
MAX_HIT_FORCE = 150
MAX_HIT_FORCE_SLAVE = 75
FORCE_CONTACT_WALL = 50
FORCE_CONTACT_WALL_SLAVE = 25
HIT_FORCE_INTERVAL = 0.2
_HASH_FORCE_RADIUS = game3d.calc_string_hash('Radius')
_HASH_FORCE_DIR = game3d.calc_string_hash('ForceDir')
_HASH_FORCE_FACTOR = game3d.calc_string_hash('ForceFactor')
AREA_RADIUS_MODEL = 100.0
IMPACT_SFX_PATH = 'effect/fx/niudan/s5wanfa/paiqiu_zhuangji.sfx'
COL_TYPE_NONE = 0
COL_TYPE_STATIC = 1
COL_TYPE_DYNAMIC = 2

class ComParadropBallCollision(ComObjCollision):
    BIND_EVENT = ComObjCollision.BIND_EVENT.copy()
    BIND_EVENT.update({'E_ROTATION': '_on_rot_changed',
       'E_ON_AGENT': '_on_agent',
       'E_CANCEL_AGENT': '_on_cancel_agent',
       'G_CHECK_SHOOT_INFO': '_check_shoot_info',
       'E_ON_HIT_POINT_INFO': '_on_hit_point_info',
       'E_ON_HIT_BOMB_INFO': '_on_bombed',
       'E_HEALTH_HP_EMPTY': '_on_die',
       'E_SET_AGENT_FROM_SERVER': '_on_set_agent_from_server',
       'E_HEALTH_HP_CHANGE': '_on_hp_changed'
       })

    def init_from_dict(self, unit_obj, bdict):
        self.sd.ref_ball_driver = None
        self._born_pos = bdict.get('born_position')
        self._move_radius = bdict.get('move_radius')
        self._agent_id = bdict.get('agent_id', None)
        if math.isnan(self._born_pos[0]) or math.isnan(self._born_pos[1]) or math.isnan(self._born_pos[2]):
            import exception_hook
            exception_hook.post_error('[ComParadropBallCollision] _born_pos is nan:%s' % self._born_pos)
            return
        else:
            self._col_type = COL_TYPE_NONE
            self._intrp_time = 0
            self._last_sync_time = 0
            self._is_compressed = False
            self._compressed_time = 0
            self._last_hit_time = 0
            self._shoot_col = None
            self._area_col = None
            self._area_model = None
            self._move_timer = 0
            super(ComParadropBallCollision, self).init_from_dict(unit_obj, bdict)
            return

    def cache(self):
        super(ComParadropBallCollision, self).cache()

    def _create_col_obj(self):
        col_type = COL_TYPE_DYNAMIC if self.sd.ref_is_agent else COL_TYPE_STATIC
        self._create_col_by_type(col_type)
        self._create_shoot_col()

    def on_model_load_complete(self, model):
        super(ComParadropBallCollision, self).on_model_load_complete(model)
        model.all_materials.set_var(_HASH_FORCE_RADIUS, 'Radius', RADIUS)
        model.all_materials.set_var(_HASH_FORCE_FACTOR, 'ForceFactor', float(0.0))
        if G_POS_CHANGE_MGR:
            self.regist_pos_change(self._on_pos_changed)
        self.send_event('E_ACTIVE_SENDER_MODE', SENDER_MODE_BALL_CTRL)
        if self._col_obj:
            self._col_obj.set_linear_velocity(math3d.vector(1, 0, 1) * 200)
        self._clear_move_timer()
        self._move_timer = global_data.game_mgr.get_post_logic_timer().register(func=self._on_tick, interval=1, timedelta=True)

    def on_post_init_complete(self, bdict):
        super(ComParadropBallCollision, self).on_post_init_complete(bdict)
        self.send_event('E_ACTIVE_SENDER_MODE', SENDER_MODE_BALL_CTRL)
        self.send_event('E_SET_ENABLE_ITPL_LV', False)
        if self._col_obj:
            self._col_obj.set_linear_velocity(math3d.vector(1, 0, 1) * 200)
        self._create_region_restrict_col()

    def on_contact(self, *args, **kwargs):
        if not self.is_enable():
            return
        else:
            model = self._model() if self._model else None
            if not model or not model.valid or not self._col_obj or not self._col_obj.valid:
                return
            if len(args) == 3:
                c_obj, point, normal = args
            else:
                my_obj, c_obj, touch, hit_info = args
                if not touch:
                    return
                point = hit_info.position
                normal = hit_info.normal
            rotation = model.world_transformation.rotation
            rotation.inverse()
            normal_local2 = normal * rotation
            normal_local2.normalize()
            need_compress = False
            ignore_collision = hasattr(c_obj, 'ignore_collision') and c_obj.ignore_collision
            if c_obj.mask == GROUP_FOOTBALL and c_obj.group == GROUP_FOOTBALL and ignore_collision:
                need_compress = True
                force = normal
                force.y = 0.3
                force.normalize()
                need_impulse = True if self.sd.ref_is_agent or self._agent_id else False
                if need_impulse:
                    self._col_obj.apply_impulse(force * FORCE_FACTOR_AGENT)
                self._create_impact_effect(point)
            if c_obj.mask == GROUP_FOOTBALL and c_obj.group == GROUP_FOOTBALL and not ignore_collision:
                need_compress = True
                force = normal
                force.y = 0.2
                force.normalize()
                if self.sd.ref_is_agent:
                    self._col_obj.apply_impulse(force * FORCE_CONTACT_WALL)
                elif self._agent_id:
                    self._col_obj.apply_impulse(force * FORCE_CONTACT_WALL_SLAVE)
                self._create_impact_effect(point)
            if not self._is_compressed and need_compress:
                rotation = model.world_transformation.rotation
                rotation.inverse()
                normal_local2 = normal * rotation
                normal_local2.normalize()
                force_normal = (-float(normal_local2.x), -float(normal_local2.y), -float(normal_local2.z))
                model.all_materials.set_var(_HASH_FORCE_DIR, 'ForceDir', force_normal)
                model.all_materials.set_var(_HASH_FORCE_FACTOR, 'ForceFactor', 0.0)
                self._is_compressed = True
                self._force = 0
            return

    def _create_col_by_type(self, col_type):
        if self._model:
            m = self._model() if 1 else None
            return m or None
        else:
            if col_type == self._col_type:
                return
            born_vec = math3d.vector(*self._born_pos)
            scene = global_data.game_mgr.get_cur_scene()
            if math.isnan(born_vec.x) or math.isnan(born_vec.y) or math.isnan(born_vec.z):
                return
            if not scene or not scene.check_collision_loaded(m.center_w, need_refresh=False) or not scene.check_collision_loaded(born_vec, need_refresh=False):
                return
            self._destroy_driver_collision()
            self._col_type = col_type
            mass = 0.5
            mask, group = 65535 ^ (GROUP_CAN_SHOOT | GROUP_AUTO_AIM) | GROUP_FOOTBALL, GROUP_MECHA_BALL | GROUP_FOOTBALL
            self._col_obj = collision.col_object(collision.SPHERE, math3d.vector(RADIUS, RADIUS, RADIUS), mask, group, mass)
            self._col_obj.static_friction = 0
            self._col_obj.dynamic_friction = 0
            self._col_obj.enable_ccd = True
            self._col_obj.is_unragdoll = True
            self._col_obj.set_notify_contact(True)
            self._col_obj.set_contact_callback(self.on_contact)
            self._col_obj.restitution = 1
            self._col_obj.notify_trigger = True
            self._col_obj.position = m.center_w
            self._col_obj.rotation_matrix = m.rotation_matrix
            self._col_obj.kinematic = True
            self.scene.scene_col.add_object(self._col_obj)
            self.sd.ref_ball_driver = self._col_obj
            if col_type == COL_TYPE_STATIC:
                self._col_obj.set_damping(0.4, 0.4)
            else:
                self._col_obj.set_damping(0.0, 0.0)
            return

    def _create_region_restrict_col(self):
        self._destroy_area_col()
        max_hp = self.ev_g_max_hp()
        now_hp = self.ev_g_hp()
        if now_hp < max_hp:
            return
        global_data.emgr.camera_lctarget_open_prez += self._on_open_prez

        def create_cb(model, *args):
            if model and model.valid:
                model.visible = True
                scale = self._move_radius / AREA_RADIUS_MODEL
                model.scale = math3d.vector(scale, 20, scale)
                model.set_rendergroup_and_priority(world.RENDER_GROUP_DECAL, 0)
                self._area_col = collision.col_object(collision.MESH, model, GROUP_FOOTBALL, GROUP_FOOTBALL, 0, True)
                self._area_col.position = math3d.vector(self._born_pos[0], self._born_pos[1], self._born_pos[2])
                self._area_col.rotation_matrix = model.rotation_matrix
                self.scene.scene_col.add_object(self._area_col)
                self._area_model = model

        pos = math3d.vector(self._born_pos[0], self._born_pos[1], self._born_pos[2])
        barrier_model_path = confmgr.get('script_gim_ref')['manyue_region_range']
        global_data.model_mgr.create_model_in_scene(barrier_model_path, pos=pos, on_create_func=create_cb)

    def _create_shoot_col(self):
        if self._model:
            m = self._model() if 1 else None
            return m or None
        else:
            self._destroy_shoot_collision()
            mask, group = GROUP_GRENADE, GROUP_DYNAMIC_SHOOTUNIT
            radius = RADIUS + 1.0
            self._shoot_col = collision.col_object(collision.SPHERE, math3d.vector(radius, radius, radius), mask, group, 0)
            self._shoot_col.ignore_collision = True
            self._shoot_col.position = m.center_w
            self._shoot_col.rotation_matrix = m.rotation_matrix
            self.scene.scene_col.add_object(self._shoot_col)
            global_data.emgr.scene_add_common_shoot_obj.emit(self._shoot_col.cid, self.unit_obj)
            global_data.emgr.scene_add_hit_mecha_event.emit(self._shoot_col.cid, self.unit_obj)
            return

    def _on_tick(self, dt):
        m = self._model() if self._model else None
        if not m or not m.valid:
            return
        else:
            need_col_type = COL_TYPE_DYNAMIC if self.sd.ref_is_agent else COL_TYPE_STATIC
            self._create_col_by_type(need_col_type)
            col_obj = self._col_obj
            if not col_obj or not col_obj.valid:
                return
            col_pos = col_obj.position
            cam_pos = world.get_active_scene().active_camera.position
            col_pos.y = 0
            cam_pos.y = 0
            dist_2 = col_pos - cam_pos
            if dist_2.length_sqr > DISABLE_PHYSICS_DIST:
                self._col_obj.kinematic = True
            elif self.sd.ref_is_agent:
                self._col_obj.kinematic = False
            cpos = col_obj.position
            m.position = cpos
            m.rotation_matrix = col_obj.rotation_matrix
            if self._shoot_col and self._shoot_col.valid:
                self._shoot_col.position = m.position
                self._shoot_col.rotation_matrix = m.rotation_matrix
            if self._is_compressed:
                self._compressed_time += dt
                force = self._calculate_force(self._compressed_time)
                m.all_materials.set_var(_HASH_FORCE_FACTOR, 'ForceFactor', float(force))
                if self._compressed_time > COMPRESSED_TIME:
                    self._compressed_time = 0
                    self._is_compressed = False
            if self.sd.ref_is_agent:
                self._sync_transform()
            return

    def _calculate_force(self, compress_time):
        if compress_time <= COMPRESSED_TIME_0:
            force = FACTOR_A * compress_time
        elif compress_time <= COMPRESSED_TIME:
            force = FACTOR_B * compress_time + CONST_B
        else:
            force = 0
        if force >= 0:
            return force
        return 0

    def _create_impact_effect(self, pos):
        global_data.sfx_mgr.create_sfx_in_scene(IMPACT_SFX_PATH, pos)

    def _clear_move_timer(self):
        if self._move_timer:
            global_data.game_mgr.get_post_logic_timer().unregister(self._move_timer)
        self._move_timer = 0

    def _on_pos_changed(self, pos):
        if self.sd.ref_is_agent:
            return
        else:
            if self._col_obj and self._col_obj.valid:
                self._col_obj.position = pos
                self._col_obj.kinematic = False
            m = self._model() if self._model else None
            if m and m.valid:
                m.position = pos
            if self._shoot_col and self._shoot_col.valid:
                self._shoot_col.position = pos
            return

    def _on_rot_changed(self, rot, force=False):
        mat = math3d.rotation_to_matrix(rot)
        if self._col_obj and self._col_obj.valid:
            self._col_obj.rotation_matrix = mat
            self._col_obj.kinematic = False
        m = self._model() if self._model else None
        if m and m.valid:
            m.rotation_matrix = mat
        if self._shoot_col and self._shoot_col.valid:
            self._shoot_col.rotation_matrix = mat
        return

    def _sync_transform(self):
        if not self._col_obj:
            return
        if time.time() - self._last_sync_time < 0.01:
            return
        self._last_sync_time = time.time()
        mat = self._col_obj.rotation_matrix
        self.notify_pos_change(self._col_obj.position)
        rot = math3d.matrix_to_rotation(mat)
        euler = math3d.rotation_to_euler(rot)
        self.send_event('E_ACTION_SYNC_EULER', euler.x, euler.y, euler.z)

    def _on_agent(self, *args):
        self.send_event('E_ACTIVE_SENDER_MODE', SENDER_MODE_BALL_CTRL)
        self._create_col_by_type(COL_TYPE_DYNAMIC)
        if self._col_obj and self._col_obj.valid:
            self._col_obj.set_linear_velocity(math3d.vector(1, 0, 1) * 200)

    def _on_cancel_agent(self, *args):
        if self._col_obj and self._col_obj.valid:
            self._col_obj.kinematic = True

    def _on_set_agent_from_server(self, agent_id):
        self._agent_id = agent_id
        if not agent_id and self._col_obj and self._col_obj.valid:
            self._col_obj.kinematic = True

    def _check_shoot_info(self, begin, pdir, hit_pos=None):
        return 0

    def _on_bombed(self, bomb_pos, damage):
        if not self.sd.ref_is_agent or not self._col_obj or not self._col_obj.valid:
            return
        col_pos = self._col_obj.position
        self._on_hit_point_info(bomb_pos, col_pos, damage)

    def _on_hit_point_info(self, from_pos, target_pos, damage):
        if not self.sd.ref_is_agent or not self._col_obj or not self._col_obj.valid:
            return
        if time.time() - self._last_hit_time < HIT_FORCE_INTERVAL:
            return
        dir = target_pos - from_pos
        if dir.is_zero:
            return
        dir.normalize()
        self._last_hit_time = time.time()
        max_force = MAX_HIT_FORCE if self.sd.ref_is_agent else MAX_HIT_FORCE_SLAVE
        hit_force = damage / 300.0 * max_force
        if hit_force > MAX_HIT_FORCE:
            hit_force = MAX_HIT_FORCE
        self._col_obj.apply_impulse(dir * hit_force)

    def _on_die(self, *args):
        m = self._model() if self._model else None
        if not m or not m.valid:
            return
        else:
            sfx_path = 'effect/fx/niudan/s5wanfa/paiqiu_die.sfx'
            global_data.sfx_mgr.create_sfx_in_scene(sfx_path, m.world_position)
            self.destroy_col()
            self._clear_move_timer()
            return

    def _on_hp_changed(self, hp, *args):
        max_hp = self.ev_g_max_hp()
        if max_hp and hp < max_hp:
            self._destroy_area_col()
            hp_change_event = {'E_HEALTH_HP_CHANGE': '_on_hp_changed'
               }
            self._unbind_event(hp_change_event)

    def _destroy_driver_col(self):
        if self._col_obj:
            self.scene.scene_col.remove_object(self._col_obj)
        self._col_obj = None
        return

    def _destroy_area_col(self):
        if self._area_col:
            self.scene.scene_col.remove_object(self._area_col)
        self._area_col = None
        if self._area_model:
            global_data.model_mgr.remove_model(self._area_model)
            global_data.emgr.camera_lctarget_open_prez -= self._on_open_prez
        self._area_model = None
        return

    def _destroy_shoot_collision(self):
        if self._shoot_col:
            global_data.emgr.scene_remove_common_shoot_obj.emit(self._shoot_col.cid)
            self.scene.scene_col.remove_object(self._shoot_col)
        self._shoot_col = None
        return

    def _destroy_driver_collision(self):
        if self._col_obj:
            self.scene.scene_col.remove_object(self._col_obj)
        self._col_obj = None
        self._col_type = COL_TYPE_NONE
        self.sd.ref_ball_driver = None
        return

    def _on_open_prez(self, enable):
        if self._area_model and self._area_model.valid:
            if enable:
                self._area_model.all_materials.set_macro('DEPTH_OUTLINE', 'FALSE')
            else:
                self._area_model.all_materials.set_macro('DEPTH_OUTLINE', 'TRUE')
            self._area_model.all_materials.rebuild_tech()

    def destroy_col(self):
        self._destroy_area_col()
        self._destroy_shoot_collision()
        super(ComParadropBallCollision, self).destroy_col()

    def destroy(self):
        self._clear_move_timer()
        super(ComParadropBallCollision, self).destroy()