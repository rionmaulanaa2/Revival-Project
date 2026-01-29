# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComExplosiveRobotDriver.py
from __future__ import absolute_import
import world
import math
import math3d
import weakref
import game3d
from common.cfg import confmgr
from logic.gcommon.const import NEOX_UNIT_SCALE
from ..UnitCom import UnitCom
from ...cdata import jump_physic_config
import common.utils.timer as timer
from mobile.common.EntityManager import EntityManager
import random
import logic.gcommon.common_utils.bcast_utils as bcast
import world
from logic.entities import Avatar, Puppet
from logic.gcommon.common_utils.math3d_utils import v3d_to_tp
from logic.gcommon.common_const import collision_const
import collision
from logic.gcommon.utility import dummy_cb
from logic.gutils.weapon_skin_utils import get_explosive_robot_conf
from common.utils.sfxmgr import CREATE_SRC_SIMPLE
EXPLOSIVE_ROBOT_STATE_APPEAR = 0
EXPLOSIVE_ROBOT_STATE_MOVE = 1
EXPLOSIVE_ROBOT_STATE_JMUP = 2
EXPLOSIVE_ROBOT_STATE_SWOOP = 3
EXPLOSIVE_ROBOT_STATE_DISABLE = 4
APPEAR_LAST_TIME = 1.3
SEARCH_RADIUS = 40 * NEOX_UNIT_SCALE
DOT_VALUE_TO_JUMP = 0.6
ROBOT_AIM_SOCKET_NAME = 'aim_start'
CHECK_JUMP_DISTANCE = 1.5

class ComExplosiveRobotDriver(UnitCom):
    CHECK_JUMP_MIN_DISTANCE_SQR = (2.5 * NEOX_UNIT_SCALE) ** 2
    CHECK_LAST_JUMP_POS_DISTANCE_SQE = (0.5 * NEOX_UNIT_SCALE) ** 2
    CHECK_INTERVAL = 0.5
    SLOW_MODEL_POS_SCALE = 0.8
    BIND_EVENT = {'E_MODEL_LOADED': 'on_model_loaded',
       'E_EXPLOSIVE_ROBOT_LOCK_TARGET': 'on_lock_target',
       'E_EXPLOSIVE_ROBOT_TIMEOUT': 'on_explosive',
       'G_IS_ENEMY': 'is_enemy'
       }

    def __init__(self):
        super(ComExplosiveRobotDriver, self).__init__()
        self._tick_func = None
        self._lock_target = None
        self._lock_model = None
        self.sd.ref_is_robot = True
        self._pos_cache = None
        self.need_check_reattach_model = False
        return

    def init_from_dict(self, unit_obj, bdict):
        super(ComExplosiveRobotDriver, self).init_from_dict(unit_obj, bdict)
        if not self.sd.ref_gravity_scale:
            self.sd.ref_gravity_scale = 1.0
        target_id = bdict.get('trace_target', None)
        if target_id is None:
            self._lock_target = None
            self._lock_model = None
        else:
            entity = EntityManager.getentity(target_id)
            if entity:
                self._lock_target = entity.logic
                self._lock_model = self._lock_target.ev_g_model()
        master_id = bdict.get('master_id', None)
        if master_id:
            self._master = EntityManager.getentity(master_id)
            if self._master:
                self._master = self._master.logic
        else:
            self._master = None
        self.model = None
        self.need_update = True
        self._save_pos = None
        self._last_jump_pos = math3d.vector(0, 0, 0)
        self._check_jump_end = 0
        self._move_direction = math3d.vector(1, 0, 1)
        self.state = EXPLOSIVE_ROBOT_STATE_APPEAR
        self._refresh_to_pos_tick = 0.0
        self._to_pos = None
        robot_id = bdict.get('robot_no', 105611)
        spd_add_factor = self._master.ev_g_add_attr('boom_robot_charge_spd_factor') if self._master else 0
        range_add_factor = self._master.ev_g_add_attr('boom_robot_charge_range_factor') if self._master else 0
        self.robot_data = get_explosive_robot_conf(robot_id)
        self.cur_speed = self.robot_data['walk'] * NEOX_UNIT_SCALE * (1 + spd_add_factor)
        self.mecha_range_charge = self.robot_data['mecha_range_charge'] * NEOX_UNIT_SCALE
        self.human_range_charge = self.robot_data['human_range_charge'] * NEOX_UNIT_SCALE
        self.range_charge = self.human_range_charge
        self.range_speed = self.robot_data['range_speed'] * NEOX_UNIT_SCALE
        self.active_dist_mecha = self.robot_data['active_dist'] * NEOX_UNIT_SCALE * (1 + range_add_factor)
        self.active_dist_human = self.robot_data['active_dist_human'] * NEOX_UNIT_SCALE * (1 + range_add_factor)
        self.attack_dist = self.robot_data['attack_dist'] * NEOX_UNIT_SCALE
        self.attack_dist_human = self.robot_data['attack_dist_human'] * NEOX_UNIT_SCALE
        self.init_character()
        self.model = self.ev_g_model()
        if self.model:
            self.on_model_loaded(self.model)
        self._tick_func = self.tick_appear
        self.jump_check_downcount = 0.0
        self.explosion_downcount = 0.0
        self.appear_downcount = 0.0
        self.cur_animate = None
        self.lock_sfx = None
        self.lock_sfx_id = None
        self.lock_socket_name = ''
        self.search_timer = None
        self._diff_pre = None
        self.upload_tick = 0.0
        self.old_upload_pos = None
        return

    def on_init_complete(self):
        pass

    def on_model_loaded(self, model):
        self.model = model
        self.set_physx_sync_lod(model)
        self.play_animation('transform')
        self.model.register_on_end_event(self.animate_callback, False)
        passenger = self.ev_g_passenger_info()
        scene = self.scene
        char_ctrl = self.sd.ref_character
        if char_ctrl and scene:
            scene = self.scene
            char_ctrl.activate(scene.scene_col)
            char_ctrl.group = char_ctrl.group | collision_const.GROUP_GRENADE
            self.send_event('E_FOOT_POSITION', model.position)
        mat = math3d.matrix.make_rotation_y(random.random() * 6.414)
        self.send_event('E_ROTATION', mat)
        self.search_timer = global_data.game_mgr.register_logic_timer(self.search_target, interval=10, times=-1, mode=timer.LOGIC)

    def animate_callback(self, *args):
        if self._lock_target:
            self.play_animation('run', loop=1)
        else:
            self.play_animation('idle', loop=1)

    def set_physx_sync_lod(self, model):
        from logic.gcommon.const import PHYSX_SYNC_LOD_DIST, PHYSX_SYNC_LOD_SKIP_FRAMES
        char_ctrl = self.sd.ref_character
        if model and char_ctrl:
            char_ctrl.setRefModel(model)
            char_ctrl.setSyncLodDist(PHYSX_SYNC_LOD_DIST, PHYSX_SYNC_LOD_SKIP_FRAMES)

    def on_pos_changed(self, pos, *arg):
        if G_POS_CHANGE_MGR:
            self.notify_pos_change(pos)
        else:
            self.send_event('E_POSITION', pos)

    def on_rotation_changed(self):
        char_ctrl = self.sd.ref_character
        self.send_event('E_SYNC_MODEL_ROTATION_TO_COL', char_ctrl.getSlope())

    def uninit_character(self):
        char_ctrl = self.sd.ref_character
        if char_ctrl:
            char_ctrl.setPositionChangedCallback(None)
            char_ctrl.setRotationChangedCallback(None)
            char_ctrl.setOnFallCallback(None, 0.0)
        return

    def init_character(self):
        char_ctrl = self.sd.ref_character
        if char_ctrl is None:
            return
        else:
            char_ctrl.setPositionChangedCallback(self._on_pos_changed)
            char_ctrl.setRotationChangedCallback(self._on_rotation_changed)
            char_ctrl.setOnFallCallback(self._on_fall, jump_physic_config.fall_speed_to_jump * NEOX_UNIT_SCALE)
            self.reset_phys_attr()
            return

    def reset_phys_attr(self):
        from ...cdata import state_physic_arg
        stepheight = 0.3 * NEOX_UNIT_SCALE
        max_slope = 75
        padding = state_physic_arg.padding * NEOX_UNIT_SCALE
        added_margin = state_physic_arg.added_margin * NEOX_UNIT_SCALE
        pos_interpolate = state_physic_arg.pos_interpolate
        self._jump_speed = self.robot_data['jump_speed'] * NEOX_UNIT_SCALE
        gravity = self.robot_data['gravity'] * NEOX_UNIT_SCALE
        fall_speed = 50 * NEOX_UNIT_SCALE
        self.y_off = 0.8 * NEOX_UNIT_SCALE
        self.x_off = 0
        character = self.sd.ref_character
        character.setStepHeight(stepheight)
        character.setPadding(padding)
        character.setAddedMargin(added_margin)
        character.setMaxSlope(math.radians(max_slope))
        character.setJumpSpeed(self._jump_speed)
        character.setFallSpeed(fall_speed)
        character.setGravity(gravity * self.sd.ref_gravity_scale)
        character.setXOffset(-self.x_off)
        character.setYOffset(-self.y_off)
        character.setSmoothFactor(pos_interpolate)
        character.enableFollow = False
        character.mask = character.mask & ~collision_const.GROUP_MECHA_BALL
        self.char_size = (
         0.5 * NEOX_UNIT_SCALE, 1.6 * NEOX_UNIT_SCALE)
        self.send_event('E_RECREATE_CHARACTER', self.char_size[0], self.char_size[1], 0.6)

    def on_rotate_by_dir(self, forward):
        forward = math3d.vector(forward)
        forward.y = 0
        rot = math3d.matrix.make_orient(forward, math3d.vector(0, 1, 0))
        self.model.rotation_matrix = rot
        model_rot = math3d.matrix_to_rotation(rot)
        char_ctrl = self.sd.ref_character
        char_ctrl.setCharacterDirection(model_rot)
        self.send_event('E_ACTION_SYNC_FORCE_YAW', rot.yaw)

    def recreate(self, width, height):
        char_ctrl = self.sd.ref_character
        if not char_ctrl:
            return
        pos = char_ctrl.getFootPosition()
        stepheight = char_ctrl.getStepHeight()
        self.send_event('E_RECREATE_CHARACTER', width, height, stepheight)
        self.init_character()
        char_ctrl.setXOffset(-self.x_off)
        char_ctrl.setYOffset(-self.y_off)

    def _on_fall(self):
        pass

    def _on_pos_changed(self, pos, *arg):
        old_model_position = self._pos_cache
        char_ctrl = self.sd.ref_character
        if char_ctrl.verticalVelocity < 0 and old_model_position:
            pos_y = old_model_position.y + self.SLOW_MODEL_POS_SCALE * (pos.y - old_model_position.y)
            pos.y = pos_y
        if G_POS_CHANGE_MGR:
            self.notify_pos_change(pos)
        else:
            self.send_event('E_POSITION', pos)
        self._pos_cache = pos

    def _on_rotation_changed(self):
        pass

    def _move_toward(self, move_dir, force_update=False):
        self._move_direction = move_dir
        self.send_event('E_ACTION_MOVE', move_dir)
        speed = self.cur_speed
        move_dir *= speed
        self.send_event('E_ACTION_SYNC_DIR', move_dir)
        self.set_walk_direction(move_dir)
        mat = math3d.matrix.make_rotation_between(math3d.vector(0, 0, 1), math3d.vector(move_dir.x, 0, move_dir.z))
        self.send_event('E_ROTATION', mat)

    def set_walk_direction(self, move_dir):
        char_ctrl = self.sd.ref_character
        if not char_ctrl:
            return
        self.send_event('E_CHARACTER_WALK', move_dir)

    def tick(self, dt):
        if self._tick_func:
            self._tick_func(dt)
        self.update_lock_sfx()
        self.upload_pos(dt)

    def tick_appear(self, dt):
        self.appear_downcount += dt
        if self.appear_downcount > APPEAR_LAST_TIME:
            self._on_ground()

    def tick_move(self, dt):
        self.tick_move_to(dt)
        self.check_swoop()
        self.checK_jump(dt)

    def tick_jump(self, dt):
        char_ctrl = self.sd.ref_character
        if char_ctrl:
            if char_ctrl.verticalVelocity == 0.0:
                self._check_jump_end += 1
                if self._check_jump_end > 4:
                    self._on_ground()
            else:
                self._check_jump_end = 0
            self.check_swoop()

    def tick_none(self, dt):
        pass

    def tick_swoop(self, dt):
        self.explosion_downcount -= dt
        if self.explosion_downcount <= 0.0:
            self_pos = self._pos_cache
            self.send_event('E_CALL_SYNC_METHOD', 'explosive_robot_explode', ((self_pos.x, self_pos.y, self_pos.z),), True)
            self.on_explosive(False)
            self.state = EXPLOSIVE_ROBOT_STATE_DISABLE
            self._tick_func = self.tick_none

    def tick_move_to(self, dt):
        if self._lock_target:
            l_pos = self._lock_target.ev_g_position()
            m_pos = self._pos_cache
            if l_pos is None or m_pos is None:
                self._to_pos = None
                self.on_lock_target(None)
                self.send_event('E_CALL_SYNC_METHOD', 'explosive_robot_target', (None, ), True)
                return
            if self._lock_target.sd.ref_is_mecha:
                dist = self.attack_dist
            else:
                dist = self.attack_dist_human
            if (l_pos - m_pos).length > dist:
                self._to_pos = None
                self.on_lock_target(None)
                self.send_event('E_CALL_SYNC_METHOD', 'explosive_robot_target', (None, ), True)
                return
            self._refresh_to_pos_tick -= dt
            if self._refresh_to_pos_tick < 0.0:
                self._refresh_to_pos_tick = 0.5
                self._to_pos = l_pos
        if not self._to_pos:
            return
        else:
            char_ctrl = self.sd.ref_character
            if not char_ctrl:
                return
            dt_pos = self._to_pos - char_ctrl.position
            dt_pos.y = 0
            if dt_pos.is_zero or dt_pos.length < 4.0:
                self._to_pos = None
                return
            dt_pos.normalize()
            move_dir = dt_pos
            if math.isnan(move_dir.length):
                return
            self._move_toward(move_dir)
            return

    def check_swoop(self):
        if self._lock_model and self._lock_model.valid and self.model:
            if self._lock_model.has_socket(self.lock_socket_name):
                mat = self._lock_model.get_socket_matrix(self.lock_socket_name, world.SPACE_TYPE_WORLD)
                target_pos = mat.translation
            else:
                target_pos = self._lock_model.center_w
            if not target_pos:
                return
            self_pos = self._pos_cache
            if not self_pos:
                return
            dirction = target_pos - self_pos
            if dirction.length < self.range_charge:
                self.change_swoop_state(dirction, target_pos, self_pos)

    def change_swoop_state(self, dirction, target_pos, self_pos):
        dirction.y = 0.0
        dirction.normalize()
        move_vector = target_pos - self_pos - dirction * NEOX_UNIT_SCALE
        time = move_vector.length / self.range_speed
        char_ctrl = self.sd.ref_character
        gravity = char_ctrl.getGravity()
        extra_vertical_s = 0.5 * gravity * time
        move_vector.normalize()
        speed_vector = move_vector * self.range_speed + math3d.vector(0, 1, 0) * extra_vertical_s
        self.set_walk_direction(speed_vector)
        self._tick_func = self.tick_swoop
        self.state = EXPLOSIVE_ROBOT_STATE_SWOOP
        self.explosion_downcount = time
        self.play_animation('attack')

    def checK_jump(self, dt):
        if not self._lock_target or not self.model:
            return
        mat = self.model.get_socket_matrix(ROBOT_AIM_SOCKET_NAME, world.SPACE_TYPE_WORLD)
        pos = mat.translation
        self._move_direction.y = 0.0
        self._move_direction.normalize()
        result = self.scene.scene_col.hit_by_ray(pos, pos + self._move_direction * CHECK_JUMP_DISTANCE * NEOX_UNIT_SCALE, 0, collision_const.GROUP_STATIC_SHOOTUNIT, collision_const.GROUP_STATIC_SHOOTUNIT, collision.INCLUDE_FILTER, False)
        if result[0]:
            self.set_jump()
            return
        self.jump_check_downcount += dt
        if self.jump_check_downcount > self.CHECK_INTERVAL:
            self.jump_check_downcount -= self.CHECK_INTERVAL
            char_ctrl = self.sd.ref_character
            cur_pos = char_ctrl.position
            if self._save_pos and cur_pos:
                if (self._save_pos - cur_pos).length_sqr < self.CHECK_JUMP_MIN_DISTANCE_SQR and (self._last_jump_pos - cur_pos).length_sqr > self.CHECK_LAST_JUMP_POS_DISTANCE_SQE or self._check_dir_to_jump(cur_pos - self._save_pos):
                    self._last_jump_pos = cur_pos
                    self.set_jump()
            self._save_pos = cur_pos

    def set_jump(self):
        self.state = EXPLOSIVE_ROBOT_STATE_JMUP
        self._vert_zero_speed_time = 0.0
        self._tick_func = self.tick_jump
        char_ctrl = self.sd.ref_character
        char_ctrl.verticalVelocity = self._jump_speed
        char_ctrl.setOnTouchGroundCallback(self._on_ground)
        self.play_animation('attack')

    def _check_dir_to_jump(self, diff):
        pos_dir = math3d.vector(diff.x, 0, diff.z)
        if pos_dir.is_zero:
            return False
        if not self._diff_pre:
            self._diff_pre = pos_dir
            return False
        pos_dir.normalize()
        char_ctrl = self.sd.ref_character
        if not char_ctrl:
            return False
        cha_dir = char_ctrl.getWalkDirection()
        if cha_dir.is_zero:
            return False
        cha_dir.normalize()
        if cha_dir.dot(pos_dir) < DOT_VALUE_TO_JUMP:
            return True
        return False

    def _on_ground(self, *args):
        self.state = EXPLOSIVE_ROBOT_STATE_MOVE
        self._tick_func = self.tick_move
        if self._lock_target:
            self.play_animation('run', loop=1)
        else:
            self.play_animation('idle', loop=1)

    def explosion(self):
        self._explosion_timer = None
        return

    def _move_stop(self, force_stop=False):
        self.send_event('E_ACTION_SYNC_STOP')
        self.send_event('E_ACTION_MOVE_STOP')
        self.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', [bcast.E_ACTION_MOVE_STOP, ()], False)
        self.set_walk_direction(math3d.vector(0, 0, 0))

    def on_lock_target(self, target):
        self._lock_target = target
        if target:
            self._lock_model = self._lock_target.ev_g_model()
            self.need_check_reattach_model = bool(self._lock_target.sd.ref_second_model_dir)
            self.send_event('E_AIM_LOCK_TARGET', self._lock_target.id)
            self.create_lock_sfx()
            self.lock_socket_name = 'fx_buff'
            if self._lock_target.sd.ref_is_mecha:
                self.range_charge = self.mecha_range_charge
            else:
                self.range_charge = self.human_range_charge
            if self.cur_animate == 'idle':
                self.play_animation('run', loop=1)
        else:
            self._lock_model = None
            self.need_check_reattach_model = False
            self._move_stop(True)
            self.send_event('E_AIM_LOCK_TARGET', None)
            if self.lock_sfx_id:
                global_data.sfx_mgr.shutdown_sfx_by_id(self.lock_sfx_id)
                self.lock_sfx_id = None
            if self.lock_sfx:
                global_data.sfx_mgr.shutdown_sfx(self.lock_sfx)
                self.lock_sfx = None
        return

    def create_lock_sfx(self):
        if not self.model:
            return
        if self.lock_sfx_id:
            return
        if self.lock_sfx:
            return

        def create_cb(sfx):
            if self.lock_sfx:
                global_data.sfx_mgr.shutdown_sfx(self.lock_sfx)
            self.lock_sfx = sfx
            self.lock_sfx_id = None
            self.lock_sfx.world_scale = math3d.vector(1.0, 1.0, 1.0)
            self.update_lock_sfx()
            return

        self.lock_sfx_id = global_data.sfx_mgr.create_sfx_on_model(self.robot_data['lock_sfx'], self.model, ROBOT_AIM_SOCKET_NAME, on_create_func=create_cb)

    def update_lock_sfx(self):
        if self.lock_sfx and self.model and self.model.valid and self._lock_model and self._lock_model.valid:
            if self.need_check_reattach_model:
                if not self._lock_model.visible and self._lock_target and self._lock_target.is_valid():
                    self._lock_model = self._lock_target.ev_g_model()
            if self._lock_model.has_socket(self.lock_socket_name):
                mat = self._lock_model.get_socket_matrix(self.lock_socket_name, world.SPACE_TYPE_WORLD)
                pos = mat.translation
            else:
                pos = self._lock_model.center_w
            self.lock_sfx.end_pos = pos

    def play_animation(self, anim, transit_time=-1.0, transit_type=0, init_time=0, loop=2):
        if self.cur_animate == anim:
            return
        if self.model and self.model.valid:
            self.model.play_animation(anim, transit_time, transit_type, init_time, loop)
            self.cur_animate = anim

    def on_explosive(self, is_time_out=True):
        if self.state != EXPLOSIVE_ROBOT_STATE_DISABLE and self.model and self.model.valid:
            self.state = EXPLOSIVE_ROBOT_STATE_DISABLE
            if is_time_out:
                sfx = self.robot_data['sfx']
                scale = self.robot_data['sfx_scale']
            else:
                sfx = self.robot_data['death_sfx']
                scale = self.robot_data['death_sfx_scale']
            scale = math3d.vector(scale, scale, scale)

            def create_cb(sfx):
                sfx.scale = scale

            global_data.sfx_mgr.create_sfx_in_scene(sfx, self.model.position, duration=0.5, on_create_func=create_cb, int_check_type=CREATE_SRC_SIMPLE)
            global_data.sound_mgr.play_sound_optimize('Play_grenade', self.unit_obj, self.model.position, ('grenade', self.robot_data['explosive_sound']))
            self.model.visible = False

    def search_target(self):
        if self._master:
            pos = self.model.position + math3d.vector(0, 0.5 * NEOX_UNIT_SCALE, 0)
            unit_data = global_data.emgr.scene_get_nearest_enemy_unit.emit(self._master, pos, self.active_dist_mecha, self.active_dist_human)
            if unit_data and unit_data[0]:
                lock_target_id = unit_data[0].id
                self.send_event('E_CALL_SYNC_METHOD', 'explosive_robot_target', (lock_target_id,), True)
                global_data.game_mgr.unregister_logic_timer(self.search_timer)
                self.search_timer = None
                return True
        return False

    def upload_pos(self, dt):
        if self._master == global_data.cam_lctarget:
            self.upload_tick -= dt
            if self.upload_tick < 0.0:
                self.upload_tick = 0.2
                model_position = self._pos_cache
                if model_position and model_position != self.old_upload_pos:
                    self.old_upload_pos = model_position
                    self.send_event('E_CALL_SYNC_METHOD', 'update_explosive_robot_position', (global_data.player.id, v3d_to_tp(model_position)), True)

    def is_enemy(self):
        if self._master and global_data.cam_lplayer and not global_data.cam_lplayer.ev_g_is_campmate(self._master.ev_g_camp_id()):
            return True
        return False

    def destroy(self):
        if self.search_timer:
            global_data.game_mgr.unregister_logic_timer(self.search_timer)
            self.search_timer = None
        self.on_lock_target(None)
        self.uninit_character()
        self._tick_func = dummy_cb
        super(ComExplosiveRobotDriver, self).destroy()
        return